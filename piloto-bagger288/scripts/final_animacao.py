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
