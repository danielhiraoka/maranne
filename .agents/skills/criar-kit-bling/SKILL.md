---
name: criar-kit-bling
description: Cadastra kits/combos da Maranne no Bling (ERP) a partir de um SKU que já tem variações de cor e tamanho — kit de 2, 3, 5 peças com as combinações de cores (Kit21, Kit22, Kit31…), cada tamanho com composição, estoque virtual e descrição com a composição de cada kit. Use quando pedirem para criar, montar ou cadastrar kit, combo ou conjunto de peças no Bling, "kit de 2 da blusa X", "combina as cores em kit", mesmo sem dizer "skill". Para as FOTOS do kit, use a skill criar-combos.
---

# Criar kit no Bling

Cria, numa única chamada `createProduct` do MCP do Bling, um produto-kit com
variações de composição. O script `scripts/planejar_kit.py` faz o trabalho
pesado (combinações, códigos, dados copiados, descrição); você coleta, mostra
o plano, pede aprovação e envia.

## Padrão Maranne (não mude sem o usuário pedir)

Igual ao kit que já existe `19312PlusSizeKit2` (KIT - 2 CAMISETAS PLUS SIZE):

| O quê | Formato | Exemplo (kit de 2 do 2209121) |
|---|---|---|
| SKU base | o SKU do produto pai de origem, como o usuário mandou | `2209121` |
| Produto pai | `<base>Kit<N>` (N = peças: Kit2, Kit3, Kit5), formato V | `2209121Kit2` |
| Variação | `<base>Kit<N><combo><tam>`, formato E | `2209121Kit22P` |
| Nome da variação | `Cor:Kit<N><combo>;Tamanho:<tam>` | `Cor:Kit22;Tamanho:P` |
| Composição | as cores da combinação, no mesmo tamanho | 1x Offwhite P + 1x Preto P |
| Estoque | virtual (calculado pelas peças) | menor saldo ÷ quantidade |
| Descrição | a da peça unitária + bloco **COMPOSIÇÃO DO KIT** antes de DETALHES DO TECIDO (guia: `guias/descricao-produto.md` §4) | `Kit22: 1x Offwhite, 1x Preto` |

`combo` numera as combinações na ordem das cores informadas.

**Regra: não repetir cor.** Cada kit leva cores diferentes: Offwhite, Preto,
Rosa → Kit21 Offwhite+Preto, Kit22 Offwhite+Rosa, Kit23 Preto+Rosa. Só use
`"repetir_cor": true` (kits como "2x Preto") se o usuário pedir explicitamente.

## Antes de tudo: o que é obrigatório perguntar

1. **Preço de venda do kit.** Nunca invente nem calcule sozinho. Mudança de
   preço é aprovada pelo daniel (`pessoas.md`). Sem preço, não crie.
2. Quantas peças por kit (2, 3, 5…).
3. Quais cores entram (padrão: todas) — avise as que estão sem estoque.
4. Ativo ou inativo (padrão: ativo).

## Passo a passo

### 1. Buscar o produto de origem (sem gastar tokens)
- Ache o produto pai: `listProducts` com `codigos: ["<base>"]`,
  `fields: ["id","nome","codigo"]`.
- Confira cedo se o kit já existe: `listProducts` com `codigos: ["<base>Kit<N>"]`.
  Se existir, **pare e avise** — acrescentar combinações num kit existente é
  outro fluxo (patchProduct). A conferência completa (todos os SKUs) é no passo 5.
- `getProduct` no **produto pai** de origem. A resposta é grande e o MCP a
  salva num arquivo — **não leia o arquivo**; passe o caminho para o script
  com `--origem`. Ele extrai ids, estoques, dados fiscais e a descrição.
  (Se a resposta vier inteira na conversa, salve-a num arquivo e passe igual.)
- Se as cores do SKU estiverem em produtos-pai diferentes (acontece, ex.:
  21080402), não use `--origem`: preencha `pecas` e `copiar` no entrada.json
  com `listProducts` (fields enxutos) — veja o formato no topo do script.

### 2. Planejar
Pasta de trabalho: `cadastros/<AAAA-MM-DD>_<base>-kit<N>/`. Escreva
`entrada.json` (formato no topo do script) e rode, numa linha:

```
<python> .agents/skills/criar-kit-bling/scripts/planejar_kit.py cadastros/<pasta>/entrada.json --saida cadastros/<pasta> --origem <arquivo do getProduct>
```

`<python>`: `.venv/bin/python` (Mac) ou `.venv\Scripts\python.exe` (Windows).

A descrição sai com HTML limpo (sem estilos inline do copiar/colar, negritos
mantidos; ~80% menor) e vai **só no produto pai** — repetida nas variações,
o envio ficaria ~16x maior. `"limpar_html": false` mantém o HTML original.

### 3. GTIN
Cada variação precisa de um GTIN (EAN) livre. Fonte: planilha **GTIN** no
Google Drive (conector Google Sheets; id e regras em `integracoes.md`).
Coluna A = EAN, coluna B = SKU que usou.

1. **Ache o ponto de partida:** leia só a coluna B de um trecho no fim
   (ex.: `B3200:B3400`) e pegue a **primeira linha depois da última com SKU**.
   Nunca use EAN de linha em branco *antes* da última usada (há lacunas antigas).
2. **Leia os candidatos:** `A<início>:B<fim>`, um por variação.
3. **Confira no Bling:** `listProducts` com `gtins: [...]`, `criterio: "5"`,
   `fields: ["id","codigo"]` — tem de voltar vazio. Se algum existir, marque
   esse na planilha com o SKU do Bling, avise e pegue o próximo.
4. Coloque em `"gtins": {"<codigo da variação>": "<ean>"}` no entrada.json
   (o script recusa EAN com dígito verificador errado ou repetido).
5. **Só depois de criar o kit** no Bling, escreva os SKUs na coluna B das
   mesmas linhas (`update_values`, um bloco contínuo `B<início>:B<fim>`).
   Releia antes de escrever para garantir que ninguém usou essas linhas.

Sem o conector (cada ferramenta/pessoa conecta o seu — ver `integracoes.md`),
peça os GTINs ao usuário ou crie sem GTIN e avise.

### 4. Aprovar
Mostre o `plano.md` (combinações, códigos, estoque estimado, avisos) e o
bloco de composição. **Só envie com OK explícito** do usuário.

### 5. Criar
**Antes, confira que nenhum SKU existe** (pai + todas as variações): o script
grava a lista em `codigos.json`. `listProducts` com `codigos: <essa lista>`,
`criterio: "5"` (inclui inativos e excluídos), `fields: ["id","codigo"]` —
tem de voltar vazio. Se algum existir, **não crie**: mostre quais e pergunte.

Depois chame `createProduct` com o conteúdo de `body.json` como `body`. Confira
com `listProducts` (`idsProdutos` do pai e das variações; `fields`
codigo/estoque/situacao) se o estoque virtual bateu.

### 6. Registrar
- Log do dia com `#sku/<base>Kit<N>` e `#sku/<base>`, ids criados, preço, situação.
- Linha na página do SKU, se existir.
- Avise o que falta: **fotos** (skill criar-combos; o Bling só aceita imagem
  por link público) e **publicar nos canais** (feito no Bling pela aline).

## Limitações conhecidas
- O Bling **não** copia a descrição do pai para as variações (kits antigos têm
  descrição em cada variação). Ainda em aberto se isso afeta site/marketplaces.
- Com estoque virtual não se envia `lancamentoEstoque` (o Bling ignora e avisa).
- O MCP do Bling não exclui produtos: erros são corrigidos com `patchProduct`
  ou apagados à mão no Bling.
- Kit com mais de 9 combinações gera `Kit210`, `Kit211`… (único, mas menos legível).
