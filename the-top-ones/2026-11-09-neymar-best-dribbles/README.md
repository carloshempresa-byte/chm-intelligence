# The Top Ones: Ranking Neymar's BEST Dribbles

Short faceless de ranking, 1080x1920, 30 fps, 60,6 s.

| Arquivo | O que é |
|---|---|
| `the_top_ones_neymar_best_dribbles_1080p.mp4` | Versão final para upload (H.264 High, CRF 17, AAC 192k), 43 MB |
| `the_top_ones_neymar_best_dribbles_720p.mp4` | Cópia 720x1280 para o celular, 17,3 MB |
| `preview.jpg` | Frame de prévia (aos 48 s: o chapéu do #1, lista completa) |
| `post.txt` | Título, descrição com créditos e hashtags, pronto para colar |
| `config.json` | Cortes, enquadramento e parâmetros usados (caminhos locais anonimizados) |

## Clipes (ordem de exibição 4, 2, 5, 3, 1)

| # | Nome na lista | Criador | Views* | Trecho da fonte | Tipo de imagem |
|---|---|---|---|---|---|
| 4 | Street 1v1 Nutmeg | @street_panna | 5,5M | 0,00 a 8,20 s | Amadora (celular) |
| 2 | Solo Goal at the Parc | @psg | 15,2M | 6,33 a 17,10 s | Transmissão de TV (postada pelo clube) |
| 5 | Touchline Escape | @thiago.leutz | 15,2M | 0,00 a 10,00 s | Amadora (arquibancada) |
| 3 | Slalom vs Corinthians | @tntsportsbr | 1,0M | 0,00 a 13,45 s | Transmissão de TV (câmera aérea) |
| 1 | Sombrero vs Fluminense | @santosfc | 4,2M | 0,00 a 18,20 s | Câmera do clube, do alto da arquibancada |

*Views lidas nos metadados do yt-dlp em 09/11/2026.

Cada corte termina num ponto natural da jogada (risada depois da caneta, bola na rede e comemoração, passe concluído, falta sofrida, passe depois do chapéu). Todos começam antes do lance e nenhum inclui frame de outra cena: os pontos de corte foram medidos com detecção de cena e conferidos frame a frame.

## Edição

- Título em Archivo Black, "NEYMAR'S" e "DRIBBLES" em #44C9F0.
- Vídeo no meio (1080x870) e lista 1..5 embaixo. O nome entra deslizando quando o clipe daquela posição começa, e a linha atual fica destacada em azul.
- A lista termina em y = 1550 para não ficar debaixo do nome do canal e da legenda do Shorts.
- Zoom de 1,1x sobre o enquadramento, espelhamento no 2º e no 4º clipe (#2 e #3), contraste +7% e saturação +14%. O clipe da TNT ficou mais neutro porque a fonte já vinha saturada.

## Áudio

- Todo o áudio original foi descartado (os clipes são renderizados com `-an`).
- Trilha: "Lord Knows" (Arulo, Mixkit, Stock Music Free License). Começa aos 11,08 s da faixa, no drop do 808, então o vídeo abre com a batida cheia.
- Whoosh da Mixkit ("Fast whoosh transition") nas 4 trocas, com o pico alinhado ao corte.
- Fade-out de 2,2 s. Medido no MP4 final: -14,1 LUFS integrado e true peak de -1,1 dBTP.

## Ferramentas

`../tools/` tem os scripts usados: `build.py` (cortes, composição e áudio), `overlays.py` (título e lista) e `discover.js` (coleta das páginas de descoberta do TikTok num navegador headless). Os clipes de origem não foram versionados.
