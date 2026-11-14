"""EP01 — A viga caixão de fundação. Monta a cena inteira, anima e salva o .blend.
Uso:  blender -b --factory-startup -P cena_ep01.py -- <saida.blend> [anchors.json]
Tempos (s) vêm da narração enxugada (audio/narracao_tight.json)."""
import bpy, sys, os, math, random
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import importlib, lowpoly_lib
importlib.reload(lowpoly_lib)
from lowpoly_lib import *

argv = sys.argv[sys.argv.index('--') + 1:] if '--' in sys.argv else []
OUT_BLEND = argv[0] if argv else '/tmp/ep01.blend'
OUT_ANCH = argv[1] if len(argv) > 1 else None
END_T = 67.6
random.seed(7)

# ------------------------------------------------------------------ limpa/config
bpy.ops.wm.read_factory_settings(use_empty=True)
sc = bpy.context.scene
sc.render.fps = FPS
sc.frame_start = 1
sc.frame_end = F(END_T)
sc.render.resolution_x, sc.render.resolution_y = 1080, 1920
sc.render.engine = 'BLENDER_EEVEE'
ee = sc.eevee
ee.taa_render_samples = 12
ee.use_soft_shadows = True
ee.shadow_cascade_size = '2048'
ee.shadow_cube_size = '1024'
ee.use_gtao = True
ee.gtao_distance = 1.2
ee.gtao_factor = 0.8
ee.use_bloom = True
ee.bloom_threshold = 1.2
ee.bloom_intensity = 0.06
ee.bloom_radius = 5.0
sc.view_settings.view_transform = 'Standard'
sc.view_settings.look = 'None'
sc.view_settings.exposure = 0.0
sc.render.image_settings.file_format = 'PNG'
sc.render.image_settings.color_mode = 'RGB'
sc.render.use_overwrite = False
sc.render.use_placeholder = True

# céu: gradiente simples (cima azul, horizonte claro)
w = bpy.data.worlds.new('Ceu'); sc.world = w; w.use_nodes = True
nt = w.node_tree; bg = nt.nodes['Background']
tc = nt.nodes.new('ShaderNodeTexCoord'); sep = nt.nodes.new('ShaderNodeSeparateXYZ')
ramp = nt.nodes.new('ShaderNodeValToRGB')
nt.links.new(tc.outputs['Generated'], sep.inputs[0])
mapr = nt.nodes.new('ShaderNodeMapRange'); mapr.inputs['From Min'].default_value = 0.5; mapr.inputs['From Max'].default_value = 0.8
nt.links.new(sep.outputs['Z'], mapr.inputs['Value']); nt.links.new(mapr.outputs['Result'], ramp.inputs['Fac'])
ramp.color_ramp.elements[0].color = hexrgb('#e6f4fb'); ramp.color_ramp.elements[1].color = hexrgb('#6fbde8')
nt.links.new(ramp.outputs['Color'], bg.inputs['Color']); bg.inputs['Strength'].default_value = 0.9

sun_d = bpy.data.lights.new('Sol', 'SUN'); sun_d.energy = 3.3; sun_d.angle = math.radians(7)
sun_d.color = hexrgb('#fff3e0')[:3]
sun = link(bpy.data.objects.new('Sol', sun_d)); sun.rotation_euler = (math.radians(48), math.radians(8), math.radians(38))
sun_d.shadow_cascade_max_distance = 120; sun_d.shadow_cascade_count = 4

# ------------------------------------------------------------------ paleta
P = dict(
    ground=mat('ground', '#e7d6ae', 0.95, spec=0.1), grass=mat('grass', '#a9cf7a', 0.95, spec=0.1),
    concrete=mat('concrete', '#c9c3b8', 0.9, spec=0.15), concrete_d=mat('concrete_d', '#aaa397', 0.9),
    asphalt=mat('asphalt', '#55595f', 0.9), lane=mat('lane', '#ffd23f', 0.6),
    ibeam=mat('ibeam', '#8e99a6', 0.45, spec=0.5),
    flange=mat('flange', '#2f6fa3', 0.45, spec=0.5), web=mat('web', '#58a6d6', 0.45, spec=0.5),
    diaph=mat('diaph', '#f29e4c', 0.5), load=mat('load', '#e5484d', 0.5),
    weld=mat('weld', '#5d6470', 0.5, emit='#ff9a2e', emit_strength=0.0),
    spark=mat('spark', '#ffd27a', 0.5, emit='#ffb13b', emit_strength=12.0),
    scan=mat('scan', '#2ee6d6', 0.3, emit='#2ee6d6', emit_strength=2.5, alpha=0.55),
    boiler=mat('boiler', '#e9e4da', 0.8), steel_d=mat('steel_d', '#3b4a5c', 0.6), red=mat('red', '#d64545', 0.6),
    white=mat('white', '#f7f7f2', 0.7), crane=mat('crane', '#f5c242', 0.45), dark=mat('dark', '#2a2d33', 0.7),
    truck=mat('truck', '#e74c3c', 0.45), glass=mat('glass', '#9fd6f2', 0.15), wood=mat('wood', '#b07a46', 0.9),
    tree=mat('tree', '#5fae5a', 0.9), trunk=mat('trunk', '#8a5a3b', 0.9), cone=mat('cone', '#ff7a1f', 0.6),
    dust=mat('dust', '#e8dcc2', 1.0), cloud=mat('cloud', '#ffffff', 1.0, emit='#ffffff', emit_strength=0.3),
    container1=mat('cont1', '#3e8e7e', 0.7), container2=mat('cont2', '#c8553d', 0.7), car=mat('car', '#7b5ea7', 0.4),
)

# ------------------------------------------------------------------ cenário
prim('plane', 'Chao', (0, 0, 0), P['ground'], size=900)
for i in range(70):  # tufos de grama low-poly espalhados longe da obra
    a = random.uniform(0, 2 * math.pi); r = random.uniform(30, 140)
    x, y = r * math.cos(a), r * math.sin(a)
    if -40 < x < 40 and -30 < y < 50: continue
    prim('cone', f'Grama{i}', (x, y, 0.2), P['grass'], vertices=5, radius1=1.2, depth=0.4)
for i in range(45):  # árvores
    a = random.uniform(0, 2 * math.pi); r = random.uniform(34, 120)
    x, y = r * math.cos(a), r * math.sin(a) + 10
    if -30 < x < 30 and -25 < y < 48: continue
    s = random.uniform(0.8, 1.6)
    prim('cyl', f'Tronco{i}', (x, y, 1.0 * s), P['trunk'], vertices=5, radius=0.3 * s, depth=2 * s)
    prim('cone', f'Copa{i}', (x, y, 3.6 * s), P['tree'], vertices=6, radius1=1.9 * s, depth=4.5 * s)
for i in range(7):  # nuvens
    x, y, z = random.uniform(-60, 60), random.uniform(60, 140), random.uniform(45, 75)
    for j in range(3):
        prim('ico', f'Nuvem{i}_{j}', (x + j * 4 - 4, y, z + (j == 1) * 1.5), P['cloud'], subdivisions=1, radius=random.uniform(3, 5), scale=(1.3, 1, 0.7))

# pátio de concreto e apoios (blocos de fundação)
prim('cube', 'Patio', (0, 2, 0.05), P['concrete_d'], scale=(13, 10, 0.05))
PEDX = 5.8
peds = []
for sx in (-1, 1):
    pd = box(f'Apoio{sx}', (2.4, 3.4, 1.4), (sx * PEDX, 0, 0.7), P['concrete'], bevel=0.04)
    box(f'ApoioPlaca{sx}', (1.9, 2.6, 0.06), (sx * PEDX, 0, 1.43), P['steel_d'], bevel=0.01)
    peds.append(pd)
# berço de madeira (área de pré-montagem para o içamento)
for sx in (-1, 1):
    for j in range(3):
        box(f'Calco{sx}_{j}', (1.2, 3.0, 0.17), (sx * 4.5, 6.5, 0.085 + 0.17 * j), P['wood'], bevel=0.02)

# estrada de acesso (atrás da obra)
prim('cube', 'Estrada', (0, 18, 0.03), P['asphalt'], scale=(300, 3.2, 0.03))
for i in range(-30, 31):
    prim('cube', f'Faixa{i}', (i * 5, 18, 0.065), P['lane'], scale=(1.2, 0.12, 0.01))
carro = empty('Carro', (-6, 16.8, 0))
box('CarroCorpo', (4.2, 1.8, 0.8), (0, 0, 0.75), P['car'], bevel=0.08, parent=carro)
box('CarroTeto', (2.2, 1.6, 0.6), (-0.2, 0, 1.4), P['glass'], bevel=0.06, parent=carro)
for sx in (-1, 1):
    for sy in (-1, 1):
        prim('cyl', f'CarroRoda{sx}{sy}', (1.35 * sx, 0.9 * sy, 0.38), P['dark'], carro, rot=(math.pi / 2, 0, 0), vertices=8, radius=0.38, depth=0.25)

# containers e cones de sinalização
for i, (x, y, m) in enumerate([(-15, 6, 'container1'), (-15, 9, 'container2'), (15.5, 7, 'container1')]):
    box(f'Container{i}', (6, 2.4, 2.6), (x, y, 1.3), P[m], bevel=0.05)
for i, (x, y) in enumerate([(-8, -6), (-4, -6.5), (4, -6.5), (8, -6), (11.5, -3), (-11.5, -3)]):
    prim('cone', f'Cone{i}', (x, y, 0.35), P['cone'], vertices=8, radius1=0.28, radius2=0.04, depth=0.7)
    prim('cube', f'ConeBase{i}', (x, y, 0.03), P['cone'], scale=(0.32, 0.32, 0.03))

# ------------------------------------------------------------------ caldeira de recuperação (silhueta estilizada)
BY = 40
cald = empty('Caldeira', (0, BY, 0))
box('CaldCorpo', (14, 14, 46), (0, 0, 23), P['boiler'], parent=cald, bevel=0.1)
for j in range(9):
    box(f'CaldFaixa{j}', (14.5, 14.5, 0.6), (0, 0, 4 + j * 5), P['steel_d'], parent=cald, bevel=0.05)
for sx in (-1, 1):
    for sy in (-1, 1):
        box(f'CaldColuna{sx}{sy}', (1.2, 1.2, 52), (sx * 9, sy * 9, 26), P['steel_d'], parent=cald, bevel=0.05)
box('CaldTeto', (20, 20, 3), (0, 0, 53), P['steel_d'], parent=cald, bevel=0.1)
box('CaldCasa', (14, 10, 5), (0, 0, 57), P['boiler'], parent=cald, bevel=0.1)
prim('cyl', 'CaldTubulao', (0, -2, 49.5), P['red'], cald, rot=(0, math.pi / 2, 0), vertices=12, radius=1.6, depth=13)
box('CaldEscada', (3, 3, 50), (-10.8, -6, 25), P['crane'], parent=cald, bevel=0.05)
for j in range(0):
    box(f'CaldPlataforma{j}', (22, 2, 0.3), (0, -10.3, 5 + j * 5), P['steel_d'], parent=cald, bevel=0.02)
box('CaldPrecip', (12, 18, 16), (-22, 4, 8), P['boiler'], parent=cald, bevel=0.1)
box('CaldDuto', (10, 3, 3), (-12, 4, 14), P['steel_d'], parent=cald, bevel=0.05)
chamine = empty('Chamine', (22, BY + 12, 0))
for j in range(8):
    prim('cyl', f'ChamineSeg{j}', (0, 0, 4.5 + j * 9), P['red'] if j % 2 else P['white'], chamine, vertices=12, radius=2.6 - j * 0.12, depth=9)
a_boiler = empty('a_boiler', (-7.2, -7.2, 34), cald)

# ------------------------------------------------------------------ mascote
mas = Mascot('Mascote', (1.6, -3.6, 0), rotz=math.radians(55))

# ------------------------------------------------------------------ viga I (problema)
L = 14.0
ib_parts = [((L, 1.5, 0.22), (0, 0, -1.09)), ((L, 0.16, 1.96), (0, 0, 0)), ((L, 1.5, 0.22), (0, 0, 1.09))]
ibeam = box('PerfilI', None, (0, 0, 1.4 + 1.2), P['ibeam'], segx=56, parts=ib_parts, bevel=0.015)
bend = ibeam.modifiers.new('Bend', 'SIMPLE_DEFORM'); bend.deform_method = 'BEND'; bend.deform_axis = 'Y'; bend.angle = 0
twist = ibeam.modifiers.new('Twist', 'SIMPLE_DEFORM'); twist.deform_method = 'TWIST'; twist.deform_axis = 'X'; twist.angle = 0
a_ibeam = empty('a_ibeam', (5.5, -0.8, 1.2), ibeam)
a_ibeam_mid = empty('a_ibeam_mid', (0, -0.8, -1.2), ibeam)

# setas de carga
arrows = []
for i, x in enumerate((-4.2, 0, 4.2)):
    ar = empty(f'Seta{i}', (x, 0, 120))
    prim('cone', f'SetaPonta{i}', (0, 0, 0.75), P['load'], ar, rot=(math.pi, 0, 0), vertices=8, radius1=0.9, depth=1.5)
    prim('cyl', f'SetaHaste{i}', (0, 0, 2.9), P['load'], ar, vertices=8, radius=0.36, depth=2.9)
    arrows.append(ar)
a_load = empty('a_load', (0, -0.5, 3.0), arrows[1])

# ------------------------------------------------------------------ viga caixão (solução)
root = empty('VigaRoot', (0, 0, 0))
W_FL, T_FL, H_WEB, T_WEB, Y_WEB = 2.5, 0.26, 2.5, 0.18, 0.82
Z0 = 1.46  # topo da placa do apoio
zb = Z0 + T_FL / 2
zw = Z0 + T_FL + H_WEB / 2
zt = Z0 + T_FL + H_WEB + T_FL / 2
TOP = Z0 + 2 * T_FL + H_WEB
mesa_inf = box('MesaInferior', (L, W_FL, T_FL), (0, 0, zb), P['flange'], segx=8, parent=root)
mesa_sup = box('MesaSuperior', (L, W_FL, T_FL), (0, 0, zt), P['flange'], segx=8, parent=root)
almas = []
for sy in (-1, 1):
    al = box(f'Alma{sy}', (L, T_WEB, H_WEB), (0, sy * Y_WEB, zw), P['web'], segx=60, segz=8, parent=root)
    wv = al.modifiers.new('Ondula', 'WAVE')
    wv.use_x, wv.use_y = True, False
    wv.use_normal = True; wv.use_normal_x = False; wv.use_normal_y = True; wv.use_normal_z = False
    wv.height = 0.0; wv.width = 1.6; wv.narrowness = 1.2; wv.speed = 0.03; wv.start_position_x = -7
    almas.append(al)
a_mesa_sup = empty('a_mesa_sup', (4.5, -1.25, 0.13), mesa_sup)
a_mesa_inf = empty('a_mesa_inf', (3.0, -1.25, -0.13), mesa_inf)
a_alma_f = empty('a_alma_f', (-3.0, -0.09, 0.4), almas[0])
a_alma_t = empty('a_alma_t', (6.6, 0.0, 1.0), almas[1])
a_secao = empty('a_secao', (7.0, 0, zw), root)
a_topo = empty('a_topo', (0, 0, TOP + 0.1), root)
a_flamb = empty('a_flamb', (1.5, -0.1, 0.0), almas[0])

# diafragmas (com furo de inspeção)
diafs = []
hw, hh = 0.32, 0.45
inner_w = 2 * Y_WEB - T_WEB  # vão livre entre almas
for i, x in enumerate((-6, -4, -2, 0, 2, 4, 6)):
    parts = [((0.14, inner_w, (H_WEB - 2 * hh) / 2), (0, 0, hh + (H_WEB / 2 - hh) / 2)),
             ((0.14, inner_w, (H_WEB - 2 * hh) / 2), (0, 0, -hh - (H_WEB / 2 - hh) / 2)),
             ((0.14, (inner_w - 2 * hw) / 2, 2 * hh), (0, hw + (inner_w / 2 - hw) / 2, 0)),
             ((0.14, (inner_w - 2 * hw) / 2, 2 * hh), (0, -hw - (inner_w / 2 - hw) / 2, 0))]
    d = box(f'Diafragma{i}', None, (x, 0, zw), P['diaph'], parts=parts, bevel=0.012, parent=root)
    diafs.append(d)
a_diaf = empty('a_diaf', (0, -0.3, H_WEB / 2 + 0.05), diafs[3])

# cordões de solda (4 cantos) + cabeçotes de solda com faíscas
seams = []
for sy in (-1, 1):
    for zz in (Z0 + T_FL + 0.06, Z0 + T_FL + H_WEB - 0.06):
        sm = box(f'Solda{sy}_{zz:.1f}', (L, 0.13, 0.13), (-L / 2, sy * (Y_WEB + T_WEB / 2 + 0.05), zz), P['weld'], segx=1, bevel=0.03, parent=root)
        sm.data.transform(__import__('mathutils').Matrix.Translation((L / 2, 0, 0)))
        seams.append(sm)
heads = []
for zz in (Z0 + T_FL + 0.06, Z0 + T_FL + H_WEB - 0.06):
    hd = prim('ico', f'Tocha{zz:.1f}', (-L / 2, -(Y_WEB + T_WEB / 2 + 0.12), zz), P['spark'], root, subdivisions=1, radius=0.12)
    heads.append(hd)
a_solda = empty('a_solda', (0, 0, 0.1), heads[1])

# scanner de ultrassom (anel ciano)
scan = empty('Scanner', (-7.6, 0, zw), root)
for nm, sz, off in [('S1', (0.12, 3.0, 0.14), (0, 0, 1.75)), ('S2', (0.12, 3.0, 0.14), (0, 0, -1.75)),
                    ('S3', (0.12, 0.14, 3.6), (0, -1.5, 0)), ('S4', (0.12, 0.14, 3.6), (0, 1.5, 0))]:
    box(f'Scan{nm}', sz, off, P['scan'], parent=scan, bevel=0)
prim('cube', 'ScanPlano', (0, 0, 0), P['scan'], scan, scale=(0.02, 1.45, 1.72))
a_scan = empty('a_scan', (0, -1.5, 1.75), scan)

# olhais de içamento
lugs = []
for sx in (-1, 1):
    lg = empty(f'Olhal{sx}', (sx * 3.6, 0, TOP), root)
    box(f'OlhalPlaca{sx}', (0.7, 0.1, 0.7), (0, 0, 0.35), P['red'], parent=lg, bevel=0.02)
    prim('torus', f'OlhalFuro{sx}', (0, 0, 0.45), P['dark'], lg, rot=(math.pi / 2, 0, 0), major_segments=10, minor_segments=5, major_radius=0.16, minor_radius=0.05)
    lugs.append(lg)
a_olhal = empty('a_olhal', (0, 0, 0.8), lugs[1])

# módulos (viga segmentada para transporte)
def module(name, x0, x1, parent=None, loc=(0, 0, 0)):
    lx = x1 - x0; cx = (x0 + x1) / 2
    parts = [((lx, W_FL, T_FL), (0, 0, zb)), ((lx, W_FL, T_FL), (0, 0, zt))]
    o_fl = box(name, None, loc, P['flange'], parts=parts, parent=parent)
    o_wb = box(name + '_almas', None, (0, 0, 0), P['web'], parts=[((lx, T_WEB, H_WEB), (0, sy * Y_WEB, zw)) for sy in (-1, 1)], parent=o_fl)
    o_d = box(name + '_tampa', None, (0, 0, 0), P['diaph'], parts=[((0.14, inner_w, H_WEB), (sx * (lx / 2 - 0.07), 0, zw)) for sx in (-1, 1)], parent=o_fl, bevel=0.01)
    return o_fl, cx

mods = []
for i, (x0, x1) in enumerate([(-7, -7 + L / 3), (-7 + L / 3, 7 - L / 3), (7 - L / 3, 7)]):
    m, cx = module(f'Modulo{i}', x0, x1)
    m.location = (cx, 0, 0)
    mods.append(m)
a_mod = empty('a_mod', (0, -1.25, zt + 0.1), mods[1])

# ------------------------------------------------------------------ carreta
truck = empty('Carreta', (60, 18, 0))
truck.rotation_euler.z = math.pi  # cabine à frente no sentido -X
box('CavaloCab', (2.6, 2.6, 2.6), (7.6, 0, 2.1), P['truck'], parent=truck, bevel=0.1)
box('CavaloVidro', (0.1, 2.2, 1.0), (8.92, 0, 2.7), P['glass'], parent=truck, bevel=0)
box('CavaloChassi', (5, 2.4, 0.5), (6.6, 0, 0.9), P['dark'], parent=truck, bevel=0.03)
box('Prancha', (11, 2.9, 0.35), (-0.5, 0, 1.0), P['dark'], parent=truck, bevel=0.03)
box('PranchaPescoco', (2, 2.6, 0.4), (5.0, 0, 1.4), P['dark'], parent=truck, bevel=0.03)
for j, x in enumerate([8.0, 6.0, 5.0] + [-2.8 + i * 1.1 for i in range(6)]):
    for sy in (-1, 1):
        prim('cyl', f'Roda{j}{sy}', (x, sy * 1.2, 0.5), P['dark'], truck, rot=(math.pi / 2, 0, 0), vertices=10, radius=0.5, depth=0.45)
tm, _ = module('ModuloCarreta', -2.33, 2.33, parent=truck, loc=(-0.5, 0, 1.17 - Z0))
for sx in (-1, 1):  # faixas de amarração
    box(f'Cinta{sx}', (0.12, 2.7, 3.1), (-0.5 + sx * 1.4, 0, 2.75), P['crane'], parent=truck, bevel=0)
prim('cube', 'Placa', (9.0, 0, 3.6), P['crane'], truck, scale=(0.05, 1.2, 0.3))
a_truck = empty('a_truck', (-0.5, -1.4, 4.4), truck)

# ------------------------------------------------------------------ guindaste (esteiras + lança treliçada)
CR = (0, 13.0, 0)
crane = empty('Guindaste', CR)
for sx in (-1, 1):
    box(f'Esteira{sx}', (2.0, 8.5, 1.4), (sx * 2.4, 0, 0.7), P['dark'], parent=crane, bevel=0.15)
box('Giro', (4.6, 5.6, 0.6), (0, 0.5, 1.7), P['dark'], parent=crane)
box('Casa', (4.2, 6.5, 2.6), (0, 1.2, 3.3), P['crane'], parent=crane, bevel=0.08)
box('Cabine', (1.4, 1.8, 2.0), (-2.2, -1.6, 3.0), P['crane'], parent=crane, bevel=0.06)
box('CabineVidro', (1.45, 0.08, 1.2), (-2.2, -2.52, 3.3), P['glass'], parent=crane, bevel=0)
box('Contrapeso', (4.4, 2.0, 2.4), (0, 4.6, 3.4), P['steel_d'], parent=crane, bevel=0.06)
boom = empty('Lanca', (0, -1.6, 3.4), crane)
BL = 26.0
for sx in (-1, 1):
    for sz in (-1, 1):
        prim('cube', f'LancaBanzo{sx}{sz}', (sx * 0.55, -BL / 2, sz * 0.55), P['crane'], boom, scale=(0.09, BL / 2, 0.09))
for j in range(13):
    yy = -1 - j * 2.0
    for sx in (-1, 1):
        prim('cube', f'LancaDiag{j}{sx}', (sx * 0.55, yy, 0), P['crane'], boom, rot=(math.radians(45 if j % 2 else -45), 0, 0), scale=(0.05, 0.05, 0.78))
    prim('cube', f'LancaTrav{j}', (0, yy, 0.55), P['crane'], boom, scale=(0.55, 0.05, 0.05))
    prim('cube', f'LancaTravB{j}', (0, yy, -0.55), P['crane'], boom, scale=(0.55, 0.05, 0.05))
prim('cyl', 'LancaPonta', (0, -BL, 0), P['dark'], boom, rot=(0, math.pi / 2, 0), vertices=10, radius=0.5, depth=1.3)
tip = empty('LancaTip', (0, -BL, -0.5), boom)
a_lanca = empty('a_lanca', (0.6, -BL * 0.55, 0), boom)
hook = empty('Gancho', (0, 6.5, 12))
box('Moitao', (0.9, 0.5, 1.2), (0, 0, 0.6), P['crane'], parent=hook, bevel=0.06)
prim('torus', 'Anzol', (0, 0, -0.2), P['dark'], hook, rot=(math.pi / 2, 0, 0), major_segments=10, minor_segments=5, major_radius=0.3, minor_radius=0.09)

def rope(name, a, b, radius=0.05):
    r = prim('cyl', name, (0, 0, 0), P['dark'], vertices=6, radius=radius, depth=1.0)
    r.data.transform(__import__('mathutils').Matrix.Translation((0, 0, 0.5)))  # base na origem, cresce em +Z
    r.data.transform(__import__('mathutils').Matrix.Rotation(-math.pi / 2, 4, 'X'))  # agora cresce em +Y
    c = r.constraints.new('COPY_LOCATION'); c.target = a
    s = r.constraints.new('STRETCH_TO'); s.target = b; s.rest_length = 1.0; s.volume = 'NO_VOLUME'
    return r
cabo = rope('Cabo', tip, hook, 0.06)
lug_pts = [empty(f'OlhalPt{i}', (0, 0, 0.5), lg) for i, lg in enumerate(lugs)]
slings = [rope(f'Linga{i}', p, hook, 0.05) for i, p in enumerate(lug_pts)]
crane_objs = [crane, hook, cabo] + slings

# poeira e confete
dusts = []
for i in range(10):
    sx = -1 if i < 5 else 1
    d = prim('ico', f'Poeira{i}', (sx * PEDX + random.uniform(-1.3, 1.3), random.choice((-1.75, 1.75)) + random.uniform(-0.2, 0.2), 1.5), P['dust'], subdivisions=1, radius=random.uniform(0.3, 0.5))
    d.scale = (0.001,) * 3; k(d, 'scale', 0, (0.001,) * 3, 'CONSTANT', frame=1)
    dusts.append(d)

# ================================================================== ANIMAÇÃO
def tl(t):  # atalho
    return t

# --- 0) intro: caldeira gigante, mascote assustado
mas.look(0.0, tilt=-0.45, turn=0.0, dur=0.01)
mas.scared(0.35, hold=1.2)
mas.look(2.4, tilt=-0.6, turn=0.0)
mas.sweat(3.6)
mas.look(5.6, tilt=0.0, turn=0.0)
# --- 1) viga I cai nos apoios
hidden_until(ibeam, 0)
k(ibeam, 'location', 6.05, (0, 0, 22), 'BOUNCE', 'EASE_OUT')
k(ibeam, 'scale', 6.05, (1, 1, 1), 'CONSTANT')
k(ibeam, 'location', 7.0, (0, 0, 2.6))
mas.move(6.08, (7.6, -4.6, 0), rotz=math.radians(50), cut=True)
mas.look(6.08, 0, 0, 0.05)
mas.hop(7.0, 0.2)
# --- 2) carga + flexão
for i, ar in enumerate(arrows):
    k(ar, 'location', 9.2 + 0.08 * i, (ar.location.x, 0, 120), 'BOUNCE', 'EASE_OUT')
    k(ar, 'location', 9.9 + 0.08 * i, (ar.location.x, 0, 3.85))
k(ibeam, 'modifiers["Bend"].angle', 10.3, 0.0, 'QUAD', 'EASE_IN')
k(ibeam, 'modifiers["Bend"].angle', 11.15, math.radians(-26), 'ELASTIC', 'EASE_OUT')
k(ibeam, 'modifiers["Bend"].angle', 12.0, math.radians(-22))
k(ibeam, 'location', 10.3, (0, 0, 2.6))
k(ibeam, 'location', 11.15, (0, 0, 2.15))
for i, ar in enumerate(arrows):
    dz = -0.45 - (0.4 if i == 1 else 0.0)
    k(ar, 'location', 10.3, (ar.location.x, 0, 3.85))
    k(ar, 'location', 11.15, (ar.location.x, 0, 3.85 + dz))
mas.scared(11.15, 0.8)
# --- 3) torção (perfil aberto)
k(ibeam, 'modifiers["Twist"].angle', 12.9, 0.0, 'QUAD', 'EASE_IN')
k(ibeam, 'modifiers["Twist"].angle', 14.05, math.radians(55), 'ELASTIC', 'EASE_OUT')
k(ibeam, 'modifiers["Twist"].angle', 14.6, math.radians(50))
for i, ar in enumerate(arrows):
    k(ar, 'location', 14.6, (ar.location.x, 0, ar.location.z), 'BACK', 'EASE_IN')
    k(ar, 'location', 15.1, (ar.location.x, 0, 120), 'CONSTANT')
mas.scared(14.05, 0.5)
# --- 4) some a viga I
k(ibeam, 'scale', 14.7, (1, 1, 1), 'BACK', 'EASE_IN')
k(ibeam, 'scale', 15.0, (0.001,) * 3, 'CONSTANT')

# --- 5) monta a viga caixão
for o in [mesa_inf, mesa_sup] + almas + diafs + seams + heads + lugs + [scan]:
    hidden_until(o, 0)
k(mesa_inf, 'location', 16.0, (-34, 0, zb), 'BACK', 'EASE_OUT'); k(mesa_inf, 'scale', 16.0, (1, 1, 1), 'CONSTANT')
k(mesa_inf, 'location', 16.6, (0, 0, zb))
k(mesa_sup, 'location', 17.45, (0, 0, 22), 'BACK', 'EASE_OUT'); k(mesa_sup, 'scale', 17.45, (1, 1, 1), 'CONSTANT')
k(mesa_sup, 'location', 17.95, (0, 0, zt + 2.6))
for j, (al, sy) in enumerate(zip(almas, (-1, 1))):
    t0 = (19.25, 19.9)[j] if sy == 1 else 19.25
    t0 = 19.25 if j == 1 else 19.9  # primeiro a de trás, depois a da frente
    k(al, 'location', t0, (0, sy * 16, zw), 'BACK', 'EASE_OUT'); k(al, 'scale', t0, (1, 1, 1), 'CONSTANT')
    k(al, 'location', t0 + 0.5, (0, sy * Y_WEB, zw))
k(mesa_sup, 'location', 22.05, (0, 0, zt + 2.6), 'BOUNCE', 'EASE_OUT')
k(mesa_sup, 'location', 22.55, (0, 0, zt))
mas.hop(18.7); mas.hop(21.4)
mas.celebrate(27.05, jumps=1, period=0.55)
# --- 6) carga volta e almas flambam
for i, ar in enumerate(arrows):
    k(ar, 'location', 27.9 + 0.07 * i, (ar.location.x, 0, 120), 'BOUNCE', 'EASE_OUT')
    k(ar, 'location', 28.5 + 0.07 * i, (ar.location.x, 0, TOP + 0.02))
for al in almas:
    k(al, 'modifiers["Ondula"].height', 30.6, 0.0, 'QUAD', 'EASE_IN')
    k(al, 'modifiers["Ondula"].height', 32.4, 0.22)
    k(al, 'modifiers["Ondula"].height', 33.6, 0.22, 'QUAD', 'EASE_OUT')
    k(al, 'modifiers["Ondula"].height', 34.6, 0.0)
mas.scared(32.42, 0.6)
for i, ar in enumerate(arrows):
    k(ar, 'location', 33.0, (ar.location.x, 0, TOP + 0.02), 'BACK', 'EASE_IN')
    k(ar, 'location', 33.5, (ar.location.x, 0, 120), 'CONSTANT')
# --- 7) abre a tampa e entram os diafragmas
k(mesa_sup, 'location', 33.1, (0, 0, zt), 'BACK', 'EASE_OUT')
k(mesa_sup, 'location', 33.6, (0, 0, zt + 5.5))
for i, d in enumerate(diafs):
    t0 = 33.85 + i * 0.3
    k(d, 'location', t0, (d.location.x, 0, zw + 9), 'BOUNCE', 'EASE_OUT'); k(d, 'scale', t0, (1, 1, 1), 'CONSTANT')
    k(d, 'location', t0 + 0.45, (d.location.x, 0, zw))
mas.hop(36.85)
k(mesa_sup, 'location', 37.15, (0, 0, zt + 5.5), 'BOUNCE', 'EASE_OUT')
k(mesa_sup, 'location', 37.65, (0, 0, zt))
# --- 8) peças soltas chacoalham
for o, amp in [(mesa_sup, 0.12), (almas[0], 0.1), (almas[1], 0.1), (mesa_inf, 0.05)]:
    base = tuple(o.location)
    t = 38.0
    k(o, 'location', t, base, 'LINEAR')
    n = 0
    while t < 39.4:
        t += 0.1; n += 1
        k(o, 'location', t, (base[0] + random.uniform(-amp, amp), base[1] + random.uniform(-amp, amp) * 0.6, base[2] + random.uniform(-amp, amp) * 0.6), 'LINEAR')
    k(o, 'location', 39.6, base)
mas.scared(38.1, 0.7)
# --- 9) solda (cordões crescem) e ultrassom
WS, WE = 40.35, 43.05
for sm in seams:
    k(sm, 'scale', WS - 0.04, (0.001, 1, 1), 'CONSTANT')
    k(sm, 'scale', WS, (0.001, 1, 1), 'LINEAR')
    k(sm, 'scale', WE, (1, 1, 1))
for hd in heads:
    k(hd, 'scale', WS - 0.04, (1, 1, 1), 'CONSTANT')
    k(hd, 'location', WS, (-L / 2, hd.location.y, hd.location.z), 'LINEAR')
    k(hd, 'location', WE, (L / 2, hd.location.y, hd.location.z))
    k(hd, 'scale', WE, (1, 1, 1), 'CONSTANT')
    k(hd, 'scale', WE + 0.05, (0.001,) * 3, 'CONSTANT')
ksock(P['weld'], 'Emission Strength', WS - 0.1, 0.0, 'CONSTANT')
ksock(P['weld'], 'Emission Strength', WS, 6.0, 'CONSTANT')
ksock(P['weld'], 'Emission Strength', WE, 6.0)
ksock(P['weld'], 'Emission Strength', WE + 1.0, 0.0)
# faíscas: sistema de partículas em cada tocha
spark_obj = prim('ico', 'Faisca', (0, 0, -50), P['spark'], subdivisions=1, radius=1.0)
for hd in heads:
    ps = hd.modifiers.new('Faiscas', 'PARTICLE_SYSTEM').particle_system
    st = ps.settings
    st.count = 260; st.frame_start = F(WS); st.frame_end = F(WE); st.lifetime = 10; st.lifetime_random = 0.5
    st.emit_from = 'FACE'; st.normal_factor = 3.0; st.factor_random = 2.5
    st.render_type = 'OBJECT'; st.instance_object = spark_obj; st.particle_size = 0.035; st.size_random = 0.6
    st.effector_weights.gravity = 1.0
    hd.show_instancer_for_render = True
ksock(P['spark'], 'Emission Strength', 0, 12.0)
k(scan, 'scale', 43.25, (0.001,) * 3, 'BACK', 'EASE_OUT')
k(scan, 'scale', 43.5, (1, 1, 1))
k(scan, 'location', 43.3, (-7.6, 0, zw), 'SINE')
k(scan, 'location', 44.55, (7.6, 0, zw))
k(scan, 'scale', 44.6, (1, 1, 1), 'BACK', 'EASE_IN')
k(scan, 'scale', 44.85, (0.001,) * 3, 'CONSTANT')
mas.hop(44.1)
# --- 10) grande demais -> módulos
carro.location = (-40, 16.8, 0)
k(carro, 'location', 44.7, (-40, 16.8, 0), 'LINEAR')
k(carro, 'location', 48.9, (30, 16.8, 0))
mas.scared(46.9, 0.5)
box_parts = [mesa_inf, mesa_sup] + almas + seams
for m in mods:
    vis(m, 0, False, frame=1)
    for ch in m.children: vis(ch, 0, False, frame=1)
SPLIT = 47.5
for o in box_parts + diafs:
    vis(o, 0, True, frame=1); vis(o, SPLIT, False)
for m in mods:
    vis(m, SPLIT, True)
    for ch in m.children: vis(ch, SPLIT, True)
for m, dx in zip(mods, (-1.6, 0, 1.6)):
    k(m, 'location', 47.9, tuple(m.location), 'BACK', 'EASE_OUT')
    k(m, 'location', 48.5, (m.location.x + dx, 0, 0))
mas.hop(48.55)
# --- 11) carreta na estrada
k(truck, 'location', 48.8, (17, 18, 0), 'LINEAR')
k(truck, 'location', 51.0, (-13, 18, 0))
# --- 12) guindaste: corte, viga montada no berço
CUT = 50.92
for m in mods:
    vis(m, CUT, False)
    for ch in m.children: vis(ch, CUT, False)
for o in box_parts + diafs:
    vis(o, CUT, True)
for lg in lugs:
    k(lg, 'scale', CUT, (1, 1, 1), 'CONSTANT')
for o in crane_objs:
    vis(o, 0, False, frame=1); vis(o, CUT, True)
for ch in list(crane.children_recursive) + list(hook.children):
    vis(ch, 0, False, frame=1); vis(ch, CUT, True)
mas.move(CUT, (6.5, -5.5, 0), rotz=math.radians(45), cut=True)
# trajetória: berço (y=6.5) -> sobe -> desloca para y=0 -> desce devagar até os apoios
STAGE_Z = 0.51 - Z0  # base da viga sobre os calços
SLING = 4.0
def ease(x): return x * x * (3 - 2 * x)
def beam_pos(t):
    # (y, z_root)
    if t < 51.85: return 6.5, STAGE_Z
    if t < 53.6: u = ease((t - 51.85) / 1.75); return 6.5, STAGE_Z + u * (3.2 - STAGE_Z)
    if t < 55.6: u = ease((t - 53.6) / 2.0); return 6.5 - 6.5 * u, 3.2
    if t < 58.7: u = (t - 55.6) / 3.1; u = 1 - (1 - u) ** 1.6; return 0.0, 3.2 * (1 - u)
    return 0.0, 0.0
k(root, 'location', 0, (0, 0, 0), 'CONSTANT', frame=1)
k(root, 'location', 0, (0, 0, 0), 'CONSTANT', frame=F(CUT) - 1)
PIV_Y = CR[1] - 1.6
PIV_Z = 3.4
for fr in range(F(CUT), F(END_T) + 1):
    t = (fr - 1) / FPS
    y, z = beam_pos(t)
    k(root, 'location', 0, (0, y, z), 'LINEAR', frame=fr)
    hook_z = TOP + z + SLING
    dist = PIV_Y - y
    ang = math.acos(min(0.99, dist / BL))
    k(boom, 'rotation_euler', 0, (-ang, 0, 0), 'LINEAR', frame=fr)
    tipz = PIV_Z + BL * math.sin(ang)
    k(hook, 'location', 0, (0, y, hook_z), 'LINEAR', frame=fr)
mas.wave_signal(55.8, 58.4)
# pouso + poeira
for i, d in enumerate(dusts):
    t0 = 58.65 + random.uniform(0, 0.08)
    k(d, 'scale', t0, (0.001,) * 3, 'QUAD', 'EASE_OUT')
    k(d, 'location', t0, tuple(d.location), 'QUAD', 'EASE_OUT')
    k(d, 'scale', t0 + 0.35, (1.4, 1.4, 1.0))
    k(d, 'location', t0 + 0.9, (d.location.x * 1.08, d.location.y * 1.5, d.location.z + 0.4))
    k(d, 'scale', t0 + 0.9, (0.001,) * 3, 'CONSTANT')
# --- 13) parabéns: confete + comemoração
mas.celebrate(59.5, jumps=4, period=0.5)
mas.celebrate(62.0, jumps=3, period=0.5)
mas.celebrate(64.0, jumps=3, period=0.5)
mas.celebrate(66.0, jumps=2, period=0.5)
conf_col = bpy.data.collections.new('Confete'); sc.collection.children.link(conf_col)
for i, c in enumerate(['#ffd23f', '#e5484d', '#58a6d6', '#5fae5a', '#ff7a1f', '#ffffff', '#b06ab3']):
    cp = prim('plane', f'ConfPeca{i}', (0, 0, -60), mat(f'conf{i}', c, 0.5, emit=c, emit_strength=0.4), size=1.0)
    cp.scale = (1, 0.5, 1)
    bpy.context.scene.collection.objects.unlink(cp); conf_col.objects.link(cp)
conf_em = prim('plane', 'ConfeteEmissor', (0, -1, 16), None, size=1.0, scale=(14, 8, 1))
ps = conf_em.modifiers.new('Confete', 'PARTICLE_SYSTEM').particle_system
st = ps.settings
st.count = 1400; st.frame_start = F(59.45); st.frame_end = F(60.6); st.lifetime = 400
st.normal_factor = 0.0; st.object_align_factor = (0, 0, -2.0); st.factor_random = 1.2
st.render_type = 'COLLECTION'; st.instance_collection = conf_col; st.use_collection_pick_random = True
st.particle_size = 0.32; st.size_random = 0.4
st.use_rotations = True; st.rotation_mode = 'NONE'; st.rotation_factor_random = 1.0
st.angular_velocity_mode = 'RAND'; st.angular_velocity_factor = 8.0
st.effector_weights.gravity = 0.18; st.drag_factor = 0.4
conf_em.show_instancer_for_render = False
conf_em.hide_viewport = False

# ------------------------------------------------------------------ CÂMERA
cam, tgt = camera_rig()
TT = (0, 0, 2.9)
shots = [
    (0.0, (3.6, -9.5, 1.4), (0, BY, 26), 26, ''),
    (2.4, (3.0, -10.0, 1.1), (0, BY, 33), 21, ''),
    (5.95, (2.4, -11.5, 1.6), (0, BY, 30), 22, ''),
    (6.08, (14, -17, 8.5), (0, 0, 2.4), 30, 'cut'),
    (8.8, (11, -15, 6.0), (0, 0, 2.4), 30, ''),
    (11.5, (6.5, -13.5, 4.0), (0, 0, 2.4), 28, ''),
    (12.4, (13.5, -8.5, 4.8), (1.5, 0, 2.4), 30, ''),
    (14.6, (14.5, -6.5, 4.4), (1.5, 0, 2.4), 30, ''),
    (15.2, (12.5, -15, 8.5), (0, 0, 2.8), 28, ''),
    (18.2, (10.5, -14, 7.5), (0, 0, 3.2), 28, ''),
    (21.6, (8, -13, 5.5), (0, 0, 3.0), 28, ''),
    (22.9, (17.5, -4.2, 4.6), (6.5, 0, 2.9), 36, ''),
    (25.9, (18.5, -2.8, 3.8), (6.8, 0, 2.9), 40, ''),
    (26.55, (11.5, -13.5, 8.5), (0, 0, 3.0), 27, ''),
    (27.7, (9.5, -14, 7.2), (0, 0, 3.0), 27, ''),
    (28.5, (2.5, -12.5, 3.4), (0, 0, 3.0), 27, ''),
    (32.9, (0.5, -11.0, 3.1), (0, 0, 3.0), 27, ''),
    (33.75, (3.0, -7.5, 15), (0, 0, 2.6), 28, ''),
    (37.0, (1.5, -7.0, 14), (0, 0, 2.6), 28, ''),
    (37.9, (10, -12.5, 6.8), (0, 0, 3.0), 28, ''),
    (39.9, (9, -12, 6.0), (0, 0, 3.0), 28, ''),
    (40.35, (-6.5, -8.0, 4.2), (-6.0, -0.9, 2.9), 30, 'lin'),
    (43.05, (6.5, -8.0, 4.2), (6.0, -0.9, 2.9), 30, ''),
    (43.4, (9.5, -10.5, 5.5), (0, 0, 3.0), 28, ''),
    (44.7, (7.5, -11, 5.0), (1.5, 0, 3.0), 28, ''),
    (46.6, (22, -28, 15), (0, 5, 3.0), 28, ''),
    (48.85, (16, -21, 10), (0, 2, 3.0), 28, ''),
    (48.95, (12, 6.0, 3.8), (8, 18, 2.6), 26, 'cut'),
    (50.85, (4, 6.0, 3.6), (-6, 18, 2.6), 26, ''),
    (CUT, (19, -19, 8.0), (0, 3, 9.0), 22, 'cut'),
    (55.6, (15, -21, 10.0), (0, 2, 9.0), 22, ''),
    (55.75, (10, -12.5, 4.4), (0, 0, 3.4), 27, 'cut'),
    (58.7, (8, -11.5, 3.6), (0, 0, 2.6), 27, ''),
    (59.5, (11, -13, 6.0), (0, 0, 3.0), 25, ''),
    (63.5, (0.5, -16, 7.0), (0, 0, 3.4), 25, ''),
    (END_T, (-11, -13, 7.5), (0, 0, 3.4), 25, ''),
]
shots = [(t, l, g, lens * 0.62, m) for t, l, g, lens, m in shots]  # vertical 9:16 pede lente mais aberta
camera_path(cam, tgt, shots)
add_noise(cam, 'location', strength=0.06, scale=40)

# âncoras das etiquetas
anchors = [a_boiler, a_ibeam, a_ibeam_mid, a_load, a_mesa_sup, a_mesa_inf, a_alma_f, a_alma_t, a_secao, a_topo,
           a_flamb, a_diaf, a_solda, a_scan, a_mod, a_truck, a_lanca, a_olhal]
a_apoio = empty('a_apoio', (PEDX, -1.7, 1.2)); anchors.append(a_apoio)
a_carro = empty('a_carro', (0, 0, 1.8), carro); anchors.append(a_carro)

bpy.ops.wm.save_as_mainfile(filepath=OUT_BLEND)
# bake das partículas (render em blocos precisa do cache pronto)
with bpy.context.temp_override(scene=sc):
    bpy.ops.ptcache.bake_all(bake=True)
bpy.ops.wm.save_as_mainfile(filepath=OUT_BLEND)
if OUT_ANCH:
    project_anchors(anchors, 1, sc.frame_end, OUT_ANCH)
print('OK cena salva', OUT_BLEND, 'frames', sc.frame_end)
