# Mapa

Índice do que existe nesta pasta. Atualize ao criar uma pasta ou tipo de página novo.

## Repositório
- GitHub privado: https://github.com/danielhiraoka/maranne (branch `main`). Antes de trabalhar: `git pull`; depois: commit + `git push`.

## Regras
- `AGENTS.md` — regras da wiki para qualquer agente (Claude Code, Codex…). `CLAUDE.md` e `.agents/rules/maranne.md` (Antigravity) só apontam para ele.

- `.agents/agora.py` — data/hora de São Paulo e o arquivo de log do dia (usar antes de registrar)
- `.agents/configurar.py` — prepara um computador novo (Mac ou Windows): atalho de skills + `.venv`
- `.gitignore` / `.gitattributes` — o que não vai para o GitHub e fim de linha igual nos dois sistemas

## Wiki
- `pessoas.md` — sócios, equipe, quem cuida de quê, contatos externos
- `log/AAAA/MM/` — diário de ações, análises e decisões (buscar por etiqueta)

## Ferramentas
- Skills ficam em `.agents/skills/` (`.claude/skills` é atalho)
- Skill `find-skills` (`.agents/skills/find-skills/`, da Vercel) — procura skills prontas no ecossistema (skills.sh) quando pedirem "tem skill para X?"; usa `npx skills` (precisa de Node)
- Skill `criar-combos` (`.agents/skills/criar-combos/`) — fotos de kits 3:4 para a Bagy a partir das fotos individuais
- Skill `criar-kit-bling` (`.agents/skills/criar-kit-bling/`) — cadastra kits no Bling a partir de um SKU com cores × tamanhos (padrão `<base>Kit21P`)
- `kits-bling/<data>_<base>-kit<N>/` — entrada, plano e corpo enviado ao Bling de cada kit
- `combos/<data>_<nome>/` — entradas e saídas de cada kit montado
- `entrada/`, `saida/`, `referencia/` — arquivos soltos da skill de kits (referência de layout)

## Integrações (MCP)
Detalhes, quem precisa e como conectar em cada ferramenta: `integracoes.md`.
- **Emori** — análises e ações nos marketplaces (ML, Shopee, TikTok, Amazon)
- **Bling** (ERP) — produtos, variações, kits (composição), estoque, pedidos, NF-e. Não publica nos canais: isso é feito no Bling ou via Emori
