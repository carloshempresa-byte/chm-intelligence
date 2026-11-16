"""Gera config_tuneladora.json (legendas/etiquetas/títulos) e config_audio_tuneladora.json (SFX + música).
Rodar da pasta piloto-tuneladora. Tempos amarrados a audio/narracao_tight.json."""
import json

END = 113.6
A = '../piloto-ep01/assets/'

pills = [
    # gancho
    dict(text='133 m', anchor='a_tbm', t_in=1.56, t_out=7.6, off=[0, -330], style='yellow', size=92),
    dict(text='2.600 t', anchor='a_tbm', t_in=3.09, t_out=7.6, off=[0, -190], style='red', size=80, line=False),
    dict(text='CAVA + MONTA AS PAREDES', anchor='a_aneis', t_in=7.68, t_out=10.1, off=[80, 280], style='white', size=52),
    # o que é
    dict(text='TUNELADORA = TBM', anchor='a_tbm', t_in=10.34, t_out=17.7, off=[0, -330], style='yellow', size=62),
    dict(text='"TATUZÃO"', anchor='a_tbm', t_in=14.19, t_out=17.7, off=[0, -200], style='orange', size=78, line=False),
    dict(text='A CIDADE NÃO PARA', anchor='a_rua', t_in=16.14, t_out=17.7, off=[0, -230], style='white', size=52),
    # roda de corte
    dict(text='RODA DE CORTE', anchor='a_roda', t_in=18.62, t_out=24.0, off=[-170, -300], style='yellow', size=64),
    dict(text='11,67 m', anchor='a_frente', t_in=21.78, t_out=24.0, off=[-150, 320], style='yellow', size=96),
    # escudo e câmara
    dict(text='ESCUDO DE AÇO', anchor='a_escudo', t_in=28.13, t_out=29.05, off=[0, -280], style='yellow', size=64),
    dict(text='CÂMARA DE TERRA', anchor='a_camara', t_in=30.97, t_out=33.3, off=[-220, -360], style='orange', size=60),
    dict(text='PRESSÃO', anchor='a_frente', t_in=32.38, t_out=33.3, off=[-120, 300], style='yellow', size=70),
    # painel
    dict(text='VELOCIDADE DA ROSCA', anchor='a_botoes', t_in=35.14, t_out=37.6, off=[-60, -330], style='red', size=50),
    dict(text='VELOCIDADE DE AVANÇO', anchor='a_botoes', t_in=37.82, t_out=39.5, off=[60, -330], style='green', size=50),
    dict(text='EQUILÍBRIO', anchor='a_mano', t_in=38.99, t_out=39.5, off=[0, -230], style='green', size=64),
    # rosca e esteiras
    dict(text='ROSCA', anchor='a_rosca', t_in=39.62, t_out=41.0, off=[0, -280], style='yellow', size=70),
    dict(text='ESTEIRAS', anchor='a_esteira', t_in=42.03, t_out=43.85, off=[0, -280], style='white', size=64),
    # backup
    dict(text='BACKUP', anchor='a_tbm', t_in=46.06, t_out=51.3, off=[0, -300], style='yellow', size=74),
    dict(text='VENTILAÇÃO', anchor='a_duto', t_in=47.38, t_out=51.3, off=[-60, -200], style='orange', size=54),
    dict(text='ESTRUTURA DAS ADUELAS', anchor='a_estrut', t_in=48.29, t_out=51.3, off=[0, 260], style='white', size=48),
    dict(text='CÂMARA HIPERBÁRICA', anchor='a_caps', t_in=50.26, t_out=55.55, off=[0, -300], style='cyan', size=54),
    dict(text='TROCA DE FERRAMENTAS', anchor='a_caps', t_in=52.91, t_out=55.55, off=[0, -180], style='white', size=48, line=False),
    dict(text='AR COMPRIMIDO', anchor='a_frente', t_in=55.89, t_out=57.85, off=[-200, -560], style='blue', size=60),
    # anel
    dict(text='BRAÇO MECÂNICO', anchor='a_eretor', t_in=62.19, t_out=66.9, off=[60, 340], style='yellow', size=56),
    dict(text='ADUELAS (CONCRETO PRÉ-MOLDADO)', anchor='a_anel_novo', t_in=64.88, t_out=66.9, off=[0, -330], style='white', size=44),
    dict(text='ANEL', anchor='a_anel_novo', t_in=66.1, t_out=66.9, off=[0, -200], style='green', size=70, line=False),
    # pistões
    dict(text='PISTÕES HIDRÁULICOS', anchor='a_pistao', t_in=69.05, t_out=77.3, off=[0, -330], style='yellow', size=56),
    dict(text='ÚLTIMO ANEL', anchor='a_anel_novo', t_in=70.71, t_out=77.3, off=[-120, 300], style='white', size=56),
    # avanço e obra
    dict(text='ATÉ 15 m/DIA EM SOLO', anchor='a_tbm', t_in=79.53, t_out=83.35, off=[0, -360], style='yellow', size=58),
    dict(text='~10 m/DIA EM ROCHA', anchor='a_tbm', t_in=81.82, t_out=83.35, off=[0, -230], style='white', size=54, line=False),
    dict(text='~7 km', anchor='a_linha', t_in=85.55, t_out=89.85, off=[160, -150], style='yellow', size=90),
    dict(text='PENHA', anchor='a_penha', t_in=87.75, t_out=89.85, off=[-60, -160], style='white', size=54),
    dict(text='DUTRA', anchor='a_dutra', t_in=87.99, t_out=89.85, off=[0, -170], style='white', size=54),
    dict(text='DIVISA COM GUARULHOS', anchor='a_gru', t_in=89.14, t_out=89.85, off=[-150, -140], style='red', size=46),
    # nomes
    dict(text='NOME DE MULHER', anchor='a_rodaSP', t_in=92.06, t_out=95.85, off=[0, -380], style='orange', size=60),
    dict(text='11,67 m', anchor='a_rodaSP', t_in=99.4, t_out=101.25, off=[-60, -150], style='yellow', size=64),
    dict(text='BERTHA (SEATTLE, EUA)', anchor='a_placaBE', t_in=98.79, t_out=101.25, off=[0, -200], style='white', size=50),
    dict(text='17,5 m', anchor='a_rodaBE', t_in=99.31, t_out=101.25, off=[0, -100], style='yellow', size=80, line=False),
]
blocks = [
    dict(text='CURIOSIDADE', pos=[540, 200], t_in=0.0, t_out=3.6, style='orange', size=44),
    dict(text='O TATUZÃO', pos=[540, 300], t_in=0.05, t_out=3.6, style='yellow', size=64),
    dict(text='A MÁQUINA QUE CAVA O TÚNEL', pos=[540, 395], t_in=0.1, t_out=3.6, style='white', size=36),
    dict(text='DESABA!', pos=[540, 520], t_in=25.91, t_out=26.9, style='red', size=110),
    dict(text='SEM RODAS', pos=[540, 480], t_in=68.36, t_out=69.0, style='red', size=96),
    dict(text='ANDA EMPURRANDO O PRÓPRIO TÚNEL', pos=[540, 420], t_in=74.6, t_out=77.3, style='yellow', size=44),
    dict(text='SANTA BÁRBARA, PADROEIRA DOS MINEIROS', pos=[540, 420], t_in=93.6, t_out=95.85, style='white', size=36),
    dict(text='PARABÉNS!', pos=[540, 330], t_in=101.43, t_out=104.2, style='yellow', size=96),
    dict(text='SABIA? COMENTE', pos=[540, 250], t_in=104.29, t_out=108.4, style='white', size=46),
    dict(text='ENGENHEIRO', pos=[540, 360], t_in=105.75, t_out=108.4, style='green', size=84),
    dict(text='NÃO SABIA? COMENTE', pos=[540, 510], t_in=106.41, t_out=108.4, style='white', size=46),
    dict(text='ESTAGIÁRIO', pos=[540, 620], t_in=107.69, t_out=108.4, style='orange', size=84),
    dict(text='COMENTE O QUE ACHOU', pos=[540, 280], t_in=108.47, t_out=END, style='white', size=56),
    dict(text='MANDA PRO AMIGO', pos=[540, 400], t_in=108.57, t_out=END, style='yellow', size=70),
    dict(text='SEGUE PRA MAIS MÁQUINAS GIGANTES', pos=[540, 520], t_in=110.23, t_out=END, style='green', size=44),
]
hl = ['133 METROS', '2.600 TONELADAS', 'TUNELADORA', 'TBM', 'TATUZÃO', 'MINHOCA', 'RODA', 'CORTE', '11,67 METROS', 'DESABA',
      'ESCUDO', 'AÇO', 'CÂMARA', 'PRESSÃO', 'ROSCA', 'VELOCIDADE', 'ESTEIRAS', 'BACKUP', 'VENTILAÇÃO', 'HIPERBÁRICA',
      'COMPRIMIDO', 'ADUELAS', 'ANEL', 'RODAS', 'PISTÕES', 'HIDRÁULICOS', '15 METROS', '10 METROS', 'SOLO', 'ROCHA',
      '7 QUILÔMETROS', 'PENHA', 'DUTRA', 'GUARULHOS', 'MULHER', 'BÁRBARA', 'BERTHA', '17,5 METROS', 'PARABÉNS',
      'ENGENHEIRO', 'ESTAGIÁRIO', 'AMIGO', 'SEGUE', 'GIGANTES', 'NÃO']
cfg = dict(font=A + 'fonts/Montserrat.ttf', words='audio/narracao_tight.json', anchors='build/anchors.json',
           frames='build/frames', n_frames=int(round(END * 30)) + 1, out_video='build/video_sem_audio.mp4',
           caption_y=1330, highlight=hl, pills=pills, blocks=blocks)
json.dump(cfg, open('config_tuneladora.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)

ev = [
    # gancho
    ['whoosh', 0.1, 0.35], ['whoosh2', 3.7, 0.45], ['motor', 4.0, 0.3, 5.0], ['big_impact', 5.0, 0.25, 1.2], ['boing', 5.05, 0.3],
    ['whoosh', 10.1, 0.4], ['pop2', 11.8, 0.35], ['boing', 12.3, 0.3], ['pop2', 13.3, 0.35], ['beeps', 16.2, 0.1, 1.2],
    # roda de corte
    ['whoosh', 17.7, 0.4], ['gear', 17.8, 0.4], ['motor', 18.0, 0.35, 6.0], ['plate_drop', 19.6, 0.2], ['plate_drop', 21.0, 0.2],
    # problema / escudo / câmara
    ['whoosh2', 24.0, 0.4], ['big_impact', 25.4, 0.35, 1.5], ['creak', 25.5, 0.3, 1.2], ['fail', 25.95, 0.45],
    ['whistle_fall', 26.55, 0.25, 0.6], ['whoosh', 27.0, 0.45], ['metal_hit', 28.15, 0.6],
    ['whoosh', 29.1, 0.35], ['gear', 31.9, 0.35],
    # painel
    ['whoosh', 33.38, 0.4], ['gear', 35.15, 0.4], ['beeps', 35.5, 0.12, 0.6], ['gear', 37.75, 0.4], ['bell', 38.95, 0.35],
    # rosca, esteiras
    ['whoosh', 39.58, 0.4], ['motor', 39.7, 0.25, 4.2], ['whoosh2', 41.0, 0.3],
    # backup e câmara hiperbárica
    ['whoosh', 43.87, 0.45], ['whoosh2', 46.0, 0.3], ['scanner', 50.3, 0.3, 1.0], ['metal_hit', 54.7, 0.4],
    ['metal_hit', 55.4, 0.45], ['whoosh', 55.6, 0.4], ['hammer', 56.2, 0.35], ['hammer', 56.55, 0.35],
    ['hammer', 56.9, 0.35], ['hammer', 57.25, 0.35],
    # anel
    ['whoosh', 57.92, 0.4], ['boing', 59.45, 0.3], ['gear', 62.0, 0.35], ['plate_drop', 62.9, 0.45], ['gear', 63.3, 0.35],
    ['plate_drop', 64.4, 0.45], ['gear', 64.9, 0.35], ['plate_drop', 65.9, 0.45], ['bell', 66.1, 0.4],
    # pistões
    ['whoosh', 67.0, 0.4], ['pop2', 67.4, 0.3], ['fail', 68.4, 0.4], ['pop2', 68.85, 0.3],
    ['motor', 70.0, 0.35, 2.0], ['metal_hit', 71.9, 0.4], ['plate_drop', 72.9, 0.4], ['plate_drop', 73.3, 0.4],
    ['motor', 74.0, 0.35, 1.5], ['metal_hit', 75.4, 0.4], ['plate_drop', 75.9, 0.4], ['plate_drop', 76.4, 0.4]] + [
    ['plate_drop', 78.1 + i * 0.95, 0.3] for i in range(6)] + [
    ['whoosh', 77.43, 0.4], ['bell', 79.6, 0.25],
    # mapa
    ['whoosh', 83.41, 0.45], ['whoosh2', 85.45, 0.35], ['pop', 87.75, 0.4], ['pop', 88.0, 0.4],
    # nomes / Bertha
    ['whoosh', 89.89, 0.4], ['whistle_fall', 91.9, 0.2, 0.6], ['bell', 92.5, 0.4], ['cheer', 92.55, 0.12, 1.2],
    ['whoosh', 95.9, 0.45], ['big_impact', 96.9, 0.3, 1.2], ['boing', 97.05, 0.3], ['bell', 99.2, 0.35],
    # rompimento + final
    ['whoosh', 101.3, 0.45], ['deep_impact', 101.65, 0.5, 1.6], ['big_impact', 101.7, 0.4, 1.4],
    ['cheer', 101.8, 0.22, 4.0], ['bell', 101.5, 0.45], ['win', 105.8, 0.45], ['win', 107.75, 0.45],
]
for p in pills + [b for b in blocks if b['t_in'] > 1]:
    ev.append(['pop', p['t_in'], 0.55])
ev.sort(key=lambda e: e[1])
acfg = {"narration": "audio/narracao_tight.wav", "music": A + "music/feeling_happy_mixkit5.mp3",
        "music_vol": 0.13, "sfx_vol": 0.8, "sfx_dir": A + "sfx", "duration": END,
        "out": "build/mix.wav", "sfx": ev}
json.dump(acfg, open('config_audio_tuneladora.json', 'w'), indent=1)
print(len(pills), 'etiquetas,', len(blocks), 'blocos,', len(ev), 'efeitos')
