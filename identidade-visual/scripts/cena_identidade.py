"""Identidade visual do canal Engenharia Animada — cenas 3D low-poly (mesma paleta do EP01).
Uso:  blender -b --factory-startup -P cena_identidade.py -- <perfil|banner> <saida.png> [escala_res]
- perfil: mascote em close com o nome "Eng. Carlin" na faixa do capacete, fundo transparente (o fundo é feito no Pillow)
- banner: diorama da obra (caldeira, guindaste, viga caixão, mascote) 2560x1440"""
import bpy, sys, os, math, random
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '..', 'piloto-ep01', 'scripts'))
from lowpoly_lib import mat, box, prim, empty, link, hexrgb, Mascot

argv = sys.argv[sys.argv.index('--') + 1:]
MODE, OUT = argv[0], argv[1]
RES = float(argv[2]) if len(argv) > 2 else 1.0
FONT = os.path.join(HERE, '..', 'assets', 'Montserrat-Black.ttf')  # instância estática wght=900 (sem contornos sobrepostos)
random.seed(11)

bpy.ops.wm.read_factory_settings(use_empty=True)
sc = bpy.context.scene
sc.render.engine = 'BLENDER_EEVEE'
ee = sc.eevee
ee.taa_render_samples = 32
ee.use_soft_shadows = True
ee.shadow_cascade_size = '4096'
ee.shadow_cube_size = '1024'
ee.use_gtao = True; ee.gtao_distance = 1.2; ee.gtao_factor = 0.8
sc.view_settings.view_transform = 'Standard'
sc.render.image_settings.file_format = 'PNG'
sc.render.image_settings.color_mode = 'RGBA'

w = bpy.data.worlds.new('Ceu'); sc.world = w; w.use_nodes = True
nt = w.node_tree; bg = nt.nodes['Background']
tc = nt.nodes.new('ShaderNodeTexCoord'); sep = nt.nodes.new('ShaderNodeSeparateXYZ')
ramp = nt.nodes.new('ShaderNodeValToRGB')
mapr = nt.nodes.new('ShaderNodeMapRange'); mapr.inputs['From Min'].default_value = 0.5; mapr.inputs['From Max'].default_value = 0.75
nt.links.new(tc.outputs['Generated'], sep.inputs[0]); nt.links.new(sep.outputs['Z'], mapr.inputs['Value'])
nt.links.new(mapr.outputs['Result'], ramp.inputs['Fac'])
ramp.color_ramp.elements[0].color = hexrgb('#e6f4fb'); ramp.color_ramp.elements[1].color = hexrgb('#6fbde8')
nt.links.new(ramp.outputs['Color'], bg.inputs['Color']); bg.inputs['Strength'].default_value = 0.9

sun_d = bpy.data.lights.new('Sol', 'SUN'); sun_d.energy = 3.3; sun_d.angle = math.radians(7)
sun_d.color = hexrgb('#fff3e0')[:3]; sun_d.shadow_cascade_max_distance = 140
sun = link(bpy.data.objects.new('Sol', sun_d)); sun.rotation_euler = (math.radians(48), math.radians(8), math.radians(38))

P = dict(
    ground=mat('ground', '#e7d6ae', 0.95, spec=0.1), grass=mat('grass', '#a9cf7a', 0.95, spec=0.1),
    concrete=mat('concrete', '#c9c3b8', 0.9, spec=0.15), concrete_d=mat('concrete_d', '#aaa397', 0.9),
    asphalt=mat('asphalt', '#55595f', 0.9), lane=mat('lane', '#ffd23f', 0.6),
    flange=mat('flange', '#2f6fa3', 0.45, spec=0.5), web=mat('web', '#58a6d6', 0.45, spec=0.5),
    diaph=mat('diaph', '#f29e4c', 0.5), boiler=mat('boiler', '#e9e4da', 0.8), steel_d=mat('steel_d', '#3b4a5c', 0.6),
    red=mat('red', '#d64545', 0.6), white=mat('white', '#f7f7f2', 0.7), crane=mat('crane', '#f5c242', 0.45),
    dark=mat('dark', '#2a2d33', 0.7), glass=mat('glass', '#9fd6f2', 0.15), wood=mat('wood', '#b07a46', 0.9),
    tree=mat('tree', '#5fae5a', 0.9), trunk=mat('trunk', '#8a5a3b', 0.9), cone=mat('cone', '#ff7a1f', 0.6),
    cloud=mat('cloud', '#ffffff', 1.0, emit='#ffffff', emit_strength=0.3),
    cont1=mat('cont1', '#3e8e7e', 0.7), cont2=mat('cont2', '#c8553d', 0.7),
    badge=mat('badge', '#ffffff', 0.4), badge_txt=mat('badge_txt', '#2f6fa3', 0.4),
)


def camera(loc, target, lens, shift_y=0.0):
    cd = bpy.data.cameras.new('Cam'); cd.lens = lens; cd.shift_y = shift_y; cd.sensor_fit = 'HORIZONTAL'
    cam = link(bpy.data.objects.new('Cam', cd)); cam.location = loc
    tgt = empty('CamAlvo', target)
    c = cam.constraints.new('TRACK_TO'); c.target = tgt; c.track_axis = 'TRACK_NEGATIVE_Z'; c.up_axis = 'UP_Y'
    sc.camera = cam
    return cam


def text3d(name, txt, loc, size, material, parent=None, rot=(math.pi / 2, 0, 0), extrude=0.02):
    cu = bpy.data.curves.new(name, 'FONT'); cu.body = txt; cu.size = size; cu.extrude = extrude
    cu.align_x = 'CENTER'; cu.align_y = 'CENTER'
    f = bpy.data.fonts.load(FONT); cu.font = f
    ob = link(bpy.data.objects.new(name, cu)); ob.location = loc; ob.rotation_euler = rot
    ob.data.materials.append(material)
    if parent:
        ob.parent = parent
    return ob


HELMET_NAME = 'Eng. Carlin'  # nome do mascote, escrito na faixa do capacete


def helmet_band(m, txt=HELMET_NAME, size=0.16):
    """Faixa branca em volta da cúpula do capacete com o nome do mascote curvado acompanhando a cúpula.
    O texto é convertido em malha e cada vértice é enrolado na superfície (sem cortar letras)."""
    import bmesh
    H = m.headpivot
    piv = empty('FaixaPiv', (0, 0, 0.47), H)  # centro da cúpula (raio 0.39, achatada 0.8 em Z)
    RX, RZ = 0.39, 0.39 * 0.8
    H0, H1 = 0.02, 0.19  # altura da faixa acima da aba
    rdome = lambda h: RX * math.sqrt(max(0.0, 1 - (h / RZ) ** 2)) + 0.012
    # faixa: anel com o perfil da cúpula
    me = bpy.data.meshes.new('Faixa'); bm = bmesh.new()
    N, ROWS = 72, 6
    rings = []
    for r in range(ROWS + 1):
        h = H0 + (H1 - H0) * r / ROWS
        rings.append([bm.verts.new((rdome(h) * math.sin(2 * math.pi * i / N), -rdome(h) * math.cos(2 * math.pi * i / N), h)) for i in range(N)])
    for r in range(ROWS):
        for i in range(N):
            j = (i + 1) % N
            bm.faces.new((rings[r][i], rings[r][j], rings[r + 1][j], rings[r + 1][i]))
    bm.to_mesh(me); bm.free()
    band = link(bpy.data.objects.new('Faixa', me)); band.parent = piv; me.materials.append(P['badge'])
    sol = band.modifiers.new('Esp', 'SOLIDIFY'); sol.thickness = 0.012; sol.offset = -1
    # texto -> malha -> enrolado na faixa
    cu = bpy.data.curves.new('NomeTxt', 'FONT'); cu.body = txt; cu.size = size; cu.extrude = 0.006
    cu.align_x = 'CENTER'; cu.align_y = 'CENTER'; cu.font = bpy.data.fonts.load(FONT)
    t = link(bpy.data.objects.new('NomeTxt', cu))
    bpy.context.view_layer.objects.active = t; t.select_set(True)
    bpy.ops.object.convert(target='MESH')
    t = bpy.context.object
    xs = [v.co.x for v in t.data.vertices]; ys = [v.co.y for v in t.data.vertices]
    xc, yc = (min(xs) + max(xs)) / 2, (min(ys) + max(ys)) / 2
    hc = (H0 + H1) / 2
    R0 = rdome(hc)
    for v in t.data.vertices:
        x, y, z = v.co.x - xc, v.co.y - yc, v.co.z
        h = hc + y
        R = rdome(h) + 0.004 + (z + 0.006)
        th = x / R0
        v.co = (R * math.sin(th), -R * math.cos(th), h)
    t.parent = piv; t.data.materials.clear(); t.data.materials.append(P['badge_txt'])
    half_arc = math.degrees((max(xs) - min(xs)) / 2 / R0)
    print('FAIXA texto', txt, 'largura', round(max(xs) - min(xs), 3), 'arco ±%.0f°' % half_arc)
    bpy.data.objects[m.headpivot.name.replace('_headpivot', '_hatridge')].hide_render = True
    return band, t


def smile(m):
    """Troca a boca reta por um sorriso (meio toro)."""
    import bmesh
    m.mouth.hide_render = True
    sm = prim('torus', 'Sorriso', (0, -0.325, 0.2), m.mouth.data.materials[0], m.headpivot, rot=(math.pi / 2, 0, 0),
              major_segments=16, minor_segments=6, major_radius=0.085, minor_radius=0.022)
    bm = bmesh.new(); bm.from_mesh(sm.data)
    bmesh.ops.delete(bm, geom=[v for v in bm.verts if v.co.y > 0.005], context='VERTS')
    bm.to_mesh(sm.data); bm.free()
    return sm


def boiler(loc, s=1.0, chimney_x=17, chimney_segs=8):
    g = empty('Caldeira', loc)
    box('CaldCorpo', (14, 14, 46), (0, 0, 23), P['boiler'], parent=g, bevel=0.1)
    for j in range(9):
        box(f'CaldFaixa{j}', (14.5, 14.5, 0.6), (0, 0, 4 + j * 5), P['steel_d'], parent=g, bevel=0.05)
    for sx in (-1, 1):
        for sy in (-1, 1):
            box(f'CaldColuna{sx}{sy}', (1.2, 1.2, 52), (sx * 9, sy * 9, 26), P['steel_d'], parent=g, bevel=0.05)
    box('CaldTeto', (20, 20, 3), (0, 0, 53), P['steel_d'], parent=g, bevel=0.1)
    box('CaldCasa', (14, 10, 5), (0, 0, 57), P['boiler'], parent=g, bevel=0.1)
    prim('cyl', 'CaldTubulao', (0, -2, 49.5), P['red'], g, rot=(0, math.pi / 2, 0), vertices=12, radius=1.6, depth=13)
    box('CaldEscada', (3, 3, 50), (-10.8, -6, 25), P['crane'], parent=g, bevel=0.05)
    box('CaldPrecip', (12, 18, 16), (-22, 4, 8), P['boiler'], parent=g, bevel=0.1)
    box('CaldDuto', (10, 3, 3), (-12, 4, 14), P['steel_d'], parent=g, bevel=0.05)
    ch = empty('Chamine', (chimney_x, 10, 0), g)
    for j in range(chimney_segs):
        prim('cyl', f'ChamineSeg{j}', (0, 0, 4.5 + j * 9), P['red'] if j % 2 else P['white'], ch, vertices=12, radius=2.6 - j * 0.12, depth=9)
    g.scale = (s, s, s)
    return g


def box_girder(loc, L=14.0, s=1.0, rotz=0.0):
    g = empty('Viga', loc); g.rotation_euler.z = rotz
    for sx in (-1, 1):
        box(f'Apoio{sx}', (2.4, 3.4, 1.4), (sx * 5.8, 0, 0.7), P['concrete'], parent=g, bevel=0.04)
    v = empty('VigaCorpo', (0, 0, 2.6), g)
    box('MesaSup', (L, 2.6, 0.22), (0, 0, 1.09), P['flange'], parent=v, bevel=0.03)
    box('MesaInf', (L, 2.6, 0.22), (0, 0, -1.09), P['flange'], parent=v, bevel=0.03)
    for sy in (-1, 1):
        box(f'Alma{sy}', (L, 0.16, 1.96), (0, sy * 0.9, 0), P['web'], parent=v, bevel=0.01)
    for sx in (-1, 1):
        box(f'Diaf{sx}', (0.12, 1.66, 1.96), (sx * (L / 2 - 0.06), 0, 0), P['diaph'], parent=v, bevel=0.01)
    g.scale = (s, s, s)
    return g


def crane(loc, s=1.0, rotz=0.0, luff=55):
    g = empty('Guindaste', loc); g.rotation_euler.z = rotz
    for sx in (-1, 1):
        box(f'Esteira{sx}', (2.0, 8.5, 1.4), (sx * 2.4, 0, 0.7), P['dark'], parent=g, bevel=0.15)
    box('Giro', (4.6, 5.6, 0.6), (0, 0.5, 1.7), P['dark'], parent=g)
    box('Casa', (4.2, 6.5, 2.6), (0, 1.2, 3.3), P['crane'], parent=g, bevel=0.08)
    box('Cabine', (1.4, 1.8, 2.0), (-2.2, -1.6, 3.0), P['crane'], parent=g, bevel=0.06)
    box('CabineVidro', (1.45, 0.08, 1.2), (-2.2, -2.52, 3.3), P['glass'], parent=g, bevel=0)
    box('Contrapeso', (4.4, 2.0, 2.4), (0, 4.6, 3.4), P['steel_d'], parent=g, bevel=0.06)
    boom = empty('Lanca', (0, -1.6, 3.4), g); boom.rotation_euler.x = -math.radians(luff)
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
    g.scale = (s, s, s)
    return g, boom


def tree(x, y, s):
    prim('cyl', 'Tronco', (x, y, 1.0 * s), P['trunk'], vertices=5, radius=0.3 * s, depth=2 * s)
    prim('cone', 'Copa', (x, y, 3.6 * s), P['tree'], vertices=6, radius1=1.9 * s, depth=4.5 * s)


def cloud(x, y, z, r=4):
    for j in range(3):
        prim('ico', 'Nuvem', (x + j * r - r, y, z + (j == 1) * r * 0.35), P['cloud'], subdivisions=1, radius=r * random.uniform(0.8, 1.15), scale=(1.3, 1, 0.7))


# =============================================================== PERFIL
if MODE == 'perfil':
    sc.render.resolution_x = sc.render.resolution_y = int(800 * RES)
    sc.render.film_transparent = True
    m = Mascot('Mascote', (0, 0, 0), rotz=0.0)
    helmet_band(m)
    m.headpivot.rotation_euler = (math.radians(4), 0, math.radians(-2))
    # joinha: braço direito (lado +X) levantado
    m.arms[0].rotation_euler = (0, math.radians(-25), 0)
    m.arms[1].rotation_euler = (math.radians(-20), math.radians(150), math.radians(10))
    smile(m)
    sun.rotation_euler = (math.radians(52), math.radians(-6), math.radians(24))
    camera((0.55, -4.6, 2.05), (0.0, 0, 1.72), 82)
    sc.render.filepath = OUT
    bpy.ops.render.render(write_still=True)

# =============================================================== BANNER
else:
    # Câmera quase horizontal: horizonte em y≈760 px, céu limpo atrás do título.
    # Faixa segura (1546x423, centro): mascote à esquerda, caldeira à direita, título no meio (Pillow).
    # Fora dela (só aparece no desktop/TV): guindaste, viga caixão nos apoios, contêineres.
    sc.render.resolution_x, sc.render.resolution_y = int(2560 * RES), int(1440 * RES)
    mapr.inputs['From Max'].default_value = 0.56
    prim('plane', 'Chao', (0, 0, 0), P['ground'], size=1600)
    prim('cube', 'Estrada', (0, 40, 0.03), P['asphalt'], scale=(500, 3.0, 0.03))
    for i in range(-60, 61):
        prim('cube', 'Faixa', (i * 6, 40, 0.065), P['lane'], scale=(1.4, 0.12, 0.01))
    prim('cube', 'Patio', (0, 6, 0.05), P['concrete_d'], scale=(70, 14, 0.05))
    boiler((17.6, 8, 0), 0.172, chimney_x=12, chimney_segs=6)
    cr, boom = crane((-35, 22, 0), 1.0, rotz=math.radians(78), luff=62)
    box_girder((31, 0, 0), 14.0, 1.0, rotz=math.radians(28))
    for c, (x, y, rz) in enumerate([(44, 18, 10), (50, 24, -5), (-50, 10, 20), (-44, 16, 4)]):
        box(f'Cont{c}', (6, 2.4, 2.6), (x, y, 1.3), P['cont1'] if c % 2 else P['cont2'], bevel=0.05).rotation_euler.z = math.radians(rz)
    for i, (x, y) in enumerate([(-12.5, -3), (-21, -4), (11, -4), (24, -5), (-27, -3), (38, -6)]):
        s_ = 1.6
        prim('cone', 'Cone', (x, y, 0.35 * s_), P['cone'], vertices=8, radius1=0.28 * s_, radius2=0.04 * s_, depth=0.7 * s_)
    m = Mascot('Mascote', (-17.5, 0, 0.1), rotz=math.radians(18))
    m.pos.scale = (3.3,) * 3
    for ob in m.arms + [m.headpivot]:
        ob.animation_data_clear()  # o Mascot cria keyframes no quadro 1; sem isso a pose manual é ignorada
    m.arms[1].rotation_euler = (0, math.radians(-145), 0)  # acenando para o título
    m.headpivot.rotation_euler = (math.radians(-4), 0, math.radians(10))
    smile(m)
    # primeiro plano (só aparece na TV): pátio com faixa de segurança, tubos e madeira
    prim('cube', 'PatioFrente', (0, -45, 0.04), P['concrete'], scale=(90, 35, 0.04))
    for i in range(-30, 31):
        prim('cube', 'Zebra', (i * 3, -10.2, 0.09), P['crane'] if i % 2 else P['dark'], scale=(0.75, 0.25, 0.01))
    for j, (x, y) in enumerate([(-24, -52), (-22.6, -52), (-23.3, -51)]):
        prim('cyl', 'Tubo', (x, y, 0.65 + (j == 2) * 1.1), P['web'], rot=(math.pi / 2, 0, math.radians(20)), vertices=10, radius=0.65, depth=8)
    for j in range(4):
        box(f'Madeira{j}', (5, 1.0, 0.35), (17, -50, 0.18 + j * 0.36), P['wood'], bevel=0.03).rotation_euler.z = math.radians(-12 + j * 6)
    for i, (x, y) in enumerate([(-6, -48), (5, -55), (26, -46), (-34, -47)]):
        prim('cone', 'ConeF', (x, y, 0.5), P['cone'], vertices=8, radius1=0.4, radius2=0.05, depth=1.0)
    for i in range(140):
        x, y = random.uniform(-220, 220), random.uniform(50, 190)
        if abs(x) < 40 and y < 140:
            continue
        tree(x, y, random.uniform(1.2, 2.4))
    for (x, y, z, r) in [(-150, 260, 44, 9), (-60, 300, 58, 10), (70, 280, 52, 8), (160, 260, 40, 9),
                         (-230, 260, 30, 8), (230, 270, 32, 8), (5, 320, 72, 11)]:
        cloud(x, y, z, r)
    cam = camera((0, -90, 4.0), (0, 0, 4.0), 50, shift_y=40 / 2560)
    if 'dry' in argv:
        from bpy_extras.object_utils import world_to_camera_view
        bpy.context.view_layer.update()
        for nm in ('Caldeira', 'CaldCasa', 'Chamine', 'Mascote_pos', 'Mascote_headpivot', 'Viga', 'Guindaste', 'LancaPonta'):
            ob = bpy.data.objects[nm]
            v = world_to_camera_view(sc, cam, ob.matrix_world.translation)
            print('PROJ', nm, round(v.x * 2560), round((1 - v.y) * 1440))
        sys.exit(0)
    sc.render.filepath = OUT
    bpy.ops.render.render(write_still=True)
print('ok', OUT)
