#!/bin/bash
# Render retomável da Bagger 288 (JPEG 95, mesma qualidade dos testes_v2). Pula quadros já prontos.
# Uso (da pasta piloto-bagger288): scripts/render_bloco.sh
B3=${BLENDER:-/opt/blender/blender-3.6.19-linux-x64/blender}
mkdir -p build/frames
find build/frames -size 0 -delete
xvfb-run -a $B3 -b build/bagger.blend -o "$PWD/build/frames/f_####" -F JPEG -a 2>&1 | grep -E "Saved|Error|Traceback" | awk 'NR%25==0 || /Error|Traceback/'
