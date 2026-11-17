"""Lista as fotos de uma pasta do computador para subir ao Google Drive.

Uso:
    python listar_fotos_locais.py "<pasta>" --saida cadastros/<pasta-do-cadastro>

Gera listagem.json no mesmo formato que planejar_fotos.py lê:
    [{"id": "/caminho/absoluto/foto.jpg", "nome": "foto.jpg", "pasta": "Preto",
      "sha256": "...", "mime": "image/jpeg", "kb": 2252}, ...]

- "pasta" = nome da subpasta onde a foto está (a cor costuma vir dela). Foto solta
  na pasta indicada recebe o nome da própria pasta indicada (ex.: "26111701 - Calça
  Wide Leg Azul ..."), de onde planejar_fotos.py tira a cor.
- sha256 e caminho servem para o create_file do conector do Drive
  (base64Content = "sha256:<hash>:<caminho>"), sem a foto passar pela conversa.
- Ignora arquivos ocultos (.DS_Store) e o que não é foto. As fotos não são abertas.
"""

import argparse
import hashlib
import json
from pathlib import Path

MIMES = {".jpg": "image/jpeg", ".jpeg": "image/jpeg", ".png": "image/png",
         ".webp": "image/webp", ".heic": "image/heic", ".heif": "image/heif"}


def sha256(caminho):
    h = hashlib.sha256()
    with open(caminho, "rb") as f:
        for bloco in iter(lambda: f.read(1 << 20), b""):
            h.update(bloco)
    return h.hexdigest()


def listar(raiz):
    raiz = Path(raiz).expanduser().resolve()
    if not raiz.is_dir():
        raise SystemExit(f"Pasta não encontrada: {raiz}")
    fotos = []
    for arq in sorted(raiz.rglob("*")):
        rel = arq.relative_to(raiz)
        if not arq.is_file() or any(p.startswith(".") for p in rel.parts):
            continue
        mime = MIMES.get(arq.suffix.lower())
        if not mime:
            continue
        pasta = rel.parts[-2] if len(rel.parts) > 1 else raiz.name
        fotos.append({"id": arq.as_posix(), "nome": arq.name, "pasta": pasta,
                      "sha256": sha256(arq), "mime": mime, "kb": arq.stat().st_size // 1024})
    return fotos


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("pasta", help="pasta do computador com as fotos (com ou sem subpastas por cor)")
    p.add_argument("--saida", required=True, help="pasta do cadastro onde salvar listagem.json")
    args = p.parse_args()

    fotos = listar(args.pasta)
    saida = Path(args.saida)
    saida.mkdir(parents=True, exist_ok=True)
    (saida / "listagem.json").write_text(json.dumps(fotos, ensure_ascii=False, indent=1), encoding="utf-8")

    por_pasta = {}
    for f in fotos:
        por_pasta.setdefault(f["pasta"], []).append(f)
    for pasta, lista in por_pasta.items():
        print(f"{pasta}: {len(lista)} foto(s), {sum(f['kb'] for f in lista) // 1024} MB")
    heic = [f["nome"] for f in fotos if f["mime"] in ("image/heic", "image/heif")]
    if heic:
        print(f"⚠️ {len(heic)} foto(s) HEIC: converta antes com a skill converter-heic (o Bling não aceita HEIC).")
    if not fotos:
        print("⚠️ Nenhuma foto encontrada.")
    print(f"-> {saida / 'listagem.json'}")


if __name__ == "__main__":
    main()
