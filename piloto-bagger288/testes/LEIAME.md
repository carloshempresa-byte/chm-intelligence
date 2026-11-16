# Bagger 288: quadros de teste do novo padrão visual

São quadros parados para aprovação do Carlos **antes** do render completo. Ainda não há voz nem animação final.

| Quadro | Cena do roteiro | Tempo de render (1080x1920, 16 amostras, motion blur) |
|---|---|---|
| `01_gancho_engole_montanhas.png` | 0, gancho: a roda mordendo a "montanha" em camadas, golden hour, poeira | 13,6 s |
| `02_roda_cavando_close.png` | 7: close na roda de 21,6 m com 18 caçambas e dentes, partículas e motion blur | 16,1 s |
| `03_escala_dois_cristos.png` | 2: 96 m × dois Cristos (76 m), com régua de 96 m | 9,4 s |
| `04_drone_dois_campos.png` | 3: drone de cima, 225 m × dois campos de futebol | 12,3 s |
| `05_esteiras_camera_baixa.png` | 11: câmera baixa nas esteiras com o Eng. Carlin para escala | 12,4 s |
| `06_mudanca_rodovia.png` | 15: mudança de 2001 atravessando a rodovia (carros parados, pessoas, caminho preparado) | 10,0 s |

`com_texto/` tem os mesmos quadros com os textos grandes do estilo final (títulos, pílulas e legenda). `folha_de_contato.jpg` junta todos.

**Estimativa do render completo** (~2 min = ~3.600 quadros): média de ~12 s por quadro (9–16 s), ou seja, **~12 h** (faixa de 9,5–16 h). Roda em blocos de 2 h, retomável, nesta mesma máquina e sem custo extra.

**Como gerar de novo:**
```bash
blender -b --factory-startup -P scripts/cena_bagger_testes.py -- testes 16 1.0
python3 scripts/textos_teste.py testes
```
