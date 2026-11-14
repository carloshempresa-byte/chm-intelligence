#!/bin/bash
# Pipeline completo do episódio (rodar da pasta piloto-ep01). Etapas já feitas podem ser puladas.
set -e
B3=${BLENDER:-/opt/blender/blender-3.6.19-linux-x64/blender}
step=${1:-all}
if [[ $step == all || $step == tts ]]; then
  python3 scripts/tts.py scripts/narracao.txt audio/narracao            # voz + tempos das palavras
  python3 scripts/tighten.py audio/narracao audio/narracao_tight         # tira os silêncios
fi
if [[ $step == all || $step == cena ]]; then
  xvfb-run -a $B3 -b --factory-startup -P scripts/cena_ep01.py -- build/ep01.blend build/anchors.json
fi
if [[ $step == all || $step == render ]]; then
  scripts/render_all.sh build/ep01.blend build/frames                  # retomável
fi
if [[ $step == all || $step == final ]]; then
  python3 scripts/composite.py config_ep01.json                          # legendas + pílulas -> build/video_sem_audio.mp4
  python3 scripts/make_audio_cfg.py && python3 scripts/mix_audio.py config_audio_ep01.json
  mkdir -p entrega
  ffmpeg -y -loglevel error -i build/video_sem_audio.mp4 -i build/mix.wav -map 0:v -map 1:a -c:v copy \
    -c:a aac -b:a 192k -shortest -movflags +faststart entrega/EP01_viga_caixao_de_fundacao.mp4
  for t in 1.3 27.4 41.9 62.0; do
    f=$(python3 -c "print(int(round($t*30)))")
    ffmpeg -y -loglevel error -ss $t -i entrega/EP01_viga_caixao_de_fundacao.mp4 -frames:v 1 -q:v 2 entrega/previa_${t}s.jpg
  done
  ls -la entrega
fi
