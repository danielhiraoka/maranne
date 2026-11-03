"""Data e hora de São Paulo (fuso da Maranne) e o arquivo de log do dia.

Uso (Mac: python3 / Windows: py):
    python3 .agents/agora.py
    -> 2026-11-02 23:10  log/2026/11/2026-11-02.md

Use sempre isto para datar registros; nunca estime a hora.
"""

from datetime import datetime, timedelta, timezone

try:
    from zoneinfo import ZoneInfo
    FUSO = ZoneInfo("America/Sao_Paulo")
except Exception:  # Windows sem tzdata: o Brasil não tem horário de verão desde 2019
    FUSO = timezone(timedelta(hours=-3))

agora = datetime.now(FUSO)
print(f"{agora:%Y-%m-%d %H:%M}  log/{agora:%Y/%m/%Y-%m-%d}.md")
