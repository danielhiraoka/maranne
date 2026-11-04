# Mapa

Índice do que existe nesta pasta. Atualize ao criar uma pasta ou tipo de página novo.

## Repositório
- GitHub privado: https://github.com/danielhiraoka/maranne (branch `main`). Antes de trabalhar: `git pull`; depois: commit, `git pull --rebase`, `git push`.

## Regras
- `AGENTS.md` — regras da wiki para qualquer agente (Claude Code, Codex…). `CLAUDE.md` e `.agents/rules/maranne.md` (Antigravity) só apontam para ele.

- `.agents/agora.py` — data/hora de São Paulo e o arquivo de log do dia (usar antes de registrar)
- `.agents/configurar.py` — prepara um computador novo (Mac ou Windows): atalho de skills + `.venv`
- `.gitignore` / `.gitattributes` — o que não vai para o GitHub e fim de linha igual nos dois sistemas

## Wiki
- `guias/descricao-produto.md` — padrão de títulos, descrições, medidas, tecidos e kits (usado pelas skills de cadastro)
- `pessoas.md` — sócios, equipe, quem cuida de quê, contatos externos
- `analises/<data>_<tema>.md` — análises de vendas, margem, promoções e ads (relatórios completos; o log aponta para elas)
- `log/AAAA/MM/` — diário de ações, análises e decisões (buscar por etiqueta)

## Ferramentas
- Skills ficam em `.agents/skills/` (`.claude/skills` é atalho)
- Skill `find-skills` (`.agents/skills/find-skills/`, da Vercel) — procura skills prontas no ecossistema (skills.sh) quando pedirem "tem skill para X?"; usa `npx skills` (precisa de Node)
- Skill `criar-combos` (`.agents/skills/criar-combos/`) — fotos de kits 3:4 para a Bagy a partir das fotos individuais
- Skill `criar-produto` (`.agents/skills/criar-produto/`) — cadastra produto novo no Bling (título, descrição no modelo, preços, cores × tamanhos, fiscal de produto parecido, GTIN) e organiza as fotos do ensaio no Drive
- `produtos/<data>_<SKU>/` — entrada, descrição, plano e corpo enviado ao Bling de cada produto novo
- Skill `criar-kit-bling` (`.agents/skills/criar-kit-bling/`) — cadastra kits no Bling a partir de um SKU com cores × tamanhos (padrão `<base>Kit21P`)
- Skill `vincular-amazon-bling` (`.agents/skills/vincular-amazon-bling/`) — vincula no Bling as variações de um anúncio novo da Amazon (código = SKU, pai sem vínculo)
- `kits-bling/<data>_<base>-kit<N>/` — entrada, plano e corpo enviado ao Bling de cada kit
- `combos/<data>_<nome>/` — entradas e saídas de cada kit montado
- `entrada/`, `saida/`, `referencia/` — arquivos soltos da skill de kits (referência de layout)

## Integrações (MCP)
Detalhes, quem precisa e como conectar em cada ferramenta: `integracoes.md`.
- **Emori** — análises e ações nos marketplaces (ML, Shopee, TikTok, Amazon)
- **Bling** (ERP) — produtos, variações, kits (composição), estoque, pedidos, NF-e. Não publica nos canais: isso é feito no Bling ou via Emori
- **NFE DAH** — ponte marketplaces ↔ Bling: vínculos produto↔loja e anúncios
