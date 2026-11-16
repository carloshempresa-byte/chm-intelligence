"""Short avulso — A tuneladora (tatuzão). Monta a cena em corte, anima e salva o .blend.
Uso:  blender -b --factory-startup -P cena_tuneladora.py -- <saida.blend> [anchors.json]
Visual genérico, sem marca de fabricante. Tempos amarrados a audio/narracao_tight.json.
A cena é um "bolo cortado": tudo o que é subterrâneo é cortado no plano y=0 e a câmera olha de -Y."""
import bpy, bmesh, sys, os, math, random
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import importlib, lowpoly_lib
importlib.reload(lowpoly_lib)
from lowpoly_lib import *
from mathutils import Vector

argv = sys.argv[sys.argv.index('--') + 1:] if '--' in sys.argv else []
OUT_BLEND = argv[0] if argv else '/tmp/tun.blend'
OUT_ANCH = argv[1] if len(argv) > 1 else None
FONT = os.path.join(HERE, '..', '..', 'identidade-visual', 'assets', 'Montserrat-Black.ttf')
END_T = 113.6
random.seed(5)


def fa(t):
    return (F(t) - 1) / FPS


# ------------------------------------------------------------------ config (igual EP01/EP02)
bpy.ops.wm.read_factory_settings(use_empty=True)
sc = bpy.context.scene
sc.render.fps = FPS; sc.frame_start = 1; sc.frame_end = F(END_T)
sc.render.resolution_x, sc.render.resolution_y = 1080, 1920
sc.render.engine = 'BLENDER_EEVEE'
ee = sc.eevee
ee.taa_render_samples = 8
ee.use_soft_shadows = True; ee.shadow_cascade_size = '2048'; ee.shadow_cube_size = '1024'
ee.use_gtao = True; ee.gtao_distance = 1.2; ee.gtao_factor = 0.8
ee.use_bloom = True; ee.bloom_threshold = 1.2; ee.bloom_intensity = 0.06; ee.bloom_radius = 5.0
sc.view_settings.view_transform = 'Standard'
sc.render.image_settings.file_format = 'PNG'; sc.render.image_settings.color_mode = 'RGB'
sc.render.use_overwrite = False; sc.render.use_placeholder = True

w = bpy.data.worlds.new('Ceu'); sc.world = w; w.use_nodes = True
nt = w.node_tree; bg = nt.nodes['Background']
tc = nt.nodes.new('ShaderNodeTexCoord'); sep = nt.nodes.new('ShaderNodeSeparateXYZ'); ramp = nt.nodes.new('ShaderNodeValToRGB')
nt.links.new(tc.outputs['Generated'], sep.inputs[0])
mapr = nt.nodes.new('ShaderNodeMapRange'); mapr.inputs['From Min'].default_value = 0.5; mapr.inputs['From Max'].default_value = 0.8
nt.links.new(sep.outputs['Z'], mapr.inputs['Value']); nt.links.new(mapr.outputs['Result'], ramp.inputs['Fac'])
ramp.color_ramp.elements[0].color = hexrgb('#e6f4fb'); ramp.color_ramp.elements[1].color = hexrgb('#6fbde8')
nt.links.new(ramp.outputs['Color'], bg.inputs['Color']); bg.inputs['Strength'].default_value = 0.9
sun_d = bpy.data.lights.new('Sol', 'SUN'); sun_d.energy = 3.3; sun_d.angle = math.radians(7)
sun_d.color = hexrgb('#fff3e0')[:3]; sun_d.shadow_cascade_max_distance = 140
sun = link(bpy.data.objects.new('Sol', sun_d)); sun.rotation_euler = (math.radians(50), math.radians(6), math.radians(28))
# luz de preenchimento para o interior do túnel
fill_d = bpy.data.lights.new('Preench', 'SUN'); fill_d.energy = 0.9; fill_d.use_shadow = False
fill = link(bpy.data.objects.new('Preench', fill_d)); fill.rotation_euler = (math.radians(80), 0, math.radians(-10))

P = dict(
    top=mat('top', '#9c7650', 0.95, spec=0.1), soil=mat('soil', '#c39a68', 0.95, spec=0.1), rock=mat('rock', '#8d8f93', 0.9, spec=0.15),
    asphalt=mat('asphalt', '#55595f', 0.9), lane=mat('lane', '#ffd23f', 0.6), side=mat('side', '#c9c3b8', 0.9),
    ring=mat('ring', '#cfc9be', 0.85), ring2=mat('ring2', '#b9b2a6', 0.85),
    ringglow=mat('ringglow', '#cfc9be', 0.8, emit='#ffd23f', emit_strength=0.0),
    shield=mat('shield', '#f5c242', 0.45, spec=0.5), steel=mat('steel', '#3b4a5c', 0.6), dark=mat('dark', '#2a2d33', 0.7),
    cutter=mat('cutter', '#4a5563', 0.5, spec=0.5), tooth=mat('tooth', '#d9dde3', 0.4, metal=0.5),
    chamber=mat('chamber', '#a8794a', 0.95), belt=mat('belt', '#2a2d33', 0.8), chunk=mat('chunk', '#9c7650', 0.95),
    piston=mat('piston', '#f5c242', 0.35, spec=0.6), rod=mat('rod', '#e6e9ee', 0.2, metal=0.8),
    gantry=mat('gantry', '#58a6d6', 0.5), duct=mat('duct', '#f29e4c', 0.6), capsule=mat('capsule', '#f7f7f2', 0.5),
    glass=mat('glass', '#9fd6f2', 0.15), red=mat('red', '#e5484d', 0.5), green=mat('green', '#3fbf6f', 0.5),
    arrowY=mat('arrowY', '#ffd23f', 0.5, emit='#ffd23f', emit_strength=0.5), arrowB=mat('arrowB', '#58a6d6', 0.4, emit='#9fd6f2', emit_strength=0.6),
    worm=mat('worm', '#f2a0b4', 0.6), bldg1=mat('bldg1', '#e9e4da', 0.8), bldg2=mat('bldg2', '#58a6d6', 0.7), bldg3=mat('bldg3', '#f29e4c', 0.7),
    tree=mat('tree', '#5fae5a', 0.9), trunk=mat('trunk', '#8a5a3b', 0.9), car1=mat('car1', '#e74c3c', 0.4), car2=mat('car2', '#7b5ea7', 0.4),
    car3=mat('car3', '#3e8e7e', 0.4), white=mat('white', '#f7f7f2', 0.7), wood=mat('wood', '#b07a46', 0.9),
    mapgrass=mat('mapgrass', '#bfe0a0', 0.95), mapcity=mat('mapcity', '#e9e4da', 0.9), mapline=mat('mapline', '#3fbf6f', 0.4, emit='#3fbf6f', emit_strength=0.4),
    border=mat('border', '#e5484d', 0.6), ground=mat('ground', '#e7d6ae', 0.95, spec=0.1), concrete=mat('concrete', '#aaa397', 0.9),
    ribbon=mat('ribbon', '#f2a0b4', 0.5), plate=mat('plate', '#2f6fa3', 0.5), platetxt=mat('platetxt', '#ffffff', 0.5),
    band=mat('m_band', '#ffffff', 0.4), bandtxt=mat('m_bandtxt', '#2f6fa3', 0.4), gauge=mat('gauge', '#f7f7f2', 0.6),
    dust=mat('dust', '#d9c3a0', 1.0), cloud=mat('cloud', '#ffffff', 1.0, emit='#ffffff', emit_strength=0.3),
)


def text3d(name, txt, loc, size, material, parent=None, rot=(math.pi / 2, 0, 0), extrude=0.05):
    cu = bpy.data.curves.new(name, 'FONT'); cu.body = txt; cu.size = size; cu.extrude = extrude
    cu.align_x = 'CENTER'; cu.align_y = 'CENTER'; cu.font = bpy.data.fonts.load(FONT)
    ob = link(bpy.data.objects.new(name, cu)); ob.location = loc; ob.rotation_euler = rot
    ob.data.materials.append(material)
    if parent:
        ob.parent = parent
    return ob


def show_between(objs, t0, t1):
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
    return a + (b - a) * u


def kk(ob, path, val, fr):
    setattr(ob, path, val); ob.keyframe_insert(path, frame=fr)


# ------------------------------------------------------------------ malhas em corte (metade y>=0)
def half_tube(name, r_out, r_in, x0, x1, material, parent=None, phi0=0.0, phi1=math.pi, n=20):
    """Tubo cortado: ângulo phi medido do topo (z+) para o lado +y. y=r·sin(phi), z=r·cos(phi)."""
    me = bpy.data.meshes.new(name); bm = bmesh.new()
    ring = lambda x, r: [bm.verts.new((x, r * math.sin(phi0 + (phi1 - phi0) * i / n), r * math.cos(phi0 + (phi1 - phi0) * i / n))) for i in range(n + 1)]
    oa, ob_, ia, ib = ring(x0, r_out), ring(x1, r_out), ring(x0, r_in), ring(x1, r_in)
    for i in range(n):
        bm.faces.new((oa[i], oa[i + 1], ob_[i + 1], ob_[i]))
        bm.faces.new((ia[i + 1], ia[i], ib[i], ib[i + 1]))
        bm.faces.new((oa[i + 1], oa[i], ia[i], ia[i + 1]))
        bm.faces.new((ob_[i], ob_[i + 1], ib[i + 1], ib[i]))
    for j in (0, n):
        bm.faces.new((oa[j], ia[j], ib[j], ob_[j]) if j == 0 else (ia[j], oa[j], ob_[j], ib[j]))
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    bm.to_mesh(me); bm.free()
    ob = link(bpy.data.objects.new(name, me)); me.materials.append(material)
    if parent:
        ob.parent = parent
    return ob


def half_disc(name, r, x, thick, material, parent=None, n=20):
    return half_tube(name, r, 0.02, x - thick / 2, x + thick / 2, material, parent, n=n)


# ================================================================== DIORAMA: rua em cima, terreno cortado embaixo
ZT = -16.0          # eixo do túnel
R_BORE = 5.05
R_RING_O, R_RING_I = 5.0, 4.6
W_RING = 1.6
X_SHAFT = 16.2      # parede do poço de saída
FLOOR = ZT - 4.42  # piso do mascote (y=1.2 dentro do anel)
YM = 1.2


def soil_box(name, x0, x1, y0, y1, z0, z1, m):
    return box(name, (x1 - x0, y1 - y0, z1 - z0), ((x0 + x1) / 2, (y0 + y1) / 2, (z0 + z1) / 2), m, bevel=0.0)


layers = [soil_box('TerraTopo', -220, X_SHAFT, 0, 70, -6, -0.6, P['top']),
          soil_box('TerraMeio', -220, X_SHAFT, 0, 70, -26, -6, P['soil']),
          soil_box('Rocha', -220, X_SHAFT, 0, 70, -70, -26, P['rock'])]
# poço de saída (aberto para a câmera), com fundo e paredes
soil_box('PocoFundoTerra', X_SHAFT, 60, 0, 70, -70, -22.0, P['soil'])
soil_box('PocoParedeFundo', 34, 60, 0, 70, -22.0, -0.6, P['soil'])
soil_box('PocoParedeTras', X_SHAFT, 34, 22, 70, -22.0, -0.6, P['soil'])
box('PocoPiso', (17.8, 22, 0.3), ((X_SHAFT + 34) / 2, 11, -21.85), P['concrete'], bevel=0.02)
# furo do túnel: cilindro booleano que acompanha a máquina (parent no TBM)
TBM = empty('TBM', (0, 0, ZT))
bore = prim('cyl', 'FuroTunel', (-120 + 0.35, 0, 0), None, TBM, rot=(0, math.pi / 2, 0), vertices=40, radius=R_BORE, depth=240)
bore.hide_render = True; bore.display_type = 'WIRE'
for L in layers:
    md = L.modifiers.new('Furo', 'BOOLEAN'); md.operation = 'DIFFERENCE'; md.object = bore; md.solver = 'FAST'
# rua
box('Calcada', (236, 5, 0.6), (-102, 2.5, -0.3), P['side'], bevel=0.02)
box('Rua', (236, 14, 0.6), (-102, 12, -0.3), P['asphalt'], bevel=0.0)
for i in range(-36, 3):
    box(f'Faixa{i}', (2.6, 0.25, 0.02), (i * 6, 12, 0.01), P['lane'], bevel=0)
box('Calcada2', (236, 51, 0.6), (-102, 44.5, -0.3), P['side'], bevel=0.02)
for i in range(26):
    x = -150 + i * 6.5 + random.uniform(-1, 1)
    h = random.uniform(6, 22)
    box(f'Predio{i}', (5.0, 7.0, h), (x, 26 + random.uniform(0, 6), h / 2), [P['bldg1'], P['bldg2'], P['bldg3']][i % 3], bevel=0.1)
for i in range(18):
    x = -140 + i * 9 + random.uniform(-2, 2)
    prim('cyl', f'Tronco{i}', (x, 20.5, 1.0), P['trunk'], vertices=5, radius=0.3, depth=2)
    prim('cone', f'Copa{i}', (x, 20.5, 3.4), P['tree'], vertices=6, radius1=1.7, depth=3.8)
for i in range(6):
    x, z = random.uniform(-120, 20), random.uniform(32, 45)
    for j in range(3):
        prim('ico', f'Nuvem{i}_{j}', (x + j * 4 - 4, 90, z + (j == 1) * 1.5), P['cloud'], subdivisions=1, radius=random.uniform(3, 4.5), scale=(1.3, 1, 0.7))
cars = []
for i, (lane, d, c) in enumerate([(8.5, 1, 'car1'), (8.5, 1, 'car3'), (15.5, -1, 'car2'), (15.5, -1, 'car1')]):
    car = empty(f'Carro{i}', (0, lane, 0))
    box(f'CarroCorpo{i}', (4.2, 1.9, 0.9), (0, 0, 0.75), P[c], parent=car, bevel=0.1)
    box(f'CarroTeto{i}', (2.2, 1.7, 0.7), (-0.2 * d, 0, 1.45), P['glass'], parent=car, bevel=0.06)
    for sx in (-1, 1):
        for sy in (-1, 1):
            prim('cyl', f'CarroRoda{i}{sx}{sy}', (1.35 * sx, 0.95 * sy, 0.38), P['dark'], car, rot=(math.pi / 2, 0, 0), vertices=8, radius=0.38, depth=0.25)
    x0 = -70 + i * 22 if d > 0 else 20 - i * 18
    k(car, 'location', 0, (x0, lane, 0), 'LINEAR')
    k(car, 'location', 22, (x0 + d * 95, lane, 0), 'LINEAR')
    car.rotation_euler.z = 0 if d > 0 else math.pi
    cars.append(car)
a_rua = empty('a_rua', (-26, 1.0, 1.5))

# ------------------------------------------------------------------ revestimento: anéis de aduelas (estáticos, já montados)
def seg_mesh(name, x0, x1, phi_a, phi_b, m, parent=None):
    return half_tube(name, R_RING_O, R_RING_I, x0, x1, m, parent, phi0=phi_a, phi1=phi_b, n=6)


rings_static = []
for kx in range(70):
    x1 = -14.0 - kx * W_RING; x0 = x1 - W_RING + 0.05
    for j, (a, b) in enumerate(((0.0, math.pi / 3), (math.pi / 3, 2 * math.pi / 3), (2 * math.pi / 3, math.pi))):
        rings_static.append(seg_mesh(f'Anel{kx}_{j}', x0, x1, a + 0.012, b - 0.012, P['ring'] if (kx + j) % 2 else P['ring2']))
# junta tudo num objeto só (render mais leve)
bpy.ops.object.select_all(action='DESELECT')
for o in rings_static:
    o.select_set(True)
bpy.context.view_layer.objects.active = rings_static[0]
bpy.ops.object.join()
rings_obj = bpy.context.object; rings_obj.name = 'AneisMontados'; rings_obj.location = (0, 0, ZT)
for o in bpy.context.selected_objects:
    o.select_set(False)
a_aneis = empty('a_aneis', (-40, 1.0, ZT + R_RING_O + 0.2))

# ------------------------------------------------------------------ TUNELADORA (genérica, sem marca), em corte
CUT = empty('RodaCorte', (0.3, 0, 0), TBM)   # gira em X
prim('cyl', 'RodaDisco', (0, 0, 0), P['cutter'], CUT, rot=(0, math.pi / 2, 0), vertices=32, radius=4.95, depth=0.6)
prim('cyl', 'RodaCentro', (0.4, 0, 0), P['shield'], CUT, rot=(0, math.pi / 2, 0), vertices=16, radius=0.9, depth=0.6)
for i in range(6):
    sp = empty(f'RaioPiv{i}', (0, 0, 0), CUT); sp.rotation_euler.x = i * math.pi / 3
    box(f'Raio{i}', (0.35, 0.7, 4.3), (0.38, 0, 2.6), P['shield'], parent=sp, bevel=0.05)
    for j in range(4):
        prim('cone', f'Dente{i}{j}', (0.6, 0.0, 1.4 + j * 0.95), P['tooth'], sp, rot=(0, math.pi / 2, 0), vertices=6, radius1=0.2, depth=0.4)
a_roda = empty('a_roda', (0.6, -0.4, 4.2), TBM)
shield = empty('Escudo', (0, 0, 0), TBM)
half_tube('EscudoCasco', 5.0, 4.72, -14.0, -0.05, P['shield'], shield)
for x in (-4.5, -9.5):
    half_tube(f'EscudoFaixa{x}', 5.04, 4.98, x - 0.25, x + 0.25, P['steel'], shield)
a_escudo = empty('a_escudo', (-7, 0.2, 5.1), TBM)
half_disc('Antepara', 4.72, -2.3, 0.3, P['steel'], TBM)
camara = half_tube('CamaraTerra', 4.7, 0.05, -2.15, -0.35, P['chamber'], TBM)
a_camara = empty('a_camara', (-1.2, 0.0, 1.0), TBM)
setas_frente = []
for i, z in enumerate((-2.5, 0.0, 2.5)):
    s = empty(f'SetaFrente{i}', (1.0, -0.6, z), TBM)
    prim('cone', f'SetaFPonta{i}', (1.4, 0, 0), P['arrowY'], s, rot=(0, math.pi / 2, 0), vertices=8, radius1=0.6, depth=1.0)
    prim('cyl', f'SetaFHaste{i}', (0.5, 0, 0), P['arrowY'], s, rot=(0, math.pi / 2, 0), vertices=8, radius=0.25, depth=1.2)
    setas_frente.append(s)
setas_ar = []
for i, z in enumerate((-2.0, 1.5)):
    s = empty(f'SetaAr{i}', (-0.1, -0.6, z), TBM)
    prim('cone', f'SetaArPonta{i}', (0.9, 0, 0), P['arrowB'], s, rot=(0, math.pi / 2, 0), vertices=8, radius1=0.5, depth=0.8)
    prim('cyl', f'SetaArHaste{i}', (0.2, 0, 0), P['arrowB'], s, rot=(0, math.pi / 2, 0), vertices=8, radius=0.2, depth=0.9)
    setas_ar.append(s)
# rosca inclinada: da câmara (embaixo) para trás e para cima
rosca = empty('Rosca', (-2.4, 1.0, -3.6), TBM)
ang_r = math.atan2(2.5, 9.0)
rosca.rotation_euler.y = ang_r  # sobe para trás (-X)
half_tube('RoscaTubo', 0.85, 0.75, -9.4, 0.0, P['steel'], rosca, n=10)
helice = empty('Helice', (0, 0, 0), rosca)
hb = box('HeliceLamina', None, (0, 0, 0), P['shield'], parts=[((9.2, 0.12, 1.3), (-4.6, 0, 0))], parent=helice, segx=40, bevel=0)
tw = hb.modifiers.new('Torce', 'SIMPLE_DEFORM'); tw.deform_method = 'TWIST'; tw.deform_axis = 'X'; tw.angle = math.radians(1440)
a_rosca = empty('a_rosca', (-4.5, -0.4, 0.9), rosca)
# esteira ao longo do backup
belt = box('Esteira', (66, 1.4, 0.25), (-44, 1.6, -1.2), P['belt'], parent=TBM, bevel=0.02)
for i in range(24):
    box(f'EsteiraRolo{i}', (0.3, 1.5, 0.3), (-12 - i * 2.8, 1.6, -1.45), P['steel'], parent=TBM, bevel=0.02)
a_esteira = empty('a_esteira', (-24, 0.8, -0.9), TBM)
chunks = [box(f'TerraEsteira{i}', (0.7, 0.7, 0.5), (0, 1.6, -0.8), P['chunk'], parent=TBM, bevel=0.08) for i in range(14)]
# backup: pórticos, duto de ventilação, câmara hiperbárica, carro de aduelas
BACKUP = []
for i in range(9):
    x = -17 - i * 6.5
    g = empty(f'Portico{i}', (x, 0, 0), TBM)
    box(f'PorticoPerna{i}', (0.4, 0.4, 7.6), (0, 3.6, -0.6), P['gantry'], parent=g, bevel=0.04)
    box(f'PorticoViga{i}', (0.4, 3.6, 0.4), (0, 1.8, 3.1), P['gantry'], parent=g, bevel=0.04)
    box(f'PorticoPiso{i}', (5.6, 3.4, 0.2), (0, 1.9, -2.2), P['steel'], parent=g, bevel=0.02)
    BACKUP.append(g)
half_tube('DutoVent', 0.9, 0.8, -75, -15, P['duct'], TBM, n=10).location = (0, 0.0, 3.6)
a_duto = empty('a_duto', (-34, -0.2, 4.6), TBM)
caps = empty('CamaraHiperbarica', (-17.5, 2.3, -1.0), TBM)
prim('cyl', 'CapsCorpo', (0, 0, 0), P['capsule'], caps, rot=(0, math.pi / 2, 0), vertices=20, radius=1.15, depth=3.0)
for sx in (-1, 1):
    prim('uv', f'CapsTampo{sx}', (sx * 1.5, 0, 0), P['capsule'], caps, segments=16, ring_count=8, radius=1.15, scale=(0.45, 1, 1))
porta = prim('cyl', 'CapsPorta', (0, -1.13, 0), P['steel'], caps, rot=(math.pi / 2, 0, 0), vertices=16, radius=0.75, depth=0.08)
prim('cyl', 'CapsVigia', (0.9, -1.12, 0.3), P['glass'], caps, rot=(math.pi / 2, 0, 0), vertices=12, radius=0.22, depth=0.08)
a_caps = empty('a_caps', (0, -1.2, 1.3), caps)
carro_ad = empty('CarroAduelas', (-15.5, 2.0, -3.3), TBM)
box('CarroAdBase', (3.0, 2.2, 0.3), (0, 0, 0), P['steel'], parent=carro_ad, bevel=0.03)
for j in range(3):
    box(f'AduelaCarro{j}', (2.6, 1.8, 0.3), (0, 0, 0.32 + 0.33 * j), P['ring'] if j % 2 else P['ring2'], parent=carro_ad, bevel=0.04)
a_estrut = empty('a_estrut', (-14.5, 0.3, -2.0), TBM)
# braço montador (eretor) na cauda
ER = empty('Eretor', (-13.2, 0, 0), TBM)
half_tube('EretorAnel', 1.4, 1.0, -0.3, 0.3, P['steel'], TBM).location = (-13.2, 0, 0)
er_arm = empty('EretorBraco', (0, 0, 0), ER)
box('EretorHaste', (0.5, 0.5, 3.0), (0, 1.0, -1.7), P['shield'], parent=er_arm, bevel=0.05).rotation_euler.x = math.radians(30)
box('EretorGarra', (1.0, 0.9, 0.5), (0, 1.9, -3.25), P['dark'], parent=er_arm, bevel=0.05).rotation_euler.x = math.radians(30)
a_eretor = empty('a_eretor', (-13.2, 0.0, -2.0), TBM)
# pistões (3 visíveis no corte) — base presa à máquina; haste estica para trás até o último anel
PIST_PHI = (math.pi / 6, math.pi / 2, 5 * math.pi / 6)
rods = []
for i, ph in enumerate(PIST_PHI):
    y, z = 4.3 * math.sin(ph), 4.3 * math.cos(ph)
    prim('cyl', f'PistaoCorpo{i}', (-8.2, y, z), P['piston'], TBM, rot=(0, math.pi / 2, 0), vertices=10, radius=0.32, depth=2.4)
    hp = empty(f'PistaoHastePiv{i}', (-9.4, y, z), TBM)
    rd = prim('cyl', f'PistaoHaste{i}', (-0.5, 0, 0), P['rod'], hp, rot=(0, math.pi / 2, 0), vertices=8, radius=0.16, depth=1.0)
    box(f'PistaoSapata{i}', (0.2, 0.7, 0.7), (-1.0, 0, 0), P['piston'], parent=hp, bevel=0.03)
    rods.append(hp)
a_pistao = empty('a_pistao', (-10.4, 0.0, 4.2 * math.cos(PIST_PHI[0])), TBM)
# rodinhas (gag: "ela não tem rodas")
rodas = [prim('cyl', f'RodaGag{i}', (x, -0.9, -5.6), P['dark'], TBM, rot=(math.pi / 2, 0, 0), vertices=14, radius=0.9, depth=0.6) for i, x in enumerate((-2.5, -7, -11.5))]
# terra que desaba (problema) — blocos acima da frente
caindo = []
for i in range(12):
    x = random.uniform(-9, 0.5); ph = random.uniform(0.2, 1.3)
    b = box(f'TerraCai{i}', (random.uniform(0.8, 1.6),) * 2 + (0.9,), (x, -random.uniform(0.6, 1.4), 5.3), P['top'], bevel=0.1)
    b.parent = TBM
    caindo.append(b)
# terra solta na câmara (frente)
farelos = [box(f'Farelo{i}', (0.35, 0.35, 0.35), (0.1, -0.5, 0), P['chunk'], parent=TBM, bevel=0.05) for i in range(10)]
# painel didático: botões ROSCA e AVANÇO + manômetro
painel = empty('Painel', (-26.6, 3.0, FLOOR + 2.9))
box('PainelPlaca', (3.4, 0.25, 2.2), (0, 0.15, 0), P['steel'], parent=painel, bevel=0.06)
box('PainelPe', (0.3, 0.3, 2.6), (0, 0.3, -1.4), P['dark'], parent=painel, bevel=0.03)
knobs = []
for i, x in enumerate((-1.0, 0.0)):
    kb = prim('cyl', f'Botao{i}', (x, -0.15, -0.45), P['red'] if i == 0 else P['green'], painel, rot=(math.pi / 2, 0, 0), vertices=12, radius=0.36, depth=0.25)
    box(f'BotaoMarca{i}', (0.08, 0.1, 0.3), (0, -0.14, 0.14), P['white'], parent=kb, bevel=0).rotation_euler.x = -math.pi / 2
    knobs.append(kb)
gauge = empty('Manometro', (1.05, -0.12, 0.25), painel)
prim('cyl', 'ManoFundo', (0, 0, 0), P['gauge'], gauge, rot=(math.pi / 2, 0, 0), vertices=20, radius=0.75, depth=0.08)
for j, (c, a) in enumerate((('green', 0), ('red', 55), ('red', -55))):
    zone = box(f'ManoZona{j}', (0.12, 0.05, 0.3), (0, -0.05, 0.55), P[c], parent=gauge, bevel=0)
    zp = empty(f'ManoZonaPiv{j}', (0, 0, 0), gauge); zone.parent = zp; zp.rotation_euler.y = math.radians(a)
needle = empty('Ponteiro', (0, -0.08, 0), gauge)
box('PonteiroHaste', (0.06, 0.04, 0.6), (0, 0, 0.3), P['dark'], parent=needle, bevel=0)
a_botoes = empty('a_botoes', (-0.5, -0.4, -0.2), painel)
a_mano = empty('a_mano', (1.05, -0.4, 0.4), painel)
# aduelas do anel novo (montadas pelo eretor) e anéis do avanço rápido
def new_ring(name, x_world):
    segs = []
    for j in range(3):
        piv = empty(f'{name}Piv{j}', (x_world, 0, ZT))
        s = seg_mesh(f'{name}Seg{j}', -W_RING + 0.05, 0.0, 2 * math.pi / 3 + 0.012, math.pi - 0.012, P['ring'] if j % 2 else P['ring2'], piv)
        segs.append(piv)
    return segs


RING_X = [-12.4 + i * W_RING for i in range(9)]   # face dianteira de cada anel novo (mundo)
new_rings = [new_ring(f'AnelNovo{i}', RING_X[i]) for i in range(9)]
a_anel_novo = empty('a_anel_novo', (RING_X[0] - 0.8, 0.5, ZT + R_RING_O * 0.5))
worm = []
for i in range(9):
    s = prim('uv', f'Minhoca{i}', (-44 + i * 5.2, -2.0, ZT), P['worm'], segments=12, ring_count=8, radius=2.6 - abs(i - 4) * 0.12)
    worm.append(s)

# ------------------------------------------------------------------ mapa (Penha – Dutra, esquemático)
OM = Vector((400, 0, 0))
mapa = empty('Mapa', OM)
prim('plane', 'MapaFundo', (0, 0, 0), P['mapgrass'], mapa, size=40)
for i in range(30):
    box(f'MapaQuadra{i}', (random.uniform(1.2, 2.6), random.uniform(1.2, 2.6), 0.15), (random.uniform(-14, 14), random.uniform(-14, 8), 0.08), P['mapcity'], parent=mapa, bevel=0.02)
for i in range(12):
    box(f'MapaDivisa{i}', (1.1, 0.3, 0.1), (-15 + i * 2.6, 9.5 + 0.6 * math.sin(i), 0.12), P['border'], parent=mapa, bevel=0)
linha = box('MapaLinha', None, (-7, -5, 0.2), P['mapline'], parts=[((1.0, 0.7, 0.12), (0.5, 0, 0))], parent=mapa, bevel=0)
linha.rotation_euler.z = math.atan2(13.0, 12.0)
LLEN = math.hypot(12.0, 13.0)
pins = []
for nm, (x, y) in (('Penha', (-7, -5)), ('Dutra', (5, 8))):
    pn = empty(f'Pin{nm}', (x, y, 0), mapa)
    prim('cyl', f'Pin{nm}Haste', (0, 0, 0.8), P['dark'], pn, vertices=8, radius=0.1, depth=1.6)
    prim('uv', f'Pin{nm}Cabeca', (0, 0, 1.8), P['red'], pn, segments=12, ring_count=8, radius=0.55)
    pins.append(pn)
a_penha = empty('a_penha', (-7, -5, 2.4), mapa)
a_dutra = empty('a_dutra', (5, 8, 2.4), mapa)
a_linha = empty('a_linha', (-1, 1.5, 0.6), mapa)
a_gru = empty('a_gru', (8, 10.5, 0.6), mapa)

# ------------------------------------------------------------------ palco: placas de nome e comparação com a Bertha
OB = Vector((600, 0, 0))
palco = empty('Palco', OB)
prim('plane', 'PalcoChao', (0, 0, 0), P['ground'], palco, size=120)
K = 4.95 / (11.67 / 2)   # unidades por metro (roda da máquina nova = 11,67 m)
R_SP, R_BE = 11.67 / 2 * K, 17.5 / 2 * K


def roda_palco(name, r, x):
    g = empty(name, (x, 0, 0), palco)
    box(f'{name}Base', (r * 0.9, 3.0, 0.8), (0, 0.8, 0.4), P['steel'], parent=g, bevel=0.05)
    d = prim('cyl', f'{name}Disco', (0, 0, r + 0.6), P['cutter'], g, rot=(math.pi / 2, 0, 0), vertices=36, radius=r, depth=0.8)
    prim('cyl', f'{name}Centro', (0, -0.45, r + 0.6), P['shield'], g, rot=(math.pi / 2, 0, 0), vertices=16, radius=r * 0.18, depth=0.4)
    for i in range(6):
        sp = empty(f'{name}RaioPiv{i}', (0, -0.45, r + 0.6), g); sp.rotation_euler.y = i * math.pi / 3
        box(f'{name}Raio{i}', (r * 0.07, 0.3, r * 0.82), (0, 0, r * 0.5), P['shield'], parent=sp, bevel=0.04)
    return g


rSP = roda_palco('RodaSP', R_SP, -4.0)
rBE = roda_palco('RodaBertha', R_BE, 11.0)
plaquinha = empty('Plaquinha', (-4.0, -0.6, 2 * R_SP + 2.6), palco)
box('PlaquinhaChapa', (3.4, 0.2, 1.1), (0, 0, 0), P['plate'], parent=plaquinha, bevel=0.08)
for sx in (-1, 1):
    prim('cone', f'Laco{sx}', (sx * 0.55, -0.15, 0.75), P['ribbon'], plaquinha, rot=(0, sx * math.pi / 2, 0), vertices=4, radius1=0.45, depth=0.9)
prim('ico', 'LacoNo', (0, -0.15, 0.75), P['ribbon'], plaquinha, subdivisions=1, radius=0.22)
placa_b = empty('PlacaBertha', (11.0, -0.6, 2 * R_BE + 2.4), palco)
box('PlacaBerthaChapa', (5.4, 0.2, 1.4), (0, 0, 0), P['plate'], parent=placa_b, bevel=0.08)
text3d('PlacaBerthaTxt', 'BERTHA', (0, -0.15, 0), 0.95, P['platetxt'], placa_b, extrude=0.04)
a_rodaSP = empty('a_rodaSP', (-4.0, -0.6, 2 * R_SP + 0.6), palco)
a_rodaBE = empty('a_rodaBE', (11.0, -0.6, 2 * R_BE + 0.6), palco)
a_placaBE = empty('a_placaBE', (11.0, -0.6, 2 * R_BE + 3.2), palco)

# ------------------------------------------------------------------ rompimento no poço: blocos de terra
parede = []
for i in range(16):
    ph = random.uniform(0, math.pi); r = random.uniform(0.5, 4.6)
    b = box(f'Parede{i}', (1.0, random.uniform(0.9, 1.6), random.uniform(0.9, 1.6)), (X_SHAFT - 0.4, r * math.sin(ph), ZT + r * math.cos(ph)), P['soil'], bevel=0.1)
    parede.append(b)
dusts = [prim('ico', f'Poeira{i}', (X_SHAFT + 0.5, random.uniform(0.2, 4.5), ZT + random.uniform(-4, 4)), P['dust'], subdivisions=1, radius=random.uniform(0.6, 1.0)) for i in range(10)]
for d in dusts:
    d.scale = (0.001,) * 3; k(d, 'scale', 0, (0.001,) * 3, 'CONSTANT', frame=1)

# ------------------------------------------------------------------ mascote
mas = Mascot('Mascote', (6.0, 2.6, 0.0), rotz=math.radians(10))
helmet_band(mas, 'Eng. Carlin', FONT, P['band'], P['bandtxt'])
a_carlin = empty('a_carlin', (0, -0.5, 2.6), mas.pos)
chave = box('ChaveInglesa', (0.15, 0.15, 0.9), (0.0, -0.3, -0.62), P['steel'], parent=mas.arms[1], bevel=0.03)

# ================================================================== ANIMAÇÃO
T_S1, T_S2, T_S3, T_CAM, T_PAINEL, T_ROSCA, T_EST, T_BACK = (fa(10.13), fa(17.7), fa(24.0), fa(29.1), fa(33.38), fa(36.4), fa(39.58), fa(43.87))
T_CHAM, T_ERET, T_PIST, T_LAPSO, T_MAPA, T_NOME, T_BERTHA, T_POCO = (fa(55.6), fa(57.92), fa(67.0), fa(77.43), fa(83.41), fa(89.89), fa(95.89), fa(101.3))

# visibilidade
show_between([mapa], T_MAPA, T_NOME)
show_between([palco], T_NOME, T_POCO)
show_between([painel], T_PAINEL, T_EST)
show_between(worm, 11.8, 13.4)
show_between(rodas, 67.4, 68.9)
show_between(setas_frente, 31.8, T_PAINEL)
show_between(setas_ar, 56.0, T_ERET)
show_between([rBE, placa_b], T_BERTHA, None)
show_between([plaquinha], 91.9, None)

# --- avanço da máquina (X), pistões e anéis novos
PUSHES = [(70.0, 71.9), (74.0, 75.4)] + [(77.6 + i * 0.95, 77.6 + i * 0.95 + 0.5) for i in range(6)]
RINGS_T = [(62.0, 66.3)] + [(72.6, 73.5), (75.55, 76.6)] + [(e + 0.02, e + 0.4) for _, e in PUSHES[2:]]


def tbm_x(t):
    x = 0.0
    for i, (a, b) in enumerate(PUSHES):
        x += sm(0.0, W_RING, a, b, t)
    x += sm(0.0, 3.6, T_POCO, 102.2, t)
    return x


def rod_len(t):
    """comprimento da haste: encosta no anel mais novo; retrai antes de montar o próximo."""
    X = tbm_x(t)
    n = sum(1 for (a, b) in RINGS_T if t >= b)  # anéis novos já montados
    if n == 0:
        contact = -14.0          # último anel estático (face dianteira em -14)
    else:
        contact = RING_X[n - 1]
    full = (X - 9.4) - contact    # distância da base até o anel
    # retração durante a montagem do anel seguinte
    for (a, b) in RINGS_T[1:]:
        if a - 0.35 <= t < b + 0.1:
            return max(0.4, full - 1.3)
    return max(0.4, full)


for fr in range(1, F(END_T) + 1):
    t = (fr - 1) / FPS
    kk(TBM, 'location', (tbm_x(t), 0, ZT), fr)
    L = rod_len(t)
    for hp in rods:
        kk(hp, 'scale', (L, 1, 1), fr)
# anéis novos: aduelas giram da base até a posição final, junto com o braço
k(er_arm, 'rotation_euler', 0, (0, 0, 0), frame=1)
for ri, segs in enumerate(new_rings):
    t0, t1 = RINGS_T[ri]
    dur = (t1 - t0) / 3.0
    for j, piv in enumerate(segs):
        final = j * math.pi / 3
        ts = t0 + j * dur
        k(piv, 'scale', 0, (1, 0.001, 0.001), 'CONSTANT', frame=1)
        k(piv, 'scale', ts, (1, 0.001, 0.001), 'BACK', 'EASE_OUT')
        k(piv, 'scale', ts + dur * 0.3, (1, 0.82, 0.82))
        k(piv, 'rotation_euler', ts + dur * 0.3, (0, 0, 0))
        k(piv, 'rotation_euler', ts + dur * 0.85, (final, 0, 0))
        k(piv, 'scale', ts + dur * 0.85, (1, 0.82, 0.82))
        k(piv, 'scale', ts + dur, (1, 1, 1))
        k(er_arm, 'rotation_euler', ts + dur * 0.3, (0, 0, 0))
        k(er_arm, 'rotation_euler', ts + dur * 0.85, (final, 0, 0))
    k(er_arm, 'rotation_euler', t1 + 0.05, (0, 0, 0))
# brilho do anel completo (cena do eretor)
for piv in new_rings[0]:
    for ch in piv.children:
        ch.data.materials[0] = P['ringglow']
ksock(P['ringglow'], 'Emission Strength', 0, 0.0)
ksock(P['ringglow'], 'Emission Strength', 66.0, 0.0)
ksock(P['ringglow'], 'Emission Strength', 66.3, 1.6)
ksock(P['ringglow'], 'Emission Strength', 67.0, 0.0)

# --- roda de corte gira o tempo todo; hélice da rosca gira
CUT.rotation_euler.x = 0
k(CUT, 'rotation_euler', 0, (0, 0, 0), 'LINEAR', frame=1)
k(CUT, 'rotation_euler', END_T, (END_T * 1.6, 0, 0), 'LINEAR')
k(helice, 'rotation_euler', 0, (0, 0, 0), 'LINEAR', frame=1)
k(helice, 'rotation_euler', END_T, (-END_T * 6.0, 0, 0), 'LINEAR')

# --- terra caindo da frente (farelos) em loop
for i, f in enumerate(farelos):
    z0 = random.uniform(-3.5, 3.5)
    t = 17.8 + i * 0.13
    k(f, 'scale', 0, (0.001,) * 3, 'CONSTANT', frame=1)
    while t < 33.0:
        k(f, 'location', t, (0.0, -0.5, z0), 'CONSTANT'); k(f, 'scale', t, (1, 1, 1), 'CONSTANT')
        k(f, 'location', t + 0.01, (0.0, -0.5, z0), 'QUAD', 'EASE_IN')
        k(f, 'location', t + 0.75, (-0.6, -0.5, -4.4))
        k(f, 'scale', t + 0.74, (1, 1, 1), 'CONSTANT'); k(f, 'scale', t + 0.75, (0.001,) * 3, 'CONSTANT')
        t += 0.78

# --- problema: escudo sai, terra desaba; rebobina; escudo volta
k(shield, 'location', T_S3, (0, 0, 0), 'BACK', 'EASE_IN')
k(shield, 'location', T_S3 + 0.45, (-60, 0, 0), 'CONSTANT')
k(shield, 'location', 27.0, (-60, 0, 0), 'BACK', 'EASE_OUT')
k(shield, 'location', 28.2, (0, 0, 0))
for b in caindo:
    base = tuple(b.location)
    k(b, 'scale', 0, (0.001,) * 3, 'CONSTANT', frame=1)
    k(b, 'scale', 25.3, (1, 1, 1), 'CONSTANT')
    k(b, 'location', 25.3, base, 'QUAD', 'EASE_IN')
    k(b, 'location', 26.2 + random.uniform(0, 0.25), (base[0], base[1], -3.6 + random.uniform(-0.6, 0.6)), 'LINEAR')
    k(b, 'location', 26.55, (base[0], base[1], -3.6), 'QUAD', 'EASE_OUT')
    k(b, 'location', 26.95, base)
    k(b, 'scale', 26.95, (1, 1, 1), 'CONSTANT'); k(b, 'scale', 27.0, (0.001,) * 3, 'CONSTANT')
# setas da câmara pulsam; câmara esvazia um pouco na cena do ar comprimido
for i, s in enumerate(setas_frente):
    for t0 in (31.9, 32.6, 33.0):
        k(s, 'location', t0, (1.0, -0.6, s.location.z), 'SINE')
        k(s, 'location', t0 + 0.25, (1.5, -0.6, s.location.z))
k(camara, 'scale', 0, (1, 1, 1), 'CONSTANT', frame=1)
k(camara, 'scale', T_CHAM, (1, 0.001, 0.001), 'CONSTANT')
k(camara, 'scale', T_ERET, (1, 1, 1), 'CONSTANT')

# --- painel: botões giram, ponteiro sobe e volta ao verde
k(needle, 'rotation_euler', T_PAINEL, (0, math.radians(-50), 0))
k(knobs[0], 'rotation_euler', 35.1, (math.pi / 2, 0, 0)); k(knobs[0], 'rotation_euler', 35.7, (math.pi / 2, math.radians(120), 0))
k(needle, 'rotation_euler', 35.2, (0, math.radians(-50), 0), 'BACK', 'EASE_OUT'); k(needle, 'rotation_euler', 35.9, (0, math.radians(55), 0))
k(knobs[1], 'rotation_euler', 37.7, (math.pi / 2, 0, 0)); k(knobs[1], 'rotation_euler', 38.3, (math.pi / 2, math.radians(-120), 0))
k(needle, 'rotation_euler', 37.8, (0, math.radians(55), 0), 'ELASTIC', 'EASE_OUT'); k(needle, 'rotation_euler', 38.9, (0, 0, 0))

# --- terra na esteira (loop)
for i, c in enumerate(chunks):
    t = 36.0 + i * 0.45
    k(c, 'scale', 0, (0.001,) * 3, 'CONSTANT', frame=1)
    while t < 58.0:
        k(c, 'location', t, (-11.0, 1.6, -0.85), 'CONSTANT'); k(c, 'scale', t, (1, 1, 1), 'CONSTANT')
        k(c, 'location', t + 0.01, (-11.0, 1.6, -0.85), 'LINEAR')
        k(c, 'location', t + 6.0, (-76.0, 1.6, -0.85))
        t += 6.3
    k(c, 'scale', 58.0, (0.001,) * 3, 'CONSTANT')

# --- minhoca (gag)
for i, s in enumerate(worm):
    k(s, 'location', 11.8, (s.location.x, -2.0, ZT + 0.6 * math.sin(i)), 'SINE')
    k(s, 'location', 12.6, (s.location.x, -2.0, ZT + 0.6 * math.sin(i + 2)), 'SINE')
    k(s, 'location', 13.3, (s.location.x, -2.0, ZT + 0.6 * math.sin(i + 4)))
    pop_in(s, 11.8 + i * 0.03, 0.25)

# --- mapa: linha cresce, pinos aparecem
k(linha, 'scale', 0, (0.001, 1, 1), 'CONSTANT', frame=1)
k(linha, 'scale', 85.4, (0.001, 1, 1), 'QUAD', 'EASE_IN_OUT')
k(linha, 'scale', 86.6, (LLEN, 1, 1))
for i, pn in enumerate(pins):
    pop_in(pn, (87.7, 87.95)[i], 0.3)

# --- palco: plaquinha desce, Bertha desliza para dentro
k(plaquinha, 'location', 91.9, (-4.0, -0.6, 2 * R_SP + 14), 'BOUNCE', 'EASE_OUT')
k(plaquinha, 'location', 92.5, (-4.0, -0.6, 2 * R_SP + 2.6))
k(rBE, 'location', T_BERTHA, (40.0, 0, 0), 'BACK', 'EASE_OUT')
k(rBE, 'location', 97.0, (11.0, 0, 0))
k(placa_b, 'location', 98.6, (11.0, -0.6, 2 * R_BE + 14), 'BOUNCE', 'EASE_OUT')
k(placa_b, 'location', 99.2, (11.0, -0.6, 2 * R_BE + 2.4))
k(placa_b, 'location', 0, (11.0, -0.6, 2 * R_BE + 14), 'CONSTANT', frame=1)

# --- rompimento: blocos voam, poeira
for b in parede:
    base = tuple(b.location)
    k(b, 'location', 101.65, base, 'QUAD', 'EASE_OUT')
    k(b, 'location', 102.5, (base[0] + random.uniform(4, 9), base[1] - random.uniform(0, 2), -21.0 + random.uniform(0, 0.6)), 'BOUNCE', 'EASE_OUT')
    k(b, 'rotation_euler', 101.65, (0, 0, 0))
    k(b, 'rotation_euler', 102.5, (random.uniform(-2, 2), random.uniform(-2, 2), random.uniform(-2, 2)))
for d in dusts:
    t0 = 101.7 + random.uniform(0, 0.1)
    k(d, 'scale', t0, (0.001,) * 3, 'QUAD', 'EASE_OUT'); k(d, 'location', t0, tuple(d.location), 'QUAD', 'EASE_OUT')
    k(d, 'scale', t0 + 0.4, (1.6, 1.6, 1.4)); k(d, 'location', t0 + 1.2, (d.location.x + 3, d.location.y - 1, d.location.z + 1.5))
    k(d, 'scale', t0 + 1.2, (0.001,) * 3, 'CONSTANT')

# --- mascote
mas.look(0.0, tilt=0.15, turn=0.0, dur=0.05)
mas.look(4.4, tilt=0.55, turn=0.3)
mas.scared(5.0, hold=0.9)
mas.sweat(6.1)
mas.move(T_S3, (-21.5, YM, FLOOR), rotz=math.radians(-60), cut=True)
mas.look(T_S3, 0, 0, 0.05)
mas.move(T_PAINEL, (-28.6, YM, FLOOR), rotz=math.radians(-15), cut=True)
mas.look(T_PAINEL, tilt=0.1, turn=-0.6, dur=0.05)
mas._arms(35.0, -0.18, 1.5, 'BACK', 'EASE_OUT'); mas._arms(35.8, -0.18, 1.5); mas._rest_arms(36.1)
mas._arms(37.6, -0.18, 1.5, 'BACK', 'EASE_OUT'); mas._arms(38.4, -0.18, 1.5); mas._rest_arms(38.7)
mas.hop(39.0)
mas.move(T_BACK, (-15.0, 1.4, ZT - 2.1), rotz=math.radians(-20), cut=True)
mas.look(T_BACK, 0, 0, 0.05)
mas.move(52.2, (-16.6, 1.0, ZT - 2.1), rotz=math.radians(-90))
mas.move(54.7, (-17.5, 1.0, ZT - 2.1), rotz=math.radians(0))
k(mas.pos, 'scale', 54.7, (1, 1, 1)); k(mas.pos, 'scale', 55.3, (0.001,) * 3, 'CONSTANT')
k(porta, 'location', 54.6, (0, -1.13, 0)); k(porta, 'location', 54.75, (-1.4, -1.13, 0)); k(porta, 'location', 55.35, (-1.4, -1.13, 0)); k(porta, 'location', 55.5, (0, -1.13, 0))
mas.move(T_CHAM, (-1.25, 2.0, ZT - 4.2), rotz=math.radians(-80), cut=True)
k(mas.pos, 'scale', T_CHAM - 1 / FPS, (0.001,) * 3, 'CONSTANT'); k(mas.pos, 'scale', T_CHAM, (1, 1, 1), 'CONSTANT')
mas._arms(55.8, -0.18, 2.0, 'BACK', 'EASE_OUT')
for i in range(4):
    mas._arms(56.2 + i * 0.35, -0.18, 1.6); mas._arms(56.37 + i * 0.35, -0.18, 2.1)
mas._rest_arms(57.8)
k(chave, 'scale', 0, (0.001,) * 3, 'CONSTANT', frame=1)
k(chave, 'scale', T_CHAM, (1, 1, 1), 'CONSTANT'); k(chave, 'scale', T_ERET, (0.001,) * 3, 'CONSTANT')
mas.move(T_ERET, (-20.5, YM, FLOOR), rotz=math.radians(-55), cut=True)
mas.look(T_ERET, tilt=-0.1, turn=0.3, dur=0.05)
mas.hop(59.45)
mas.celebrate(66.1, jumps=1, period=0.5)
mas.move(T_PIST, (-23.0, YM, FLOOR), rotz=math.radians(-35), cut=True)
mas.scared(68.4, 0.4)
mas.hop(73.5); mas.hop(76.65)
mas.move(T_LAPSO, (-34.0, YM, FLOOR), rotz=math.radians(-30), cut=True)
mas.move(T_MAPA, (OM.x + 9.5, OM.y - 9.0, 0.0), rotz=math.radians(20), cut=True)
mas.look(T_MAPA, tilt=0.3, turn=0.3, dur=0.05)
mas.hop(87.75)
mas.move(T_NOME, (OB.x + 2.6, OB.y - 3.0, 0.0), rotz=math.radians(-15), cut=True)
mas.look(T_NOME, tilt=-0.4, turn=-0.4, dur=0.05)
mas._arms(92.5, -2.4, 2.4, 'BACK', 'EASE_OUT'); mas._arms(92.75, -1.0, 1.0); mas._arms(93.0, -2.4, 2.4); mas._rest_arms(93.4)
mas.look(96.2, tilt=-0.6, turn=0.5)
mas.scared(97.0, 0.6)
mas.move(T_POCO, (23.0, 3.0, -21.7), rotz=math.radians(-35), cut=True)
mas.look(T_POCO, tilt=-0.1, turn=-0.4, dur=0.05)
mas.celebrate(101.5, jumps=5, period=0.5)
mas.celebrate(104.3, jumps=3, period=0.5)
mas.celebrate(106.4, jumps=3, period=0.5)
mas._arms(108.5, -0.18, 1.5, 'BACK', 'EASE_OUT'); mas._arms(109.9, -0.18, 1.5)   # aponta (manda pro amigo)
mas._arms(110.2, -0.18, 2.6, 'BACK', 'EASE_OUT'); mas.hop(110.25); mas._arms(111.6, -0.18, 2.6)  # joinha (segue)
mas._rest_arms(112.0)

# confete no poço
conf_col = bpy.data.collections.new('Confete'); sc.collection.children.link(conf_col)
for i, c in enumerate(['#ffd23f', '#e5484d', '#58a6d6', '#5fae5a', '#ff7a1f', '#ffffff', '#b06ab3']):
    cp = prim('plane', f'ConfPeca{i}', (0, 0, -90), mat(f'conf{i}', c, 0.5, emit=c, emit_strength=0.4), size=1.0)
    cp.scale = (1, 0.5, 1); sc.collection.objects.unlink(cp); conf_col.objects.link(cp)
conf_em = prim('plane', 'ConfeteEmissor', (25, 8, -3), None, size=1.0, scale=(9, 9, 1))
ps = conf_em.modifiers.new('Confete', 'PARTICLE_SYSTEM').particle_system
st = ps.settings
st.count = 1100; st.frame_start = F(101.5); st.frame_end = F(102.7); st.lifetime = 400
st.normal_factor = 0.0; st.object_align_factor = (0, 0, -2.0); st.factor_random = 1.2
st.render_type = 'COLLECTION'; st.instance_collection = conf_col; st.use_collection_pick_random = True
st.particle_size = 0.3; st.size_random = 0.4
st.use_rotations = True; st.rotation_mode = 'NONE'; st.rotation_factor_random = 1.0
st.angular_velocity_mode = 'RAND'; st.angular_velocity_factor = 8.0
st.effector_weights.gravity = 0.18; st.drag_factor = 0.4
conf_em.show_instancer_for_render = False

# ================================================================== CÂMERA
cam, tgt = camera_rig()
shots = [
    # 0) gancho: da rua, mergulha até a máquina
    (0.0, (12.0, -24.0, 9.0), (2.0, 6.0, 1.5), 15, ''),
    (3.6, (10.0, -30.0, 6.0), (0.0, 4.0, -2.0), 15, ''),
    (6.6, (-6.0, -44.0, -6.0), (-12.0, 0.0, -13.0), 14, ''),
    (T_S1 - 0.04, (-10.0, -46.0, -7.0), (-14.0, 0.0, -13.0), 14, ''),
    # 1) TBM inteira + cidade em cima
    (T_S1, (-26.0, -58.0, -8.0), (-26.0, 0.0, -11.0), 14, 'cut'),
    (T_S2 - 0.04, (-20.0, -56.0, -6.0), (-22.0, 0.0, -9.0), 14, ''),
    # 2) roda de corte (frente)
    (T_S2, (12.0, -15.0, -13.0), (0.0, 0.0, -16.0), 16, 'cut'),
    (T_S3 - 0.04, (9.0, -12.0, -14.0), (0.0, 0.0, -16.0), 17, ''),
    # 3) problema / escudo / câmara
    (T_S3, (8.0, -26.0, -11.0), (-5.0, 0.0, -15.0), 15, 'cut'),
    (fa(28.4), (6.0, -26.0, -12.0), (-6.0, 0.0, -15.0), 15, ''),
    (T_CAM, (3.5, -12.0, -14.0), (-1.2, 0.0, -16.0), 18, 'cut'),
    (T_PAINEL - 0.04, (2.5, -11.0, -14.5), (-1.2, 0.0, -16.0), 18, ''),
    # 4) painel + rosca
    (T_PAINEL, (-23.0, -8.0, -16.8), (-27.4, 2.4, -18.4), 18, 'cut'),
    (T_EST - 0.04, (-23.8, -7.2, -17.0), (-27.4, 2.4, -18.4), 19, ''),
    # 5) rosca e esteiras: acompanha a terra
    (T_EST, (-2.0, -13.0, -14.5), (-6.5, 0.0, -18.0), 17, 'cut'),
    (fa(41.0) - 0.04, (-3.0, -12.5, -14.5), (-7.0, 0.0, -18.0), 17, ''),
    (fa(41.0), (-8.0, -13.0, -14.0), (-12.0, 0.0, -17.0), 16, 'cut'),
    (T_BACK - 0.04, (-30.0, -13.0, -14.0), (-34.0, 0.0, -17.0), 16, 'lin'),
    # 6) backup (de trás para a frente) e câmara hiperbárica
    (T_BACK, (-60.0, -17.0, -12.5), (-62.0, 0.0, -16.0), 15, 'cut'),
    (50.6, (-14.0, -13.0, -14.5), (-17.0, 0.0, -16.6), 16, ''),
    (T_CHAM - 0.04, (-13.5, -11.0, -15.0), (-17.0, 1.0, -16.8), 17, ''),
    (T_CHAM, (-1.3, -9.5, -17.2), (-1.3, 1.6, -19.0), 18, 'cut'),
    (T_ERET - 0.04, (-1.3, -8.8, -17.4), (-1.3, 1.6, -19.0), 19, ''),
    # 7) eretor monta o anel
    (T_ERET, (-6.0, -12.0, -14.0), (-12.5, 0.0, -16.5), 16, 'cut'),
    (T_PIST - 0.04, (-8.0, -11.0, -14.5), (-13.0, 0.0, -16.5), 17, ''),
    # 8) pistões empurram o último anel
    (T_PIST, (-6.0, -24.0, -13.0), (-10.0, 0.0, -16.0), 15, 'cut'),
    (T_LAPSO - 0.04, (-2.0, -24.0, -13.0), (-6.0, 0.0, -16.0), 15, ''),
    # 9) avanço rápido
    (T_LAPSO, (-6.0, -48.0, -10.0), (-6.0, 0.0, -14.0), 14, 'cut'),
    (T_MAPA - 0.04, (2.0, -46.0, -10.0), (2.0, 0.0, -14.0), 14, ''),
    # mapa
    (T_MAPA, OM + Vector((0.0, -17.0, 17.0)), OM + Vector((-1.0, 1.5, 0.0)), 15, 'cut'),
    (T_NOME - 0.04, OM + Vector((0.0, -15.0, 15.5)), OM + Vector((-1.0, 1.5, 0.0)), 15, ''),
    # 10) palco: nome / Bertha
    (T_NOME, OB + Vector((-2.0, -26.0, 7.0)), OB + Vector((-3.0, 0.0, 5.0)), 15, 'cut'),
    (T_BERTHA - 0.04, OB + Vector((-1.0, -24.0, 7.0)), OB + Vector((-3.0, 0.0, 5.0)), 15, ''),
    (97.5, OB + Vector((5.0, -42.0, 9.0)), OB + Vector((4.0, 0.0, 7.0)), 14, ''),
    (T_POCO - 0.04, OB + Vector((5.0, -40.0, 9.0)), OB + Vector((4.0, 0.0, 7.0)), 14, ''),
    # 11-12) rompimento no poço + CTA
    (T_POCO, (31.0, -17.0, -15.0), (18.5, 3.0, -18.0), 15, 'cut'),
    (104.3, (30.0, -18.0, -14.0), (20.5, 3.5, -18.5), 16, ''),
    (END_T, (24.0, -21.0, -14.0), (21.0, 3.5, -18.5), 16, ''),
]
camera_path(cam, tgt, shots)
cam.data.clip_end = 800
add_noise(cam, 'location', strength=0.06, scale=40)

anchors = [a_rua, a_aneis, a_roda, a_escudo, a_camara, a_rosca, a_esteira, a_duto, a_caps, a_estrut, a_eretor, a_pistao,
           a_anel_novo, a_botoes, a_mano, a_penha, a_dutra, a_linha, a_gru, a_rodaSP, a_rodaBE, a_placaBE, a_carlin]
a_tbm = empty('a_tbm', (-30, 0.0, 5.5), TBM); anchors.append(a_tbm)
a_frente = empty('a_frente', (1.2, -0.5, -4.2), TBM); anchors.append(a_frente)

bpy.ops.wm.save_as_mainfile(filepath=OUT_BLEND)
with bpy.context.temp_override(scene=sc):
    bpy.ops.ptcache.bake_all(bake=True)
bpy.ops.wm.save_as_mainfile(filepath=OUT_BLEND)
if OUT_ANCH:
    project_anchors(anchors, 1, sc.frame_end, OUT_ANCH)
print('OK cena salva', OUT_BLEND, 'frames', sc.frame_end)
