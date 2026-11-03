# Guia de títulos e descrições — Maranne

Baseado em 28 produtos do Bling (12 simples antigos, 11 kits, 5 lançamentos de 2026),
analisados em 03/11/2026. Usado pelas skills `criar-produto` e `criar-kit-bling`.
Modelo pronto para preencher: `.agents/skills/criar-produto/modelo-descricao.html`.

## 1. Padrão atual (2026) — usar este

Visto em 2605087 (Blusa Um Ombro Só), 2601101 (Blusa Tomara que Caia Peplum) e nos kits deles.
Ordem fixa das seções:

1. **DESCRIÇÃO DO PRODUTO:**
   - 1ª linha: o título do produto, sozinho.
   - **3 parágrafos** (≈ 60–90 palavras cada):
     1. *O que é + para quem*: "A {título} é a escolha ideal para quem busca {estilo, modernidade e
        feminilidade}…" + o detalhe que diferencia (ombro só, peplum, gola alta, renda…).
     2. *Material + versatilidade*: "Confeccionada em {tecido}, é uma opção versátil…" + ocasiões
        (passeios, encontros, trabalho, eventos, noite de sono…).
     3. *Como combinar*: "Combine com calça jeans, shorts, saias ou peças de alfaiataria…",
        "do casual ao sofisticado". (Pijama: conforto, noite de sono, presente.)
2. **– DETALHES DO TECIDO:**
   - `Tecido:` nome comercial (Malha Viscolycra, Malha Suplex, Ribana Canelada, Tule…)
   - `Composição:` percentuais (96% Viscose e 4% Elastano)
   - `Descrição do Tecido:` 2–3 frases sobre toque, elasticidade, caimento, conforto
     (ver §5 para textos prontos por tecido).
3. **COMPOSIÇÃO DO KIT:** (só kits) — ver §4.
4. **MEDIDAS APROXIMADAS:** uma linha por tamanho — ver §3.
5. **Medidas da modelo** (`Medidas da modelo: Altura: 1,65 m | Manequim: 38/P`) — ver §3.
6. **ATENÇÃO – Cor, encolhimento, instruções de lavagem:** texto fixo (§6).
7. **– ENCOLHIMENTO:** texto fixo para malha (§6); ajustar/remover em tecido plano.
8. **– COR:** texto fixo (§6).

Formatação: títulos de seção em **negrito e MAIÚSCULAS terminando em ":"**; itens de lista com
"–"; quebras de linha com `<br />`. **Nunca tabela HTML** (nenhum produto usa; marketplaces
cortam). HTML limpo, sem estilos inline (o script de kit limpa automaticamente).

## 2. Padrão antigo (2023–2025) — só para reconhecer

`DETALHES:` → `Tecido: …` → 1 parágrafo curto e emotivo → `– ESTAMPA:` → `SUGESTÃO DE TAMANHOS:` →
`MEDIDAS APROXIMADAS:` → Medidas da Ju → ATENÇÃO / ENCOLHIMENTO / COR.
Tom: caixa alta e exclamações ("Aquela peça PERFEITA", "VOCÊ VAI AMAR!!!", "Seu Look de dormir
será um ARRASOOOO!", "pijaminha", "Lookinhos"). O padrão 2026 trocou isso por texto descritivo,
com termos de busca (bom para Mercado Livre/Shopee/Google).

## 3. Tamanhos e medidas

- Grade padrão: **P, M, G, GG**. Plus size: **G1, G2, G3, G4** (busto até 110 / 120 / 130 / 140 cm).
- Uma linha por tamanho, medidas separadas por " / ":
  `P – Busto: até 90 cm / Cintura: até 70 cm / Comprimento: 60 cm`
  - "até" nas medidas do corpo que a malha acompanha (busto, cintura, quadril);
    medida da peça sem "até" (comprimento, manga, barra, cavalo, top).
- Medidas usadas por tipo de peça:

| Peça | Medidas |
|---|---|
| Blusa / camiseta | Comprimento (ou "Comprimento com a alça"), Busto, Cintura, Manga, Barra, Circunferência da manga |
| Baby doll / pijama | Quadril, Cintura, Comprimento (do short/calça), Cavalo, Busto, Top, Comprimento kimono |
| Calça | Cintura, Quadril, Comprimento, Cavalo (ver produto parecido no Bling) |

- **Sem "Sugestão de tamanhos"** (era do padrão antigo; o 2026 não usa).
- **Medidas da modelo** (padrão desde 03/11/2026, decisão do daniel):
  `Medidas da modelo: Altura: 1,65 m | Manequim: 38/P`
  Não citar o nome da modelo (antes era "Medidas da Ju"/"da Carol"). Busto, cintura e quadril
  da modelo só se o usuário informar.

## 4. Kits

- **Título:** `Kit 2 Blusas Feminina {resto do título da peça}` (padrão 2026).
  Antigo: `KIT - 2 …` — não usar mais.
- **Descrição:** a da peça unitária + bloco de composição logo depois da DESCRIÇÃO DO PRODUTO
  (antes de DETALHES DO TECIDO):
  ```
  COMPOSIÇÃO DO KIT:
  Kit21: 1x Preto, 1x Branco
  Kit22: 1x Preto, 1x Vermelho
  *Todas as peças são da mesma numeração.
  ```
  Cores sem repetir (regra da Maranne), salvo pedido. Kit sortido:
  `*As cores do kit são SORTIDAS, não é possível escolher as cores.`

## 5. Tecidos (textos prontos)

| Tecido | Composição usual | Descrição do tecido |
|---|---|---|
| Malha Viscolycra | 96% Viscose e 4% Elastano | Tecido leve, fresco e muito macio ao toque. Sua composição elástica proporciona um caimento perfeito e ajusta-se suavemente ao corpo, garantindo conforto e liberdade de movimento. |
| Malha Suplex | 98% Poliéster e 2% Elastano | Tecido macio, confortável e com ótima elasticidade, proporcionando um caimento ajustado ao corpo sem abrir mão da liberdade de movimentos. Toque agradável, ótima opção para o dia a dia. |
| Ribana Canelada | 97% Poliéster e 3% Elastano | Tecido macio e flexível, conhecido pelas listras em relevo que garantem elasticidade, ajuste ao corpo e muito conforto. Valoriza o caimento e acompanha os movimentos sem perder a forma. |
| Ribana Lafayete | 93% Viscose e 7% Elastano | (escrever no 1º uso e acrescentar aqui) |
| Malha Buble | 96% Viscose e 4% Elastano | (escrever no 1º uso e acrescentar aqui) |

Tecido novo: escreva a descrição no mesmo tom e **acrescente nesta tabela**.

## 6. Textos fixos (copiar igual)

- **ATENÇÃO – Cor, encolhimento, instruções de lavagem:**
  – Conforme instrução de lavagem na etiqueta: **esta peça pode ser lavada em máquina porém não deve
  ser usado o modo secagem/secadora.** Este tecido por ser delicado, as costuras podem ser danificadas
  então indicamos que NÃO seja torcido à mão e também por ser estampado/colorido não deixar de molho.
  Desta forma, sua peça será **melhor conservada**, bem como a taxa de **encolhimento** será menor. =)
- **– ENCOLHIMENTO:** Como trata-se de uma malha, após a primeira lavagem, há uma taxa de encolhimento
  de até **10%** da peça (se lavada e secada corretamente).
- **– COR:** Como são produzidas em estúdio as fotos podem apresentar uma pequena variação de cor por
  conta do flash e também tem o fator de cada monitor/celular que pode mudar a tonalidade.
- **ESTAMPA:** não usar (o padrão 2026 não tem essa seção).

## 7. Títulos

Estrutura 2026: **{Tipo} Feminina {modelo/detalhe} de {Tecido} com {Detalhe}** — até 120 caracteres
(Bling); o Mercado Livre corta em 60, então o essencial vai no começo.
Ex.: "Blusa Feminina Um Ombro Só de Suplex com Estampa de Poá", "Blusa Feminina Tomara que Caia Peplum",
"Baby Doll Canelado com Laço de Cetim". A cor **não** vai no título do produto pai (vai na variação).

## 8. Palavras e tom

- **Usar (2026):** escolha ideal, estilo, modernidade, feminilidade, versátil, valoriza, charme,
  delicadeza, sofisticado, atemporal, confortável, caimento, toque macio, do casual ao sofisticado,
  combine com, renovar o guarda-roupa. Pijama: noite de sono perfeita, conforto, delicado, romântico.
- **Evitar:** caixa alta para ênfase, "!!!", gírias ("arrasooo", "pijaminha"), prometer o que não dá
  ("não tem ajuste" deve ser dito quando for o caso: "elástico na cintura (sem regulagem)").
- Dizer sempre: tipo de fechamento/ajuste (alça regulável, elástico, amarração), comprimento/modelagem
  (cintura alta, cropped, longo), e o que NÃO tem quando o cliente pode esperar (ex.: sem bojo).

## 9. Erros encontrados no Bling (corrigir quando editar)

- 2605087 e o kit: título diz **Suplex**, mas a descrição diz "Malha Viscolyra" 96% Viscose
  (tecido divergente e "Viscolyra" sem o c).
- 2605087Kit2 e 2601101Kit2: **sem** bloco COMPOSIÇÃO DO KIT; 2601101Kit2 com MEDIDAS vazio.
- "Medidas da Ju" com manequim **38/P** (antigos) e **38/M** (2026) e altura "1.60 cm" — trocar pela
  linha padrão de medidas da modelo (§3).
- Erros de digitação repetidos no texto fixo antigo: "torcio", "Deste forma"; "comoposto",
  "Canaledas".
- Composição de kit escrita de 4 jeitos diferentes ("COMPOSIÇÃO KIT 5:", "*Kit composto por",
  "** Kit1 é composto por", "Cores:") — padronizar como no §4.

## Decisões (daniel, 03/11/2026)

- Padrão 2026 mantido: **sem** SUGESTÃO DE TAMANHOS e **sem** ESTAMPA.
- Medidas da modelo: `Medidas da modelo: Altura: 1,65 m | Manequim: 38/P` (sem nome da modelo).
