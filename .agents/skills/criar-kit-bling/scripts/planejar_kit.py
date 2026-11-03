"""Planeja um kit de N peças no Bling a partir das variações (cor x tamanho) de um produto.

Uso:
    python planejar_kit.py entrada.json --saida <pasta> [--origem <getProduct do produto pai>]

--origem: arquivo com a resposta do getProduct do PRODUTO PAI de origem (o MCP salva
em arquivo quando a resposta é grande). Dele saem, sem passar pelo agente: id e estoque
de cada cor/tamanho, dados fiscais e de catálogo, e a descrição. Sem --origem, informe
"pecas" e "copiar" no entrada.json.

Gera na pasta de saída:
    plano.md      tabela para o usuário aprovar
    body.json     corpo pronto para a ferramenta createProduct do MCP do Bling
    origem.json   (com --origem) só os dados usados, para registro

Padrão Maranne (igual ao 19312PlusSizeKit2):
    produto pai   <base>Kit<N>                    formato V
    variação      <base>Kit<N><combo><tamanho>    formato E, estoque virtual
    nome variação Cor:Kit<N><combo>;Tamanho:<tamanho>
    descrição     a da peça + bloco "COMPOSIÇÃO DO KIT" (Kit21: 1x Preto, 1x Rosa...)

entrada.json mínimo (com --origem):
{
  "base": "2209121", "nome": "KIT - 2 BABY DOLL BUBLE FEMININO",
  "pecas_por_kit": 2, "preco": 119.9, "situacao": "I",
  "cores": ["Offwhite", "Preto", "Rosa"],   # ordem define Kit21, Kit22...
  "tamanhos": ["P", "M", "G", "GG"],
  "repetir_cor": false                      # regra Maranne: false; true (2x Preto) só se pedirem
}
"""

import argparse
import itertools
import json
import re
from collections import Counter
from html.parser import HTMLParser
from pathlib import Path

CAMPOS_COPIADOS = ("categoria", "marca", "unidade", "pesoBruto", "pesoLiquido", "dimensoes",
                   "camposCustomizados", "descricaoCurta")
MARCADORES_DESCRICAO = ("DETALHES DO TECIDO", "ESTAMPA", "SUGESTÃO DE TAMANHOS", "MEDIDAS", "ATENÇÃO")


def ler_origem(caminho):
    """Lê a resposta do getProduct (JSON puro ou com texto antes/depois)."""
    raw = Path(caminho).read_text(encoding="utf-8")
    dados = json.loads(raw[raw.index("{"):raw.rindex("}") + 1])
    if "pecas" in dados:  # origem.json gerado por uma rodada anterior
        return dados["pecas"], dados["copiar"]
    pai = dados["data"]
    pecas = {}
    for v in pai.get("variacoes", []):
        atributos = dict(p.split(":", 1) for p in v["variacao"]["nome"].split(";") if ":" in p)
        cor, tam = atributos.get("Cor"), atributos.get("Tamanho")
        if cor and tam:
            pecas.setdefault(cor, {})[tam] = {"id": v["id"], "codigo": v["codigo"],
                                              "estoque": v.get("estoque", {}).get("saldoVirtualTotal", 0)}
    ref = pai["variacoes"][0] if pai.get("variacoes") else pai
    copiar = {k: ref[k] for k in CAMPOS_COPIADOS if ref.get(k) not in (None, "", [], {})}
    copiar["categoria"] = ref["categoria"]["id"]
    if "dimensoes" in copiar:  # o Bling devolve número, mas exige texto na criação
        copiar["dimensoes"]["unidadeMedida"] = str(copiar["dimensoes"].get("unidadeMedida", "1"))
    trib = ref.get("tributacao", {})
    copiar.update({k: trib[k] for k in ("ncm", "cest", "origem") if trib.get(k) not in (None, "")})
    return pecas, copiar


def gtin_valido(gtin):
    """Confere o dígito verificador (GTIN-8/12/13/14)."""
    if not gtin.isdigit() or len(gtin) not in (8, 12, 13, 14):
        return False
    corpo = [int(d) for d in reversed(gtin[:-1])]
    soma = sum(d * (3 if i % 2 == 0 else 1) for i, d in enumerate(corpo))
    return (10 - soma % 10) % 10 == int(gtin[-1])


def bloco_composicao(n, combos):
    linhas = []
    for i, combo in enumerate(combos, start=1):
        itens = ", ".join(f"{q}x {cor}" for cor, q in Counter(combo).items())
        linhas.append(f"Kit{n}{i}: {itens}")
    return ("<p><strong>COMPOSIÇÃO DO KIT:</strong><br />" + "<br />".join(linhas)
            + "<br />*Todas as peças são da mesma numeração.</p>\n")


class _Limpador(HTMLParser):
    """Remove atributos, <span> e <div>; <span> em negrito (font-weight 600+/bold) vira <strong>."""
    MANTER = {"p", "br", "strong", "b", "em", "i", "u", "h1", "h2", "h3", "h4", "h5", "h6", "ul", "ol", "li"}

    def __init__(self):
        super().__init__(convert_charrefs=False)
        self.saida, self.spans = [], []

    def handle_starttag(self, tag, attrs):
        if tag == "span":
            estilo = dict(attrs).get("style") or ""
            negrito = re.search(r"font-weight:\s*(bold|[6-9]00)", estilo) is not None
            self.spans.append(negrito)
            if negrito:
                self.saida.append("<strong>")
        elif tag in self.MANTER:
            self.saida.append("<br />" if tag == "br" else f"<{tag}>")

    def handle_startendtag(self, tag, attrs):
        if tag == "br":
            self.saida.append("<br />")

    def handle_endtag(self, tag):
        if tag == "span":
            if self.spans and self.spans.pop():
                self.saida.append("</strong>")
        elif tag in self.MANTER and tag != "br":
            self.saida.append(f"</{tag}>")

    def handle_data(self, data):
        self.saida.append(data)

    def handle_entityref(self, name):
        self.saida.append(f"&{name};")

    def handle_charref(self, name):
        self.saida.append(f"&#{name};")


def limpar_html(html):
    """Tira estilos inline e marcas do editor (vêm de copiar/colar) mantendo texto, negrito e estrutura.
    Reduz a descrição ~80%, o que importa porque o agente precisa enviá-la inteira."""
    limpador = _Limpador()
    limpador.feed(html)
    html = "".join(limpador.saida)
    html = re.sub(r"<strong>(\s*)</strong>", r"\1", html)
    html = re.sub(r"<p>\s*(?:&nbsp;| )?\s*</p>", "", html)
    return re.sub(r"[ \t]*\r?\n\s*", "\n", html).strip() + "\n"


def inserir_composicao(html, bloco):
    """Põe o bloco antes da primeira seção técnica (DETALHES DO TECIDO, ESTAMPA, MEDIDAS...); se não achar, no fim."""
    posicoes = [html.find(m) for m in MARCADORES_DESCRICAO if m in html]
    if not posicoes:
        return html + bloco
    # recua sobre o que abre a seção ("– ", <strong>, <br />, espaços) até o início dela
    inicio = min(posicoes)
    while True:
        m = re.search(r"(\s|–|-|<strong>|<b>|<br\s*/?>)$", html[:inicio])
        if not m:
            break
        inicio = m.start()
    antes = html[:inicio]
    if re.search(r"<p>\s*$", antes):  # a seção começa um parágrafo: entra antes dele
        corte = antes.rstrip().rfind("<p>")
        return html[:corte] + bloco + html[corte:]
    # a seção está no meio de um parágrafo: fecha o parágrafo, põe o bloco e reabre
    return antes + "</p>\n" + bloco + "<p>" + html[inicio:]


def planejar(cfg, pecas, copiar):
    base, n = cfg["base"], cfg["pecas_por_kit"]
    cores, tamanhos = cfg["cores"], cfg["tamanhos"]

    faltando = [f"{c} {t}" for c in cores for t in tamanhos if t not in pecas.get(c, {})]
    if faltando:
        raise SystemExit("Peças sem cadastro no Bling: " + ", ".join(faltando))
    if any(t[:1].isdigit() for t in tamanhos):
        raise SystemExit("Tamanho começando com número deixaria o código ambíguo (ex.: Kit21 + 0G).")

    gtins = cfg.get("gtins", {})
    invalidos = [g for g in gtins.values() if not gtin_valido(str(g))]
    repetidos = [g for g, q in Counter(gtins.values()).items() if q > 1]
    if invalidos or repetidos:
        raise SystemExit(f"GTIN inválido: {invalidos} / repetido: {repetidos}")

    gerar = itertools.combinations_with_replacement if cfg.get("repetir_cor") else itertools.combinations
    combos = list(gerar(cores, n))
    if not combos:
        raise SystemExit(f"Preciso de pelo menos {n} cores para kits de {n} peças sem repetir cor "
                         "(ou use \"repetir_cor\": true).")

    descricao = copiar.get("descricaoCurta")
    if descricao:
        if cfg.get("limpar_html", True):
            descricao = limpar_html(descricao)
        descricao = inserir_composicao(descricao, bloco_composicao(n, combos))

    campos = {}
    for c in copiar.get("camposCustomizados") or []:  # o Bling repete o campo por vínculo
        campos[c["idCampoCustomizado"]] = {"idCampoCustomizado": c["idCampoCustomizado"], "valor": c["valor"]}

    comuns = {k: v for k, v in {
        "tipo": "P",
        "situacao": cfg.get("situacao", "A"),
        "unidade": copiar.get("unidade", "UN"),
        "marca": copiar.get("marca"),
        "preco": cfg["preco"],
        "itensPorCaixa": n,
        "pesoBruto": round(copiar["pesoBruto"] * n, 3) if "pesoBruto" in copiar else None,
        "pesoLiquido": round(copiar["pesoLiquido"] * n, 3) if "pesoLiquido" in copiar else None,
        "dimensoes": copiar.get("dimensoes"),
        "categoria": {"id": copiar["categoria"]} if "categoria" in copiar else None,
        "camposCustomizados": list(campos.values()) or None,
        "tributacao": {k: copiar[k] for k in ("ncm", "cest", "origem") if k in copiar} or None,
    }.items() if v is not None}

    variacoes, linhas = [], []
    for i, combo in enumerate(combos, start=1):
        rotulo = f"Kit{n}{i}"
        itens = ", ".join(f"{q}x {cor}" for cor, q in Counter(combo).items())
        for t in tamanhos:
            qtd = Counter(combo)
            componentes = [{"produto": {"id": pecas[c][t]["id"]}, "quantidade": q} for c, q in qtd.items()]
            estoque = min(pecas[c][t].get("estoque", 0) // q for c, q in qtd.items())
            variacoes.append({
                **comuns,
                "nome": f"{cfg['nome']} Cor:{rotulo};Tamanho:{t}",
                "codigo": f"{base}{rotulo}{t}",
                "formato": "E",
                "variacao": {"nome": f"Cor:{rotulo};Tamanho:{t}", "ordem": len(variacoes) + 1, "produtoPai": {}},
                "estrutura": {"tipoEstoque": "V", "componentes": componentes},
                **({"gtin": cfg["gtins"][f"{base}{rotulo}{t}"]} if f"{base}{rotulo}{t}" in cfg.get("gtins", {}) else {}),
            })
            linhas.append((rotulo, itens, t, f"{base}{rotulo}{t}", estoque))

    # descrição só no pai: repetida nas variações multiplicaria o tamanho do envio
    body = {**comuns, "nome": cfg["nome"], "codigo": f"{base}Kit{n}", "formato": "V",
            **({"descricaoCurta": descricao} if descricao else {}), "variacoes": variacoes}

    md = [f"# {cfg['nome']}", "",
          f"Produto pai: `{base}Kit{n}` · {len(combos)} combinação(ões) × {len(tamanhos)} tamanho(s) = "
          f"{len(variacoes)} variações · preço R$ {cfg['preco']:.2f} · situação {comuns['situacao']}", "",
          "| Cor (variação) | Peças | Tam. | Código | Estoque estimado |", "|---|---|---|---|---|"]
    md += [f"| {r} | {p} | {t} | `{c}` | {e} |" for r, p, t, c, e in linhas]
    sem = [c for *_, c, e in linhas if e <= 0]
    if sem:
        md += ["", f"⚠️ {len(sem)} variação(ões) nascem sem estoque (alguma peça zerada ou negativa)."]
    md += ["", "Composição na descrição: " + ("sim" if descricao else "NÃO (sem descrição de origem)"),
           "Copiado da peça de origem: " + ", ".join(sorted(copiar)),
           "Não preenchido: GTIN (cada variação precisa do seu) e imagens."]
    return body, "\n".join(md) + "\n"


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("entrada", help="arquivo JSON com a configuração do kit")
    p.add_argument("--saida", required=True, help="pasta onde salvar plano.md e body.json")
    p.add_argument("--origem", help="resposta do getProduct do produto pai de origem")
    args = p.parse_args()

    cfg = json.loads(Path(args.entrada).read_text(encoding="utf-8"))
    saida = Path(args.saida)
    saida.mkdir(parents=True, exist_ok=True)
    if args.origem:
        pecas, copiar = ler_origem(args.origem)
        (saida / "origem.json").write_text(json.dumps({"pecas": pecas, "copiar": copiar}, ensure_ascii=False,
                                                      indent=1), encoding="utf-8")
    else:
        pecas, copiar = cfg["pecas"], cfg.get("copiar", {})

    body, md = planejar(cfg, pecas, copiar)
    (saida / "body.json").write_text(json.dumps(body, ensure_ascii=False, indent=1), encoding="utf-8")
    (saida / "plano.md").write_text(md, encoding="utf-8")
    # todos os SKUs que serão criados, para conferir no Bling antes (listProducts aceita até 100)
    codigos = [body["codigo"]] + [v["codigo"] for v in body["variacoes"]]
    (saida / "codigos.json").write_text(json.dumps(codigos), encoding="utf-8")
    print(md)
    print("SKUs a conferir no Bling:", json.dumps(codigos))
    print(f"-> {saida / 'plano.md'}\n-> {saida / 'body.json'}")


if __name__ == "__main__":
    main()
