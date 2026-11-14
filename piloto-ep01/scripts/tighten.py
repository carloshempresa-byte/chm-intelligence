"""Remove silêncios longos entre frases (estilo reel, sem respiro) e reajusta os tempos das palavras."""
import json, subprocess, sys
src, out = sys.argv[1], sys.argv[2]           # audio/narracao  audio/narracao_tight
MAXGAP = 0.22
w = json.load(open(src + ".json"))
subprocess.run(["ffmpeg","-y","-loglevel","error","-i",src+".mp3","-ar","48000","-ac","1",src+".wav"],check=True)
# segmentos de fala: corta no meio de cada pausa maior que MAXGAP
cuts = []  # (start_cut, end_cut) intervalos a remover
for a, b in zip(w, w[1:]):
    gap = b["t0"] - a["t1"]
    if gap > MAXGAP:
        cuts.append((a["t1"] + 0.08, b["t0"] - (MAXGAP - 0.08)))
keep, t = [], 0.0
for c0, c1 in cuts:
    keep.append((t, c0)); t = c1
keep.append((t, w[-1]["t1"] + 0.4))
filt = "".join(f"[0:a]atrim={a:.3f}:{b:.3f},asetpts=PTS-STARTPTS,afade=t=in:d=0.01,afade=t=out:st={b-a-0.012:.3f}:d=0.012[s{i}];" for i,(a,b) in enumerate(keep))
filt += "".join(f"[s{i}]" for i in range(len(keep))) + f"concat=n={len(keep)}:v=0:a=1[o]"
subprocess.run(["ffmpeg","-y","-loglevel","error","-i",src+".wav","-filter_complex",filt,"-map","[o]",out+".wav"],check=True)
def remap(x):
    shift = 0.0
    for c0, c1 in cuts:
        if x >= c1: shift += c1 - c0
    return x - shift
for x in w: x["t0"], x["t1"] = round(remap(x["t0"]),3), round(remap(x["t1"]),3)
json.dump(w, open(out + ".json","w",encoding="utf-8"), ensure_ascii=False, indent=0)
print("cortes:", len(cuts), "nova duração:", round(w[-1]["t1"],2))
