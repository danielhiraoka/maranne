"""Decide o nome de cada foto do ensaio a partir da listagem da pasta no Google Drive.

Uso:
    python planejar_fotos.py listagem.json --cores Preto "Off White" Vermelho --saida <pasta>

listagem.json: arquivos da pasta indicada pelo usuário, como o conector do Drive lista:
    [{"id": "1AbC...", "nome": "IMG_0001.jpg", "pasta": "Preto"},   # dentro da subpasta Preto
     {"id": "1XyZ...", "nome": "vermelho frente.jpg", "pasta": ""}] # solta na pasta indicada

A cor vem, nesta ordem: (1) do nome da subpasta; (2) de uma cor citada no nome do arquivo.
As fotos não são abertas. Gera copias.json com o que copiar no Drive:
    [{"id": "1AbC...", "de": "IMG_0001.jpg", "para": "preto-01.jpg", "cor": "Preto"}, ...]
e lista as fotos sem cor reconhecida (pergunte ao usuário; não chute).
"""

import argparse
import json
import unicodedata
from pathlib import Path

EXTENSOES = {".jpg", ".jpeg", ".png", ".webp", ".heic"}

# nomes gerados por ferramentas (IA, câmera) costumam vir em inglês
SINONIMOS = {
    "preto": ["black"], "branco": ["white"], "offwhite": ["off white", "offwhite", "ivory", "cream"],
    "rosa": ["pink"], "vermelho": ["red"], "azul": ["blue"], "marinho": ["navy"], "verde": ["green"],
    "bege": ["beige"], "marrom": ["brown"], "cinza": ["gray", "grey"], "amarelo": ["yellow"],
    "vinho": ["wine", "burgundy"], "lilas": ["lilac"], "roxo": ["purple"], "laranja": ["orange"],
    "caqui": ["khaki"], "creme": ["cream"], "nude": ["nude"], "terracota": ["terracotta"],
}


def normalizar(texto):
    sem_acento = unicodedata.normalize("NFKD", texto).encode("ascii", "ignore").decode()
    return " ".join(sem_acento.lower().replace("_", " ").replace("-", " ").split())


def cor_do_arquivo(nome, cores):
    """Cor mais longa citada no nome ('poa preto' ganha de 'preto'), em português ou inglês."""
    alvo = f" {normalizar(Path(nome).stem)} "
    achadas = []
    for c in cores:
        termos = [normalizar(c)] + SINONIMOS.get(normalizar(c).replace(" ", ""), [])
        if any(f" {t} " in alvo for t in termos):
            achadas.append(c)
    return max(achadas, key=len) if achadas else None


def planejar(arquivos, cores):
    por_cor, sem_cor = {c: [] for c in cores}, []
    for a in sorted(arquivos, key=lambda a: (normalizar(a.get("pasta", "")), a["nome"].lower())):
        if Path(a["nome"]).suffix.lower() not in EXTENSOES:
            continue
        pasta = a.get("pasta", "")
        cor = next((c for c in cores if normalizar(c) == normalizar(pasta)), None) if pasta else None
        cor = cor or cor_do_arquivo(a["nome"], cores)
        (por_cor[cor] if cor else sem_cor).append(a)

    copias = []
    for cor, lista in por_cor.items():
        for i, a in enumerate(lista, start=1):
            ext = Path(a["nome"]).suffix.lower()
            copias.append({"id": a["id"], "de": a["nome"], "para": f"{'-'.join(normalizar(cor).split())}-{i:02d}{ext}",
                           "cor": cor})
    return copias, sem_cor


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("listagem")
    p.add_argument("--cores", nargs="+", required=True, help="cores do produto, como no Bling")
    p.add_argument("--saida", required=True)
    args = p.parse_args()

    arquivos = json.loads(Path(args.listagem).read_text(encoding="utf-8"))
    copias, sem_cor = planejar(arquivos, args.cores)
    saida = Path(args.saida)
    saida.mkdir(parents=True, exist_ok=True)
    (saida / "copias.json").write_text(json.dumps(copias, ensure_ascii=False, indent=1), encoding="utf-8")

    for cor in args.cores:
        nomes = [c["para"] for c in copias if c["cor"] == cor]
        print(f"{cor}: {len(nomes)} foto(s)" + (f" -> {nomes[0]} … {nomes[-1]}" if nomes else "  ⚠️ nenhuma"))
    if sem_cor:
        print(f"⚠️ {len(sem_cor)} foto(s) sem cor reconhecida: {', '.join(a['nome'] for a in sem_cor[:8])}")
    print(f"-> {saida / 'copias.json'}")


if __name__ == "__main__":
    main()
