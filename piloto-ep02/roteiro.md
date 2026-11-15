# Como montar a maior caldeira de recuperação do mundo
## Episódio 2: "O drum"

**Canal:** Engenharia Animada
**Formato:** Short vertical 9:16, 1080x1920, 30 fps, com o mesmo estilo e pipeline do EP01:
- animação 3D low-poly, cores chapadas, sombra suave e câmera em movimento
- mascote **Eng. Carlin**, com o nome na faixa do capacete
- narração masculina PT-BR rápida e sem silêncio
- legendas palavra a palavra
- etiquetas em pílula apontando as peças

**Duração estimada:** ~66–70 s de narração. São 213 palavras, mais os números falados por extenso. Se o TTS passar de 70 s, corto antes de renderizar.
**Voz:** edge-tts `pt-BR-AntonioNeural`, +20%, pausas cortadas para ≤ 0,22 s.

**Revisão 2:** já inclui as respostas do Carlos (lista abaixo).

### Dados confirmados pelo Carlos
| Dado | Valor / resposta |
|---|---|
| O que é o drum | Balão de vapor da caldeira. O termo usado é **"drum"**. "Onde a água e o vapor se separam" pode ficar. |
| Peso do drum | **320 t** |
| Altura de içamento | **75 m** (comparação "prédio de 25 andares" aprovada) |
| Guindastes | **2 guindastes de 700 t cada**, marca **Liebherr** |
| Por que 2 guindastes | Quanto mais alto se iça a carga, menor fica a capacidade do guindaste |
| Como foi içado | **Na horizontal**, **um guindaste em cada ponta**, com **cabos de aço da grossura de uma perna** |
| Planejamento do içamento | **5 meses** |
| Transporte | **Do porto até a obra, 2 meses, pela estrada, num caminhão especial** |
| Entrada na estrutura | **Por cima, antes de fechar o teto** |

Ainda sem resposta (no texto ficam genéricos ou fora): sinaleiro/rádio, forma de fixação final e o termo "tandem". Ver a lista no fim.

---

## Narração completa (texto para o TTS)

> 5 meses de planejamento e 2 meses de estrada, tudo pra levantar uma peça só: 320 toneladas, a 75 metros de altura. Essa peça é o drum, o balão de vapor da caldeira de recuperação: o cilindro gigante lá no topo, onde a água e o vapor se separam. 75 metros é um prédio de 25 andares. Só pra chegar do porto até a obra, foram 2 meses de estrada, num caminhão especial. Aí você chama um guindaste de 700 toneladas. Resolvido? Não. Quanto mais alto você iça a carga, menor fica a capacidade do guindaste, e lá em cima um só não dá conta. Então você usa dois guindastes de 700 toneladas, um em cada ponta, com o drum na horizontal, pendurado em cabos de aço da grossura de uma perna. Mas se um guindaste sobe mais rápido que o outro, o drum inclina e o peso vai todo pra um lado. Não dá pra improvisar: foram 5 meses planejando esse içamento. No dia, os dois sobem juntos, bem devagar, comandados por um sinaleiro. E lá em cima o teto ainda está aberto: o drum entra por cima, desce até o lugar dele, e só depois o teto é fechado. Parabéns, você montou o drum. Se você sabia, comente Engenheiro. Se não sabia, comente Estagiário.

**O que mudou em relação à revisão 1**
- **Gancho:** passa a abrir com "5 meses de planejamento e 2 meses de estrada".
- **Drum:** fica "drum, o balão de vapor". Saiu "tubulão".
- **Novas frases:** o transporte, os guindastes içando na horizontal, um em cada ponta, com cabos da grossura de uma perna, e o teto aberto.
- **Termo "tandem":** saiu da narração, porque ainda não foi confirmado.
- **Sinaleiro:** ficou genérico ("comandados por um sinaleiro"); saiu "no rádio".
- **Fixação final:** ficou genérica ("desce até o lugar dele").

**Notas de produção da voz**
- **Números:** vou testar se o TTS lê "320 toneladas" como "trezentas e vinte". Se não ler, escrevo por extenso só no áudio e a legenda continua em algarismos (**320 TONELADAS**, **75 METROS**, **700 TONELADAS**, **5 MESES**, **2 MESES**).
- **"Drum":** vou conferir se o TTS pronuncia "drâm". Se não, uso grafia fonética só no áudio.

---

## Roteiro cena a cena (tempos aproximados, ajustados depois do TTS)

| # | Tempo | Narração | Visual / câmera | Etiquetas (pílulas) | SFX |
|---|---|---|---|---|---|
| 0 | 0,0–6,5 | "5 meses de planejamento e 2 meses de estrada, tudo pra levantar uma peça só: 320 toneladas, a 75 metros de altura." | **Gancho rápido, três batidas:** **(a)** um calendário low-poly folheia 5 páginas em segundos, com pranchetas e plantas voando; **(b)** um mapinha com o caminhão andando do porto até a obra; **(c)** corte para o drum no chão do pátio e a câmera sobe na vertical, seguindo uma trena amarela até o topo da estrutura. Lá de cima, olha para baixo: o Eng. Carlin minúsculo ao lado do drum leva susto e sua. Títulos do episódio no topo por 3,5 s. | EP. 2 · O DRUM · **5 MESES** · **2 MESES** · **320 t** · **75 m** | folhas de calendário, whoosh, buzina, whoosh subindo, boing |
| 1 | 6,5–12,5 | "Essa peça é o drum, o balão de vapor da caldeira de recuperação: o cilindro gigante lá no topo, onde a água e o vapor se separam." | A caldeira estilizada do EP01, com a estrutura aberta no topo. O "fantasma" translúcido do drum aparece no lugar dele, lá em cima. Close em corte esquemático: dentro do drum, a metade de baixo azul (água) e bolhas subindo para a metade de cima branca (vapor). | DRUM = BALÃO DE VAPOR · ÁGUA · VAPOR | pop, bolhas |
| 2 | 12,5–15,0 | "75 metros é um prédio de 25 andares." | Um prediozinho low-poly cresce andar por andar ao lado da caldeira até a mesma altura. O Carlin olha pra cima, boquiaberto. | 75 m = 25 ANDARES | "tic" a cada andar, whoosh |
| 3 | 15,0–19,5 | "Só pra chegar do porto até a obra, foram 2 meses de estrada, num caminhão especial." | Estrada low-poly (como a do EP01): caminhão especial com prancha comprida levando o drum, que ocupa a pista inteira. Placas passando ("PORTO", "OBRA"), dia e noite alternando rápido (sol e lua girando) para mostrar o tempo. O Carlin vai sentado na cabine. | **2 MESES** · CAMINHÃO ESPECIAL | caminhão acelerando, buzina, "tic-tac" |
| 4 | 19,5–22,5 | "Aí você chama um guindaste de 700 toneladas. Resolvido? Não." | Um guindaste de esteiras com lança treliçada amarela entra no quadro e para com um quique. **LIEBHERR** está escrito na casa de máquinas (só o nome em texto simples, sem reproduzir o logotipo). No "Resolvido?" o Carlin faz joinha; no "Não." a música corta e aparece um X vermelho. | GUINDASTE **700 t** · LIEBHERR | motor, clang, "fail" |
| 5 | 22,5–28,0 | "Quanto mais alto você iça a carga, menor fica a capacidade do guindaste, e lá em cima um só não dá conta." | A carga sobe e uma barra de capacidade ao lado do guindaste vai do verde (embaixo) ao vermelho (no alto), sem números. O guindaste range e as esteiras de trás levantam um pouco (exagero didático). O Carlin, apavorado, segura a esteira. | + ALTURA = – CAPACIDADE · UM SÓ NÃO DÁ | rangido metálico, bipes de alarme |
| 6 | 28,0–34,5 | "Então você usa dois guindastes de 700 toneladas, um em cada ponta, com o drum na horizontal, pendurado em cabos de aço da grossura de uma perna." | O segundo guindaste LIEBHERR entra espelhado. Plano aberto: um guindaste em cada ponta e o drum na horizontal, saindo do chão. **Close no cabo de aço ao lado da perna do Carlin**: mesma grossura. O Carlin compara, aponta e arregala os olhos. | 2 × **700 t** · NA HORIZONTAL · CABO = UMA PERNA | motor ×2, clang, boing |
| 7 | 34,5–39,5 | "Mas se um guindaste sobe mais rápido que o outro, o drum inclina e o peso vai todo pra um lado." | Simulação do erro (exagerada): o gancho da esquerda sobe rápido, o drum inclina, e uma seta vermelha de peso escorrega para o lado do outro guindaste, que range e balança. O Carlin cobre os olhos e sua. | DESNÍVEL · SOBRECARGA | rangido, "fail", boing |
| 8 | 39,5–43,5 | "Não dá pra improvisar: foram 5 meses planejando esse içamento." | Rebobina (efeito rewind rápido) e o drum volta ao chão, nivelado. Mesa com plantas, prancheta e o calendário de novo, agora folheando os 5 meses até um carimbo "APROVADO". O Carlin de óculos estudando a planta. | **5 MESES** · PLANO DE IÇAMENTO | rewind, papel, carimbo, "ding" |
| 9 | 43,5–48,0 | "No dia, os dois sobem juntos, bem devagar, comandados por um sinaleiro." | Os dois ganchos sobem em sincronia; as barras de capacidade dos dois ficam iguais e verdes. O Carlin é o sinaleiro, com o gesto de braço do EP01. **Sem rádio na mão até o Carlos confirmar.** | JUNTOS E DEVAGAR · SINALEIRO | motor ×2 (baixo, constante), apito curto |
| 10 | 48,0–55,5 | "E lá em cima o teto ainda está aberto: o drum entra por cima, desce até o lugar dele, e só depois o teto é fechado." | Câmera alta olhando para baixo: o topo da estrutura ainda **sem teto**. Uma trena com contador sobe até 75 m enquanto o drum chega. Ele passa por cima, desce no vão e assenta no lugar de forma genérica (baque e poeira, sem mostrar o tipo de fixação). As lingas afrouxam e saem. As vigas e chapas do teto caem no lugar uma a uma, fechando tudo. | TETO ABERTO · **75 m** · NO LUGAR! · TETO FECHADO | contador "tic-tic", baque grave, clangs em sequência |
| 11 | 55,5–58,0 | "Parabéns, você montou o drum." | Chuva de confete. O Carlin pula e comemora. Câmera orbitando o topo da caldeira, com os dois guindastes ao fundo. | PARABÉNS! · DRUM MONTADO | torcida, sino |
| 12 | 58,0–~68 | "Se você sabia, comente Engenheiro. Se não sabia, comente Estagiário." | A órbita continua e o Carlin comemora. CTA em pílulas grandes no topo, igual ao EP01. | SABIA? COMENTE **ENGENHEIRO** · NÃO SABIA? COMENTE **ESTAGIÁRIO** | "win" ×2 |

**Trilha:** a mesma do EP01 ("Feeling Happy", Mixkit), bem baixa e com ducking. Pop automático em cada etiqueta.

### Produção (o que muda em relação ao EP01)
- **Novos elementos 3D:**
  - drum: cilindro com tampos arredondados, vermelho como no EP01, com corte esquemático água/vapor
  - calendário que folheia, mapinha porto→obra e trena/contador de altura
  - prediozinho de 25 andares
  - caminhão especial com prancha, reaproveitando a carreta do EP01
  - segundo guindaste espelhado com ganchos independentes
  - barras de capacidade sem números
  - cabo de aço grosso, para o close ao lado da perna do Carlin
  - estrutura do topo sem teto, com as peças do teto caindo no fim
- **Marca Liebherr:** só o nome em letras simples na casa de máquinas, sem logotipo, fonte ou desenho oficial da marca. Num canal monetizado, usar o nome do fabricante que aparece no equipamento real costuma ser aceitável. Reproduzir o logotipo exigiria autorização da Liebherr. Se preferir zero risco, tiro o nome.
- **Mascote:** o Carlin usa a faixa **"Eng. Carlin"** no capacete (função `helmet_band` da identidade visual).
- **Escala:** é estilizada. Para caber no vertical, a caldeira, os guindastes e o drum não ficam em escala real (como no EP01).

---

## Pontos que ainda faltam confirmar [CONFIRMAR COM CARLOS]

1. **Sinaleiro:** o içamento foi comandado por um sinaleiro? Por rádio? A narração diz só "comandados por um sinaleiro" e a animação não mostra rádio.
2. **Fixação final:** como o drum fica preso no lugar (suspenso, apoiado em selas ou outro)? A narração diz só "desce até o lugar dele" e a animação mostra só ele assentando, sem detalhe.
3. **Termo "tandem":** é o termo usado na obra? Por enquanto saiu da narração. Se o Carlos confirmar, pode voltar como etiqueta ("IÇAMENTO EM TANDEM").
4. **Desnível entre os guindastes:** a cena 7 mostra o drum inclinando e o peso indo todo para um lado. É uma simplificação didática, exagerada na animação. Ok usar? A frase "o planejamento levou 5 meses" vem logo depois. Confirmar que não fica parecendo que os 5 meses foram só por causa disso.
5. **Barra de capacidade "do verde ao vermelho" e esteiras levantando:** são exageros visuais para explicar o princípio, sem números. Ok?
6. **Caminhão especial:** a cena mostra uma prancha comprida (carreta do EP01). Ok genérico? (Sem número de eixos.)
7. **"Do porto até a obra" num mapinha:** o mapa é ilustrativo, sem cidades nem distância. Ok?
8. **Marca Liebherr no visual:** confirmar que pode aparecer o nome escrito (sem logotipo). Os guindastes do vídeo são genéricos e não reproduzem o modelo real.
9. **"Bem devagar":** é só expressão, sem velocidade no texto. Se o Carlos quiser, pode passar a duração real do içamento.
10. **"A maior caldeira de recuperação do mundo":** continua sem números além dos confirmados (320 t, 75 m, 2 × 700 t, 5 meses, 2 meses, 25 andares).
11. **Visual estilizado:** caldeira, estrutura, guindastes e canteiro não representam o layout real e não estão em escala. Ok para o canal?

## Próximo passo
Com o ok desta revisão, eu gero a voz e confiro a duração (meta de 60–70 s), amarro os tempos das cenas, monto `piloto-ep02/scripts/cena_ep02.py` (reaproveitando `lowpoly_lib.py`), renderizo e monto o vídeo final.
