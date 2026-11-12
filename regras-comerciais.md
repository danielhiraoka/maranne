# Regras comerciais

Decisões **em vigor** sobre preço, promoção, ads e Amazon. Leia antes de propor ou executar qualquer uma dessas ações.

- Regra nova ou mudada: edite aqui e registre no log (`#tema/<assunto>`, tipo `decisão`). Cada regra aponta para o log onde nasceu.
- Aqui só entra o que vale daqui para frente. Decisão pontual (um anúncio, uma data) fica só no log.
- Regras de cadastro, título e descrição ficam em `guias/descricao-produto.md` e nas skills.

## Preço

- Mudança de preço em qualquer loja só com aprovação do **daniel** (ver `pessoas.md`).
- Mudança em lote: antes de alterar, salvar os preços atuais em `precos/<data>_<loja>-<tema>-antes.csv` e registrar no log o caminho do CSV. → log 2026-11-11 09:57
- Desconto com prazo: anotar a data de fim em `pendencias.md` ("Com data"). Sem prazo definido: anotar em "Descontos ativos sem data de fim".
- Bagy: o preço fica nas variações e no produto pai. Para a vitrine mostrar "de X por Y", o pai precisa do preço novo e do preço "de". → log 2026-11-11 11:16

## Promoções (ML e Shopee)

- Só aderir se a **margem depois do desconto, já com o Ads da última semana, ficar em 15% ou mais** (alvo perto de 20%). Mostrar a simulação antes de aderir. → log 2026-11-03 12:47 e 2026-11-04 19:58
- ML, ofertas DEAL (11.11, Black Friday): os 13% são sugestão; o desconto pode ser editado até cerca de 3%. Quando 13% não fecha a margem, usar o mínimo (3%). Nas Smart (Moda, Impulsione) o desconto é fixo. → log 2026-11-03 14:41
- Kits no ML: entrar com 3% nas DEAL. → log 2026-11-03 14:50 e 20:20
- Se a margem cai abaixo de 15% por causa do Ads, o caminho é baixar o ACOS alvo da campanha, não sair da promoção. → log 2026-11-03 14:50
- Shopee: o desconto criado pela Emori dura 30 dias por padrão; campanhas da plataforma só pelo Seller Center. → log 2026-11-03 12:47

## Tipo de anúncio no ML

- Premium paga 19% e Clássico 14%. Preferir Clássico quando a margem está apertada. → log 2026-11-03 14:41
- A Emori não troca o tipo; a troca é no painel do ML, e o ML pode recusar. → log 2026-11-03 14:50 e 20:08

## Ads

- Ads na Emori é só leitura: mudanças de campanha, orçamento e ACOS são feitas no painel de cada plataforma e contadas aqui para registro. → log 2026-11-06 15:09

## Amazon

- Anúncios novos entram por clone (Emori) de um anúncio do ML, Shopee ou TikTok; depois, vínculo no Bling pela skill `vincular-amazon-bling`.
- **Preço = o do Mercado Livre**, não a sugestão da Emori. Sem anúncio no ML: preço do canal de origem, igual ao do Bling. → log 2026-11-05 15:47 e 2026-11-06 00:01
- Atributos padrão: faixa etária Adulto; cuidados Lavagem à máquina; tamanho especial Padrão; cores pela composição do Bling. → log 2026-11-04 20:27 e 2026-11-05 15:47
- GTIN: enviar **sem GTIN** (isenção). Nunca aceitar troca de model_number que ligue a peça a um ASIN de terceiro. A isenção ainda precisa ser conferida no Seller Central (ver `pendencias.md`). → log 2026-11-05 16:24
- Envio que demora ou dá timeout: **não reenviar**; conferir antes no Seller Central ou na Emori se o anúncio foi criado. → log 2026-11-05 11:24
