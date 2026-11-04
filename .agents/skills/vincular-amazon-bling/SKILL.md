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
| Preço | o preço do anúncio, em `preco` e `precoPromocional`. Se o preço no Bling for diferente do anúncio de origem, pergunte ao usuário qual usar |

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
2. **Procurar o anúncio da Amazon (Emori).** Veja se `get_items_by_sku` já traz um item
   com `marketplace` Amazon. Se trouxer, compare os SKUs dele com os do passo 1. Clone
   recente pode ainda não aparecer: nesse caso, avise que os SKUs não foram confirmados.
3. **Achar os ids (Bling).** `listProducts` com `codigos` (pai e variações), `criterio: "5"`
   e `fields` `id`, `codigo`, `nome`, `situacao`, `idProdutoPai`, `preco`. Confira que todos existem,
   estão ativos e têm o mesmo pai. Se faltar algum, pare e mostre.
4. **Conferir vínculos existentes (NFE DAH).** `consultar_vinculos` com `id_empresa` e `sku`
   do pai e de cada variação. Essa consulta usa um espelho local; para ver o dado direto do
   Bling, use `listar_produtos_lojas` com `idProduto` e `idLoja`. Variação que já tem vínculo
   na Loja Amazon fica fora do lote. Mostre ao usuário.
5. **Pedir o OK.** Mostre a tabela SKU × id Bling, o preço e o aviso do passo 2, se houver.
   Só continue com a aprovação do usuário.
6. **Criar os vínculos (NFE DAH).** `vincular_produto_loja` funciona em duas chamadas por
   variação:
   - 1ª, sem `confirmar`: devolve a prévia e um `token_confirmacao`. Nada é gravado.
   - 2ª, com os mesmos argumentos, `confirmar: true` e o token. O token vale só para aquela
     variação.

   Com o OK do passo 5, faça as prévias de todas, confira que batem com o aprovado e grave.
   Se uma variação falhar, ou se a ferramenta devolver um vínculo que já existe, não force:
   grave as outras e relate. Para corrigir um vínculo, use `atualizar_vinculo_produto_loja`.
7. **Registrar no log**, conforme o `AGENTS.md`, com `#tema/cadastro` `#tema/anuncios`
   `#loja/amazon` `#sku/<pai>`, a conta, o nº de variações e o preço. Se os SKUs não foram
   confirmados no passo 2, anote em `Pendente:`.

## Depois de vincular

Quando o anúncio aparecer na Emori, confira se os SKUs da Amazon são iguais aos do Bling.
Se algum for diferente, o vínculo daquela variação fica com o código errado e o estoque
não chega nela.
