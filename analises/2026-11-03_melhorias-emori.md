# Melhorias e correções para a equipe Emori

Levantado em 03/11/2026 pela Maranne (conta com ML LILIH STORE 136674333, ML LILIH STORE2 1336305738, Shopee 265604406, TikTok e Amazon), durante uma análise de vendas, Ads e adesão a promoções (11.11, Black Friday e campanhas Smart) feita pelo MCP da Emori. Cada item traz o que aconteceu, o anúncio e o que esperávamos.

## 1. Falta uma ferramenta para trocar o tipo de anúncio (Premium ↔ Clássico)

- **O que aconteceu:** para a Blusa manga 3/4 (MLB5353470708, Lilih), a margem só ficava acima do nosso mínimo se o anúncio passasse de Premium (19%) para Clássico (14%). Não existe ferramenta no MCP para isso, e a troca teve que ser feita à mão no painel do ML.
- **O que esperávamos:** uma ferramenta para mudar o `listing_type` (gold_pro ↔ gold_special), com prévia da nova taxa e da margem, e com confirmação, como as outras que alteram a conta.

## 2. Dados desatualizados depois de alterações

- **Tipo de anúncio:** depois da troca no ML para Clássico, `get_item_info` e `filtrar_oportunidades_promocao` continuaram mostrando `tipo_anuncio: gold_pro` e taxa de 19% no MLB5353470708. Toda a simulação de margem ficou errada até sincronizar.
- **Promoções:** depois de 5 adesões confirmadas pelo ML (resposta "Anúncio aderido à promoção com sucesso"), `listar_itens_promocoes_ativas` voltou com 0 itens e `get_margem_anuncio_promocao` ainda mostrava a campanha como "Elegível". Exemplo: MLB3999624839 na Moda Nov26 (P-MLB18197010).
- **O que esperávamos:** que, depois de uma escrita feita pelo próprio MCP, o item fosse relido da API oficial e o retorno já trouxesse o estado novo. Ou, pelo menos, um campo de "última sincronização" para sabermos se o dado é confiável.

## 3. `get_item_info` ignora o anúncio pedido

- **O que aconteceu:** chamamos `get_item_info` com `item_mlb = MLB5353470708` e `just_summary=false`. O retorno trouxe 100 anúncios da conta (`recordsTotal` 16.890, cerca de 150 mil caracteres), e o primeiro registro era outro anúncio (MLB3286347431). Só achamos o anúncio certo filtrando a lista do nosso lado.
- **O que esperávamos:** só o anúncio pedido.

## 4. Adesão ao "Desconto no Pix" (BANK) falha

- **O que aconteceu:** ao aderir o Combo 5 (MLB3272093035, Lilih2) à P-MLB18215036 pelo `aderir_promocoes_lote`, o ML devolveu `PIX_OPTIN_PERCENTAGE_NULL_ERROR - Both meli_percentage and seller_percentage must be present and not null`. As ferramentas de adesão não aceitam esses dois campos.
- **O que esperávamos:** aceitar `meli_percentage` e `seller_percentage` nas promoções BANK, ou preencher com os valores sugeridos pelo ML.

## 5. Elegibilidade da 11.11 diferente do que o ML aceita

- **O que aconteceu:** a "11.11 da Black" (P-MLB17909028, DEAL, até 12/11) aparecia como elegível para o Tule gola alta (MLB2649786064) em `buscar_campanhas_por_nome`, `filtrar_oportunidades_promocao` e `get_margem_anuncio_promocao`. Na adesão, o ML recusou: "não está apto ou a oportunidade expirou". Logo depois, o mesmo filtro já não listava a 11.11 para esse anúncio.
- **Outro caso:** `simular_margem_promocao` devolveu 0 promoções para o Kit 2 (MLB3375267590, Lilih2). Pouco depois, `filtrar_oportunidades_promocao` e `get_margem_anuncio_promocao` mostraram várias campanhas elegíveis para o mesmo anúncio.
- **O que esperávamos:** a mesma lista de campanhas em todas as ferramentas, conferida na API do ML antes de aparecer como elegível.

## 6. Status "started" em oferta que ainda não começou

- **O que aconteceu:** as adesões à Black Friday 2026 (P-MLB17911004, de 12/11 a 01/12) voltaram com `status: started` no dia 03/11. Não sabemos se o preço promocional já está valendo ou se está só agendado.
- **O que esperávamos:** o status real (agendada × ativa) e a data em que o preço entra.

## 7. Shopee: desconto sem escolha de datas

- **O que aconteceu:** `criar_desconto_shopee` não tem campos de início e fim. O desconto "11.11 Kits Maranne" (ID 521834793742377) foi criado com 30 dias, de 03/11 a 03/12, e nós queríamos só o período da 11.11.
- **O que esperávamos:** `start_time` e `end_time` opcionais, e também a possibilidade de incluir ou retirar itens de um desconto já criado.

## 8. Shopee: campanhas da plataforma não aparecem

- **O que aconteceu:** as campanhas da própria Shopee (como a 11.11) não aparecem em nenhuma ferramenta. Só dá para criar descontos da loja, e a inscrição nas campanhas tem que ser feita no Seller Center.
- **O que esperávamos:** listar as campanhas da plataforma com os requisitos de cada uma, e permitir a inscrição.

## 9. Shopee: visitas zeradas e Ads de grupo sem rateio

- **Visitas:** em `get_lucro_anuncio`, todos os anúncios da Shopee vêm com `Visitas: 0`, então não dá para calcular conversão.
- **Ads de grupo:** a campanha de grupo "Kit 2 camisetas básicas" (id 99029495, `SemPorProduto: true`) gastou R$ 67,85 na semana. Mesmo assim, o Kit 2 (19958252870) aparece com `CustoAds: 0` no lucro por anúncio, e a margem e o TACOS ficam maiores do que são.
- **O que esperávamos:** as visitas da Shopee, e o gasto das campanhas de grupo dividido entre os anúncios do grupo.

## 10. Sem histórico de alterações

- **Anúncios:** `get_historico_alteracoes` voltou vazio para o MLB3286413799, que teve várias mudanças de preço e promoção em 2026.
- **Ads:** não há como ver quem mudou o ACOS alvo, o orçamento ou o status de uma campanha, nem quando. A ML Lilih teve uma queda de 78% no gasto de Ads em uma semana e não conseguimos saber se foi alteração manual ou o próprio ML reduzindo os lances.
- **O que esperávamos:** o histórico de preço, promoção, tipo de anúncio e campanhas de Ads, com data e origem.

## 11. Respostas grandes demais e sem filtro por item

- **O que aconteceu:** `filtrar_oportunidades_shopee` não tem filtro por `item_id`. Para pegar as variações de 3 kits, foi preciso pedir 200 linhas da loja inteira (92 mil caracteres) e filtrar do nosso lado. O mesmo vale para `get_item_info` (item 3).
- **O que esperávamos:** filtro por `item_id`, e resposta resumida por anúncio com a lista de `model_id`.

## 12. Sugestões de melhoria

- **Margem com Ads nas simulações:** `simular_margem_promocao`, `filtrar_oportunidades_promocao` e `simular_margem_shopee` calculam a margem sem o Ads. Ajudaria ter um parâmetro para descontar o TACOS do anúncio num período (por exemplo, últimos 7 ou 30 dias) e um filtro de margem mínima já com Ads.
- **Alerta de cadastro divergente:** o mesmo SKU tem CMV diferente entre lojas (25343Un: R$ 13 × R$ 14; 25764Un: R$ 17 × R$ 21), e o imposto é 9% em umas lojas e 10% em outras. Um alerta de divergência por SKU evitaria margens erradas.
- **Faixas de frete e de taxa na simulação:** ajudaria indicar quando um preço promocional cruza uma faixa de frete do ML (por exemplo, abaixo de R$ 49 o frete cai) ou de taxa fixa da Shopee (abaixo de R$ 100 a taxa fixa cai de R$ 20 para R$ 16), porque isso muda o melhor desconto.
