#!/bin/bash
# Atualiza piloto-bagger288/progresso.txt e faz commit/push (rodar da raiz do repositório).
cd "$(dirname "$0")/../.."
TOTAL=3331
N=$(find piloto-bagger288/build/frames -name 'f_*.jpg' -size +0 2>/dev/null | wc -l)
PCT=$(python3 -c "print(round(100*$N/$TOTAL,1))")
RESTAM=$(python3 -c "print(round(($TOTAL-$N)*66/3600,1))")
cat > piloto-bagger288/progresso.txt <<TXT
Bagger 288 — render completo (1080x1920, EEVEE, mesma qualidade dos testes_v2)
Atualizado: $(date -u '+%Y-%m-%d %H:%M UTC')
Quadros prontos: $N / $TOTAL ($PCT%)
Estimativa restante: ~$RESTAM h (a ~66 s por quadro), em blocos de 2 h retomáveis
TXT
git add piloto-bagger288/progresso.txt
git commit -qm "Bagger 288: progresso do render $N/$TOTAL ($PCT%)

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_016vtzhyhdkM7m6fLda6PiiV" && for i in 1 2 3 4; do git push -q -u origin claude/trusting-tesla-4iyooz && break; sleep $((2**i)); done
cat piloto-bagger288/progresso.txt
