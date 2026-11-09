"""Build the ranking Short from a JSON config.

usage: python3 -I build.py <config.json> [--stage clips|compose|all|post] [--draft]

Pipeline:
  0. preflight (post_kit.py + rules.json): title, hashtags, clip sources (official/broadcast warning)
     and music licence. A music that is not royalty-free from an allowed library ABORTS the build.
  1. every clip -> trimmed, 30fps, zoomed ~1.1x, cropped to the video window,
     mirrored on alternate clips, light colour/contrast grade, NO audio (original audio is never used)
  2. overlays.py renders title + ranking-list layers
  3. compose: black 1080x1920 canvas + clip window + title + animated list
  4. audio: royalty-free track (starts on an energetic part at 0s) + whoosh on every cut,
     fade-out at the end, gain + limiter to -14 LUFS / -1.5 dBTP
  5. post_kit writes post.txt (title + description) and checklist.txt next to the output video
     (--stage post regenerates only these two files)
Rules: the-top-ones/REGRAS.md
"""
import json, math, os, subprocess, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import post_kit  # noqa: E402  (tools dir, not the downloaded-clip dirs)

cfg_path = sys.argv[1]
stage = 'all'
if '--stage' in sys.argv:
    stage = sys.argv[sys.argv.index('--stage') + 1]
draft = '--draft' in sys.argv
cfg = json.load(open(cfg_path))

pre = post_kit.preflight(cfg)
pre.print('preflight')
if pre.errors:
    sys.exit('preflight falhou (veja ERRO acima); nada foi renderizado')
if stage == 'post':
    post_txt, checklist_txt, _ = post_kit.write_outputs(cfg, cfg['output'])
    print('wrote', post_txt, '\nwrote', checklist_txt)
    sys.exit(0)

B = cfg['build_dir']
os.makedirs(B, exist_ok=True)
FPS = 30
W, H = 1080, 1920
VX, VY, VW, VH = 0, cfg['layout']['video_y'], 1080, cfg['layout']['video_h']


def run(cmd, **kw):
    print('+', ' '.join(cmd) if len(' '.join(cmd)) < 600 else ' '.join(cmd)[:600] + ' ...', flush=True)
    r = subprocess.run(cmd, **kw)
    if r.returncode != 0:
        sys.exit(f'command failed ({r.returncode})')
    return r


def probe(path):
    out = subprocess.run(['ffprobe', '-v', 'error', '-select_streams', 'v:0', '-show_entries',
                          'stream=width,height', '-of', 'json', path], capture_output=True, text=True).stdout
    s = json.loads(out)['streams'][0]
    return s['width'], s['height']


def lerp_expr(keys, var='t'):
    """piecewise-linear ffmpeg expression through [(t, v), ...] (clamped at the ends)"""
    keys = sorted(keys)
    if len(keys) == 1:
        return f'{keys[0][1]:.5f}'
    expr = f'{keys[-1][1]:.5f}'
    for (t0, v0), (t1, v1) in reversed(list(zip(keys[:-1], keys[1:]))):
        seg = f'({v0:.5f}+({v1 - v0:.5f})*({var}-{t0:.4f})/{max(t1 - t0, 1e-3):.4f})'
        expr = f'if(lt({var},{t1:.4f}),{seg},{expr})'
    return f'if(lt({var},{keys[0][0]:.4f}),{keys[0][1]:.5f},{expr})'


def clip_filter(c, idx):
    sw, sh = probe(c['src'])
    cx, cy, cw, ch = c.get('src_crop', [0, 0, sw, sh])
    zoom = c.get('zoom', cfg['zoom'])
    s = max(VW / cw, VH / ch) * zoom
    tw, th = int(math.ceil(cw * s / 2) * 2), int(math.ceil(ch * s / 2) * 2)
    fx = c.get('focus_x', 0.5)
    fy = c.get('focus_y', 0.5)
    # keyframed focus (time is relative to the trimmed clip)
    xk = c.get('focus_x_keys') or [[0, fx]]
    yk = c.get('focus_y_keys') or [[0, fy]]
    xexpr = f"({tw - VW})*({lerp_expr(xk)})"
    yexpr = f"({th - VH})*({lerp_expr(yk)})"
    g = dict(cfg['grade']); g.update(c.get('grade', {}))
    f = [f'fps={FPS}', f'crop={cw}:{ch}:{cx}:{cy}', f'scale={tw}:{th}:flags=lanczos',
         f"crop={VW}:{VH}:x='{xexpr}':y='{yexpr}'"]
    if c.get('flip'):
        f.append('hflip')
    f += [f"eq=contrast={g['contrast']}:brightness={g['brightness']}:saturation={g['saturation']}:gamma={g.get('gamma', 1.0)}",
          'unsharp=5:5:0.35:5:5:0.0', 'setsar=1', 'format=yuv420p']
    return ','.join(f)


clips = cfg['clips']  # in playback order
starts = []
t = 0.0
for c in clips:
    c['frames'] = int(round((c['end'] - c['start']) * FPS))
    starts.append(t)
    t += c['frames'] / FPS
TOTAL = t
print(f'total duration {TOTAL:.2f}s, cuts at', [round(s, 2) for s in starts])

# ---------------------------------------------------------------- clips
if stage in ('clips', 'all'):
    lst = []
    for i, c in enumerate(clips):
        out = f'{B}/clip_{i}.mp4'
        run(['ffmpeg', '-v', 'error', '-y', '-ss', f"{c['start']:.3f}", '-i', c['src'], '-an',
             '-vf', clip_filter(c, i), '-frames:v', str(c['frames']), '-r', str(FPS),
             '-c:v', 'libx264', '-preset', 'veryfast' if draft else 'medium', '-crf', '14', out])
        lst.append(f"file '{out}'")
    open(f'{B}/concat.txt', 'w').write('\n'.join(lst) + '\n')
    run(['ffmpeg', '-v', 'error', '-y', '-f', 'concat', '-safe', '0', '-i', f'{B}/concat.txt', '-c', 'copy',
         f'{B}/window.mp4'])

# ---------------------------------------------------------------- overlays
ov = f'{B}/ov'
if stage in ('compose', 'all'):
    ocfg = {'font': cfg['font'], 'blue': cfg['blue'], 'title': cfg['title'], 'layout': cfg['layout'],
            'order': [c['rank'] for c in clips], 'names': {str(c['rank']): c['name'] for c in clips}}
    json.dump(ocfg, open(f'{B}/overlay_cfg.json', 'w'))
    run(['python3', '-I', os.path.join(os.path.dirname(os.path.abspath(__file__)), 'overlays.py'),
         f'{B}/overlay_cfg.json', ov])
    layout = json.load(open(f'{ov}/layout.json'))

    # ------------------------------------------------------------ audio
    a = cfg['audio']
    whoosh_times = [s - a['whoosh_peak'] for s in starts[1:]]
    inputs = ['-ss', f"{a['music_offset']:.3f}", '-t', f'{TOTAL + 0.5:.3f}', '-i', a['music']]
    for _ in whoosh_times:
        inputs += ['-i', a['whoosh']]
    fc = [f"[0:a]aresample=48000,atrim=0:{TOTAL:.3f},asetpts=PTS-STARTPTS,"
          f"afade=t=out:st={TOTAL - a['fade_out']:.3f}:d={a['fade_out']:.3f}[m]"]
    mix = ['[m]']
    for i, wt in enumerate(whoosh_times):
        d = max(0, int(round(wt * 1000)))
        fc.append(f"[{i + 1}:a]aresample=48000,volume={a['whoosh_gain_db']}dB,adelay={d}|{d}[w{i}]")
        mix.append(f'[w{i}]')
    fc.append(f"{''.join(mix)}amix=inputs={len(mix)}:normalize=0:duration=first[mx]")
    run(['ffmpeg', '-v', 'error', '-y', *inputs, '-filter_complex', ';'.join(fc), '-map', '[mx]',
         '-c:a', 'pcm_s24le', '-ar', '48000', '-ac', '2', f'{B}/mix_raw.wav'])
    # loudness: gain + peak limiter, iterated until integrated loudness hits the target
    def measure(path):
        r = subprocess.run(['ffmpeg', '-hide_banner', '-i', path, '-af', 'ebur128=peak=true', '-f', 'null', '-'],
                           capture_output=True, text=True).stderr
        summ = r[r.rindex('Summary:'):]
        I = float(summ.split('I:')[1].split('LUFS')[0])
        tp = float(summ.split('Peak:')[1].split('dBFS')[0])
        return I, tp
    I0, tp0 = measure(f'{B}/mix_raw.wav')
    print(f'raw mix: {I0} LUFS, true peak {tp0} dBFS')
    gain = a['lufs'] - I0
    lim = 10 ** ((a['true_peak'] - 0.5) / 20)
    for it in range(4):
        run(['ffmpeg', '-v', 'error', '-y', '-i', f'{B}/mix_raw.wav', '-af',
             f"volume={gain:.2f}dB,alimiter=limit={lim:.4f}:attack=2:release=60:level=false,aresample=48000",
             '-c:a', 'pcm_s24le', f'{B}/mix.wav'])
        I, tp = measure(f'{B}/mix.wav')
        print(f'  iter {it}: gain {gain:+.2f} dB -> {I} LUFS, TP {tp} dBFS')
        if abs(I - a['lufs']) <= 0.15:
            break
        gain += a['lufs'] - I

    # ------------------------------------------------------------ video compose
    N = len(clips)
    vin = ['-f', 'lavfi', '-i', f'color=c=black:s={W}x{H}:r={FPS}:d={TOTAL:.3f}',
           '-i', f'{B}/window.mp4',
           '-loop', '1', '-framerate', str(FPS), '-i', f'{ov}/title.png']
    for k in range(N):
        vin += ['-loop', '1', '-framerate', str(FPS), '-i', f'{ov}/list_base_{k}.png']
    for k in range(N):
        vin += ['-loop', '1', '-framerate', str(FPS), '-i', f'{ov}/name_{k}.png']
    vin += ['-i', f'{B}/mix.wav']
    fc = [f'[0:v][1:v]overlay={VX}:{VY}:shortest=1[v0]', '[v0][2:v]overlay=0:0[v1]']
    cur = 'v1'
    ends = starts[1:] + [TOTAL + 1]
    for k in range(N):
        t0, t1 = starts[k], ends[k]
        fc.append(f"[{cur}][{3 + k}:v]overlay=0:0:enable='between(t,{t0:.4f},{t1 - 0.0005:.4f})'[b{k}]")
        cur = f'b{k}'
    for k in range(N):
        t0, t1 = starts[k], ends[k]
        row = layout['rows'][str(k)]
        fc.append(f"[{3 + N + k}:v]format=rgba,fade=t=in:st={t0:.4f}:d=0.22:alpha=1[n{k}]")
        xe = f"{row['x']}+40*pow(1-min(1\\,max(0\\,(t-{t0:.4f})/0.30))\\,2)"
        fc.append(f"[{cur}][n{k}]overlay=x='{xe}':y={row['y']}:enable='between(t,{t0:.4f},{t1 - 0.0005:.4f})'[c{k}]")
        cur = f'c{k}'
    fc.append(f'[{cur}]format=yuv420p[vout]')
    out = cfg['output']
    enc = ['-c:v', 'libx264', '-preset', 'veryfast' if draft else 'slow', '-crf', '20' if draft else '17',
           '-profile:v', 'high', '-level', '4.2', '-pix_fmt', 'yuv420p', '-r', str(FPS),
           '-g', str(FPS * 2), '-bf', '2', '-movflags', '+faststart']
    run(['ffmpeg', '-v', 'error', '-y', *vin, '-filter_complex', ';'.join(fc), '-map', '[vout]',
         '-map', f'{3 + 2 * N}:a', *enc, '-c:a', 'aac', '-b:a', '192k', '-ar', '48000', '-ac', '2',
         '-t', f'{TOTAL:.3f}', out])
    json.dump({'starts': starts, 'total': TOTAL, 'order': [c['rank'] for c in clips]},
              open(f'{B}/timeline.json', 'w'), indent=1)
    print('wrote', out)
    post_txt, checklist_txt, rep = post_kit.write_outputs(cfg, out)
    print('wrote', post_txt, '\nwrote', checklist_txt)
