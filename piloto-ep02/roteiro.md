# Como montar a maior caldeira de recuperação do mundo
## Episódio 2: "O drum (tubulão)"

**Canal:** Engenharia Animada
**Formato:** Short vertical 9:16, 1080x1920, 30 fps, com o mesmo estilo e pipeline do EP01:
- animação 3D low-poly, cores chapadas, sombra suave e câmera em movimento
- mascote **Eng. Carlin**, com o nome na faixa do capacete
- narração masculina PT-BR rápida e sem silêncio
- legendas palavra a palavra
- etiquetas em pílula apontando as peças

**Duração estimada:** ~62–66 s de narração. Os tempos exatos saem do TTS, como no EP01.
**Voz:** edge-tts `pt-BR-AntonioNeural`, +20%, pausas cortadas para ≤ 0,22 s.

### Dados confirmados pelo Carlos (únicos números do vídeo)
| Dado | Valor |
|---|---|
| Peso do drum | **320 t** |
| Altura de içamento | **75 m** |
| Guindastes | **2 guindastes de 700 t cada** |

Qualquer outro número ou detalhe técnico abaixo está marcado **[CONFIRMAR COM CARLOS]**. A comparação "prédio de 25 andares" é uma conta minha (75 m ÷ ~3 m por andar) e também precisa de aprovação.

---

## Narração completa (texto para o TTS)

> Você precisa colocar uma peça de 320 toneladas a 75 metros de altura. Essa peça é o drum, o tubulão da caldeira de recuperação: um cilindro gigante lá no topo, onde a água e o vapor se separam. 75 metros é mais ou menos um prédio de 25 andares. Então você chama um guindaste de 700 toneladas. Resolvido? Não. Esses 700 são a capacidade com a lança curta e a carga pertinho. Quanto mais alto e mais longe, menos o guindaste aguenta. Então você chama dois guindastes de 700 toneladas, um em cada ponta do drum. Isso é um içamento em tandem. Mas aí, se um guindaste sobe mais rápido que o outro, o drum inclina e o peso vai todo pra um lado só. Então tudo segue um plano de içamento, e os dois sobem juntos, bem devagar, comandados por um sinaleiro no rádio. Mas lá em cima o drum precisa entrar certinho no meio da estrutura. Então ele sobe metro por metro, até os 75 metros, e encaixa no lugar dele. Parabéns, você montou o drum de uma caldeira de recuperação. Se você sabia, comente Engenheiro. Se não sabia, comente Estagiário.

(~205 palavras. No EP01, 213 palavras deram 66 s.)

**Notas de produção da voz**
- **Números:** vou testar se o TTS lê "320 toneladas" como "trezentas e vinte". Se ler errado ("trezentos"), escrevo por extenso no TTS e mantenho os algarismos na legenda (**320 TONELADAS**, **75 METROS**, **700 TONELADAS**).
- **"Drum":** vou conferir se o TTS pronuncia como na obra ("drâm"). Se não pronunciar, uso grafia fonética só no áudio.

---

## Roteiro cena a cena (tempos aproximados, ajustados depois do TTS)

| # | Tempo | Narração | Visual / câmera | Etiquetas (pílulas) | SFX |
|---|---|---|---|---|---|
| 0 | 0,0–4,5 | "Você precisa colocar uma peça de 320 toneladas a 75 metros de altura." | **Gancho já com problema:** o drum (cilindro vermelho com tampos arredondados, mesmo vermelho do EP01) está no chão do pátio. A câmera sobe na vertical, seguindo uma régua/trena amarela que cresce até o topo da estrutura da caldeira. Lá de cima, olha para baixo: o Eng. Carlin minúsculo ao lado do drum leva susto e sua. Títulos do episódio no topo por 3,5 s. | EP. 2 · O DRUM (TUBULÃO) · **320 t** · **75 m** | whoosh subindo, boing, pop |
| 1 | 4,5–10,5 | "Essa peça é o drum, o tubulão da caldeira de recuperação: um cilindro gigante lá no topo, onde a água e o vapor se separam." | Corte para a caldeira estilizada do EP01, com a estrutura aberta no topo. O "fantasma" translúcido do drum aparece no lugar dele, lá em cima. Close em corte esquemático: dentro do drum, a metade de baixo azul (água) e bolhas subindo para a metade de cima branca (vapor). **[CONFIRMAR COM CARLOS: essa explicação simplificada]** | DRUM (TUBULÃO) · ÁGUA · VAPOR | pop, bolhas |
| 2 | 10,5–13,5 | "75 metros é mais ou menos um prédio de 25 andares." | Um prediozinho low-poly cresce andar por andar ao lado da caldeira até a mesma altura. O Carlin olha pra cima, boquiaberto. **[CONFIRMAR COM CARLOS: comparação]** | 75 m ≈ 25 ANDARES | "tic" a cada andar, whoosh |
| 3 | 13,5–17,0 | "Então você chama um guindaste de 700 toneladas. Resolvido? Não." | Um guindaste de esteiras com lança treliçada amarela (o do EP01) entra no quadro e para com um quique. Plaquinha na lança. No "Resolvido?" o Carlin faz joinha; no "Não." a música corta e aparece um X vermelho. | GUINDASTE **700 t** | caminhão/motor, clang, "fail" |
| 4 | 17,0–24,0 | "Esses 700 são a capacidade com a lança curta e a carga pertinho. Quanto mais alto e mais longe, menos o guindaste aguenta." | Explicação visual sem números: a lança começa curta e quase vertical, com uma barra de capacidade cheia (verde). A lança se alonga e abaixa, a carga vai para longe e a barra esvazia até o vermelho. O guindaste range e as esteiras de trás levantam um pouco (exagero didático). O Carlin, apavorado, segura a esteira. **[CONFIRMAR COM CARLOS: princípio e se esse foi o motivo dos 2 guindastes]** | CAPACIDADE · LANÇA CURTA = MAIS · ALTO E LONGE = MENOS | rangido metálico, alarme curto (bipes) |
| 5 | 24,0–29,5 | "Então você chama dois guindastes de 700 toneladas, um em cada ponta do drum. Isso é um içamento em tandem." | Corte para o plano aberto: o segundo guindaste entra espelhado. Os dois ficam um de cada lado do drum, com lingas descendo até as pontas. O drum sai do chão alguns centímetros e fica nivelado. **[CONFIRMAR COM CARLOS: posição dos guindastes, pontos de pega e termo "tandem"]** | 2 × **700 t** · IÇAMENTO EM TANDEM | whoosh, motor ×2, clang |
| 6 | 29,5–35,5 | "Mas aí, se um guindaste sobe mais rápido que o outro, o drum inclina e o peso vai todo pra um lado só." | Simulação do erro (exagerada): o gancho da esquerda sobe rápido, o drum inclina, e uma seta vermelha de peso escorrega para o lado do outro guindaste, que range e balança. O Carlin cobre os olhos e sua. Barra de carga de cada guindaste: uma esvazia, a outra estoura no vermelho. | DESNÍVEL · SOBRECARGA | rangido, "fail", boing |
| 7 | 35,5–43,5 | "Então tudo segue um plano de içamento, e os dois sobem juntos, bem devagar, comandados por um sinaleiro no rádio." | Rebobina (efeito rewind rápido) e o drum volta nivelado. Uma prancheta "PLANO DE IÇAMENTO" pousa na tela com um check. O Carlin vira sinaleiro (gesto de braço do EP01, com rádio na mão). Os dois ganchos sobem em sincronia; ondinhas de rádio saem do Carlin para as duas cabines. As barras de carga ficam iguais e verdes. **[CONFIRMAR COM CARLOS: sinaleiro/rádio, plano de rigging, monitoramento de carga]** | PLANO DE IÇAMENTO · SINALEIRO · JUNTOS E DEVAGAR | papel, "ding", chiado de rádio, motor ×2 |
| 8 | 43,5–47,5 | "Mas lá em cima o drum precisa entrar certinho no meio da estrutura." | Câmera alta, olhando de cima para baixo: a abertura no topo da estrutura, com vigas por todos os lados. O drum subindo parece grande demais para o vão. O Carlin (miniatura lá embaixo) sua. **[CONFIRMAR COM CARLOS: o drum entra por cima, antes de fechar o topo? Por onde passa?]** | VÃO DA ESTRUTURA | suspense curto, rangido |
| 9 | 47,5–53,5 | "Então ele sobe metro por metro, até os 75 metros, e encaixa no lugar dele." | Plano herói lateral: a régua de altura conta subindo (contador de metros vai até 75) enquanto o drum sobe. Ele passa pelo vão com folga mínima, desce um pouquinho e assenta no lugar com um baque e poeira low-poly. As lingas afrouxam. **[CONFIRMAR COM CARLOS: como o drum é fixado/apoiado no topo]** | **75 m** · ENCAIXADO! | contador "tic-tic", baque grave + clang |
| 10 | 53,5–57,5 | "Parabéns, você montou o drum de uma caldeira de recuperação." | Chuva de confete. O Carlin pula e comemora. Câmera orbitando o topo da caldeira com o drum no lugar e os dois guindastes ao fundo. | PARABÉNS! · DRUM MONTADO | torcida, sino |
| 11 | 57,5–~63 | "Se você sabia, comente Engenheiro. Se não sabia, comente Estagiário." | A órbita continua e o Carlin comemora. CTA em pílulas grandes no topo, igual ao EP01. | SABIA? COMENTE **ENGENHEIRO** · NÃO SABIA? COMENTE **ESTAGIÁRIO** | "win" ×2 |

**Trilha:** a mesma do EP01 ("Feeling Happy", Mixkit), bem baixa e com ducking. Pop automático em cada etiqueta.

### O que muda em relação ao EP01 (produção)
- **Novos elementos 3D:**
  - drum: cilindro com tampos semiesféricos e corte esquemático água/vapor
  - régua/contador de altura e prediozinho de 25 andares
  - segundo guindaste espelhado, com ganchos independentes
  - barras de capacidade sobre cada guindaste
  - topo da estrutura com o vão
  - rádio na mão do Carlin
- **Mascote:** o mascote do vídeo passa a usar a faixa **"Eng. Carlin"** no capacete (função `helmet_band` da identidade visual). Ela é legível nos closes.
- **Escala:** é estilizada. Para caber num vídeo vertical, a caldeira, os guindastes e o drum não ficam em escala real (como no EP01).

---

## Pontos para o Carlos conferir [CONFIRMAR COM CARLOS]

1. **"Drum" e "tubulão":** qual termo a equipe usa na obra? A narração usa os dois ("o drum, o tubulão"). Confirmar também a pronúncia ("drâm").
2. **Função do drum, de forma simplificada:** "um cilindro gigante lá no topo, onde a água e o vapor se separam". Essa simplificação está ok?
3. **Posição:** o drum fica no topo da caldeira, dentro da estrutura? A cena mostra ele entrando pelo vão do topo.
4. **Fixação final:** como o drum fica no lugar? Suspenso por tirantes, apoiado em selas ou outro? A narração diz só "encaixa no lugar dele", e a animação mostra ele assentando, de forma genérica.
5. **Comparação "prédio de 25 andares":** 75 m ÷ ~3 m por andar. Pode usar?
6. **Por que 2 guindastes:** a explicação é que a capacidade de 700 t vale com a lança curta e a carga perto, e cai com altura e raio. Confirmar que esse foi o motivo real, e não só um dos motivos (disponibilidade, espaço no canteiro, equilíbrio da carga etc.).
7. **"700 t":** é a capacidade nominal de cada guindaste (o "nome" do guindaste)? Confirmar que a frase "esses 700 são a capacidade com a lança curta e a carga pertinho" está correta para os modelos usados.
8. **Tipo e configuração dos guindastes:** de esteiras, com lança treliçada? Usaram contrapeso extra ou superlift? A animação mostra o modelo genérico do EP01.
9. **Termo "içamento em tandem":** é o termo usado na obra?
10. **Pontos de pega:** um guindaste em cada ponta do drum? Como o drum é preso (olhais, munhões, viga de içamento/balancim, lingas)? Ele foi içado na horizontal?
11. **Risco de desnível:** a frase "se um sobe mais rápido, o peso vai todo pra um lado só" é uma simplificação didática (na animação é exagerada). Ok usar?
12. **Controle do içamento:** existe plano de içamento (rigging)? Sinaleiro comandando por rádio? Houve monitoramento de carga nos guindastes (indicador de momento de carga, célula de carga)? A narração cita só "plano de içamento" e "sinaleiro no rádio".
13. **"Bem devagar" e "metro por metro":** são só expressões. Se quiser, o Carlos pode passar a duração real do içamento.
14. **Sequência de montagem:** o drum entra por cima antes de fechar o topo da estrutura? A frase "precisa entrar certinho no meio da estrutura" está ok? Tinha alguma folga apertada que valha mostrar?
15. **Vento e clima:** não está na narração. Se o Carlos quiser, dá para incluir um problema→solução "e se ventar?", mas só com o critério real da obra.
16. **"A maior caldeira de recuperação do mundo":** continua sem números além dos três confirmados (320 t, 75 m, 2 × 700 t).
17. **Visual estilizado:** caldeira, estrutura, guindastes e canteiro não representam o layout real, e as proporções não são em escala. Ok para o canal?

---

## Próximo passo
Com o ok do Carlos (ou ajustes no texto), eu gero a voz, amarro os tempos das cenas na narração, monto a cena 3D (`piloto-ep02/scripts/cena_ep02.py`, reaproveitando `lowpoly_lib.py`), renderizo e monto o vídeo final com legendas, etiquetas, SFX e música, como no EP01.
