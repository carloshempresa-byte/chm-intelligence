"""Gera config_bagger.json (legendas, textos grandes animados, pílulas, CTA) e config_audio_bagger.json.
Rodar da pasta piloto-bagger288. Tempos amarrados a audio/narracao_tight.json. Números do roteiro aprovado (rev. 2)."""
import json
END = 111.0
A = '../piloto-ep01/assets/'
Y, WH, OR, GR, RD = '#ffd23f', '#ffffff', '#ff7a1f', '#3fbf6f', '#e5484d'


def big(text, t0, t1, y, size=150, color=Y):
    return dict(text=text, pos=[540, y], t_in=t0, t_out=t1, big=True, size=size, color=color)


def pb(text, t0, t1, y, style='white', size=58):
    return dict(text=text, pos=[540, y], t_in=t0, t_out=t1, style=style, size=size)


blocks = [
    big('ENGOLE', 0.0, 1.8, 330, 160, Y), big('MONTANHAS', 0.25, 1.8, 500, 150, WH),
    big('BAGGER 288', 1.99, 6.25, 330, 130, Y), pb('ESCAVADEIRA DE RODA DE CAÇAMBAS', 3.72, 6.25, 470, 'white', 40), pb('ALEMANHA', 5.66, 6.25, 560, 'orange', 52),
    big('96 m', 6.65, 10.5, 300, 190, Y), pb('2 × CRISTO (38 m) = 76 m', 8.53, 10.5, 470, 'white', 50),
    big('225 m', 10.72, 14.55, 280, 180, Y), pb('MAIS DE 2 CAMPOS', 13.21, 14.55, 440, 'green', 62),
    big('~13 MIL t', 15.33, 18.35, 300, 150, Y), pb('= MAIS DE 8 MIL CARROS', 17.34, 18.35, 460, 'white', 54),
    pb('MINA A CÉU ABERTO', 20.94, 25.3, 300, 'white', 60), pb('CAMADAS DE TERRA', 23.84, 25.3, 420, 'orange', 56),
    pb('TIRAR A TERRA DE CIMA', 27.10, 29.0, 330, 'red', 56), big('A RODA', 29.70, 30.2, 330, 170, Y),
    big('21,6 m', 32.42, 39.45, 290, 170, Y), pb('18 CAÇAMBAS', 34.53, 39.45, 450, 'white', 66), pb('COM DENTES', 37.60, 39.45, 560, 'orange', 54),
    pb('INDO E VOLTANDO?', 44.44, 45.33, 360, 'red', 66),
    big('CORREIA', 48.06, 50.9, 300, 140, Y), pb('BRAÇO → CORPO → DESCARGA', 50.32, 53.15, 440, 'white', 46), pb('PRA FORA DA MINA', 54.91, 55.7, 330, 'green', 58),
    big('CAVA + DESPEJA', 56.68, 59.0, 320, 110, WH), big('240 MIL m³/DIA', 59.27, 64.9, 320, 105, Y), pb('= MAIS DE 10 MIL CAMINHÕES', 63.14, 64.9, 470, 'white', 50),
    big('12 ESTEIRAS', 67.74, 73.05, 300, 120, Y), pb('3,8 m CADA', 69.25, 73.05, 450, 'white', 60), pb('PESO ESPALHADO', 71.03, 73.05, 550, 'orange', 52),
    big('2 a 10 m/min', 75.13, 76.8, 320, 110, Y),
    pb('SEM DIESEL', 77.68, 78.5, 320, 'red', 66), big('ELÉTRICA', 78.53, 81.85, 300, 130, Y), pb('16,56 MW', 79.32, 81.85, 450, 'cyan', 72),
    big('SÓ 5 PESSOAS', 84.08, 84.9, 330, 120, Y),
    big('2001', 86.66, 98.1, 280, 170, Y), pb('22 km EM 3 SEMANAS', 91.41, 98.1, 440, 'white', 56),
    pb('RODOVIA', 93.93, 94.6, 560, 'orange', 60), pb('RIO', 94.80, 95.15, 560, 'blue', 64), pb('FERROVIA', 95.20, 98.1, 560, 'orange', 60),
    pb('CAMINHO PREPARADO', 96.0, 98.1, 660, 'white', 50),
    big('PARABÉNS!', 98.14, 101.85, 330, 130, Y),
    pb('SABIA? COMENTE', 101.91, 105.95, 250, 'white', 46), pb('ENGENHEIRO', 103.13, 105.95, 360, 'green', 84),
    pb('NÃO SABIA? COMENTE', 103.83, 105.95, 510, 'white', 46), pb('ESTAGIÁRIO', 105.19, 105.95, 620, 'orange', 84),
    pb('COMENTE O QUE ACHOU', 106.0, END, 280, 'white', 56), pb('MANDA PRO AMIGO', 106.11, END, 400, 'yellow', 70),
    pb('SEGUE PRA MAIS MÁQUINAS GIGANTES', 107.77, END, 520, 'green', 44),
]
pills = [
    dict(text='CARVÃO', anchor='a_carvao', t_in=22.37, t_out=25.3, off=[150, -220], style='white', size=60),
    dict(text='CABINE', anchor='a_cab', t_in=82.51, t_out=84.9, off=[-120, -300], style='white', size=54),
    dict(text='CABO DE ENERGIA', anchor='a_cabo', t_in=81.36, t_out=81.85, off=[0, -260], style='cyan', size=50),
]
hl = ['MONTANHAS', 'BAGGER', '288', '96 METROS', 'CRISTOS', '225 METROS', 'CAMPOS', '13 MIL', '8 MIL', 'CARROS', 'CARVÃO', 'CAMADAS',
      'RODA', '21,6 METROS', '18', 'CAÇAMBAS', 'DENTES', 'PROBLEMA', 'CORREIA', 'TRANSPORTADORA', 'CORREIAS', '240 MIL', '10 MIL',
      'CAMINHÕES', 'ESTEIRAS', '12', '3,8 METROS', '2 A 10 METROS', 'DIESEL', 'ELÉTRICA', '16,56', 'MEGAWATTS', 'CINCO', 'EM 2001',
      '22 QUILÔMETROS', 'RODOVIA', 'RIO', 'FERROVIA', 'PARABÉNS', 'ENGENHEIRO', 'ESTAGIÁRIO', 'AMIGO', 'SEGUE', 'GIGANTES']
cfg = dict(font=A + 'fonts/Montserrat.ttf', words='audio/narracao_tight.json', anchors='build/anchors.json',
           frames='build/frames', frame_ext='jpg', n_frames=int(round(END * 30)) + 1, out_video='build/video_sem_audio.mp4',
           caption_y=1330, highlight=hl, pills=pills, blocks=blocks)
json.dump(cfg, open('config_bagger.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
ev = [
    ['big_impact', 0.05, 0.4, 1.4], ['deep_impact', 0.1, 0.45, 1.6], ['whoosh', 1.8, 0.45], ['motor', 1.9, 0.25, 4.0],
    ['whoosh', 6.27, 0.45], ['bell', 6.7, 0.3], ['whoosh', 10.54, 0.45], ['whistle_fall', 11.0, 0.15, 0.8],
    ['whoosh', 14.57, 0.45], ['big_impact', 15.35, 0.3, 1.2], ['creak', 15.5, 0.25, 1.4],
    ['whoosh', 18.38, 0.45], ['whoosh2', 22.0, 0.3], ['whoosh', 25.31, 0.4], ['whoosh2', 28.8, 0.5], ['gear', 29.7, 0.4],
    ['whoosh', 30.23, 0.4], ['motor', 30.3, 0.3, 9.0], ['creak', 33.0, 0.2, 2.0], ['plate_drop', 37.6, 0.3], ['plate_drop', 38.4, 0.3],
    ['whoosh', 39.48, 0.4], ['whoosh2', 41.6, 0.45], ['whoosh2', 42.4, 0.45], ['whoosh2', 43.2, 0.45], ['whoosh2', 44.0, 0.45], ['fail', 44.5, 0.45],
    ['whoosh', 45.36, 0.4], ['motor', 45.5, 0.22, 10.0], ['plate_drop', 46.2, 0.3], ['whoosh2', 50.9, 0.3], ['whoosh2', 53.2, 0.3],
    ['whoosh', 55.75, 0.45], ['bell', 59.3, 0.3], ['truck', 62.3, 0.3, 2.6],
    ['whoosh', 64.95, 0.45], ['creak', 67.8, 0.25, 2.0], ['boing', 75.2, 0.3], ['whoosh', 73.08, 0.4],
    ['whoosh', 76.81, 0.4], ['fail', 77.7, 0.35], ['scanner', 78.5, 0.4, 1.4], ['beeps', 79.4, 0.15, 1.5],
    ['whoosh', 81.85, 0.4], ['pop', 84.1, 0.4], ['pop', 84.25, 0.4], ['pop', 84.4, 0.4], ['pop', 84.55, 0.4], ['pop', 84.7, 0.4],
    ['whoosh', 84.9, 0.45], ['motor', 85.2, 0.3, 12.5], ['truck', 93.9, 0.2, 1.2], ['whoosh2', 94.63, 0.35], ['whoosh2', 95.18, 0.35],
    ['cheer', 98.15, 0.25, 4.0], ['bell', 98.2, 0.5], ['win', 103.2, 0.45], ['win', 105.25, 0.45],
]
for b in blocks + pills:
    ev.append(['pop', b['t_in'], 0.5])
ev.sort(key=lambda e: e[1])
acfg = {"narration": "audio/narracao_tight.wav", "music": A + "music/feeling_happy_mixkit5.mp3", "music_vol": 0.13, "sfx_vol": 0.8,
        "sfx_dir": A + "sfx", "duration": END, "out": "build/mix.wav", "sfx": ev}
json.dump(acfg, open('config_audio_bagger.json', 'w'), indent=1)
print(len(blocks), 'blocos,', len(pills), 'pílulas,', len(ev), 'efeitos')
