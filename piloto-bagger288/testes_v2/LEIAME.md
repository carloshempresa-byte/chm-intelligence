# Bagger 288: quadros de teste, rodada 2 (salto de detalhe)

São os mesmos 6 quadros da rodada 1, refeitos com o pedido do Carlos. Sem voz e sem render completo.

## O que mudou
- **Geometria**
  - Treliças de **cantoneiras** (perfil L) com **chapas de ligação**.
  - **Bevel** real nas peças; peças redondas com 32–128 segmentos.
  - **Caçambas com formato de caçamba** (costas curvas, fundo arredondado, lábio), **5 dentes** com adaptador e **corrente**.
  - **Esteiras** com sapatas individuais com garra, **roda motriz dentada**, roda-guia, roletes de baixo e de cima e motor.
  - **Correias em calha** com 3 roletes por cavalete, roletes de retorno e tambores.
  - **Motores e redutores** com aletas, **painéis elétricos** com portas e puxadores, **polias** (moitão no topo e nas pontas) e cabos em 4 pernas.
  - Escada com **degraus individuais**, longarinas e corrimão; passarelas com piso de grade, corrimão, travessa e rodapé.
  - **Cabine** com colunas, vidro, banco, console e telas acesas; **faróis** com suporte.
  - **Parafusos** em anéis (giro e cubo da roda), nervuras de reforço, ventiladores no telhado.
- **Materiais procedurais**
  - Tinta com **variação de tom**, **ferrugem** em manchas e **sujeira de terra** subindo de baixo e nas frestas (AO).
  - **Roughness variado** e bump de chapa.
  - Solo com **pedregulhos** (voronoi), sulcos e **marcas de esteira**; rocha com bump forte; asfalto com textura.
- **Cenário**
  - Piso das bancadas com **relevo**; frente de lavra e degraus com **cortes irregulares** (deslocamento).
  - **Morros** com árvores atrás da frente de lavra.
  - Mais de mil **pedras** espalhadas e **pilha de entulho** na mordida da roda.
  - Mais de mil árvores (2 tipos) ao longe; lavouras; torres de energia.
  - **Céu com nuvens procedurais**, **névoa volumétrica** leve + névoa distante.
- **Luz**
  - Golden hour com mais contraste, **sombras de contato** e **luz de borda (contraluz)** em cada plano.
  - EEVEE com AO (bent normals + bounce), **SSR**, sombras suaves de alta resolução, **bloom**, **volumetria**, motion blur e vinheta leve.
- **Composição**
  - Quadro 3: **dois Cristos grandes e empilhados**, ao lado da máquina, com lente longa (sem distorção de perspectiva), régua de 96 m e sem metade de céu vazio.
  - Quadro 1: montanha com textura, morro ao fundo e chão com entulho e pedras.

## Tempo por quadro (1080x1920, EEVEE, 24 amostras, volumetria + SSR + AO + motion blur)

| Quadro | Tempo |
|---|---|
| 01 gancho | 90,8 s |
| 02 roda (close) | 90,7 s |
| 03 dois Cristos | 52,1 s |
| 04 drone/campos | 61,1 s |
| 05 esteiras/Carlin | 63,7 s |
| 06 rodovia | 36,6 s |

Média: **~66 s por quadro**.

## Cycles com denoise (teste)
`extra_cycles_05_meia_resolucao.png` é o quadro 05 em **Cycles**, com 32 amostras e denoise OpenImageDenoise, em **meia resolução**. Levou 47 s, o que dá **~3 min por quadro** em 1080x1920 nesta máquina (4 CPUs, sem GPU). A luz fica visivelmente mais bonita (iluminação global), mas o vídeo inteiro levaria **~180 h**, o que não é viável aqui. Comparação lado a lado: `comparacao_v1_v2_cycles.jpg` (v1 · v2 EEVEE · Cycles).

## Estimativa do render completo (~2 min ≈ 3.600 quadros)
| Opção | Tempo por quadro | Total |
|---|---|---|
| EEVEE exatamente como estes testes | ~66 s | **~66 h** |
| EEVEE otimizado (12 amostras, volumetria mais leve, sombras 2048; quase igual a olho nu) | ~25–35 s (a medir) | **~25–35 h** |
| Cycles + denoise | ~3 min | **~180 h** (inviável nesta máquina) |

Todas rodam em blocos de 2 h, retomáveis, nesta máquina e sem custo extra.

## Gerar de novo
```bash
blender -b --factory-startup -P scripts/cena_bagger_v2.py -- testes_v2 24 1.0 EEVEE
python3 scripts/textos_teste.py testes_v2
```
