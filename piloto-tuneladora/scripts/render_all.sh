#!/bin/bash
# Render completo (retomável: pula quadros já existentes). Uso: render_all.sh arquivo.blend pasta_saida
B3=${BLENDER:-/opt/blender/blender-3.6.19-linux-x64/blender}
mkdir -p "$2"
xvfb-run -a $B3 -b "$1" --python-expr "import bpy; bpy.context.scene.eevee.taa_render_samples=${SAMPLES:-8}" -o "$2/f_####" -F PNG -a 2>&1 | grep -E "Saved|Error|Traceback" | awk 'NR%50==0 || /Error|Traceback/'
