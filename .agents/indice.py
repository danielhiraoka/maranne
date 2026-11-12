#!/usr/bin/env python3
"""Índice do log por etiqueta. Funciona igual em Mac e Windows (não usa grep).

  python3 .agents/indice.py                 lista as etiquetas e quantas entradas cada uma tem
  python3 .agents/indice.py sku/2605084     linha do tempo dessa etiqueta (uma linha por entrada)
  python3 .agents/indice.py sku/2605084 -c  o mesmo, com o texto completo de cada entrada
  python3 .agents/indice.py sku/2605        prefixo também vale (pega 2605084, 2605084Kit2, 2605085...)

No Windows: py .agents/indice.py ...
"""
import re
import sys
from collections import Counter
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
ETIQUETA = re.compile(r"#([a-z]+/[^\s#]+)")


def entradas():
    """Devolve (data, cabeçalho, etiquetas, texto, arquivo, linha) de cada entrada do log."""
    for arq in sorted((RAIZ / "log").rglob("*.md")):
        data = arq.stem
        linhas = arq.read_text(encoding="utf-8").splitlines()
        inicios = [i for i, l in enumerate(linhas) if l.startswith("## ")]
        for n, i in enumerate(inicios):
            fim = inicios[n + 1] if n + 1 < len(inicios) else len(linhas)
            corpo = [l for l in linhas[i + 1:fim] if l.strip()]
            etiquetas, texto = [], []
            for l in corpo:
                if l.startswith("#") and not texto:
                    etiquetas += ETIQUETA.findall(l)
                else:
                    texto.append(l)
            yield data, linhas[i][3:], etiquetas, texto, arq.relative_to(RAIZ).as_posix(), i + 1


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("-")]
    completo = "-c" in sys.argv[1:]
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")

    if not args:
        conta = Counter(e for _, _, ets, _, _, _ in entradas() for e in set(ets))
        tipo_atual = None
        for et, n in sorted(conta.items(), key=lambda x: (x[0].split("/")[0], -x[1], x[0])):
            tipo = et.split("/")[0]
            if tipo != tipo_atual:
                print(f"\n# {tipo}")
                tipo_atual = tipo
            print(f"{n:4d}  #{et}")
        return

    alvo = args[0].lstrip("#").lower()
    achou = 0
    for data, cab, ets, texto, arq, linha in entradas():
        if not any(e.lower().startswith(alvo) for e in ets):
            continue
        achou += 1
        if completo:
            print(f"\n## {data} {cab}  ({arq}:{linha})")
            print("\n".join(texto))
        else:
            resumo = texto[0] if texto else ""
            if len(resumo) > 160:
                resumo = resumo[:157] + "..."
            print(f"{data} {cab} · {resumo}  ({arq}:{linha})")
    if not achou:
        print(f"Nenhuma entrada com a etiqueta #{alvo}. Rode sem argumentos para ver as etiquetas.")


if __name__ == "__main__":
    main()
