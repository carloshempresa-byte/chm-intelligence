# Engenharia Animada: vídeo curto de curiosidade
## "A máquina que engole montanhas": a escavadeira Bagger 288

**Formato:** vertical 9:16, 1080x1920, 30 fps, publicado como Reels e Short. Mesma identidade do vídeo da tuneladora:
- mascote **Eng. Carlin** com o nome no capacete
- low-poly, narração pt-BR (edge-tts `pt-BR-AntonioNeural`, +20%)
- legendas palavra a palavra e etiquetas em pílula

**Status:** revisão 2, **aprovada pelo Carlos**. Inclui as correções conferidas na página oficial do fabricante (arquivada), na Der Spiegel e no museu de mineração de Bochum: peso, comprimento, roda com 18 caçambas e a comparação dos caminhões. Os [VERIFICAR] foram resolvidos. Fase atual: modelagem e quadros de teste (sem voz, sem render completo).

**Duração estimada:** ~1 min 55 s a 2 min 5 s. São ~350 palavras, mais os números por extenso. Na tuneladora, 380 palavras deram 1 min 54 s. Fica abaixo do teto pedido (~2 min 30 s) e do limite de 3 min do Short e do Reels.

**Regras deste roteiro**
- **Números:** só os que têm fonte, listados no fim e conferidos nas fontes oficiais.
- **Marcas:** nenhuma no visual nem na narração. Nem fabricante nem dona da mina; a máquina aparece só pelo nome, "Bagger 288".
- **Custo:** tudo dentro do plano atual, sem nada pago. Blender 3.6 (gratuito), edge-tts, efeitos e música Mixkit (gratuitos) e a mesma máquina de nuvem desta sessão.

---

## Narração completa (texto para o TTS)

> Essa máquina engole montanhas. É a Bagger 288, uma escavadeira de roda de caçambas que trabalha na Alemanha. Ela tem 96 metros de altura, mais que dois Cristos Redentores empilhados. Tem 225 metros de comprimento, mais de dois campos de futebol. E pesa quase 13 mil toneladas, o peso de mais de 8 mil carros. Mas pra que uma máquina desse tamanho? Ela trabalha em minas a céu aberto, onde o carvão fica escondido debaixo de camadas e camadas de terra. E pra chegar no carvão, alguém precisa tirar toda essa terra de cima. É aí que entra a roda. Na ponta de um braço gigante, uma roda de 21,6 metros de diâmetro, com 18 caçambas, gira sem parar. Cada caçamba tem dentes e raspa uma fatia do barranco. Mas aí vem o problema: se cada caçamba tivesse que ir lá longe esvaziar, a máquina ia passar o dia indo e voltando. Então a terra cai, do alto da roda, direto numa correia transportadora. A correia corre pelo braço, passa pelo corpo da máquina e sai do outro lado, pra outras correias que levam tudo pra fora da mina. Ou seja: ela cava e despeja ao mesmo tempo, sem parar. São 240 mil metros cúbicos de material por dia. Isso enche mais de 10 mil caminhões basculantes. E como um gigante desses anda? Sem rodas: são 12 esteiras, cada uma com 3,8 metros de largura, espalhando o peso pra máquina não afundar. Mas não espere velocidade: ela anda de 2 a 10 metros por minuto. E não tem motor a diesel. Ela é elétrica e puxa 16,56 megawatts por um cabo. Sabe quantas pessoas operam esse monstro? Só cinco. Agora, o momento mais doido: em 2001, ela precisou mudar de mina. Em vez de desmontar, ela foi andando. Foram 22 quilômetros em três semanas, atravessando uma rodovia, um rio e uma ferrovia, num caminho preparado antes pra aguentar o peso. Parabéns, você entendeu como funciona a Bagger 288. Sabia? Comente Engenheiro. Não sabia? Comente Estagiário. E manda pro amigo que ia curtir isso e segue pra ver mais máquinas gigantes.

**Números:** todos confirmados pelo Carlos nas fontes oficiais (fabricante, Der Spiegel e museu de mineração de Bochum). Ver a tabela no fim.

**Notas de produção da voz:**
- **"Bagger":** o TTS deve ler "báguer". Vou testar e, se ler errado, uso grafia fonética só no áudio.
- **Números por extenso no áudio, se o TTS errar:** 13.500, 16,56, 240 mil.
- **Legenda:** fica em algarismos.

---

## Padrão visual novo (pedido do Carlos: subir muito a qualidade)

Continua low-poly, mas **rico em detalhe e com luz de cinema**. O que muda em relação aos vídeos anteriores:

| Item | Antes (EP01/EP02/tuneladora) | Agora (Bagger 288) |
|---|---|---|
| Modelo principal | Formas simples (caixas e cilindros) | Roda de caçambas com **todas as caçambas** (copo com borda, **dentes** individuais e corrente de reforço), **estrutura treliçada** de verdade (banzos e diagonais no braço e nos mastros), **cabos tensionados** de sustentação, **esteiras** com sapatas e roletes, **correias** com roletes e cobertura, **cabine** com vidros, **escadas**, **passarelas com guarda-corpo**, contrapeso, anel de giro |
| Cenário | Pátio plano | **Mina a céu aberto em degraus (bancadas)**, com camadas de solo de cores diferentes (terra clara, argila, areia e um veio escuro de carvão), poças, rampas, **correias de pátio** saindo da mina, **outros equipamentos** (escavadeira menor, tratores de esteira, caminhões), **pessoas pequenas** de capacete para escala, horizonte com campos, linhas de transmissão, **névoa atmosférica** ao fundo |
| Luz | Sol branco de meio-dia | **Golden hour**: sol baixo e quente (âmbar), céu em degradê laranja→azul, sombras longas e suaves, **ambient occlusion**, **bloom** leve nos reflexos e nas luzes da máquina |
| Câmera | Planos mais parados | **Sempre em movimento**: drone sobrevoando, órbitas, close nas caçambas cavando, câmera baixa (contra-plongée) para o gigantismo, travelling ao longo da correia, *whip-pans* e *push-ins* entre cenas |
| Efeitos | Poucos | **Poeira** saindo da roda, **terra caindo** das caçambas, **correia andando** (textura/peças em movimento), partículas no ar contra a luz, **motion blur** nos movimentos rápidos |
| Escala | Números só na pílula | **Comparações visuais** lado a lado (Cristo Redentor, campo de futebol, carro e pessoas), sempre com o número da fonte na tela |
| Texto | Pílulas médias | **Textos grandes e animados** (entra com *pop* e *shake*, contador de números rolando), **cortes rápidos** a cada 1,5–3 s, ritmo de Short viral |

**Como isso cabe no EEVEE e no plano atual (sem nada pago):**
- **Detalhe por instanciação:** as caçambas, os dentes, as sapatas das esteiras, os roletes e as diagonais da treliça são modelados uma vez e instanciados (linked duplicates), o que deixa a cena leve.
- **Névoa:** uso o passe *mist* do EEVEE com o compositor, e não volumetria pesada. Volumétrico só num plano curto de poeira, se couber no tempo.
- **Motion blur:** o do próprio EEVEE (1–2 passos).
- **Poeira:** partículas simples, *baked*.
- **Correia em movimento:** blocos de terra e roletes animados.

Tudo procedural em Python, com a mesma biblioteca dos vídeos anteriores (`lowpoly_lib.py`), ampliada.

---

## Roteiro cena a cena (tempos aproximados; ajustados depois do TTS)

| # | Tempo | Narração | Visual / câmera | Texto na tela | SFX |
|---|---|---|---|---|---|
| 0 | 0,0–2,0 | "Essa máquina engole montanhas." | **Gancho de 2 s:** câmera de drone rasante descendo no meio da névoa dourada. Uma **colina inteira** some, fatia por fatia, para dentro de uma roda de caçambas que gira enorme no primeiro plano. Terra despenca das caçambas contra o sol, com partículas brilhando. **Corte seco** na última sílaba. | **ENGOLE MONTANHAS** (gigante, entra com *shake*) | ronco grave, terra caindo, *whoosh* |
| 1 | 2,0–6,5 | "É a Bagger 288, uma escavadeira de roda de caçambas que trabalha na Alemanha." | Câmera baixa ao pé das esteiras subindo em *crane* até revelar a máquina inteira contra o céu laranja: mastros, cabos, braço da roda e braço de descarga. Pessoas minúsculas de capacete no chão. O Carlin aparece pequenininho, olhando para cima, boquiaberto. | **BAGGER 288** · ESCAVADEIRA DE RODA DE CAÇAMBAS · ALEMANHA | *boom* de revelação, vento |
| 2 | 6,5–10,0 | "Ela tem 96 metros de altura, mais que dois Cristos Redentores empilhados." | **Comparação 1:** a câmera recua para um plano lateral limpo. Duas silhuetas low-poly do Cristo Redentor (38 m cada, sem detalhe de rosto) surgem empilhadas ao lado e não alcançam o topo. Uma régua vertical anima subindo e o contador rola de 0 a **96 m**. | **96 m** · 2 × CRISTO (38 m) = 76 m | *tic-tic* do contador, "ding" |
| 3 | 10,0–13,0 | "Tem 225 metros de comprimento, mais de dois campos de futebol." | **Comparação 2:** vista de drone de cima. Dois campos de futebol com grama listrada e linhas brancas deslizam por baixo da máquina, que cobre os dois e ainda sobra. | **225 m** · MAIS DE 2 CAMPOS | *whoosh*, apito |
| 4 | 13,0–15,5 | "E pesa quase 13 mil toneladas, o peso de mais de 8 mil carros." | **Comparação 3:** close numa esteira afundando levemente na terra, com poeira. Ao lado, um carro low-poly genérico (sem marca) parece de brinquedo. Ele se multiplica numa onda de carros (instanciados) que enche o chão até o horizonte, enquanto o contador rola. O Carlin olha a fila de carros. | **~13 MIL t** · = **+8 MIL CARROS** | impacto grave, rangido |
| 5 | 15,5–24,0 | "Mas pra que uma máquina desse tamanho? Ela trabalha em minas a céu aberto, onde o carvão fica escondido debaixo de camadas e camadas de terra." | **Drone em órbita alta** sobre a mina em degraus. Corte para uma **seção do terreno** (estilo "bolo cortado" da tuneladora, agora mais rico): camadas coloridas (terra, argila e areia) e, lá embaixo, o **veio escuro de carvão**. A câmera desce pelas camadas como um elevador. | MINA A CÉU ABERTO · CAMADAS DE TERRA · **CARVÃO** | vento, terra escorrendo |
| 6 | 24,0–27,5 | "E pra chegar no carvão, alguém precisa tirar toda essa terra de cima. É aí que entra a roda." | As camadas de cima piscam em vermelho ("tirar!"). *Whip-pan* para a roda, que começa a girar, com as luzes da máquina acendendo (bloom). | TIRAR A TERRA DE CIMA · **A RODA** | motor elétrico subindo, "clank" |
| 7 | 27,5–36,0 | "Na ponta de um braço gigante, uma roda de 21,6 metros de diâmetro, com 18 caçambas, gira sem parar. Cada caçamba tem dentes e raspa uma fatia do barranco." | **Close cinematográfico:** câmera quase encostada na roda girando. Cada caçamba com dentes morde o barranco, a terra esfarela e cai, e a poeira sobe contra o sol. Corte para uma vista de perfil com o círculo da roda medido (anel animado) e um prédio genérico ao fundo para escala. *Slow-motion* curto de uma caçamba cheia subindo. | **21,6 m** · **18 CAÇAMBAS** · DENTES | raspagem de terra, rangido da roda, cascalho |
| 8 | 36,0–41,5 | "Mas aí vem o problema: se cada caçamba tivesse que ir lá longe esvaziar, a máquina ia passar o dia indo e voltando." | **Problema (gag):** em animação acelerada, uma caçamba "solta" vai e volta sozinha até o fim da mina, deixando um rastro de poeira. Um relógio gira rápido e o Carlin boceja e sua. Um X vermelho grande carimba a tela. | ✗ INDO E VOLTANDO | *whoosh* ida e volta, tique-taque, "fail" |
| 9 | 41,5–52,0 | "Então a terra cai, do alto da roda, direto numa correia transportadora. A correia corre pelo braço, passa pelo corpo da máquina e sai do outro lado, pra outras correias que levam tudo pra fora da mina." | **Solução:** a câmera acompanha um bloco de terra. Ele cai da caçamba no topo da roda para a **correia** (roletes girando, motion blur), corre pelo braço treliçado e passa pelo corpo da máquina por baixo das passarelas com guarda-corpo. Depois sai pelo **braço de descarga** e cai em correias de pátio que serpenteiam pela mina até o horizonte enevoado. | **CORREIA TRANSPORTADORA** · BRAÇO → CORPO → DESCARGA | correia rodando, terra caindo em cascata |
| 10 | 52,0–58,0 | "Ou seja: ela cava e despeja ao mesmo tempo, sem parar. São 240 mil metros cúbicos de material por dia. Isso enche mais de 10 mil caminhões basculantes." | Tela dividida animada: em cima a roda cavando, embaixo a correia despejando, em sincronia. Depois, *time-lapse* com sol e sombras correndo e uma pilha enorme de material crescendo ao lado da mina. Contador rolando. Depois, uma **fila de caminhões basculantes** genéricos (instanciados) se estende até o horizonte, cada um enchendo com um *pop*. | CAVA + DESPEJA · **240 MIL m³/DIA** · **+10 MIL CAMINHÕES** | ritmo acelerado, "ding" |
| 11 | 58,0–66,0 | "E como um gigante desses anda? Sem rodas: são 12 esteiras, cada uma com 3,8 metros de largura, espalhando o peso pra máquina não afundar." | **Câmera baixa** rente ao chão, entre as esteiras: as sapatas passam como ondas. Vista de baixo (corte translúcido) com as 12 esteiras destacadas uma a uma (pop + número). Setas de peso se espalhando no chão. Carlin ao lado de uma esteira: ela é bem mais larga que ele de braços abertos. | **12 ESTEIRAS** · **3,8 m** CADA · PESO ESPALHADO | estalos de esteira, rangido |
| 12 | 66,0–70,0 | "Mas não espere velocidade: ela anda de 2 a 10 metros por minuto." | Gag: uma tartaruga low-poly e o Carlin caminhando ultrapassam a máquina. Um velocímetro com o ponteiro quase parado. | **2 a 10 m/min** | "boing", tique-taque lento |
| 13 | 70,0–76,0 | "E não tem motor a diesel. Ela é elétrica e puxa 16,56 megawatts por um cabo." | Ícone de diesel com X. Um **cabo grosso** serpenteando pelo chão até a máquina pulsa com energia (brilho percorrendo o cabo, bloom) e as luzes da máquina se acendem em sequência. | ✗ DIESEL · **ELÉTRICA** · **16,56 MW** | zumbido elétrico, faísca |
| 14 | 76,0–80,0 | "Sabe quantas pessoas operam esse monstro? Só cinco." | *Push-in* rápido na cabine: cinco pessoinhas de capacete acenam, e a câmera recua até a máquina inteira, que faz as pessoas parecerem formigas. | **SÓ 5 PESSOAS** | "pop" ×5, risada curta |
| 15 | 80,0–98,0 | "Agora, o momento mais doido: em 2001, ela precisou mudar de mina. Em vez de desmontar, ela foi andando. Foram 22 quilômetros em três semanas, atravessando uma rodovia, um rio e uma ferrovia, num caminho preparado antes pra aguentar o peso." | **Sequência épica de drone:** a máquina saindo da mina ao pôr do sol. Mapa ilustrativo com a linha de 22 km sendo traçada e um calendário de 3 semanas folheando. Ela cruza **uma rodovia** (carros parados pequeninos, gente olhando), **um rio** (sobre o caminho preparado) e **uma ferrovia**, cada travessia com um corte rápido e uma pílula. O caminho aparece primeiro sendo preparado (camada nova de terra/areia por cima). | **2001** · **22 km** · **3 SEMANAS** · RODOVIA · RIO · FERROVIA · CAMINHO PREPARADO | sirene leve, multidão, trem ao fundo, música crescendo |
| 16 | 98,0–101,0 | "Parabéns, você entendeu como funciona a Bagger 288." | Plano herói de baixo para cima, com o sol estourando atrás da roda (*lens flare* via bloom). Confete dourado e o Carlin pulando no topo de um caminhão. | **PARABÉNS!** | torcida, sino |
| 17 | 101,0–~113 | "Sabia? Comente Engenheiro. Não sabia? Comente Estagiário. E manda pro amigo que ia curtir isso e segue pra ver mais máquinas gigantes." | Órbita lenta em volta da máquina na golden hour, com o Carlin comemorando. CTA em pílulas grandes, como nos vídeos anteriores. O Carlin aponta para a tela no "manda pro amigo" e faz joinha no "segue". | SABIA? COMENTE **ENGENHEIRO** · NÃO SABIA? COMENTE **ESTAGIÁRIO** · **COMENTE O QUE ACHOU** · MANDA PRO AMIGO · SEGUE PRA MAIS MÁQUINAS GIGANTES | "win" ×2, pop, pop |

**Trilha:** "Feeling Happy" (Mixkit) baixa no começo, crescendo na sequência épica da mudança de mina. Se quiser mais "cinema" nessa sequência, troco por outra trilha gratuita da Mixkit. Ducking sob a voz e pop automático em cada texto.

**Detalhes de modelagem (sem marca e sem copiar desenho de fábrica):**
- **Roda:** **18 caçambas** (dado do fabricante), cada uma com dentes e lábio reforçado.
- **Superestrutura:** mastros treliçados com cabos tensionados até o braço da roda e até o contrapeso, cabine com vidro, escadas, passarelas com guarda-corpo, luzes de trabalho.
- **Correias:** com roletes, transferência no centro e braço de descarga.
- **Chassi:** 12 esteiras (3 grupos), cada uma com sapatas.
- **Cores:** genéricas (amarelo/cinza/azul da paleta do canal), sem logotipo.

---

## De onde vem cada número/fato

| Na narração | Valor usado | Fonte(s) | Observação |
|---|---|---|---|
| Altura | **96 m** | [Fabricante, página oficial arquivada](https://web.archive.org/web/20221205121502/https:/thyssenkrupp-mining-technologies.com/de/products/schaufelradbagger-bagger-288/); Der Spiegel; Deutsches Bergbau-Museum Bochum (conferidos pelo usuário) | Confirmado. |
| Comprimento | **225 m** → "mais de dois campos de futebol" | [Fabricante (arquivado)](https://web.archive.org/web/20221205121502/https:/thyssenkrupp-mining-technologies.com/de/products/schaufelradbagger-bagger-288/); Der Spiegel; museu de Bochum | Confirmado. Campo de jogos internacionais: 100–110 m ([IFAB – Regra 1](https://downloads.theifab.com/downloads/laws-of-the-game-2015-16?l=de)), então 2 campos = 200–220 m < 225 m. |
| Peso | **12.840 t** → "quase 13 mil toneladas" | [Fabricante (arquivado)](https://web.archive.org/web/20221205121502/https:/thyssenkrupp-mining-technologies.com/de/products/schaufelradbagger-bagger-288/) | Confirmado. Substitui os 13.500 t da revisão 1. |
| Comparação de peso | **8.667 carros** → "mais de 8 mil carros" | [Fabricante (arquivado)](https://web.archive.org/web/20221205121502/https:/thyssenkrupp-mining-technologies.com/de/products/schaufelradbagger-bagger-288/) | Comparação dada pelo próprio fabricante. |
| Roda de caçambas | **21,6 m** de diâmetro, **18 caçambas** | [Fabricante (arquivado)](https://web.archive.org/web/20221205121502/https:/thyssenkrupp-mining-technologies.com/de/products/schaufelradbagger-bagger-288/); museu de Bochum | Confirmado. |
| Produção diária | **240 mil m³/dia** | [Fabricante (arquivado)](https://web.archive.org/web/20221205121502/https:/thyssenkrupp-mining-technologies.com/de/products/schaufelradbagger-bagger-288/) | Confirmado. |
| Comparação de produção | "**mais de 10 mil caminhões basculantes**" por dia | [Fabricante (arquivado)](https://web.archive.org/web/20221205121502/https:/thyssenkrupp-mining-technologies.com/de/products/schaufelradbagger-bagger-288/) | Comparação dada pelo próprio fabricante. |
| Esteiras | **12**, de **3,8 m** de largura | Confirmado pelo usuário; [Wikipedia – Bagger 288](https://en.wikipedia.org/wiki/Bagger_288) | |
| Velocidade | **2 a 10 m/min** | Confirmado pelo usuário; [Wikipedia – Bagger 288](https://en.wikipedia.org/wiki/Bagger_288) | |
| Energia | **16,56 MW**, elétrica, por cabo | Confirmado pelo usuário; [Wikipedia – Bagger 288](https://en.wikipedia.org/wiki/Bagger_288) | |
| Operadores | **5 pessoas** | Confirmado pelo usuário; [Wikipedia – Bagger 288](https://en.wikipedia.org/wiki/Bagger_288) | |
| Mina a céu aberto, terra removida para chegar ao carvão (linhito) | — | [Wikipedia – Bagger 288](https://en.wikipedia.org/wiki/Bagger_288); [Wikipedia – Bucket-wheel excavator](https://en.wikipedia.org/wiki/Bucket-wheel_excavator) | |
| Roda → correias → braço de descarga | — | [Wikipedia – Bucket-wheel excavator](https://en.wikipedia.org/wiki/Bucket-wheel_excavator) | Princípio geral desse tipo de máquina. |
| Mudança de **2001**: **22 km** em **3 semanas**, cruzando **rodovia, rio e ferrovia**, em caminho preparado | — | Confirmado pelo usuário (Der Spiegel, museu de Bochum); [museum-digital westfalen (PDF, alemão)](https://westfalen.museum-digital.de/pdf/object/32517.pdf?lang=de); [Wikipedia – Bagger 288](https://en.wikipedia.org/wiki/Bagger_288) | |
| **Cristo Redentor = 38 m** (≈30 m + pedestal de 8 m) → 2 × 38 = 76 m < 96 m | 38 m | [Cultura Genial](https://www.culturagenial.com/monumento-cristo-redentor/); [Assembleia Legislativa de SP](https://www.al.sp.gov.br/noticia/?id=310849) | Aprovado pelo Carlos junto com o roteiro. Aparece como silhueta simples, sem rosto. |

O nome do fabricante aparece só nesta lista de fontes, nunca no vídeo.

### Ficou de fora (fontes divergentes ou sem fonte boa)
- **Volume de cada caçamba:** as fontes citam 6,6 m³ e 15 m³. Ficou fora da narração.
- **Pressão no solo (1,71 bar):** é estimativa, não dado do fabricante.
- **Custo da mudança de 2001 (~15 milhões de marcos) e número de trabalhadores (70):** fonte única. Ficou fora.
- **"Maior/mais pesado veículo terrestre do mundo":** o recorde atual de peso do Guinness é da Bagger 293. Não usei.

### Conferência
Os números principais foram conferidos pelo usuário e pelo Carlos na página oficial do fabricante (arquivada no Internet Archive), na Der Spiegel e no Deutsches Bergbau-Museum Bochum.

---

## Lista de fontes (URLs)
0. **Fabricante: página oficial do Bagger 288 (arquivada no Internet Archive, em alemão)**: 96 m, 225 m, 12.840 t (= 8.667 carros), roda de 21,6 m com 18 caçambas, 240 mil m³/dia (= mais de 10 mil caminhões basculantes). https://web.archive.org/web/20221205121502/https:/thyssenkrupp-mining-technologies.com/de/products/schaufelradbagger-bagger-288/
0b. Der Spiegel e Deutsches Bergbau-Museum Bochum: conferidos pelo usuário (sem URL informada).
1. Wikipedia: Bagger 288. https://en.wikipedia.org/wiki/Bagger_288
2. Wikipedia: List of largest machines. https://en.wikipedia.org/wiki/List_of_largest_machines
3. Wikipedia: Bagger 293. https://en.wikipedia.org/wiki/Bagger_293
4. Wikipedia: Bucket-wheel excavator. https://en.wikipedia.org/wiki/Bucket-wheel_excavator
5. Guinness World Records: Heaviest land vehicle (Bagger 293, 14.196 t). https://guinnessworldrecords.com/world-records/384401-heaviest-land-vehicle
6. LWL / museum-digital westfalen: registro de museu sobre a mudança de 2001 (PDF, alemão). https://westfalen.museum-digital.de/pdf/object/32517.pdf?lang=de
7. Worcon: "Tuesday's marvels of engineering: Bagger 288". https://blog.wor-con.com/en/featured/tuesdays-marvels-of-engineering-bagger-288/
8. Mining Zimbabwe: "The Bagger 288 – the largest land vehicle". https://miningzimbabwe.com/the-bagger-288-the-largest-land-vehicle/
9. ScienceBlog: mudança de 2001 (225 m, 96 m, 22 km, 3 semanas). https://scienceblog.com/a-in-2001-germanys-rheinbraun-needed-to-move-its-bucket-wheel-excavator-bagger-288-a-machine-225-meters-long-and-96-meters-tall-some-22-kilometers-between-two-open-pit-mines-taking-three-weeks-at-a/
10. Cultura Genial: Cristo Redentor (30 m + 8 m de pedestal). https://www.culturagenial.com/monumento-cristo-redentor/
11. Assembleia Legislativa de SP: "Cristo Redentor: 80 anos de um símbolo". https://www.al.sp.gov.br/noticia/?id=310849
12. IFAB: Laws of the Game, Regra 1 (dimensões do campo). https://downloads.theifab.com/downloads/laws-of-the-game-2015-16?l=de
13. The FA: Law 1, The Field of Play. https://www.thefa.com/football-rules-governance/lawsandrules/laws/football-11-11/law-1---the-field-of-play

---

## Estimativa de render (com esse nível de detalhe)

| Etapa | Estimativa |
|---|---|
| Modelagem procedural + cenário + testes de enquadramento (folhas de contato em baixa resolução) | ~2–3 h de trabalho de script/teste |
| Render final 1080x1920, 30 fps, ~115 s = **~3.450 quadros** | No ritmo dos vídeos anteriores (3,8–5 s por quadro, cenas simples), a cena rica deve ficar em **~8–12 s por quadro**: mais geometria (instanciada), sombras suaves com cascata maior, AO, bloom, motion blur de 1–2 passos, partículas e névoa por *mist*. **Total: ~8 a 11,5 h de render.** |
| Composição 2D (legendas, textos animados), mixagem e montagem | ~10–15 min |

- **Tudo roda nesta máquina de nuvem**, com ferramentas gratuitas e sem custo extra.
- **O render é retomável.** Como cada tarefa em segundo plano dura no máximo 2 h, ele vai rodar em ~5–6 blocos, retomando de onde parar (igual ao EP02 e à tuneladora).
- **Se quiser encurtar:** dá para cair para ~6–8 h tirando o motion blur e usando menos partículas em planos longos, sem perder o visual principal (luz golden hour, AO, bloom, detalhes e câmera dinâmica).

## Próximo passo
Roteiro aprovado. Próximos passos:
1. gero a voz;
2. monto `piloto-bagger288/scripts/cena_bagger288.py`;
3. mostro **uma folha de contato com quadros de teste** do novo padrão visual antes de soltar o render completo, para o Carlos aprovar o salto de qualidade.
