---
name: criar-produto
description: Cadastra um produto NOVO da Maranne no Bling do zero — título, descrição no modelo da Maranne (a partir de fotos, tecido, medidas), preço de custo e de venda, variações cor × tamanho, NCM/CEST de um produto parecido, GTIN da planilha — e organiza as fotos do ensaio no Drive (pasta "SKU - Nome" com unitario/kit/promocional/video). Use quando pedirem para criar, cadastrar ou subir produto novo, lançamento, peça nova, "vou criar um produto", mesmo sem dizer "skill". Para kits de um produto que já existe, use criar-kit-bling.
---

# Criar produto no Bling

Fluxo conversado: o usuário traz as informações aos poucos, você propõe e
debate (título, descrição), e só cria no Bling com tudo aprovado.
`scripts/planejar_produto.py` monta o produto; `scripts/planejar_fotos.py`
decide o nome de cada foto, que é copiada no próprio Google Drive.

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
7. **Fotos** — só se já existirem; sem fotos, cria sem e sobe depois.

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
tem de voltar vazio. Mostre `plano.md`, título e descrição. **Só crie com OK
explícito.**

### 5. Criar
1. `createProduct` com `body.json`.
2. **Custo:** para cada variação criada, `createProductSupplier` com
   `produto.id`, `fornecedor.id` (ache com `listContacts`), `precoCusto`,
   `precoCompra` e `padrao: true`.
3. Confira com `listProducts` (`idsProdutos`, `fields` codigo/situacao/preco).
4. Marque os GTINs usados na planilha (coluna B = SKU da variação).

### 6. Fotos (se houver) — tudo pelo Google Drive (conector), nunca pelo app do computador
O usuário diz em que **pasta do Drive** estão as fotos (link ou nome). A cor
vem do **nome da subpasta** (Preto/, Branco/…) ou de uma **cor citada no nome
do arquivo** ("vermelho frente.jpg"). Ninguém precisa renomear, e você **não
abre as imagens**.

1. Liste a pasta e as subpastas com o conector do Drive: `search_files` com
   `query: "parentId = '<id da pasta>'"`, `excludeContentSnippets: true`,
   `pageSize: 100` (o id está no link: `.../folders/<id>`). Repita para cada
   subpasta. Salve só o essencial em `cadastros/<pasta>/listagem.json`:
   `[{"id","nome","pasta"}]` (`pasta` = nome da subpasta, ou `""` se solta).
   A cor também é reconhecida em inglês no nome (black, white, pink…), comum
   em fotos geradas por IA.
2. Rode, numa linha:
   ```
   <python> .agents/skills/criar-produto/scripts/planejar_fotos.py cadastros/<pasta>/listagem.json --cores <cores do produto> --saida cadastros/<pasta>
   ```
   Fotos sem cor reconhecida: pergunte a cor; não chute nem abra a foto.
3. Mostre o resumo por cor e peça OK.
4. No Drive, dentro de **Maranne(Ensaios)/<ano>/** (ids em `integracoes.md`),
   veja se `<SKU> - <Nome>` já existe (`search_files` com `parentId` do ano e
   `title contains '<SKU>'`). Se não, crie a pasta e as subpastas `unitario`,
   `kit`, `promocional`, `video` com `create_file` (`title`, `parentId`,
   `contentMimeType: "application/vnd.google-apps.folder"` — testado).
5. Copie cada foto de `copias.json` para `unitario/` com `copy_file`
   (`fileId`, `parentId` = id de `unitario`, `title` = nome novo). A foto não
   passa pela conversa e o original fica onde está.

Se o conector do Drive não estiver ligado nesta ferramenta, avise (ver
`integracoes.md`) e siga o cadastro sem fotos.

### 6b. Fotos no Bling (pelos links do Drive) — testado
O Bling **baixa e guarda uma cópia** da foto (vira imagem "interna" no
servidor dele): o link do Drive só precisa funcionar na hora do cadastro.

1. Compartilhe por link **só as pastas `unitario` e `kit`** do produto:
   `share_file` com `fileId` = id da pasta, `permissionId: "anyoneWithLink"`,
   `role: "reader"` (as fotos de dentro herdam). São fotos que irão para a loja
   de qualquer jeito; o resto do Drive continua privado. **Peça OK antes.**
   O conector não consegue desfazer compartilhamento: só manualmente no Drive.
2. Link de cada foto: `https://drive.google.com/uc?export=view&id=<id do arquivo>`
   (devolve a foto original; o link `/view` abre página, não serve).
3. No `createProduct` (ou `patchProduct` depois):
   - **pai:** `midia.imagens.imagensURL` com todas as fotos de `unitario`, na
     ordem cor por cor (`preto-01` primeiro = capa);
   - **cada variação:** só as fotos da cor dela (`123PretoP` ← `preto-01`, `preto-02`…).
4. Confira barato: `listProducts` com `fields: ["codigo","imagemURL"]` —
   vem preenchido quando a foto entrou.

### 7. Registrar
Log do dia (`#sku/<SKU>`), com ids, preços, de onde veio o fiscal e o que
ficou pendente (fotos no Bling, publicar nos canais — aline).

## Limitações conhecidas
- Fotos no Bling: só por link público (passo 6b). O conector do Drive não remove
  compartilhamento; foto compartilhada por engano tem de ser restringida à mão no Drive.
- O MCP do Bling não exclui produtos: erros se corrigem com `patchProduct`.
