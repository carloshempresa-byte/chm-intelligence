"""Split-layout streamer Short: facecam on top, gameplay below, headline box at the seam,
big word-by-word burned captions (active word highlighted). Original audio only.

usage: python3 -I split_short.py spec.json
spec: {"out", "work", "fontsdir", "font", "words": {key: [[start,end,word],...]},
       "fix": {"wrong": "right"}, "censor": true,
       "segments": [{"key", "src", "parts": [[s,e],...], "face": [x,y,w,h], "game": [x,y,w,h],
                     "headline": "TEXT"}]}
"""
import json, math, os, re, subprocess, sys

W, H, FACE_H = 1080, 1920, 810
GAME_H = H - FACE_H
spec = json.load(open(sys.argv[1]))
work = spec['work']; os.makedirs(work, exist_ok=True)


def run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode:
        sys.exit(r.stderr[-2000:])
    return r


def probe(src):
    o = run(['ffprobe', '-v', 'error', '-select_streams', 'v:0', '-show_entries', 'stream=width,height',
             '-of', 'csv=p=0', src]).stdout.strip().split(',')
    return int(o[0]), int(o[1])


def cover(rect, tw, th):
    x, y, w, h = rect
    s = max(tw / w, th / h)
    sw, sh = math.ceil(w * s / 2) * 2, math.ceil(h * s / 2) * 2
    return f"crop={w}:{h}:{x}:{y},scale={sw}:{sh}:flags=lanczos,crop={tw}:{th}"


# 1) render every part in the split layout
parts, t = [], 0.0
for si, seg in enumerate(spec['segments']):
    for pi, (s, e) in enumerate(seg['parts']):
        out = f"{work}/p{si}_{pi}.mkv"
        vf = (f"[0:v]fps=30,split[a][b];[a]{cover(seg['face'], W, FACE_H)}[f];"
              f"[b]{cover(seg['game'], W, GAME_H)}[g];[f][g]vstack,setsar=1,"
              f"eq=contrast=1.03:saturation=1.06,format=yuv420p[v]")
        run(['ffmpeg', '-v', 'error', '-y', '-ss', str(s), '-to', str(e), '-i', seg['src'], '-filter_complex', vf,
             '-map', '[v]', '-map', '0:a', '-af', 'loudnorm=I=-16:TP=-2:LRA=15,aresample=48000', '-ac', '2',
             '-c:v', 'libx264', '-crf', '17', '-preset', 'medium', '-c:a', 'pcm_s16le', out])
        d = float(run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', out]).stdout)
        parts.append(dict(file=out, seg=si, s=s, e=e, t0=t, dur=d))
        t += d
total = t

# 2) concat
n = len(parts)
inputs = sum([['-i', p['file']] for p in parts], [])
fc = ''.join(f'[{i}:v][{i}:a]' for i in range(n)) + f'concat=n={n}:v=1:a=1[v][a]'
run(['ffmpeg', '-v', 'error', '-y', *inputs, '-filter_complex', fc, '-map', '[v]', '-map', '[a]',
     '-c:v', 'libx264', '-crf', '17', '-c:a', 'pcm_s16le', f'{work}/cat.mkv'])

# 3) ASS: headline per segment + word captions
CENSOR = {r'\bfuck': 'F*CK', r'\bshit': 'SH*T', r'\bbitch': 'B*TCH', r'\bnigga': 'N*GGA', r'\bporra': 'P*RRA',
          r'\bcaralho': 'C*RALHO', r'\bmerda': 'M*RDA', r'\bputa': 'P*TA', r'\bfoder': 'F*DER', r'\bfodendo': 'F*DENDO'}


def clean(w):
    for a, b in spec.get('fix', {}).items():
        w = w.replace(a, b)
    w = w.upper()
    if spec.get('censor', True):
        for pat, rep in CENSOR.items():
            w = re.sub(pat, rep, w, flags=re.I)
    return w.replace('{', '').replace('}', '')


def ts(x):
    x = max(0, x); h = int(x // 3600); m = int(x % 3600 // 60); s = x % 60
    return f'{h}:{m:02d}:{s:05.2f}'


font = spec.get('font', 'Archivo Black')
ass = [
    '[Script Info]', 'ScriptType: v4.00+', f'PlayResX: {W}', f'PlayResY: {H}', 'WrapStyle: 0', '',
    '[V4+ Styles]',
    'Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, '
    'Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding',
    f'Style: Head,{font},60,&H00000000,&H00000000,&H00FFFFFF,&H00FFFFFF,0,0,0,0,100,100,0,0,3,18,0,5,60,60,0,1',
    f'Style: Cap,{font},84,&H00FFFFFF,&H00FFFFFF,&H00000000,&H96000000,0,0,0,0,100,100,1,0,1,7,4,5,50,50,0,1',
    '', '[Events]', 'Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text']

# headline: whole span of each segment
for si, seg in enumerate(spec['segments']):
    ps = [p for p in parts if p['seg'] == si]
    a, b = ps[0]['t0'], ps[-1]['t0'] + ps[-1]['dur']
    ass.append(f"Dialogue: 1,{ts(a)},{ts(b)},Head,,0,0,0,,{{\\pos(540,{FACE_H})}}{seg['headline']}")

# words mapped to the output timeline
for p in parts:
    seg = spec['segments'][p['seg']]
    ws = [w for w in spec['words'].get(seg['key'], []) if p['s'] <= w[0] < p['e'] - 0.05 and w[2].strip()]
    out = [[w[0] - p['s'] + p['t0'], min(w[1], p['e']) - p['s'] + p['t0'], clean(w[2])] for w in ws]
    out = [w for w in out if w[2]]
    chunks, cur = [], []
    for w in out:
        if cur and (len(cur) >= 3 or w[0] - cur[-1][1] > 0.6 or len(' '.join(x[2] for x in cur + [w])) > 18):
            chunks.append(cur); cur = []
        cur.append(w)
    if cur:
        chunks.append(cur)
    end_part = p['t0'] + p['dur']
    for ci, ch in enumerate(chunks):
        nxt = chunks[ci + 1][0][0] if ci + 1 < len(chunks) else end_part
        for wi, w in enumerate(ch):
            st = w[0]
            en = ch[wi + 1][0] if wi + 1 < len(ch) else min(max(w[1] + 0.35, w[0] + 0.3), nxt, end_part)
            if en <= st:
                continue
            txt = ' '.join((f'{{\\c&H00F0FF&}}{x[2]}{{\\c&HFFFFFF&}}' if xi == wi else x[2])
                           for xi, x in enumerate(ch))
            ass.append(f"Dialogue: 2,{ts(st)},{ts(en)},Cap,,0,0,0,,{{\\pos(540,1560)}}{txt}")

open(f'{work}/subs.ass', 'w').write('\n'.join(ass) + '\n')

# 4) burn subtitles + final loudness (two-pass) + fade
j = run(['ffmpeg', '-hide_banner', '-i', f'{work}/cat.mkv', '-af', 'loudnorm=I=-14:TP=-1.5:LRA=11:print_format=json',
         '-f', 'null', '-']).stderr
m = json.loads(j[j.rindex('{'):j.rindex('}') + 1])
ln = (f"loudnorm=I=-14:TP=-1.5:LRA=11:measured_I={m['input_i']}:measured_TP={m['input_tp']}:"
      f"measured_LRA={m['input_lra']}:measured_thresh={m['input_thresh']}:offset={m['target_offset']}:linear=true")
fd = max(0, total - 1.2)
run(['ffmpeg', '-v', 'error', '-y', '-i', f'{work}/cat.mkv',
     '-vf', f"ass={work}/subs.ass:fontsdir={spec['fontsdir']}",
     '-af', f'{ln},aresample=48000,afade=t=out:st={fd:.2f}:d=1.2',
     '-c:v', 'libx264', '-crf', '18', '-preset', 'medium', '-profile:v', 'high', '-pix_fmt', 'yuv420p',
     '-c:a', 'aac', '-b:a', '256k', '-movflags', '+faststart', spec['out']])
print(json.dumps({'out': spec['out'], 'duration': round(total, 2),
                  'cuts': [round(p['t0'], 2) for p in parts]}))
