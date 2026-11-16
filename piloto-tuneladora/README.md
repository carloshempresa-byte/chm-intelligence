# Engenharia Animada: "O tatuzão" (tuneladora / TBM)

Vídeo avulso de curiosidade, vertical 1080x1920, 30 fps, com cerca de 1 min 54 s. Fica abaixo do teto de 3 min do Reels e do Short (ver `roteiro.md`).

## Entregáveis
- `entrega/tuneladora_tatuzao.mp4`: vídeo final (H.264 + AAC).
- `entrega/previa_*.jpg`: quadros de prévia.
- `roteiro.md`: roteiro aprovado pelo Carlos (revisão 3), com a fonte pública de cada dado.

## Pipeline
É o mesmo do EP01/EP02. Rodar da pasta `piloto-tuneladora`:
```bash
scripts/montar_final.sh [tts|cena|render|final|all]
```

| Etapa | Script |
|---|---|
| Voz | `scripts/tts.py` (edge-tts `pt-BR-AntonioNeural`, +20%) e `scripts/tighten.py` |
| Cena 3D em corte | `scripts/cena_tuneladora.py` + `scripts/lowpoly_lib.py`. Tuneladora genérica, sem marca. O Carlin aparece com "Eng. Carlin" no capacete. |
| Render | `scripts/render_all.sh` (Blender 3.6 EEVEE, retomável) |
| Legendas, etiquetas e áudio | `scripts/make_configs.py`, que gera `config_tuneladora.json` e `config_audio_tuneladora.json`. Depois rodam `scripts/composite.py` e `scripts/mix_audio.py`. |

- Assets (efeitos sonoros, música e fonte das legendas): `../piloto-ep01/assets/`.
- Texto 3D: `../identidade-visual/assets/Montserrat-Black.ttf`.
