---
name: converter-heic
description: Converte fotos .HEIC/.HEIF (formato do iPhone) para .JPG no Mac e no Windows. Abre a caixa do sistema para o usuário escolher várias fotos e salva os .jpg numa subpasta "jpg" dentro da pasta das fotos. Use quando pedirem para converter HEIC, "transformar as fotos do iPhone em JPG", "a foto não abre / o Bling ou o marketplace não aceita HEIC", ou quando uma pasta de fotos de ensaio tiver arquivos .heic, mesmo sem dizer "skill".
---

# Converter HEIC para JPG

O script `scripts/heic_para_jpg.py` faz tudo. Rode a partir da raiz do projeto,
numa linha só. `<python>` é o Python do `.venv`: `.venv/bin/python` no Mac,
`.venv\Scripts\python.exe` no Windows.

**Dois cliques, sem terminal** (para a equipe usar sozinha): na raiz do projeto,
`converter-heic.command` no Mac e `converter-heic.bat` no Windows. Os dois só chamam
o script abaixo; a regra fica toda no Python.

**Com a caixa de seleção** (o padrão: o usuário escolhe as fotos):

```
<python> .agents/skills/converter-heic/scripts/heic_para_jpg.py
```

A caixa abre na tela do usuário e o comando fica esperando ele escolher. Avise
antes de rodar ("abri a caixa, escolha as fotos") e rode sem limite curto de tempo.
Se ele cancelar, o script termina com "nenhuma foto escolhida".

**Sem caixa** (quando o usuário já disse a pasta ou os arquivos):

```
<python> .agents/skills/converter-heic/scripts/heic_para_jpg.py "<pasta ou arquivo>"
```

Aceita várias pastas e arquivos; numa pasta, pega também as subpastas. Caminho com
espaço vai entre aspas.

## O que ele faz

- Salva os `.jpg` na subpasta **`jpg`**, criada dentro da pasta onde as fotos estão
  (`ensaio/IMG_0001.HEIC` → `ensaio/jpg/IMG_0001.jpg`).
- **Não apaga o original.** Só apague os `.heic` se o usuário pedir, depois de ele conferir os `.jpg`.
- Foto que já tem `.jpg` na subpasta é pulada: pode repetir com as mesmas fotos.
- As cores são convertidas de Display P3 (iPhone) para sRGB, para não saírem lavadas nas lojas.
- O `.jpg` sai **sem EXIF** (a foto do celular leva o GPS de onde foi tirada). A foto já sai em pé.
- Qualidade 92, tamanho original. Não redimensiona.

No fim ele diz quantas converteu, quantas pulou, onde salvou e quais deram erro
(uma foto ruim não para o lote). Repasse esse resumo ao usuário.

## Limites

- Só arquivos **no computador**. Fotos que estão só no Google Drive: peça para baixar
  a pasta (ou usar a pasta do Drive para computador).
- Live Photo e HEIC com várias imagens: converte só a imagem principal.
- A caixa usa o `osascript` no Mac e o `tkinter` no Windows (vem com o Python do python.org).
  No Mac ela mostra todos os arquivos, sem filtro: o filtro por extensão deixava as fotos
  cinza. Se escolherem outro tipo de imagem (PNG, WebP), ela também vira `.jpg`.
- No Mac, se o duplo clique for bloqueado ("não pode ser aberto"): clique com o botão
  direito no `converter-heic.command` → Abrir.
- Se der `No module named 'pillow_heif'`: rode `python3 .agents/configurar.py`
  (Windows: `py .agents/configurar.py`).

Conferir o script: `<python> .agents/skills/converter-heic/scripts/heic_para_jpg.py --teste`
