"""Gera config_audio_ep01.json: eventos de SFX manuais + 'pop' automático em cada etiqueta."""
import json
v = json.load(open('config_ep01.json', encoding='utf-8'))
ev = [
    # [efeito, tempo(s), volume, duração_máx]
    ['boing', 0.35, 0.3], ['whoosh', 2.3, 0.35],
    ['whoosh', 5.95, 0.5], ['metal_hit', 6.95, 0.7], ['hammer', 7.25, 0.4],
    ['whoosh2', 9.2, 0.35], ['big_impact', 9.85, 0.35, 1.5],
    ['creak', 10.2, 0.3, 2.3], ['fail', 11.15, 0.45],
    ['creak', 12.85, 0.3, 1.7], ['boing', 14.05, 0.45],
    ['whoosh', 14.65, 0.5], ['whoosh', 15.95, 0.45], ['metal_hit', 16.55, 0.6],
    ['whoosh2', 17.4, 0.35], ['plate_drop', 17.9, 0.5],
    ['whoosh', 19.2, 0.4], ['metal_hit', 19.72, 0.55], ['whoosh', 19.85, 0.4], ['metal_hit', 20.37, 0.55],
    ['metal_hit', 22.5, 0.7], ['gear', 22.6, 0.6],
    ['bell', 27.05, 0.5], ['boing', 27.1, 0.35],
    ['whoosh2', 27.9, 0.35], ['big_impact', 28.45, 0.3, 1.5], ['creak', 30.5, 0.3, 2.4], ['fail', 32.42, 0.4],
    ['whoosh', 33.05, 0.4],
    ['plate_drop', 34.3, 0.45], ['plate_drop', 34.6, 0.45], ['plate_drop', 34.9, 0.45], ['plate_drop', 35.2, 0.45],
    ['plate_drop', 35.5, 0.45], ['plate_drop', 35.8, 0.45], ['plate_drop', 36.1, 0.45],
    ['metal_hit', 37.6, 0.6],
    ['hammer', 38.0, 0.3], ['hammer', 38.25, 0.3], ['hammer', 38.5, 0.3], ['hammer', 38.75, 0.3], ['hammer', 39.0, 0.3],
    ['fail', 38.15, 0.45],
    ['weld', 40.3, 0.7, 2.85], ['weld2', 40.4, 0.45],
    ['scanner', 43.3, 0.5, 1.4], ['win', 44.1, 0.3],
    ['whoosh', 44.75, 0.35], ['fail', 46.9, 0.35],
    ['gear', 47.95, 0.5], ['metal_hit', 48.45, 0.4],
    ['truck', 48.8, 0.35, 2.3], ['whoosh', 50.85, 0.4],
    ['motor', 51.4, 0.45, 7.3], ['beeps', 55.8, 0.18, 2.5],
    ['deep_impact', 58.6, 0.5, 1.6], ['metal_hit', 58.68, 0.8],
    ['cheer', 59.45, 0.22, 4.0], ['bell', 59.5, 0.5],
    ['win', 63.25, 0.45], ['win', 65.2, 0.45],
]
for p in v['pills'] + [b for b in v['blocks'] if b['t_in'] > 1]:
    ev.append(['pop', p['t_in'], 0.55])
ev.sort(key=lambda e: e[1])
cfg = {"narration": "audio/narracao_tight.wav", "music": "assets/music/feeling_happy_mixkit5.mp3",
       "music_vol": 0.13, "sfx_vol": 0.8, "sfx_dir": "assets/sfx", "duration": 67.6,
       "out": "build/mix.wav", "sfx": ev}
json.dump(cfg, open('config_audio_ep01.json', 'w'), indent=1)
print(len(ev), 'eventos')
