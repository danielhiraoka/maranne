"""Planeja um produto novo no Bling: produto pai com variações cor x tamanho.

Uso:
    python planejar_produto.py entrada.json --saida <pasta>

Gera na pasta de saída:
    plano.md      resumo para o usuário aprovar
    body.json     corpo para a ferramenta createProduct do MCP do Bling
    codigos.json  todos os SKUs que serão criados (conferir no Bling antes)

Padrão Maranne (igual ao 2209121):
    produto pai   <SKU>                       formato V
    variação      <SKU><Cor><Tamanho>         formato S   ex.: 2209121OffwhiteG
    nome variação Cor:<Cor>;Tamanho:<Tamanho>

entrada.json:
{
  "sku": "123",
  "nome": "Calça Pantalona Feminina ...",      # título aprovado (máx. 120 caracteres)
  "descricao_arquivo": "descricao.html",       # relativo ao entrada.json
  "preco": 129.9,                              # preço de venda (vem do usuário)
  "situacao": "A",
  "cores": ["Preto", {"nome": "Off White", "codigo": "Offwhite"}],   # codigo = como vai no SKU
  "tamanhos": ["P", "M", "G", "GG"],
  "fiscal": {"categoria": 2381792, "ncm": "6204.63.00", "cest": "28.059.00", "origem": 0,
             "marca": "Maranne", "unidade": "UN", "pesoBruto": 0.3, "pesoLiquido": 0.3,
             "dimensoes": {"altura": 5, "largura": 10, "profundidade": 5, "unidadeMedida": "1"},
             "camposCustomizados": [{"idCampoCustomizado": 715880, "valor": "54884514"}]},
  "gtins": {"123PretoP": "7795792433602", ...}  # opcional
}
"""

import argparse
import json
import unicodedata
from collections import Counter
from pathlib import Path


def codigo_cor(nome):
    sem_acento = unicodedata.normalize("NFKD", nome).encode("ascii", "ignore").decode()
    return "".join(sem_acento.split())


def gtin_valido(gtin):
    """Confere o dígito verificador (GTIN-8/12/13/14)."""
    if not gtin.isdigit() or len(gtin) not in (8, 12, 13, 14):
        return False
    corpo = [int(d) for d in reversed(gtin[:-1])]
    soma = sum(d * (3 if i % 2 == 0 else 1) for i, d in enumerate(corpo))
    return (10 - soma % 10) % 10 == int(gtin[-1])


def ler_referencia(caminho):
    """Dados fiscais/catálogo de um produto parecido (resposta do getProduct, pai ou variação)."""
    raw = Path(caminho).read_text(encoding="utf-8")
    p = json.loads(raw[raw.index("{"):raw.rindex("}") + 1])["data"]
    ref = p["variacoes"][0] if p.get("variacoes") else p
    trib = ref.get("tributacao", {})
    campos = {c["idCampoCustomizado"]: {"idCampoCustomizado": c["idCampoCustomizado"], "valor": c["valor"]}
              for c in ref.get("camposCustomizados") or []}  # o Bling repete o campo por vínculo
    fiscal = {"categoria": ref["categoria"]["id"], "marca": ref.get("marca") or "Maranne",
              "unidade": ref.get("unidade") or "UN", "pesoBruto": ref.get("pesoBruto"),
              "pesoLiquido": ref.get("pesoLiquido"), "camposCustomizados": list(campos.values()),
              **{k: trib[k] for k in ("ncm", "cest", "origem") if trib.get(k) not in (None, "")}}
    if ref.get("dimensoes"):
        fiscal["dimensoes"] = {**ref["dimensoes"], "unidadeMedida": str(ref["dimensoes"].get("unidadeMedida", "1"))}
    vazio = {k for k, v in fiscal.items() if v is None or v == [] or (v == 0 and k != "origem")}
    return {k: v for k, v in fiscal.items() if k not in vazio}, f"{ref['codigo']} ({p['nome']})"


def planejar(cfg, pasta):
    sku, nome = cfg["sku"], cfg["nome"].strip()
    if len(nome) > 120:
        raise SystemExit(f"Título com {len(nome)} caracteres; o Bling aceita até 120.")
    if "preco" not in cfg:
        raise SystemExit("Falta o preço de venda (vem do usuário).")
    tamanhos = cfg["tamanhos"]
    if any(t[:1].isdigit() for t in tamanhos):
        raise SystemExit("Tamanho começando com número deixaria o SKU ambíguo.")
    cores = [c if isinstance(c, dict) else {"nome": c} for c in cfg["cores"]]
    for c in cores:
        c.setdefault("codigo", codigo_cor(c["nome"]))

    gtins = cfg.get("gtins", {})
    invalidos = [g for g in gtins.values() if not gtin_valido(str(g))]
    repetidos = [g for g, q in Counter(gtins.values()).items() if q > 1]
    if invalidos or repetidos:
        raise SystemExit(f"GTIN inválido: {invalidos} / repetido: {repetidos}")

    descricao = None
    if cfg.get("descricao_arquivo"):
        descricao = (pasta / cfg["descricao_arquivo"]).read_text(encoding="utf-8").strip()

    f = cfg.get("fiscal", {})
    comuns = {k: v for k, v in {
        "tipo": "P",
        "situacao": cfg.get("situacao", "A"),
        "unidade": f.get("unidade", "UN"),
        "marca": f.get("marca", "Maranne"),
        "preco": cfg["preco"],
        "pesoBruto": f.get("pesoBruto"),
        "pesoLiquido": f.get("pesoLiquido"),
        "dimensoes": f.get("dimensoes"),
        "categoria": {"id": f["categoria"]} if "categoria" in f else None,
        "camposCustomizados": f.get("camposCustomizados"),
        "tributacao": {k: f[k] for k in ("ncm", "cest", "origem") if k in f} or None,
    }.items() if v is not None}

    variacoes = []
    for c in cores:
        for t in tamanhos:
            codigo = f"{sku}{c['codigo']}{t}"
            variacoes.append({
                **comuns,
                "nome": f"{nome} Cor:{c['nome']};Tamanho:{t}",
                "codigo": codigo,
                "formato": "S",
                "variacao": {"nome": f"Cor:{c['nome']};Tamanho:{t}", "ordem": len(variacoes) + 1,
                             "produtoPai": {}},
                **({"gtin": str(gtins[codigo])} if codigo in gtins else {}),
            })

    body = {**comuns, "nome": nome, "codigo": sku, "formato": "V",
            **({"descricaoCurta": descricao} if descricao else {}), "variacoes": variacoes}

    sem_gtin = [v["codigo"] for v in variacoes if "gtin" not in v]
    md = [f"# {nome}", "",
          f"SKU pai `{sku}` · {len(cores)} cor(es) × {len(tamanhos)} tamanho(s) = {len(variacoes)} variações · "
          f"venda R$ {cfg['preco']:.2f} · situação {comuns['situacao']} · título {len(nome)}/120", "",
          "| Cor | Código da cor | Tamanhos | SKUs |", "|---|---|---|---|"]
    md += [f"| {c['nome']} | {c['codigo']} | {', '.join(tamanhos)} | `{sku}{c['codigo']}{tamanhos[0]}` … "
           f"`{sku}{c['codigo']}{tamanhos[-1]}` |" for c in cores]
    md += ["", "Fiscal/catálogo: " + ", ".join(f"{k}={v}" for k, v in f.items()
                                               if k in ("ncm", "cest", "categoria", "pesoBruto")),
           "Descrição: " + (f"{len(descricao)} caracteres" if descricao else "NÃO informada"),
           "GTIN: " + ("todos preenchidos" if not sem_gtin else f"faltam {len(sem_gtin)}")]
    return body, "\n".join(md) + "\n"


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("entrada", help="arquivo JSON com o produto")
    p.add_argument("--saida", required=True, help="pasta onde salvar plano.md, body.json e codigos.json")
    p.add_argument("--referencia", help="resposta do getProduct de um produto parecido (preenche 'fiscal')")
    args = p.parse_args()

    entrada = Path(args.entrada)
    cfg = json.loads(entrada.read_text(encoding="utf-8"))
    if args.referencia:
        fiscal, origem = ler_referencia(args.referencia)
        cfg["fiscal"] = {**fiscal, **cfg.get("fiscal", {})}  # o que vier no entrada.json prevalece
        print(f"Fiscal copiado de {origem} — conferir depois.")
    body, md = planejar(cfg, entrada.parent)
    saida = Path(args.saida)
    saida.mkdir(parents=True, exist_ok=True)
    codigos = [body["codigo"]] + [v["codigo"] for v in body["variacoes"]]
    (saida / "body.json").write_text(json.dumps(body, ensure_ascii=False, indent=1), encoding="utf-8")
    (saida / "codigos.json").write_text(json.dumps(codigos), encoding="utf-8")
    (saida / "plano.md").write_text(md, encoding="utf-8")
    print(md)
    print("SKUs a conferir no Bling:", json.dumps(codigos))


if __name__ == "__main__":
    main()
