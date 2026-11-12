---
name: vincular-amazon-bling
description: Vincula no Bling as variações de um anúncio novo da Amazon da Maranne (normalmente clonado de um anúncio do Mercado Livre pela Emori), para o Bling mandar o estoque à Amazon. Parte de um MLB ou SKU, confere SKUs e ids na Emori e no Bling, e cria os vínculos na Loja Amazon pelo conector NFE DAH. Use quando pedirem para vincular, ligar ou conectar anúncio ou produto da Amazon no Bling, "clonei para a Amazon, falta vincular", mesmo sem dizer "skill".
---

# Vincular anúncio da Amazon no Bling

Depois de clonar um anúncio para a Amazon, cada variação precisa de um vínculo com a
Loja Amazon no Bling. É esse vínculo que faz o Bling mandar o estoque ao anúncio.

## Padrão Maranne na Amazon (não mude sem o usuário pedir)

| O quê | Valor |
|---|---|
| Conta | **Bling 1**: MRN COMERCIO DE VESTUARIO LTDA, `id_empresa` `05eb6a2049b5fa1ef5b1e2bf76d3fafd` |
| Loja | **Loja Amazon**, `idLoja` `205660849` |
| Produto pai | **sem vínculo** |
| Cada variação | 1 vínculo, com `idProduto` da variação e `codigo` = **SKU da variação** |
| Preço | o preço do anúncio **na Amazon**, em `preco` e `precoPromocional`. Se ele ainda não aparecer na Emori, ou se divergir do Bling, pergunte ao usuário qual usar. O preço do anúncio de origem pode não ser o da Amazon (no 2605084: Shopee R$ 44,90, Amazon R$ 39,90) |

Exemplo: variação `25343UnPretoP` (id `16448965267`) → `codigo` `25343UnPretoP`.

Por enquanto só se vincula no Bling 1. A outra conta é a MRN II
(`c11698532af5bf698c6f57053f307945`); se pedirem para vincular nela, confira antes o id
da loja com `listar_lojas` e como os produtos de lá estão vinculados.

**Diferente dos outros canais:** no Mercado Livre, TikTok e Shopee o código é o id do
anúncio ou da variação no canal. Na Amazon é o SKU. A descrição da ferramenta
`vincular_produto_loja` cita o padrão dos outros canais (vínculo também no pai); na
Amazon, siga a tabela acima.

## Integrações necessárias

- **Emori:** dados do anúncio de origem.
- **Bling:** ids dos produtos (`listProducts`).
- **NFE DAH:** vínculos. Se aparecer conectado mas sem ferramentas, peça ao usuário para
  desativar e ativar de novo nos Conectores. Foi o que resolveu em 04/11/2026.

Se faltar alguma, siga `integracoes.md`: avise qual falta e não improvise.

## Passo a passo

1. **Achar os SKUs (Emori).** Com o id do anúncio de origem (MLB ou id da Shopee),
   `get_item_info` dá o SKU pai e o preço. Com o SKU pai,
   `get_items_by_sku` lista as variações. Se a resposta trouxer vários anúncios, use as
   variações do anúncio de origem.
2. **Procurar o anúncio da Amazon (Emori).** Use `get_items_by_sku` com o SKU de uma
   **variação**, não o do pai: a busca pelo pai para em 50 resultados e pode esconder o
   item da Amazon. Se vier item com `marketplace` Amazon, compare o SKU, anote o preço
   (`preco_venda` da variação) e o status. Clone recente pode ainda não aparecer: nesse
   caso, avise que SKU e preço não foram confirmados.
3. **Achar os ids (Bling).** `listProducts` com `codigos` (pai e variações), `criterio: "5"`
   e `fields` `id`, `codigo`, `nome`, `situacao`, `idProdutoPai`, `preco`. Confira que todos existem,
   estão ativos e têm o mesmo pai. Se faltar algum, pare e mostre.
4. **Conferir vínculos existentes (NFE DAH).** `consultar_vinculos` com `id_empresa` e `sku`
   do pai e de cada variação. Essa consulta usa um espelho local; para ver o dado direto do
   Bling, use `listar_produtos_lojas` com `idProduto` e `idLoja`. Variação que já tem vínculo
   na Loja Amazon fica fora do lote. Mostre ao usuário.
5. **Pedir o OK.** Mostre a tabela SKU × id Bling, o preço e o aviso do passo 2, se houver.
   Só continue com a aprovação do usuário.
6. **Criar os vínculos (NFE DAH).** Prefira `vincular_produtos_loja_lote` (até 50 itens por
   chamada, com `idLoja` e `id_empresa`; cada item tem `idProduto`, `codigo`, `preco` e
   `precoPromocional`). Não inclua o pai. Funciona em duas chamadas:
   - 1ª, sem `confirmar`: devolve a prévia, com preços de referência e itens pulados, e um
     `token_confirmacao`. Nada é gravado.
   - 2ª, com os mesmos argumentos, `confirmar: true` e o token.

   Com o OK do passo 5, confira que a prévia bate com o aprovado e grave. Item pulado ou com
   falha não se força: relate. Para corrigir preço de vários vínculos, use
   `atualizar_precos_vinculos`; para outro campo, `atualizar_vinculo_produto_loja`.
7. **Registrar no log**, conforme o `AGENTS.md`, com `#tema/cadastro` `#tema/anuncios`
   `#loja/amazon` `#sku/<pai>`, a conta, o nº de variações e o preço. Se os SKUs não foram
   confirmados no passo 2, anote em `pendencias.md`.

## Depois de vincular

Quando o anúncio aparecer na Emori, confira se os SKUs da Amazon são iguais aos do Bling.
Se algum for diferente, o vínculo daquela variação fica com o código errado e o estoque
não chega nela.

Confira também, com `get_item_info` no ASIN do pai (vem em `variacoes` do resultado de
`get_items_by_sku`): `n_variacoes` deve ser igual ao nº de vínculos criados, e o preço
igual ao do vínculo. Depois veja se o estoque chegou e se as variações saíram de
`paused`/`inactive`. Se o anúncio apareceu antes de gravar, faça essa conferência antes.
