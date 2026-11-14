"""Gera narração com edge-tts e salva tempos palavra a palavra (JSON)."""
import asyncio, json, os, ssl, sys, edge_tts, edge_tts.communicate as _ec
# Em ambientes com proxy HTTPS (ex.: nuvem), usa o proxy e o CA do sistema
PROXY = os.environ.get("HTTPS_PROXY") or os.environ.get("https_proxy")
CA = os.environ.get("SSL_CERT_FILE") or ("/root/.ccr/ca-bundle.crt" if os.path.exists("/root/.ccr/ca-bundle.crt") else None)
if CA: _ec._SSL_CTX = ssl.create_default_context(cafile=CA)
VOICE = sys.argv[3] if len(sys.argv) > 3 else "pt-BR-AntonioNeural"
async def main(txt, out):
    text = open(txt, encoding="utf-8").read().strip()
    c = edge_tts.Communicate(text, VOICE, rate="+20%", pitch="+2Hz", boundary="WordBoundary", proxy=PROXY)
    words = []
    with open(out + ".mp3", "wb") as f:
        async for ch in c.stream():
            if ch["type"] == "audio": f.write(ch["data"])
            elif ch["type"] == "WordBoundary":
                words.append({"w": ch["text"], "t0": ch["offset"]/1e7, "t1": (ch["offset"]+ch["duration"])/1e7})
    json.dump(words, open(out + ".json", "w", encoding="utf-8"), ensure_ascii=False, indent=0)
    print(len(words), "palavras, fim em", words[-1]["t1"])
asyncio.run(main(sys.argv[1], sys.argv[2]))
