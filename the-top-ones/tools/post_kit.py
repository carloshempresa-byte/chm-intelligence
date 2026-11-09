"""Kit de publicação dos Shorts do The Top Ones.

Valida título, hashtags, origem dos clipes e música contra rules.json e gera, ao lado do vídeo:
  post.txt       título + descrição (gancho com pergunta, créditos, música/licença, "Subscribe", hashtags)
  checklist.txt  checklist de postagem + verificação automática do export + avisos

uso:
  python3 -I post_kit.py <config.json> --check            só valida (não escreve nada)
  python3 -I post_kit.py <config.json> [--video <mp4>]    valida e escreve post.txt e checklist.txt
build.py importa este módulo: preflight() antes de renderizar e write_outputs() depois.

Campos usados no config.json:
  post.title           título do post (opcional; sem ele o título é montado com subject/keyword/topic)
  post.main_keyword    palavra-chave principal (ex.: "BEST"); tem de aparecer em MAIÚSCULO no título
  post.subject/keyword/topic   peças para montar o título sugerido ("Ranking Neymar's BEST Dribbles #shorts")
  post.hook            1 linha de gancho com pergunta para o público
  post.hashtags        2–3 hashtags do nicho (#shorts vai só no título)
  post.niche_terms     termos do nicho, para checar se as hashtags estão no tema (opcional)
  clips[].creator / creator_name / url / views   crédito do clipe (se faltar, lido do <src>.info.json do yt-dlp)
  clips[].source_type  "amador" para silenciar um falso alerta de conta oficial
  audio.music_meta     {title, artist, source, license, url, license_url}  (obrigatório)
  audio.sfx_meta       {title, source, license, url}                        (recomendado)
"""
import datetime, json, os, re, subprocess, sys
from urllib.parse import urlparse

TOOLS = os.path.dirname(os.path.abspath(__file__))
RULES = json.load(open(os.path.join(TOOLS, 'rules.json'), encoding='utf-8'))

EMOJI_RE = re.compile('[\U0001F000-\U0001FAFF\u2600-\u27BF\u2B00-\u2BFF\uFE0F\u200d\u20e3]+')
HASHTAG_RE = re.compile(r'#[^\W\d_]\w*')
SEPARATORS_RE = re.compile(r'[?!|•–—:]|' + EMOJI_RE.pattern)


class Report:
    def __init__(self):
        self.errors, self.warnings, self.info = [], [], []

    def err(self, msg):
        self.errors.append(msg)

    def warn(self, msg):
        self.warnings.append(msg)

    def note(self, msg):
        self.info.append(msg)

    def merge(self, other):
        self.errors += other.errors
        self.warnings += other.warnings
        self.info += other.info
        return self

    def print(self, header='post_kit'):
        for m in self.info:
            print(f'[{header}] {m}')
        for m in self.warnings:
            print(f'[{header}] AVISO: {m}')
        for m in self.errors:
            print(f'[{header}] ERRO: {m}')


# ------------------------------------------------------------------ título
def _strip_suffix(title):
    suf = RULES['title']['suffix']
    t = title.strip()
    return t[:-len(suf)].strip() if t.lower().endswith(suf) else t


def title_words(title):
    """palavras do título sem contar #shorts, outras hashtags e emojis ("#1" conta como palavra)"""
    t = EMOJI_RE.sub(' ', HASHTAG_RE.sub(' ', _strip_suffix(title)))
    return [w for w in t.split() if any(ch.isalnum() for ch in w)]


def _is_upper_word(w):
    letters = [ch for ch in w if ch.isalpha()]
    return len(letters) >= 3 and all(ch.isupper() for ch in letters)


def validate_title(title, main_keyword=None):
    r, tr = Report(), RULES['title']
    if not title or not title.strip():
        r.warn('título vazio')
        return r
    t = title.strip()
    if not t.endswith(tr['suffix']):
        r.warn(f'o título deve terminar com {tr["suffix"]}')
    if len(t) > tr['max_chars']:
        r.err(f'título com {len(t)} caracteres (limite do YouTube: {tr["max_chars"]})')
    words = title_words(t)
    if len(words) > tr['max_words']:
        r.warn(f'título com {len(words)} palavras; o máximo é ~{tr["max_words"]} (sem contar #shorts e emojis)')
    upper = [w for w in words if _is_upper_word(w)]
    if tr['require_uppercase_keyword']:
        if main_keyword:
            kw = main_keyword.upper()
            if not re.search(r'(?<![\w#])' + re.escape(kw) + r"(?:'S)?(?!\w)", t):
                r.warn(f'a palavra-chave principal "{kw}" tem de aparecer em MAIÚSCULO no título')
        elif not upper:
            r.warn('nenhuma palavra-chave em MAIÚSCULO (ex.: BEST, WORST)')
    if len(upper) > tr['max_uppercase_words']:
        r.warn(f'{len(upper)} palavras em caixa alta ({", ".join(upper)}); deixe só a palavra-chave principal em MAIÚSCULO')
    extra = [h for h in HASHTAG_RE.findall(t) if h.lower() != tr['suffix']]
    if extra:
        r.warn(f'hashtags no título além de {tr["suffix"]} ({" ".join(extra)}); as do nicho vão na descrição')
    return r


SMALL_WORDS = {'the', 'of', 'a', 'an', 'in', 'on', 'and', 'vs', 'to', 'for', 'at', 'by', 'with', 'or'}


def _bare(w):
    return re.sub(r"'s$", '', w, flags=re.I).strip('.,;').lower()


def suggest_title(post, fallback_title=None):
    """título no padrão: até ~6 palavras, só a palavra-chave em MAIÚSCULO, termina com #shorts"""
    tr = RULES['title']
    kw = (post.get('main_keyword') or post.get('keyword') or '').strip()
    if post.get('topic') and kw:
        subj = post.get('subject')
        core = f"Ranking {subj} {kw.upper()} {post['topic']}" if subj else f"Ranking the {kw.upper()} {post['topic']}"
        return ' '.join(core.split()[:tr['max_words']]) + ' ' + tr['suffix']
    base = HASHTAG_RE.sub(' ', _strip_suffix(fallback_title or post.get('title') or ''))
    parts = [p.strip() for p in SEPARATORS_RE.split(base) if p and len(p.split()) >= 2]
    words = [w for w in (parts[0] if parts else base).split() if any(ch.isalnum() for ch in w)][:tr['max_words']]
    # caixa normal em tudo (palavras pequenas em minúsculo), depois só a palavra-chave em MAIÚSCULO
    words = [w.lower() if i and w.lower() in SMALL_WORDS else
             (w[:1].upper() + w[1:].lower() if (w.isupper() or w.islower()) else w) for i, w in enumerate(words)]
    target = _bare(kw) if kw else next((_bare(w) for w in words if _bare(w).upper() in tr['auto_keywords']), None)
    if not target:  # sem superlativo: destaca a 1ª palavra de conteúdo (normalmente o assunto)
        target = next((_bare(w) for w in words if _bare(w) not in SMALL_WORDS | {'ranking', 'ranked'}), None)
    words = [w.upper() if target and _bare(w) == target else w for w in words]
    return ' '.join(words) + ' ' + tr['suffix']


# ------------------------------------------------------------------ hashtags
def _root(tag):
    return re.sub(r'[^a-z]', '', tag.lower())


def clean_hashtags(tags, context_terms=()):
    """devolve (hashtags finais, Report): tira virais, #shorts, variações repetidas; limita a 2–3"""
    r, hr = Report(), RULES['hashtags']
    banned = {t.lower() for t in hr['banned_viral']}
    title_only = {t.lower() for t in hr['title_only']}
    kept = []
    for raw in tags or []:
        tag = '#' + raw.strip().lstrip('#').lower()
        tag = re.sub(r'[^\w#]', '', tag)
        if len(tag) < 3:
            continue
        if tag in title_only:
            r.warn(f'{tag} removida das hashtags: ela vai só no título')
            continue
        if tag in banned:
            r.warn(f'{tag} removida: hashtag viral genérica, fora do tema')
            continue
        rt = _root(tag)
        dup = next((k for k in kept if len(min(_root(k), rt, key=len)) >= 4 and
                    (_root(k).startswith(rt) or rt.startswith(_root(k)))), None)
        if dup:
            r.warn(f'{tag} removida: variação repetida de {dup}')
            continue
        kept.append(tag)
    if len(kept) > hr['max']:
        r.warn(f'hashtags limitadas a {hr["max"]}: removidas {" ".join(kept[hr["max"]:])}')
        kept = kept[:hr['max']]
    if len(kept) < hr['min']:
        r.warn(f'só {len(kept)} hashtag(s) do nicho; use {hr["min"]}–{hr["max"]}')
    ctx = {_root(w) for w in context_terms if len(_root(w)) >= 4}
    if ctx:
        for tag in kept:
            rt = _root(tag)
            if not any(c in rt or rt in c for c in ctx):
                r.warn(f'{tag} pode estar fora do tema (não bate com os termos do nicho)')
    return kept, r


# ------------------------------------------------------------------ clipes
def clip_credit(clip):
    """handle, nome, url e views do criador original: do config ou do <src>.info.json do yt-dlp"""
    info = {}
    src = clip.get('src') or ''
    for p in (os.path.splitext(src)[0] + '.info.json', os.path.join(os.path.dirname(src), 'full.info.json')):
        if src and os.path.exists(p):
            try:
                info = json.load(open(p, encoding='utf-8'))
            except Exception:
                info = {}
            break
    handle = (clip.get('creator') or info.get('uploader') or '').lstrip('@')
    return {'handle': handle, 'name': clip.get('creator_name') or info.get('channel') or handle,
            'url': clip.get('url') or info.get('webpage_url') or '', 'views': clip.get('views') or info.get('view_count')}


def classify_source(handle, name=''):
    """(tipo, motivo) se parece conta oficial/transmissão; (None, '') se não"""
    cr = RULES['clips']
    h = (handle or '').lower().lstrip('@')
    for kind, key in (('emissora/mídia', 'broadcasters_media'), ('liga/federação', 'leagues_federations'), ('clube', 'clubs')):
        if h in cr[key]:
            return kind, f'@{h} está na lista de contas de {kind}'
    for pat in cr['official_name_patterns']:
        for target in (h, (name or '').lower()):
            if target and re.search(pat, target):
                return 'provável oficial', f'"{target}" bate com o padrão /{pat}/'
    return None, ''


def check_clips(clips):
    r = Report()
    flagged = 0
    for c in sorted(clips, key=lambda c: c.get('rank', 0)):
        cr = clip_credit(c)
        tag = f"#{c.get('rank', '?')} {c.get('name', '')}".strip()
        if not cr['handle'] or not cr['url']:
            r.warn(f'clipe {tag}: crédito incompleto (falta @criador ou link do original)')
        if (c.get('source_type') or '').lower() in ('amador', 'amateur'):
            continue
        kind, why = classify_source(cr['handle'], cr['name'])
        if kind:
            flagged += 1
            r.warn(f'clipe {tag} vem de conta oficial/transmissão ({kind}: {why}). Risco de copyright/Content ID. '
                   + RULES['clips']['advice'])
    if flagged:
        r.note(f'{flagged} de {len(clips)} clipes vêm de conta oficial/transmissão')
    return r


# ------------------------------------------------------------------ música
def _check_audio_meta(meta, allowed, label, required):
    r, mr = Report(), RULES['music']
    if not meta:
        (r.err if required else r.warn)(f'{label}: declare fonte e licença em audio.{"music_meta" if required else "sfx_meta"} '
                                        f'(só biblioteca livre de direitos, ex.: Mixkit)')
        return r
    src = (meta.get('source') or '').strip().lower()
    if src not in allowed:
        r.err(f'{label}: fonte "{meta.get("source")}" não permitida; use {", ".join(sorted(allowed))}')
        return r
    lic_ok = [l.lower() for l in allowed[src]['licenses']]
    if (meta.get('license') or '').strip().lower() not in lic_ok:
        r.err(f'{label}: licença "{meta.get("license")}" não confere com a de {meta.get("source")} '
              f'({" / ".join(allowed[src]["licenses"])})')
    host = urlparse(meta.get('url') or '').netloc.lower()
    if not host:
        r.err(f'{label}: falta o link (url) da faixa na biblioteca')
    elif not any(host == d or host.endswith('.' + d) for d in allowed[src]['domains']):
        r.err(f'{label}: link fora do domínio de {meta.get("source")} ({host})')
    blob = ' '.join(str(meta.get(k) or '') for k in ('title', 'artist', 'url', 'file')).lower()
    for d in mr['banned_domains']:
        if d in blob:
            r.err(f'{label}: domínio proibido ({d}): nada de música em alta/streaming')
    for kw in mr['banned_keywords']:
        if kw in blob:
            r.err(f'{label}: "{kw}" indica música em alta/remix; use só faixa livre de direitos')
    return r


def check_music(audio):
    mr = RULES['music']
    r = _check_audio_meta((audio or {}).get('music_meta'), mr['allowed_sources'], 'música', True)
    music_file = ((audio or {}).get('music') or '').lower()
    for d in mr['banned_domains']:
        if d in music_file:
            r.err(f'música: arquivo/URL de origem proibida ({d})')
    if (audio or {}).get('whoosh'):
        r.merge(_check_audio_meta((audio or {}).get('sfx_meta'), mr['allowed_sfx_sources'], 'efeito sonoro', False))
    return r


# ------------------------------------------------------------------ post (título + descrição)
def _post(cfg):
    return cfg.get('post') or {}


def final_title(cfg):
    post = _post(cfg)
    return post.get('title') or suggest_title(post, post.get('title'))


def build_description(cfg, hashtags):
    d, post, a = RULES['description'], _post(cfg), cfg.get('audio') or {}
    hook = (post.get('hook') or d['default_hook']).strip().splitlines()[0]
    lines = [hook, '', d['credits_header']]
    for c in sorted(cfg['clips'], key=lambda c: c.get('rank', 0)):
        cr = clip_credit(c)
        who = f"{cr['name']} (@{cr['handle']})" if cr['handle'] else cr['name']
        lines.append(f"#{c['rank']} {c.get('name', '')}: {who} {cr['url']}".rstrip())
    lines.append('')
    m = a.get('music_meta') or {}
    if m:
        lines.append(f'🎵 Music: "{m.get("title")}" by {m.get("artist")}, from {m.get("source")}, used under the {m.get("license")}')
        if m.get('url'):
            lines.append(m['url'])
        if m.get('license_url'):
            lines.append(f'License: {m["license_url"]}')
    s = a.get('sfx_meta') or {}
    if s:
        lines.append(f'🔊 Sound effect: "{s.get("title")}", from {s.get("source")}, used under the {s.get("license")}')
        if s.get('url'):
            lines.append(s['url'])
    lines += ['', d['subscribe_line'], '', ' '.join(hashtags)]
    return '\n'.join(lines).strip() + '\n'


def _context_terms(cfg):
    post = _post(cfg)
    terms = list(post.get('niche_terms') or [])
    if not terms:
        terms = title_words(final_title(cfg)) + [w for c in cfg['clips'] for w in (c.get('name') or '').split()]
        terms += [post.get('subject') or '', post.get('topic') or '']
    return terms


def check_post(cfg):
    post, r = _post(cfg), Report()
    title = final_title(cfg)
    if not post.get('title'):
        r.note(f'post.title não definido; título gerado: {title}')
    tr = validate_title(title, post.get('main_keyword'))
    if tr.warnings or tr.errors:
        tr.warn(f'título sugerido (cumpre a regra): {suggest_title(post, title)}')
    r.merge(tr)
    hook = post.get('hook') or RULES['description']['default_hook']
    if RULES['description']['require_question_hook'] and '?' not in hook:
        r.warn('o gancho da descrição (post.hook) precisa ser uma pergunta para o público')
    _, hr = clean_hashtags(post.get('hashtags'), _context_terms(cfg))
    return r.merge(hr)


def preflight(cfg):
    """roda antes de renderizar: post, clipes e música (erro de música aborta o build)"""
    return Report().merge(check_post(cfg)).merge(check_clips(cfg['clips'])).merge(check_music(cfg.get('audio')))


# ------------------------------------------------------------------ verificação do export + checklist
def autocheck_export(video):
    lines, problems = [], []
    if not video or not os.path.exists(video):
        return [f'vídeo não encontrado: {video}'], ['vídeo não encontrado']
    pr = json.loads(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'stream=codec_type,width,height,r_frame_rate',
                                    '-show_entries', 'format=duration', '-of', 'json', video],
                                   capture_output=True, text=True).stdout or '{}')
    vs = [s for s in pr.get('streams', []) if s.get('codec_type') == 'video']
    has_audio = any(s.get('codec_type') == 'audio' for s in pr.get('streams', []))
    dur = float(pr.get('format', {}).get('duration', 0))
    if vs:
        num, den = (vs[0].get('r_frame_rate') or '0/1').split('/')
        lines.append(f'Duração {dur:.1f} s | {vs[0].get("width")}x{vs[0].get("height")} | {float(num) / float(den or 1):.0f} fps')
    blk = subprocess.run(['ffmpeg', '-hide_banner', '-i', video, '-vf', 'blackdetect=d=0.5:pix_th=0.10', '-an', '-f', 'null', '-'],
                         capture_output=True, text=True).stderr
    blacks = re.findall(r'black_start:([\d.]+) black_end:([\d.]+)', blk)
    if blacks:
        problems.append('tela preta')
        lines.append('Tela preta: ' + ', '.join(f'{float(a):.1f}–{float(b):.1f} s' for a, b in blacks))
    else:
        lines.append('Tela preta: nenhum trecho de 0,5 s ou mais')
    if not has_audio:
        problems.append('sem áudio')
        lines.append('Áudio: NENHUMA faixa de áudio')
        return lines, problems
    au = subprocess.run(['ffmpeg', '-hide_banner', '-i', video, '-af', 'silencedetect=noise=-45dB:d=1,ebur128=peak=true',
                         '-vn', '-f', 'null', '-'], capture_output=True, text=True).stderr
    sil = re.findall(r'silence_start: ([\d.]+)', au)
    summ = au[au.rfind('Summary:'):] if 'Summary:' in au else ''
    I = re.search(r'I:\s+(-?[\d.]+) LUFS', summ)
    tp = re.search(r'Peak:\s+(-?[\d.]+) dBFS', summ)
    lines.append(f'Áudio: {I.group(1) if I else "?"} LUFS, pico {tp.group(1) if tp else "?"} dBTP, '
                 + ('silêncio ≥1 s em ' + ', '.join(f'{float(s):.1f} s' for s in sil) if sil else 'sem silêncio de 1 s ou mais'))
    if sil:
        problems.append('silêncio no áudio')
    if I and abs(float(I.group(1)) - (-14)) > 1.5:
        problems.append('loudness fora de -14 LUFS')
    if tp and float(tp.group(1)) > -1.0:
        problems.append(f'pico de {tp.group(1)} dBTP no arquivo final (acima de -1 dBTP; baixe audio.true_peak no config)')
    return lines, problems


def write_checklist(path, video, report, auto_lines, auto_problems):
    now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
    out = [f'CHECKLIST DE POSTAGEM: {RULES["channel"]}', f'Vídeo: {os.path.basename(video or "")}   (gerado em {now})', '',
           'Verificação automática do export (confira assistindo mesmo assim):']
    out += [f'  - {l}' for l in auto_lines]
    out.append('  => ' + ('ATENÇÃO: ' + ', '.join(auto_problems) if auto_problems else 'nada de errado encontrado'))
    if report.errors or report.warnings:
        out += ['', 'Avisos do gerador:'] + [f'  - ERRO: {m}' for m in report.errors] + [f'  - {m}' for m in report.warnings]
    out += ['', 'Antes de publicar:'] + [f'[ ] {i}. {item}' for i, item in enumerate(RULES['checklist'], 1)]
    open(path, 'w', encoding='utf-8').write('\n'.join(out) + '\n')


def write_outputs(cfg, video):
    """escreve post.txt e checklist.txt na pasta do vídeo; devolve (post_path, checklist_path, report)"""
    rep = preflight(cfg)
    post = _post(cfg)
    hashtags, _ = clean_hashtags(post.get('hashtags'), _context_terms(cfg))
    title = final_title(cfg)
    folder = os.path.dirname(os.path.abspath(video))
    post_path, chk_path = os.path.join(folder, 'post.txt'), os.path.join(folder, 'checklist.txt')
    open(post_path, 'w', encoding='utf-8').write(
        f'TITLE ({len(title_words(title))} words)\n{title}\n\nDESCRIPTION\n{build_description(cfg, hashtags)}')
    auto_lines, auto_problems = autocheck_export(video)
    write_checklist(chk_path, video, rep, auto_lines, auto_problems)
    return post_path, chk_path, rep


if __name__ == '__main__':
    cfg = json.load(open(sys.argv[1], encoding='utf-8'))
    rep = preflight(cfg)
    rep.print()
    if '--check' not in sys.argv:
        video = sys.argv[sys.argv.index('--video') + 1] if '--video' in sys.argv else cfg.get('output')
        p, c, _ = write_outputs(cfg, video)
        print(f'[post_kit] escrito: {p}\n[post_kit] escrito: {c}')
    sys.exit(1 if rep.errors else 0)
