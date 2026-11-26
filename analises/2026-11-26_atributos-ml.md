# Atributos do ML — proposta de preenchimento (26/11/2026)

Fonte: MCP Emori (`get_ficha_ml`, ao vivo), 10 mais vendidos de 27/10–25/11. Itens 1–3 gravados em 26/11 16:17 via Emori, aprovados por daniel (ver log). GTIN, Cor filtrável e embalagem ficaram pendentes.

## 1. Pantalona 25128 · Lilih · MLB3999624839 (5 campos do anúncio faltando)
| Atributo | Proposta | Confiança |
|---|---|---|
| É oversized (IS_OVERSIZED_FIT) | Não (242084) | alta |
| É rasgada (IS_RIPPED) | Não (242084) | alta |
| Tipo de fechamento (CLOSURE_TYPE) | Elástico (1164222) | confirmar: cós com elástico? |
| Tipo de bainha (HEM_TYPE) | Clássica (579609) | confirmar |
| Detalhes de design (DESIGN_DETAILS) | não se aplica (-1) | pregas ≠ plissada; nenhuma opção serve |
Variação 25128PretoP (183105352442): Cor principal vazia → Preto (2450295).

## 2. Camiseta 2007113Un · Lilih · MLB3907074383 (Cor principal por variação)
- Vazia → preencher: Vermelho G/GG/M (182205559774/772/776) → Vermelho; Cáqui G/GG (182205559780/782) → Bege; Verde Salsa G/GG/M (182205559810/806/814) → Verde.
- Errada → corrigir: Pink P/M/G/GG e Rosa-chiclete P/M/G/GG estão "Vermelho" → Rosa (2450312).
- Não mexer: Amarelo Manteiga (4 variações) sem GTIN — não inventar código.

## 3. Blusa manga 3/4 25343Un · Lilih · MLB5353470708 (Cor principal por variação)
- Vazia → preencher: Preto P/M/G/GG → Preto; Marrom P/M/G/GG → Marrom; Verde Salsa P/M/G/GG → Verde (e Cor filtrável também vazia no Verde).
- Problema maior, não resolvido aqui: as 12 variações antigas têm o MESMO GTIN 7795788969320. O ML pode penalizar; decidir se troca pelos GTINs da planilha.

## Outros achados
- Combo 3 Lilih2 MLB3375318744: ficha completa, mas peso e medidas da embalagem estão 0.
- Kit 2 Lilih MLB2895199720: ficha completa.

## Rodada completa (meta: zerar atributos faltando) — progresso
Autorizado por daniel em 26/11 para preencher tudo sem pedir de novo. Regras usadas: calça de malha → oversized Não, rasgada Não, fechamento Elástico, bainha Clássica, detalhes de design não se aplica; segunda pele/tule → caimento Slim; Viscolycra = 96% Viscose e 4% Elastano (guias/descricao-produto.md); kits → formato Pack; esportiva Não; gestação Não; usos recomendados não se aplica.

| MLB | Loja | Gravado |
|---|---|---|
| MLB1502337363 | Lilih | oversized, rasgada, fechamento, bainha, design (5) |
| MLB1505862149 | Lilih | oversized, rasgada, fechamento, bainha, design (5) |
| MLB2014027084 | Lilih | composição, gestação, usos (3) |
| MLB3147208096 | Lilih | formato Pack, esportiva Não (2) |
| MLB2649786064 | Lilih | caimento Slim (1) |
| MLB3333283501 | Lilih | material Viscose, estilos Casual/Trabalho (2) |
| MLB3279304519 | Lilih | caimento Slim (1) |
| MLB3267977045 | Lilih | caimento Slim (1) |
| MLB3428173192 | Lilih | caimento Slim (1) |
| MLB3680919912 | Lilih | composição 96/4, ano 2023 (criado 29/05/2023) (2) |
| MLB3524499381 | Lilih | materiais reciclados Não (1) |
| MLB3278177457 | Lilih | caimento Slim, estilos Casual/Trabalho (2) |

Obs.: `get_attributes` da Emori às vezes está desatualizado (ex.: MLB3695643638 já tinha caimento e estilos); a conferência vale pelo `get_ficha_ml`. "Produto não encontrado" no get_attributes = nada faltando.
| MLB4285317166 | Lilih | 10 campos copiados do Kit 2 irmão MLB4285166766 (Viscolycra, Pack, Slim, Camiseta, sem mangas, gola alta, não se aplica em gestação/esportiva/usos, tecido Viscolycra) |
| MLB4285166766 | Lilih | formato Pack (1) |
| MLB3893486753 | Lilih | reciclados Não, esportiva Não (2) |

Lilih já completos (ficha sem faltando): MLB2653348310, MLB2897464137, MLB3356203446, MLB3284929011, MLB3439246182, MLB2895100530, MLB2895199720, MLB2652323121, MLB3966918042, MLB3431379787, MLB3817676703, MLB5033452106, MLB5046066410, MLB3987395659, MLB3988766919, MLB3907074383, MLB5353470708, MLB3999624839 (feito antes), MLB3695643638.
| MLB3532534698 | Lilih2 | caimento Slim, estilos (2) |
| MLB3336732333 | Lilih2 | caimento Slim, estilos (2) |
| MLB3532522616 | Lilih2 | caimento Slim, estilos (2) |
| MLB3375267590 | Lilih2 | gestação Não (1) |
| MLB3272093035 | Lilih2 | gestação Não (1) |
| MLB3286413799 | Lilih2 | caimento Slim (1) |
| MLB3375303128 | Lilih2 | caimento Slim, estilos (2) |
| MLB3287257291 | Lilih2 | 5 campos de calça (5) |
| MLB3317557815 | Lilih2 | caimento Larga, estilos (2) |
| MLB3286381279 | Lilih2 | estilos (1) |
| MLB3286347431 | Lilih2 | formato Unidade, tipo Camiseta (2) |

Não preenchido: MLB3333720719 (Kit 2 tule, Lilih2) — falta só GTIN; kit não tem GTIN.
Lilih2 já completos: MLB3299441769, MLB3375315976, MLB3532490194, MLB3375318744.
| MLB4200005650 | Lilih2 | 5 de calça + reciclados Não, bolsos e punhos não se aplica (8) |
| MLB3466137888 | Lilih2 | 5 de calça (5) |
| MLB3431321155 | Lilih2 | copiado do irmão Lilih MLB3431379787: oversized n/a, rasgada Não, Elástico, Clássica, amarração na cintura (5) |
| MLB4287784546 | Lilih2 | gestação n/a, caimento Slim (2) |
| MLB4287633396 | Lilih2 | reciclados Não, esportes n/a (2) |
| MLB4287004642 | Lilih2 | reciclados Não, esportes n/a (2) |
| MLB3479931741 | Lilih2 | material Viscose, estilos (2) |
| MLB3431178435 | Lilih2 | pijama: fechamento, reciclados, gestante, lactante, personagem = não se aplica (5) |
Lilih2 já completos: MLB3443846360, MLB3897335584, MLB3899256586, MLB4243960166, MLB3894356538, MLB3407015681.

### Anúncios novos do ML (um anúncio por cor/tamanho, MLB5…/MLB7…)
Cada anúncio guarda a própria ficha: gravar em um não replica para os irmãos.
- Pantalona de poá (Lilih, 13 anúncios): fechamento Elástico, bainha Clássica, detalhes de design **Amarração na cintura** (valor que os irmãos MLB7868308232/228 já tinham; corrigi MLB7868346134 e MLB5446121327, que eu tinha posto "não se aplica"). MLB7868346098, 308232 e 308228 já estavam completos.
- Kit 2 blusa barra de renda (Lilih2): temporada Primavera/Verão, caimento Oversized, reciclados Não.
- Macacão um ombro (Lilih2): corte da parte inferior Palazzo.
- Kit 2 regatas franzido (Lilih e Lilih2): esportes recomendados não se aplica.

### Segunda varredura (anúncios fora da primeira lista)
| MLB | Loja | Gravado |
|---|---|---|
| MLB4534248772 | Lilih2 | vestido: fecho, bainha, design n/a; bordado Não; oversized Não (5) |
| MLB5150824720 | Lilih2 | vestido: fecho, bainha n/a; bordado Não; oversized Não; design Fenda (5) |
| MLB3540541977 | Lilih2 | reciclados Não, usos n/a (2) |
| MLB3892342861 | Lilih2 | reciclados Não, esportiva Não (2) |
| MLB5146671506 | Lilih2 | temporada P/V, reciclados Não, material Viscose, estilo Casual (4) |
| MLB5159772768 | Lilih2 | reciclados Não, esportiva Não (2) |
Já completos: MLB3539210297, MLB4350136166, MLB4699384000, MLB3713297335, MLB3817688341, MLB5046556994, MLB3842280713, MLB3845131433, MLB3891249859.
| MLB5301803366 | Lilih2 | temporada P/V (1) |
| MLB5301905100 | Lilih2 | temporada P/V (1) |
| MLB5314292586 | Lilih2 | pantalona 25128 Lilih2: 5 de calça iguais ao MLB3999624839 (5) |
Já completos: MLB3972059705, MLB5282339044, MLB5284065748, MLB5301752154, MLB5322829250, MLB5331671210, MLB5332667262, MLB4034118057, MLB4034281819, MLB4040163523, MLB5361773280, MLB5361863730.

### Fila (a conferir) — a Emori lista no máx. 30 por consulta
Lilih: MLB4057511369 MLB4057560493 MLB4136107593 MLB5698876604 MLB4206311487 MLB5708582758 MLB4209359729 MLB5901586428 MLB4555435111; família Kit 2 regatas alcinha poliamida (MLB4545…/MLB6486…, ~18); calça couro PU (MLB6507…).
Lilih2: MLB4040261241 MLB4040210765 MLB4056490465 MLB4057562677 MLB5419409998 MLB4087754349 MLB5420870952 MLB5459196832 MLB4106330791 MLB5459197852 MLB4106447107 MLB4144208721 MLB5694702112 MLB5694741732 MLB5694743494 MLB4203240969 MLB5708572296 MLB5708572740 MLB5708651300 MLB5715888168 MLB5783582112 MLB5903457252 MLB5904021562 MLB5904073144 MLB5904099438 MLB4345656329 MLB4470197971; família Kit 3 regatas alcinha (MLB6486…).

### Fila Lilih — feito
- MLB5698876604, MLB5708582758: temporada P/V. MLB4206311487: temporada P/V, material "Poliamida", estilo Casual.
- Jaqueta puffer (MLB4555435111 Lilih; MLB6511901512, MLB6511937910 Lilih2): impermeabilidade e tecnologia = não se aplica.
- Calça couro PU (MLB6507059996, MLB6507071962, MLB6507093846 Lilih; MLB6512268536, MLB6512355878, MLB6512268532 Lilih2): bainha Clássica, oversized Não, rasgada Não, design n/a. **Fechamento deixado vazio** (não sei se é zíper, botão ou elástico).
- Já completos: MLB4057511369, MLB4057560493, MLB4136107593, MLB4209359729, MLB5901586428, Kit 2 regatas alcinha poliamida (amostras MLB4545212733, MLB6486245928).

### Fila Lilih2 — feito
- Pantalonas de alfaiataria (MLB5419409998, MLB4144208721, MLB4470197971 + formato Unidade): bainha Clássica, oversized Não, rasgada Não, design n/a. **Fechamento deixado vazio** (alfaiataria: zíper/botão/elástico? confirmar).
- Regatas poliamida (MLB5694702112, MLB5694741732, MLB5694743494, MLB4203240969): esportes n/a, reciclados Não.
- Regatas caneladas (MLB5708572296, MLB5708572740 + material Ribana, MLB5708651300): temporada P/V, estilo Casual.
- Shorts alfaiataria MLB5783582112: grávidas Não, temporada P/V, reciclados Não. **Faltam composição, ano, cintura e caimento** (não sei).
- Conjunto cardigan+shorts Duna MLB5904073144: temporada P/V. **Falta composição.**
- Conjunto colete+shorts MLB5904099438: **faltam cintura do short e caimento** (não sei).
- Vestido longo Três Marias MLB4345656329: fecho, bainha n/a; bordado Não; oversized Não; design Camadas.
- Kit 3 regatas alcinha (MLB6486738924): gestação, reciclados, gola, usos = n/a (copiado do Kit 2 irmão MLB4545212733).
- Já completos: MLB4040261241, MLB4040210765, MLB4056490465, MLB4057562677, MLB4087754349, MLB5420870952, MLB5459196832, MLB4106330791, MLB5459197852, MLB4106447107, MLB5715888168, MLB5903457252, MLB5904021562.
- Kit 3 regatas alcinha Lilih2 (17 anúncios: MLB6486738924/751760/726776/751780/773562/751790/773574/773576/751798/751800/751802/773580/726840/738954, MLB4545575845/588529/626269): gestação, reciclados, gola, usos = n/a.

### Próxima fila (terceira varredura)
Lilih2: vestido gola alta MLB4558270449; camisa cetim MLB4558290965; vestido anarruga (MLB6512802742/793116/793120/824680/824660/824662, MLB4558923411); camisa jeans MLB4558932561; pantufas MLB4562010703 MLB4564088509 MLB4564213553 MLB4564124997; Kit 3 assimétrica poliamida (MLB4609…/MLB6624…); Kit 2 assimétrica (MLB4609789535 MLB6624740940 MLB4609717595 MLB6624579846 MLB6624740942 MLB6624791104).
Lilih: vestido anarruga (MLB4555886275/271, MLB4555852429); pantufa MLB6507192280; Kit 3/Kit 2/unit assimétrica poliamida (MLB6622…, MLB4608…, MLB6623…); tule marrom (MLB6674266586/394982/394984, MLB4636558345); courino wide leg (MLB4657165287/291, MLB4657153709, MLB6721183202); tule vinho (MLB6781832172/174, MLB6781806480, MLB4698390713).

### Terceira varredura — feito
- Vestido anarruga (Lilih MLB4555886275/271, MLB4555852429; Lilih2 MLB6512802742/793116/793120/824680/824660/824662, MLB4558923411): fecho e bainha n/a, bordado Não, oversized Não, design Franzido.
- Vestido gola alta com bolsos MLB4558270449: fecho, bainha, design n/a; bordado Não; oversized Não.
- Camisa jeans MLB4558932561: ocasiões Diário/Trabalho.
- Pantufa fechada MLB4562010703: personagem n/a. **Faltam material da sola e do calçado** (não sei).
- Calça courino wide leg (Lilih MLB4657165287/291, MLB4657153709, MLB6721183202; Lilih2 MLB4657192173/175, MLB4657171249/247): bainha Clássica, oversized Não, rasgada Não, design n/a (+ reciclados Não e punhos n/a onde vazios). **Fechamento deixado vazio.**
- Já completos: camisa cetim MLB4558290965, pantufa tiras MLB4564088509, blusas/kits assimétricos de poliamida (amostras), tule marrom e tule vinho (amostras).

## Resumo (16:48)
Cerca de 175 anúncios do ML revisados nas duas contas; uns 130 receberam atributos (todos conferidos pela Emori, nenhum recusado). Só preenchi campos vazios, nunca troquei valor existente (exceto a correção da poá que eu mesmo tinha gravado).

### O que ficou vazio de propósito (precisa de informação)
- Tipo de fechamento: calças couro PU (6), courino (8), pantalonas de alfaiataria (3 anúncios: MLB5419409998, MLB4144208721, MLB4470197971).
- Shorts alfaiataria MLB5783582112: composição, ano, cintura, caimento. Conjunto colete+shorts MLB5904099438: cintura, caimento. Conjunto cardigan+shorts Duna MLB5904073144: composição.
- Pantufa fechada MLB4562010703: material da sola e do calçado.
- GTIN de kits (Kit 2 tule MLB3333720719 e outros) — kit não tem GTIN; não inventei.
- Peso/medidas zerados (não é atributo, é embalagem): Combo 3 MLB3375318744, Kit 2 MLB3147208096, camiseta MLB3333283501, Kit 3 regatas MLB4285317166, Kit 2 regatas MLB4285166766, regata MLB5301803366, Kit 3 regatas MLB5159772768, pantufas, kits manga 3/4 e outros.
- Manga 3/4 MLB5353470708: mesmo GTIN em 12 variações.
- Pode haver mais anúncios ativos: a Emori só lista 30 por consulta; as famílias novas (MLB5…/MLB6…) foram conferidas por amostra.

### Pendências resolvidas pela descrição do anúncio (16:52)
- Calças de courino (8): fechamento Elástico ("elástico na cintura" na descrição).
- Pantalonas de alfaiataria MLB5419409998 ("elástico nas costas"), MLB4470197971 ("elástico na cintura") e Kit 2 MLB4144208721 (mesmo modelo e medidas da MLB5419409998): fechamento Elástico.
- Shorts alfaiataria MLB5783582112: composição 95% Poliéster e 5% Elastano; ano 2025 (anúncio de 10/2025).
- Pantufa fechada MLB4562010703: sola Borracha (TPR), material do calçado Poliéster.
Continuam vazios (a descrição não diz): fechamento das calças couro PU (descrição fala só em "estilo legging"); cintura e caimento dos shorts MLB5783582112 e do conjunto colete MLB5904099438; composição do conjunto cardigan Duna MLB5904073144 — **a descrição dele está copiada do conjunto colete Marram** (fala em colete e botões); corrigir a descrição.
