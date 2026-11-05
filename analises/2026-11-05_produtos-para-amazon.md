# O que subir na Amazon: vendas de 90 dias (07/08 a 05/11/2026)

Fonte: Emori (lucro por anúncio em 90 e 30 dias, curva ABC por SKU, busca por SKU) e NFE DAH (vínculos da Loja Amazon no Bling, espelho de 05/11). Análise feita em 05/11/2026 para daniel.

## Conclusão

1. **Cinco produtos valem clone agora**, nesta ordem: Pantalona, Kit 2 Manga 3/4, Regata Decote V (Kit 2 e unitária) e Regata Decote Quadrado (Kit 2 e unitária).
2. **O maior ganho não é clone.** Os kits de camiseta 2007113 já estão na Amazon, mas nas 3 variações sem vínculo que conferi estão pausados com estoque 0. O Kit 5 sozinho vendeu R$ 37.813 fora da Amazon.
3. **A Amazon quase não vende hoje:** R$ 334 e 6 pedidos em 90 dias, contra R$ 239.873 nos outros canais. Subir anúncio pode não bastar. Vale testar a venda com poucos produtos antes de clonar muitos.

## 1. Clonar agora

| # | Produto | SKU base | Total vendido 90d | Un. | Lucro | Ritmo 30d* | Preço | Margem Amazon estimada | Origem sugerida |
|---|---|---|---|---|---|---|---|---|---|
| 1 | Calça Pantalona Viscolycra | `25128` | R$ 13.945 | 212 | 29,0% | 31% | 69,90 | ~35% | `MLB3999624839` |
| 2 | Kit 2 Blusas Manga 3/4 | `25343Kit2` | R$ 6.569 | 91 | 25,2% | 21% | 74,90 | ~31% | `MLB4034118057` |
| 3 | Kit 2 Regatas Decote V | `25764Kit2` | R$ 5.861 | 59 | 31,5% | 14% | 99,90 | 22–31% | `MLB5694702112` |
| 4 | Regata Decote V | `25764Un` | R$ 2.999 | 56 | 23,1% | 29% | 54,90 | ~29% | `MLB5698876604` |
| 5 | Regata Decote Quadrado, Kit 2 e unitária | `2501141` | R$ 1.553 | 32 | 21% | 56% | 59,90 / 39,90 | ~22% / ~27% | `MLB5301752154` / `MLB3988766919` |

\* Unidades dos últimos 30 dias sobre as de 90. Ritmo constante daria 33%.

Pontos de atenção:
- **Pantalona:** é o melhor caso, com volume, a melhor margem entre os produtos de volume e ritmo estável. No Bling da Loja Amazon existe um vínculo solto no SKU pai `25128`, com preço 0, e a Emori não mostra anúncio Amazon para `25128PretoM`. Limpar esse vínculo ao clonar, pois o padrão é pai sem vínculo. A Emori usa custo R$ 21 na variação e R$ 25 no anúncio `MLB3999624839`; com R$ 25, a margem estimada cai para ~30%.
- **Kit 2 Manga 3/4:** completa a família, já que unitária e Kit 3 entraram na Amazon em 04/11.
- **Kit 2 Regatas Decote V:** 52 das 59 unidades vieram do TikTok, a cerca de R$ 99, e o ritmo caiu. O anúncio da Lilih está pausado; a origem sugerida é o da Lilih2. É uma aposta para o verão, não um produto comprovado em vários canais.
- **Regata Decote Quadrado:** deixei o Kit 3 de fora (lucro de 9,4%). É o único aqui que acelerou: 18 das 32 unidades (9 de cada) vieram nos últimos 30 dias, mas o volume ainda é pequeno.
- Algumas grades estão zeradas nos canais (ex.: `25343Kit21P`, `25764UnPretoM`). Conferir o estoque por variação antes de clonar.

## 2. Já está na Amazon, mas parado (resolver antes dos clones)

| Família | Total vendido 90d | Vendas em SKUs com vínculo Amazon | Amostra na Emori |
|---|---|---|---|
| Kit 5 Camisetas Viscose (`2007113Kit…Viscose`) | R$ 37.813 | ~24% | `2007113Kit6ViscoseGG`: paused, estoque 0 |
| Kit 2 Camiseta Básica (`2007113Kit2`) | R$ 47.265 | ~74% | `2007113Kit29GG`: paused, estoque 0 (`2007113Kit29M`, com vínculo: active, estoque 32) |
| Kit 3 Camiseta Básica (`2007113Kit3`) | R$ 22.171 | ~49% | `2007113Kit32GG`: paused, estoque 0 |
| Camiseta Gola V unitária (`2007113Un`) | R$ 29.885 | 0% | `2007113UnPretoM`: active, estoque 203, sem vínculo |

- Isso soma cerca de **R$ 82 mil** vendidos em 90 dias em variações sem vínculo Amazon (Kit 5 ~R$ 28,7 mil, Un R$ 29,9 mil, Kit 2 ~R$ 12,3 mil, Kit 3 ~R$ 11,3 mil).
- **Risco na unitária:** o anúncio está ativo e sem vínculo nas duas contas Bling, então o estoque da Amazon (203) pode não acompanhar o real e gerar venda sem peça. Conferi só `2007113UnPretoM` nas duas contas; os outros SKUs da unitária, só na Loja Amazon.
- O caminho provável é vincular as variações que faltam com a skill `vincular-amazon-bling`. Conferi só uma variação sem vínculo por família, então falta listar quantas estão pausadas no Seller Central.

## 3. Deixar para depois

- **Tule Marrom e Vinho (`1911283`):** R$ 7.716 e 207 un. no ML, lucro de 18,5% e 22,7%. O clone de 04/11 levou 10 cores e deixou essas duas de fora, mas elas estão entre as cores que mais vendem. O ritmo caiu com o fim do inverno (31 un. em 30 dias, contando Shopee). Sugestão: subir antes do próximo inverno.
- **Pijamas (`20102010`, `2103231`, `2319061`):** R$ 10.822 e 136 un., só no TikTok. Foram só 3 un. nos últimos 30 dias, com estoque quase zerado no TikTok (Cereja P 3, M/G/GG 0; Luiza 0). Venderam perto de R$ 80, com lista de R$ 119,90 a 139,90. Só faz sentido com estoque e preço definidos.
- **Camisas de crepe e viscose (`26072702`, `26072703`), jaqueta e veludo cotelê (`26052601`, `26051201`):** menos de 25 un. cada. Ainda não têm volume para justificar o clone.

## Como chegar a esses números

- **Famílias:** agrupei por SKU base e formato (unitária, Kit 2, 3, 5). Sem SKU na venda, usei o título do anúncio.
- **"Está na Amazon":** cruzei os 219 vínculos da Loja Amazon no Bling e confirmei os candidatos com busca na Emori pelo SKU da variação (a busca pelo pai para em 50 resultados, ver log de 04/11). A listagem completa de anúncios Amazon não saiu: a consulta da Emori cortou o resultado.
- **Margem Amazon estimada:** não é simulação. Usei preço menos 15% de taxa, 10% de imposto, custo cadastrado e frete de R$ 6,50–6,75 (o que a Emori mostra na Amazon nessa faixa de preço). No Kit 2 Decote V usei de R$ 6,75 a R$ 15,70. A prévia de clone da Emori daria o número certo, mas custa 2 créditos por anúncio.
- **Lucro realizado na Amazon não serve de base:** a Emori registra taxa zero em 2 dos 3 anúncios com venda na Amazon.
- **Cores do tule:** a Shopee soma todas as cores em um anúncio, então usei só os anúncios do ML por cor para Marrom e Vinho.

## Perguntas para decidir

1. Reativar e vincular os kits 2007113 antes de clonar, ou em paralelo?
2. Por que a Amazon vende tão pouco? Sem Ads, sem FBA e preço igual aos outros canais são hipóteses a conferir; nada disso foi medido aqui.
3. Quanto subir agora: só a Pantalona como teste, ou os cinco?

## Atualização das 10:57: conferências antes de executar

- **Kits com categoria errada:** `2007113Kit6ViscoseGG` e `2007113Kit29GG` estão como `ANTENNA`, com taxa de 28,76% na Emori e margem de 2,27% e 8,87%. `2007113Kit32GG` está como `SHIRT`, com 15% e 24,62%. Foi conferida uma variação por kit. Reativar os dois primeiros sem corrigir pode dar pouca margem.
- **Pantalona:** a origem `MLB3999624839` só leva Preto e Marrom (8 de 20 variações do Bling). A prévia sugere R$ 59,91, com custo R$ 25 (as variações têm R$ 21). A margem de ~35% da tabela vale a R$ 69,90 e custo R$ 21; não foi simulada.
