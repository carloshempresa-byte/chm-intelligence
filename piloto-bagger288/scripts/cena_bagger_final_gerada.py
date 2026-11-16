"""Bagger 288 — RODADA 2 de testes: salto de detalhe (geometria, materiais procedurais, terreno com relevo,
luz golden hour com contraluz, volumetria). Mesmos 6 quadros da rodada 1.
Uso:  blender -b --factory-startup -P cena_bagger_v2.py -- <pasta_saida> [amostras] [escala_res] [engine EEVEE|CYCLES] [shots...]
Escala real em metros. Visual genérico, sem marca."""
import bpy, bmesh, sys, os, math, random, time
from mathutils import Vector, Matrix, Euler
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from lowpoly_lib import hexrgb, link, empty, Mascot, helmet_band
import detalhe_lib as D
from detalhe_lib import inst, frame_between, paint, soil, simple, bevel_box_mesh, cyl_mesh, MESH

argv = sys.argv[sys.argv.index('--') + 1:]
OUT = argv[0]
SAMPLES = int(argv[1]) if len(argv) > 1 else 24
RES = float(argv[2]) if len(argv) > 2 else 1.0
ENGINE = argv[3] if len(argv) > 3 else 'EEVEE'
ONLY = argv[4:] if len(argv) > 4 else None
FONT = os.path.join(HERE, '..', '..', 'identidade-visual', 'assets', 'Montserrat-Black.ttf')
rnd = random.Random(288)
random.seed(288)
os.makedirs(OUT, exist_ok=True)

# ================================================================== render
bpy.ops.wm.read_factory_settings(use_empty=True)
sc = bpy.context.scene
sc.render.resolution_x, sc.render.resolution_y = int(1080 * RES), int(1920 * RES)
sc.render.fps = 30
if ENGINE == 'CYCLES':
    sc.render.engine = 'CYCLES'; sc.cycles.samples = SAMPLES; sc.cycles.use_denoising = True
    sc.cycles.denoiser = 'OPENIMAGEDENOISE'; sc.cycles.device = 'CPU'; sc.cycles.max_bounces = 4
    sc.render.use_motion_blur = True
else:
    sc.render.engine = 'BLENDER_EEVEE'
ee = sc.eevee
ee.taa_render_samples = SAMPLES
ee.use_soft_shadows = True; ee.shadow_cascade_size = '4096'; ee.shadow_cube_size = '2048'; ee.use_shadow_high_bitdepth = True
ee.use_gtao = True; ee.gtao_distance = 5.0; ee.gtao_factor = 1.25; ee.use_gtao_bent_normals = True; ee.use_gtao_bounce = True
ee.use_bloom = True; ee.bloom_threshold = 0.85; ee.bloom_intensity = 0.08; ee.bloom_radius = 6.0; ee.bloom_color = hexrgb('#ffd9a0')[:3]
ee.use_ssr = True; ee.use_ssr_refraction = False; ee.ssr_quality = 0.5; ee.ssr_max_roughness = 0.55
ee.use_motion_blur = True; ee.motion_blur_shutter = 0.5; ee.motion_blur_steps = 1
VOL = os.environ.get('VOL', '1') == '1'
ee.use_volumetric_lights = True; ee.volumetric_start = 2.0; ee.volumetric_end = 1600; ee.volumetric_tile_size = '8'; ee.volumetric_samples = 48
ee.use_volumetric_shadows = False
sc.view_settings.view_transform = 'Filmic'; sc.view_settings.look = 'Medium High Contrast'; sc.view_settings.exposure = 0.15
sc.render.image_settings.file_format = 'PNG'; sc.render.image_settings.color_mode = 'RGB'
sc.frame_start, sc.frame_end = 1, 90
FR = 75

# ------------------------------------------------------------------ céu: degradê golden hour + nuvens procedurais + névoa volumétrica
w = bpy.data.worlds.new('Ceu'); sc.world = w; w.use_nodes = True
nt = w.node_tree; bg = nt.nodes['Background']
tc = nt.nodes.new('ShaderNodeTexCoord')
vm = nt.nodes.new('ShaderNodeVectorMath'); vm.operation = 'MULTIPLY_ADD'
vm.inputs[1].default_value = (2, 2, 2); vm.inputs[2].default_value = (-1, -1, -1)
nt.links.new(tc.outputs['Generated'], vm.inputs[0])
dirv = vm.outputs[0]
sep = nt.nodes.new('ShaderNodeSeparateXYZ'); nt.links.new(dirv, sep.inputs[0])
mapr = nt.nodes.new('ShaderNodeMapRange'); mapr.inputs['From Min'].default_value = -0.04; mapr.inputs['From Max'].default_value = 0.6
nt.links.new(sep.outputs['Z'], mapr.inputs['Value'])
ramp = nt.nodes.new('ShaderNodeValToRGB'); nt.links.new(mapr.outputs['Result'], ramp.inputs['Fac'])
cr = ramp.color_ramp
cr.elements[0].color = hexrgb('#ffae6a'); cr.elements[1].color = hexrgb('#2f6db8')
e = cr.elements.new(0.08); e.color = hexrgb('#ffd3a0')
e = cr.elements.new(0.25); e.color = hexrgb('#a9c9ea')
# nuvens: projeta a direção num "plano de céu" e aplica ruído
zc = nt.nodes.new('ShaderNodeMath'); zc.operation = 'MAXIMUM'; zc.inputs[1].default_value = 0.06; nt.links.new(sep.outputs['Z'], zc.inputs[0])
cmb = nt.nodes.new('ShaderNodeCombineXYZ'); nt.links.new(zc.outputs[0], cmb.inputs[0]); nt.links.new(zc.outputs[0], cmb.inputs[1]); nt.links.new(zc.outputs[0], cmb.inputs[2])
pv = nt.nodes.new('ShaderNodeVectorMath'); pv.operation = 'DIVIDE'; nt.links.new(dirv, pv.inputs[0]); nt.links.new(cmb.outputs[0], pv.inputs[1])
cn_ = nt.nodes.new('ShaderNodeTexNoise'); cn_.inputs['Scale'].default_value = 1.3; cn_.inputs['Detail'].default_value = 8; cn_.inputs['Roughness'].default_value = 0.62
nt.links.new(pv.outputs[0], cn_.inputs['Vector'])
cr2 = nt.nodes.new('ShaderNodeValToRGB'); nt.links.new(cn_.outputs['Fac'], cr2.inputs['Fac'])
cr2.color_ramp.elements[0].position = 0.52; cr2.color_ramp.elements[0].color = (0, 0, 0, 1)
cr2.color_ramp.elements[1].position = 0.7; cr2.color_ramp.elements[1].color = (1, 1, 1, 1)
hz = nt.nodes.new('ShaderNodeMapRange'); hz.inputs['From Min'].default_value = 0.02; hz.inputs['From Max'].default_value = 0.16
nt.links.new(sep.outputs['Z'], hz.inputs['Value'])
cm = nt.nodes.new('ShaderNodeMath'); cm.operation = 'MULTIPLY'; nt.links.new(cr2.outputs[0], cm.inputs[0]); nt.links.new(hz.outputs['Result'], cm.inputs[1])
cm2 = nt.nodes.new('ShaderNodeMath'); cm2.operation = 'MULTIPLY'; cm2.inputs[1].default_value = 0.85; nt.links.new(cm.outputs[0], cm2.inputs[0])
mixc = nt.nodes.new('ShaderNodeMixRGB'); nt.links.new(cm2.outputs[0], mixc.inputs[0]); nt.links.new(ramp.outputs['Color'], mixc.inputs[1])
mixc.inputs[2].default_value = hexrgb('#ffe3c4')
nt.links.new(mixc.outputs[0], bg.inputs['Color']); bg.inputs['Strength'].default_value = 0.75
if VOL:
    vs = nt.nodes.new('ShaderNodeVolumePrincipled'); vs.inputs['Density'].default_value = 0.00008
    vs.inputs['Color'].default_value = hexrgb('#fff1e2'); vs.inputs['Anisotropy'].default_value = 0.55
    nt.links.new(vs.outputs[0], nt.nodes['World Output'].inputs['Volume'])

sun_d = bpy.data.lights.new('Sol', 'SUN'); sun_d.energy = 5.2; sun_d.angle = math.radians(1.6)
sun_d.color = hexrgb('#ffc898')[:3]; sun_d.shadow_cascade_max_distance = 700; sun_d.shadow_cascade_count = 4; sun_d.shadow_cascade_fade = 0.12
sun_d.use_contact_shadow = True; sun_d.contact_shadow_distance = 1.5; sun_d.contact_shadow_thickness = 0.4; sun_d.volume_factor = 1.0
sun = link(bpy.data.objects.new('Sol', sun_d))
fill_d = bpy.data.lights.new('CeuAzul', 'SUN'); fill_d.energy = 0.35; fill_d.color = hexrgb('#8fb4e6')[:3]; fill_d.use_shadow = False; fill_d.volume_factor = 0
fill = link(bpy.data.objects.new('CeuAzul', fill_d))
rim_d = bpy.data.lights.new('Contraluz', 'SUN'); rim_d.energy = 3.2; rim_d.color = hexrgb('#ffe2bd')[:3]; rim_d.use_shadow = False; rim_d.volume_factor = 0
rim = link(bpy.data.objects.new('Contraluz', rim_d))

# névoa distante (passe mist, só no terreno, sem lavar o céu)
vl = sc.view_layers[0]; vl.use_pass_mist = True; vl.use_pass_z = True
w.mist_settings.start = 350; w.mist_settings.depth = 2600; w.mist_settings.falloff = 'QUADRATIC'
sc.use_nodes = True
cn = sc.node_tree
for n in list(cn.nodes):
    cn.nodes.remove(n)
rl = cn.nodes.new('CompositorNodeRLayers'); comp = cn.nodes.new('CompositorNodeComposite')
mix = cn.nodes.new('CompositorNodeMixRGB'); mix.inputs[2].default_value = hexrgb('#e3cdb6')
geo = cn.nodes.new('CompositorNodeMath'); geo.operation = 'LESS_THAN'; geo.inputs[1].default_value = 5000.0
cn.links.new(rl.outputs['Depth'], geo.inputs[0])
mm = cn.nodes.new('CompositorNodeMath'); mm.operation = 'MULTIPLY'; mm.inputs[1].default_value = 0.55
mm2 = cn.nodes.new('CompositorNodeMath'); mm2.operation = 'MULTIPLY'
cn.links.new(rl.outputs['Mist'], mm.inputs[0]); cn.links.new(mm.outputs[0], mm2.inputs[0]); cn.links.new(geo.outputs[0], mm2.inputs[1])
cn.links.new(mm2.outputs[0], mix.inputs[0]); cn.links.new(rl.outputs['Image'], mix.inputs[1])
# leve vinheta (cinema)
ell = cn.nodes.new('CompositorNodeEllipseMask'); ell.width = 1.05; ell.height = 1.0
blr = cn.nodes.new('CompositorNodeBlur'); blr.size_x = 200; blr.size_y = 200; blr.filter_type = 'FAST_GAUSS'
cn.links.new(ell.outputs['Mask'], blr.inputs['Image'])
vig = cn.nodes.new('CompositorNodeMixRGB'); vig.blend_type = 'MULTIPLY'; vig.inputs[0].default_value = 0.35
mv = cn.nodes.new('CompositorNodeMath'); mv.operation = 'ADD'; mv.inputs[1].default_value = 0.35
cn.links.new(blr.outputs['Image'], mv.inputs[0])
cn.links.new(mix.outputs[0], vig.inputs[1]); cn.links.new(mv.outputs[0], vig.inputs[2])
cn.links.new(vig.outputs[0], comp.inputs[0])

# ================================================================== materiais
M = dict(
    steel=paint('Pintura_cinza', '#d6d8d2', 0.42, 0.25, 0.9, 0.28, 7.0), frame=paint('Estrutura', '#babeb8', 0.45, 0.3, 1.0, 0.35, 8.0),
    steel_dark=paint('Aco_escuro', '#40464e', 0.38, 0.6, 0.8, 0.35, 8.0), rail=paint('Amarelo', '#f0b43a', 0.4, 0.1, 0.6, 0.12, 6.0),
    blue=paint('Azul', '#2f6fa3', 0.45, 0.15, 0.6, 0.12, 6.0), motor=paint('Motor', '#3e7f73', 0.4, 0.3, 0.5, 0.15, 6.0),
    bucket=paint('Cacamba', '#6d737a', 0.45, 0.55, 1.3, 0.6, 40.0, 0.12), tooth=paint('Dente', '#5a5e64', 0.35, 0.75, 1.0, 0.35, 40.0),
    track=paint('Sapata', '#3a3d42', 0.55, 0.5, 1.6, 0.45, 4.5), grating=paint('Grade', '#8f9399', 0.45, 0.55, 0.6, 0.2, 6.0),
    chain=simple('Corrente', '#34373c', 0.35, 0.8), belt=simple('Lona', '#1b1c1f', 0.88), cable=simple('CaboAco', '#2c3036', 0.3, 0.8),
    glass=simple('Vidro', '#a9d8f0', 0.05, 0.0, alpha=0.4, spec=0.9), lamp=simple('Lampada', '#fff1c9', 0.4, emit='#ffe7b0', es=14.0),
    win=simple('JanelaLuz', '#ffd28a', 0.4, emit='#ffcf88', es=2.0), screen=simple('Tela', '#7fd4ff', 0.3, emit='#7fd4ff', es=3.0),
    seat=simple('Banco', '#2a2d33', 0.7),
    l_grass=soil('Grama', '#76964a', 0.12, False, 0.6, 0.4), l_top=soil('SoloEscuro', '#74512f', 0.55), l_clay=soil('Argila', '#b98249', 0.5),
    l_sand=soil('Areia', '#dcbd88', 0.45), l_coal=soil('Carvao', '#2a2522', 0.25, False, 1.0, 0.9), l_floor=soil('Piso', '#b19370', 0.7, True),
    rock=soil('Rocha', '#8d877e', 0.25, False, 1.6, 1.4), rock2=soil('Rocha2', '#a3896a', 0.3, False, 1.6, 1.4),
    water=simple('Agua', '#6b97bd', 0.05, spec=0.9), stone=paint('PedraSabao', '#e5e0d5', 0.6, 0.0, 0.15, 0.0, 2.0, 0.05),
    field=simple('Gramado', '#4f9a3f', 0.85), field2=simple('Gramado2', '#5fae4b', 0.85), line=simple('Linha', '#ffffff', 0.6),
    asphalt=soil('Asfalto', '#4b4e53', 0.35, False, 3.0, 0.25), lane=simple('Faixa', '#f2f2ee', 0.6), path=soil('Caminho', '#c9ad80', 0.6, True),
    crop1=soil('Lavoura1', '#cfae55', 0.1, True, 0.5, 0.3), crop2=soil('Lavoura2', '#8fb04d', 0.1, True, 0.5, 0.3),
    tree=simple('Copa', '#4a8743', 0.9), tree2=simple('Copa2', '#3d7539', 0.9), trunk=simple('Tronco', '#6b4a30', 0.9),
    car1=paint('Carro1', '#c9352b', 0.3, 0.4, 0.2, 0.0), car2=paint('Carro2', '#2f5f9e', 0.3, 0.4, 0.2, 0.0), car3=paint('Carro3', '#ededea', 0.3, 0.4, 0.2, 0.0),
    car4=paint('Carro4', '#2f7a6c', 0.3, 0.4, 0.2, 0.0), truck=paint('Caminhao', '#f0b43a', 0.45, 0.2, 1.2, 0.2, 5.0),
    tire=simple('Pneu', '#1e1f22', 0.85), vest=simple('Colete', '#ff7a1f', 0.6), skin=simple('Pele', '#f2c39b', 0.7), hat=simple('Capacete', '#ffd23f', 0.4),
    band=simple('m_band', '#ffffff', 0.4), bandtxt=simple('m_bandtxt', '#2f6fa3', 0.4), pole=paint('Torre', '#8d9196', 0.5, 0.5, 0.2, 0.2),
    bolt=simple('Parafuso', '#2c3036', 0.3, 0.8),
)
D.rock_meshes(M)

# ------------------------------------------------------------------ peças auxiliares
BOLT = cyl_mesh('parafuso', M['bolt'], 0.06, 0.08, 6, 'Z')


def bolt_circle(cx, cy, cz, r, n, parent, axis='Z'):
    for i in range(n):
        a = i * 2 * math.pi / n
        if axis == 'Z':
            inst(BOLT, (cx + r * math.cos(a), cy + r * math.sin(a), cz), parent=parent, name='Parafuso')
        else:  # disco no plano XZ (eixo Y)
            inst(BOLT, (cx + r * math.cos(a), cy, cz + r * math.sin(a)), (math.pi / 2, 0, 0), parent=parent, name='Parafuso')


def cabinet_row(x0, y, z, n, parent, rot=0.0):
    cab = bevel_box_mesh('armario', (1.2, 0.7, 2.1), M['steel'], 0.04, 2)
    line = bevel_box_mesh('armario_linha', (0.03, 0.02, 1.9), M['steel_dark'], 0.0, 1)
    hdl = bevel_box_mesh('armario_puxador', (0.05, 0.06, 0.25), M['steel_dark'], 0.01, 1)
    g = empty('Paineis', (x0, y, z), parent); g.rotation_euler.z = rot
    for i in range(n):
        inst(cab, (i * 1.25, 0, 1.05), parent=g, name='Armario')
        inst(line, (i * 1.25, -0.36, 1.05), parent=g, name='ArmarioPorta')
        inst(hdl, (i * 1.25 + 0.15, -0.37, 1.1), parent=g, name='Puxador')
    return g


def motor_unit(loc, parent, rot=(0, 0, 0), s=1.0):
    g = empty('Acionamento', loc, parent); g.rotation_euler = rot; g.scale = (s, s, s)
    inst(bevel_box_mesh('redutor', (2.6, 2.2, 2.4), M['steel_dark'], 0.12, 2), (0, 0, 0), parent=g, name='Redutor')
    mot = cyl_mesh('motor_corpo', M['motor'], 0.95, 2.6, 32, 'X', 0.08)
    inst(mot, (-2.6, 0, 0.1), parent=g, name='Motor')
    rib = cyl_mesh('motor_aleta', M['motor'], 1.08, 0.08, 32, 'X')
    for k in range(9):
        inst(rib, (-3.6 + k * 0.25, 0, 0.1), parent=g, name='Aleta')
    inst(cyl_mesh('motor_tampa', M['steel_dark'], 0.7, 0.4, 24, 'X', 0.05), (-4.1, 0, 0.1), parent=g, name='Ventoinha')
    for sx in (-1, 1):
        for sy in (-1, 1):
            inst(BOLT, (sx * 1.1, sy * 0.95, 1.22), parent=g, name='Parafuso')
    return g


def work_light(loc, parent, rot=(0, 0, 0)):
    g = empty('Farol', loc, parent); g.rotation_euler = rot
    inst(bevel_box_mesh('farol_corpo', (0.7, 0.5, 0.45), M['steel_dark'], 0.05, 1), (0, 0, 0), parent=g, name='FarolCorpo')
    inst(bevel_box_mesh('farol_lente', (0.06, 0.42, 0.36), M['lamp'], 0.0, 1), (0.37, 0, 0), parent=g, name='FarolLente')
    inst(bevel_box_mesh('farol_suporte', (0.12, 0.12, 0.7), M['rail'], 0.0, 1), (0, 0, -0.5), parent=g, name='FarolSuporte')


# ================================================================== A MÁQUINA
B = empty('Bagger', (0, 0, 0))
for gx, gy in ((14, 0), (-14, 14), (-14, -14)):
    grp = empty('GrupoEsteiras', (gx, gy, 0), B)
    for cx in (-8.4, 8.4):
        for cy in (-4.7, 4.7):
            D.crawler((cx, cy, 0), grp, M)
    inst(bevel_box_mesh('grupo_viga', (21, 13, 2.6), M['frame'], 0.25, 2), (0, 0, 5.0), parent=grp, name='GrupoViga')
    inst(bevel_box_mesh('grupo_long', (19, 1.6, 2.0), M['frame'], 0.2, 2), (0, -4.7, 3.9), parent=grp, name='Balancim')
    inst(bevel_box_mesh('grupo_long', (19, 1.6, 2.0), M['frame'], 0.2, 2), (0, 4.7, 3.9), parent=grp, name='Balancim')
    inst(cyl_mesh('grupo_pino', M['steel_dark'], 2.6, 2.2, 32, 'Z', 0.1), (0, 0, 7.3), parent=grp, name='GrupoPino')
    bolt_circle(0, 0, 8.45, 2.2, 16, grp)
for a, b_ in (((14, 0, 7.6), (-14, 14, 7.6)), ((-14, 14, 7.6), (-14, -14, 7.6)), ((-14, -14, 7.6), (14, 0, 7.6))):
    e_, L_ = frame_between(a, b_, B, 'Chassi')
    inst(bevel_box_mesh('chassi_viga', (1, 2.8, 3.2), M['frame'], 0.0, 1), (L_ / 2, 0, 0), scale=(L_, 1, 1), parent=e_, name='ChassiViga')
inst(cyl_mesh('pedestal', M['steel'], 12, 5, 64, 'Z', 0.25), (0, 0, 9.6), parent=B, name='Pedestal')
inst(cyl_mesh('pedestal_aba', M['steel_dark'], 12.9, 0.7, 64, 'Z', 0.08), (0, 0, 12.3), parent=B, name='AnelGiro')
bolt_circle(0, 0, 12.7, 12.4, 120, B)
SUP = empty('Superestrutura', (0, 0, 12.6), B)
inst(bevel_box_mesh('plataforma', (46, 24, 3.2), M['steel'], 0.3, 3), (-2, 0, 1.6), parent=SUP, name='Plataforma')
for x in range(-24, 21, 3):  # nervuras / chapas de reforço na lateral da plataforma
    for sy in (-1, 1):
        inst(bevel_box_mesh('nervura', (0.25, 0.4, 3.0), M['frame'], 0.03, 1), (x, sy * 12.15, 1.6), parent=SUP, name='Nervura')
WINM = bevel_box_mesh('janela', (1.7, 0.12, 1.1), M['win'], 0.02, 1)
FRM = bevel_box_mesh('janela_moldura', (1.9, 0.1, 1.3), M['steel_dark'], 0.02, 1)
PNL = bevel_box_mesh('painel_linha', (0.06, 0.06, 1.0), M['steel_dark'], 0.0, 1)
for hx, hy, hl, hw, hh in ((-6, -6, 18, 10, 9), (-6, 7.5, 18, 8, 7), (12, 0, 9, 14, 6)):
    inst(bevel_box_mesh(f'casa_{hl}_{hw}_{hh}', (hl, hw, hh), M['blue'], 0.25, 2), (hx, hy, 3.2 + hh / 2), parent=SUP, name='Casa')
    for j in range(int(hl / 3)):
        x = hx - hl / 2 + 1.8 + j * 3.0
        inst(FRM, (x, hy - hw / 2 - 0.06, 3.2 + hh * 0.7), parent=SUP, name='Moldura')
        inst(WINM, (x, hy - hw / 2 - 0.1, 3.2 + hh * 0.7), parent=SUP, name='Janela')
    for j in range(int(hl / 1.5) + 1):
        inst(PNL, (hx - hl / 2 + j * 1.5, hy - hw / 2 - 0.04, 3.2 + hh / 2), scale=(1, 1, hh), parent=SUP, name='LinhaPainel')
    inst(bevel_box_mesh(f'telhado_{hl}_{hw}', (hl + 0.6, hw + 0.6, 0.5), M['frame'], 0.1, 1), (hx, hy, 3.2 + hh + 0.25), parent=SUP, name='Telhado')
    for k in range(2):  # ventiladores/AC no telhado
        inst(cyl_mesh('ventilador', M['steel_dark'], 0.9, 0.9, 24, 'Z', 0.05), (hx - hl / 4 + k * hl / 2, hy, 3.2 + hh + 0.95), parent=SUP, name='Ventilador')
cabinet_row(-22, -11.4, 3.2, 6, SUP)
cabinet_row(10, 11.4, 3.2, 5, SUP, math.pi)
for side in (-1, 1):
    D.walkway(Vector((-25, side * 12.7, 3.25)), Vector((21, side * 12.7, 3.25)), SUP, M)
# mastros (treliça de cantoneiras, com chapas de ligação)
D.truss((6, 0, 3.2), (4, 0, 83.4), 7, 7, 12, M['steel'], 0.8, SUP, 'MastroPrinc', gusset_m=M['frame'])
D.truss((-18, 0, 3.2), (-20, 0, 50), 6, 6, 8, M['steel'], 0.7, SUP, 'MastroTras', gusset_m=M['frame'])
inst(bevel_box_mesh('topo_mastro', (9, 9, 2.2), M['rail'], 0.15, 2), (4, 0, 84.5), parent=SUP, name='TopoMastro')
SHEAVE = cyl_mesh('polia', M['steel_dark'], 1.7, 0.5, 40, 'Y', 0.06)
for k in range(4):  # moitão do topo (polias)
    inst(SHEAVE, (4, -1.5 + k * 1.0, 86.8), parent=SUP, name='Polia')
    bolt_circle(4, -1.5 + k * 1.0 - 0.27, 86.8, 0.8, 8, SUP, 'Y')
D.stairs(Vector((10.6, -4.3, 3.2)), 78, SUP, M, flights=18)
for i in range(7):
    work_light(Vector((8.4, -3.6, 10 + i * 11)), SUP, (0, 0, math.radians(-60)))
# braço da roda
PIV = Vector((22, 0, 10.0)); HUB = Vector((92, -1, 4.0))
D.truss(PIV, HUB, 9, 8, 16, M['steel'], 0.9, SUP, 'BracoRoda', gusset_m=M['frame'])
arm_e, arm_L = frame_between(PIV, HUB, SUP, 'BracoRef')
D.walkway(Vector((0, -5.6, 4.1)), Vector((arm_L, -5.6, 4.1)), arm_e, M)
D.walkway(Vector((0, 5.6, 4.1)), Vector((arm_L, 5.6, 4.1)), arm_e, M)
belt_e, belt_L, belt_chunks = D.troughed_belt(PIV + Vector((0, 0, 4.2)), HUB + Vector((-6, 0, 4.2)), SUP, M, 3.0, 1.6, True, rnd)
motor_unit(PIV + Vector((-2, 3.5, 6.2)), SUP)
for i in range(9):
    p = PIV.lerp(HUB, (i + 0.5) / 9)
    work_light(Vector((p.x, p.y - 5.8, p.z - 4.2)), SUP, (0, math.radians(30), math.radians(-90)))
# cabine do operador com janelas e interior
cab = empty('Cabine', HUB + Vector((-15, 7.2, -1.6)), SUP)
inst(bevel_box_mesh('cab_base', (6.4, 4.6, 0.5), M['rail'], 0.08, 2), (0, 0, -1.9), parent=cab, name='CabPiso')
inst(bevel_box_mesh('cab_teto', (6.6, 4.8, 0.45), M['rail'], 0.12, 2), (0, 0, 1.9), parent=cab, name='CabTeto')
inst(bevel_box_mesh('cab_meia', (6.4, 4.6, 1.2), M['rail'], 0.08, 2), (0, 0, -1.1), parent=cab, name='CabParede')
post = bevel_box_mesh('cab_coluna', (0.16, 0.16, 2.6), M['steel_dark'], 0.03, 1)
for x in (-3.1, -1.0, 1.0, 3.1):
    for y in (-2.2, 2.2):
        inst(post, (x, y, 0.6), parent=cab, name='CabColuna')
inst(bevel_box_mesh('cab_vidro', (6.2, 4.4, 2.5), M['glass'], 0.02, 1), (0, 0, 0.6), parent=cab, name='CabVidro')
inst(bevel_box_mesh('cab_banco', (0.9, 0.8, 1.2), M['seat'], 0.12, 2), (-0.5, 0, -0.1), parent=cab, name='CabBanco')
inst(bevel_box_mesh('cab_console', (1.0, 1.8, 0.9), M['steel_dark'], 0.06, 2), (1.2, 0, -0.2), parent=cab, name='CabConsole')
inst(bevel_box_mesh('cab_tela', (0.05, 0.9, 0.5), M['screen'], 0.0, 1), (1.72, -0.4, 0.4), (0, math.radians(-20), 0), parent=cab, name='CabTela')
inst(bevel_box_mesh('cab_tela', (0.05, 0.9, 0.5), M['screen'], 0.0, 1), (1.72, 0.5, 0.4), (0, math.radians(-20), 0), parent=cab, name='CabTela')
for x in (-2.5, 2.5):
    work_light(Vector((x, -2.5, 2.4)), cab, (0, math.radians(25), math.radians(-90)))
e_, L_ = frame_between(HUB + Vector((-15, 4.6, -3.5)), HUB + Vector((-15, 1.5, 0.5)), SUP, 'CabSuporte')
inst(bevel_box_mesh('cab_sup', (1, 0.7, 0.7), M['frame'], 0.0, 1), (L_ / 2, 0, 0), scale=(L_, 1, 1), parent=e_, name='CabSuporte')

# RODA DE CAÇAMBAS: 21,6 m, 18 caçambas
R_W = 10.8
WHL = empty('RodaPiv', HUB + Vector((0, -6.4, 0)), SUP)
wheel = empty('Roda', (0, 0, 0), WHL)
bpy.ops.mesh.primitive_torus_add(major_segments=128, minor_segments=12, major_radius=R_W - 1.65, minor_radius=0.5)
tor = bpy.context.object; tor.data.materials.append(M['steel_dark']); tor_me = tor.data; bpy.data.objects.remove(tor)
for sy in (-1.55, 1.55):
    inst(tor_me, (0, sy, 0), (math.pi / 2, 0, 0), parent=wheel, name='RodaAro')
bpy.ops.mesh.primitive_cylinder_add(vertices=128, radius=R_W - 2.0, depth=3.0, end_fill_type='NOTHING')
drm = bpy.context.object; drm.data.materials.append(M['steel']); drm_me = drm.data; bpy.data.objects.remove(drm)
inst(drm_me, (0, 0, 0), (math.pi / 2, 0, 0), parent=wheel, name='RodaAnel')
inst(cyl_mesh('roda_cubo', M['steel_dark'], 2.5, 4.4, 48, 'Y', 0.12), (0, 0, 0), parent=wheel, name='RodaCubo')
for sy in (-2.25, 2.25):
    bolt_circle(0, sy, 0, 1.9, 24, wheel, 'Y')
SPK = bevel_box_mesh('raio_roda', (1, 0.5, 0.6), M['frame'], 0.06, 2)
for i in range(9):
    a = i * 2 * math.pi / 9 + 0.17
    for sy in (-1.55, 1.55):
        inst(SPK, ((R_W - 2.2) / 2 * math.cos(a), sy, (R_W - 2.2) / 2 * math.sin(a)), (0, -a, 0), (R_W - 4.4, 1, 1), wheel, 'Raio')
inst(cyl_mesh('roda_eixo', M['steel_dark'], 1.2, 7.0, 32, 'Y', 0.06), (0, 4.2, 0), parent=WHL, name='RodaEixo')
motor_unit(Vector((0, 8.2, 0)), WHL, (0, 0, math.pi / 2), 1.2)
bk_me = D.bucket_mesh(M)
adp, tip, lk = D.tooth_meshes(M)
for i in range(18):
    a = i * 2 * math.pi / 18
    piv = empty(f'CacambaPiv{i}', (0, 0, 0), wheel); piv.rotation_euler.y = -a
    b = inst(bk_me, (R_W - 0.7, 0, 0), (0, -math.pi / 2, 0), (1.3, 1.25, 1.3), parent=piv, name=f'Cacamba{i}')
    so = b.modifiers.new('Esp', 'SOLIDIFY'); so.thickness = 0.16
    bv = b.modifiers.new('Chanfro', 'BEVEL'); bv.width = 0.05; bv.segments = 2; bv.limit_method = 'ANGLE'
    inst(bevel_box_mesh('labio', (0.4, 3.5, 0.5), M['steel_dark'], 0.06, 2), (R_W + 0.05, 0, 1.7), parent=piv, name='Labio')
    for j in range(5):
        y = -1.3 + j * 0.65
        inst(adp, (R_W + 0.4, y, 1.85), (0, -0.25, 0), parent=piv, name='DenteAdapt')
        inst(tip, (R_W + 0.4, y, 1.85), (0, -0.25, 0), parent=piv, name='DentePonta')
    for sy in (-1.0, 1.0):  # corrente no fundo da caçamba
        for k in range(5):
            inst(lk, (R_W - 2.2 + k * 0.28, sy, -1.0 + k * 0.05), (0, 0, (k % 2) * math.pi / 2), parent=piv, name='Elo')
fall = []
for i in range(16):
    c = inst(MESH[f'rocha{i % 6}'], (rnd.uniform(-2.0, 1.0), rnd.uniform(-1.0, 1.0), R_W - 1.0 - i * 0.6), (rnd.uniform(0, 3), rnd.uniform(0, 3), 0),
             (rnd.uniform(0.3, 0.75),) * 3, WHL, 'TerraCaindo')
    fall.append(c)
# braço do contrapeso, contrapeso, cabos
CW_P = Vector((-20, 0, 12)); CW_E = Vector((-72, 0, 20))
D.truss(CW_P, CW_E, 8, 7, 10, M['steel'], 0.8, SUP, 'BracoContrapeso', gusset_m=M['frame'])
cwe, cwl = frame_between(CW_P, CW_E, SUP, 'CWRef')
D.walkway(Vector((0, -5.0, 3.6)), Vector((cwl, -5.0, 3.6)), cwe, M)
CW = empty('Contrapeso', CW_E + Vector((-3, 0, -2)), SUP)
inst(bevel_box_mesh('contrapeso', (13, 12, 11), M['steel_dark'], 0.35, 3), (0, 0, 0), parent=CW, name='ContrapesoBloco')
for k in range(6):
    inst(bevel_box_mesh('contrapeso_placa', (13.4, 0.25, 1.2), M['frame'], 0.05, 1), (0, -6.1, -4.5 + k * 1.8), parent=CW, name='ContrapesoPlaca')
TOP = Vector((4, 0, 86.8))
CABLE = cyl_mesh('cabo', M['cable'], 1.0, 1.0, 10, 'X')


def rope(p0, p1, r, parent=None):
    e_, L_ = frame_between(p0, p1, parent, 'Cabo')
    inst(CABLE, (L_ / 2, 0, 0), scale=(L_, r, r), parent=e_, name='CaboFio')


for k in range(4):
    sy = -1.5 + k * 1.0
    rope(TOP + Vector((0, sy, 0)), HUB + Vector((-2, sy, 4.4)), 0.16, SUP)
    rope(TOP + Vector((0, sy, 0)), (PIV + HUB) / 2 + Vector((0, sy, 4.4)), 0.14, SUP)
    rope(TOP + Vector((0, sy, 0)), CW_E + Vector((0, sy, 4)), 0.16, SUP)
    rope(Vector((-20, sy, 50)), CW_E + Vector((-8, sy, 3)), 0.14, SUP)
for p in (HUB + Vector((-2, 0, 4.6)), CW_E + Vector((0, 0, 4.3))):
    for k in range(4):
        inst(SHEAVE, (p.x, -1.5 + k, p.z), (0, 0, 0), (0.6, 1, 0.6), SUP, 'PoliaPonta')
# ponte de descarga + unidade de carga
DP0 = Vector((-12, -10, 16)); DP1 = Vector((-128, -10, 12))
D.truss(DP0 - Vector((0, 0, 12.6)), DP1 - Vector((0, 0, 12.6)), 6, 5, 18, M['steel'], 0.6, B, 'PonteDescarga', gusset_m=M['frame'])
dpe, dpl = frame_between(DP0 - Vector((0, 0, 12.6)), DP1 - Vector((0, 0, 12.6)), B, 'DPRef')
D.walkway(Vector((0, -3.9, 2.6)), Vector((dpl, -3.9, 2.6)), dpe, M)
D.troughed_belt(DP0 - Vector((0, 0, 10.0)), DP1 - Vector((0, 0, 10.0)), B, M, 2.4, 1.8, True, rnd)
UC = empty('UnidadeCarga', (-130, -10, 0), B)
for cy in (-3.6, 3.6):
    D.crawler((0, cy, 0), UC, M)
inst(bevel_box_mesh('uc_corpo', (12, 12, 5), M['steel'], 0.25, 2), (0, 0, 6.6), parent=UC, name='UCCorpo')
inst(cyl_mesh('uc_coluna', M['frame'], 1.3, 6, 24, 'Z', 0.08), (0, 0, 11.6), parent=UC, name='UCColuna')
# cabo de energia no chão (alimentação elétrica)
for i in range(14):
    p0 = Vector((-30 - i * 18, 40 + 6 * math.sin(i), 0.45)); p1 = Vector((-48 - i * 18, 40 + 6 * math.sin(i + 1), 0.45))
    rope(p0, p1, 0.42)

# ================================================================== MINA (terreno com relevo, cortes irregulares, pedras)
MINE = empty('Mina', (0, 0, 0))
LAYERS = [(-60, -40, 'l_floor'), (-40, -33, 'l_sand'), (-33, -27, 'l_coal'), (-27, -18, 'l_clay'), (-18, -8, 'l_sand'),
          (-8, -1.5, 'l_clay'), (-1.5, 0, 'l_floor'), (0, 9, 'l_sand'), (9, 19, 'l_clay'), (19, 25.5, 'l_top'), (25.5, 27.2, 'l_grass')]


def block(x0, x1, y0, y1, z0, z1, name='Bancada', rel=None, seed=0):
    out = []
    for a, b_, m in LAYERS:
        lo, hi = max(a, z0), min(b_, z1)
        if hi - lo > 0.01:
            me = bevel_box_mesh(f'{name}_{x0}_{y0}_{lo}', (x1 - x0, y1 - y0, hi - lo), M[m], 0.0, 1)
            ob = inst(me, ((x0 + x1) / 2, (y0 + y1) / 2, (lo + hi) / 2), parent=MINE, name=name)
            if rel:
                D.relief(ob, rel[0], rel[1], rel[2], seed)
            out.append(ob)
    return out


block(-420, 103, -70, 160, -40, -0.3, 'BancadaMaquina')
block(103, 520, -70, 160, -40, 27.2, 'Montanha', (3.2, 9.0, 6), 1)
block(96, 103, -70, -14, -40, -0.3, 'Mordida', (1.2, 5.0, 4), 2)
for i, (y0, y1, ztop) in enumerate([(-110, -70, -12), (-150, -110, -24), (-200, -150, -36)]):
    block(-420, 520, y0, y1, -60, ztop, f'Degrau{i}', (1.8, 7.0, 6), 3 + i)
bpy.ops.mesh.primitive_grid_add(x_subdivisions=160, y_subdivisions=72, size=1)
fl = bpy.context.object; fl.name = 'PisoBancada'; fl.scale = (516, 230, 1); fl.location = (-162, 45, 0.0)
fl.data.materials.append(M['l_floor']); fl.parent = MINE
dp = fl.modifiers.new('Relevo', 'DISPLACE'); tx = bpy.data.textures.new('PisoRelevo', 'CLOUDS'); tx.noise_scale = 6; dp.texture = tx; dp.strength = 0.9; dp.texture_coords = 'GLOBAL'
box_floor_cava = inst(bevel_box_mesh('fundo_cava', (940, 260, 0.6), M['l_floor'], 0.0, 1), (50, -330, -48.3), parent=MINE, name='FundoCava')
inst(bevel_box_mesh('poca', (60, 40, 0.2), M['water'], 0.0, 1), (-80, -260, -47.9), parent=MINE, name='Poca')
block(-420, 520, 160, 240, -40, 27.2, 'Borda', (2.5, 9.0, 5), 7)
# morro de verdade atrás da frente de lavra (silhueta de montanha)
bpy.ops.mesh.primitive_cone_add(vertices=64, radius1=260, radius2=30, depth=95, location=(330, 70, 27 + 46))
hill = bpy.context.object; hill.name = 'Morro'; hill.data.materials.append(M['l_clay']); hill.parent = MINE
D.relief(hill, 9.0, 40.0, 4, 11)
bpy.ops.mesh.primitive_cone_add(vertices=48, radius1=200, radius2=20, depth=70, location=(520, -60, 27 + 34))
hill2 = bpy.context.object; hill2.name = 'Morro2'; hill2.data.materials.append(M['l_top']); hill2.parent = MINE
D.relief(hill2, 8.0, 35.0, 4, 12)
for nm, sz, loc in (('CampoFundo', (6000, 3000, 1), (0, 1700, 26.7)), ('CampoLado', (3000, 3000, 1), (2000, -400, 26.7)), ('CampoLado2', (3000, 3000, 1), (-1930, -400, 26.7))):
    inst(bevel_box_mesh(nm, sz, M['crop2'], 0.0, 1), loc, parent=MINE, name=nm)
# pedras e entulho
D.scatter_rocks((-160, 100, -68, 60), 0.4, 420, 0.25, 2.2, MINE, rnd)
D.scatter_rocks((84, 102, -26, 10), 0.4, 160, 0.4, 2.8, MINE, rnd)          # entulho na mordida
D.scatter_rocks((-300, 400, -108, -72), -12, 260, 0.3, 2.4, MINE, rnd)
D.scatter_rocks((-300, 400, -148, -112), -24, 220, 0.3, 2.4, MINE, rnd)
D.scatter_rocks((110, 480, -64, 150), 27.3, 260, 0.4, 3.0, MINE, rnd)     # em cima da montanha
bpy.ops.mesh.primitive_cone_add(vertices=24, radius1=9, radius2=1.5, depth=6, location=(90, -18, 2.6))
pile = bpy.context.object; pile.name = 'PilhaEntulho'; pile.data.materials.append(M['l_clay']); pile.parent = MINE
D.relief(pile, 1.2, 3.0, 3, 13)


# vegetação: dois tipos de árvore instanciados + arbustos
def tree_meshes():
    if 'pinheiro' not in MESH:
        bm = bmesh.new()
        for k, (r, h, z) in enumerate(((2.6, 4.0, 2.6), (2.0, 3.4, 4.6), (1.3, 2.8, 6.4))):
            bmesh.ops.create_cone(bm, cap_ends=True, segments=7, radius1=r, radius2=0.1, depth=h, matrix=Matrix.Translation((0, 0, z)))
        bmesh.ops.create_cone(bm, cap_ends=True, segments=5, radius1=0.35, radius2=0.3, depth=2.0, matrix=Matrix.Translation((0, 0, 1.0)))
        me = bpy.data.meshes.new('pinheiro'); bm.to_mesh(me); bm.free(); me.materials.append(M['tree2']); MESH['pinheiro'] = me
        bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=1, radius=2.4, location=(0, 0, 4.2))
        ob = bpy.context.object
        for v in ob.data.vertices:
            v.co *= rnd.uniform(0.85, 1.12)
        ob.data.materials.append(M['tree']); MESH['frondosa'] = ob.data; bpy.data.objects.remove(ob)
    return MESH['pinheiro'], MESH['frondosa']


pin, fro = tree_meshes()


def forest(rect, z, n, parent, smin=0.8, smax=1.8):
    for i in range(n):
        x, y = rnd.uniform(rect[0], rect[1]), rnd.uniform(rect[2], rect[3])
        s = rnd.uniform(smin, smax)
        inst(pin if i % 3 else fro, (x, y, z), (0, 0, rnd.uniform(0, 6.28)), (s, s, s * rnd.uniform(0.9, 1.3)), parent, 'Arvore')


forest((-1400, 1400, 250, 1500), 26.8, 900, MINE, 1.0, 2.6)
forest((-1500, -500, -900, 200), 26.8, 300, MINE, 1.0, 2.4)
forest((600, 1500, -900, 200), 26.8, 300, MINE, 1.0, 2.4)
forest((140, 480, 20, 150), 27.2, 120, MINE, 0.8, 1.8)
for (hx, hy, hr, hh) in ((330, 70, 260, 95), (520, -60, 200, 70)):
    for i in range(260):
        a = rnd.uniform(0, 6.28); r = hr * math.sqrt(rnd.uniform(0.05, 0.92))
        z = 27 + hh * (1 - r / hr) * 0.98
        inst(pin if i % 3 else fro, (hx + r * math.cos(a), hy + r * math.sin(a), z - 1.5), (0, 0, rnd.uniform(0, 6.28)), (1.4,) * 3, MINE, 'ArvMorro')
    D.scatter_rocks((hx - hr * 0.6, hx + hr * 0.6, hy - hr * 0.6, hy + hr * 0.6), 0, 0, 1, 2, MINE, rnd)
for i in range(7):
    x = -900 + i * 300; y = 720
    for sx in (-6, 6):
        e_, L_ = frame_between((x + sx, y, 27), (x, y, 27 + 42), None, 'Torre')
        inst(bevel_box_mesh('torre_perna', (1, 0.8, 0.8), M['pole'], 0.0, 1), (L_ / 2, 0, 0), scale=(L_, 1, 1), parent=e_, name='TorrePerna')
    e_, L_ = frame_between((x - 9, y, 60), (x + 9, y, 60), None, 'TorreBraco')
    inst(bevel_box_mesh('torre_perna', (1, 0.8, 0.8), M['pole'], 0.0, 1), (L_ / 2, 0, 0), scale=(L_, 1, 1), parent=e_, name='TorreBracoV')
    if i < 6:
        rope(Vector((x - 8, y, 60)), Vector((x + 292, y, 60)), 0.1)
for yb, zb in ((-90, -11.6), (-130, -23.6)):
    D.troughed_belt(Vector((-400, yb, zb + 1.2)), Vector((480, yb, zb + 1.2)), None, M, 2.0, 3.0, True, rnd)


# ------------------------------------------------------------------ caminhões, tratores, pessoas
def haul_truck(loc, rotz=0.0):
    g = empty('Caminhao', loc); g.rotation_euler.z = rotz
    inst(bevel_box_mesh('cam_chassi', (9.5, 4.0, 1.2), M['steel_dark'], 0.12, 2), (0, 0, 2.2), parent=g, name='CamChassi')
    def bin_b(bm):
        D._cube(bm, (7.4, 5.6, 0.25), (0, 0, -1.3)); D._cube(bm, (7.4, 0.25, 2.8), (0, 2.7, 0)); D._cube(bm, (7.4, 0.25, 2.8), (0, -2.7, 0))
        D._cube(bm, (0.25, 5.6, 3.4), (3.6, 0, 0.3)); D._cube(bm, (3.0, 5.6, 0.25), (5.0, 0, 1.9))
    bn = D.mesh_from_bm('cam_cacamba', bin_b, [M['truck']])
    inst(bn, (-1.6, 0, 4.4), parent=g, name='CamCacamba')
    inst(bevel_box_mesh('cam_cab', (2.4, 2.2, 2.0), M['truck'], 0.15, 2), (3.7, -1.2, 4.1), parent=g, name='CamCabine')
    inst(bevel_box_mesh('cam_vidro', (0.08, 1.9, 0.9), M['glass'], 0.0, 1), (4.92, -1.2, 4.4), parent=g, name='CamVidro')
    tire = cyl_mesh('pneu', M['tire'], 1.35, 1.1, 32, 'Y', 0.18)
    rim_ = cyl_mesh('aro', M['steel'], 0.7, 1.15, 16, 'Y', 0.05)
    for x in (3.4, -2.0, -4.0):
        for sy in (-1, 1):
            inst(tire, (x, sy * 2.4, 1.35), parent=g, name='CamPneu'); inst(rim_, (x, sy * 2.42, 1.35), parent=g, name='CamAro')
    inst(MESH['rocha1'], (-1.6, 0, 6.0), (0.3, 0.2, 0.1), (2.6, 2.2, 1.2), g, 'CamCarga')
    return g


def dozer(loc, rotz=0.0):
    g = empty('Trator', loc); g.rotation_euler.z = rotz
    for sy in (-1, 1):
        inst(bevel_box_mesh('trat_est', (5.0, 0.9, 1.2), M['track'], 0.3, 2), (0, sy * 1.6, 0.6), parent=g, name='TratEst')
    inst(bevel_box_mesh('trat_corpo', (3.8, 2.6, 1.6), M['truck'], 0.15, 2), (-0.3, 0, 1.9), parent=g, name='TratCorpo')
    inst(bevel_box_mesh('trat_cab', (1.6, 1.8, 1.6), M['glass'], 0.1, 1), (-0.8, 0, 3.4), parent=g, name='TratCab')
    inst(bevel_box_mesh('trat_lam', (0.4, 4.0, 1.4), M['steel_dark'], 0.06, 1), (2.9, 0, 0.9), parent=g, name='TratLamina')
    return g


def person(loc, rotz=0.0, parent=None):
    g = empty('Pessoa', loc, parent); g.rotation_euler.z = rotz
    if 'p_body' not in MESH:
        MESH['p_body'] = cyl_mesh('p_body', M['vest'], 0.25, 1.0, 10, 'Z', 0.05)
        bpy.ops.mesh.primitive_uv_sphere_add(segments=10, ring_count=8, radius=0.14); o = bpy.context.object; o.data.materials.append(M['skin']); MESH['p_head'] = o.data; bpy.data.objects.remove(o)
        bpy.ops.mesh.primitive_uv_sphere_add(segments=10, ring_count=6, radius=0.16); o = bpy.context.object; o.scale = (1, 1, 0.6); bpy.ops.object.transform_apply(scale=True)
        o.data.materials.append(M['hat']); MESH['p_hat'] = o.data; bpy.data.objects.remove(o)
        MESH['p_leg'] = cyl_mesh('p_leg', M['steel_dark'], 0.1, 0.8, 8, 'Z')
    inst(MESH['p_body'], (0, 0, 1.2), parent=g, name='PCorpo'); inst(MESH['p_head'], (0, 0, 1.85), parent=g, name='PCabeca')
    inst(MESH['p_hat'], (0, 0, 1.97), parent=g, name='PCapacete')
    for sx in (-1, 1):
        inst(MESH['p_leg'], (0, sx * 0.12, 0.4), parent=g, name='PPerna')
    return g


for (x, y, z, r) in ((-40, -95, -12, 0.2), (60, -88, -12, 3.1), (-150, -135, -24, 0.1), (140, -128, -24, 2.9), (10, -180, -36, 1.4), (62, -36, 0.3, 2.6)):
    haul_truck((x, y, z), r)
for (x, y, z, r) in ((72, -44, 0.3, 1.0), (-60, -52, 0.3, 2.4), (-200, -100, -12, 0.5)):
    dozer((x, y, z), r)
for i in range(22):
    person((rnd.uniform(-40, 70), rnd.uniform(-62, -28), 0.3), rnd.uniform(0, 6.28))

# ------------------------------------------------------------------ poeira e partículas
dust_src = link(bpy.data.objects.new('PoeiraSrc', MESH['rocha0'].copy())); dust_src.data.materials.clear(); dust_src.data.materials.append(simple('Poeira', '#e9caa2', 1.0, alpha=0.28))
dust_src.location = (0, 0, -500)
bpy.ops.mesh.primitive_plane_add(size=1, location=(100.5, -12, 6), rotation=(0, math.pi / 2, 0)); dem = bpy.context.object; dem.scale = (4, 12, 8)
ps = dem.modifiers.new('Poeira', 'PARTICLE_SYSTEM').particle_system; st = ps.settings
st.count = 650; st.frame_start = 1; st.frame_end = 90; st.lifetime = 75; st.lifetime_random = 0.5
st.normal_factor = 1.6; st.factor_random = 1.8; st.object_align_factor = (-0.6, -0.4, 1.2)
st.render_type = 'OBJECT'; st.instance_object = dust_src; st.particle_size = 1.5; st.size_random = 0.75
st.effector_weights.gravity = -0.03; st.drag_factor = 0.6
dem.show_instancer_for_render = False
mote = link(bpy.data.objects.new('GraoSrc', MESH['rocha0'].copy())); mote.data.materials.clear(); mote.data.materials.append(M['lamp']); mote.location = (0, 0, -500)
bpy.ops.mesh.primitive_plane_add(size=1, location=(96, -10, 14), rotation=(0, math.pi / 2, 0)); gem = bpy.context.object; gem.scale = (6, 14, 10)
ps2 = gem.modifiers.new('Graos', 'PARTICLE_SYSTEM').particle_system; s2 = ps2.settings
s2.count = 320; s2.frame_start = 1; s2.frame_end = 90; s2.lifetime = 80; s2.normal_factor = 0.6; s2.factor_random = 2.0
s2.render_type = 'OBJECT'; s2.instance_object = mote; s2.particle_size = 0.05; s2.size_random = 0.6; s2.effector_weights.gravity = 0.02
gem.show_instancer_for_render = False
chunk_src = link(bpy.data.objects.new('TorraoSrc', MESH['rocha0'])); chunk_src.location = (0, 0, -500)
bpy.ops.mesh.primitive_plane_add(size=1, location=(92, -6.4, 27), rotation=(0, 0, 0)); cem = bpy.context.object; cem.scale = (3, 2, 1); cem.parent = None
ps3 = cem.modifiers.new('Torroes', 'PARTICLE_SYSTEM').particle_system; s3 = ps3.settings
s3.count = 120; s3.frame_start = 1; s3.frame_end = 90; s3.lifetime = 40; s3.normal_factor = -0.5; s3.factor_random = 1.0
s3.render_type = 'OBJECT'; s3.instance_object = chunk_src; s3.particle_size = 0.35; s3.size_random = 0.6; s3.use_rotations = True
s3.rotation_factor_random = 1.0; s3.angular_velocity_mode = 'RAND'; s3.angular_velocity_factor = 4
cem.show_instancer_for_render = False


# ------------------------------------------------------------------ comparações de escala
def cristo(loc, name='Cristo'):
    """silhueta do Cristo Redentor (38 m: pedestal 8 m + estátua ~30 m), sem rosto; mais polida."""
    g = empty(name, loc)
    inst(bevel_box_mesh('cr_pedestal', (9, 9, 8), M['stone'], 0.35, 3), (0, 0, 4), parent=g, name=name + 'Pedestal')
    inst(bevel_box_mesh('cr_base', (10.5, 10.5, 0.8), M['stone'], 0.2, 2), (0, 0, 8.2), parent=g, name=name + 'Base')
    bm = bmesh.new()
    prof = [(3.8, 0), (3.5, 6), (3.0, 12), (2.7, 16), (2.9, 19), (3.1, 21.3), (1.3, 22.6), (0.9, 23.3)]
    rings = []
    for r, z in prof:
        rings.append([bm.verts.new((r * math.cos(2 * math.pi * i / 24), r * 0.82 * math.sin(2 * math.pi * i / 24), z)) for i in range(24)])
    for a, b_ in zip(rings, rings[1:]):
        for i in range(24):
            j = (i + 1) % 24
            bm.faces.new((a[i], a[j], b_[j], b_[i]))
    bm.faces.new(rings[0][::-1]); bm.faces.new(rings[-1])
    me = bpy.data.meshes.new('cr_corpo'); bm.to_mesh(me); bm.free(); me.materials.append(M['stone'])
    inst(me, (0, 0, 8.6), parent=g, name=name + 'Manto')
    arm = bevel_box_mesh('cr_braco', (28, 2.4, 2.4), M['stone'], 0.6, 4)
    inst(arm, (0, 0, 8.6 + 20.4), parent=g, name=name + 'Bracos')
    for sy in (-1, 1):
        inst(bevel_box_mesh('cr_manga', (4.5, 3.0, 3.6), M['stone'], 0.6, 3), (sy * 11.8, 0, 8.6 + 19.6), parent=g, name=name + 'Manga')
    bpy.ops.mesh.primitive_uv_sphere_add(segments=24, ring_count=16, radius=1.9, location=(0, 0, 0)); hd = bpy.context.object
    hd.data.materials.append(M['stone']); hd.parent = g; hd.location = (0, 0, 8.6 + 25.4); hd.scale = (0.9, 0.9, 1.1)
    return g


CR = empty('SetCristos', (0, 0, 0))
c1 = cristo((-24, -34, 0.3), 'Cristo1'); c1.parent = CR
c2 = cristo((-24, -34, 38.3), 'Cristo2'); c2.parent = CR
reg = inst(bevel_box_mesh('regua', (2.4, 2.4, 96), M['rail'], 0.15, 2), (-48, -34, 48.3), parent=CR, name='Regua96')
for j in range(0, 97, 8):
    inst(bevel_box_mesh('regua_marca', (3.6, 2.6, 0.7), M['steel_dark'], 0.05, 1), (-48, -34, j + 0.3), parent=CR, name='ReguaMarca')
CAMPOS = empty('SetCampos', (0, 0, 0))
for i, cx in enumerate((-60, 52)):
    fz = empty(f'Campo{i}', (cx, 0, 1.25), CAMPOS)
    for k_ in range(10):
        inst(bevel_box_mesh('campo_faixa', (10.5, 68, 0.1), M['field'] if k_ % 2 else M['field2'], 0.0, 1), (-52.5 + 5.25 + k_ * 10.5, 0, 0), parent=fz, name='CampoFaixa')
    for (sx, sy, lx, ly) in ((0, 34, 105, 0.3), (0, -34, 105, 0.3), (52.5, 0, 0.3, 68), (-52.5, 0, 0.3, 68), (0, 0, 0.3, 68)):
        inst(bevel_box_mesh(f'campo_l_{lx}_{ly}', (lx, ly, 0.12), M['line'], 0.0, 1), (sx, sy, 0.06), parent=fz, name='CampoLinha')
    bpy.ops.mesh.primitive_torus_add(major_segments=64, minor_segments=4, major_radius=9.15, minor_radius=0.15)
    t_ = bpy.context.object; t_.scale = (1, 1, 0.3); t_.data.materials.append(M['line']); t_.parent = fz; t_.location = (0, 0, 0.08)
    for sx in (-1, 1):
        for (ax, ay, alx, aly) in ((sx * (52.5 - 16.5), 0, 0.3, 40.3), (sx * (52.5 - 8.25), 20.15, 16.5, 0.3), (sx * (52.5 - 8.25), -20.15, 16.5, 0.3)):
            inst(bevel_box_mesh(f'campo_l_{alx}_{aly}', (alx, aly, 0.12), M['line'], 0.0, 1), (ax, ay, 0.07), parent=fz, name='CampoLinha')

# set da rodovia (mudança de 2001)
RD = empty('SetRodovia', (4000, 0, 0))
bpy.ops.mesh.primitive_grid_add(x_subdivisions=120, y_subdivisions=120, size=1); rg = bpy.context.object
rg.scale = (2400, 2400, 1); rg.location = (0, 0, -0.4); rg.parent = RD; rg.data.materials.append(M['crop2'])
dp = rg.modifiers.new('Relevo', 'DISPLACE'); tx = bpy.data.textures.new('RodRelevo', 'CLOUDS'); tx.noise_scale = 60; dp.texture = tx; dp.strength = 2.5; dp.texture_coords = 'GLOBAL'
for i in range(50):
    inst(bevel_box_mesh(f'lavoura{i % 3}', (160, 130, 0.3), M['crop1'] if i % 2 else M['crop2'], 0.0, 1),
         (rnd.uniform(-1100, 1100), rnd.uniform(70, 1100) * rnd.choice((-1, 1)), 0.9), (0, 0, rnd.uniform(-0.3, 0.3)), (rnd.uniform(0.6, 1.4), rnd.uniform(0.6, 1.4), 1), RD, 'RodLavoura')
inst(bevel_box_mesh('rod_pista', (2400, 24, 0.5), M['asphalt'], 0.0, 1), (0, 0, 0.6), parent=RD, name='RodPista')
for sy in (-6, 6):
    for i in range(-60, 60):
        inst(bevel_box_mesh('rod_faixa', (6, 0.25, 0.05), M['lane'], 0.0, 1), (i * 20, sy, 0.88), parent=RD, name='RodFaixa')
for sy in (-12.5, 12.5):
    inst(bevel_box_mesh('rod_guarda', (2400, 0.3, 0.45), M['steel'], 0.05, 1), (0, sy, 1.35), parent=RD, name='RodGuarda')
    for i in range(-300, 300):
        inst(bevel_box_mesh('rod_poste', (0.15, 0.15, 1.0), M['steel_dark'], 0.0, 1), (i * 4, sy, 1.0), parent=RD, name='RodPoste')
inst(bevel_box_mesh('rod_canteiro', (2400, 2.0, 0.6), M['l_grass'], 0.0, 1), (0, 0, 0.8), parent=RD, name='RodCanteiro')
inst(bevel_box_mesh('caminho', (70, 1200, 1.6), M['path'], 0.5, 2), (0, 0, 1.0), parent=RD, name='CaminhoPreparado')
for sx in (-1, 1):
    inst(bevel_box_mesh('talude', (7, 1200, 1.0), M['l_sand'], 0.4, 2), (sx * 38, 0, 0.6), (0, sx * 0.25, 0), parent=RD, name='CaminhoTalude')
D.scatter_rocks((-34, 34, -500, 500), 1.8, 260, 0.15, 0.6, RD, rnd)
cars_m = [M['car1'], M['car2'], M['car3'], M['car4']]


def car(loc, rotz, m, parent):
    g = empty('Carro', loc, parent); g.rotation_euler.z = rotz
    inst(bevel_box_mesh(f'carro_corpo_{m.name}', (4.4, 1.9, 0.85), m, 0.22, 3), (0, 0, 0.75), parent=g, name='CarroCorpo')
    inst(bevel_box_mesh('carro_teto', (2.3, 1.7, 0.7), M['glass'], 0.15, 2), (-0.2, 0, 1.45), parent=g, name='CarroTeto')
    tire = cyl_mesh('carro_pneu', M['tire'], 0.36, 0.26, 20, 'Y', 0.05)
    for sx in (-1, 1):
        for sy in (-1, 1):
            inst(tire, (sx * 1.4, sy * 0.95, 0.36), parent=g, name='CarroRoda')
    return g


for side, sy in ((-1, -9), (1, 9)):
    for i in range(16):
        car((side * (52 + i * 7.5), sy if i % 2 else sy * 0.35, 0.85), 0 if side < 0 else math.pi, cars_m[i % 4], RD)
for i in range(60):
    person((rnd.uniform(-30, 30) + rnd.choice((-80, 80)), rnd.uniform(16, 32) * rnd.choice((-1, 1)), 0.85), rnd.uniform(0, 6.28), RD)
for i in range(500):
    x, y = rnd.uniform(-1100, 1100), rnd.uniform(-1100, 1100)
    if abs(y) < 40 or abs(x) < 70:
        continue
    s = rnd.uniform(0.8, 2.2)
    inst(pin if i % 3 else fro, (x, y, 0.5), (0, 0, rnd.uniform(0, 6.28)), (s, s, s), RD, 'RodArvore')

# ------------------------------------------------------------------ mascote (Eng. Carlin)
mas = Mascot('Carlin', (34, -11.5, 0.3), rotz=math.radians(-150))
helmet_band(mas, 'Eng. Carlin', FONT, M['band'], M['bandtxt'])
mas.headpivot.animation_data_clear(); mas.headpivot.rotation_euler = (math.radians(-28), 0, 0)
for a in mas.arms:
    a.animation_data_clear()
mas.arms[1].rotation_euler = (0, math.radians(150), 0)

# ================================================================== ANIMAÇÃO FINAL (anexada à cena v2 por montar_cena_final.py)
# Tempos amarrados a audio/narracao_tight.json (109,5 s de fala). Mesma qualidade dos testes_v2.
from lowpoly_lib import F, k, vis, camera_rig, camera_path, project_anchors, add_noise
END_T = 111.0
sc.frame_start, sc.frame_end = 1, F(END_T)
sc.render.use_overwrite = False; sc.render.use_placeholder = True
sc.render.image_settings.file_format = 'JPEG'; sc.render.image_settings.quality = 95; sc.render.image_settings.color_mode = 'RGB'
NF = F(END_T)


def fa(t):
    return (F(t) - 1) / 30.0


# ------------------------------------------------------------------ objetos extras das cenas novas
# 1) carros (onda de "mais de 8 mil carros"): malha única por cor, instanciada
car_meshes = []
for i, m in enumerate((M['car1'], M['car2'], M['car3'], M['car4'])):
    def cb(bm, m=m):
        D._cube(bm, (4.4, 1.9, 0.85), (0, 0, 0.75)); D._cube(bm, (2.3, 1.7, 0.7), (-0.2, 0, 1.45))
        for sx in (-1, 1):
            for sy in (-1, 1):
                D._cube(bm, (0.72, 0.26, 0.72), (sx * 1.4, sy * 0.95, 0.36))
    car_meshes.append(D.mesh_from_bm(f'carro_onda{i}', cb, [m]))
CARS = empty('OndaCarros', (0, 0, 0))
cars = []
for ix in range(30):
    for iy in range(8):
        x = 100 - ix * 5.6 + rnd.uniform(-0.6, 0.6); y = -36 - iy * 3.6
        if 20 < x < 50 and y > -48:
            continue
        c = inst(car_meshes[(ix + iy) % 4], (x, y, 0.35), (0, 0, rnd.uniform(-0.15, 0.15)), (1, 1, 1), CARS, 'CarroOnda')
        cars.append((c, ix))
# 2) fila de caminhões basculantes ("mais de 10 mil caminhões")
TRK = empty('FilaCaminhoes', (0, 0, 0))
trucks = []
for i in range(46):
    g = haul_truck((-210 + i * 13.5, -128, -24), 0.0); g.parent = TRK
    trucks.append(g)
# 3) caçamba "solta" (gag do indo e voltando)
lone = empty('CacambaSolta', (92, -6.4, 28), None)
lb = inst(bk_me, (0, 0, 0), (0, -math.pi / 2, 0), (1.3, 1.25, 1.3), lone, 'CacambaSoltaMalha')
lb.modifiers.new('Esp', 'SOLIDIFY').thickness = 0.16
# 4) tartaruga (gag da velocidade)
tart = empty('Tartaruga', (60, -22, 0.3))
bpy.ops.mesh.primitive_uv_sphere_add(segments=16, ring_count=8, radius=0.6); o = bpy.context.object; o.scale = (1.2, 1, 0.55)
o.data.materials.append(simple('Casco', '#4f7f3a', 0.6)); o.parent = tart; o.location = (0, 0, 0.35)
bpy.ops.mesh.primitive_uv_sphere_add(segments=12, ring_count=8, radius=0.22); o = bpy.context.object
o.data.materials.append(simple('PeleTart', '#9cc46a', 0.7)); o.parent = tart; o.location = (0.8, 0, 0.3)
for sx in (-0.4, 0.4):
    for sy in (-0.4, 0.4):
        bpy.ops.mesh.primitive_uv_sphere_add(segments=8, ring_count=6, radius=0.14); o = bpy.context.object
        o.data.materials.append(simple('PeleTart', '#9cc46a', 0.7)); o.parent = tart; o.location = (sx, sy, 0.1)
# 5) cinco operadores na passarela da cabine
ops_people = []
for i in range(5):
    p = person(Vector((74.6 + i * 1.2, 6.2, 17.15)), math.radians(-60))
    ops_people.append(p)
# 6) rio e ferrovia no set da rodovia
inst(bevel_box_mesh('rio', (2400, 36, 0.3), M['water'], 0.0, 1), (0, 105, 0.35), parent=RD, name='Rio')
for sy in (-22, 22):
    inst(bevel_box_mesh('rio_margem', (2400, 6, 0.8), M['l_sand'], 0.3, 2), (0, 105 + sy, 0.4), parent=RD, name='RioMargem')
inst(bevel_box_mesh('lastro', (2400, 9, 0.9), M['rock'], 0.3, 2), (0, 175, 0.45), parent=RD, name='Lastro')
for sy in (-1.6, 1.6):
    inst(bevel_box_mesh('trilho', (2400, 0.2, 0.25), M['steel_dark'], 0.0, 1), (0, 175 + sy, 1.1), parent=RD, name='Trilho')
for i in range(-500, 500):
    inst(bevel_box_mesh('dormente', (0.4, 4.6, 0.2), M['wood'] if 'wood' in M else M['trunk'], 0.0, 1), (i * 1.2, 175, 0.95), parent=RD, name='Dormente')
# confete (parabéns)
conf_col = bpy.data.collections.new('Confete'); sc.collection.children.link(conf_col)
for i, c in enumerate(['#ffd23f', '#e5484d', '#58a6d6', '#5fae5a', '#ff7a1f', '#ffffff']):
    bpy.ops.mesh.primitive_plane_add(size=1.0, location=(0, 0, -900)); cp = bpy.context.object
    cp.scale = (1, 0.5, 1); cp.data.materials.append(simple(f'Conf{i}', c, 0.5, emit=c, es=0.6))
    sc.collection.objects.unlink(cp); conf_col.objects.link(cp)
bpy.ops.mesh.primitive_plane_add(size=1, location=(40, -40, 60)); conf_em = bpy.context.object; conf_em.scale = (60, 40, 1)
psc = conf_em.modifiers.new('Confete', 'PARTICLE_SYSTEM').particle_system; stc = psc.settings
stc.count = 2500; stc.frame_start = F(98.1); stc.frame_end = F(99.4); stc.lifetime = 600
stc.normal_factor = 0.0; stc.object_align_factor = (0, 0, -3.0); stc.factor_random = 2.0
stc.render_type = 'COLLECTION'; stc.instance_collection = conf_col; stc.use_collection_pick_random = True
stc.particle_size = 0.9; stc.size_random = 0.5; stc.use_rotations = True; stc.rotation_factor_random = 1.0
stc.angular_velocity_mode = 'RAND'; stc.angular_velocity_factor = 6.0; stc.effector_weights.gravity = 0.12; stc.drag_factor = 0.4
conf_em.show_instancer_for_render = False
# âncoras das etiquetas
a_roda = empty('a_roda', (0, 0, R_W + 1.5), WHL)
a_cab = empty('a_cab', (0, -2.5, 2.5), cab)
a_cristo = empty('a_cristo', (-24, -34, 77.5))
a_esteira = empty('a_esteira', (14 + 8.4, -4.7 - 2.0, 3.5), B)
a_cabo = empty('a_cabo', (-66, 40, 1.0))
a_carvao = empty('a_carvao', (-20, -150.5, -30), None)
a_correia = empty('a_correia', (0, 0, 0.8), belt_e)
a_rod = empty('a_rod', (4000 - 30, 0, 2.0)); a_rio = empty('a_rio', (4000 - 30, 105, 1.5)); a_fer = empty('a_fer', (4000 - 30, 175, 2.0))
a_maq = empty('a_maq', (0, 0, 50), B)

# ------------------------------------------------------------------ animações contínuas
wheel.rotation_euler.y = 0; wheel.keyframe_insert('rotation_euler', frame=1)
wheel.rotation_euler.y = -END_T * 2 * math.pi / 9.0; wheel.keyframe_insert('rotation_euler', frame=NF)   # 1 volta a cada 9 s
for fc in wheel.animation_data.action.fcurves:
    for kp in fc.keyframe_points:
        kp.interpolation = 'LINEAR'
for c in belt_chunks:
    x0 = c.location.x
    c.keyframe_insert('location', frame=1); c.location.x = x0 - 1.4; c.keyframe_insert('location', frame=16)
    for fc in c.animation_data.action.fcurves:
        for kp in fc.keyframe_points:
            kp.interpolation = 'LINEAR'
        fc.modifiers.new('CYCLES')
for c in fall:
    z0 = c.location.z
    c.keyframe_insert('location', frame=1); c.location.z = z0 - 3.0; c.keyframe_insert('location', frame=24)
    for fc in c.animation_data.action.fcurves:
        fc.modifiers.new('CYCLES')
# leve giro da superestrutura enquanto cava (vai e vem)
SUP.rotation_euler.z = 0; SUP.keyframe_insert('rotation_euler', frame=1)
for fc in SUP.animation_data.action.fcurves:
    if fc.array_index == 2:
        m_ = fc.modifiers.new('NOISE'); m_.strength = 0.05; m_.scale = 180
# partículas cobrindo o vídeo todo
st.frame_end = NF; st.count = 9000
s2.frame_end = NF; s2.count = 4500
s3.frame_end = NF; s3.count = 2400
ps_list = (st, s2, s3)

# ------------------------------------------------------------------ cenas: visibilidade de sets, máquina, sol e contraluz
T = dict(s0=0.0, s1=fa(1.83), s2=fa(6.29), s3=fa(10.56), s4=fa(14.59), s5=fa(18.40), s6=fa(25.33), s7=fa(30.25), s7b=fa(35.67),
         s8=fa(39.50), s9=fa(45.38), s9b=fa(50.90), s9c=fa(53.20), s10=fa(55.77), s11=fa(64.97), s12=fa(73.10), s13=fa(76.83),
         s14=fa(81.87), s15=fa(84.92), s15b=fa(94.63), s15c=fa(95.18), s16=fa(98.14), s17=fa(101.90))


def vis_tree(ob, t, on):
    for x in [ob] + list(ob.children_recursive):
        vis(x, t, on, frame=F(t) if t > 0 else 1)


def window(ob, t0, t1):
    for x in [ob] + list(ob.children_recursive):
        vis(x, 0, False, frame=1); vis(x, t0, True); vis(x, t1, False)


window(CR, T['s2'], T['s3'])
window(CAMPOS, T['s3'], T['s4'])
window(CARS, T['s4'], T['s5'])
window(TRK, fa(62.0), T['s11'])
window(lone, T['s8'], T['s9'])
window(tart, T['s12'], T['s13'])
for p in ops_people:
    window(p, T['s14'], T['s15'])
# rodovia só na cena 15; mina escondida nela
for x in [RD] + list(RD.children_recursive):
    vis(x, 0, False, frame=1); vis(x, T['s15'], True); vis(x, T['s16'], False)
for x in [MINE] + list(MINE.children_recursive):
    vis(x, 0, True, frame=1); vis(x, T['s15'], False); vis(x, T['s16'], True)
for hn in ('Morro', 'Morro2'):
    h_ = bpy.data.objects[hn]
    vis(h_, T['s3'], False); vis(h_, T['s4'], True)
# carros surgem em onda
for c, ix in cars:
    t0 = 15.3 + ix * 0.07
    k(c, 'scale', 0, (0.001,) * 3, 'CONSTANT', frame=1)
    k(c, 'scale', t0, (0.001,) * 3, 'BACK', 'EASE_OUT'); k(c, 'scale', t0 + 0.3, (1, 1, 1))
# caminhões surgem em fila
for i, g in enumerate(trucks):
    t0 = 62.3 + i * 0.05
    k(g, 'scale', 0, (0.001,) * 3, 'CONSTANT', frame=1)
    k(g, 'scale', t0, (0.001,) * 3, 'BACK', 'EASE_OUT'); k(g, 'scale', t0 + 0.3, (1, 1, 1))
# caçamba solta vai e volta (2 vezes)
for j, t0 in enumerate((41.6, 43.2)):
    k(lone, 'location', t0, (92, -6.4, 28), 'QUAD', 'EASE_IN_OUT')
    k(lone, 'location', t0 + 0.75, (-240, -6.4, 40))
    k(lone, 'location', t0 + 1.5, (92, -6.4, 28))
k(lone, 'rotation_euler', 41.6, (0, 0, 0), 'LINEAR'); k(lone, 'rotation_euler', 44.7, (0, 0, math.radians(720)))
# tartaruga e Carlin passam a máquina
k(tart, 'location', T['s12'], (58, -22, 0.3), 'LINEAR'); k(tart, 'location', 76.8, (12, -22, 0.3))
tart.rotation_euler.z = math.pi
# máquina: mina (0,0,0) e set da rodovia (cena 15)
def bkey(t, loc, rz, ip='CONSTANT'):
    k(B, 'location', t, loc, ip); k(B, 'rotation_euler', t, (0, 0, rz), ip)


bkey(0, (0, 0, 0), 0)
k(B, 'location', T['s12'], (0, 0, 0), 'LINEAR'); k(B, 'location', 76.8, (-0.6, 0, 0), 'CONSTANT')   # anda 0,6 m (devagar)
bkey(T['s15'], (4000, -60, 1.8), math.radians(90), 'LINEAR')
k(B, 'location', T['s15b'] - 1 / 30, (4000, 20, 1.8), 'CONSTANT')
bkey(T['s15b'], (4000, 82, 1.8), math.radians(90), 'LINEAR')
k(B, 'location', T['s15c'] - 1 / 30, (4000, 92, 1.8), 'CONSTANT')
bkey(T['s15c'], (4000, 150, 1.8), math.radians(90), 'LINEAR')
k(B, 'location', T['s16'] - 1 / 30, (4000, 168, 1.8), 'CONSTANT')
bkey(T['s16'], (0, 0, 0), 0)
# cabo de energia acende (cena 13): brilho percorre o cabo
cable_glow = simple('CaboEnergia', '#2a2d33', 0.6, emit='#7fd4ff', es=0.0)
for ob in bpy.data.objects:
    if ob.name.startswith('CaboFio') and ob.parent and ob.parent.location.z < 1.0 and ob.parent.location.x < -20:
        ob.material_slots[0].link = 'OBJECT'; ob.material_slots[0].material = cable_glow
from lowpoly_lib import ksock
ksock(cable_glow, 'Emission Strength', 0, 0.0)
ksock(cable_glow, 'Emission Strength', 78.4, 0.0)
ksock(cable_glow, 'Emission Strength', 79.2, 6.0)
ksock(cable_glow, 'Emission Strength', 81.8, 6.0)
ksock(cable_glow, 'Emission Strength', 82.3, 0.0)
# sol e contraluz por cena (elevação, azimute)
SUN_AT = [('s0', 8, 60), ('s1', 10, -40), ('s2', 14, -55), ('s3', 16, -70), ('s4', 10, -40), ('s5', 12, -60), ('s6', 9, 70),
          ('s7', 10, 140), ('s8', 11, -50), ('s9', 10, 120), ('s10', 12, -60), ('s11', 10, -40), ('s12', 10, -40), ('s13', 9, -100),
          ('s14', 10, 150), ('s15', 8, -35), ('s16', 7, 30), ('s17', 9, -50)]
sun_by_t = {}
for key_, el, az in SUN_AT:
    t = T[key_]
    k(sun, 'rotation_euler', t, (math.radians(90 - el), 0, math.radians(az)), 'CONSTANT', frame=max(1, F(t)))
    k(fill, 'rotation_euler', t, (math.radians(55), 0, math.radians(az + 180)), 'CONSTANT', frame=max(1, F(t)))
    sun_by_t[key_] = az

# ------------------------------------------------------------------ mascote
mas.pos.animation_data_clear() if mas.pos.animation_data else None
def mloc(t, loc, rz):
    k(mas.pos, 'location', t, loc, 'CONSTANT', frame=max(1, F(t))); k(mas.pos, 'rotation_euler', t, (0, 0, rz), 'CONSTANT', frame=max(1, F(t)))


mloc(0, (34, -11.5, 0.3), math.radians(-150))
mloc(T['s4'], (28, -30, 0.3), math.radians(-160))
mloc(T['s11'], (31.5, -15.5, 0.3), math.radians(-150))
mloc(T['s12'], (56, -24.5, 0.3), math.radians(90))
k(mas.pos, 'location', 74.0, (56, -24.5, 0.3), 'LINEAR'); k(mas.pos, 'location', 76.8, (30, -24.5, 0.3), 'CONSTANT')
mloc(T['s13'], (-40, 34, 0.3), math.radians(-120))
mloc(T['s15'], (4000 + 50, -20, 0.85), math.radians(-150))
mloc(T['s16'], (62, -44, 0.3), math.radians(-160))
mas.hop(15.4); mas.scared(15.9, 0.6); mas.sweat(17.6)
mas.hop(74.5); mas.hop(75.4); mas.hop(76.2)
mas.celebrate(98.2, jumps=5, period=0.5); mas.celebrate(101.9, jumps=4, period=0.5)
mas._arms(106.1, -0.18, 1.5, 'BACK', 'EASE_OUT'); mas._arms(107.6, -0.18, 1.5)
mas._arms(107.8, -0.18, 2.6, 'BACK', 'EASE_OUT'); mas.hop(107.8); mas._arms(109.6, -0.18, 2.6); mas._rest_arms(110.0)

# ------------------------------------------------------------------ CÂMERA (sempre em movimento)
bpy.data.objects.remove(cam) if 'cam' in dir() and cam else None
cam2, tgt2 = camera_rig('CamFinal')
cam2.data.clip_start = 0.3; cam2.data.clip_end = 6000
trk2 = cam2.constraints['Track To']
X = 4000
shots = [
    # 0) gancho: push-in rápido na roda mordendo a montanha
    (0.0, (78, -54, 3.0), (98, -4, 20), 15, ''),
    (T['s1'] - 0.04, (86, -34, 3.6), (97, -5, 18), 15, 'lin'),
    # 1) revelação: da esteira até a máquina inteira contra o céu
    (T['s1'], (44, -30, 1.5), (14, -2, 10), 14, 'cut'),
    (T['s2'] - 0.04, (150, -190, 46), (0, 0, 42), 18, ''),
    # 2) dois Cristos (lente longa, sem distorção) — leve push
    (T['s2'], (-10, -470, 46), (-10, 0, 46), 82, 'cut'),
    (T['s3'] - 0.04, (-6, -420, 47), (-8, 0, 47), 82, ''),
    # 3) drone de cima (campos)
    (T['s3'], (-12, -1, 560), (-12, 0, 0), 30, 'cut'),
    (T['s4'] - 0.04, (-12, -1, 500), (-12, 0, 0), 30, ''),
    # 4) peso: câmera baixa vendo a onda de carros
    (T['s4'], (70, -78, 6), (10, -30, 10), 15, 'cut'),
    (T['s5'] - 0.04, (40, -86, 9), (0, -30, 14), 15, ''),
    # 5) drone em órbita alta sobre a mina e descida até as camadas (carvão)
    (T['s5'], (-220, -330, 190), (0, -40, -10), 20, 'cut'),
    (fa(22.0), (60, -360, 120), (0, -80, -15), 20, ''),
    (T['s6'] - 0.04, (-10, -215, -22), (-20, -150, -30), 20, ''),
    # 6) da cava olhando a frente de lavra; whip-pan para a roda
    (T['s6'], (120, -170, -10), (150, -40, 14), 18, 'cut'),
    (fa(28.8), (110, -150, -6), (140, -40, 16), 18, ''),
    (T['s7'] - 0.04, (98, -40, 6), (96, -6, 16), 16, ''),
    # 7) close da roda e perfil com a escala
    (T['s7'], (100.5, -27, 5.5), (95, -7, 13), 22, 'cut'),
    (T['s7b'] - 0.04, (99.0, -24, 7.0), (95, -7, 14), 22, ''),
    (T['s7b'], (96, -75, 16), (90, -6, 16), 26, 'cut'),
    (T['s8'] - 0.04, (88, -70, 18), (88, -6, 16), 26, ''),
    # 8) caçamba indo e voltando (vista lateral larga)
    (T['s8'], (-60, -260, 60), (-70, 0, 25), 20, 'cut'),
    (T['s9'] - 0.04, (-40, -250, 55), (-60, 0, 25), 20, ''),
    # 9) acompanha a terra: braço -> corpo -> ponte de descarga -> correias da mina
    (T['s9'], (86, -16, 26), (70, 0, 20), 18, 'cut'),
    (T['s9b'] - 0.04, (28, -16, 30), (10, 0, 22), 18, 'lin'),
    (T['s9b'], (-10, -24, 24), (-40, -10, 6), 18, 'lin'),
    (T['s9c'] - 0.04, (-90, -30, 22), (-130, -10, 4), 18, 'lin'),
    (T['s9c'], (-150, -60, 14), (100, -95, -10), 18, 'cut'),
    (T['s10'] - 0.04, (-150, -70, 8), (300, -95, -10), 18, ''),
    # 10) plano herói em órbita + fila de caminhões
    (T['s10'], (210, -230, 70), (0, 0, 30), 18, 'cut'),
    (fa(61.9), (-60, -300, 80), (0, 0, 30), 18, ''),
    (fa(62.0), (-260, -260, 30), (60, -128, -20), 18, 'cut'),
    (T['s11'] - 0.04, (-200, -250, 34), (120, -128, -20), 18, ''),
    # 11) câmera baixa entre as esteiras (Carlin)
    (T['s11'], (40, -23, 1.2), (16, -4, 12), 14, 'cut'),
    (T['s12'] - 0.04, (36, -26, 1.4), (14, -4, 10), 14, ''),
    # 12) tartaruga e Carlin passam a máquina
    (T['s12'], (48, -40, 2.0), (36, -18, 3), 18, 'cut'),
    (T['s13'] - 0.04, (30, -42, 2.2), (22, -18, 4), 18, ''),
    # 13) cabo de energia acende
    (T['s13'], (-120, 20, 2.0), (-40, 40, 3), 18, 'cut'),
    (T['s14'] - 0.04, (-80, 18, 3.0), (0, 20, 30), 18, ''),
    # 14) push-in na cabine: só 5 pessoas
    (T['s14'], (58, -72, 34), (77, 6, 16), 22, 'cut'),
    (T['s15'] - 0.04, (70, -26, 21), (77, 6, 16.5), 24, ''),
    # 15) mudança de 2001: rodovia, rio, ferrovia
    (T['s15'], (X - 260, -260, 140), (X, -20, 20), 20, 'cut'),
    (fa(91.0), (X - 150, -160, 70), (X, 10, 24), 20, ''),
    (T['s15b'] - 0.04, (X - 110, -100, 40), (X, 20, 26), 20, ''),
    (T['s15b'], (X - 120, 30, 24), (X, 95, 18), 20, 'cut'),
    (T['s15c'] - 0.04, (X - 115, 35, 26), (X, 100, 18), 20, ''),
    (T['s15c'], (X - 140, 110, 30), (X, 170, 20), 20, 'cut'),
    (T['s16'] - 0.04, (X - 150, 100, 40), (X, 175, 24), 20, ''),
    # 16) herói de baixo com o sol atrás da roda + confete
    (T['s16'], (99, -82, 1.6), (88, -6, 22), 15, 'cut'),
    (T['s17'] - 0.04, (97, -78, 2.2), (88, -6, 24), 15, ''),
    # 17) órbita final (CTA)
    (T['s17'], (180, -180, 40), (20, 0, 34), 18, 'cut'),
    (106.0, (-40, -260, 50), (20, 0, 34), 18, ''),
    (END_T, (-200, -170, 60), (20, 0, 34), 18, ''),
]
camera_path(cam2, tgt2, shots)
add_noise(cam2, 'location', strength=0.12, scale=60)
# drone de cima: Track To desligado e rotação fixa
trk2.mute = False; trk2.keyframe_insert('mute', frame=1)
trk2.mute = True; trk2.keyframe_insert('mute', frame=F(T['s3']))
trk2.mute = False; trk2.keyframe_insert('mute', frame=F(T['s4']))
cam2.rotation_euler = (0, 0, math.radians(90)); cam2.keyframe_insert('rotation_euler', frame=F(T['s3']))
sc.camera = cam2
# contraluz: sempre vindo de trás do assunto (contra a câmera), por quadro
for fr in range(1, NF + 1, 6):
    sc.frame_set(fr)
    cp_ = cam2.matrix_world.translation; tp_ = tgt2.matrix_world.translation
    v = tp_ - cp_; v.z = 0
    if v.length < 1e-3:
        v = Vector((0, 1, 0))
    v.normalize()
    az = math.atan2(-v.x, v.y)
    rim.rotation_euler = (math.radians(74), 0, az + math.pi); rim.keyframe_insert('rotation_euler', frame=fr)

anchors = [a_roda, a_cab, a_cristo, a_esteira, a_cabo, a_carvao, a_correia, a_rod, a_rio, a_fer, a_maq]
with bpy.context.temp_override(scene=sc):
    bpy.ops.ptcache.free_bake_all()
    bpy.ops.ptcache.bake_all(bake=True)
OUT_BLEND = os.path.join(OUT, 'bagger.blend')
bpy.ops.wm.save_as_mainfile(filepath=OUT_BLEND)
project_anchors(anchors, 1, NF, os.path.join(OUT, 'anchors.json'))
print('OK cena final', OUT_BLEND, 'quadros', NF)
