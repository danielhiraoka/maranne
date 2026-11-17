#!/bin/sh
# Mac: dois cliques abrem a caixa para escolher as fotos HEIC. Só chama o script da skill converter-heic.
cd "$(dirname "$0")" || exit 1
[ -x .venv/bin/python ] || python3 .agents/configurar.py || exit 1
exec .venv/bin/python .agents/skills/converter-heic/scripts/heic_para_jpg.py
