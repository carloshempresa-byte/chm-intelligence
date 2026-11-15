"""Biblioteca reutilizável para os episódios: materiais chapados, peças low-poly,
keyframes com easing, mascote low-poly com reações e câmera.
Feito para Blender 3.6 (EEVEE legado), rodando headless:
    blender -b --factory-startup -P cena_epXX.py
"""
import bpy, bmesh, math
from mathutils import Vector

FPS = 30


def F(t):
    """segundos -> frame (frame 1 = t 0)"""
    return int(round(t * FPS)) + 1


def hexrgb(h, a=1.0):
    h = h.lstrip('#')
    c = [int(h[i:i + 2], 16) / 255 for i in (0, 2, 4)]
    # sRGB -> linear
    c = [x / 12.92 if x <= 0.04045 else ((x + 0.055) / 1.055) ** 2.4 for x in c]
    return (*c, a)


_MATS = {}


def mat(name, color, rough=0.6, emit=None, emit_strength=0.0, alpha=1.0, metal=0.0, spec=0.3):
    if name in _MATS:
        return _MATS[name]
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    p = m.node_tree.nodes['Principled BSDF']
    p.inputs['Base Color'].default_value = hexrgb(color)
    p.inputs['Roughness'].default_value = rough
    p.inputs['Metallic'].default_value = metal
    p.inputs['Specular'].default_value = spec
    if emit:
        p.inputs['Emission'].default_value = hexrgb(emit)
        p.inputs['Emission Strength'].default_value = emit_strength
    if alpha < 1.0:
        p.inputs['Alpha'].default_value = alpha
        m.blend_method = 'BLEND'
        m.shadow_method = 'NONE'
        m.show_transparent_back = False
    m.diffuse_color = hexrgb(color)
    _MATS[name] = m
    return m


def link(obj, coll=None):
    (coll or bpy.context.scene.collection).objects.link(obj)
    return obj


def _box_into(bm, size, offset=(0, 0, 0), segx=1, segz=1):
    sx, sy, sz = size
    ox, oy, oz = offset
    # grade em X e Z para permitir deformação (flexão, torção, ondulação)
    xs = [ox - sx / 2 + sx * i / segx for i in range(segx + 1)]
    zs = [oz - sz / 2 + sz * j / segz for j in range(segz + 1)]
    ys = [oy - sy / 2, oy + sy / 2]
    V = {}
    for i, x in enumerate(xs):
        for k, y in enumerate(ys):
            for j, z in enumerate(zs):
                V[i, k, j] = bm.verts.new((x, y, z))
    f = bm.faces.new
    for i in range(segx):
        for j in range(segz):
            f((V[i, 0, j], V[i + 1, 0, j], V[i + 1, 0, j + 1], V[i, 0, j + 1]))  # frente (-y)
            f((V[i, 1, j], V[i, 1, j + 1], V[i + 1, 1, j + 1], V[i + 1, 1, j]))  # trás
    for i in range(segx):
        f((V[i, 0, 0], V[i, 1, 0], V[i + 1, 1, 0], V[i + 1, 0, 0]))  # baixo
        f((V[i, 0, segz], V[i + 1, 0, segz], V[i + 1, 1, segz], V[i, 1, segz]))  # cima
    for j in range(segz):
        f((V[0, 0, j], V[0, 0, j + 1], V[0, 1, j + 1], V[0, 1, j]))  # ponta -x
        f((V[segx, 0, j], V[segx, 1, j], V[segx, 1, j + 1], V[segx, 0, j + 1]))  # ponta +x


def box(name, size, loc=(0, 0, 0), material=None, segx=1, segz=1, bevel=0.02, parts=None, parent=None):
    """Caixa (ou várias caixas unidas em `parts=[(size, offset), ...]`) com origem em loc."""
    me = bpy.data.meshes.new(name)
    bm = bmesh.new()
    for sz, off in (parts or [(size, (0, 0, 0))]):
        _box_into(bm, sz, off, segx, segz)
    bm.normal_update()
    bm.to_mesh(me)
    bm.free()
    ob = link(bpy.data.objects.new(name, me))
    ob.location = loc
    if material:
        ob.data.materials.append(material)
    if bevel:
        m = ob.modifiers.new('Bevel', 'BEVEL')
        m.width = bevel
        m.segments = 1
        m.limit_method = 'ANGLE'
        m.harden_normals = False
    if parent:
        ob.parent = parent
    return ob


def prim(kind, name, loc=(0, 0, 0), material=None, parent=None, rot=(0, 0, 0), scale=(1, 1, 1), **kw):
    ops = {
        'ico': bpy.ops.mesh.primitive_ico_sphere_add,
        'uv': bpy.ops.mesh.primitive_uv_sphere_add,
        'cyl': bpy.ops.mesh.primitive_cylinder_add,
        'cone': bpy.ops.mesh.primitive_cone_add,
        'cube': bpy.ops.mesh.primitive_cube_add,
        'torus': bpy.ops.mesh.primitive_torus_add,
        'plane': bpy.ops.mesh.primitive_plane_add,
    }
    ops[kind](location=loc, rotation=rot, **kw)
    ob = bpy.context.object
    ob.name = name
    ob.scale = scale
    if material:
        ob.data.materials.append(material)
    if parent:
        ob.parent = parent
    return ob


def empty(name, loc=(0, 0, 0), parent=None):
    e = link(bpy.data.objects.new(name, None))
    e.location = loc
    e.empty_display_size = 0.3
    if parent:
        e.parent = parent
    return e


# ---------------------------------------------------------------- keyframes
def _set_key_interp(ob, path, frame, ip, easing):
    ad = ob.animation_data if not isinstance(ob, bpy.types.ShaderNodeTree) else ob.animation_data
    if not ad or not ad.action:
        return
    for fc in ad.action.fcurves:
        if fc.data_path == path:
            for kp in fc.keyframe_points:
                if abs(kp.co.x - frame) < 0.5:
                    kp.interpolation = ip
                    if easing:
                        kp.easing = easing


def k(ob, path, t, value, ip='BEZIER', easing=None, frame=None):
    """Keyframe com interpolação definida (vale para o trecho que COMEÇA nesta chave).
    ip: BEZIER (ease in-out suave), LINEAR, CONSTANT, BACK, BOUNCE, ELASTIC, SINE, QUAD, CUBIC, EXPO."""
    fr = frame if frame is not None else F(t)
    if '.' in path and not path.startswith('modifiers') and not path.startswith('constraints'):
        raise ValueError(path)
    target = ob
    # suporta caminhos tipo 'location', 'scale', 'rotation_euler', 'modifiers["X"].angle'
    try:
        cur = target.path_resolve(path)
    except Exception:
        cur = None
    if hasattr(cur, '__len__') and not isinstance(value, (list, tuple, Vector)):
        raise ValueError('vector esperado em ' + path)
    if path.startswith('modifiers') or path.startswith('constraints'):
        head, attr = path.rsplit('.', 1)
        holder = target.path_resolve(head)
        setattr(holder, attr, value)
    else:
        setattr(target, path, value)
    target.keyframe_insert(data_path=path, frame=fr)
    _set_key_interp(target, path, fr, ip, easing)


def vis(ob, t, show, frame=None):
    fr = frame if frame is not None else F(t)
    ob.hide_render = not show
    ob.hide_viewport = not show
    ob.keyframe_insert('hide_render', frame=fr)
    ob.keyframe_insert('hide_viewport', frame=fr)


def pop_in(ob, t, dur=0.3, final=None):
    final = final or tuple(ob.scale)
    if t > 0.05:
        k(ob, 'scale', 0, (0.001,) * 3, 'CONSTANT', frame=F(t) - 1)
    k(ob, 'scale', t, (0.001,) * 3, 'BACK', 'EASE_OUT')
    k(ob, 'scale', t + dur, final)


def pop_out(ob, t, dur=0.25):
    s = tuple(ob.scale)
    k(ob, 'scale', t, s, 'BACK', 'EASE_IN')
    k(ob, 'scale', t + dur, (0.001,) * 3, 'CONSTANT')


def hidden_until(ob, t):
    final = tuple(ob.scale)
    ob.scale = (0.001,) * 3
    k(ob, 'scale', 0, (0.001,) * 3, 'CONSTANT', frame=1)
    ob.scale = final
    return final


def add_noise(ob, path, strength=0.05, scale=25.0, phase=0.0):
    ad = ob.animation_data
    for fc in ad.action.fcurves:
        if fc.data_path == path:
            m = fc.modifiers.new('NOISE')
            m.strength = strength
            m.scale = scale
            m.phase = phase + fc.array_index * 13.7


def ksock(mat_, input_name, t, value, ip='BEZIER', node='Principled BSDF'):
    """Keyframe num input de nó de material (ex.: força de emissão, alpha)."""
    nt = mat_.node_tree
    sock = nt.nodes[node].inputs[input_name]
    sock.default_value = value
    fr = F(t)
    sock.keyframe_insert('default_value', frame=fr)
    for fc in nt.animation_data.action.fcurves:
        if fc.data_path.endswith('default_value') and f'inputs[{list(nt.nodes[node].inputs).index(sock)}]' in fc.data_path:
            for kp in fc.keyframe_points:
                if abs(kp.co.x - fr) < 0.5:
                    kp.interpolation = ip


# ---------------------------------------------------------------- mascote
class Mascot:
    """Bonequinho low-poly: capacete amarelo, colete laranja. Olha para -Y."""

    def __init__(self, name='Mascote', loc=(0, 0, 0), rotz=0.0):
        M = {
            'skin': mat('m_skin', '#f2c39b', 0.7),
            'vest': mat('m_vest', '#ff7a1f', 0.6),
            'stripe': mat('m_stripe', '#f4f1e8', 0.4, emit='#ffffff', emit_strength=0.15),
            'pants': mat('m_pants', '#2c3e66', 0.7),
            'boot': mat('m_boot', '#3a2a20', 0.8),
            'hat': mat('m_hat', '#ffd23f', 0.35),
            'eye': mat('m_eye', '#141414', 0.3),
            'white': mat('m_eyewhite', '#ffffff', 0.4),
            'cheek': mat('m_cheek', '#f08a7a', 0.8),
            'sweat': mat('m_sweat', '#6ec6ff', 0.1, emit='#bfe8ff', emit_strength=0.4),
        }
        self.pos = empty(name + '_pos', loc)
        self.pos.rotation_euler.z = rotz
        self.jump = empty(name + '_jump', (0, 0, 0), self.pos)
        J = self.jump
        # pernas
        for sx in (-1, 1):
            prim('cyl', f'{name}_leg{sx}', (0.17 * sx, 0, 0.42), M['pants'], J, vertices=7, radius=0.13, depth=0.7)
            prim('cube', f'{name}_boot{sx}', (0.17 * sx, -0.06, 0.07), M['boot'], J, scale=(0.15, 0.22, 0.08))
        # corpo
        self.body = prim('cyl', f'{name}_body', (0, 0, 1.05), M['vest'], J, vertices=8, radius=0.36, depth=0.75)
        prim('cyl', f'{name}_stripe', (0, 0, 1.0), M['stripe'], J, vertices=8, radius=0.372, depth=0.09)
        prim('cyl', f'{name}_hip', (0, 0, 0.72), M['pants'], J, vertices=8, radius=0.33, depth=0.12)
        # cabeça
        self.headpivot = empty(f'{name}_headpivot', (0, 0, 1.45), J)
        H = self.headpivot
        self.head = prim('ico', f'{name}_head', (0, 0, 0.33), M['skin'], H, subdivisions=2, radius=0.36)
        prim('uv', f'{name}_hat', (0, 0, 0.47), M['hat'], H, segments=10, ring_count=6, radius=0.39, scale=(1, 1, 0.8))
        prim('cyl', f'{name}_brim', (0, -0.08, 0.47), M['hat'], H, vertices=10, radius=0.47, depth=0.05)
        prim('cube', f'{name}_hatridge', (0, 0, 0.74), M['hat'], H, scale=(0.05, 0.3, 0.06))
        self.eyes = []
        for sx in (-1, 1):
            e = prim('uv', f'{name}_eye{sx}', (0.13 * sx, -0.31, 0.33), M['eye'], H, segments=8, ring_count=6, radius=0.06, scale=(1, 0.6, 1.3))
            prim('uv', f'{name}_eyeshine{sx}', (0.13 * sx + 0.02, -0.345, 0.37), M['white'], H, segments=6, ring_count=4, radius=0.018)
            prim('uv', f'{name}_cheek{sx}', (0.22 * sx, -0.27, 0.22), M['cheek'], H, segments=6, ring_count=4, radius=0.06, scale=(1, 0.4, 0.7))
            self.eyes.append(e)
        self.mouth = prim('cube', f'{name}_mouth', (0, -0.335, 0.17), M['eye'], H, scale=(0.07, 0.02, 0.025))
        # braços (pivô no ombro)
        self.arms = []
        for sx in (-1, 1):
            sh = empty(f'{name}_shoulder{sx}', (0.42 * sx, 0, 1.33), J)
            prim('cyl', f'{name}_arm{sx}', (0, 0, -0.3), M['vest'], sh, vertices=6, radius=0.1, depth=0.55)
            prim('ico', f'{name}_hand{sx}', (0, 0, -0.62), M['skin'], sh, subdivisions=1, radius=0.12)
            sh.rotation_euler.y = 0.18 * sx
            self.arms.append(sh)
        # gotas de suor
        self.drops = []
        for i, sx in enumerate((-1, 1)):
            d = prim('uv', f'{name}_drop{sx}', (0.36 * sx, -0.1, 0.55), M['sweat'], H, segments=6, ring_count=5, radius=0.07, scale=(1, 1, 1.6))
            d.scale = (0.001,) * 3
            k(d, 'scale', 0, (0.001,) * 3, 'CONSTANT', frame=1)
            self.drops.append(d)
        k(self.jump, 'location', 0, (0, 0, 0), frame=1)
        for a in self.arms:
            k(a, 'rotation_euler', 0, tuple(a.rotation_euler), frame=1)
        k(self.headpivot, 'rotation_euler', 0, (0, 0, 0), frame=1)
        for e in self.eyes:
            k(e, 'scale', 0, (1, 0.6, 1.3), frame=1)

    def move(self, t, loc, rotz=None, cut=False):
        if cut:
            k(self.pos, 'location', t - 1 / FPS, tuple(self.pos.location), 'CONSTANT')
            if rotz is not None:
                k(self.pos, 'rotation_euler', t - 1 / FPS, tuple(self.pos.rotation_euler), 'CONSTANT')
        self.pos.location = loc
        k(self.pos, 'location', t, tuple(loc), 'CONSTANT' if cut else 'BEZIER')
        if rotz is not None:
            k(self.pos, 'rotation_euler', t, (0, 0, rotz), 'CONSTANT' if cut else 'BEZIER')

    def look(self, t, tilt=0.0, turn=0.0, dur=0.3):
        k(self.headpivot, 'rotation_euler', t, tuple(self.headpivot.rotation_euler))
        self.headpivot.rotation_euler = (tilt, 0, turn)
        k(self.headpivot, 'rotation_euler', t + dur, (tilt, 0, turn))

    def _arms(self, t, ang_l, ang_r, ip='BEZIER', easing=None):
        for a, ang in zip(self.arms, (ang_l, ang_r)):
            k(a, 'rotation_euler', t, (0, ang, 0), ip, easing)

    def _rest_arms(self, t):
        self._arms(t, -0.18, 0.18)

    def hop(self, t, h=0.35):
        k(self.jump, 'location', t, (0, 0, 0), 'QUAD', 'EASE_OUT')
        k(self.jump, 'location', t + 0.15, (0, 0, h), 'QUAD', 'EASE_IN')
        k(self.jump, 'location', t + 0.3, (0, 0, 0))

    def scared(self, t, hold=0.9):
        """Susto: pulo, braços pra cima, olhos arregalados, gotas de suor."""
        self._rest_arms(t - 0.05)
        k(self.jump, 'location', t, (0, 0, 0), 'QUAD', 'EASE_OUT')
        k(self.jump, 'location', t + 0.12, (0, 0, 0.55), 'BOUNCE', 'EASE_OUT')
        k(self.jump, 'location', t + 0.45, (0, 0, 0))
        self._arms(t + 0.1, -2.5, 2.5, 'BACK', 'EASE_OUT')
        self._arms(t + hold, -2.5, 2.5)
        self._rest_arms(t + hold + 0.3)
        for e in self.eyes:
            k(e, 'scale', t, (1, 0.6, 1.3), 'BACK', 'EASE_OUT')
            k(e, 'scale', t + 0.15, (1.5, 0.6, 1.9))
            k(e, 'scale', t + hold, (1.5, 0.6, 1.9))
            k(e, 'scale', t + hold + 0.25, (1, 0.6, 1.3))
        self.sweat(t + 0.1)

    def sweat(self, t):
        for i, d in enumerate(self.drops):
            sx = -1 if i == 0 else 1
            t0 = t + 0.08 * i
            k(d, 'location', t0, (0.36 * sx, -0.1, 0.55), 'LINEAR')
            k(d, 'scale', t0, (0.001,) * 3, 'BACK', 'EASE_OUT')
            k(d, 'scale', t0 + 0.15, (1, 1, 1.6))
            k(d, 'location', t0 + 0.7, (0.6 * sx, -0.1, 0.05), 'LINEAR')
            k(d, 'scale', t0 + 0.55, (1, 1, 1.6))
            k(d, 'scale', t0 + 0.75, (0.001,) * 3, 'CONSTANT')

    def celebrate(self, t, jumps=2, period=0.5):
        self._arms(t, -0.18, 0.18)
        for j in range(jumps):
            tj = t + 0.05 + j * period
            k(self.jump, 'location', tj, (0, 0, 0), 'QUAD', 'EASE_OUT')
            k(self.jump, 'location', tj + period * 0.45, (0, 0, 0.7), 'QUAD', 'EASE_IN')
            k(self.jump, 'location', tj + period * 0.9, (0, 0, 0))
            self._arms(tj, -2.7, 2.7, 'BACK', 'EASE_OUT')
            self._arms(tj + period * 0.5, -2.2, 2.2)
        self._arms(t + jumps * period + 0.1, -2.6, 2.6)
        self._rest_arms(t + jumps * period + 0.45)

    def wave_signal(self, t0, t1, period=0.45):
        """Sinaleiro: braço direito acenando (guiando o guindaste)."""
        t = t0
        self._arms(t, -0.18, 2.4)
        while t < t1:
            self._arms(t + period / 2, -0.18, 1.7)
            self._arms(t + period, -0.18, 2.5)
            t += period
        self._rest_arms(t1 + 0.3)


# ---------------------------------------------------------------- câmera
def camera_rig(name='Cam'):
    cd = bpy.data.cameras.new(name)
    cam = link(bpy.data.objects.new(name, cd))
    tgt = empty(name + '_target')
    c = cam.constraints.new('TRACK_TO')
    c.target = tgt
    c.track_axis = 'TRACK_NEGATIVE_Z'
    c.up_axis = 'UP_Y'
    cd.sensor_fit = 'VERTICAL'
    cd.sensor_height = 24
    cd.clip_end = 600
    bpy.context.scene.camera = cam
    return cam, tgt


def camera_path(cam, tgt, shots):
    """shots: lista de (t, loc, alvo, lente, modo) — modo 'cut' = corte seco a partir do anterior,
    'lin' = movimento linear até a próxima chave, padrão = ease in-out."""
    prev = None
    for t, loc, target, lens, mode in shots:
        if mode == 'cut' and prev is not None:
            pt, ploc, ptar, plens = prev
            fr = F(t) - 1
            k(cam, 'location', 0, ploc, 'CONSTANT', frame=fr)
            k(tgt, 'location', 0, ptar, 'CONSTANT', frame=fr)
            k(cam.data, 'lens', 0, plens, 'CONSTANT', frame=fr)
        ip = 'LINEAR' if mode == 'lin' else 'BEZIER'
        k(cam, 'location', t, loc, ip)
        k(tgt, 'location', t, target, ip)
        k(cam.data, 'lens', t, lens, ip)
        prev = (t, loc, target, lens)


def project_anchors(anchors, f0, f1, out_json):
    """Exporta a posição 2D (pixels) de cada âncora por quadro, para as etiquetas em pílula."""
    import json
    from bpy_extras.object_utils import world_to_camera_view
    sc = bpy.context.scene
    W, H = sc.render.resolution_x, sc.render.resolution_y
    data = {a.name: [] for a in anchors}
    for fr in range(f0, f1 + 1):
        sc.frame_set(fr)
        cam = sc.camera
        for a in anchors:
            p = a.matrix_world.translation
            v = world_to_camera_view(sc, cam, p)
            data[a.name].append([round(v.x * W, 1), round((1 - v.y) * H, 1), 1 if v.z > 0 else 0])
    json.dump({'f0': f0, 'W': W, 'H': H, 'anchors': data}, open(out_json, 'w'))


# ---------------------------------------------------------------- faixa do capacete (identidade visual)
def helmet_band(m, txt, font_path, mat_band, mat_txt, size=0.16):
    """Faixa branca em volta da cúpula do capacete com o nome do mascote enrolado na superfície
    (mesmo desenho da foto de perfil do canal). Texto vira malha e cada vértice é enrolado na cúpula."""
    H = m.headpivot
    piv = empty(m.headpivot.name + '_faixa', (0, 0, 0.47), H)
    RX, RZ = 0.39, 0.39 * 0.8
    H0, H1 = 0.02, 0.19
    rdome = lambda h: RX * math.sqrt(max(0.0, 1 - (h / RZ) ** 2)) + 0.012
    me = bpy.data.meshes.new('Faixa'); bm = bmesh.new()
    N, ROWS = 48, 4
    rings = []
    for r in range(ROWS + 1):
        h = H0 + (H1 - H0) * r / ROWS
        rings.append([bm.verts.new((rdome(h) * math.sin(2 * math.pi * i / N), -rdome(h) * math.cos(2 * math.pi * i / N), h)) for i in range(N)])
    for r in range(ROWS):
        for i in range(N):
            j = (i + 1) % N
            bm.faces.new((rings[r][i], rings[r][j], rings[r + 1][j], rings[r + 1][i]))
    bm.to_mesh(me); bm.free()
    band = link(bpy.data.objects.new(H.name + '_faixaMalha', me)); band.parent = piv; me.materials.append(mat_band)
    sol = band.modifiers.new('Esp', 'SOLIDIFY'); sol.thickness = 0.012; sol.offset = -1
    cu = bpy.data.curves.new('NomeTxt', 'FONT'); cu.body = txt; cu.size = size; cu.extrude = 0.006
    cu.align_x = 'CENTER'; cu.align_y = 'CENTER'; cu.font = bpy.data.fonts.load(font_path)
    t = link(bpy.data.objects.new(H.name + '_nome', cu))
    for o in bpy.context.selected_objects:
        o.select_set(False)
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
    t.parent = piv; t.data.materials.clear(); t.data.materials.append(mat_txt)
    t.select_set(False)
    ridge = bpy.data.objects.get(H.name.replace('_headpivot', '_hatridge'))
    if ridge:
        ridge.hide_render = True
    return band, t
