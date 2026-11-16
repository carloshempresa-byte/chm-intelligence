"""Biblioteca de DETALHE (rodada 2 da Bagger 288): materiais procedurais com desgaste, perfis de treliça,
caçambas com dentes e corrente, esteiras com sapatas, correias em calha, pedras e terreno com relevo.
Tudo procedural e gratuito (Blender 3.6, EEVEE)."""
import bpy, bmesh, math, random
from mathutils import Vector, Matrix
from lowpoly_lib import hexrgb, link, empty

# ================================================================== materiais procedurais
def _nodes(m):
    m.use_nodes = True
    nt = m.node_tree
    for n in list(nt.nodes):
        nt.nodes.remove(n)
    out = nt.nodes.new('ShaderNodeOutputMaterial')
    bsdf = nt.nodes.new('ShaderNodeBsdfPrincipled')
    nt.links.new(bsdf.outputs[0], out.inputs[0])
    return nt, bsdf


def _noise(nt, scale, detail=4.0, rough=0.55, coord=None):
    n = nt.nodes.new('ShaderNodeTexNoise'); n.inputs['Scale'].default_value = scale
    n.inputs['Detail'].default_value = detail; n.inputs['Roughness'].default_value = rough
    if coord is not None:
        nt.links.new(coord, n.inputs['Vector'])
    return n


def _ramp(nt, inp, stops):
    r = nt.nodes.new('ShaderNodeValToRGB')
    el = r.color_ramp.elements
    el[0].position, el[0].color = stops[0][0], stops[0][1]
    el[1].position, el[1].color = stops[-1][0], stops[-1][1]
    for p, c in stops[1:-1]:
        e = el.new(p); e.color = c
    nt.links.new(inp, r.inputs[0])
    return r


def _mix(nt, fac, a, b, blend='MIX'):
    mx = nt.nodes.new('ShaderNodeMixRGB'); mx.blend_type = blend
    if isinstance(fac, float):
        mx.inputs[0].default_value = fac
    else:
        nt.links.new(fac, mx.inputs[0])
    for i, v in ((1, a), (2, b)):
        if isinstance(v, tuple):
            mx.inputs[i].default_value = v
        else:
            nt.links.new(v, mx.inputs[i])
    return mx.outputs[0]


def _math(nt, op, a, b=None, clamp=True):
    m = nt.nodes.new('ShaderNodeMath'); m.operation = op; m.use_clamp = clamp
    for i, v in ((0, a), (1, b)):
        if v is None:
            continue
        if isinstance(v, (int, float)):
            m.inputs[i].default_value = v
        else:
            nt.links.new(v, m.inputs[i])
    return m.outputs[0]


_PM = {}


def paint(name, base, rough=0.42, metal=0.25, dirt=0.8, rust=0.25, dirt_top=6.0, var=0.10):
    """tinta industrial: variação de tom, sujeira de terra subindo de baixo (por altura no mundo) e nas frestas (AO),
    manchas de ferrugem e roughness variado; leve bump de chapa."""
    if name in _PM:
        return _PM[name]
    m = bpy.data.materials.new(name); _PM[name] = m
    nt, b = _nodes(m)
    geo = nt.nodes.new('ShaderNodeNewGeometry')
    pos = geo.outputs['Position']
    base_c = hexrgb(base)
    # variação de tinta
    nv = _noise(nt, 0.09, 3.0, 0.6, pos)
    rv = _ramp(nt, nv.outputs['Fac'], [(0.3, tuple(c * (1 - var) for c in base_c[:3]) + (1,)), (0.7, tuple(min(1, c * (1 + var)) for c in base_c[:3]) + (1,))])
    col = rv.outputs[0]
    # ferrugem
    if rust > 0:
        nr = _noise(nt, 0.55, 6.0, 0.7, pos)
        rr = _ramp(nt, nr.outputs['Fac'], [(0.58, (0, 0, 0, 1)), (0.68, (1, 1, 1, 1))])
        rmask = _math(nt, 'MULTIPLY', rr.outputs[0], rust)
        col = _mix(nt, rmask, col, hexrgb('#7a3f22'))
    # sujeira: de baixo para cima (altura no mundo) e nas frestas
    if dirt > 0:
        sep = nt.nodes.new('ShaderNodeSeparateXYZ'); nt.links.new(pos, sep.inputs[0])
        mr = nt.nodes.new('ShaderNodeMapRange'); mr.inputs['From Min'].default_value = 0.5; mr.inputs['From Max'].default_value = dirt_top
        mr.inputs['To Min'].default_value = 1.0; mr.inputs['To Max'].default_value = 0.0
        nt.links.new(sep.outputs['Z'], mr.inputs['Value'])
        nd = _noise(nt, 0.35, 5.0, 0.65, pos)
        dmask = _math(nt, 'MULTIPLY', mr.outputs[0], nd.outputs['Fac'])
        dmask = _math(nt, 'MULTIPLY', dmask, dirt * 1.6)
        ao = nt.nodes.new('ShaderNodeAmbientOcclusion'); ao.inputs['Distance'].default_value = 0.8
        crev = _math(nt, 'MULTIPLY', _math(nt, 'SUBTRACT', 1.0, ao.outputs['AO']), 0.55 * dirt)
        dm = _math(nt, 'MAXIMUM', dmask, crev)
        col = _mix(nt, dm, col, hexrgb('#5e4630'))
    nt.links.new(col, b.inputs['Base Color'])
    # roughness variado
    nrg = _noise(nt, 0.8, 3.0, 0.5, pos)
    rg = _math(nt, 'ADD', _math(nt, 'MULTIPLY', nrg.outputs['Fac'], 0.3), rough - 0.15)
    nt.links.new(rg, b.inputs['Roughness'])
    b.inputs['Metallic'].default_value = metal
    b.inputs['Specular'].default_value = 0.5
    # bump sutil de chapa
    bp = nt.nodes.new('ShaderNodeBump'); bp.inputs['Strength'].default_value = 0.08
    nb = _noise(nt, 2.5, 2.0, 0.5, pos)
    nt.links.new(nb.outputs['Fac'], bp.inputs['Height']); nt.links.new(bp.outputs['Normal'], b.inputs['Normal'])
    m.diffuse_color = base_c
    return m


def soil(name, base, pebble=0.6, tracks=False, scale=1.0, bump=0.6):
    """solo procedural: variação de cor, pedregulhos (voronoi), sulcos e marcas de esteira (opcional)."""
    if name in _PM:
        return _PM[name]
    m = bpy.data.materials.new(name); _PM[name] = m
    nt, b = _nodes(m)
    geo = nt.nodes.new('ShaderNodeNewGeometry'); pos = geo.outputs['Position']
    c = hexrgb(base)
    nv = _noise(nt, 0.05 * scale, 5.0, 0.6, pos)
    col = _ramp(nt, nv.outputs['Fac'], [(0.25, tuple(x * 0.78 for x in c[:3]) + (1,)), (0.5, c), (0.78, tuple(min(1, x * 1.18) for x in c[:3]) + (1,))]).outputs[0]
    vo = nt.nodes.new('ShaderNodeTexVoronoi'); vo.inputs['Scale'].default_value = 0.9 * scale; nt.links.new(pos, vo.inputs['Vector'])
    vo.feature = 'F1'
    peb = _ramp(nt, vo.outputs['Distance'], [(0.0, (1, 1, 1, 1)), (0.22, (0, 0, 0, 1))]).outputs[0]
    pm = _math(nt, 'MULTIPLY', peb, pebble)
    col = _mix(nt, pm, col, tuple(x * 0.62 for x in c[:3]) + (1,))
    hgt = _math(nt, 'ADD', _math(nt, 'MULTIPLY', nv.outputs['Fac'], 0.6), _math(nt, 'MULTIPLY', peb, 0.6 * pebble))
    if tracks:
        wv = nt.nodes.new('ShaderNodeTexWave'); wv.wave_type = 'BANDS'; wv.bands_direction = 'Y'
        wv.inputs['Scale'].default_value = 0.9; wv.inputs['Distortion'].default_value = 1.5
        nt.links.new(pos, wv.inputs['Vector'])
        tr = _ramp(nt, wv.outputs['Fac'], [(0.4, (0, 0, 0, 1)), (0.6, (1, 1, 1, 1))]).outputs[0]
        col = _mix(nt, _math(nt, 'MULTIPLY', tr, 0.25), col, tuple(x * 0.7 for x in c[:3]) + (1,))
        hgt = _math(nt, 'ADD', hgt, _math(nt, 'MULTIPLY', tr, 0.5))
    nt.links.new(col, b.inputs['Base Color'])
    b.inputs['Roughness'].default_value = 0.95; b.inputs['Specular'].default_value = 0.15
    bp = nt.nodes.new('ShaderNodeBump'); bp.inputs['Strength'].default_value = bump; bp.inputs['Distance'].default_value = 0.4
    nt.links.new(hgt, bp.inputs['Height']); nt.links.new(bp.outputs['Normal'], b.inputs['Normal'])
    m.diffuse_color = c
    return m


def simple(name, color, rough=0.5, metal=0.0, emit=None, es=0.0, alpha=1.0, spec=0.5):
    if name in _PM:
        return _PM[name]
    m = bpy.data.materials.new(name); _PM[name] = m
    nt, b = _nodes(m)
    b.inputs['Base Color'].default_value = hexrgb(color); b.inputs['Roughness'].default_value = rough
    b.inputs['Metallic'].default_value = metal; b.inputs['Specular'].default_value = spec
    if emit:
        b.inputs['Emission'].default_value = hexrgb(emit); b.inputs['Emission Strength'].default_value = es
    if alpha < 1:
        b.inputs['Alpha'].default_value = alpha; m.blend_method = 'BLEND'; m.shadow_method = 'NONE'
    m.diffuse_color = hexrgb(color)
    return m


# ================================================================== malhas compartilhadas (instâncias)
MESH = {}


def mesh_from_bm(key, build, mats):
    if key in MESH:
        return MESH[key]
    me = bpy.data.meshes.new(key); bm = bmesh.new()
    build(bm)
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    bm.to_mesh(me); bm.free()
    for m in mats:
        me.materials.append(m)
    MESH[key] = me
    return me


def _cube(bm, size, off=(0, 0, 0), mat=0):
    r = bmesh.ops.create_cube(bm, size=1.0)
    vs = r['verts']
    bmesh.ops.scale(bm, vec=size, verts=vs)
    bmesh.ops.translate(bm, vec=off, verts=vs)
    for f in {f for v in vs for f in v.link_faces}:
        f.material_index = mat
    return vs


def bevel_box_mesh(key, size, m, bevel=0.06, segs=2):
    """caixa com arestas chanfradas de verdade (geometria, não modificador) — boa para instanciar."""
    def b(bm):
        vs = _cube(bm, size)
        bmesh.ops.bevel(bm, geom=list({e for v in vs for e in v.link_edges}) + vs, offset=bevel, segments=segs, affect='EDGES', profile=0.5)
    return mesh_from_bm(key, b, [m])


def angle_mesh(key, m, leg=0.6, t=0.09):
    """cantoneira (perfil L) de comprimento 1 em X, para escalar só em X."""
    def b(bm):
        _cube(bm, (1, leg, t), (0, 0, -leg / 2 + t / 2))
        _cube(bm, (1, t, leg), (0, -leg / 2 + t / 2, 0))
    return mesh_from_bm(key, b, [m])


def cyl_mesh(key, m, r=1.0, depth=1.0, n=32, axis='X', bevel=0.0):
    def b(bm):
        res = bmesh.ops.create_cone(bm, cap_ends=True, cap_tris=False, segments=n, radius1=r, radius2=r, depth=depth)
        vs = res['verts']
        if bevel:
            ed = [e for e in bm.edges if len(e.link_faces) == 2 and abs(e.calc_face_angle(0)) > 0.9]
            bmesh.ops.bevel(bm, geom=ed, offset=bevel, segments=2, affect='EDGES', profile=0.5)
        if axis == 'X':
            bmesh.ops.rotate(bm, verts=bm.verts, cent=(0, 0, 0), matrix=Matrix.Rotation(math.pi / 2, 3, 'Y'))
        elif axis == 'Y':
            bmesh.ops.rotate(bm, verts=bm.verts, cent=(0, 0, 0), matrix=Matrix.Rotation(math.pi / 2, 3, 'X'))
    return mesh_from_bm(key, b, [m])


def inst(me, loc, rot=(0, 0, 0), scale=(1, 1, 1), parent=None, name='i'):
    ob = link(bpy.data.objects.new(name, me))
    ob.location = loc; ob.rotation_euler = rot; ob.scale = scale
    if parent:
        ob.parent = parent
    return ob


def frame_between(p0, p1, parent=None, name='Quadro'):
    p0, p1 = Vector(p0), Vector(p1)
    d = p1 - p0
    e = empty(name, tuple(p0), parent)
    e.rotation_euler = d.to_track_quat('X', 'Z').to_euler()
    return e, d.length


# ================================================================== treliça com cantoneiras e chapas de ligação
def truss(p0, p1, w_, h_, nseg, m, leg=0.7, parent=None, name='Trelica', gusset_m=None, bolt_me=None):
    e, L = frame_between(p0, p1, parent, name)
    ch = angle_mesh('ang_ch_' + m.name + str(leg), m, leg, leg * 0.14)
    dg = angle_mesh('ang_dg_' + m.name + str(leg), m, leg * 0.6, leg * 0.1)
    for sy in (-1, 1):
        for sz in (-1, 1):
            o = inst(ch, (L / 2, sy * w_ / 2, sz * h_ / 2), (0, 0, 0), (L, 1, 1), e, name + 'Banzo')
            o.rotation_euler.x = {(1, 1): math.pi, (1, -1): math.pi / 2, (-1, 1): -math.pi / 2, (-1, -1): 0}[(sy, sz)]
    step = L / nseg
    gus = gusset_m and bevel_box_mesh('gusset_' + gusset_m.name, (leg * 2.6, 0.08, leg * 2.0), gusset_m, 0.03, 1)
    for i in range(nseg + 1):
        x = i * step
        for sz in (-1, 1):
            inst(dg, (x, 0, sz * h_ / 2), (0, 0, math.pi / 2), (w_, 1, 1), e, name + 'Trav')
        for sy in (-1, 1):
            inst(dg, (x, sy * w_ / 2, 0), (0, math.pi / 2, 0), (h_, 1, 1), e, name + 'Mont')
            if gus:
                for sz in (-1, 1):
                    inst(gus, (x, sy * (w_ / 2 + 0.05), sz * (h_ / 2 - leg)), parent=e, name=name + 'Chapa')
        if i < nseg:
            for sy in (-1, 1):
                a = math.atan2(h_, step) * (1 if i % 2 else -1)
                inst(dg, (x + step / 2, sy * w_ / 2, 0), (0, a, 0), (math.hypot(step, h_), 1, 1), e, name + 'Diag')
            for sz in (-1, 1):
                a = math.atan2(w_, step) * (1 if i % 2 else -1)
                inst(dg, (x + step / 2, 0, sz * h_ / 2), (0, 0, a), (math.hypot(step, w_), 1, 1), e, name + 'DiagH')
    return e, L


# ================================================================== passarelas, guarda-corpos, escadas
def walkway(p0, p1, parent, M, floor_w=1.4, h=1.1, gap=1.8):
    e, L = frame_between(p0, p1, parent, 'Passarela')
    grade = M['grating']; am = M['rail']
    fl = bevel_box_mesh('pass_floor', (1, 1, 1), grade, 0.0, 1)
    rl = cyl_mesh('rail_tube', am, 1.0, 1.0, 10, 'X')
    post = cyl_mesh('rail_post', am, 1.0, 1.0, 8, 'Z')
    kick = bevel_box_mesh('kick', (1, 1, 1), am, 0.0, 1)
    inst(fl, (L / 2, 0, 0), scale=(L, floor_w, 0.1), parent=e, name='PassPiso')
    for sy in (-1, 1):
        y = sy * floor_w / 2
        inst(rl, (L / 2, y, h), scale=(L, 0.05, 0.05), parent=e, name='Corrimao')
        inst(rl, (L / 2, y, h * 0.55), scale=(L, 0.035, 0.035), parent=e, name='CorrimaoMeio')
        inst(kick, (L / 2, y, 0.12), scale=(L, 0.03, 0.18), parent=e, name='Rodape')
        n = max(2, int(L / gap))
        for i in range(n + 1):
            inst(post, (i * L / n, y, h / 2), scale=(0.04, 0.04, h), parent=e, name='Poste')
    return e


def stairs(base, height, parent, M, flights=None, w_=1.2, along='X'):
    flights = flights or max(2, int(height / 3.6))
    fh = height / flights
    step_me = bevel_box_mesh('degrau', (0.32, w_, 0.06), M['grating'], 0.0, 1)
    strg = bevel_box_mesh('longarina', (1, 0.08, 0.3), M['rail'], 0.0, 1)
    rl = cyl_mesh('rail_tube', M['rail'], 1.0, 1.0, 10, 'X')
    land = bevel_box_mesh('patamar', (1.8, w_ + 0.3, 0.1), M['grating'], 0.0, 1)
    for i in range(flights):
        z0 = base.z + i * fh
        sx = 1 if i % 2 == 0 else -1
        p0 = Vector((base.x - sx * 2.4, base.y, z0)); p1 = Vector((base.x + sx * 2.4, base.y, z0 + fh))
        e, L = frame_between(p0, p1, parent, 'Lance')
        nst = int(L / 0.3)
        for j in range(nst):
            st = inst(step_me, (j * L / nst, 0, 0), parent=e, name='Degrau')
            st.rotation_euler.y = math.atan2(fh, 4.8)  # degraus nivelados
        for sy in (-1, 1):
            inst(strg, (L / 2, sy * w_ / 2, 0), scale=(L, 1, 1), parent=e, name='Longarina')
            inst(rl, (L / 2, sy * w_ / 2, 1.0), scale=(L, 0.045, 0.045), parent=e, name='CorrEsc')
        inst(land, tuple(p1) if False else (L, 0, 0), parent=e, name='Patamar')


# ================================================================== caçamba (formato real), dentes e corrente
def bucket_mesh(M):
    """caçamba: costas curvas + fundo arredondado + laterais trapezoidais + lábio grosso. Boca para +X."""
    def b(bm):
        Lx, W, H = 3.8, 3.2, 2.8
        prof = []  # perfil lateral (x, z): costas -> fundo curvo -> boca
        for i in range(10):
            a = math.pi * 0.5 + math.pi * 0.5 * i / 9  # 90..180 graus
            prof.append((-Lx / 2 + 1.4 + 1.4 * math.cos(a), -H / 2 + 1.4 + 1.4 * math.sin(a) - 1.4))
        prof = [(-Lx / 2, H / 2)] + [(x, z) for x, z in prof[::-1]] + [(Lx / 2 - 0.2, -H / 2 + 0.1), (Lx / 2, -H / 2 + 0.55)]
        rows = []
        for sy in (-W / 2, W / 2):
            rows.append([bm.verts.new((x, sy, z)) for x, z in prof])
        for i in range(len(prof) - 1):
            bm.faces.new((rows[0][i], rows[0][i + 1], rows[1][i + 1], rows[1][i]))
        for r in rows:
            bm.faces.new(r)
        bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
        # espessura (casca) — feita com solidify no objeto
    me = mesh_from_bm('cacamba_v2', b, [M['bucket']])
    return me


def tooth_meshes(M):
    adp = bevel_box_mesh('dente_adapt', (0.55, 0.32, 0.42), M['steel_dark'], 0.05, 2)
    def tip(bm):
        res = bmesh.ops.create_cone(bm, cap_ends=True, segments=6, radius1=0.17, radius2=0.03, depth=0.65)
        bmesh.ops.rotate(bm, verts=bm.verts, cent=(0, 0, 0), matrix=Matrix.Rotation(-math.pi / 2, 3, 'Y'))
        bmesh.ops.translate(bm, vec=(0.55, 0, 0), verts=bm.verts)
    tp = mesh_from_bm('dente_ponta', tip, [M['tooth']])
    def link_b(bm):
        bmesh.ops.create_circle(bm, cap_ends=False, segments=8, radius=0.16)
    lk = MESH.get('elo')
    if lk is None:
        o = bpy.ops.mesh.primitive_torus_add(major_segments=10, minor_segments=5, major_radius=0.17, minor_radius=0.05)
        ob = bpy.context.object; ob.scale = (1.5, 1, 1); bpy.ops.object.transform_apply(scale=True)
        ob.data.materials.append(M['chain']); MESH['elo'] = ob.data; bpy.data.objects.remove(ob); lk = MESH['elo']
    return adp, tp, lk


# ================================================================== esteira com sapatas individuais
def crawler(loc, parent, M, L=14.5, W=3.8, H=3.6, nshoe=None):
    g = empty('Esteira', loc, parent)
    shoe = MESH.get('sapata')
    if shoe is None:
        def b(bm):
            _cube(bm, (1.0, W, 0.28), (0, 0, 0))
            _cube(bm, (0.16, W * 0.96, 0.22), (0.25, 0, -0.2))   # garra
            _cube(bm, (0.5, W * 0.3, 0.12), (0, 0, 0.18))        # guia
        shoe = mesh_from_bm('sapata', b, [M['track']])
    R = H / 2 - 0.2
    straight = L - 2 * R
    per = 2 * straight + 2 * math.pi * R
    n = nshoe or int(per / 1.02)
    for i in range(n):
        s = per * i / n
        if s < straight:
            x, z, a = -straight / 2 + s, -R, 0.0
        elif s < straight + math.pi * R:
            t = (s - straight) / R
            x, z, a = straight / 2 + R * math.sin(t), -R * math.cos(t), -t
        elif s < 2 * straight + math.pi * R:
            x, z, a = straight / 2 - (s - straight - math.pi * R), R, -math.pi
        else:
            t = (s - 2 * straight - math.pi * R) / R
            x, z, a = -straight / 2 - R * math.sin(t), R * math.cos(t), -math.pi - t
        inst(shoe, (x, 0, z + H / 2), (0, a, 0), parent=g, name='Sapata')
    # quadro, roda motriz dentada, roda guia, roletes inferiores e superiores
    fr = bevel_box_mesh('est_quadro', (straight + 0.6, W * 0.62, H * 0.5), M['frame'], 0.12, 2)
    inst(fr, (0, 0, H / 2), parent=g, name='EstQuadro')
    drum = cyl_mesh('est_roda', M['steel_dark'], R - 0.25, W * 0.7, 32, 'Y', 0.06)
    inst(drum, (straight / 2, 0, H / 2), parent=g, name='RodaMotriz')
    inst(drum, (-straight / 2, 0, H / 2), parent=g, name='RodaGuia')
    tooth = bevel_box_mesh('est_dente', (0.34, W * 0.5, 0.34), M['steel_dark'], 0.04, 1)
    for k in range(14):
        a = k * 2 * math.pi / 14
        inst(tooth, (straight / 2 + (R - 0.12) * math.cos(a), 0, H / 2 + (R - 0.12) * math.sin(a)), (0, -a, 0), parent=g, name='DenteMotriz')
    rl = cyl_mesh('est_rolete', M['steel'], 0.42, W * 0.55, 20, 'Y', 0.04)
    for k in range(6):
        inst(rl, (-straight / 2 + 0.9 + k * (straight - 1.8) / 5, 0, H / 2 - R + 0.55), parent=g, name='RoleteInf')
    for k in range(3):
        inst(rl, (-straight / 2 + 1.6 + k * (straight - 3.2) / 2, 0, H / 2 + R - 0.5), (0, 0, 0), (0.7, 1, 0.7), g, 'RoleteSup')
    mot = cyl_mesh('est_motor', M['motor'], 0.55, 1.3, 24, 'Y', 0.04)
    inst(mot, (straight / 2 - 1.4, W * 0.55, H / 2 + 0.3), parent=g, name='MotorEsteira')
    return g


# ================================================================== correia em calha (troughed belt) com roletes
def troughed_belt(p0, p1, parent, M, width=3.0, gap=1.6, chunks=True, rnd=None):
    rnd = rnd or random
    e, L = frame_between(p0, p1, parent, 'Correia')
    side = width * 0.32
    belt = mesh_from_bm('correia_calha', lambda bm: (
        _cube(bm, (1, width * 0.38, 0.06), (0, 0, 0)),
        [bmesh.ops.rotate(bm, verts=_cube(bm, (1, side, 0.06), (0, sy * (width * 0.19 + side * 0.43), side * 0.25)), cent=(0, sy * (width * 0.19 + side * 0.43), side * 0.25),
                          matrix=Matrix.Rotation(sy * math.radians(30), 3, 'X')) for sy in (-1, 1)]), [M['belt']])
    inst(belt, (L / 2, 0, 0.3), scale=(L, 1, 1), parent=e, name='CorreiaLona')
    roll = cyl_mesh('rolete_c', M['steel'], 0.13, 1.0, 16, 'Y')
    stand = bevel_box_mesh('rolete_cav', (0.12, width + 0.5, 0.12), M['frame'], 0.02, 1)
    for i in range(int(L / gap)):
        x = i * gap
        inst(roll, (x, 0, 0.18), scale=(1, width * 0.38, 1), parent=e, name='RoleteC')
        for sy in (-1, 1):
            inst(roll, (x, sy * (width * 0.19 + side * 0.43), 0.18 + side * 0.25), (sy * math.radians(30), 0, 0), (1, side, 1), e, 'RoleteL')
        inst(stand, (x, 0, 0.02), parent=e, name='Cavalete')
        if i % 3 == 0:
            inst(roll, (x, 0, -0.45), scale=(1, width, 1), parent=e, name='RoleteRetorno')
    drum = cyl_mesh('tambor', M['steel_dark'], 0.55, width + 0.3, 32, 'Y', 0.04)
    inst(drum, (0, 0, 0.0), parent=e, name='Tambor')
    inst(drum, (L, 0, 0.0), parent=e, name='Tambor')
    out = []
    if chunks:
        rock = MESH.get('rocha0')
        for i in range(int(L / 1.4)):
            c = inst(rock, (i * 1.4 + rnd.uniform(-0.4, 0.4), rnd.uniform(-0.5, 0.5), 0.55), (rnd.uniform(0, 6), rnd.uniform(0, 6), rnd.uniform(0, 6)),
                     (rnd.uniform(0.35, 0.7),) * 3, e, 'TerraCorreia')
            out.append(c)
    return e, L, out


# ================================================================== pedras (variações) e dispersão
def rock_meshes(M, n=6, seed=3):
    rnd = random.Random(seed)
    for k in range(n):
        if f'rocha{k}' in MESH:
            continue
        bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=2, radius=1.0)
        ob = bpy.context.object
        for v in ob.data.vertices:
            v.co *= rnd.uniform(0.75, 1.15)
            v.co.z *= rnd.uniform(0.55, 0.85)
        ob.data.materials.append(M['rock'] if k % 2 else M['rock2'])
        MESH[f'rocha{k}'] = ob.data; bpy.data.objects.remove(ob)
    return [MESH[f'rocha{k}'] for k in range(n)]


def scatter_rocks(rect, z, count, smin, smax, parent=None, rnd=None, zfn=None):
    rnd = rnd or random
    rocks = [MESH[f'rocha{k}'] for k in range(6)]
    x0, x1, y0, y1 = rect
    for i in range(count):
        x, y = rnd.uniform(x0, x1), rnd.uniform(y0, y1)
        s = smin * (smax / smin) ** (rnd.random() ** 2.2)
        zz = zfn(x, y) if zfn else z
        inst(rocks[i % 6], (x, y, zz + s * 0.15), (rnd.uniform(0, 6), rnd.uniform(0, 6), rnd.uniform(0, 6)), (s, s, s), parent, 'Pedra')


def relief(ob, strength=1.5, size=8.0, levels=4, seed=0):
    """relevo: subdivide (simples) e desloca com textura de nuvens."""
    sd = ob.modifiers.new('Sub', 'SUBSURF'); sd.subdivision_type = 'SIMPLE'; sd.levels = levels; sd.render_levels = levels
    tx = bpy.data.textures.new(f'Relevo{seed}', 'CLOUDS'); tx.noise_scale = size; tx.noise_depth = 3
    dp = ob.modifiers.new('Relevo', 'DISPLACE'); dp.texture = tx; dp.strength = strength; dp.mid_level = 0.5
    dp.texture_coords = 'GLOBAL'
    return ob
