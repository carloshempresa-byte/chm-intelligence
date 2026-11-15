"""Gera config_ep02.json (legendas/etiquetas/títulos) e config_audio_ep02.json (SFX + música).
Rodar da pasta piloto-ep02. Tempos amarrados a audio/narracao_tight.json."""
import json

END = 64.6
A = '../piloto-ep01/assets/'

pills = [
    # gancho
    dict(text='5 MESES', anchor='a_cal', t_in=0.12, t_out=1.4, off=[-90, 330], style='yellow', size=80),
    dict(text='PORTO', anchor='a_porto', t_in=1.5, t_out=2.55, off=[-170, 90], style='blue', size=44),
    dict(text='OBRA', anchor='a_obra', t_in=1.6, t_out=2.55, off=[170, -60], style='white', size=44),
    dict(text='2 MESES', anchor='a_token', t_in=1.5, t_out=2.55, off=[190, 120], style='yellow', size=80, line=False),
    dict(text='320 t', anchor='a_drum', t_in=4.17, t_out=7.35, off=[-40, -330], style='red', size=90),
    dict(text='75 m', anchor='a_trena', t_in=6.2, t_out=7.4, off=[230, 160], style='yellow', size=90),
    # o drum
    dict(text='DRUM', anchor='a_ghost', t_in=8.09, t_out=12.15, off=[0, -330], style='yellow', size=80),
    dict(text='= BALÃO DE VAPOR', anchor='a_ghost', t_in=8.57, t_out=12.15, off=[0, -200], style='white', size=54, line=False),
    dict(text='NO TOPO', anchor='a_ghost', t_in=11.55, t_out=12.15, off=[0, 260], style='cyan', size=50, line=False),
    dict(text='ÁGUA', anchor='a_agua', t_in=12.48, t_out=13.95, off=[60, 300], style='blue', size=64),
    dict(text='VAPOR', anchor='a_vapor', t_in=12.9, t_out=13.95, off=[0, -320], style='white', size=64),
    dict(text='75 m = 25 ANDARES', anchor='a_predio', t_in=15.0, t_out=16.8, off=[-230, -170], style='yellow', size=60),
    # estrada
    dict(text='2 MESES', anchor='a_carreta', t_in=18.82, t_out=21.25, off=[0, -330], style='yellow', size=80),
    dict(text='CAMINHÃO ESPECIAL', anchor='a_carreta', t_in=20.19, t_out=21.25, off=[0, -200], style='white', size=54, line=False),
    # um guindaste
    dict(text='GUINDASTE 700 t', anchor='a_gA', t_in=22.75, t_out=23.65, off=[160, -260], style='yellow', size=62),
    dict(text='+ ALTURA = – CAPACIDADE', anchor='a_barA', t_in=26.3, t_out=31.2, off=[300, -170], style='white', size=48),
    dict(text='UM SÓ NÃO DÁ', anchor='a_gA', t_in=30.07, t_out=31.2, off=[200, -300], style='red', size=64),
    # dois guindastes
    dict(text='UM EM CADA PONTA', anchor='a_drum_ponta', t_in=34.42, t_out=35.3, off=[-120, -300], style='white', size=54),
    dict(text='NA HORIZONTAL', anchor='a_drum', t_in=35.57, t_out=36.55, off=[0, -300], style='yellow', size=62),
    dict(text='CABO DE AÇO', anchor='a_cabo', t_in=37.13, t_out=38.95, off=[180, -320], style='white', size=60),
    dict(text='= UMA PERNA', anchor='a_perna', t_in=38.29, t_out=38.95, off=[-230, 230], style='yellow', size=66),
    # desnível
    dict(text='DESNÍVEL', anchor='a_drum', t_in=41.66, t_out=43.55, off=[-200, -330], style='red', size=66),
    dict(text='SOBRECARGA', anchor='a_seta', t_in=42.6, t_out=43.55, off=[-80, -220], style='red', size=58),
    # planejamento
    dict(text='5 MESES', anchor='a_cal', t_in=45.1, t_out=47.0, off=[-120, -380], style='yellow', size=84),
    dict(text='PLANO DE IÇAMENTO', anchor='a_cal', t_in=45.77, t_out=47.0, off=[-120, -240], style='white', size=52, line=False),
    # no dia
    dict(text='JUNTOS E DEVAGAR', anchor='a_drum', t_in=48.03, t_out=51.15, off=[0, -300], style='yellow', size=60),
    dict(text='SINALEIRO', anchor='a_carlin', t_in=50.53, t_out=51.15, off=[160, -170], style='white', size=54),
    # topo
    dict(text='TETO ABERTO', anchor='a_topo', t_in=51.87, t_out=53.3, off=[0, -330], style='white', size=60),
    dict(text='75 m', anchor='a_drum', t_in=53.37, t_out=54.9, off=[0, -280], style='yellow', size=84),
    dict(text='NO LUGAR!', anchor='a_drum', t_in=55.0, t_out=56.4, off=[0, -280], style='green', size=66),
    dict(text='TETO FECHADO', anchor='a_topo', t_in=56.5, t_out=57.2, off=[0, -330], style='white', size=60),
    dict(text='DRUM MONTADO', anchor='a_drum', t_in=57.7, t_out=59.1, off=[0, 300], style='red', size=60),
]
blocks = [
    dict(text='EP. 2', pos=[540, 200], t_in=0.0, t_out=3.6, style='orange', size=44),
    dict(text='O DRUM', pos=[540, 300], t_in=0.05, t_out=3.6, style='yellow', size=64),
    dict(text='A MAIOR CALDEIRA DE RECUPERAÇÃO DO MUNDO', pos=[540, 395], t_in=0.1, t_out=3.6, style='white', size=32),
    dict(text='RESOLVIDO?', pos=[540, 480], t_in=24.17, t_out=25.0, style='white', size=70),
    dict(text='NÃO!', pos=[540, 480], t_in=25.01, t_out=25.6, style='red', size=130),
    dict(text='2 × 700 t', pos=[540, 330], t_in=32.15, t_out=35.3, style='yellow', size=90),
    dict(text='NÃO DÁ PRA IMPROVISAR', pos=[540, 420], t_in=43.6, t_out=44.82, style='white', size=52),
    dict(text='PARABÉNS!', pos=[540, 330], t_in=57.24, t_out=59.1, style='yellow', size=96),
    dict(text='SABIA? COMENTE', pos=[540, 250], t_in=59.12, t_out=END, style='white', size=46),
    dict(text='ENGENHEIRO', pos=[540, 360], t_in=60.58, t_out=END, style='green', size=84),
    dict(text='NÃO SABIA? COMENTE', pos=[540, 510], t_in=61.23, t_out=END, style='white', size=46),
    dict(text='ESTAGIÁRIO', pos=[540, 620], t_in=62.52, t_out=END, style='orange', size=84),
]
hl = ['5 MESES', '2 MESES', '320 TONELADAS', '75 METROS', '25 ANDARES', '700 TONELADAS', 'DRUM', 'BALÃO', 'VAPOR', 'ÁGUA',
      'CAMINHÃO', 'ESPECIAL', 'GUINDASTE', 'GUINDASTES', 'CAPACIDADE', 'DOIS', 'HORIZONTAL', 'PERNA', 'INCLINA', 'IMPROVISAR',
      'PLANEJANDO', 'PLANEJAMENTO', 'JUNTOS', 'DEVAGAR', 'SINALEIRO', 'TETO', 'ABERTO', 'FECHADO', 'PARABÉNS',
      'ENGENHEIRO', 'ESTAGIÁRIO', 'NÃO']
cfg = dict(font=A + 'fonts/Montserrat.ttf', words='audio/narracao_tight.json', anchors='build/anchors.json',
           frames='build/frames', n_frames=int(round(END * 30)) + 1, out_video='build/video_sem_audio.mp4',
           caption_y=1330, highlight=hl, pills=pills, blocks=blocks)
json.dump(cfg, open('config_ep02.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)

ev = [
    # gancho: calendário, mapa, drum, trena
    ['whoosh2', 0.05, 0.3], ['pop2', 0.17, 0.35], ['pop2', 0.39, 0.35], ['pop2', 0.61, 0.35], ['pop2', 0.83, 0.35], ['pop2', 1.05, 0.35],
    ['whoosh', 1.42, 0.45], ['truck', 1.55, 0.25, 1.0],
    ['whoosh', 2.56, 0.45], ['metal_hit', 4.2, 0.35], ['boing', 4.25, 0.3],
    ['whistle_fall', 5.75, 0.2, 1.2], ['whoosh2', 6.0, 0.4], ['boing', 6.78, 0.35],
    # drum, corte, prédio
    ['whoosh', 7.4, 0.45], ['bell', 8.1, 0.3], ['whoosh2', 12.18, 0.4], ['pop', 12.5, 0.3], ['pop', 12.9, 0.3],
    ['whoosh', 13.98, 0.4]] + [['pop2', 14.1 + i * 0.13, 0.22] for i in range(12)] + [
    ['boing', 15.7, 0.3],
    # estrada
    ['whoosh', 16.82, 0.4], ['truck', 16.9, 0.4, 4.3], ['whoosh2', 17.6, 0.2], ['whoosh2', 19.3, 0.2],
    # um guindaste
    ['whoosh', 21.3, 0.45], ['motor', 21.35, 0.4, 1.6], ['big_impact', 22.15, 0.3, 1.2], ['metal_hit', 22.2, 0.5],
    ['bell', 24.2, 0.3], ['fail', 25.03, 0.5],
    ['motor', 25.9, 0.35, 3.6], ['creak', 27.8, 0.3, 2.2], ['beeps', 29.0, 0.22, 2.2], ['creak', 29.6, 0.35, 1.6],
    ['fail', 30.1, 0.35],
    # dois guindastes
    ['whoosh', 31.28, 0.45], ['motor', 31.4, 0.4, 1.4], ['big_impact', 32.45, 0.25, 1.2], ['metal_hit', 34.45, 0.55],
    ['metal_hit', 34.6, 0.5], ['motor', 35.5, 0.3, 1.0], ['whoosh2', 36.58, 0.35], ['boing', 38.35, 0.35],
    # desnível
    ['whoosh', 39.02, 0.4], ['motor', 39.1, 0.3, 2.6], ['creak', 40.6, 0.35, 2.4], ['big_impact', 42.0, 0.3, 1.2],
    ['fail', 42.25, 0.45], ['creak', 42.4, 0.3, 1.2], ['boing', 42.9, 0.3],
    # rebobina + planejamento
    ['whistle_fall', 43.6, 0.25, 1.0], ['whoosh2', 43.65, 0.45], ['whoosh', 44.82, 0.4]] + [
    ['pop2', 45.12 + i * 0.22, 0.35] for i in range(5)] + [
    ['hammer', 46.33, 0.55], ['bell', 46.4, 0.35],
    # no dia
    ['whoosh', 47.05, 0.4], ['motor', 47.15, 0.4, 4.0], ['beeps', 49.2, 0.15, 1.8],
    # topo
    ['whoosh', 51.2, 0.4], ['motor', 51.3, 0.3, 4.2], ['whoosh2', 53.3, 0.3], ['deep_impact', 55.45, 0.5, 1.6],
    ['metal_hit', 55.5, 0.7]] + [['metal_hit', 56.15 + i * 0.17, 0.45] for i in range(4)] + [
    ['big_impact', 56.9, 0.3, 1.2],
    # final
    ['cheer', 57.2, 0.22, 4.0], ['bell', 57.25, 0.5], ['win', 60.6, 0.45], ['win', 62.55, 0.45],
]
for p in pills + [b for b in blocks if b['t_in'] > 1]:
    ev.append(['pop', p['t_in'], 0.55])
ev.sort(key=lambda e: e[1])
acfg = {"narration": "audio/narracao_tight.wav", "music": A + "music/feeling_happy_mixkit5.mp3",
        "music_vol": 0.13, "sfx_vol": 0.8, "sfx_dir": A + "sfx", "duration": END,
        "out": "build/mix.wav", "sfx": ev}
json.dump(acfg, open('config_audio_ep02.json', 'w'), indent=1)
print(len(pills), 'etiquetas,', len(blocks), 'blocos,', len(ev), 'efeitos')
