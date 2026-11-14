#!/usr/bin/env bash
# Gera a identidade visual do canal: build/*_3d.png (Blender) -> perfil e banner finais (Pillow)
set -e
cd "$(dirname "$0")/.."
B3=${BLENDER:-/opt/blender/blender-3.6.19-linux-x64/blender}
mkdir -p build
xvfb-run -a $B3 -b --factory-startup -P scripts/cena_identidade.py -- perfil "$PWD/build/perfil_3d.png" 2
xvfb-run -a $B3 -b --factory-startup -P scripts/cena_identidade.py -- banner "$PWD/build/banner_3d.png" 1
python3 scripts/compor.py build .
