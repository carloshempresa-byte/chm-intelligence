"""EP02 — O drum. Monta a cena inteira, anima e salva o .blend.
Uso:  blender -b --factory-startup -P cena_ep02.py -- <saida.blend> [anchors.json]
Tempos (s) amarrados à narração enxugada (audio/narracao_tight.json).
Dados do Carlos usados no visual: drum 320 t, 75 m, 2 guindastes de 700 t (sem marca), içamento na horizontal,
um guindaste em cada ponta, cabos da grossura de uma perna, entra por cima antes de fechar o teto.
Fixação final, sinaleiro e desnível ficam genéricos (ver roteiro)."""
import bpy, sys, os, math, random
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import importlib, lowpoly_lib
importlib.reload(lowpoly_lib)
from lowpoly_lib import *

argv = sys.argv[sys.argv.index('--') + 1:] if '--' in sys.argv else []
OUT_BLEND = argv[0] if argv else '/tmp/ep02.blend'
OUT_ANCH = argv[1] if len(argv) > 1 else None
FONT = os.path.join(HERE, '..', '..', 'identidade-visual', 'assets', 'Montserrat-Black.ttf')
END_T = 64.6
random.seed(7)


def fa(t):  # alinha um tempo de corte ao quadro
    return (F(t) - 1) / FPS


# ------------------------------------------------------------------ limpa/config (igual ao EP01)
bpy.ops.wm.read_factory_settings(use_empty=True)
sc = bpy.context.scene
sc.render.fps = FPS
sc.frame_start = 1
sc.frame_end = F(END_T)
sc.render.resolution_x, sc.render.resolution_y = 1080, 1920
sc.render.engine = 'BLENDER_EEVEE'
ee = sc.eevee
ee.taa_render_samples = 8
ee.use_soft_shadows = True
ee.shadow_cascade_size = '2048'
ee.shadow_cube_size = '1024'
ee.use_gtao = True; ee.gtao_distance = 1.2; ee.gtao_factor = 0.8
ee.use_bloom = True; ee.bloom_threshold = 1.2; ee.bloom_intensity = 0.06; ee.bloom_radius = 5.0
sc.view_settings.view_transform = 'Standard'
sc.render.image_settings.file_format = 'PNG'
sc.render.image_settings.color_mode = 'RGB'
sc.render.use_overwrite = False
sc.render.use_placeholder = True

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
sun_d.shadow_cascade_max_distance = 160; sun_d.shadow_cascade_count = 4

# ------------------------------------------------------------------ paleta (EP01)
P = dict(
    ground=mat('ground', '#e7d6ae', 0.95, spec=0.1), grass=mat('grass', '#a9cf7a', 0.95, spec=0.1),
    concrete=mat('concrete', '#c9c3b8', 0.9, spec=0.15), concrete_d=mat('concrete_d', '#aaa397', 0.9),
    asphalt=mat('asphalt', '#55595f', 0.9), lane=mat('lane', '#ffd23f', 0.6),
    flange=mat('flange', '#2f6fa3', 0.45, spec=0.5), web=mat('web', '#58a6d6', 0.45, spec=0.5),
    load=mat('load', '#e5484d', 0.5),
    boiler=mat('boiler', '#e9e4da', 0.8), steel_d=mat('steel_d', '#3b4a5c', 0.6), red=mat('red', '#d64545', 0.55, spec=0.45),
    white=mat('white', '#f7f7f2', 0.7), crane=mat('crane', '#f5c242', 0.45), dark=mat('dark', '#2a2d33', 0.7),
    cable=mat('cable', '#6b7280', 0.35, metal=0.6, spec=0.6),
    truck=mat('truck', '#e74c3c', 0.45), glass=mat('glass', '#9fd6f2', 0.15), wood=mat('wood', '#b07a46', 0.9),
    tree=mat('tree', '#5fae5a', 0.9), trunk=mat('trunk', '#8a5a3b', 0.9), cone=mat('cone', '#ff7a1f', 0.6),
    dust=mat('dust', '#e8dcc2', 1.0), cloud=mat('cloud', '#ffffff', 1.0, emit='#ffffff', emit_strength=0.3),
    cont1=mat('cont1', '#3e8e7e', 0.7), cont2=mat('cont2', '#c8553d', 0.7),
    ghost=mat('ghost', '#2ee6d6', 0.3, emit='#2ee6d6', emit_strength=1.5, alpha=0.4),
    water=mat('water', '#3d8fd1', 0.2, emit='#3d8fd1', emit_strength=0.25, alpha=0.85),
    steam=mat('steam', '#ffffff', 0.6, emit='#ffffff', emit_strength=0.35, alpha=0.55),
    bubble=mat('bubble', '#e8f6ff', 0.2, emit='#ffffff', emit_strength=0.4),
    inside=mat('inside', '#8f3030', 0.7),
    paper=mat('paper', '#fbfaf5', 0.8), blueprint=mat('blueprint', '#2f6fa3', 0.7), bpline=mat('bpline', '#e6f4fb', 0.6),
    calred=mat('calred', '#e5484d', 0.6), green=mat('green', '#3fbf6f', 0.5),
    sea=mat('sea', '#58a6d6', 0.3, spec=0.6), mapgrass=mat('mapgrass', '#bfe0a0', 0.95),
    band=mat('m_band', '#ffffff', 0.4), bandtxt=mat('m_bandtxt', '#2f6fa3', 0.4),
    bar_bg=mat('bar_bg', '#2a2d33', 0.7), bar_A=mat('bar_A', '#3fbf6f', 0.5, emit='#3fbf6f', emit_strength=0.6),
    bar_B=mat('bar_B', '#3fbf6f', 0.5, emit='#3fbf6f', emit_strength=0.6),
)
GREEN, RED = '#3fbf6f', '#e5484d'


def text3d(name, txt, loc, size, material, parent=None, rot=(math.pi / 2, 0, 0), extrude=0.05):
    cu = bpy.data.curves.new(name, 'FONT'); cu.body = txt; cu.size = size; cu.extrude = extrude
    cu.align_x = 'CENTER'; cu.align_y = 'CENTER'; cu.font = bpy.data.fonts.load(FONT)
    ob = link(bpy.data.objects.new(name, cu)); ob.location = loc; ob.rotation_euler = rot
    ob.data.materials.append(material)
    if parent:
        ob.parent = parent
    return ob


def show_between(objs, t0, t1):
    """Visível só entre t0 e t1 (cortes de cena). Inclui filhos."""
    for o in objs:
        for x in [o] + list(o.children_recursive):
            vis(x, 0, t0 <= 0, frame=1)
            if t0 > 0:
                vis(x, t0, True)
            if t1 is not None:
                vis(x, t1, False)


def sm(a, b, t0, t1, t, lin=False):
    u = min(1.0, max(0.0, (t - t0) / (t1 - t0)))
    if not lin:
        u = u * u * (3 - 2 * u)
    if isinstance(a, (tuple, list)):
        return tuple(x + (y - x) * u for x, y in zip(a, b))
    return a + (b - a) * u


def rope(name, a, b, radius=0.05, material=None):
    import mathutils
    r = prim('cyl', name, (0, 0, 0), material or P['dark'], vertices=8, radius=radius, depth=1.0)
    r.data.transform(mathutils.Matrix.Translation((0, 0, 0.5)))
    r.data.transform(mathutils.Matrix.Rotation(-math.pi / 2, 4, 'X'))
    c = r.constraints.new('COPY_LOCATION'); c.target = a
    s = r.constraints.new('STRETCH_TO'); s.target = b; s.rest_length = 1.0; s.volume = 'NO_VOLUME'
    return r


# ================================================================== CENÁRIO DA OBRA
prim('plane', 'Chao', (0, 0, 0), P['ground'], size=1400)
for i in range(70):
    a = random.uniform(0, 2 * math.pi); r = random.uniform(60, 170)
    x, y = r * math.cos(a), r * math.sin(a) + 20
    prim('cone', f'Grama{i}', (x, y, 0.2), P['grass'], vertices=5, radius1=1.2, depth=0.4)
for i in range(60):
    a = random.uniform(0, 2 * math.pi); r = random.uniform(70, 160)
    x, y = r * math.cos(a), r * math.sin(a) + 20
    s = random.uniform(1.4, 2.6)
    prim('cyl', f'Tronco{i}', (x, y, 1.0 * s), P['trunk'], vertices=5, radius=0.3 * s, depth=2 * s)
    prim('cone', f'Copa{i}', (x, y, 3.6 * s), P['tree'], vertices=6, radius1=1.9 * s, depth=4.5 * s)
for i in range(9):
    x, y, z = random.uniform(-90, 90), random.uniform(90, 170), random.uniform(70, 110)
    for j in range(3):
        prim('ico', f'Nuvem{i}_{j}', (x + j * 6 - 6, y, z + (j == 1) * 2), P['cloud'], subdivisions=1, radius=random.uniform(4.5, 7), scale=(1.3, 1, 0.7))
prim('cube', 'Patio', (0, 22, 0.05), P['concrete_d'], scale=(36, 24, 0.05))
prim('cube', 'ViaObra', (0, -30, 0.03), P['asphalt'], scale=(400, 3.2, 0.03))
for i in range(-40, 41):
    prim('cube', f'ViaFaixa{i}', (i * 6, -30, 0.065), P['lane'], scale=(1.4, 0.12, 0.01))
for c, (x, y, rz) in enumerate([(40, 10, 10), (44, 16, -5), (-42, 12, 20), (-46, 18, 4)]):
    box(f'Cont{c}', (6, 2.4, 2.6), (x, y, 1.3), P['cont1'] if c % 2 else P['cont2'], bevel=0.05).rotation_euler.z = math.radians(rz)

# ------------------------------------------------------------------ caldeira (EP01) com o topo aberto
BY = 40
cald = empty('Caldeira', (0, BY, 0))
box('CaldCorpo', (14, 14, 46), (0, 0, 23), P['boiler'], parent=cald, bevel=0.1)
for j in range(9):
    box(f'CaldFaixa{j}', (14.5, 14.5, 0.6), (0, 0, 4 + j * 5), P['steel_d'], parent=cald, bevel=0.05)
for sx in (-1, 1):
    for sy in (-1, 1):
        box(f'CaldColuna{sx}{sy}', (1.2, 1.2, 52), (sx * 9, sy * 9, 26), P['steel_d'], parent=cald, bevel=0.05)
    box(f'CaldVigaTopo{sx}', (1.0, 19, 1.0), (sx * 9, 0, 51.5), P['steel_d'], parent=cald, bevel=0.04)
box('CaldEscada', (3, 3, 50), (-10.8, -6, 25), P['crane'], parent=cald, bevel=0.05)
box('CaldPrecip', (12, 18, 16), (-22, 4, 8), P['boiler'], parent=cald, bevel=0.1)
box('CaldDuto', (10, 3, 3), (-12, 4, 14), P['steel_d'], parent=cald, bevel=0.05)
chamine = empty('Chamine', (22, BY + 12, 0))
for j in range(8):
    prim('cyl', f'ChamineSeg{j}', (0, 0, 4.5 + j * 9), P['red'] if j % 2 else P['white'], chamine, vertices=12, radius=2.6 - j * 0.12, depth=9)
# teto: 4 faixas + casa de máquinas, caem no fim
ROOF_Z = 53.0
roof = [box(f'Teto{i}', (20, 5, 3), (0, BY - 7.5 + 5 * i, ROOF_Z), P['steel_d'], bevel=0.08) for i in range(4)]
casa = box('CaldCasa', (14, 10, 5), (0, BY, 57.0), P['boiler'], bevel=0.1)
a_topo = empty('a_topo', (0, BY - 9, 52.5))

# ------------------------------------------------------------------ drum
SEAT_Z = 47.7
Y0, Z0 = BY - 14, 1.9
R_D, L_D = 1.6, 13.0


def drum_geom(name, material, parent):
    prim('cyl', name + '_casco', (0, 0, 0), material, parent, rot=(0, math.pi / 2, 0), vertices=20, radius=R_D, depth=L_D)
    for sx in (-1, 1):
        prim('uv', name + f'_tampo{sx}', (sx * L_D / 2, 0, 0), material, parent, segments=20, ring_count=10, radius=R_D, scale=(0.55, 1, 1))


drum = empty('Drum', (0, Y0, Z0))
drum_geom('Drum', P['red'], drum)
for sx in (-1, 1):
    prim('cyl', f'DrumAnel{sx}', (sx * 5.0, 0, 0), P['steel_d'], drum, rot=(0, math.pi / 2, 0), vertices=20, radius=R_D + 0.04, depth=0.25)
for x in (-3.0, 0.0, 3.0):
    prim('cyl', f'DrumBocal{x}', (x, 0, R_D + 0.15), P['steel_d'], drum, vertices=10, radius=0.28, depth=0.5)
lugs = []
for sx in (-1, 1):
    prim('torus', f'DrumPega{sx}', (sx * 5.6, 0, R_D + 0.25), P['dark'], drum, rot=(0, 0, 0), major_segments=10, minor_segments=5, major_radius=0.3, minor_radius=0.1).rotation_euler = (math.pi / 2, 0, math.pi / 2)
    lugs.append(empty(f'DrumPegaPt{sx}', (sx * 5.6, 0, R_D + 0.4), drum))
for sx in (-1, 1):
    box(f'BercoDrum{sx}', (1.6, 3.4, 0.3), (sx * 4.0, Y0, 0.15), P['wood'], bevel=0.02)
a_drum = empty('a_drum', (0, -0.6, R_D * 0.6), drum)
a_drum_ponta = empty('a_drum_ponta', (L_D / 2 + 0.6, -0.4, 0.5), drum)
ghost = empty('DrumFantasma', (0, BY, SEAT_Z))
drum_geom('Fantasma', P['ghost'], ghost)
a_ghost = empty('a_ghost', (0, -1.2, 0.8), ghost)

# ------------------------------------------------------------------ guindastes (sem marca), escala 3


CS = 3.0
BL = 26.0 * CS
PIV_OFF = (0, -1.6 * CS, 3.4 * CS)


def crane(name, loc):
    base = empty(name, loc)
    for sx in (-1, 1):
        box(f'{name}Esteira{sx}', (2.0 * CS, 8.5 * CS, 1.4 * CS), (sx * 2.4 * CS, 0, 0.7 * CS), P['dark'], parent=base, bevel=0.3)
        for j in range(7):
            prim('cyl', f'{name}Roda{sx}{j}', (sx * 2.4 * CS - sx * 3.05, -3.4 * CS + j * 1.13 * CS, 0.7 * CS), P['steel_d'], base, rot=(0, math.pi / 2, 0), vertices=10, radius=0.42 * CS, depth=0.2)
    up = empty(name + 'Giro', (0, 0, 0), base)
    box(f'{name}GiroBase', (4.6 * CS, 5.6 * CS, 0.6 * CS), (0, 0.5 * CS, 1.7 * CS), P['dark'], parent=up)
    box(f'{name}Casa', (4.2 * CS, 6.5 * CS, 2.6 * CS), (0, 1.2 * CS, 3.3 * CS), P['crane'], parent=up, bevel=0.2)
    box(f'{name}Cabine', (1.4 * CS, 1.8 * CS, 2.0 * CS), (-2.2 * CS, -1.6 * CS, 3.0 * CS), P['crane'], parent=up, bevel=0.15)
    box(f'{name}Vidro', (1.45 * CS, 0.08 * CS, 1.2 * CS), (-2.2 * CS, -2.52 * CS, 3.3 * CS), P['glass'], parent=up, bevel=0)
    box(f'{name}Contrapeso', (4.4 * CS, 2.0 * CS, 2.4 * CS), (0, 4.6 * CS, 3.4 * CS), P['steel_d'], parent=up, bevel=0.15)
    box(f'{name}Faixa', (4.25 * CS, 0.3, 0.35 * CS), (0, 1.2 * CS - 3.26 * CS, 3.3 * CS), P['dark'], parent=up, bevel=0)
    boom = empty(name + 'Lanca', PIV_OFF, up)
    hw = 0.75 * CS
    for sx in (-1, 1):
        for sz in (-1, 1):
            prim('cube', f'{name}Banzo{sx}{sz}', (sx * hw, -BL / 2, sz * hw), P['crane'], boom, scale=(0.22, BL / 2, 0.22))
    nseg = 18
    for j in range(nseg):
        yy = -2 - j * (BL - 3) / nseg
        for sx in (-1, 1):
            prim('cube', f'{name}Diag{j}{sx}', (sx * hw, yy, 0), P['crane'], boom, rot=(math.radians(45 if j % 2 else -45), 0, 0), scale=(0.12, 0.12, hw * 1.4))
        prim('cube', f'{name}Trav{j}', (0, yy, hw), P['crane'], boom, scale=(hw, 0.12, 0.12))
        prim('cube', f'{name}TravB{j}', (0, yy, -hw), P['crane'], boom, scale=(hw, 0.12, 0.12))
    prim('cyl', f'{name}Ponta', (0, -BL, 0), P['dark'], boom, rot=(0, math.pi / 2, 0), vertices=10, radius=1.2, depth=2.6)
    tip = empty(name + 'Tip', (0, -BL, -1.2), boom)
    hook = empty(name + 'Gancho', (0, 0, 0))
    box(f'{name}Moitao', (1.6, 1.0, 2.0), (0, 0, 1.6), P['crane'], parent=hook, bevel=0.1)
    prim('torus', f'{name}Anzol', (0, 0, 0.2), P['dark'], hook, rot=(math.pi / 2, 0, 0), major_segments=10, minor_segments=5, major_radius=0.45, minor_radius=0.14)
    cab = rope(name + 'Cabo', tip, hook, 0.12, P['cable'])
    # barra de capacidade (didática, sem números)
    bar = empty(name + 'Barra', (0, 0, 0))
    box(f'{name}BarraFundo', (1.6, 0.4, 10.4), (0, 0.15, 5.2), P['bar_bg'], parent=bar, bevel=0.1)
    fill = box(f'{name}BarraNivel', None, (0, -0.1, 0.2), P['bar_A' if name == 'GA' else 'bar_B'], parts=[((1.2, 0.3, 10.0), (0, 0, 5.0))], parent=bar, bevel=0.04)
    return dict(base=base, up=up, boom=boom, tip=tip, hook=hook, cab=cab, bar=bar, fill=fill)


CA = crane('GA', (-17, BY - 34, 0))
CB = crane('GB', (17, BY - 34, 0))
a_gA = empty('a_gA', (0, -2.5 * CS, 4.6 * CS), CA['up'])
a_gB = empty('a_gB', (0, -2.5 * CS, 4.6 * CS), CB['up'])
a_barA = empty('a_barA', (0, -0.6, 10.6), CA['bar'])
a_barB = empty('a_barB', (0, -0.6, 10.6), CB['bar'])
CA['bar'].location = (-30, BY - 38, 0)
CB['bar'].location = (30, BY - 38, 0)

# lingas: içamento simples (V num gancho só) e tandem (uma por ponta, cabo grosso = perna)
LEG_R = 0.13  # raio da perna do mascote = raio do cabo
sV = [rope(f'LingaV{i}', lugs[i], CA['hook'], LEG_R, P['cable']) for i in range(2)]
sL = rope('LingaA', lugs[0], CA['hook'], LEG_R, P['cable'])
sR = rope('LingaB', lugs[1], CB['hook'], LEG_R, P['cable'])
a_linga = empty('a_linga', (0, 0, 0))

# seta de peso (desnível)
seta = empty('SetaPeso', (0, Y0, 120))
prim('cone', 'SetaPesoPonta', (0, 0, 1.2), P['load'], seta, rot=(math.pi, 0, 0), vertices=8, radius1=1.4, depth=2.4)
prim('cyl', 'SetaPesoHaste', (0, 0, 4.4), P['load'], seta, vertices=8, radius=0.55, depth=4.4)
a_seta = empty('a_seta', (0, -0.8, 5), seta)

# trena (gancho)
trena = box('Trena', None, (-9.8, Y0 - 2.6, 0), P['crane'], parts=[((1.6, 0.3, 1.0), (0, 0, 0.5))], bevel=0.02)
for j in range(0, 56, 4):
    box(f'TrenaMarca{j}', (1.6, 0.34, 0.15), (0, -0.02, j / 56.0), P['dark'], parent=trena, bevel=0)
a_trena = empty('a_trena', (0, -0.3, 1.0), trena)

# prédio de 25 andares (comparação aprovada)
FLOOR_H = (ROOF_Z + 1.5) / 25
predio = []
for i in range(25):
    f = box(f'Andar{i}', (9, 9, FLOOR_H * 0.98), (34, BY - 4, FLOOR_H * (i + 0.5)), P['web'] if i % 2 else P['flange'], bevel=0.06)
    for sx in (-1, 0, 1):
        box(f'Janela{i}{sx}', (1.8, 0.1, FLOOR_H * 0.45), (sx * 2.8, -4.53, 0), P['glass'], parent=f, bevel=0)
    predio.append(f)
a_predio = empty('a_predio', (34, BY - 8.8, ROOF_Z + 1.5))

# cabo de aço de amostra ao lado do mascote (close: cabo = perna)
cabo_am = empty('CaboAmostra', (1.6, Y0 - 4.2, 0))
prim('torus', 'CaboRolo', (0, 0.6, LEG_R), P['cable'], cabo_am, major_segments=24, minor_segments=8, major_radius=0.9, minor_radius=LEG_R)
cpe = prim('cyl', 'CaboPonta', (0.0, -0.45, 0.75), P['cable'], cabo_am, vertices=8, radius=LEG_R, depth=1.5)
a_cabo = empty('a_cabo', (0.0, -0.6, 1.4), cabo_am)

# poeira do pouso
dusts = []
for i in range(10):
    sx = -1 if i < 5 else 1
    d = prim('ico', f'Poeira{i}', (sx * random.uniform(4, 7.5), BY + random.choice((-1.8, 1.8)), 46.3), P['dust'], subdivisions=1, radius=random.uniform(0.5, 0.8))
    d.scale = (0.001,) * 3; k(d, 'scale', 0, (0.001,) * 3, 'CONSTANT', frame=1)
    dusts.append(d)

# ================================================================== CONJUNTOS FORA DA OBRA
# --- escritório: calendário + planta (gancho e "5 meses")
OC = Vector((300, 0, 0)) if 'Vector' in dir() else None
from mathutils import Vector
OC = Vector((300, 0, 0))
prim('plane', 'PisoEsc', OC + Vector((0, 0, 0.01)), P['concrete'], size=40)
mesa = box('Mesa', (8, 4.5, 0.3), OC + Vector((0, 0, 1.3)), P['wood'], bevel=0.05)
for sx in (-1, 1):
    for sy in (-1, 1):
        box(f'MesaPe{sx}{sy}', (0.3, 0.3, 1.2), OC + Vector((sx * 3.7, sy * 2.0, 0.6)), P['dark'], bevel=0.02)
planta = box('Planta', (5.0, 3.2, 0.03), OC + Vector((-0.8, 0.2, 1.47)), P['blueprint'], bevel=0)
for j in range(6):
    box(f'PlantaLinha{j}', (4.2 if j % 2 else 2.6, 0.05, 0.01), (0.2 * (j % 3), -1.2 + j * 0.45, 0.02), P['bpline'], parent=planta, bevel=0)
desenho = empty('PlantaDrum', OC + Vector((-0.8, 0.4, 1.5)))
prim('cyl', 'PlantaDrumC', (0, 0, 0), P['bpline'], desenho, rot=(0, math.pi / 2, 0), vertices=12, radius=0.35, depth=2.6, scale=(1, 1, 0.05))
cal = empty('Calendario', OC + Vector((2.6, 0.6, 1.45)))
box('CalBase', (2.2, 0.8, 0.2), (0, 0, 0.1), P['dark'], parent=cal, bevel=0.03)
box('CalFundo', (2.0, 0.12, 2.4), (0, 0.25, 1.4), P['paper'], parent=cal, bevel=0.02)
pages = []
for i in range(5):
    hinge = empty(f'CalPagina{i}', (0, 0.1 - 0.02 * i, 2.6), cal)
    box(f'CalPag{i}', (1.9, 0.02, 2.2), (0, 0, -1.12), P['paper'], parent=hinge, bevel=0.01)
    box(f'CalPagTopo{i}', (1.9, 0.03, 0.45), (0, -0.01, -0.25), P['calred'], parent=hinge, bevel=0.01)
    for r in range(3):
        for c in range(4):
            box(f'CalDia{i}{r}{c}', (0.28, 0.03, 0.22), (-0.6 + c * 0.4, -0.012, -0.8 - r * 0.42), P['steel_d'], parent=hinge, bevel=0)
    pages.append(hinge)
a_cal = empty('a_cal', (0, -0.3, 2.7), cal)
carimbo = text3d('Aprovado', 'APROVADO', OC + Vector((-0.8, 0.2, 1.56)), 0.62, P['green'], rot=(0, 0, math.radians(-12)), extrude=0.04)
folhas = []
for i in range(4):
    fl = box(f'FolhaVoando{i}', (1.6, 1.1, 0.02), OC + Vector((-8, -2, 4)), P['blueprint'] if i % 2 else P['paper'], bevel=0)
    folhas.append(fl)
office = [mesa, planta, desenho, cal, carimbo] + folhas + [o for o in bpy.data.objects if o.name.startswith('MesaPe') or o.name == 'PisoEsc']

# --- mapa porto -> obra
OM = Vector((-300, 0, 0))
mapa = empty('Mapa', OM); mapa.rotation_euler.z = math.pi / 2
prim('plane', 'MapaTerra', (2, 0, 0.02), P['mapgrass'], mapa, size=30)
prim('plane', 'MapaMar', (-11, 0, 0.04), P['sea'], mapa, size=1, scale=(8, 30, 1))
for j in range(4):
    box(f'MapaCont{j}', (1.0, 0.5, 0.5), (-5.5, -3 + j * 0.8, 0.3), P['cont2'] if j % 2 else P['cont1'], parent=mapa)
box('MapaNavio', (4.0, 1.2, 0.8), (-9.0, -1.0, 0.4), P['dark'], parent=mapa, bevel=0.1)
box('MapaNavioCasa', (1.0, 1.0, 1.0), (-10.2, -1.0, 1.2), P['white'], parent=mapa, bevel=0.05)
ROAD_PTS = [(-5, -1.5), (-1, -1.5), (1, 2.5), (5, 2.5), (7, -2.5), (10.5, -2.5)]
for i, (a, b) in enumerate(zip(ROAD_PTS, ROAD_PTS[1:])):
    mx, my = (a[0] + b[0]) / 2, (a[1] + b[1]) / 2
    ln = math.hypot(b[0] - a[0], b[1] - a[1])
    seg = box(f'MapaEstrada{i}', (ln + 0.6, 0.6, 0.06), (mx, my, 0.05), P['asphalt'], parent=mapa, bevel=0)
    seg.rotation_euler.z = math.atan2(b[1] - a[1], b[0] - a[0])
mini = empty('MapaFabrica', (11.5, -2.5, 0), mapa)
box('MiniCald', (1.4, 1.4, 4.0), (0, 0, 2.0), P['boiler'], parent=mini, bevel=0.05)
prim('cyl', 'MiniChamine', (1.6, 0.8, 3.0), P['red'], mini, vertices=8, radius=0.3, depth=6)
pin_p = text3d('PinPorto', 'PORTO', (-6.5, 3.6, 0.1), 1.6, P['dark'], mapa, rot=(math.radians(60), 0, -math.pi / 2), extrude=0.05)
pin_o = text3d('PinObra', 'OBRA', (11.5, -5.2, 0.1), 1.6, P['dark'], mapa, rot=(math.radians(60), 0, -math.pi / 2), extrude=0.05)
pin_p.hide_render = True; pin_o.hide_render = True  # nomes viram etiquetas 2D (pílulas)
a_porto = empty('a_porto', (-6.0, -2.0, 0.6), mapa)
a_obra = empty('a_obra', (11.5, -2.5, 4.2), mapa)
token = box('MapaCaminhao', (1.2, 0.6, 0.6), (ROAD_PTS[0][0], ROAD_PTS[0][1], 0.35), P['truck'], parent=mapa, bevel=0.08)
a_token = empty('a_token', (0, 0, 0.8), token)

# --- estrada com o caminhão especial
OR = Vector((0, -300, 0))
prim('cube', 'EstradaLonga', OR + Vector((0, 0, 0.03)), P['asphalt'], scale=(260, 4.0, 0.03))
for i in range(-45, 46):
    prim('cube', f'EstrFaixa{i}', OR + Vector((i * 6, 0, 0.065)), P['lane'], scale=(1.4, 0.12, 0.01))
for i in range(80):
    x = random.uniform(-200, 200); y = random.uniform(9, 45) if random.random() < 0.6 else -random.uniform(24, 50)
    s = random.uniform(1.2, 2.2)
    prim('cyl', f'EstrTronco{i}', OR + Vector((x, y, 1.0 * s)), P['trunk'], vertices=5, radius=0.3 * s, depth=2 * s)
    prim('cone', f'EstrCopa{i}', OR + Vector((x, y, 3.6 * s)), P['tree'], vertices=6, radius1=1.9 * s, depth=4.5 * s)
for nm, x in (('PORTO', -86), ('OBRA', 40)):
    pl = empty(f'Placa{nm}', OR + Vector((x, -6.5, 0)))
    for sx in (-1, 1):
        prim('cyl', f'Placa{nm}Poste{sx}', (sx * 1.8, 0, 2.0), P['steel_d'], pl, vertices=6, radius=0.12, depth=4.0)
    box(f'Placa{nm}Chapa', (5.0, 0.15, 1.6), (0, 0, 4.0), P['green'], parent=pl, bevel=0.06)
    text3d(f'Placa{nm}Txt', nm, (0, -0.12, 4.0), 0.95, P['white'], pl, extrude=0.03)
carreta = empty('Carreta', OR + Vector((-110, 1.0, 0)))
box('CavaloCab', (2.6, 2.8, 2.8), (11.6, 0, 2.2), P['truck'], parent=carreta, bevel=0.1)
box('CavaloVidro', (0.1, 2.3, 1.0), (12.92, 0, 2.8), P['glass'], parent=carreta, bevel=0)
box('CavaloChassi', (5, 2.4, 0.5), (10.6, 0, 0.9), P['dark'], parent=carreta, bevel=0.03)
box('Prancha', (17, 3.0, 0.35), (0, 0, 1.0), P['dark'], parent=carreta, bevel=0.03)
for j, x in enumerate([12.0, 10.0, 9.0] + [-7.5 + i * 1.1 for i in range(10)]):
    for sy in (-1, 1):
        prim('cyl', f'Roda{j}{sy}', (x, sy * 1.25, 0.5), P['dark'], carreta, rot=(math.pi / 2, 0, 0), vertices=10, radius=0.5, depth=0.45)
drumT = empty('DrumCarreta', (-0.5, 0, 1.17 + 0.3 + R_D), carreta)
drum_geom('DrumCarreta', P['red'], drumT)
for sx in (-1, 1):
    box(f'CintaC{sx}', (0.18, 3.5, 3.6), (-0.5 + sx * 3.5, 0, 2.9), P['crane'], parent=carreta, bevel=0)
    box(f'BercoC{sx}', (1.2, 2.8, 0.3), (-0.5 + sx * 4.0, 0, 1.3), P['wood'], parent=carreta, bevel=0.02)
a_carreta = empty('a_carreta', (-0.5, -1.0, 4.2), carreta)

# --- corte esquemático do drum (água embaixo, vapor em cima)
OX = Vector((0, 300, 20))
corte = empty('DrumCorte', OX)
import bmesh as _bm
for nm, kind in (('CorteCasco', 'cyl'),):
    ob = prim('cyl', nm, (0, 0, 0), P['red'], corte, rot=(0, math.pi / 2, 0), vertices=32, radius=R_D, depth=L_D)
    bmx = _bm.new(); bmx.from_mesh(ob.data)
    _bm.ops.delete(bmx, geom=[v for v in bmx.verts if (ob.rotation_euler.to_matrix() @ v.co).y < -0.01], context='VERTS')
    bmx.to_mesh(ob.data); bmx.free()
    sol = ob.modifiers.new('Esp', 'SOLIDIFY'); sol.thickness = 0.12
    ob.data.materials.append(P['inside'])
    sol.material_offset = 1
for sx in (-1, 1):
    prim('uv', f'CorteTampo{sx}', (sx * L_D / 2, 0.4, 0), P['red'], corte, segments=20, ring_count=10, radius=R_D, scale=(0.55, 0.75, 1))
agua = box('CorteAgua', (L_D, 0.1, R_D * 0.95), (0, 0, -R_D * 0.95 / 2), P['water'], parent=corte, bevel=0)
vapor = box('CorteVapor', (L_D, 0.1, R_D * 0.9), (0, 0.02, R_D * 0.9 / 2), P['steam'], parent=corte, bevel=0)
nivel = box('CorteNivel', (L_D, 0.12, 0.05), (0, -0.01, 0), P['bpline'], parent=corte, bevel=0)
bolhas = []
for i in range(16):
    b = prim('ico', f'Bolha{i}', (random.uniform(-5.8, 5.8), -0.12, -1.3), P['bubble'], corte, subdivisions=1, radius=random.uniform(0.08, 0.16))
    bolhas.append(b)
nuvens_v = []
for i in range(8):
    b = prim('ico', f'VaporPuff{i}', (random.uniform(-5, 5), -0.12, 0.2), P['steam'], corte, subdivisions=1, radius=random.uniform(0.22, 0.35))
    nuvens_v.append(b)
a_agua = empty('a_agua', (-2.5, -0.2, -0.75), corte)
a_vapor = empty('a_vapor', (2.5, -0.2, 0.8), corte)

# ------------------------------------------------------------------ mascote (Eng. Carlin)
mas = Mascot('Mascote', (4.2, Y0 - 4.5, 0), rotz=math.radians(20))
helmet_band(mas, 'Eng. Carlin', FONT, P['band'], P['bandtxt'])
a_carlin = empty('a_carlin', (0, -0.5, 2.6), mas.pos)
a_perna = empty('a_perna', (0.17, -0.2, 0.45), mas.jump)

# ================================================================== ANIMAÇÃO
# cortes (alinhados ao quadro)
T_MAP, T_SITE0, T_BOIL, T_CORTE, T_PRED, T_ROAD = fa(1.44), fa(2.58), fa(7.43), fa(12.2), fa(14.0), fa(16.84)
T_CRANE, T_TANDEM, T_CABO, T_TILT, T_REW, T_PLAN, T_DIA, T_TOPO, T_FIM = (fa(21.31), fa(31.28), fa(36.6), fa(39.03), fa(43.6),
                                                                         fa(44.84), fa(47.06), fa(51.21), fa(57.24))

# visibilidade por conjunto
show_between(office, 0, T_MAP)
for o in office:
    for x in [o] + list(o.children_recursive):
        vis(x, T_PLAN, True); vis(x, T_DIA, False)
show_between([mapa], T_MAP, T_SITE0)
show_between([corte], T_CORTE, T_PRED)
road_objs = [o for o in bpy.data.objects if o.name.startswith(('Estr', 'Placa', 'Carreta'))]
show_between(road_objs, T_ROAD, T_CRANE)
show_between(predio, T_PRED, T_ROAD)
show_between([ghost], T_BOIL, T_CORTE)
show_between([trena], fa(5.75), T_BOIL)
show_between([CA['base'], CA['hook'], CA['cab'], CA['bar']], T_CRANE, None)
show_between([CB['base'], CB['hook'], CB['cab'], CB['bar']], T_TANDEM, None)
show_between(sV, fa(25.45), T_TANDEM)
show_between([sL, sR], fa(34.42), fa(55.7))
show_between([cabo_am], T_CABO, T_PLAN)
show_between(roof + [casa], fa(55.75), None)
show_between([seta], fa(41.6), T_REW)
for b in (CA['bar'], CB['bar']):
    for x in [b] + list(b.children_recursive):
        vis(x, T_TOPO, False)

# --- 0) gancho: calendário folheia 5 meses, folhas voando
for i, pg in enumerate(pages[::-1]):
    t0 = 0.15 + i * 0.22
    k(pg, 'rotation_euler', t0, (0, 0, 0), 'BACK', 'EASE_IN')
    k(pg, 'rotation_euler', t0 + 0.2, (math.radians(-215), 0, 0))
    # de novo no "foram 5 meses planejando"
    k(pg, 'rotation_euler', 0, (math.radians(-215), 0, 0), 'CONSTANT', frame=F(T_PLAN) - 1)
    k(pg, 'rotation_euler', T_PLAN, (0, 0, 0), 'CONSTANT')
    t1 = 45.1 + i * 0.22
    k(pg, 'rotation_euler', t1, (0, 0, 0), 'BACK', 'EASE_IN')
    k(pg, 'rotation_euler', t1 + 0.2, (math.radians(-215), 0, 0))
for i, fl in enumerate(folhas):
    y0 = -2.2 + i * 1.2
    k(fl, 'location', 0.0, OC + Vector((-9, y0, 4.5 + i * 0.4)), 'LINEAR')
    k(fl, 'location', 1.45, OC + Vector((9, y0 + 1, 3.6 + i * 0.6)))
    k(fl, 'rotation_euler', 0.0, (0.3 * i, 0.2, 0), 'LINEAR')
    k(fl, 'rotation_euler', 1.45, (0.3 * i + 3, 1.2, 2))
k(carimbo, 'scale', 0, (0.001,) * 3, 'CONSTANT', frame=1)
k(carimbo, 'scale', 46.3, (0.001,) * 3, 'CONSTANT')
k(carimbo, 'scale', 46.35, (2.2, 2.2, 2.2), 'BACK', 'EASE_OUT')
k(carimbo, 'scale', 46.6, (1, 1, 1))
# mapa: caminhãozinho porto -> obra
segs = list(zip(ROAD_PTS, ROAD_PTS[1:]))
tot = sum(math.hypot(b[0] - a[0], b[1] - a[1]) for a, b in segs)
for fr in range(F(T_MAP), F(T_SITE0) + 1):
    t = (fr - 1) / FPS
    u = sm(0.0, 1.0, T_MAP + 0.1, T_SITE0 - 0.15, t) * tot
    for a, b in segs:
        ln = math.hypot(b[0] - a[0], b[1] - a[1])
        if u <= ln:
            x = a[0] + (b[0] - a[0]) * u / ln; y = a[1] + (b[1] - a[1]) * u / ln
            ang = math.atan2(b[1] - a[1], b[0] - a[0]); break
        u -= ln
    else:
        x, y = ROAD_PTS[-1]
    token.location = (x, y, 0.35); token.keyframe_insert('location', frame=fr)
    token.rotation_euler = (0, 0, ang); token.keyframe_insert('rotation_euler', frame=fr)
# trena cresce até o topo (75 m)
k(trena, 'scale', fa(5.75), (1, 1, 0.01), 'QUAD', 'EASE_IN_OUT')
k(trena, 'scale', 7.1, (1, 1, ROOF_Z + 1.5))
mas.look(T_SITE0, tilt=0.0, turn=0.2, dur=0.05)
mas.hop(4.2)
mas.look(5.9, tilt=-0.6, turn=0.0)
mas.scared(6.75, hold=0.6)

# --- 1) fantasma do drum pulsa no topo
for t, s in ((T_BOIL, 0.6), (8.1, 3.0), (8.6, 1.2), (9.6, 3.0), (10.6, 1.2), (11.6, 3.0)):
    ksock(P['ghost'], 'Emission Strength', t, s)
# corte: bolhas sobem na água, vapor sobe em cima
for b in bolhas:
    x0 = b.location.x
    t = T_CORTE + random.uniform(0, 0.6)
    k(b, 'location', 0, (x0, -0.12, -1.35), 'LINEAR', frame=F(T_CORTE))
    while t < T_PRED:
        k(b, 'location', t, (x0, -0.12, -1.35), 'CONSTANT')
        k(b, 'location', t + 0.01, (x0, -0.12, -1.35), 'LINEAR')
        k(b, 'location', t + 0.9, (x0 + random.uniform(-0.2, 0.2), -0.12, -0.05))
        t += 0.92
for p_ in nuvens_v:
    x0 = p_.location.x
    t = 12.5 + random.uniform(0, 0.5)
    k(p_, 'location', 0, (x0, -0.12, 0.2), 'LINEAR', frame=F(T_CORTE))
    k(p_, 'scale', 0, (0.001,) * 3, 'CONSTANT', frame=F(T_CORTE))
    while t < T_PRED:
        k(p_, 'location', t, (x0, -0.12, 0.2), 'CONSTANT'); k(p_, 'scale', t, (0.4, 0.4, 0.4), 'CONSTANT')
        k(p_, 'location', t + 0.01, (x0, -0.12, 0.2), 'LINEAR'); k(p_, 'scale', t + 0.01, (0.4, 0.4, 0.4), 'LINEAR')
        k(p_, 'location', t + 1.0, (x0 + 0.4, -0.12, 1.25)); k(p_, 'scale', t + 1.0, (1.2, 1.2, 1.0))
        t += 1.02

# --- 2) prédio cresce andar por andar
for i, f in enumerate(predio):
    t0 = T_PRED + 0.1 + i * 0.065
    pop_in(f, t0, 0.18)
mas.move(T_PRED, (27, BY - 19, 0), rotz=math.radians(-20), cut=True)
mas.look(T_PRED, tilt=-0.5, turn=0.0, dur=0.05)
mas.look(15.4, tilt=-0.75, turn=0.0)
mas.sweat(15.7)

# --- 3) estrada: caminhão especial, dia e noite (2 meses)
k(carreta, 'location', T_ROAD, OR + Vector((-95, 1.0, 0)), 'LINEAR')
k(carreta, 'location', T_CRANE, OR + Vector((32, 1.0, 0)))
mas.move(T_ROAD, OR + Vector((44, -7.5, 0)), rotz=math.radians(-35), cut=True)
mas.look(T_ROAD, 0, 0, 0.05)
mas.wave_signal(19.6, 21.0)
DAY_S, NIGHT_S = 0.9, 0.38
for t, night in ((T_ROAD, 0), (17.3, 0), (17.7, 1), (18.2, 1), (18.6, 0), (19.0, 0), (19.4, 1), (19.8, 1), (20.2, 0)):
    bg.inputs['Strength'].default_value = NIGHT_S if night else DAY_S
    bg.inputs['Strength'].keyframe_insert('default_value', frame=F(t))
    sun_d.energy = 0.9 if night else 3.3
    sun_d.keyframe_insert('energy', frame=F(t))
    for el, cday, cnight in ((ramp.color_ramp.elements[0], '#e6f4fb', '#2c3e66'), (ramp.color_ramp.elements[1], '#6fbde8', '#141b33')):
        el.color = hexrgb(cnight if night else cday)
        el.keyframe_insert('color', frame=F(t))

# --- 4..10) guindastes, ganchos e drum (cinemática assada quadro a quadro)
S = 5.0  # altura das lingas acima do ponto de pega
A_IDLE = Vector((-9, BY - 22, 16)); B_IDLE = Vector((9, BY - 22, 16))
A0 = Vector((-17, BY - 34, 0)); B0 = Vector((17, BY - 34, 0))
TILT = math.radians(14)


def drum_state(t):
    """(y, z, roty) do drum."""
    if t < 25.9:
        return Y0, Z0, 0.0
    if t < T_TANDEM:
        return Y0, sm(Z0, 22.0, 26.0, 29.3, t), 0.0
    if t < T_TILT:
        return Y0, sm(Z0, Z0 + 1.0, 35.57, 36.4, t), 0.0
    if t < T_REW:
        z = sm(Z0 + 1.0, Z0 + 4.0, 39.05, 39.9, t) + sm(0, 2.5, 39.95, 41.7, t)
        return Y0, z, sm(0.0, TILT, 39.95, 41.7, t)
    if t < 47.1:
        zE = Z0 + 6.5
        return Y0, sm(zE, Z0 + 1.0, T_REW + 0.05, 44.6, t, lin=True), sm(TILT, 0.0, T_REW + 0.05, 44.6, t, lin=True)
    top = 58.8
    if t < 54.3:
        return sm(Y0, BY, 52.9, 54.2, t), sm(Z0 + 1.0, top, 47.1, 52.9, t), 0.0
    return BY, sm(top, SEAT_Z, 54.3, 55.5, t), 0.0


def lug_world(y, z, th, sx):
    x0, z0 = sx * 5.6, R_D + 0.4
    return Vector((x0 * math.cos(th) + z0 * math.sin(th), y, z - x0 * math.sin(th) + z0 * math.cos(th)))


def hooks(t):
    y, z, th = drum_state(t)
    top_c = Vector((0, y, z + R_D + 0.4 + S))
    lL, lR = lug_world(y, z, th, -1) + Vector((0, 0, S)), lug_world(y, z, th, 1) + Vector((0, 0, S))
    # gancho A
    if t < 24.0:
        hA = A_IDLE
    elif t < 25.5:
        hA = Vector(sm(tuple(A_IDLE), tuple(Vector((0, Y0, Z0 + R_D + 0.4 + S))), 24.0, 25.4, t))
    elif t < T_TANDEM:
        hA = top_c
    elif t < 33.6:
        hA = Vector(sm(tuple(A_IDLE), tuple(lL), T_TANDEM + 0.1, 33.6, t))
    elif t < 55.6:
        hA = lL
    else:
        hA = Vector(sm(tuple(lL), tuple(lL + Vector((-2, -4, 10))), 55.6, 57.0, t))
    # gancho B
    if t < 32.6:
        hB = B_IDLE
    elif t < 34.3:
        hB = Vector(sm(tuple(B_IDLE), tuple(lR), 32.6, 34.3, t))
    elif t < 55.6:
        hB = lR
    else:
        hB = Vector(sm(tuple(lR), tuple(lR + Vector((2, -4, 10))), 55.6, 57.0, t))
    return hA, hB


def base_state(t, which):
    if which == 'A':
        x = sm(-62.0, A0.x, T_CRANE, T_CRANE + 0.9, t)
        x = x + (math.sin((t - T_CRANE - 0.9) * 18) * 0.5 * max(0, 1 - (t - T_CRANE - 0.9) / 0.4) if t > T_CRANE + 0.9 else 0)
        rx, dz = 0.0, 0.0
        if 29.4 <= t < T_TANDEM:
            rx = -sm(0, math.radians(5), 29.4, 30.1, t) + math.sin(t * 22) * math.radians(0.6)
            dz = sm(0, 1.0, 29.4, 30.1, t)
        return Vector((x, A0.y, dz)), rx, 0.0
    x = sm(62.0, B0.x, T_TANDEM + 0.1, 32.5, t)
    rx = 0.0; wob = 0.0
    if 41.9 <= t < T_REW:
        e = sm(0, 1, 41.9, 42.4, t)
        rx = math.sin(t * 25) * math.radians(1.2) * e
        wob = math.sin(t * 19) * 0.02 * e
    return Vector((x, B0.y, 0)), rx, wob


def kk(ob, path, val, fr):
    setattr(ob, path, val)
    ob.keyframe_insert(path, frame=fr)


def aim(cr, base, rx, wob, hook, fr):
    kk(cr['base'], 'location', tuple(base), fr)
    kk(cr['base'], 'rotation_euler', (rx, 0, 0), fr)
    d = hook - base
    th = math.atan2(d.x, -d.y)
    kk(cr['up'], 'rotation_euler', (0, 0, th + wob), fr)
    horiz = math.hypot(d.x, d.y) - abs(PIV_OFF[1])
    ang = math.acos(max(-0.99, min(0.99, horiz / BL)))
    kk(cr['boom'], 'rotation_euler', (-ang, 0, 0), fr)
    kk(cr['hook'], 'location', tuple(hook), fr)


for fr in range(1, F(END_T) + 1):
    t = (fr - 1) / FPS
    y, z, th = drum_state(t)
    kk(drum, 'location', (0, y, z), fr)
    kk(drum, 'rotation_euler', (0, th, 0), fr)
    hA, hB = hooks(t)
    bA, rxA, _ = base_state(t, 'A')
    bB, rxB, wB = base_state(t, 'B')
    aim(CA, bA, rxA, 0.0, hA, fr)
    aim(CB, bB, rxB, wB, hB, fr)

# barras de capacidade (sem números): nível + cor
def bar(fill, m, t, lvl, col, ip='BEZIER'):
    k(fill, 'scale', t, (1, 1, max(0.02, lvl)), ip)
    ksock(m, 'Base Color', t, hexrgb(col), ip)
    ksock(m, 'Emission', t, hexrgb(col), ip)


bar(CA['fill'], P['bar_A'], 0.0, 1.0, GREEN)
bar(CA['fill'], P['bar_A'], 26.0, 1.0, GREEN)
bar(CA['fill'], P['bar_A'], 27.6, 0.45, '#f5c242')
bar(CA['fill'], P['bar_A'], 29.3, 0.05, RED)
bar(CA['fill'], P['bar_A'], T_TANDEM - 0.05, 0.05, RED, 'CONSTANT')
bar(CA['fill'], P['bar_A'], T_TANDEM, 0.6, GREEN)
bar(CB['fill'], P['bar_B'], 0.0, 0.6, GREEN)
for fill, m, lvl, col in ((CA['fill'], P['bar_A'], 0.95, GREEN), (CB['fill'], P['bar_B'], 0.05, RED)):
    bar(fill, m, 39.95, 0.6, GREEN)
    bar(fill, m, 41.7, lvl, col)
    bar(fill, m, T_REW + 0.05, lvl, col)
    bar(fill, m, 44.6, 0.6, GREEN)
    bar(fill, m, 47.1, 0.6, GREEN)
    bar(fill, m, 51.0, 0.62, GREEN)

# seta de peso: cai no meio e escorrega para o lado do guindaste B
def drum_top_at(t, xoff):
    y, z, th = drum_state(t)
    return (xoff * math.cos(th), y, z - xoff * math.sin(th) + R_D + 0.1)
_p = drum_top_at(41.6, 0.0)
k(seta, 'location', 41.6, (_p[0], _p[1], _p[2] + 30), 'BOUNCE', 'EASE_OUT')
k(seta, 'location', 42.0, drum_top_at(42.0, 0.0))
k(seta, 'location', 42.75, drum_top_at(42.75, 5.0), 'QUAD', 'EASE_IN')
k(seta, 'location', 43.55, drum_top_at(43.55, 5.0))
k(seta, 'rotation_euler', 42.0, (0, TILT, 0), 'CONSTANT')

# mascote nas cenas da obra
mas.move(T_CRANE, (-4.5, Y0 - 8.5, 0), rotz=math.radians(-15), cut=True)
mas.look(T_CRANE, 0, 0, 0.05)
mas.look(22.0, tilt=-0.35, turn=-0.4)
mas.hop(24.17)
mas._arms(24.2, -0.18, 2.6, 'BACK', 'EASE_OUT'); mas._arms(24.85, -0.18, 2.6); mas._rest_arms(25.05)
mas.scared(25.05, 0.4)
mas.look(26.0, tilt=-0.6, turn=-0.3)
mas.scared(30.0, 0.9)
mas.move(T_TANDEM, (3.5, Y0 - 6.5, 0), rotz=math.radians(10), cut=True)
mas.look(T_TANDEM, tilt=-0.3, turn=0.0, dur=0.05)
mas.hop(34.5)
mas.move(T_CABO, (0.2, Y0 - 4.6, 0), rotz=math.radians(-10), cut=True)
mas.look(T_CABO, tilt=0.15, turn=-0.5, dur=0.05)
mas._arms(36.9, -0.18, 1.3, 'BACK', 'EASE_OUT'); mas._arms(38.3, -0.18, 1.3)
mas.look(37.8, tilt=0.35, turn=0.3)
mas._rest_arms(38.7)
mas.move(T_TILT, (2.5, Y0 - 9.0, 0), rotz=math.radians(15), cut=True)
mas.look(T_TILT, tilt=-0.35, turn=0.0, dur=0.05)
mas.scared(41.75, 1.2)
mas.sweat(42.6)
mas.move(T_PLAN, OC + Vector((-4.9, -0.8, 0)), rotz=math.radians(115), cut=True)
mas.look(T_PLAN, tilt=0.35, turn=0.25, dur=0.05)
mas.hop(46.35)
mas.move(T_DIA, (-2.6, Y0 - 12.0, 0), rotz=math.radians(200), cut=True)
mas.look(T_DIA, tilt=-0.35, turn=0.0, dur=0.05)
mas.wave_signal(47.4, 51.0)
mas.look(49.5, tilt=-0.6, turn=0.0)
mas.move(T_FIM, (8.0, BY + 7.6, ROOF_Z + 1.5), rotz=math.radians(160), cut=True)
mas.look(T_FIM, 0, 0, 0.05)
mas.celebrate(57.3, jumps=4, period=0.5)
mas.celebrate(59.6, jumps=3, period=0.5)
mas.celebrate(61.4, jumps=3, period=0.5)
mas.celebrate(63.2, jumps=2, period=0.5)

# pouso do drum: poeira; teto cai em faixas; casa de máquinas por último
for i, d in enumerate(dusts):
    t0 = 55.45 + random.uniform(0, 0.08)
    k(d, 'scale', t0, (0.001,) * 3, 'QUAD', 'EASE_OUT')
    k(d, 'location', t0, tuple(d.location), 'QUAD', 'EASE_OUT')
    k(d, 'scale', t0 + 0.35, (1.4, 1.4, 1.0))
    k(d, 'location', t0 + 0.9, (d.location.x * 1.1, BY + (d.location.y - BY) * 1.6, d.location.z + 0.6))
    k(d, 'scale', t0 + 0.9, (0.001,) * 3, 'CONSTANT')
for r in roof + [casa]:
    k(r, 'location', 0, (r.location.x, r.location.y, r.location.z + 30), 'CONSTANT', frame=1)
    r.location.z -= 30
for i, r in enumerate(roof):
    t0 = 55.8 + i * 0.17
    k(r, 'location', t0, (0, r.location.y, ROOF_Z + 30), 'BOUNCE', 'EASE_OUT')
    k(r, 'location', t0 + 0.4, (0, r.location.y, ROOF_Z))
k(casa, 'location', 56.55, (0, BY, 57 + 30), 'BOUNCE', 'EASE_OUT')
k(casa, 'location', 56.95, (0, BY, 57.0))

# confete
conf_col = bpy.data.collections.new('Confete'); sc.collection.children.link(conf_col)
for i, c in enumerate(['#ffd23f', '#e5484d', '#58a6d6', '#5fae5a', '#ff7a1f', '#ffffff', '#b06ab3']):
    cp = prim('plane', f'ConfPeca{i}', (0, 0, -60), mat(f'conf{i}', c, 0.5, emit=c, emit_strength=0.4), size=1.0)
    cp.scale = (1, 0.5, 1)
    sc.collection.objects.unlink(cp); conf_col.objects.link(cp)
conf_em = prim('plane', 'ConfeteEmissor', (2, BY + 6, 74), None, size=1.0, scale=(16, 12, 1))
ps = conf_em.modifiers.new('Confete', 'PARTICLE_SYSTEM').particle_system
st = ps.settings
st.count = 1600; st.frame_start = F(57.2); st.frame_end = F(58.4); st.lifetime = 400
st.normal_factor = 0.0; st.object_align_factor = (0, 0, -2.0); st.factor_random = 1.2
st.render_type = 'COLLECTION'; st.instance_collection = conf_col; st.use_collection_pick_random = True
st.particle_size = 0.45; st.size_random = 0.4
st.use_rotations = True; st.rotation_mode = 'NONE'; st.rotation_factor_random = 1.0
st.angular_velocity_mode = 'RAND'; st.angular_velocity_factor = 8.0
st.effector_weights.gravity = 0.18; st.drag_factor = 0.4
conf_em.show_instancer_for_render = False

# ================================================================== CÂMERA
cam, tgt = camera_rig()
TOPC = (0, BY, 50)
def carx(t):
    return sm(-95.0, 32.0, T_ROAD, T_CRANE, t, lin=True)


shots = [
    # 0) gancho: calendário, mapa, drum + trena subindo
    (0.0, OC + Vector((3.8, -7.5, 3.4)), OC + Vector((1.2, 0.3, 1.9)), 19, ''),
    (T_MAP - 0.04, OC + Vector((3.0, -6.8, 3.1)), OC + Vector((1.6, 0.4, 2.0)), 20, ''),
    (T_MAP, OM + Vector((0.0, -15.0, 21.0)), OM + Vector((0.0, 1.5, 0.0)), 15, 'cut'),
    (T_SITE0 - 0.04, OM + Vector((0.0, -13.0, 18.5)), OM + Vector((0.0, 2.0, 0.0)), 15, ''),
    (T_SITE0, (12.0, Y0 - 16.5, 3.4), (1.5, Y0 - 1.0, 2.2), 15, 'cut'),
    (5.7, (11.0, Y0 - 15.0, 3.0), (-2.0, Y0 - 1.0, 2.6), 15, ''),
    (7.0, (14.0, Y0 - 22.0, 66.0), (-4.0, BY - 12.0, 28.0), 14, ''),
    (T_BOIL - 0.04, (14.5, Y0 - 23.0, 69.0), (-2.0, BY - 14.0, 20.0), 14, ''),
    # 1) caldeira com o topo aberto e o fantasma do drum
    (T_BOIL, (34.0, BY - 92.0, 36.0), (0.0, BY, 36.0), 15, 'cut'),
    (10.4, (26.0, BY - 74.0, 44.0), (0.0, BY, 42.0), 15, ''),
    (T_CORTE - 0.04, (18.0, BY - 50.0, 52.0), (0.0, BY, 47.0), 15, ''),
    # corte esquemático (visto em perspectiva, de uma ponta)
    (T_CORTE, OX + Vector((-8.5, -7.0, 1.8)), OX + Vector((1.5, 0.0, -0.2)), 17, 'cut'),
    (T_PRED - 0.04, OX + Vector((-7.0, -7.6, 1.2)), OX + Vector((1.5, 0.0, -0.2)), 17, ''),
    # 2) prédio de 25 andares
    (T_PRED, (58.0, BY - 62.0, 8.0), (16.0, BY, 26.0), 15, 'cut'),
    (T_ROAD - 0.04, (54.0, BY - 66.0, 14.0), (16.0, BY, 28.0), 15, ''),
    # 3) estrada: câmera acompanha o caminhão
    (T_ROAD, OR + Vector((carx(T_ROAD) + 12, -16.0, 5.0)), OR + Vector((carx(T_ROAD) + 3, 1.0, 2.2)), 15, 'cut'),
    (T_CRANE - 0.04, OR + Vector((carx(T_CRANE) + 10, -16.0, 4.5)), OR + Vector((carx(T_CRANE) + 4, 1.0, 2.2)), 15, 'lin'),
    # 4) um guindaste de 700 t chega (de lado), close no Carlin no "Resolvido? Não."
    (T_CRANE, (-50.0, -22.0, 16.0), (-12.0, 12.0, 22.0), 14, 'cut'),
    (fa(23.7) - 0.04, (-46.0, -20.0, 13.0), (-10.0, 14.0, 18.0), 14, ''),
    (fa(23.7), (-0.8, Y0 - 15.0, 2.1), (-4.5, Y0 - 8.5, 1.5), 18, 'cut'),
    (fa(25.5) - 0.04, (-1.3, Y0 - 14.0, 2.0), (-4.5, Y0 - 8.5, 1.5), 18, ''),
    # 5) iça sozinho: capacidade cai, guindaste tomba pra frente
    (fa(25.5), (-48.0, -24.0, 16.0), (-8.0, 16.0, 14.0), 14, 'cut'),
    (29.3, (-52.0, -30.0, 24.0), (-8.0, 14.0, 22.0), 14, ''),
    (T_TANDEM - 0.04, (-50.0, -28.0, 20.0), (-10.0, 12.0, 16.0), 14, ''),
    # 6) dois guindastes, um em cada ponta
    (T_TANDEM, (0.0, -60.0, 26.0), (0.0, Y0, 24.0), 14, 'cut'),
    (fa(35.3) - 0.04, (0.0, -50.0, 20.0), (0.0, Y0, 18.0), 14, ''),
    (fa(35.3), (0.0, -4.0, 5.0), (0.0, Y0, 4.0), 15, 'cut'),
    (T_CABO - 0.04, (0.0, -3.0, 4.6), (0.0, Y0, 4.0), 15, ''),
    # close: cabo de aço = perna
    (T_CABO, (3.4, Y0 - 9.6, 1.1), (0.8, Y0 - 4.3, 0.75), 17, 'cut'),
    (T_TILT - 0.04, (2.8, Y0 - 9.2, 1.0), (0.8, Y0 - 4.3, 0.75), 17, ''),
    # 7) desnível (no vão entre os guindastes)
    (T_TILT, (0.0, -4.0, 9.0), (0.0, Y0, 9.0), 14, 'cut'),
    (T_REW - 0.04, (0.0, -6.0, 10.0), (0.0, Y0, 9.0), 14, ''),
    (44.6, (0.0, -5.0, 9.0), (0.0, Y0, 7.0), 14, ''),
    (T_PLAN - 0.04, (0.0, -5.0, 9.0), (0.0, Y0, 7.0), 14, ''),
    # 8) 5 meses de planejamento
    (T_PLAN, OC + Vector((0.8, -8.6, 3.0)), OC + Vector((-2.6, 0.0, 1.4)), 18, 'cut'),
    (T_DIA - 0.04, OC + Vector((0.2, -7.8, 2.8)), OC + Vector((-2.6, 0.0, 1.4)), 18, ''),
    # 9) no dia: sobem juntos, sinaleiro
    (T_DIA, (0.0, -10.0, 3.0), (0.0, Y0, 14.0), 14, 'cut'),
    (T_TOPO - 0.04, (0.0, -14.0, 6.0), (0.0, Y0, 34.0), 14, ''),
    # 10) topo aberto (visto por trás, sem as lanças na frente), entra por cima, teto fecha
    (T_TOPO, (-24.0, BY + 44.0, 84.0), (0.0, BY - 2.0, 50.0), 15, 'cut'),
    (54.3, (-20.0, BY + 38.0, 76.0), (0.0, BY, 50.0), 15, ''),
    (55.6, (-16.0, BY + 30.0, 64.0), (0.0, BY, 49.0), 16, ''),
    (T_FIM - 0.04, (-18.0, BY + 34.0, 70.0), (0.0, BY, 51.0), 15, ''),
    # 11-12) parabéns: órbita baixa no topo (drum visível no vão abaixo do teto)
    (T_FIM, (16.0, BY + 30.0, 52.0), (2.0, BY, 51.0), 16, 'cut'),
    (60.5, (0.0, BY + 34.0, 54.0), (2.0, BY, 51.5), 16, ''),
    (END_T, (-16.0, BY + 30.0, 55.0), (2.0, BY, 51.5), 16, ''),
]
camera_path(cam, tgt, shots)
cam.data.clip_end = 1000
add_noise(cam, 'location', strength=0.08, scale=40)

anchors = [a_topo, a_drum, a_drum_ponta, a_ghost, a_gA, a_gB, a_barA, a_barB, a_seta, a_trena, a_predio, a_cabo,
           a_cal, a_token, a_porto, a_obra, a_carreta, a_agua, a_vapor, a_carlin, a_perna]

bpy.ops.wm.save_as_mainfile(filepath=OUT_BLEND)
with bpy.context.temp_override(scene=sc):
    bpy.ops.ptcache.bake_all(bake=True)
bpy.ops.wm.save_as_mainfile(filepath=OUT_BLEND)
if OUT_ANCH:
    project_anchors(anchors, 1, sc.frame_end, OUT_ANCH)
print('OK cena salva', OUT_BLEND, 'frames', sc.frame_end)
