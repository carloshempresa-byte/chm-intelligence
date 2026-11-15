# EP02: "O drum"

Série *Como montar a maior caldeira de recuperação do mundo*, do canal **Engenharia Animada**.

## Entregáveis
- `entrega/EP02_o_drum.mp4`: vídeo final em 1080x1920, 30 fps, H.264 + AAC.
- `entrega/previa_*.jpg`: quadros de prévia.
- `roteiro.md`: roteiro aprovado pelo Carlos (revisão 3) e os pontos que continuam genéricos.

## Pipeline
É o mesmo do EP01 (ver `../piloto-ep01/README.md`).

| Etapa | Script |
|---|---|
| Voz | `scripts/tts.py` (edge-tts `pt-BR-AntonioNeural`, +20%) e `scripts/tighten.py` (pausas ≤ 0,22 s) |
| Cena 3D | `scripts/cena_ep02.py` + `scripts/lowpoly_lib.py`. Inclui o Carlin com a faixa "Eng. Carlin" no capacete (`helmet_band`). |
| Render | `scripts/render_all.sh` (Blender 3.6 EEVEE, retomável) |
| Legendas, etiquetas e áudio | `scripts/make_configs.py`, que gera `config_ep02.json` e `config_audio_ep02.json`. Depois rodam `scripts/composite.py` e `scripts/mix_audio.py`. |
| Tudo | `scripts/montar_final.sh [tts\|cena\|render\|final\|all]` (rodar da pasta `piloto-ep02`) |

- Assets (efeitos sonoros, música e fonte das legendas): reaproveita `../piloto-ep01/assets/`.
- Texto 3D: usa `../identidade-visual/assets/Montserrat-Black.ttf`.

## Dados usados
Todos confirmados pelo Carlos:
- drum de 320 t, içado a 75 m (comparação aprovada: prédio de 25 andares)
- 2 guindastes de 700 t, sem marca no visual
- içamento na horizontal, com um guindaste em cada ponta
- cabos de aço da grossura de uma perna
- 5 meses de planejamento
- 2 meses de transporte do porto à obra, por estrada, em caminhão especial
- o drum entrou por cima, antes de fechar o teto

Sinaleiro, fixação final e desnível ficam genéricos, como está no roteiro.
