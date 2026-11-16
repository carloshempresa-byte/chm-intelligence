# Engenharia Animada: Short de curiosidade
## "O tatuzão: a máquina que cava o túnel e monta as paredes ao mesmo tempo" (tuneladora / TBM)

**Formato:** Short vertical 9:16, 1080x1920, 30 fps. Mesmo estilo e pipeline do EP01 e do EP02:
- animação 3D low-poly, cores chapadas, sombra suave e câmera em movimento
- mascote **Eng. Carlin**, com o nome na faixa do capacete
- narração masculina PT-BR rápida e sem silêncio (edge-tts `pt-BR-AntonioNeural`, +20%)
- legendas palavra a palavra
- etiquetas em pílula

**Fora da série da caldeira.** Vídeo avulso de curiosidade.

**Duração estimada:** ~66–70 s. São 211 palavras, mais os números falados por extenso. No EP02, 213 palavras deram 64,6 s.

**Status:** só o roteiro. Ainda não gerei voz nem renderizei; aguarda o OK do Carlos.

**Regras deste roteiro**
- O Carlos não é especialista em túneis. Todo número e fato da narração vem de fonte pública, listada no fim e cruzada na tabela "De onde vem cada afirmação".
- Dado sem fonte boa ficou genérico ou saiu.
- Nenhuma marca ou logotipo de fabricante aparece no visual nem na narração. A tuneladora é genérica.

---

## Narração completa (texto para o TTS)

> São Paulo trouxe uma máquina de 133 metros e cerca de 2.600 toneladas pra cavar túnel de metrô. É a tuneladora, ou TBM. Parece uma minhoca gigante, mas aqui o apelido é tatuzão. Na frente, uma roda de corte gira e tritura o terreno. Mas aí vem o problema: terra mole desaba. Então a máquina trabalha dentro de um escudo de aço, e a própria terra escavada, presa numa câmara na frente, segura a pressão do terreno. Mas e toda essa terra? Uma rosca e esteiras levam tudo pra trás. E o túnel, não desaba? Não, porque ela mesma monta as paredes. Um braço mecânico encaixa peças de concreto pré-moldado, as aduelas, e forma um anel completo. E pra andar? Ela não tem rodas. Pistões hidráulicos empurram contra o último anel montado, a máquina avança e entra o próximo anel. Segundo o Metrô, dá pra abrir e revestir até 15 metros de túnel por dia. Por tradição, muitas dessas máquinas ganham nome de mulher, em homenagem a Santa Bárbara, padroeira dos mineiros. Em São Paulo, uma delas se chama Cora Coralina. Parabéns, você entendeu como funciona um tatuzão. Se você sabia, comente Engenheiro. Se não sabia, comente Estagiário. E manda pro amigo que ia curtir isso e segue pra ver mais máquinas gigantes.

**Chamadas de engajamento (pedido do Carlos)**
- **Faladas:** "manda pro amigo que ia curtir isso" e "segue pra ver mais máquinas gigantes". Vêm logo depois do CTA Engenheiro/Estagiário, numa frase só, para não estourar ~70 s.
- **Só na tela:** "COMENTE O QUE ACHOU", em pílula. Falado, repetiria o "comente" do CTA.
- **Se passar de 70 s no TTS:** corto primeiro "E pra andar? Ela não tem rodas." (a cena mostra isso sozinha).

**Notas de produção da voz:**
- **TBM:** o TTS deve ler "tê-bê-ême". Vou testar e, se ler errado, escrevo foneticamente só no áudio.
- **Números:** "2.600" deve sair "duas mil e seiscentas". A legenda fica em algarismos (**133 METROS**, **2.600 TONELADAS**, **15 METROS**).

---

## Roteiro cena a cena (tempos aproximados, ajustados depois do TTS)

| # | Tempo | Narração | Visual / câmera | Etiquetas (pílulas) | SFX |
|---|---|---|---|---|---|
| 0 | 0,0–5,0 | "São Paulo trouxe uma máquina de 133 metros e cerca de 2.600 toneladas pra cavar túnel de metrô." | **Gancho:** rua low-poly da cidade (prédios, carros, o Carlin na calçada). A câmera "mergulha" pelo chão num corte de terreno e revela, lá embaixo, a tuneladora comprida como um trem, atravessando o quadro inteiro. O Carlin olha para baixo, assustado. | **133 m** · **2.600 t** | whoosh mergulhando, ronco grave, boing |
| 1 | 5,0–9,0 | "É a tuneladora, ou TBM. Parece uma minhoca gigante, mas aqui o apelido é tatuzão." | Plano lateral da máquina inteira. Gag: um contorno de minhoca desenhado por cima "encaixa" na máquina e some com um pop. Depois aparece um tatu low-poly fofo de capacete, por 1 s, e some. | TUNELADORA = TBM · "TATUZÃO" | pop, boing |
| 2 | 9,0–12,0 | "Na frente, uma roda de corte gira e tritura o terreno." | Close frontal: a roda de corte gira (raios, ferramentas de corte simplificadas) e pedaços de terra low-poly se soltam da frente. | RODA DE CORTE | motor girando, terra caindo |
| 3 | 12,0–19,5 | "Mas aí vem o problema: terra mole desaba. Então a máquina trabalha dentro de um escudo de aço, e a própria terra escavada, presa numa câmara na frente, segura a pressão do terreno." | **Problema:** a roda "sozinha" avança e o teto de terra acima dela desmorona em blocos; o Carlin, dentro, se assusta e sua (exagero didático). **Rebobina.** Um cilindro de aço (escudo) desliza por cima da máquina. Corte em seção: a câmara atrás da roda se enche de terra, e setas amarelas mostram a terra empurrando de volta o terreno da frente. | DESABA! · ESCUDO DE AÇO · CÂMARA DE TERRA · PRESSÃO | desmoronamento, "fail", rewind, clang |
| 4 | 19,5–23,0 | "Mas e toda essa terra? Uma rosca e esteiras levam tudo pra trás." | A terra acumula e quase entope a câmara (o Carlin coça o capacete). Aparece uma rosca girando (hélice) que puxa a terra da câmara para uma esteira que corre para trás pela máquina. Os blocos de terra viajam pela esteira. | ROSCA · ESTEIRA | engrenagem, esteira rodando |
| 5 | 23,0–30,5 | "E o túnel, não desaba? Não, porque ela mesma monta as paredes. Um braço mecânico encaixa peças de concreto pré-moldado, as aduelas, e forma um anel completo." | Câmera dentro da cauda da máquina. Um braço mecânico gira, pega uma peça curva de concreto cinza e encaixa na parede. Peça por peça (genérico, sem número fixo de peças), fecha um anel. O anel completo brilha rapidinho. | ADUELAS (CONCRETO PRÉ-MOLDADO) · BRAÇO MECÂNICO · ANEL | encaixes de concreto (clunk), "ding" no anel completo |
| 6 | 30,5–36,5 | "E pra andar? Ela não tem rodas. Pistões hidráulicos empurram contra o último anel montado, a máquina avança e entra o próximo anel." | Gag: rodinhas de carro aparecem embaixo da máquina, levam um X vermelho e somem. Corte lateral em seção: vários pistões amarelos saem da máquina, apoiam no último anel e estendem; a máquina toda desliza para a frente. Os pistões recolhem e o braço monta o anel seguinte no espaço que abriu. | ~~RODAS~~ · PISTÕES HIDRÁULICOS · ÚLTIMO ANEL | "fail" curtinho, hidráulico (pssh), clunk |
| 7 | 36,5–41,0 | "Segundo o Metrô, dá pra abrir e revestir até 15 metros de túnel por dia." | Time-lapse: a máquina avança em pulinhos e os anéis vão se formando atrás, um atrás do outro. Uma régua no chão do túnel enche até "15 m". Sol e lua passando num quadrinho no canto (1 dia). | **ATÉ 15 m/DIA** | tic-tic dos anéis, whoosh |
| 8 | 41,0–49,0 | "Por tradição, muitas dessas máquinas ganham nome de mulher, em homenagem a Santa Bárbara, padroeira dos mineiros. Em São Paulo, uma delas se chama Cora Coralina." | A máquina para. Uma plaquinha de nome (sem marca de fabricante) desce e se prende na frente da máquina, com uma faixa de "batismo" (laço). O Carlin bate palma. A plaquinha mostra "CORA CORALINA". Santa Bárbara só aparece em texto (pílula), sem imagem religiosa. | NOME DE MULHER · SANTA BÁRBARA, PADROEIRA DOS MINEIROS · **CORA CORALINA** | sino, pop |
| 9 | 49,0–51,5 | "Parabéns, você entendeu como funciona um tatuzão." | Saída do túnel: a roda rompe uma parede de terra para a luz (estação/poço). Chuva de confete, o Carlin pulando. | PARABÉNS! | estouro de terra, torcida, sino |
| 10 | 51,5–~68 | "Se você sabia, comente Engenheiro. Se não sabia, comente Estagiário. E manda pro amigo que ia curtir isso e segue pra ver mais máquinas gigantes." | O Carlin comemora com a máquina ao fundo e a câmera orbitando. CTA em pílulas grandes no topo, como no EP01/EP02. No fim, pílulas rápidas de engajamento: o Carlin aponta para a tela (manda pro amigo) e faz joinha (segue). | SABIA? COMENTE **ENGENHEIRO** · NÃO SABIA? COMENTE **ESTAGIÁRIO** · COMENTE O QUE ACHOU · MANDA PRO AMIGO · SEGUE PRA MAIS MÁQUINAS GIGANTES | "win" ×2, pop, pop |

**Trilha:** a mesma ("Feeling Happy", Mixkit), bem baixa e com ducking. Pop automático em cada etiqueta.

**Novos elementos 3D (produção):**
- rua e corte de terreno
- tuneladora genérica com roda de corte, escudo, câmara, rosca, esteira, braço montador e pistões
- aduelas e anéis
- tatu de capacete (gag rápida) e plaquinha de nome

Reaproveita do EP01/EP02: mascote, confete, câmera, legendas, etiquetas e mixagem.

**Escala:** estilizada. A máquina fica encurtada para caber no vertical. Nada no visual reproduz uma máquina real ou de um fabricante específico.

---

## De onde vem cada afirmação

| Afirmação na narração | Fonte(s) | Observação |
|---|---|---|
| Máquina de **133 m** e **cerca de 2.600 t** trazida para túnel de metrô em SP | [SEMIL / Governo de SP (mar/2026)](https://semil.sp.gov.br/?p=133427); [Correio da Manhã (mar/2026)](https://www.correiodamanha.com.br/nacional/sao-paulo/estado-de-sao-paulo/2026/03/266052-nova-tuneladora-chega-ao-brasil-para-expandir-linha-2-verde-do-metro.html) | É a segunda tuneladora da expansão da Linha 2-Verde (trecho Penha–Dutra, cerca de 7 km). A narração não diz que ela já está cavando, porque não confirmei o status atual. O nome do fabricante aparece nas fontes, mas fica fora do vídeo. |
| Apelido "**tatuzão**" para a tuneladora | [Agência SP (Governo de SP)](https://www.agenciasp.sp.gov.br/governo-de-sp-posiciona-tatuzao-para-perfuracao-de-novo-trecho-da-linha-2-verde/) | "Minhoca gigante" é só comparação visual da narração, não é apelido oficial. |
| **Roda de corte** na frente que tritura o terreno | [Agência SP](https://www.agenciasp.sp.gov.br/governo-de-sp-posiciona-tatuzao-para-perfuracao-de-novo-trecho-da-linha-2-verde/); [ITA – EPB shield](https://tunnel.ita-aites.org/en/how-to-go-underground/construction-methods/mechanized-tunnelling/epbs-shield) | |
| Em solo, trabalha dentro de um **escudo** de aço e a **terra escavada, numa câmara, segura a pressão** do terreno | [ITA – International Tunnelling and Underground Space Association, "EPB shield"](https://tunnel.ita-aites.org/en/how-to-go-underground/construction-methods/mechanized-tunnelling/epbs-shield) | É o princípio da máquina de pressão de terra balanceada (EPB), tipo de "shield". A nova máquina de SP é descrita como de modo duplo, EPB e aberto ([Diário do Transporte, 2025](https://diariodotransporte.com.br/2025/11/23/metro-de-sao-paulo-e-fabricante-chinesa-creg-apresentam-segunda-tuneladora-da-linha-2-verde-equipamento-chega-no-brasil-no-primeiro-trimestre-de-2026/)). Por isso a narração diz "terra mole" (solo). |
| **Rosca** e **esteiras** levam a terra para trás | [ITA – EPB shield](https://tunnel.ita-aites.org/en/how-to-go-underground/construction-methods/mechanized-tunnelling/epbs-shield) (rosca que tira a terra da câmara controlando a pressão); [Agência SP](https://www.agenciasp.sp.gov.br/governo-de-sp-posiciona-tatuzao-para-perfuracao-de-novo-trecho-da-linha-2-verde/) (esteiras para retirada de terra) | |
| Ela monta as paredes com **peças de concreto pré-moldado (aduelas)** formando **anéis** | [Agência SP](https://www.agenciasp.sp.gov.br/governo-de-sp-posiciona-tatuzao-para-perfuracao-de-novo-trecho-da-linha-2-verde/) (estrutura para colocação das aduelas); [FHWA – Highway and Rail Transit Tunnel Inspection Manual, cap. 2](https://webarchive.library.unt.edu/eot2008/20081110003705/http:/www.fhwa.dot.gov/bridge/tunnel/inspectman02.cfm) (segmentos pré-fabricados montados dentro da cauda do escudo da TBM) | O número de aduelas por anel ficou **genérico**, porque as fontes divergem e variam por projeto. |
| **Braço mecânico** que encaixa as aduelas | [Robbins – EPB TBM (documento técnico)](https://www.robbinstbm.com/wp-content/uploads/2017/05/EPB6-7m_March.27.2017.pdf) ("segment erector" que monta o revestimento após cada avanço) | É documento de fabricante, usado só como referência técnica. Nada da marca vai para o vídeo. |
| **Pistões hidráulicos** empurram contra o **último anel montado** para avançar; não tem rodas | [ITA – EPB shield](https://tunnel.ita-aites.org/en/how-to-go-underground/construction-methods/mechanized-tunnelling/epbs-shield) (macacos de avanço apoiados no revestimento); [Robbins](https://www.robbinstbm.com/wp-content/uploads/2017/05/EPB6-7m_March.27.2017.pdf) ("thrust cylinders… pushing off against concrete segments") | |
| **Até 15 m** de túnel por dia, **segundo o Metrô** | [Olhar Digital (out/2026)](https://olhardigital.com.br/curiosidades/2026/10/09/como-se-constroi-uma-estacao-de-metro-dezenas-de-metros-abaixo-da-rua-sem-parar-a-cidade-a-tecnica-do-tatuzao-explicada-passo-a-passo/); [Diário do Transporte (jun/2023): "tatuzão vai avançar entre 10 e 15 metros por dia; Governo de SP explica"](https://diariodotransporte.com.br/2023/06/09/expansao-da-linha-2-verde-tatuzao-vai-avancar-entre-10-e-15-metros-por-dia-governo-de-sao-paulo-explica-como-vai-ser-operacao/) | É capacidade máxima e o ritmo real varia com o solo. Por isso a narração usa "até" e atribui ao Metrô. |
| Por tradição, muitas TBMs ganham **nome de mulher**, em homenagem a **Santa Bárbara**, padroeira dos mineiros | [ICE – Institution of Civil Engineers: "Why are TBMs named after women?"](https://ice.org.uk/news-views-insights/inside-infrastructure/why-are-tbms-named-after-women); [Cross River Rail – Governo de Queensland](https://crossriverrail.qld.gov.au/news/heres-to-the-groundbreakers-cross-river-rail-honours-iconic-queensland-women/) | As fontes divergem sobre quando a tradição começou, então a narração não cita época. |
| Em São Paulo, uma delas se chama **Cora Coralina** | [Agência SP](https://www.agenciasp.sp.gov.br/governo-de-sp-posiciona-tatuzao-para-perfuracao-de-novo-trecho-da-linha-2-verde/) | É a primeira tuneladora da expansão da Linha 2-Verde, não a de 133 m / 2.600 t do gancho. Por isso o texto diz "uma delas". |

### Dados pesquisados que ficaram de fora (fontes divergem ou não confirmei)
- **Peso e comprimento da Cora Coralina:** as reportagens citam ~2.100 t, ~2.500 t e ~2.700 t, e ~100 m. Não usei.
- **Número de aduelas por anel e peso de cada aduela:** variam por projeto e entre fontes. Ficou genérico.
- **Comparações de tamanho** ("maior da América Latina", "maior do mundo"): aparecem em manchetes, mas não confirmei em fonte oficial. Não usei.
- **Bertha (Seattle, 17,5 m de diâmetro):** bem documentada ([Wikipedia](https://en.wikipedia.org/wiki/Bertha_(tunnel_boring_machine)), [Construction Equipment Guide](https://www.constructionequipmentguide.com/bertha-breaks-through-iconic-tbm-emerges-into-daylight-in-seattle/33805)), mas ficou fora para manter o foco em SP e caber em ~70 s.

### Limitação da pesquisa
A rede desta sessão não abriu algumas páginas diretamente, entre elas learninglegacy.crossrail.co.uk e diariodotransporte.com.br. Os dados dessas fontes vêm dos trechos devolvidos pela busca. Antes do render, vale abrir os links da tabela e conferir os números (**133 m**, **2.600 t**, **até 15 m/dia** e **Cora Coralina**).

---

## Lista de fontes
1. Governo de SP / SEMIL: nova tuneladora da Linha 2-Verde (133 m, ~2.600 t). https://semil.sp.gov.br/?p=133427
2. Agência SP: "Governo de SP posiciona 'tatuzão' para perfuração de novo trecho da Linha 2-Verde". https://www.agenciasp.sp.gov.br/governo-de-sp-posiciona-tatuzao-para-perfuracao-de-novo-trecho-da-linha-2-verde/
3. Correio da Manhã: "Nova tuneladora chega ao Brasil para expandir Linha 2-Verde do Metrô" (mar/2026). https://www.correiodamanha.com.br/nacional/sao-paulo/estado-de-sao-paulo/2026/03/266052-nova-tuneladora-chega-ao-brasil-para-expandir-linha-2-verde-do-metro.html
4. Diário do Transporte: "Expansão da Linha 2-Verde: tatuzão vai avançar entre 10 e 15 metros por dia" (jun/2023). https://diariodotransporte.com.br/2023/06/09/expansao-da-linha-2-verde-tatuzao-vai-avancar-entre-10-e-15-metros-por-dia-governo-de-sao-paulo-explica-como-vai-ser-operacao/
5. Diário do Transporte: segunda tuneladora da Linha 2-Verde, tipo EPB/modo aberto (nov/2025). https://diariodotransporte.com.br/2025/11/23/metro-de-sao-paulo-e-fabricante-chinesa-creg-apresentam-segunda-tuneladora-da-linha-2-verde-equipamento-chega-no-brasil-no-primeiro-trimestre-de-2026/
6. Olhar Digital: "Como se constrói uma estação de metrô dezenas de metros abaixo da rua… a técnica do 'tatuzão'" (out/2026). https://olhardigital.com.br/curiosidades/2026/10/09/como-se-constroi-uma-estacao-de-metro-dezenas-de-metros-abaixo-da-rua-sem-parar-a-cidade-a-tecnica-do-tatuzao-explicada-passo-a-passo/
7. ITA-AITES (Associação Internacional de Túneis): "EPB shield". https://tunnel.ita-aites.org/en/how-to-go-underground/construction-methods/mechanized-tunnelling/epbs-shield
8. FHWA (Departamento de Transportes dos EUA): Highway and Rail Transit Tunnel Inspection Manual, cap. 2 (cópia arquivada). https://webarchive.library.unt.edu/eot2008/20081110003705/http:/www.fhwa.dot.gov/bridge/tunnel/inspectman02.cfm
9. Robbins: documento técnico de TBM EPB (referência técnica; marca fora do vídeo). https://www.robbinstbm.com/wp-content/uploads/2017/05/EPB6-7m_March.27.2017.pdf
10. ICE (Institution of Civil Engineers, Reino Unido): "Why are TBMs named after women?". https://ice.org.uk/news-views-insights/inside-infrastructure/why-are-tbms-named-after-women
11. Cross River Rail (Governo de Queensland, Austrália): TBMs com nomes de mulheres. https://crossriverrail.qld.gov.au/news/heres-to-the-groundbreakers-cross-river-rail-honours-iconic-queensland-women/
12. (pesquisado, não usado) Bertha (TBM de Seattle). https://en.wikipedia.org/wiki/Bertha_(tunnel_boring_machine) e https://www.constructionequipmentguide.com/bertha-breaks-through-iconic-tbm-emerges-into-daylight-in-seattle/33805

## Próximo passo
Com o OK do Carlos, eu gero a voz e confiro a duração (meta ≤ 70 s), amarro os tempos, monto `piloto-tuneladora/scripts/cena_tuneladora.py` (reaproveitando a biblioteca do EP02) e renderizo.
