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
| NFE DAH | vínculos produto↔loja e anúncios no Bling (skill `vincular-amazon-bling`) | (conector NFE DAH) | daniel |
| Google Sheets | planilha de GTINs livres (Drive da empresa) | conector oficial Google Sheets | aline, daniel |
| Google Drive | fotos dos ensaios (pasta Maranne(Ensaios)) | conector oficial Google Drive | aline, daniel |

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

## Pasta de ensaios (fotos)

- Google Drive, pasta **Maranne(Ensaios)**, uma subpasta por ano. Link:
  https://drive.google.com/drive/folders/167Tg5BOFbPIbg8I9NDEJepjR5KNGGu3o
- Ids das pastas: Maranne(Ensaios) `167Tg5BOFbPIbg8I9NDEJepjR5KNGGu3o` · 2026 `1Z1ImfBRV7AugccY7gSx-hddDLld2gj7w` ·
  2025 `11VUVFLPwQ8FkC8FRoe_jgU0FREX7RNnD` · 2024 `1YL_1CGIq9BrmIuKmKJO-UsDgedNiadtl` · 2023 `1EPrPw2eHXO2pleqCY2e7ulgWB6G2aS9P`.
  Ano novo: crie a pasta do ano dentro de Maranne(Ensaios) e anote o id aqui.
- Acesso **só pelo conector Google Drive** (na nuvem). Não usar o app Google Drive para
  computador (Mac/Windows): o caminho muda em cada máquina.
- As fotos de um ensaio ficam numa pasta do Drive que o usuário indica, com uma subpasta
  por cor (ou a cor no nome do arquivo). O agente copia dentro do próprio Drive.
- Produto novo: `<ano>/<SKU> - <Nome>/` com `unitario/`, `kit/`, `promocional/`, `video/`.
  Fotos `cor-01.jpg` (a 01 é a capa); fotos de kit com o código da variação (`Kit21.jpg`).
  Pastas antigas por data de ensaio continuam como estão.
