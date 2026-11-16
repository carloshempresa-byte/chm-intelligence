"""Mixagem: narração + efeitos (Mixkit) + música de fundo baixinha, com ducking leve.
Uso: python3 mix_audio.py <config_audio.json>"""
import json, subprocess, sys, os

cfg = json.load(open(sys.argv[1], encoding='utf-8'))
BASE = os.path.dirname(os.path.abspath(sys.argv[1]))
P = lambda p: p if os.path.isabs(p) else os.path.join(BASE, p)
DUR = cfg['duration']

inputs = ['-i', P(cfg['narration']), '-stream_loop', '-1', '-i', P(cfg['music'])]
filters = []
labels = []
# efeitos: [arquivo, tempo, volume, (duração máx)]
for n, ev in enumerate(cfg['sfx']):
    f, t, vol = ev[0], ev[1], ev[2]
    dmax = ev[3] if len(ev) > 3 else None
    inputs += ['-i', P(os.path.join(cfg['sfx_dir'], f + '.mp3'))]
    idx = 2 + n
    chain = f'[{idx}:a]aformat=sample_rates=48000:channel_layouts=stereo'
    if dmax:
        chain += f',atrim=0:{dmax},afade=t=out:st={max(0, dmax - 0.25)}:d=0.25'
    chain += f',volume={vol},adelay={int(t * 1000)}|{int(t * 1000)}[s{n}]'
    filters.append(chain)
    labels.append(f'[s{n}]')
filters.append(f'[0:a]aformat=sample_rates=48000:channel_layouts=stereo,volume=1.0,apad=whole_dur={DUR}[nar]')
filters.append(f'[1:a]aformat=sample_rates=48000:channel_layouts=stereo,atrim=0:{DUR},volume={cfg["music_vol"]},'
               f'afade=t=in:d=0.5,afade=t=out:st={DUR - 2.0}:d=2.0[mus]')
filters.append('[nar]asplit=2[nar1][nar2]')
filters.append('[mus][nar2]sidechaincompress=threshold=0.05:ratio=4:attack=20:release=300[musd]')
filters.append(''.join(labels) + f'amix=inputs={len(labels)}:normalize=0,volume={cfg["sfx_vol"]}[fx]')
filters.append(f'[nar1][musd][fx]amix=inputs=3:normalize=0,atrim=0:{DUR},alimiter=limit=0.95,loudnorm=I=-14:TP=-1.5:LRA=9[out]')
cmd = ['ffmpeg', '-y', '-loglevel', 'error'] + inputs + ['-filter_complex', ';'.join(filters), '-map', '[out]',
                                                        '-ar', '48000', '-c:a', 'pcm_s16le', P(cfg['out'])]
subprocess.run(cmd, check=True)
print('ok', cfg['out'])
