"""Monta os links das fotos do Drive para o Bling, por cor, a partir do fotos.json.

Uso:
    python links_bling.py cadastros/<pasta>/fotos.json

fotos.json (o agente grava depois de subir/copiar as fotos para unitario/):
    {"fotos": {"azul-01.jpg": "<id do arquivo no Drive>", "azul-02.jpg": "...", ...}}

Saída (imprime e grava links_bling.json ao lado):
    {"pai": [{"link": ...}, ...],                 # todas, cor por cor, 01 = capa
     "por_cor": {"azul": [{"link": ...}, ...]}}   # para cada variação daquela cor

Formato do link: https://lh3.googleusercontent.com/d/<id>=s0
- endereço diferente por foto: com drive.google.com/uc?...&id=... o Bling guarda só 1;
- =s0 entrega a resolução cheia (sem ele a foto vem reduzida).
Testado em 17/11/2026.
"""

import argparse
import json
import re
from pathlib import Path


def link(file_id):
    return {"link": f"https://lh3.googleusercontent.com/d/{file_id}=s0"}


def montar(fotos):
    por_cor = {}
    for nome in sorted(fotos):
        m = re.match(r"(.+)-(\d+)\.\w+$", nome)
        if not m:
            raise SystemExit(f"Nome fora do padrão cor-01.jpg: {nome}")
        por_cor.setdefault(m.group(1), []).append((int(m.group(2)), fotos[nome]))
    por_cor = {cor: [link(i) for _, i in sorted(lista)] for cor, lista in por_cor.items()}
    return {"pai": [l for lista in por_cor.values() for l in lista], "por_cor": por_cor}


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("fotos_json")
    args = p.parse_args()

    caminho = Path(args.fotos_json)
    resultado = montar(json.loads(caminho.read_text(encoding="utf-8"))["fotos"])
    (caminho.parent / "links_bling.json").write_text(json.dumps(resultado, indent=1), encoding="utf-8")
    for cor, lista in resultado["por_cor"].items():
        print(f"{cor}: {len(lista)} foto(s)")
    print(f"pai: {len(resultado['pai'])} foto(s) -> {caminho.parent / 'links_bling.json'}")


if __name__ == "__main__":
    main()
