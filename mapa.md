# Mapa

Índice do que existe nesta pasta. Atualize ao criar uma pasta ou tipo de página novo.

## Repositório
- GitHub privado: https://github.com/danielhiraoka/maranne (branch `main`). Antes de trabalhar: `git pull`; depois: commit, `git pull --rebase`, `git push`.

## Regras
- `AGENTS.md` — regras da wiki para qualquer agente (Claude Code, Codex…). `CLAUDE.md` e `.agents/rules/maranne.md` (Antigravity) só apontam para ele.

- `.agents/agora.py` — data/hora de São Paulo e o arquivo de log do dia (usar antes de registrar)
- `.agents/configurar.py` — prepara um computador novo (Mac ou Windows): atalho de skills + `.venv`
- `.gitignore` / `.gitattributes` — o que não vai para o GitHub e fim de linha igual nos dois sistemas

## Comece por aqui
- `pendencias.md` — lista única do que está em aberto, com prazos e descontos ativos (ler no começo; dar baixa ao resolver)
- `regras-comerciais.md` — decisões em vigor de preço, promoção, ads e Amazon (ler antes de agir nesses temas)
- `.agents/indice.py` — linha do tempo de um SKU, anúncio, loja ou tema a partir das etiquetas do log (`python3 .agents/indice.py sku/2605084`)

## Wiki
- `guias/descricao-produto.md` — padrão de títulos, descrições, medidas, tecidos e kits (usado pelas skills de cadastro)
- `pessoas.md` — sócios, equipe, quem cuida de quê, contatos externos
- `precos/<data>_<loja>-<tema>-antes.csv` — preços salvos antes de uma mudança em lote (para poder voltar)
- `analises/<data>_<tema>.md` — análises de vendas, margem, promoções e ads (relatórios completos; o log aponta para elas)
- `log/AAAA/MM/` — diário de ações, análises e decisões (buscar por etiqueta)

## Ferramentas
- Skills ficam em `.agents/skills/` (`.claude/skills` é atalho)
- Skill `find-skills` (`.agents/skills/find-skills/`, da Vercel) — procura skills prontas no ecossistema (skills.sh) quando pedirem "tem skill para X?"; usa `npx skills` (precisa de Node)
- Skill `criar-combos` (`.agents/skills/criar-combos/`) — fotos de kits 3:4 para a Bagy a partir das fotos individuais
- Skill `criar-produto` (`.agents/skills/criar-produto/`) — cadastra produto novo no Bling (título, descrição no modelo, preços, cores × tamanhos, fiscal de produto parecido, GTIN) e organiza as fotos do ensaio no Drive
- Skill `criar-kit-bling` (`.agents/skills/criar-kit-bling/`) — cadastra kits no Bling a partir de um SKU com cores × tamanhos (padrão `<base>Kit21P`)
- Skill `vincular-amazon-bling` (`.agents/skills/vincular-amazon-bling/`) — vincula no Bling as variações de um anúncio novo da Amazon (código = SKU, pai sem vínculo)

## Arquivos de trabalho das skills
- `cadastros/<data>_<SKU>/` — entrada, descrição, plano e corpo enviado ao Bling de cada produto novo (`criar-produto`) e de cada kit (`criar-kit-bling`, pasta `<data>_<base>-kit<N>`). Até 11/11/2026 eram `produtos/` e `kits-bling/`; o log antigo cita esses nomes
- `combos/<data>_<nome>/` — fotos de entrada e de saída de cada kit montado (`criar-combos`); as fotos de referência de layout ficam em `.agents/skills/criar-combos/referencia/`

## Integrações (MCP)
Detalhes, quem precisa e como conectar em cada ferramenta: `integracoes.md`.
- **Emori** — análises e ações nos marketplaces (ML, Shopee, TikTok, Amazon)
- **Bling** (ERP) — produtos, variações, kits (composição), estoque, pedidos, NF-e. Não publica nos canais: isso é feito no Bling ou via Emori
- **NFE DAH** — ponte marketplaces ↔ Bling: vínculos produto↔loja e anúncios
