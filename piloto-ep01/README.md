# Piloto EP01 — "A viga caixão de fundação"

Canal faceless: grandes equipamentos industriais em animação 3D low-poly.
Série: *Como montar a maior caldeira de recuperação do mundo*.

## Entregáveis
- `entrega/EP01_viga_caixao_de_fundacao.mp4` — vídeo final 1080x1920, 30 fps, H.264 + AAC
- `entrega/previa_*.jpg` — quadros de prévia
- `roteiro.md` — roteiro, notas visuais cena a cena e lista de pontos técnicos para conferir

## Como o vídeo é feito (reaproveitável)
| Etapa | Script | O que faz |
|---|---|---|
| Voz | `scripts/tts.py` | edge-tts `pt-BR-AntonioNeural` (+20%), salva mp3 + tempos de cada palavra |
| Ritmo | `scripts/tighten.py` | corta pausas > 0,22 s e recalcula os tempos (narração sem silêncio) |
| 3D | `scripts/lowpoly_lib.py` | biblioteca: materiais chapados, caixas com bevel, keyframes com easing (BACK/BOUNCE/ELASTIC), mascote com reações (susto, suor, comemoração, sinaleiro), câmera com alvo e corte seco, exportação das âncoras 2D das etiquetas |
| 3D | `scripts/cena_ep01.py` | cena do episódio: cenário, caldeira estilizada, perfil I, viga caixão, diafragmas, solda com faíscas, ultrassom, módulos, carreta, guindaste, confete; tempos amarrados à narração |
| Render | `scripts/render_all.sh` | Blender 3.6 (EEVEE) headless, retomável (pula quadros prontos) |
| Teste | `scripts/render_test.py`, `scripts/sheet.py` | renderiza quadros soltos em baixa resolução e monta folha de contato |
| 2D | `scripts/composite.py` + `config_ep01.json` | legendas palavra a palavra (Montserrat Black, branco/amarelo, contorno preto), pílulas que seguem as peças 3D, títulos e CTA |
| Áudio | `scripts/make_audio_cfg.py` + `scripts/mix_audio.py` | SFX Mixkit nos tempos certos (pop automático em cada etiqueta), música baixa com ducking, loudnorm -14 LUFS |
| Final | `scripts/montar_final.sh` | roda tudo e gera o mp4 + prévias |

Para um novo episódio: copie `cena_ep01.py` / `config_ep01.json`, troque `narracao.txt`, rode `tts` + `tighten`, ajuste os tempos das cenas usando `audio/narracao_tight.json` e rode o pipeline.

Requisitos: Blender 3.6 LTS (EEVEE legado é ~5x mais rápido que o EEVEE Next em CPU), `xvfb-run`, ffmpeg, Python 3 com Pillow e edge-tts.

## Licenças de mídia
- Efeitos sonoros e música: Mixkit (Mixkit Sound Effects Free License / Mixkit Stock Music Free License — uso gratuito em vídeos, inclusive comercial, sem atribuição obrigatória). Música: "Feeling Happy".
- Fonte: Montserrat (SIL Open Font License).
- Voz: Microsoft Edge TTS (verificar termos de uso para monetização; alternativa: gravar voz própria ou TTS pago com licença comercial).
