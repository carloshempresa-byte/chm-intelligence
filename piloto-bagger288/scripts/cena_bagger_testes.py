"""Bagger 288 — quadros de TESTE do novo padrão visual (golden hour, mina em degraus, máquina detalhada).
Uso:  blender -b --factory-startup -P cena_bagger_testes.py -- <pasta_saida> [amostras] [escala_res] [shots...]
Escala real em metros (1 unidade = 1 m). Visual genérico, sem marca. Comparações conforme o roteiro (rev. 2)."""
import bpy, bmesh, sys, os, math, random, time
from mathutils import Vector, Matrix, Euler
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from lowpoly_lib import mat, box, prim, empty, link, hexrgb, Mascot, helmet_band

argv = sys.argv[sys.argv.index('--') + 1:]
OUT = argv[0]
SAMPLES = int(argv[1]) if len(argv) > 1 else 16
RES = float(argv[2]) if len(argv) > 2 else 1.0
ONLY = argv[3:] if len(argv) > 3 else None
FONT = os.path.join(HERE, '..', '..', 'identidade-visual', 'assets', 'Montserrat-Black.ttf')
random.seed(288)
os.makedirs(OUT, exist_ok=True)

# ================================================================== render: EEVEE "cinema"
bpy.ops.wm.read_factory_settings(use_empty=True)
sc = bpy.context.scene
sc.render.engine = 'BLENDER_EEVEE'
sc.render.resolution_x, sc.render.resolution_y = int(1080 * RES), int(1920 * RES)
sc.render.fps = 30
ee = sc.eevee
ee.taa_render_samples = SAMPLES
ee.use_soft_shadows = True
ee.shadow_cascade_size = '4096'; ee.shadow_cube_size = '1024'
ee.use_gtao = True; ee.gtao_distance = 6.0; ee.gtao_factor = 1.1
ee.use_bloom = True; ee.bloom_threshold = 0.9; ee.bloom_intensity = 0.09; ee.bloom_radius = 6.5; ee.bloom_color = hexrgb('#ffd9a0')[:3]
ee.use_motion_blur = True; ee.motion_blur_shutter = 0.5; ee.motion_blur_steps = 1
ee.use_ssr = False
sc.view_settings.view_transform = 'Filmic'; sc.view_settings.look = 'Medium High Contrast'; sc.view_settings.exposure = -0.1
sc.render.image_settings.file_format = 'PNG'; sc.render.image_settings.color_mode = 'RGB'
sc.frame_start, sc.frame_end = 1, 90
FR = 75  # quadro renderizado (partículas já espalhadas)

# céu golden hour: horizonte laranja -> topo azul
w = bpy.data.worlds.new('Ceu'); sc.world = w; w.use_nodes = True
nt = w.node_tree; bg = nt.nodes['Background']
tc = nt.nodes.new('ShaderNodeTexCoord'); sep = nt.nodes.new('ShaderNodeSeparateXYZ'); ramp = nt.nodes.new('ShaderNodeValToRGB')
mapr = nt.nodes.new('ShaderNodeMapRange'); mapr.inputs['From Min'].default_value = 0.47; mapr.inputs['From Max'].default_value = 0.78
nt.links.new(tc.outputs['Generated'], sep.inputs[0]); nt.links.new(sep.outputs['Z'], mapr.inputs['Value'])
nt.links.new(mapr.outputs['Result'], ramp.inputs['Fac'])
cr = ramp.color_ramp
cr.elements[0].color = hexrgb('#ffb067'); cr.elements[1].color = hexrgb('#4f86c6')
e = cr.elements.new(0.22); e.color = hexrgb('#ffd7a3')
e = cr.elements.new(0.55); e.color = hexrgb('#a9c8e8')
nt.links.new(ramp.outputs['Color'], bg.inputs['Color']); bg.inputs['Strength'].default_value = 0.7
sun_d = bpy.data.lights.new('Sol', 'SUN'); sun_d.energy = 4.2; sun_d.angle = math.radians(2.5)
sun_d.color = hexrgb('#ffc48a')[:3]; sun_d.shadow_cascade_max_distance = 700; sun_d.shadow_cascade_count = 4
sun_d.shadow_cascade_fade = 0.15
sun = link(bpy.data.objects.new('Sol', sun_d))
fill_d = bpy.data.lights.new('CeuAzul', 'SUN'); fill_d.energy = 0.55; fill_d.color = hexrgb('#9cc1ee')[:3]; fill_d.use_shadow = False
fill = link(bpy.data.objects.new('CeuAzul', fill_d)); fill.rotation_euler = (math.radians(35), 0, math.radians(-150))

# névoa atmosférica: passe mist + compositor (barato no EEVEE)
vl = sc.view_layers[0]; vl.use_pass_mist = True; vl.use_pass_z = True
w.mist_settings.start = 260; w.mist_settings.depth = 2200; w.mist_settings.falloff = 'QUADRATIC'
sc.use_nodes = True
cn = sc.node_tree
for n in list(cn.nodes):
    cn.nodes.remove(n)
rl = cn.nodes.new('CompositorNodeRLayers'); comp = cn.nodes.new('CompositorNodeComposite')
mix = cn.nodes.new('CompositorNodeMixRGB'); mix.blend_type = 'MIX'; mix.inputs[2].default_value = hexrgb('#e8c39c')
mm = cn.nodes.new('CompositorNodeMath'); mm.operation = 'MULTIPLY'; mm.inputs[1].default_value = 0.62
geo = cn.nodes.new('CompositorNodeMath'); geo.operation = 'LESS_THAN'; geo.inputs[1].default_value = 5000.0  # 1 = terreno/máquina, 0 = céu
cn.links.new(rl.outputs['Depth'], geo.inputs[0])
mm2 = cn.nodes.new('CompositorNodeMath'); mm2.operation = 'MULTIPLY'
cn.links.new(rl.outputs['Mist'], mm.inputs[0]); cn.links.new(mm.outputs[0], mm2.inputs[0]); cn.links.new(geo.outputs[0], mm2.inputs[1])
cn.links.new(mm2.outputs[0], mix.inputs[0])
cn.links.new(rl.outputs['Image'], mix.inputs[1]); cn.links.new(mix.outputs[0], comp.inputs[0])

# ================================================================== materiais
M = dict(
    steel=mat('steel', '#d9dcd8', 0.5, spec=0.45), steel2=mat('steel2', '#b9bdb8', 0.55, spec=0.4), accent=mat('accent', '#f5c242', 0.45, spec=0.5),
    blue=mat('blue', '#2f6fa3', 0.5), dark=mat('dark', '#2a2d33', 0.75), dark2=mat('dark2', '#3b4a5c', 0.6),
    bucket=mat('bucket', '#e0782f', 0.5, spec=0.45), teeth=mat('teeth', '#4a4f57', 0.4, metal=0.6), belt=mat('belt', '#1f2125', 0.85),
    glass=mat('glass', '#9fd6f2', 0.1, spec=0.8), lamp=mat('lamp', '#fff1c9', 0.4, emit='#ffe7b0', emit_strength=9.0),
    win=mat('win', '#ffd28a', 0.4, emit='#ffcf88', emit_strength=2.5), cable=mat('cable', '#30343a', 0.4, metal=0.5),
    l_grass=mat('l_grass', '#7fa452', 0.95, spec=0.1), l_top=mat('l_top', '#7a5634', 0.95, spec=0.1), l_clay=mat('l_clay', '#c08a4e', 0.95, spec=0.1),
    l_sand=mat('l_sand', '#e2c48f', 0.95, spec=0.1), l_coal=mat('l_coal', '#26221f', 0.8, spec=0.2), l_floor=mat('l_floor', '#b89a72', 0.95, spec=0.1),
    l_road=mat('l_road', '#c9b28b', 0.95, spec=0.1), water=mat('water', '#6f9cc2', 0.08, spec=0.9),
    chunk=mat('chunk', '#8a6440', 0.95), dust=mat('dust', '#e8c9a0', 1.0, alpha=0.35),
    field=mat('field', '#5fa64a', 0.9, spec=0.1), field2=mat('field2', '#4f9440', 0.9, spec=0.1), line=mat('line', '#ffffff', 0.6),
    asphalt=mat('asphalt', '#4a4d52', 0.9), lane=mat('lane', '#f2f2ee', 0.6), crop1=mat('crop1', '#d9b45a', 0.95), crop2=mat('crop2', '#8fb34d', 0.95),
    tree=mat('tree', '#4d8a45', 0.9), trunk=mat('trunk', '#6e4a2f', 0.9), stone=mat('stone', '#e9e4da', 0.85),
    car1=mat('car1', '#e74c3c', 0.35, spec=0.6), car2=mat('car2', '#3e6fb0', 0.35, spec=0.6), car3=mat('car3', '#f2f2ee', 0.35, spec=0.6), car4=mat('car4', '#3e8e7e', 0.35, spec=0.6),
    truck=mat('truck', '#f5c242', 0.5), vest=mat('vest', '#ff7a1f', 0.6), skin=mat('skin', '#f2c39b', 0.7), hat=mat('hat', '#ffd23f', 0.4),
    band=mat('m_band', '#ffffff', 0.4), bandtxt=mat('m_bandtxt', '#2f6fa3', 0.4), pole=mat('pole', '#8d9196', 0.6),
)

# ------------------------------------------------------------------ utilitários de modelagem
_MESH = {}


def unit_box(key, size, m):
    """malha de caixa reutilizável (instâncias compartilham a malha)."""
    if key not in _MESH:
        ob = box('_src_' + key, size, (0, 0, 0), m, bevel=0)
        ob.data.name = key
        _MESH[key] = ob.data
        bpy.data.objects.remove(ob)
    return _MESH[key]


def inst(mesh, loc, rot=(0, 0, 0), scale=(1, 1, 1), parent=None, name='i'):
    ob = link(bpy.data.objects.new(name, mesh))
    ob.location = loc; ob.rotation_euler = rot; ob.scale = scale
    if parent:
        ob.parent = parent
    return ob


def frame_between(p0, p1, parent=None, name='Quadro'):
    """empty em p0 com eixo X apontando para p1 (Z ~ para cima)."""
    p0, p1 = Vector(p0), Vector(p1)
    d = p1 - p0
    e = empty(name, tuple(p0), parent)
    e.rotation_euler = d.to_track_quat('X', 'Z').to_euler()
    return e, d.length


def beam(p0, p1, t, m, parent=None, name='Viga'):
    """barra reta (seção t x t) entre dois pontos (no espaço do parent)."""
    e, L = frame_between(p0, p1, parent, name + 'Piv')
    me = unit_box('beam_' + m.name, (1, 1, 1), m)
    inst(me, (L / 2, 0, 0), scale=(L, t, t), parent=e, name=name)
    return e


def truss(p0, p1, w_, h_, nseg, m, chord=0.7, diag=0.35, parent=None, name='Trelica', walkway=False):
    """treliça espacial de 4 banzos entre p0 e p1 (seção w_ x h_)."""
    e, L = frame_between(p0, p1, parent, name)
    cm = unit_box('beam_' + m.name, (1, 1, 1), m)
    for sy in (-1, 1):
        for sz in (-1, 1):
            inst(cm, (L / 2, sy * w_ / 2, sz * h_ / 2), scale=(L, chord, chord), parent=e, name=name + 'Banzo')
    step = L / nseg
    for i in range(nseg + 1):
        x = i * step
        for sz in (-1, 1):
            inst(cm, (x, 0, sz * h_ / 2), scale=(diag, w_, diag), parent=e, name=name + 'Trav')
        for sy in (-1, 1):
            inst(cm, (x, sy * w_ / 2, 0), scale=(diag, diag, h_), parent=e, name=name + 'Mont')
        if i < nseg:
            for sy in (-1, 1):  # diagonais laterais em X
                a = math.atan2(h_, step) * (1 if i % 2 else -1)
                inst(cm, (x + step / 2, sy * w_ / 2, 0), (0, a, 0), (math.hypot(step, h_), diag, diag), e, name + 'Diag')
            for sz in (-1, 1):  # diagonais de cima/baixo
                a = math.atan2(w_, step) * (1 if i % 2 else -1)
                inst(cm, (x + step / 2, 0, sz * h_ / 2), (0, 0, a), (math.hypot(step, w_), diag, diag), e, name + 'DiagH')
    if walkway:
        railing(Vector((0, -w_ / 2 - 0.9, h_ / 2 + 0.05)), Vector((L, -w_ / 2 - 0.9, h_ / 2 + 0.05)), e, floor_w=1.6)
    return e, L


def railing(p0, p1, parent, floor_w=1.4, h=1.1, gap=2.0):
    """passarela com piso, postes e corrimão (guarda-corpo)."""
    d = p1 - p0; L = d.length
    e, _ = frame_between(p0, p1, parent, 'Passarela')
    fm = unit_box('beam_' + M['steel2'].name, (1, 1, 1), M['steel2'])
    am = unit_box('beam_' + M['accent'].name, (1, 1, 1), M['accent'])
    inst(fm, (L / 2, 0, 0), scale=(L, floor_w, 0.12), parent=e, name='PassPiso')
    for sy in (-1, 1):
        y = sy * floor_w / 2
        inst(am, (L / 2, y, h), scale=(L, 0.08, 0.08), parent=e, name='Corrimao')
        inst(am, (L / 2, y, h / 2), scale=(L, 0.05, 0.05), parent=e, name='CorrimaoMeio')
        n = max(2, int(L / gap))
        for i in range(n + 1):
            inst(am, (i * L / n, y, h / 2), scale=(0.07, 0.07, h), parent=e, name='Poste')
    return e


def stairs(base, height, parent, flights=None, w_=1.2):
    """escada em zigue-zague com corrimão."""
    flights = flights or max(2, int(height / 4))
    fh = height / flights
    am = unit_box('beam_' + M['accent'].name, (1, 1, 1), M['accent'])
    sm_ = unit_box('beam_' + M['steel2'].name, (1, 1, 1), M['steel2'])
    for i in range(flights):
        z0 = base.z + i * fh
        sx = 1 if i % 2 == 0 else -1
        p0 = Vector((base.x - sx * 2.2, base.y, z0)); p1 = Vector((base.x + sx * 2.2, base.y, z0 + fh))
        e, L = frame_between(p0, p1, parent, 'Lance')
        inst(sm_, (L / 2, 0, 0), scale=(L, w_, 0.15), parent=e, name='Degraus')
        inst(am, (L / 2, -w_ / 2, 1.0), scale=(L, 0.06, 0.06), parent=e, name='CorrEsc')
        inst(sm_, (0, 0, 0), scale=(1.6, w_ + 0.4, 0.15), parent=e, name='Patamar')


def rope(p0, p1, r, m, parent=None):
    e, L = frame_between(p0, p1, parent, 'Cabo')
    if 'cyl_' + m.name not in _MESH:
        ob = prim('cyl', '_cyl', (0, 0, 0), m, vertices=8, radius=1, depth=1)
        ob.data.transform(Matrix.Rotation(math.pi / 2, 4, 'Y'))
        _MESH['cyl_' + m.name] = ob.data; bpy.data.objects.remove(ob)
    inst(_MESH['cyl_' + m.name], (L / 2, 0, 0), scale=(L, r, r), parent=e, name='CaboFio')


# ================================================================== A MÁQUINA (genérica, sem marca)
B = empty('Bagger', (0, 0, 0))


def crawler(loc, parent):
    g = empty('Esteira', loc, parent)
    box('EstQuadro', (14.5, 3.0, 2.2), (0, 0, 1.9), M['dark2'], parent=g, bevel=0.15)
    shoe = unit_box('shoe', (1.05, 3.8, 0.45), M['dark'])
    n = 15
    for i in range(n):  # sapatas em volta (em cima e embaixo)
        x = -7.0 + i * 1.0
        inst(shoe, (x, 0, 0.25), parent=g, name='Sapata')
        inst(shoe, (x, 0, 3.15), parent=g, name='Sapata')
    for sx in (-1, 1):
        prim('cyl', 'EstRoda', (sx * 7.2, 0, 1.7), M['dark'], g, rot=(math.pi / 2, 0, 0), vertices=16, radius=1.55, depth=3.9)
    for i in range(5):
        prim('cyl', 'EstRolete', (-4.8 + i * 2.4, 0, 0.95), M['steel2'], g, rot=(math.pi / 2, 0, 0), vertices=10, radius=0.55, depth=4.0)
    return g


for gx, gy in ((14, 0), (-14, 14), (-14, -14)):
    grp = empty('GrupoEsteiras', (gx, gy, 0), B)
    for cx in (-8.4, 8.4):
        for cy in (-4.6, 4.6):
            crawler((cx, cy, 0), grp)
    box('GrupoViga', (19, 12.5, 2.4), (0, 0, 4.8), M['steel2'], parent=grp, bevel=0.2)
    prim('cyl', 'GrupoPino', (0, 0, 6.8), M['dark2'], grp, vertices=16, radius=2.6, depth=2.0)
# chassi triangular e anel de giro
for a, b_ in (((14, 0, 7.5), (-14, 14, 7.5)), ((-14, 14, 7.5), (-14, -14, 7.5)), ((-14, -14, 7.5), (14, 0, 7.5))):
    beam(a, b_, 2.6, M['steel2'], B, 'Chassi')
prim('cyl', 'Pedestal', (0, 0, 9.5), M['steel'], B, vertices=24, radius=12, depth=5)
prim('torus', 'AnelGiro', (0, 0, 12.2), M['dark2'], B, major_segments=36, minor_segments=8, major_radius=12.4, minor_radius=0.7)
SUP = empty('Superestrutura', (0, 0, 12.6), B)
box('Plataforma', (46, 24, 3.2), (-2, 0, 1.6), M['steel'], parent=SUP, bevel=0.3)
for hx, hy, hl, hw, hh in ((-6, -6, 18, 10, 9), (-6, 7.5, 18, 8, 7), (12, 0, 9, 14, 6)):
    hs = box('Casa', (hl, hw, hh), (hx, hy, 3.2 + hh / 2), M['blue'], parent=SUP, bevel=0.25)
    for j in range(int(hl / 3)):
        box('Janela', (1.6, 0.1, 1.0), (hx - hl / 2 + 1.8 + j * 3.0, hy - hw / 2 - 0.05, 3.2 + hh * 0.7), M['win'], parent=SUP, bevel=0)
    box('Telhado', (hl + 0.6, hw + 0.6, 0.5), (hx, hy, 3.2 + hh + 0.25), M['steel2'], parent=SUP, bevel=0.1)
for side in (-1, 1):
    railing(Vector((-25, side * 12.6, 3.25)), Vector((21, side * 12.6, 3.25)), SUP)
# mastro principal (torre treliçada) e mastro traseiro
truss((6, 0, 3.2), (4, 0, 83.4), 7, 7, 12, M['steel'], 0.8, 0.4, SUP, 'MastroPrinc')
truss((-18, 0, 3.2), (-20, 0, 50), 6, 6, 8, M['steel'], 0.7, 0.35, SUP, 'MastroTras')
box('TopoMastro', (8, 8, 2.0), (4, 0, 84.4), M['accent'], parent=SUP, bevel=0.15)
prim('cyl', 'PoliaTopo', (4, 0, 86.6), M['dark2'], SUP, rot=(math.pi / 2, 0, 0), vertices=16, radius=1.6, depth=6)
stairs(Vector((10.5, -4.2, 3.2)), 78, SUP, flights=14)
for i in range(6):
    box('LuzMastro', (0.8, 0.5, 0.5), (8.0, -3.8, 12 + i * 12), M['lamp'], parent=SUP, bevel=0)

# braço da roda (treliça inclinada) — gira junto com a superestrutura
PIV = Vector((22, 0, 10.0))
HUB = Vector((92, -1, 4.0))
arm_e, arm_L = truss(PIV, HUB, 9, 8, 14, M['steel'], 0.9, 0.42, SUP, 'BracoRoda', walkway=True)
# correia sobre o braço da roda (com roletes e terra andando)
belt_e, belt_L = frame_between(PIV + Vector((0, 0, 4.4)), HUB + Vector((-6, 0, 4.4)), SUP, 'CorreiaBraco')
box('CorreiaLona', (belt_L, 3.0, 0.3), (belt_L / 2, 0, 0.3), M['belt'], parent=belt_e, bevel=0)
rol = unit_box('rolete', (0.45, 3.4, 0.45), M['steel2'])
for i in range(int(belt_L / 2.2)):
    inst(rol, (i * 2.2, 0, 0.0), parent=belt_e, name='Rolete')
chm = unit_box('chunkS', (1.1, 1.0, 0.7), M['chunk'])
belt_chunks = []
for i in range(int(belt_L / 3.0)):
    c = inst(chm, (i * 3.0 + random.uniform(-0.6, 0.6), random.uniform(-0.6, 0.6), 0.75), (0, 0, random.uniform(0, 3)), parent=belt_e, name='TerraCorreia')
    belt_chunks.append(c)
# cabine do operador perto da roda
cab = empty('Cabine', HUB + Vector((-14, 6.5, -2.0)), SUP)
box('CabCorpo', (6, 4.2, 3.6), (0, 0, 0), M['accent'], parent=cab, bevel=0.2)
box('CabVidro', (5.2, 4.3, 1.6), (0.3, 0, 0.5), M['glass'], parent=cab, bevel=0.05)
box('CabVidroF', (0.12, 3.6, 1.6), (3.05, 0, 0.5), M['glass'], parent=cab, bevel=0)
beam(HUB + Vector((-14, 4.3, -1.0)), HUB + Vector((-14, 1.0, 1.5)), 0.6, M['steel2'], SUP, 'CabSuporte')

# RODA DE CAÇAMBAS: 21,6 m de diâmetro, 18 caçambas (dados do roteiro rev. 2)
R_W = 10.8
WHL = empty('RodaPiv', HUB + Vector((0, -6.2, 0)), SUP)
WHL.rotation_euler = (0, 0, 0)
wheel = empty('Roda', (0, 0, 0), WHL)  # gira em Y
for sy in (-1.3, 1.3):
    prim('torus', 'RodaAro', (0, sy, 0), M['steel'], wheel, rot=(math.pi / 2, 0, 0), major_segments=48, minor_segments=8, major_radius=R_W - 1.6, minor_radius=0.55)
prim('cyl', 'RodaCubo', (0, 0, 0), M['dark2'], wheel, rot=(math.pi / 2, 0, 0), vertices=20, radius=2.4, depth=4.0)
prim('cyl', 'RodaEixo', (0, 3.5, 0), M['steel2'], wheel, rot=(math.pi / 2, 0, 0), vertices=16, radius=1.2, depth=5.0)
spk = unit_box('spoke', (1, 0.6, 0.6), M['steel'])
for i in range(9):  # raios
    a = i * 2 * math.pi / 9
    for sy in (-1.3, 1.3):
        inst(spk, ((R_W - 1.8) / 2 * math.cos(a), sy, (R_W - 1.8) / 2 * math.sin(a)), (0, -a, 0), (R_W - 1.8, 1, 1), wheel, 'Raio')


def bucket_mesh():
    """caçamba em forma de 'copo' aberto (fundo + laterais + traseira), boca virada para +X local."""
    me = bpy.data.meshes.new('CacambaMalha'); bm = bmesh.new()
    def quad(a, b, c, d):
        vs = [bm.verts.new(p) for p in (a, b, c, d)]
        bm.faces.new(vs)
    Lx, W, H = 3.6, 3.0, 2.6
    # fundo curvo (3 painéis), laterais, traseira
    pts = [(-Lx / 2, -H / 2), (-Lx / 2 + 0.6, -H / 2 - 0.5), (Lx / 2 - 0.4, -H / 2 - 0.4), (Lx / 2, -H / 2 + 0.2)]
    for (x0, z0), (x1, z1) in zip(pts, pts[1:]):
        quad((x0, -W / 2, z0), (x1, -W / 2, z1), (x1, W / 2, z1), (x0, W / 2, z0))
    quad((-Lx / 2, -W / 2, -H / 2), (-Lx / 2, W / 2, -H / 2), (-Lx / 2, W / 2, H / 2), (-Lx / 2, -W / 2, H / 2))
    for sy in (-W / 2, W / 2):
        poly = [(-Lx / 2, sy, H / 2)] + [(x, sy, z) for x, z in pts] + [(Lx / 2, sy, H / 2 - 0.3)]
        vs = [bm.verts.new(p) for p in poly]
        bm.faces.new(vs)
    bmesh.ops.remove_doubles(bm, verts=bm.verts, dist=1e-4)
    bm.to_mesh(me); bm.free()
    ob = link(bpy.data.objects.new('_bk', me)); me.materials.append(M['bucket'])
    md = ob.modifiers.new('Esp', 'SOLIDIFY'); md.thickness = 0.18
    return ob


bsrc = bucket_mesh()
tooth = None
if 'tooth' not in _MESH:
    t_ob = prim('cone', '_tooth', (0, 0, 0), M['teeth'], vertices=6, radius1=0.28, radius2=0.04, depth=1.0)
    t_ob.data.transform(Matrix.Rotation(-math.pi / 2, 4, 'Y'))
    _MESH['tooth'] = t_ob.data; bpy.data.objects.remove(t_ob)
lip = unit_box('lip', (0.35, 3.3, 0.45), M['accent'])
for i in range(18):
    a = i * 2 * math.pi / 18
    piv = empty(f'CacambaPiv{i}', (0, 0, 0), wheel); piv.rotation_euler.y = -a
    b = link(bpy.data.objects.new(f'Cacamba{i}', bsrc.data)); b.parent = piv
    b.location = (R_W - 1.6, 0, 0); b.rotation_euler = (0, -math.pi / 2, 0)
    sol = b.modifiers.new('Esp', 'SOLIDIFY'); sol.thickness = 0.18
    inst(lip, (R_W - 0.1, 0, 1.6), parent=piv, name='Labio')
    for j in range(5):
        inst(_MESH['tooth'], (R_W + 0.45, -1.3 + j * 0.65, 1.75), (0, -0.25, 0), parent=piv, name='Dente')
bpy.data.objects.remove(bsrc)
# terra caindo do alto da roda para a correia
fall = []
for i in range(14):
    c = inst(chm, (random.uniform(-2.0, 1.0), random.uniform(-1.0, 1.0), R_W - 1.0 - i * 0.65), (random.uniform(0, 3), random.uniform(0, 3), 0),
             (random.uniform(0.4, 0.9),) * 3, WHL, 'TerraCaindo')
    fall.append(c)
# contrapeso e braço de contrapeso
CW_P = Vector((-20, 0, 12)); CW_E = Vector((-72, 0, 20))
truss(CW_P, CW_E, 8, 7, 9, M['steel'], 0.8, 0.4, SUP, 'BracoContrapeso', walkway=True)
box('Contrapeso', (13, 12, 11), CW_E + Vector((-3, 0, -2)), M['dark2'], parent=SUP, bevel=0.3)
# cabos de sustentação (mastro -> ponta do braço, meio do braço, contrapeso)
TOP = Vector((4, 0, 86.6))
for sy in (-2.2, 2.2):
    rope(TOP + Vector((0, sy, 0)), HUB + Vector((-2, sy, 4)), 0.32, M['cable'], SUP)
    rope(TOP + Vector((0, sy, 0)), (PIV + HUB) / 2 + Vector((0, sy, 4)), 0.28, M['cable'], SUP)
    rope(TOP + Vector((0, sy, 0)), CW_E + Vector((0, sy, 4)), 0.32, M['cable'], SUP)
    rope(Vector((-20, sy, 50)), CW_E + Vector((-8, sy, 3)), 0.28, M['cable'], SUP)
# ponte de descarga (correia até a unidade de carga) — para trás
DP0 = Vector((-12, -10, 16)); DP1 = Vector((-128, -10, 12))
truss(DP0 - Vector((0, 0, 12.6)), DP1 - Vector((0, 0, 12.6)), 6, 5, 16, M['steel'], 0.6, 0.3, B, 'PonteDescarga', walkway=True)
dbelt, dL = frame_between(DP0 - Vector((0, 0, 9.6)), DP1 - Vector((0, 0, 9.6)), B, 'CorreiaDescarga')
box('CorreiaLona2', (dL, 2.4, 0.3), (dL / 2, 0, 0), M['belt'], parent=dbelt, bevel=0)
for i in range(int(dL / 4)):
    inst(chm, (i * 4 + random.uniform(-1, 1), 0, 0.5), (0, 0, random.uniform(0, 3)), parent=dbelt, name='TerraDesc')
carro_desc = empty('UnidadeCarga', (-130, -10, 0), B)
for cy in (-3.5, 3.5):
    crawler((0, cy, 0), carro_desc)
box('UnidadeCorpo', (12, 12, 5), (0, 0, 6.5), M['steel'], parent=carro_desc, bevel=0.2)
beam((0, 0, 9), (0, 0, 14.5), 2.2, M['steel2'], carro_desc, 'UnidadeColuna')
# luzes de trabalho ao longo do braço
for i in range(8):
    p = PIV.lerp(HUB, (i + 0.5) / 8)
    box('LuzBraco', (0.7, 0.7, 0.4), (p.x, p.y - 5.0, p.z - 4.4), M['lamp'], parent=SUP, bevel=0)
# cabo de energia no chão (alimentação elétrica)
for i in range(12):
    p0 = Vector((-30 - i * 18, 40 + 6 * math.sin(i), 0.4)); p1 = Vector((-48 - i * 18, 40 + 6 * math.sin(i + 1), 0.4))
    rope(p0, p1, 0.4, M['dark'], None)

# ================================================================== MINA A CÉU ABERTO (degraus, camadas)
MINE = empty('Mina', (0, 0, 0))
LAYERS = [(-60, -40, 'l_floor'), (-40, -33, 'l_sand'), (-33, -27, 'l_coal'), (-27, -18, 'l_clay'), (-18, -8, 'l_sand'),
          (-8, -1.5, 'l_clay'), (-1.5, 0, 'l_floor'), (0, 9, 'l_sand'), (9, 19, 'l_clay'), (19, 26, 'l_top'), (26, 27.2, 'l_grass')]


def block(x0, x1, y0, y1, z0, z1, name='Bancada'):
    """bloco de terreno com faixas de camadas (cores) entre z0 e z1."""
    for a, b_, m in LAYERS:
        lo, hi = max(a, z0), min(b_, z1)
        if hi - lo > 0.01:
            box(name, (x1 - x0, y1 - y0, hi - lo), ((x0 + x1) / 2, (y0 + y1) / 2, (lo + hi) / 2), M[m], parent=MINE, bevel=0.0)


# bancada onde a máquina trabalha (topo z=0) e a "montanha" sendo comida à frente (z até 27)
block(-420, 103, -70, 160, -40, 0, 'BancadaMaquina')
block(103, 520, -70, 160, -40, 27.2, 'Montanha')
# corte em degrau na frente da roda (a mordida)
block(96, 103, -70, -14, -40, 0)
# degraus descendo em direção à câmera (y negativo)
for i, (y0, y1, ztop) in enumerate([(-110, -70, -12), (-150, -110, -24), (-200, -150, -36)]):
    block(-420, 520, y0, y1, -60, ztop, f'Degrau{i}')
box('FundoCava', (940, 260, 0.6), (50, -330, -48.3), M['l_floor'], parent=MINE, bevel=0)
box('Poca', (60, 40, 0.2), (-80, -260, -47.9), M['water'], parent=MINE, bevel=0)
# borda alta atrás (y positivo) e campo/horizonte
block(-420, 520, 160, 240, -40, 27.2, 'Borda')
box('CampoFundo', (6000, 3000, 1), (0, 1700, 26.7), M['l_grass'], parent=MINE, bevel=0)
box('CampoLado', (3000, 3000, 1), (2000, -400, 26.7), M['l_grass'], parent=MINE, bevel=0)
box('CampoLado2', (3000, 3000, 1), (-1930, -400, 26.7), M['l_grass'], parent=MINE, bevel=0)
for i in range(90):  # árvores e campos no horizonte
    x, y = random.uniform(-1200, 1200), random.uniform(260, 1300)
    s = random.uniform(4, 9)
    prim('cone', 'ArvHoriz', (x, y, 27 + s * 1.2), M['tree'], vertices=6, radius1=s * 0.6, depth=s * 2.4)
for i in range(7):  # torres de linha de transmissão no horizonte
    x = -900 + i * 300; y = 700
    for a in (0.3, -0.3):
        beam((x - 6, y, 27), (x, y, 27 + 42), 0.8, M['pole'], None, 'Torre')
        beam((x + 6, y, 27), (x, y, 27 + 42), 0.8, M['pole'], None, 'Torre')
    beam((x - 9, y, 60), (x + 9, y, 60), 0.7, M['pole'], None, 'TorreBraco')
    if i < 6:
        rope((x - 8, y, 60), (x + 292, y, 60), 0.12, M['cable'], None)
# correias de bancada saindo da mina
for yb, zb in ((-90, -11.6), (-130, -23.6)):
    cb, cL = frame_between((-400, yb, zb + 1.4), (480, yb, zb + 1.4), None, 'CorreiaBancada')
    box('CorrBancLona', (cL, 2.0, 0.3), (cL / 2, 0, 0), M['belt'], parent=cb, bevel=0)
    for i in range(0, int(cL), 6):
        inst(unit_box('cbsup', (0.4, 2.6, 1.4), M['steel2']), (i, 0, -0.7), parent=cb, name='CorrBancSup')
        if i % 12 == 0:
            inst(chm, (i + 2, 0, 0.5), parent=cb, name='TerraBanc')


# ------------------------------------------------------------------ outros equipamentos, caminhões e pessoas (escala)
def haul_truck(loc, rotz=0.0):
    g = empty('Caminhao', loc); g.rotation_euler.z = rotz
    box('CamChassi', (9.5, 4.6, 1.4), (0, 0, 2.2), M['dark2'], parent=g, bevel=0.1)
    box('CamCacamba', (7.0, 5.4, 3.0), (-1.3, 0, 4.4), M['truck'], parent=g, bevel=0.25)
    box('CamCabine', (2.6, 2.4, 2.2), (3.6, -1.2, 4.0), M['truck'], parent=g, bevel=0.15)
    box('CamVidro', (0.1, 2.0, 1.0), (4.92, -1.2, 4.3), M['glass'], parent=g, bevel=0)
    for x in (3.4, -2.2, -4.2):
        for sy in (-1, 1):
            prim('cyl', 'CamRoda', (x, sy * 2.5, 1.3), M['dark'], g, rot=(math.pi / 2, 0, 0), vertices=14, radius=1.3, depth=1.2)
    return g


def dozer(loc, rotz=0.0):
    g = empty('Trator', loc); g.rotation_euler.z = rotz
    for sy in (-1, 1):
        box('TratEst', (5.0, 0.9, 1.2), (0, sy * 1.6, 0.6), M['dark'], parent=g, bevel=0.2)
    box('TratCorpo', (3.8, 2.6, 1.6), (-0.3, 0, 1.9), M['truck'], parent=g, bevel=0.15)
    box('TratCab', (1.6, 1.8, 1.6), (-0.8, 0, 3.4), M['glass'], parent=g, bevel=0.1)
    box('TratLamina', (0.4, 4.0, 1.4), (2.9, 0, 0.9), M['dark2'], parent=g, bevel=0.05)
    return g


def person(loc, rotz=0.0, parent=None):
    g = empty('Pessoa', loc, parent); g.rotation_euler.z = rotz
    if 'p_body' not in _MESH:
        o = prim('cyl', '_pb', (0, 0, 0), M['vest'], vertices=8, radius=0.25, depth=1.0); _MESH['p_body'] = o.data; bpy.data.objects.remove(o)
        o = prim('uv', '_ph', (0, 0, 0), M['skin'], segments=8, ring_count=6, radius=0.14); _MESH['p_head'] = o.data; bpy.data.objects.remove(o)
        o = prim('uv', '_pc', (0, 0, 0), M['hat'], segments=8, ring_count=4, radius=0.16, scale=(1, 1, 0.6)); _MESH['p_hat'] = o.data; bpy.data.objects.remove(o)
        o = prim('cyl', '_pl', (0, 0, 0), M['dark2'], vertices=6, radius=0.1, depth=0.8); _MESH['p_leg'] = o.data; bpy.data.objects.remove(o)
    inst(_MESH['p_body'], (0, 0, 1.2), parent=g, name='PCorpo')
    inst(_MESH['p_head'], (0, 0, 1.85), parent=g, name='PCabeca')
    inst(_MESH['p_hat'], (0, 0, 1.97), parent=g, name='PCapacete')
    for sx in (-1, 1):
        inst(_MESH['p_leg'], (0, sx * 0.12, 0.4), parent=g, name='PPerna')
    return g


for (x, y, z, r) in ((-40, -95, -12, 0.2), (60, -88, -12, 3.1), (-150, -135, -24, 0.1), (140, -128, -24, 2.9), (10, -180, -36, 1.4)):
    haul_truck((x, y, z), r)
for (x, y, z, r) in ((70, -40, 0, 1.0), (-60, -52, 0, 2.4), (-200, -100, -12, 0.5)):
    dozer((x, y, z), r)
for i in range(16):
    person((random.uniform(-40, 60), random.uniform(-60, -30), 0), random.uniform(0, 6.28))

# ------------------------------------------------------------------ poeira e partículas (na mordida da roda)
dust_src = prim('ico', 'PoeiraSrc', (0, 0, -500), M['dust'], subdivisions=1, radius=1.0)
dem = prim('plane', 'PoeiraEmissor', (100.5, -12, 6), None, size=1, scale=(4, 12, 8), rot=(0, math.pi / 2, 0))
ps = dem.modifiers.new('Poeira', 'PARTICLE_SYSTEM').particle_system; st = ps.settings
st.count = 420; st.frame_start = 1; st.frame_end = 90; st.lifetime = 70; st.lifetime_random = 0.5
st.normal_factor = 1.5; st.factor_random = 1.6; st.object_align_factor = (-0.6, -0.4, 1.2)
st.render_type = 'OBJECT'; st.instance_object = dust_src; st.particle_size = 1.4; st.size_random = 0.7
st.effector_weights.gravity = -0.03; st.drag_factor = 0.6
dem.show_instancer_for_render = False
mote = prim('ico', 'GraoSrc', (0, 0, -500), M['lamp'], subdivisions=1, radius=1.0)
gem = prim('plane', 'GraosEmissor', (96, -10, 14), None, size=1, scale=(6, 14, 10), rot=(0, math.pi / 2, 0))
ps2 = gem.modifiers.new('Graos', 'PARTICLE_SYSTEM').particle_system; s2 = ps2.settings
s2.count = 260; s2.frame_start = 1; s2.frame_end = 90; s2.lifetime = 80
s2.normal_factor = 0.6; s2.factor_random = 2.0; s2.render_type = 'OBJECT'; s2.instance_object = mote
s2.particle_size = 0.05; s2.size_random = 0.6; s2.effector_weights.gravity = 0.02
gem.show_instancer_for_render = False

# ------------------------------------------------------------------ comparações de escala (sets)
def cristo(loc, s=1.0, name='Cristo'):
    """silhueta simples do Cristo Redentor (38 m: pedestal 8 m + estátua ~30 m), sem rosto."""
    g = empty(name, loc)
    box(name + 'Pedestal', (9, 9, 8), (0, 0, 4), M['stone'], parent=g, bevel=0.2)
    prim('cone', name + 'Manto', (0, 0, 8 + 11), M['stone'], g, vertices=12, radius1=3.6, radius2=2.4, depth=22)
    box(name + 'Bracos', (2.6, 28, 2.6), (0, 0, 8 + 21.5), M['stone'], parent=g, bevel=0.3)
    prim('uv', name + 'Cabeca', (0, 0, 8 + 25.8), M['stone'], g, segments=12, ring_count=8, radius=2.0)
    box(name + 'Peito', (4, 6, 6), (0, 0, 8 + 19.5), M['stone'], parent=g, bevel=0.4)
    return g


CR = empty('SetCristos', (0, 0, 0))
c1 = cristo((58, 30, 0), name='Cristo1'); c1.parent = CR
c2 = cristo((58, 30, 38), name='Cristo2'); c2.parent = CR
regua = box('Regua96', (2.2, 2.2, 96), (-36, 0, 48), M['accent'], bevel=0.1); regua.parent = CR
for j in range(0, 96, 8):
    box('ReguaMarca', (3.4, 2.4, 0.8), (-36, 0, j), M['dark'], parent=CR, bevel=0)
CAMPOS = empty('SetCampos', (0, 0, 0))
for i, cx in enumerate((-60, 52)):
    fz = empty(f'Campo{i}', (cx, 0, 0.06), CAMPOS)
    for k_ in range(10):
        box('CampoFaixa', (10.5, 68, 0.06), (-52.5 + 5.25 + k_ * 10.5, 0, 0), M['field'] if k_ % 2 else M['field2'], parent=fz, bevel=0)
    for (sx, sy, lx, ly) in ((0, 34, 105, 0.3), (0, -34, 105, 0.3), (52.5, 0, 0.3, 68), (-52.5, 0, 0.3, 68), (0, 0, 0.3, 68)):
        box('CampoLinha', (lx, ly, 0.08), (sx, sy, 0.05), M['line'], parent=fz, bevel=0)
    prim('torus', 'CampoCirculo', (0, 0, 0.08), M['line'], fz, major_segments=40, minor_segments=4, major_radius=9.15, minor_radius=0.15, scale=(1, 1, 0.3))
    for sx in (-1, 1):
        box('CampoArea', (16.5, 40.3, 0.08), (sx * (52.5 - 8.25), 0, 0.04), M['field'], parent=fz, bevel=0)
        for (ax, ay, alx, aly) in ((sx * (52.5 - 16.5), 0, 0.3, 40.3), (sx * (52.5 - 8.25), 20.15, 16.5, 0.3), (sx * (52.5 - 8.25), -20.15, 16.5, 0.3)):
            box('CampoLinha', (alx, aly, 0.1), (ax, ay, 0.06), M['line'], parent=fz, bevel=0)

# set da rodovia (mudança de 2001) — longe, em campo aberto
RD = empty('SetRodovia', (4000, 0, 0))
box('RodChao', (2400, 2400, 1), (0, 0, -0.5), M['crop2'], parent=RD, bevel=0)
for i in range(40):
    box('RodLavoura', (random.uniform(80, 220), random.uniform(80, 220), 0.3), (random.uniform(-1100, 1100), random.uniform(60, 1100) * random.choice((-1, 1)), 0.05),
        M['crop1'] if i % 2 else M['crop2'], parent=RD, bevel=0)
box('RodPista', (2400, 24, 0.3), (0, 0, 0.15), M['asphalt'], parent=RD, bevel=0)
for sy in (-6, 6):
    for i in range(-60, 60):
        box('RodFaixa', (6, 0.25, 0.05), (i * 20, sy, 0.32), M['lane'], parent=RD, bevel=0)
for sy in (-12.5, 12.5):
    box('RodGuarda', (2400, 0.3, 0.8), (0, sy, 0.8), M['steel2'], parent=RD, bevel=0)
box('RodCanteiro', (2400, 2.0, 0.6), (0, 0, 0.3), M['l_grass'], parent=RD, bevel=0)
box('CaminhoPreparado', (70, 1200, 1.2), (0, 0, 0.6), M['l_road'], parent=RD, bevel=0.4)
for sx in (-1, 1):
    box('CaminhoTalude', (6, 1200, 0.6), (sx * 38, 0, 0.3), M['l_sand'], parent=RD, bevel=0.3)
cars_m = [M['car1'], M['car2'], M['car3'], M['car4']]


def car(loc, rotz, m, parent):
    g = empty('Carro', loc, parent); g.rotation_euler.z = rotz
    box('CarroCorpo', (4.4, 1.9, 0.9), (0, 0, 0.75), m, parent=g, bevel=0.12)
    box('CarroTeto', (2.3, 1.7, 0.7), (-0.2, 0, 1.45), M['glass'], parent=g, bevel=0.08)
    for sx in (-1, 1):
        for sy in (-1, 1):
            prim('cyl', 'CarroRoda', (sx * 1.4, sy * 0.95, 0.38), M['dark'], g, rot=(math.pi / 2, 0, 0), vertices=10, radius=0.38, depth=0.25)
    return g


for side, sy in ((-1, -9), (1, 9)):
    for i in range(14):
        car((side * (52 + i * 7.5), sy if i % 2 else sy * 0.35, 0.3), 0 if side < 0 else math.pi, cars_m[i % 4], RD)
for i in range(40):
    person((random.uniform(-30, 30) + random.choice((-75, 75)), random.uniform(16, 30) * random.choice((-1, 1)), 0.3), random.uniform(0, 6.28), RD)
for i in range(60):
    x, y = random.uniform(-900, 900), random.uniform(-900, 900)
    if abs(y) < 40 or abs(x) < 60:
        continue
    s = random.uniform(5, 10)
    prim('cyl', 'RodTronco', (x, y, s * 0.5), M['trunk'], RD, vertices=5, radius=s * 0.07, depth=s)
    prim('ico', 'RodCopa', (x, y, s * 1.3), M['tree'], RD, subdivisions=1, radius=s * 0.6)

# ------------------------------------------------------------------ mascote (Eng. Carlin) para escala
mas = Mascot('Carlin', (34, -11.5, 0), rotz=math.radians(-150))
helmet_band(mas, 'Eng. Carlin', FONT, M['band'], M['bandtxt'])
mas.headpivot.animation_data_clear(); mas.headpivot.rotation_euler = (math.radians(-28), 0, 0)
for a in mas.arms:
    a.animation_data_clear()
mas.arms[1].rotation_euler = (0, math.radians(150), 0)

# ================================================================== animação (para motion blur e partículas)
wheel.rotation_euler.y = 0
wheel.keyframe_insert('rotation_euler', frame=1)
wheel.rotation_euler.y = -math.radians(90 * 3)   # gira ~ 3 voltas/ 3 s (exagero para o blur)
wheel.keyframe_insert('rotation_euler', frame=90)
for fc in wheel.animation_data.action.fcurves:
    for kp in fc.keyframe_points:
        kp.interpolation = 'LINEAR'
for c in belt_chunks:
    c.keyframe_insert('location', frame=1)
    c.location.x += 6.0
    c.keyframe_insert('location', frame=90)
    for fc in c.animation_data.action.fcurves:
        for kp in fc.keyframe_points:
            kp.interpolation = 'LINEAR'
for c in fall:
    c.keyframe_insert('location', frame=1)
    c.location.z -= 3.0
    c.keyframe_insert('location', frame=90)
with bpy.context.temp_override(scene=sc):
    bpy.ops.ptcache.bake_all(bake=True)

# ================================================================== câmera e quadros de teste
cd = bpy.data.cameras.new('Cam'); cd.sensor_fit = 'VERTICAL'; cd.sensor_height = 24; cd.clip_start = 0.5; cd.clip_end = 6000
cam = link(bpy.data.objects.new('Cam', cd)); sc.camera = cam
tgt = empty('CamAlvo')
trk = cam.constraints.new('TRACK_TO'); trk.target = tgt; trk.track_axis = 'TRACK_NEGATIVE_Z'; trk.up_axis = 'UP_Y'

SETS = {'cristos': CR, 'campos': CAMPOS}


def show_set(name_on):
    for nm, ob in SETS.items():
        on = (nm == name_on)
        for x in [ob] + list(ob.children_recursive):
            x.hide_render = not on


# sol: azimute de cada plano (golden hour, sol baixo ~10-14°)
def set_sun(elev, azim):
    sun.rotation_euler = Euler((math.radians(90 - elev), 0, math.radians(azim)), 'XYZ')


SHOTS = [
    # nome, câmera, alvo, lente, sol(elev, azim), set, posição/rotação da máquina, mascote
    ('01_gancho_engole_montanhas', (78, -50, 3.5), (97, -6, 17), 17, (8, 60), None, ((0, 0, 0), 0), None),
    ('02_roda_cavando_close', (100.5, -27, 5.5), (95, -7, 13), 22, (10, 140), None, ((0, 0, 0), 0), None),
    ('03_escala_dois_cristos', (20, -470, 50), (10, 0, 47), 40, (13, -55), 'cristos', ((0, 0, 0), 0), None),
    ('04_drone_dois_campos', (-12, -1, 520), (-12, 0, 0), 30, (14, -70), 'campos', ((0, 0, 0), 0), None),
    ('05_esteiras_camera_baixa', (40, -23, 1.1), (16, -4, 12), 14, (10, -40), None, ((0, 0, 0), 0), (31.5, -15.5, 0)),
    ('06_mudanca_rodovia', (4000 - 120, -118, 42), (4000 - 5, 30, 26), 20, (8, -35), 'rodovia', ((4000, 25, 1.2), math.radians(90)), (4000 + 52, -20, 0.3)),
]
times = []
for name, cpos, ctgt, lens, (el, az), set_, (mloc, mrot), mpos in SHOTS:
    if ONLY and not any(name.startswith(o) for o in ONLY):
        continue
    show_set(set_)
    RD_on = (set_ == 'rodovia')
    for x in [RD] + list(RD.children_recursive):
        x.hide_render = not RD_on
    for x in [MINE] + list(MINE.children_recursive):
        x.hide_render = RD_on
    B.location = mloc; B.rotation_euler = (0, 0, mrot)
    if mpos:
        mas.pos.location = mpos
        mas.pos.hide_render = False
    for x in [mas.pos] + list(mas.pos.children_recursive):
        x.hide_render = mpos is None
    set_sun(el, az)
    cam.location = cpos; tgt.location = ctgt; cd.lens = lens
    if name.startswith('04'):   # drone de cima: eixo da máquina na vertical da tela
        trk.mute = True; cam.rotation_euler = (0, 0, math.radians(90))
    else:
        trk.mute = False
    sc.frame_set(FR)
    sc.render.filepath = os.path.join(OUT, name + '.png')
    t0 = time.time()
    bpy.ops.render.render(write_still=True)
    dt = time.time() - t0
    times.append((name, dt))
    print(f'RENDER {name} {dt:.1f}s', flush=True)
print('TEMPOS', times)
