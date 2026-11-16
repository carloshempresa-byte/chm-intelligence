"""Gera cena_bagger_final_gerada.py = cena v2 (modelos/materiais/cenário dos testes aprovados) + animação final."""
import os
H = os.path.dirname(os.path.abspath(__file__))
v2 = open(os.path.join(H, 'cena_bagger_v2.py'), encoding='utf-8').read()
cut = v2.index('# ================================================================== animação (motion blur e partículas)')
fin = open(os.path.join(H, 'final_animacao.py'), encoding='utf-8').read()
open(os.path.join(H, 'cena_bagger_final_gerada.py'), 'w', encoding='utf-8').write(v2[:cut] + fin)
print('ok')
