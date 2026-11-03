# Integrações

Cada integração (MCP/conector) é ligada **por ferramenta e por pessoa**. Conectar no Claude
não conecta no ChatGPT/Codex nem no Antigravity, e o login de um funcionário não vale para
outro. As regras e skills desta pasta funcionam em todas as ferramentas; as integrações, não.

**Para o agente:** se uma skill precisa de uma integração que não aparece nas suas
ferramentas, não improvise — diga ao usuário qual falta, aponte esta página e ofereça o
caminho manual (ex.: pedir o GTIN para a pessoa colar no chat).

## O que existe

| Integração | Para quê | Endereço (MCP) | Quem precisa |
|---|---|---|---|
| Emori | análises e ações nos marketplaces (ML, Shopee, TikTok, Amazon) | `https://emori.com.br/mcp` | daniel, aline |
| Bling | ERP: produtos, kits, estoque, pedidos, NF-e | (conector do Bling) | aline, daniel |
| Google Sheets | planilha de GTINs livres (Drive da empresa) | conector oficial Google Sheets | aline, daniel |

## Como conectar em cada ferramenta

- **Claude (Code ou app):** Configurações → Conectores, ou no terminal
  `claude mcp add --transport http <nome> <endereço>`; depois faça login quando pedir.
- **ChatGPT / Codex:** Codex CLI em `~/.codex/config.toml` (seção `[mcp_servers.<nome>]`
  com a `url`); no app do ChatGPT, em Configurações → Conectores/Apps.
- **Antigravity:** painel de MCP Servers nas configurações do agente.

Cada pessoa faz o próprio login. Senhas e tokens nunca entram nesta pasta.

## Planilha de GTIN

Fica no Google Drive da empresa e **não** é copiada para cá (evita expor e evita duas
versões). Quem cria kits precisa de: (1) acesso à planilha no Drive e (2) o conector
Google Sheets ligado na sua ferramenta. Sem isso, a skill `criar-kit-bling` cria o kit sem
GTIN e avisa — a pessoa preenche no Bling e marca na planilha à mão.

- Planilha **GTIN**, aba `Página1`, id `1ymXEY3gnNw6QRvtF90IP4I55ibOsYWefmstOS2TVQCw`
  (link: https://docs.google.com/spreadsheets/d/1ymXEY3gnNw6QRvtF90IP4I55ibOsYWefmstOS2TVQCw)
- Coluna **A** = EAN · coluna **B** = SKU que usou o EAN (linha 1 é cabeçalho).
- Usar sempre a partir da **primeira linha depois da última com SKU** (em 02/11/2026: última
  usada 3270 → livre a partir da 3271). Há linhas em branco antigas antes disso: não usar.
- Antes de usar, conferir no Bling se o EAN não está em nenhum produto.
- Só escrever o SKU na coluna B depois que o produto foi criado no Bling.
