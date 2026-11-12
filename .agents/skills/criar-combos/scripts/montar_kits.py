"""Monta fotos de kits a partir de fotos individuais de peças.

Uso:
    python montar_kits.py --entrada entrada --saida saida --tamanho 2

Para cada combinação de N peças (C(total, N)), remove o fundo de cada foto,
recorta a modelo e sobrepõe as modelos lado a lado num fundo branco 3:4
(960x1280, formato da Bagy), no estilo dos kits de referência.
As fotos são lidas em ordem alfabética; em cada kit, a primeira peça fica
na posição da frente.
"""

import argparse
import itertools
from pathlib import Path

import cv2
import numpy as np
from PIL import Image
from pymatting import estimate_foreground_ml
from rembg import new_session, remove

EXTENSOES = {".jpg", ".jpeg", ".png", ".webp"}

# Regras por tamanho de kit, medidas nos kits de referência (pasta referencia/ desta skill):
#   centros: centro do rosto de cada posição (fração da largura)
#   profundidade: 0 = mais à frente; quem tem o mesmo valor, o da direita cobre
#   rosto: lado do rosto da modelo da frente (fração da ALTURA da tela)
#   topo: topo do rosto da modelo da frente (fração da altura)
#   recuo: quanto cada nível de profundidade encolhe e desce (dá perspectiva)
# Os rostos quase não diminuem com mais peças: as modelos se sobrepõem mais e
# as das pontas podem sair parcialmente da foto.
LAYOUTS = {
    2: {"centros": [0.334, 0.648], "profundidade": [0, 1], "rosto": 0.160, "topo": 0.062, "recuo": 0.0},
    3: {"centros": [0.196, 0.487, 0.787], "profundidade": [1, 0, 1], "rosto": 0.154, "topo": 0.058, "recuo": 0.0},
    4: {"centros": [0.19, 0.40, 0.61, 0.81], "profundidade": [1, 0, 0, 1], "rosto": 0.150, "topo": 0.056, "recuo": 0.02},
    5: {"centros": [0.203, 0.351, 0.505, 0.650, 0.805], "profundidade": [2, 1, 0, 1, 2],
        "rosto": 0.147, "topo": 0.052, "recuo": 0.03},
    6: {"centros": [0.17, 0.30, 0.435, 0.565, 0.70, 0.83], "profundidade": [2, 1, 0, 0, 1, 2],
        "rosto": 0.142, "topo": 0.052, "recuo": 0.03},
}


def recortar(caminho: Path, sessao, cache: Path) -> Image.Image:
    """Remove o fundo e devolve a modelo em RGBA (com cache em disco)."""
    destino = cache / f"{caminho.stem}.png"
    if destino.exists():
        return Image.open(destino).convert("RGBA")
    img = Image.open(caminho).convert("RGB")
    # Máscara suave (sem post_process_mask, que endurece a borda e serrilha
    # o cabelo).
    alfa = np.asarray(remove(img, session=sessao, only_mask=True), dtype=np.float64) / 255
    # Fios semitransparentes ainda carregam a cor do fundo original e viram
    # halo claro sobre a outra modelo; estima a cor real do primeiro plano.
    rgb = np.asarray(img, dtype=np.float64) / 255
    frente = estimate_foreground_ml(rgb, alfa)
    rgba = np.dstack([frente, alfa]).clip(0, 1)
    recorte = Image.fromarray((rgba * 255).round().astype(np.uint8), "RGBA")
    recorte.save(destino)
    return recorte


DETECTOR_ROSTO = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")


def rosto(recorte: Image.Image):
    """Caixa do rosto (x, y, lado) da modelo: a detecção mais alta da foto."""
    cinza = np.asarray(recorte.convert("L"))
    achados = DETECTOR_ROSTO.detectMultiScale(cinza, 1.1, 5, minSize=(60, 60))
    # O detector às vezes acha "rostos" em dobras da calça ou nos sapatos;
    # o rosto de verdade é sempre o mais alto e fica na metade de cima.
    achados = [r for r in achados if r[1] < recorte.height * 0.5]
    if achados:
        x, y, w, h = min(achados, key=lambda r: r[1])
        return float(x), float(y), float(w)
    # Sem rosto detectado: estima pela silhueta (topo da cabeça e centro).
    alfa = np.asarray(recorte.getchannel("A")) > 128
    topo = int(np.where(alfa.any(axis=1))[0][0])
    faixa = alfa[topo : topo + int(recorte.height * 0.12)]
    centro = float(np.where(faixa.any(axis=0))[0].mean())
    lado = recorte.width * 0.2
    return centro - lado / 2, topo + lado * 0.35, lado


def layout_para(n):
    if n in LAYOUTS:
        return LAYOUTS[n]
    meio = (n - 1) / 2
    return {
        "centros": list(np.linspace(0.15, 0.85, n)),
        "profundidade": [int(abs(i - meio) + 0.5) for i in range(n)],
        "rosto": 0.14, "topo": 0.052, "recuo": 0.03,
    }


def desvanecer_base(img: Image.Image, faixa: float = 0.18) -> Image.Image:
    """Faz a parte de baixo da modelo sumir aos poucos no fundo."""
    alfa = np.asarray(img.getchannel("A"), dtype=np.float64)
    altura_faixa = int(img.height * faixa)
    rampa = np.linspace(1, 0, altura_faixa) ** 1.5
    alfa[-altura_faixa:] *= rampa[:, None]
    img = img.copy()
    img.putalpha(Image.fromarray(alfa.round().astype(np.uint8)))
    return img


def montar_kit(recortes, largura=960, altura=1280, fundo=(255, 255, 255), base="ampliar"):
    """Sobrepõe as modelos. A primeira peça vai na posição da frente.

    base: o que fazer quando a foto termina antes da borda de baixo da tela
      "ampliar"    aumenta todas as modelos até o corpo chegar embaixo
      "desvanecer" mantém o tamanho da referência e some a base no branco
    """
    n = len(recortes)
    layout = layout_para(n)
    tela = Image.new("RGBA", (largura, altura), fundo + (255,))

    # Posições da frente para trás; a 1ª peça fica na frente, e assim por diante.
    posicoes = sorted(range(n), key=lambda p: (layout["profundidade"][p], abs(layout["centros"][p] - 0.5)))

    rostos = [rosto(r) for r in recortes]
    planos = []
    for recorte, (fx, fy, fw), pos in zip(recortes, rostos, posicoes):
        nivel = layout["profundidade"][pos]
        lado = altura * layout["rosto"] * (1 - layout["recuo"] * nivel)
        topo = altura * (layout["topo"] + layout["recuo"] * 0.35 * nivel)
        planos.append([recorte, fx, fy, fw, pos, nivel, lado / fw, topo])

    fator = 1.0
    if base == "ampliar":
        # Aumenta todas na mesma proporção até a que termina mais cedo
        # chegar na borda de baixo (rostos continuam do mesmo tamanho).
        fator = max(1.0, *((altura - t) / ((r.height - fy) * s) for r, _, fy, _, _, _, s, t in planos))

    camadas = []
    for recorte, fx, fy, fw, pos, nivel, escala, topo in planos:
        escala *= fator
        novo = recorte.resize(
            (round(recorte.width * escala), round(recorte.height * escala)),
            Image.LANCZOS,
        )
        x = round(layout["centros"][pos] * largura - (fx + fw / 2) * escala)
        y = round(topo - fy * escala)
        if y + novo.height < altura:
            novo = desvanecer_base(novo)
        camadas.append((nivel, pos, novo, x, y))

    # Desenha de trás para frente; no mesmo nível, o da direita por cima.
    for _, _, img, x, y in sorted(camadas, key=lambda c: (-c[0], c[1])):
        tela.paste(img, (x, y), img)
    return tela.convert("RGB")


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--entrada", default="entrada", help="pasta com as fotos individuais")
    p.add_argument("--saida", default="saida", help="pasta onde salvar os kits")
    p.add_argument("--tamanho", type=int, default=2, help="peças por kit (2, 3...)")
    p.add_argument("--modelo", default="birefnet-portrait", help="modelo do rembg")
    p.add_argument("--largura", type=int, default=960, help="padrão 3:4 (Bagy)")
    p.add_argument("--altura", type=int, default=1280)
    p.add_argument("--base", choices=["ampliar", "desvanecer"], default="ampliar",
                   help="quando a foto termina antes da borda de baixo")
    p.add_argument("--ordem", help="monta só este kit, nesta ordem (nomes sem extensão separados por vírgula; "
                                   "o primeiro fica na frente). Ex.: 2_regata_preta,1_regata_branca")
    args = p.parse_args()

    entrada, saida = Path(args.entrada), Path(args.saida)
    cache = saida / "_recortes"
    cache.mkdir(parents=True, exist_ok=True)

    fotos = sorted(f for f in entrada.iterdir() if f.suffix.lower() in EXTENSOES)
    if args.ordem:
        por_nome = {f.stem: f for f in fotos}
        nomes = [n.strip() for n in args.ordem.split(",")]
        faltando = [n for n in nomes if n not in por_nome]
        if faltando:
            raise SystemExit(f"Não achei em {entrada}: {', '.join(faltando)}")
        fotos = [por_nome[n] for n in nomes]
        combinacoes = [tuple(fotos)]
    elif len(fotos) < args.tamanho:
        raise SystemExit(f"Preciso de pelo menos {args.tamanho} fotos em {entrada}, achei {len(fotos)}.")
    else:
        combinacoes = list(itertools.combinations(fotos, args.tamanho))
    print(f"{len(fotos)} peças, kits de {args.tamanho} -> {len(combinacoes)} kit(s)")

    sessao = new_session(args.modelo)
    recortes = {f: recortar(f, sessao, cache) for f in fotos}

    for combo in combinacoes:
        nome = "kit_" + "+".join(f.stem for f in combo) + ".jpg"
        kit = montar_kit([recortes[f] for f in combo], args.largura, args.altura, base=args.base)
        kit.save(saida / nome, quality=92)
        print("  ->", saida / nome)


if __name__ == "__main__":
    main()
