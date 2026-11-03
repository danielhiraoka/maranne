---
name: criar-combos
description: Monta fotos de combos/kits de roupas da Maranne a partir de fotos individuais de cada peça (modelo vestindo a peça). Remove o fundo, recorta as modelos e sobrepõe 2 a 6 delas lado a lado em fundo branco 3:4 para a loja Bagy, gerando todas as combinações possíveis. Use sempre que o usuário colar fotos de peças no chat e falar em combo, kit, "kit de 2/3/5", montar foto de conjunto, juntar modelos numa foto só ou foto de kit para a Bagy, mesmo que não diga "skill" nem "combo".
---

# Criar combos

Transforma fotos individuais de peças em fotos de kit: as modelos ficam
recortadas e sobrepostas, como nas fotos de referência em `referencia/`.
Toda a parte pesada (recorte, alinhamento, layout) está no script
`scripts/montar_kits.py`. Seu trabalho é organizar as fotos, rodar o script e
mostrar o resultado.

## Quantos kits saem

O script gera **todas as combinações** de N peças entre as enviadas, ou seja,
C(total, N):

| Peças enviadas | Kit de 2 | Kit de 3 | Kit de 5 |
|---|---|---|---|
| 2 | 1 | – | – |
| 3 | 3 | 1 | – |
| 4 | 6 | 4 | – |
| 5 | 10 | 10 | 1 |
| 6 | 15 | 20 | 6 |

Antes de rodar, diga ao usuário quantos kits vão sair. Se forem mais de 20,
confirme antes: são muitas fotos para revisar, e talvez ele queira só alguns
(nesse caso, rode uma vez por grupo de peças).

## Passo a passo

### 1. Entender o pedido

Você precisa de duas coisas: as fotos e o tamanho do kit (2 a 6). Se ele não
disse o tamanho, pergunte. Se ele quiser uma peça específica na frente,
anote.

As fotos coladas no chat aparecem com o caminho do arquivo, no formato
`[Image: source: /caminho/para/N.webp]`. Use esses caminhos.

Olhe cada imagem. Cada uma deve ser **uma modelo vestindo uma peça**, de
frente, com o rosto visível, porque o alinhamento é feito pelo rosto. Se
alguma for um kit pronto (várias modelos), uma foto sem modelo ou uma foto de
costas, avise e pergunte o que fazer, em vez de rodar.

### 2. Organizar as fotos

Crie uma pasta de trabalho na raiz do projeto:

```
combos/<AAAA-MM-DD>_<nome-curto>/entrada/
```

Use a data de hoje e um nome que descreva o produto, por exemplo
`combos/2026-10-29_regata-alcinha/`. Copie cada foto para `entrada/` com um
nome descritivo e um número na frente, na ordem em que vieram no chat:

```
1_regata_branca.webp
2_regata_preta.webp
3_regata_nude.webp
```

**Por que o número:** em cada kit, a peça com o menor número vai para a
posição da frente (a da esquerda no kit de 2; a do meio a partir do kit de 3).
Se o usuário pediu uma peça na frente, dê o número 1 para ela. O nome serve
para os arquivos de saída serem legíveis (`kit_1_regata_branca+2_regata_preta.jpg`),
então descreva a peça pela cor e pelo tipo que você vê na foto.

### 3. Rodar

Rode a partir da raiz do projeto, numa linha só (funciona no Mac e no
Windows). `<python>` é o Python do `.venv`: `.venv/bin/python` no Mac,
`.venv\Scripts\python.exe` no Windows.

```
<python> .agents/skills/criar-combos/scripts/montar_kits.py --entrada combos/<pasta>/entrada --saida combos/<pasta>/saida --tamanho <N>
```

A primeira vez numa máquina pode demorar: o modelo de recorte (BiRefNet-portrait,
~1 GB) é baixado para `~/.rembg/`. Depois disso, leva poucos segundos por foto.
Os recortes ficam em `saida/_recortes/` e são reaproveitados se você rodar de
novo na mesma pasta. Se trocar uma foto de entrada, apague o recorte dela.

Se o `.venv` não existir, rode antes o configurador da pasta
(`python3 .agents/configurar.py` no Mac, `py .agents/configurar.py` no Windows).

### 4. Conferir e entregar

Abra cada kit gerado (com Read) e confira antes de mostrar:

- **Recorte:** nenhum pedaço de fundo sobrando, e nenhum contorno claro no
  cabelo onde uma modelo passa por cima da outra.
- **Rostos:** todos do mesmo tamanho e na mesma altura. Se um rosto ficou
  muito diferente, a detecção de rosto provavelmente falhou nessa foto. Avise
  e sugira outra foto.
- **Corpo até embaixo:** as modelos devem chegar na borda inferior.
- **Peça de trás visível:** se a modelo da frente estiver com a mão na
  cintura ou o braço aberto, o cotovelo pode cobrir a blusa da modelo de
  trás, e aí o kit não mostra o produto. Nesse caso, gere aquele kit de novo
  com a ordem invertida (a outra peça na frente), reaproveitando os recortes,
  e apague a versão ruim:

  ```
  <python> .agents/skills/criar-combos/scripts/montar_kits.py --entrada combos/<pasta>/entrada --saida combos/<pasta>/saida --ordem <peca_da_frente>,<peca_de_tras>
  ```

  Conte ao usuário que inverteu e por quê.

Depois envie os kits ao usuário (no Claude Code, com SendUserFile; em outras ferramentas, mostre os caminhos) e diga onde estão
(`combos/<pasta>/saida/`). Se algo não ficou bom, diga o que foi e por quê,
em vez de só entregar.

## Ajustes disponíveis

| Opção | Padrão | Para quê |
|---|---|---|
| `--tamanho` | 2 | peças por kit (2 a 6 têm layout calibrado) |
| `--largura` / `--altura` | 960 / 1280 | tamanho da foto final (3:4, Bagy) |
| `--base` | `ampliar` | `ampliar` aumenta as modelos até o corpo chegar embaixo; `desvanecer` mantém o tamanho e some a base no branco. O usuário escolheu `ampliar`. |
| `--modelo` | `birefnet-portrait` | modelo de recorte do rembg; `bria-rmbg` é a alternativa que empatou nos testes |

Os layouts (posição de cada modelo, quem fica na frente, tamanho do rosto)
estão no dicionário `LAYOUTS` do script, medidos nas referências em
`referencia/`. Se o usuário mandar uma referência nova de kit, meça os rostos
dela (o script tem o detector de rosto) e ajuste o layout daquele tamanho.

## Limitação conhecida: enquadramento das fotos

Nas referências, as fotos individuais mostram o corpo até o joelho. Quando a
foto termina no meio da coxa, o modo `ampliar` aumenta as modelos (~20%) para
o corpo chegar na borda, e os rostos ficam maiores que na referência. Isso
pesa mais nos kits de 5 e 6, em que as modelos das pontas ficam muito
cortadas. Se o usuário reclamar do tamanho, explique isso e recomende
fotografar até o joelho.
