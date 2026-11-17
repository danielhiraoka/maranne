"""Converte fotos .HEIC/.HEIF (iPhone) para .JPG.

Uso:
    python heic_para_jpg.py                      abre a caixa para escolher as fotos
    python heic_para_jpg.py <pasta ou arquivo>   sem caixa (várias pastas/arquivos, com subpastas)
    python heic_para_jpg.py --teste

Os .jpg vão para a subpasta "jpg", criada dentro da pasta onde as fotos estão.
O original NÃO é apagado, e foto que já tem .jpg lá é pulada (pode repetir).
"""

import io
import subprocess
import sys
import tempfile
from pathlib import Path

from PIL import Image, ImageCms
from pillow_heif import register_heif_opener

register_heif_opener()
EXTENSOES = {".heic", ".heif"}
QUALIDADE = 92
PASTA = "jpg"

# sem "of type": o filtro por extensão deixava as fotos cinza, sem poder escolher
APPLESCRIPT = """set saida to ""
repeat with f in (choose file with prompt "Escolha as fotos HEIC" with multiple selections allowed)
    set saida to saida & POSIX path of f & linefeed
end repeat
return saida"""


def escolher_fotos():
    """Abre a caixa do sistema para escolher várias fotos; lista vazia se cancelar."""
    if sys.platform == "darwin":  # o Python do Homebrew vem sem tkinter; o osascript já vem no Mac
        r = subprocess.run(["osascript", "-e", APPLESCRIPT], capture_output=True, text=True)
        return [Path(linha) for linha in r.stdout.splitlines() if linha]
    from tkinter import Tk, filedialog
    Tk().withdraw()
    return [Path(f) for f in filedialog.askopenfilenames(
        title="Escolha as fotos HEIC", filetypes=[("Fotos HEIC", "*.heic *.heif")])]


def converter(origem):
    """Grava o .jpg em <pasta da foto>/jpg/; devolve o caminho, ou None se já existia."""
    destino = origem.parent / PASTA / (origem.stem + ".jpg")
    if destino.exists():
        return None
    destino.parent.mkdir(exist_ok=True)
    try:
        with Image.open(origem) as img:
            icc = img.info.get("icc_profile")
            img = img.convert("RGB")
            if icc:  # iPhone grava em Display P3; loja que ignora o perfil mostra a cor lavada
                img = ImageCms.profileToProfile(img, ImageCms.ImageCmsProfile(io.BytesIO(icc)),
                                                ImageCms.createProfile("sRGB"))
            # sem EXIF de propósito: a foto do celular leva o GPS de onde foi tirada
            img.save(destino, "JPEG", quality=QUALIDADE)
    except BaseException:
        destino.unlink(missing_ok=True)  # .jpg pela metade seria pulado na próxima rodada
        raise
    return destino


def fotos_de(caminho):
    if not caminho.is_dir():
        return [caminho]
    return sorted(f for f in caminho.rglob("*")
                  if f.suffix.lower() in EXTENSOES and not f.name.startswith("."))


def teste():
    with tempfile.TemporaryDirectory() as tmp:
        pasta = Path(tmp) / "cor"
        pasta.mkdir()
        heic = pasta / "IMG_0001.HEIC"
        Image.new("RGB", (40, 60), (200, 30, 30)).save(heic, format="HEIF")
        assert fotos_de(Path(tmp)) == [heic]
        jpg = converter(heic)
        assert jpg == pasta / "jpg" / "IMG_0001.jpg" and heic.exists(), "o original tem de ficar"
        with Image.open(jpg) as img:
            assert img.format == "JPEG" and img.size == (40, 60)
            r, g, b = img.getpixel((20, 30))
            assert r > 180 and g < 60 and b < 60, (r, g, b)
        assert converter(heic) is None, "segunda rodada tem de pular"
    print("ok  teste passou")


def main():
    if sys.argv[1:2] in (["-h"], ["--help"]):
        sys.exit(__doc__)
    if sys.argv[1:2] == ["--teste"]:
        return teste()
    caminhos = [Path(a) for a in sys.argv[1:]] or escolher_fotos()
    if not caminhos:
        sys.exit("nenhuma foto escolhida")
    for c in caminhos:
        if not c.exists():
            sys.exit(f"não existe: {c}")

    feitas, puladas, erros, pastas = 0, 0, [], set()
    for foto in [f for c in caminhos for f in fotos_de(c)]:
        try:
            destino = converter(foto)
            if destino:
                feitas += 1
                pastas.add(destino.parent)
            else:
                puladas += 1
        except Exception as e:  # uma foto ruim não para o lote
            erros.append(f"{foto}: {e}")
    print(f"{feitas} convertida(s), {puladas} pulada(s) (já tinham .jpg), {len(erros)} com erro")
    for p in sorted(pastas):
        print(f"-> {p}")
    for e in erros:
        print(f"⚠️ {e}")
    if erros:
        sys.exit(1)


if __name__ == "__main__":
    main()
