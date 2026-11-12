# Maranne — cérebro da empresa

Maranne: confecção de roupas femininas e pijamas. Venda só online: site próprio (Bagy) e marketplaces (Mercado Livre, Shopee, TikTok, Amazon).

Esta pasta é uma **LLM wiki**: arquivos `.md` que o agente de IA (Claude, Codex, Antigravity…) escreve e mantém. A estrutura **cresce conforme o uso** — não criar pastas ou páginas "para o futuro"; só quando houver conteúdo real.

## Funciona em qualquer ferramenta
Este sistema é usado por Claude Code, Codex, Antigravity e outros agentes. Para não depender de nenhum:
- **Este `AGENTS.md` é a única fonte de regras.** `CLAUDE.md`, `.agents/rules/maranne.md` (Antigravity) e qualquer outro arquivo de ferramenta só apontam para cá — nunca escreva regras neles.
- **Skills ficam em `.agents/skills/<nome>/SKILL.md`** (padrão aberto Agent Skills). `.claude/skills` é só um atalho para essa pasta. Dentro de uma skill, não dependa de ferramentas exclusivas de um agente; se citar uma, diga a alternativa.
- **Conhecimento vai para a wiki, não para a memória interna do agente.** Decisões, preferências e regras aprendidas viram `.md` aqui (log, página ou skill), para que qualquer ferramenta e qualquer pessoa enxergue.
- MCPs são configurados **em cada ferramenta e por pessoa** (ver `integracoes.md`). Se faltar uma integração, avise e ofereça o caminho manual; não improvise.
- **Instalar skills de terceiros** (ex.: via `find-skills` / `npx skills`): sempre no projeto, em `.agents/skills/` — **nunca `-g`** (global não é compartilhado com a equipe). Antes, leia o SKILL.md e os scripts e mostre ao usuário o que fazem; instale só com o OK dele. Depois, registre no log (`#tema/skills`) e no `mapa.md`.

## Funciona em Mac e Windows
- **Computador novo:** rode `python3 .agents/configurar.py` (Mac) ou `py .agents/configurar.py` (Windows). Cria o atalho de skills e o `.venv`. Se `.claude/skills` ou `.venv` não existirem, rode-o antes de usar uma skill.
- **Nomes de arquivo e pasta:** minúsculas, sem acento, sem espaço (use `-`), nunca `: * ? " < > | \`. Dois nomes que só diferem em maiúscula/minúscula viram o mesmo arquivo no Windows.
- **Scripts de skill em Python** (com `pathlib`), não em bash ou PowerShell. Comandos nos SKILL.md numa linha só, sem `&&`, heredoc ou `\` de continuação.
- **Python do `.venv`:** `.venv/bin/python` no Mac, `.venv\Scripts\python.exe` no Windows.
- Textos em UTF-8; fim de linha controlado pelo `.gitattributes`.

Equipe e responsabilidades: `pessoas.md` — use os apelidos de lá no log e para direcionar tarefas.

## Como consultar (economizar tokens)
1. Comece pelo `mapa.md` (índice curto) e pelo `pendencias.md` (o que está em aberto). Se o pedido do usuário toca numa pendência, diga isso a ele.
2. Antes de propor ou executar preço, promoção, ads ou anúncio na Amazon: leia `regras-comerciais.md`.
3. Para SKU/anúncio/loja/tema: `python3 .agents/indice.py <etiqueta>` (ex.: `sku/2605084`, `loja/amazon`) dá a linha do tempo no log; com `-c`, o texto completo. Sem argumentos, lista as etiquetas. Windows: `py .agents/indice.py`.
4. Nunca ler pastas inteiras.

## Como registrar
Registre sempre que algo for **alterado** ou uma **análise/decisão** relevante for feita — via MCP, à mão ou contado pelo usuário ("subi a promoção ontem"). Consultas triviais não precisam.

### Marcos — registro obrigatório, na hora
Quando acontecer um destes, **registrar faz parte da ação**: logo depois de executar (ou de o usuário contar), antes de seguir para outra coisa. Na resposta, diga "registrado no log".

| Marco | Etiqueta | O que registrar |
|---|---|---|
| Cadastro de produto ou kit | `#tema/cadastro` | SKU pai, nº de variações, preço, ids, o que ficou pendente |
| Alteração de cadastro (título, descrição, fotos, fiscal, GTIN) | `#tema/cadastro` | campo, antes → depois |
| **Preço** | `#tema/precos` | SKU/anúncio, loja, antes → depois, margem se houver, motivo, quem aprovou |
| **Promoção / cupom / desconto** (entrar, sair, criar) | `#tema/promocoes` | promoção, SKUs/anúncios, %/preço, período, loja |
| **Ads / tráfego pago** (campanha criada, orçamento, pausa, ACOS/ROAS alvo) | `#tema/ads` | campanha, plataforma, antes → depois, motivo |
| Status de anúncio (ativar, pausar, inativar) | `#tema/anuncios` | anúncio/SKU, loja, motivo |
| Estoque / reposição / produção | `#tema/estoque` | SKU, quantidade, decisão |
| Decisão de negócio ou regra nova | `#tema/<assunto>` | decisão e o porquê |

Sempre com as etiquetas do item (`#sku/`, `#mlb/`, `#loja/`…) para achar depois.

### Ao encerrar uma tarefa
Antes de dar a tarefa por concluída:
1. Registre no log o que foi feito.
2. Atualize o `pendencias.md`: **apague** o que foi resolvido e **acrescente** o que ficou em aberto (uma linha: data · quem · o que falta → log de origem; com prazo, na seção "Com data"). É por ele que a próxima conversa — ou outra pessoa — continua. Não escreva mais linha `Pendente:` no log.
3. Nada do que é preciso para continuar pode ficar em arquivo temporário da conversa (scratchpad): salve nesta pasta (`cadastros/`, `precos/`, `analises/`).
4. Se nasceu ou mudou uma regra de preço, promoção, ads ou Amazon, atualize `regras-comerciais.md`.

Depois pergunte se pode enviar ao GitHub; com OK: `git add -A`, commit, `git pull --rebase`, `git push` (nessa ordem). Não envie sem OK.

**Data e hora: sempre de São Paulo (UTC−3).** Antes de registrar, rode `python3 .agents/agora.py` (Windows: `py .agents/agora.py`) — ele dá a hora e o arquivo do dia. Nunca estime a hora.

**Log do dia** em `log/AAAA/MM/AAAA-MM-DD.md` (só acrescentar, nunca reescrever entradas antigas):

```
## HH:MM · <pessoa> · <tipo: alteração | análise | decisão | cadastro | nota>
<etiquetas>
<o que foi feito, valores antes → depois, motivo, fonte (ex.: MCP Emori)>
```

**Etiquetas** (sempre neste formato, minúsculas exceto IDs):
`#sku/<SKU>` · `#mlb/<MLB...>` · `#shopee/<item_id>` · `#tiktok/<id>` · `#amazon/<ASIN>` · `#loja/<apelido>` · `#tema/<assunto>`
Apelidos de loja: `ml-lilih`, `ml-lilih2`, `shopee-maranne`, `tiktok-maranne`, `amazon`, `site-bagy`.

**Linha do tempo de uma entidade** (SKU, anúncio, loja): não se escreve à mão — sai do log pelas etiquetas, com `.agents/indice.py`. Por isso as etiquetas do item são obrigatórias em toda entrada.

**Páginas de entidade** (loja, fornecedor, produto…): crie só quando houver um **resumo que valha guardar** e que o log não dá de pronto (ex.: particularidades de uma loja, histórico de um fornecedor). A página guarda o estado atual, não a linha do tempo.

Ao criar uma pasta ou tipo de página novo, adicione uma linha no `mapa.md`.

## Regras
- **LGPD:** nunca gravar nome, CPF, endereço, telefone ou e-mail de clientes. Só nº do pedido e valores.
- Não duplicar números que a Emori/Bling já guardam; registrar o que foi feito, por quê e o resultado.
- Ações que alteram marketplace/ERP: confirmar com o usuário antes de executar.
- **Antes de criar qualquer produto no Bling**, confira que nenhum SKU que vai ser criado (pai e variações) já existe: `listProducts` com `codigos` e `criterio: "5"`. Se existir, não crie — mostre e pergunte.
- **SKU de kit:** pai `<SKU base>Kit<N>` (N = nº de peças: Kit2, Kit3, Kit5); variações `<SKU base>Kit<N><combinação><tamanho>` (Kit21P, Kit22M… / Kit51G, Kit52G…). Detalhes na skill `criar-kit-bling`.
