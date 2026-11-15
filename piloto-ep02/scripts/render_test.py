"""Renderiza quadros soltos em baixa resolução para checar enquadramento.
blender -b arquivo.blend -P render_test.py -- saida_dir pct t1 t2 ..."""
import bpy, sys
a = sys.argv[sys.argv.index('--') + 1:]
out, pct, ts = a[0], int(a[1]), [float(x) for x in a[2:]]
sc = bpy.context.scene
sc.render.resolution_percentage = pct
sc.eevee.taa_render_samples = 4
sc.render.use_overwrite = True; sc.render.use_placeholder = False
for t in ts:
    sc.frame_set(int(round(t * 30)) + 1)
    sc.render.filepath = f'{out}/t{t:05.1f}.png'
    bpy.ops.render.render(write_still=True)
