---
name: criar-produto
description: Cadastra um produto NOVO da Maranne no Bling do zero — título, descrição no modelo da Maranne (a partir de fotos, tecido, medidas), preço de custo e de venda, variações cor × tamanho, NCM/CEST de um produto parecido, GTIN da planilha — e, quando o usuário indica a pasta das fotos (no computador, ex.: Downloads, ou no Drive), sobe todas para o Drive (pasta "SKU - Nome" com unitario/kit/promocional/video) e para o Bling, no pai e em cada variação. Use quando pedirem para criar, cadastrar ou subir produto novo, lançamento, peça nova, "vou criar um produto", mesmo sem dizer "skill". Para kits de um produto que já existe, use criar-kit-bling.
---

# Criar produto no Bling

Fluxo conversado: o usuário traz as informações aos poucos, você propõe e
debate (título, descrição), e só cria no Bling com tudo aprovado.
`scripts/planejar_produto.py` monta o produto; `scripts/planejar_fotos.py`
decide o nome de cada foto, que vai para o Google Drive (do computador ou de
outra pasta do Drive) e de lá para o Bling (`scripts/links_bling.py`).

## Padrão Maranne

| O quê | Formato | Exemplo |
|---|---|---|
| Produto pai | `<SKU>`, formato V | `2209121` |
| Variação | `<SKU><Cor><Tamanho>`, formato S | `2209121OffwhiteG`, `2308261PoaPretoM` |
| Nome da variação | `Cor:<Cor>;Tamanho:<Tamanho>` | `Cor:Offwhite;Tamanho:G` |
| Código da cor | sem espaço nem acento; **confirme com o usuário** | "Off White" → `Offwhite`? `OffWhite`? |

## O que coletar (pergunte o que faltar)

1. **SKU** — confira já no início: `listProducts` com `codigos: ["<SKU>"]`,
   `criterio: "5"`, `fields: ["id","codigo"]`. Se existir, pare e avise.
2. **Título** — proponha 2–3 opções no padrão do guia (`{Tipo} Feminina {modelo}
   de {Tecido} com {Detalhe}`, até 120 caracteres, essencial nos 60 primeiros),
   debata e use o aprovado.
3. **Descrição** — siga `guias/descricao-produto.md` (padrão 2026: seções, tom,
   palavras, tecidos, medidas) e preencha `modelo-descricao.html` desta pasta,
   a partir do que o usuário mandar (fotos, tecido, medidas, referências). Mostre o
   texto para aprovação. Não invente medidas nem composição de tecido: pergunte.
4. **Preço de venda e preço de custo** — sempre do usuário (venda é aprovada
   pelo daniel, `pessoas.md`). Pergunte também o **fornecedor**.
5. **Cores e tamanhos** — e o código de cada cor no SKU.
6. **Tipo do produto** (blusa, calça, vestido, pijama…) para achar a referência fiscal.
7. **Fotos** — a pasta onde estão: no **computador** (ex.: `~/Downloads/<pasta>`) ou
   no **Drive** (link). Com a pasta indicada, as fotos vão **sempre** para o Drive e
   para o Bling (passos 6 e 6b), sem pedir de novo. Sem fotos, cria sem e sobe depois.

## Passo a passo

### 1. Referência fiscal (NCM, CEST, categoria, peso, dimensões)
Ache um produto parecido já cadastrado: `listProducts` com `nome: "<tipo>"`
(ex.: "Calça"), `tipo: "C"`, `criterio: "2"`, `fields: ["id","nome","codigo"]`,
e escolha o mais parecido. `getProduct` nele — se a resposta for para um
arquivo, **não leia**: passe o caminho em `--referencia`. Diga ao usuário de
qual produto copiou ("NCM 6204.63.00 da calça 2105xxx — conferir depois").

### 2. GTIN
Mesmo procedimento da skill `criar-kit-bling` (passo 3): planilha GTIN,
primeiros livres depois da última linha com SKU, conferir no Bling, um por
variação. Detalhes e id da planilha em `integracoes.md`.

### 3. Planejar
Pasta de trabalho `cadastros/<AAAA-MM-DD>_<SKU>/` com `entrada.json` (formato
no topo do script) e `descricao.html`. Rode numa linha:

```
<python> .agents/skills/criar-produto/scripts/planejar_produto.py cadastros/<pasta>/entrada.json --saida cadastros/<pasta> --referencia <arquivo do getProduct>
```

`<python>`: `.venv/bin/python` (Mac) ou `.venv\Scripts\python.exe` (Windows).
A data vem de `.agents/agora.py`.

### 4. Conferir SKUs e aprovar
`listProducts` com `codigos` = conteúdo de `codigos.json`, `criterio: "5"`:
tem de voltar vazio. Mostre `plano.md`, título, descrição e o resumo das fotos
(quantas por cor, passo 6.2). **Só crie com OK explícito** — o mesmo OK vale para
subir as fotos ao Drive e compartilhar por link as pastas `unitario`/`kit` (6b); diga
isso ao pedir o OK.

### 5. Criar
1. `createProduct` com `body.json`.
2. **Custo:** para cada variação criada, `createProductSupplier` com
   `produto.id`, `fornecedor.id` (ache com `listContacts`), `precoCusto`,
   `precoCompra` e `padrao: true`.
3. Confira com `listProducts` (`idsProdutos`, `fields` codigo/situacao/preco).
4. Marque os GTINs usados na planilha (coluna B = SKU da variação).

### 6. Fotos no Drive — automático quando houver pasta de fotos
Com a pasta indicada (no computador ou no Drive), faça o passo inteiro **sem
perguntar de novo**, logo depois de criar o produto, e siga direto para o 6b.
A cor vem do **nome da subpasta** (Preto/, Off White/…), de uma **cor citada no
nome do arquivo** ("vermelho frente.jpg") ou de uma **cor no nome da pasta**
("26111703 - Calça … Preta …"); aceita feminino (Preta → Preto) e inglês (black,
white…). Ninguém precisa renomear, e você **não abre as imagens**. Uma pasta por
produto; se forem vários produtos, uma pasta para cada (ex.: `<SKU> - <Nome>`).

1. **Listar** (`listagem.json` em `cadastros/<pasta>/`):
   - **computador:** numa linha
     ```
     <python> .agents/skills/criar-produto/scripts/listar_fotos_locais.py "<pasta das fotos>" --saida cadastros/<pasta>
     ```
     (ignora ocultos e o que não é foto; calcula o hash para o upload). Se avisar
     **HEIC**, converta antes com a skill `converter-heic` e liste a pasta `jpg`.
   - **Drive:** `search_files` com `query: "parentId = '<id da pasta>'"`,
     `excludeContentSnippets: true`, `pageSize: 100` (o id está no link
     `.../folders/<id>`); repita em cada subpasta. Grave
     `[{"id","nome","pasta"}]` (`pasta` = nome da subpasta, ou `""` se solta).
2. **Nomear**, numa linha:
   ```
   <python> .agents/skills/criar-produto/scripts/planejar_fotos.py cadastros/<pasta>/listagem.json --cores <cores do produto> --saida cadastros/<pasta>
   ```
   Gera `copias.json` (`cor-01.jpg`… — a 01 é a capa). Mostre o resumo por cor
   junto do plano (passo 4). Foto sem cor reconhecida: pergunte; não chute nem abra.
3. **Pasta do produto:** em **Maranne(Ensaios)/<ano>/** (ids em `integracoes.md`),
   veja se `<SKU> - <Nome>` já existe (`search_files` com `parentId` do ano e
   `title contains '<SKU>'`). Se não, crie a pasta e as subpastas `unitario`,
   `kit`, `promocional`, `video` com `create_file` (`title`, `parentId`,
   `contentMimeType: "application/vnd.google-apps.folder"`).
4. **Enviar cada foto de `copias.json` para `unitario/`** (todas; pode mandar
   várias chamadas de uma vez):
   - **do computador:** `create_file` com `title` = `para`, `parentId` = id de
     `unitario`, `contentMimeType` = `mime`, `disableConversionToGoogleType: true`
     e `base64Content` = `sha256:<sha256>:<id>` (o `id` é o caminho absoluto). A
     foto não passa pela conversa; o original fica no computador. Confira o
     `fileSize` da resposta (tem de ser o tamanho da foto, não 0).
   - **do Drive:** `copy_file` (`fileId` = `id`, `parentId` = id de `unitario`,
     `title` = `para`). O original fica onde está.
5. Grave `cadastros/<pasta>/fotos.json`:
   `{"pasta_produto": "<id>", "unitario": "<id>", "kit": "<id>", "fotos": {"azul-01.jpg": "<id no Drive>", ...}}`.

Se o conector do Drive não estiver ligado nesta ferramenta, avise (ver
`integracoes.md`) e siga o cadastro sem fotos.

### 6b. Fotos no Bling (pelos links do Drive) — automático, logo após o 6
O Bling **baixa e guarda uma cópia** da foto (vira imagem "interna" no
servidor dele): o link do Drive só precisa funcionar na hora do cadastro.

1. Compartilhe por link **só as pastas `unitario` e `kit`** do produto:
   `share_file` com `fileId` = id da pasta, `permissionId: "anyoneWithLink"`,
   `role: "reader"` (as fotos de dentro herdam). São fotos que irão para a loja
   de qualquer jeito; o resto do Drive continua privado. O OK é o do plano (passo 4);
   compartilhe `kit` só quando tiver foto dentro.
   O conector não consegue desfazer compartilhamento: só manualmente no Drive.
2. Links: rode `<python> .agents/skills/criar-produto/scripts/links_bling.py cadastros/<pasta>/fotos.json`
   → `links_bling.json` com `pai` (todas) e `por_cor`. Formato: `https://lh3.googleusercontent.com/d/<id do arquivo>=s0`
   (resolução cheia). **Não use** `drive.google.com/uc?export=view&id=…`: o Bling
   guarda só 1 foto quando todos os links têm o mesmo endereço (testado em 17/11/2026).
   Sem o `=s0`, a foto vem reduzida. Mandar de novo substitui as fotos, não soma.
3. No `createProduct` (ou `patchProduct` depois):
   - **pai:** `midia.imagens.imagensURL` = `pai` de `links_bling.json` (todas as
     fotos, cor por cor, 01 = capa);
   - **cada variação:** `por_cor[<cor>]` — **todas** as fotos da cor dela.
     (a chave é o começo do nome do arquivo: `preto`, `off-white`.)
   - Produto já criado: `patchProduct` no pai com `midia` **não** passa as fotos às
     variações; faça um `patchProduct` por variação (id dela, só `midia`) — testado.
4. Confira com `getProduct` no pai (traz as variações): conte `midia.imagens.internas`
   de cada um — tem de bater com o nº de fotos da cor. O `imagemURL` do `listProducts`
   só mostra que entrou ao menos uma.

### 7. Registrar
Log do dia (`#sku/<SKU>`), com ids, preços, de onde veio o fiscal e o que
ficou pendente (fotos no Bling, publicar nos canais — aline).

## Limitações conhecidas
- Fotos no Bling: só por link público (passo 6b), no formato `lh3…/d/<id>=s0`. O conector do Drive não remove
  compartilhamento; foto compartilhada por engano tem de ser restringida à mão no Drive.
- O MCP do Bling não exclui produtos: erros se corrigem com `patchProduct`.
