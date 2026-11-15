#!/bin/bash
# Pipeline completo do EP02 (rodar da pasta piloto-ep02). Etapas: tts | cena | render | final | all
set -e
B3=${BLENDER:-/opt/blender/blender-3.6.19-linux-x64/blender}
step=${1:-all}
OUT=entrega/EP02_o_drum.mp4
if [[ $step == all || $step == tts ]]; then
  python3 scripts/tts.py scripts/narracao.txt audio/narracao
  python3 scripts/tighten.py audio/narracao audio/narracao_tight
fi
if [[ $step == all || $step == cena ]]; then
  xvfb-run -a $B3 -b --factory-startup -P scripts/cena_ep02.py -- build/ep02.blend build/anchors.json
fi
if [[ $step == all || $step == render ]]; then
  scripts/render_all.sh build/ep02.blend build/frames
fi
if [[ $step == all || $step == final ]]; then
  python3 scripts/make_configs.py
  python3 scripts/composite.py config_ep02.json
  python3 scripts/mix_audio.py config_audio_ep02.json
  mkdir -p entrega
  ffmpeg -y -loglevel error -i build/video_sem_audio.mp4 -i build/mix.wav -map 0:v -map 1:a -c:v copy \
    -c:a aac -b:a 192k -shortest -movflags +faststart $OUT
  for t in 3.5 9.0 41.5 49.0 58.5; do
    ffmpeg -y -loglevel error -ss $t -i $OUT -frames:v 1 -q:v 2 entrega/previa_${t}s.jpg
  done
  ls -la entrega
fi
