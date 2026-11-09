# Regras do gerador de Shorts: The Top Ones

O código lê as regras de `tools/rules.json`, usado por `tools/post_kit.py` e `tools/build.py`. Este arquivo é a versão legível; ao mudar uma regra, mude os dois.

## 1. Título do post
- No máximo **~6 palavras**. #shorts e emojis não contam.
- **Palavra-chave principal em MAIÚSCULO** (ex.: BEST, WORST). Só ela fica em caixa alta.
- Termina com **#shorts** e tem até 100 caracteres. Hashtags do nicho não vão no título.
- O código avisa quando o título não cumpre e sugere um que cumpre. Exemplo: "Ranking Neymar's BEST Dribbles #shorts".

## 2. Hashtags
- **2 ou 3 hashtags do nicho**, na descrição.
- Sem variações repetidas: entre #neymar e #neymarjr, fica só a primeira.
- Sem hashtags virais fora do tema (#fyp, #viral, #trending, #foryou etc.; a lista está em `rules.json`).
- #shorts vai só no título.
- O código remove as proibidas e as repetidas, corta para no máximo 3 e avisa. Também avisa se uma hashtag parece fora dos termos do nicho.

## 3. Descrição
É gerada automaticamente no `post.txt`, nesta ordem:
1. Uma linha de gancho com **pergunta** para o público.
2. Créditos de cada clipe, do #1 ao #N: nome do lance, criador original (@) e link.
3. Música, artista, fonte e licença, mais o efeito sonoro, se houver.
4. "Subscribe to The Top Ones for more rankings!"
5. As hashtags.

## 4. Checklist de postagem
O `checklist.txt` é gerado junto com cada vídeo:
- Revisar o export do começo ao fim: sem tela preta, áudio ok. O código já roda uma verificação automática de tela preta, silêncio, loudness e resolução e anota o resultado no arquivo.
- Subir como **NÃO LISTADO**, esperar 10–20 min e conferir direitos autorais no YouTube Studio.
- Escolher a capa pelo app do celular.
- Não é conteúdo para crianças; sem restrição de idade.
- Comentários abertos, Remix ativado, sem tags e sem local.
- Preencher "Vídeo relacionado" com outro Short do canal.
- Só então deixar **PÚBLICO**.

Os avisos do gerador (título, hashtags, clipes) também aparecem no checklist.

## 5. Clipes
- O código **sinaliza com aviso** todo clipe que vem de conta oficial ou de transmissão: clubes, emissoras, ligas e federações, perfis de mídia. O aviso fala do risco de copyright/Content ID e sugere **preferir gravações amadoras** (arquibancada, celular, pelada, treino aberto).
- A detecção usa as listas e padrões de `rules.json` (`clips.*`), aplicados ao @ e ao nome do criador.
- Para silenciar um falso alerta, marque o clipe com `"source_type": "amador"`.
- Os créditos (@, nome, link, views) saem do config ou do `.info.json` que o yt-dlp grava ao lado do clipe.

## 6. Música
- **Só música livre de direitos**, de biblioteca permitida (Mixkit, YouTube Audio Library, Pixabay), com fonte, licença e link declarados em `audio.music_meta`.
- **Nada de música em alta**: sons do TikTok, Spotify, YouTube Music, sped up ou remix.
- Se a música não cumprir, o **build aborta** antes de renderizar.
- O áudio original dos clipes não é usado, **exceto** nos nichos em que o som é o conteúdo (ex.: ronco de motor), com `audio.keep_clip_audio: true`. Nesse caso a música vira só uma cama baixa (`audio.music_bed_db`, padrão -22 dB) e o código avisa todo clipe cujo áudio no TikTok não seja "original sound" (risco de música comercial).

## Regras de produção (já no build.py, do pedido original)
- 1080x1920, 30 fps.
- Título em 2 linhas, em Archivo Black, com as palavras-chave em #44C9F0.
- Vídeo no meio e lista 1..N embaixo; o nome de cada posição é preenchido quando o clipe dela toca.
- Ordem embaralhada, com o #1 sempre por último.
- Zoom de ~1,1x, clipes alternados espelhados, ajuste leve de cor e contraste.
- Clipes:
  - 5 a 7 clipes virais (1M+ views), de criadores diferentes;
  - jogada inteira até o desfecho, mais ~1 s de comemoração;
  - 8–15 s cada, o #1 até ~20 s, 60–90 s no total;
  - conferir frames a cada 0,5 s antes de renderizar.
- Áudio: trilha contínua já animada no 0 s, whoosh nas trocas, fade-out no final, -14 LUFS.

## Campos do config.json usados pelas regras
| Campo | Para quê |
|---|---|
| `post.title` | Título do post (validado). Sem ele, o código monta um com `subject` + `keyword` + `topic` |
| `post.main_keyword` | Palavra-chave que tem de estar em MAIÚSCULO |
| `post.hook` | Linha de gancho com pergunta |
| `post.hashtags` | 2–3 hashtags do nicho |
| `post.niche_terms` | Termos do nicho, para checar se as hashtags estão no tema |
| `clips[].creator`, `creator_name`, `url`, `views` | Crédito do original (opcional se houver `.info.json`) |
| `clips[].source_type` | `"amador"` silencia falso alerta de conta oficial |
| `audio.music_meta` | `{title, artist, source, license, url, license_url}`, obrigatório |
| `audio.sfx_meta` | `{title, source, license, url}`, recomendado |
| `audio.true_peak` | Teto do limitador. O AAC pode subir o pico em até ~3 dB; o checklist avisa se o arquivo final passar de -1 dBTP |
| `audio.duck` | `true` (padrão): a música abaixa sob cada whoosh, para ele aparecer em trilhas densas |
| `audio.aac_bitrate` | Padrão `256k` |
| `clips[].replay` | `{start, end, speed (0.5), zoom, focus_x, focus_y}`: replay em câmera lenta anexado ao clipe (ex.: no #1) |
| `clips[].zoom` | Zoom próprio do clipe (padrão: `zoom` global, 1,1) |
| `audio.keep_clip_audio` | `true` mantém o som original dos clipes (normalizado por clipe em `audio.clip_lufs`, padrão -16) |
| `audio.music_bed_db` | Volume da cama musical quando o som dos clipes é mantido (padrão -22 dB) |
| `clips[].mute_audio` / `audio_ok` / `clip_gain_db` | Silencia o som de um clipe / confirma que o áudio dele não tem música comercial / ajuste fino de volume |

## Como rodar
- `python3 -I tools/build.py <config.json>`: valida, renderiza e grava `post.txt` e `checklist.txt` na pasta do vídeo.
- `python3 -I tools/build.py <config.json> --stage post`: só regera o `post.txt` e o `checklist.txt`.
- `python3 -I tools/post_kit.py <config.json> --check`: só valida, sem gravar nada.
