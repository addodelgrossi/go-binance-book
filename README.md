# Robôs de Trade com Go e Binance para Iniciantes

Repositório do livro **Robôs de Trade com Go e Binance para Iniciantes** e do projeto Go que acompanha o ebook.

O livro é um guia educativo em português do Brasil para criar um robô simples usando Go, Binance Spot Testnet e uma estratégia de cruzamento de médias móveis. Ele foi pensado como um primeiro teste de publicação na Amazon KDP em **dois formatos: Kindle eBook e paperback impresso**, sem promessa de lucro e sem operação com dinheiro real.

## Retomando o projeto

Se você abrir este repositório em uma nova conversa com Codex/ChatGPT ou em outro editor, comece por:

1. `docs/CONTEXTO_DO_PROJETO.md`
2. `docs/PUBLICACAO_KDP.md`
3. `docs/VALIDACAO.md`
4. `manuscrito/robo-trade-go-binance-manuscrito.md`

O arquivo de contexto guarda as decisões principais, estado atual, limitações conhecidas e próximos passos para não depender do histórico desta conversa.

## Estrutura

- `manuscrito/`: fonte principal do livro em Markdown.
- `dist/`: artefatos finais para revisão/publicação: EPUB, DOCX, PDFs e ZIP do código.
- `assets/`: capa do Kindle em JPG 1600x2560.
- `kdp/`: metadados sugeridos para cadastro no KDP.
- `codigo-robo-go-binance/`: projeto Go do robô educativo.
- `scripts/`: gerador local de EPUB/DOCX/PDFs/capas/ZIP.
- `docs/`: contexto, checklist de publicação, validação e roadmap.

## Tabela-mestra de publicação KDP

Tudo que existe no projeto e onde cada arquivo entra no KDP. O ZIP do código **não** é enviado ao KDP; ele é material de apoio para o leitor.

| Arquivo | Formato | Especificações | Onde usar no KDP | Status |
| --- | --- | --- | --- | --- |
| `dist/robo-trade-go-binance.epub` | EPUB 3 | UTF-8, sumário navegável, capa nos metadados | **Kindle eBook → campo "Manuscrito"** | Gerado por `make build` |
| `assets/capa-robo-trade-go-binance.jpg` | JPG | 1600×2560 px, proporção 1.6:1, RGB/sRGB, < 50 MB, só frente, sem sangria | **Kindle eBook → campo "Capa"** (upload separado) | Gerado por `make build` |
| `dist/robo-trade-go-binance.docx` | DOCX | Calibri, títulos, blocos de código mono | Alternativa: importar no **Kindle Create** e exportar KPF | Gerado por `make build` |
| `dist/robo-trade-go-binance-print-6x9.pdf` | PDF | **6×9"** (432×648 pt), P&B, papel branco, 300 DPI, sem sangria, margens espelhadas (gutter), **sem capa** | **Paperback → campo "Manuscrito (miolo)"** | Gerado por `make build` |
| `dist/robo-trade-go-binance-capa-print.pdf` | PDF | Capa **wraparound** (contracapa + lombada + frente), 300 DPI, sangria 0,125", lombada calculada pela contagem de páginas | **Paperback → campo "Capa"** | Gerado por `make build` |
| `dist/robo-trade-go-binance-revisao.pdf` | PDF | 5×8", **com capa embutida** | Somente leitura/revisão de tela — **NÃO usar no upload** | Gerado por `make build` |
| `dist/codigo-robo-go-binance.zip` | ZIP | Projeto Go completo | Material de apoio ao leitor — **NÃO é upload KDP** | Gerado por `make build` |
| `kdp/metadados-kdp.md` | Markdown | Título, subtítulo, descrição, palavras-chave, categorias | Preenche os campos do formulário do KDP (ambos os formatos) | Mantido à mão |

## Passo a passo de publicação

### A. Kindle eBook

1. Rode `make build` e depois `make validate`.
2. Abra `dist/robo-trade-go-binance.epub` no **Kindle Previewer** e confira sumário, blocos de código, acentos e quebras em tela pequena.
3. No KDP, crie um novo **Kindle eBook**.
4. Preencha título, subtítulo, autor, descrição, palavras-chave e categorias usando `kdp/metadados-kdp.md`.
5. Marque o **disclosure de conteúdo gerado por IA** (texto e capa) se publicar esta versão como está.
6. Envie o manuscrito: `dist/robo-trade-go-binance.epub`.
7. Envie a capa: `assets/capa-robo-trade-go-binance.jpg`.
8. Use o **Previewer online do KDP** para a conferência final.
9. Defina preço (sugerido R$ 9,90) e publique. KDP Select: não inscrever no primeiro lançamento.

### B. Paperback impresso

1. Rode `make build` e depois `make validate` (a validação confere trim, contagem de páginas e dimensão da capa).
2. No KDP, crie um novo **Paperback** (pode ser vinculado ao mesmo título do eBook).
3. Em opções de impressão, escolha: **papel branco**, **interior em preto e branco**, tamanho de corte (trim) **6×9 pol (15,24 × 22,86 cm)**.
4. ISBN: use o **ISBN grátis fornecido pelo KDP** (ou informe o seu).
5. Envie o miolo: `dist/robo-trade-go-binance-print-6x9.pdf`.
6. Envie a capa: `dist/robo-trade-go-binance-capa-print.pdf`.
7. Confira tudo no **Visualizador de Impressão** do KDP (margens, lombada, sangria, gutter).
8. Defina o preço de lista (o KDP mostra o custo de impressão e a royalty estimada) e publique.

> Boa prática: antes de finalizar a capa impressa, gere o **template oficial** no KDP Cover Calculator (informando trim, contagem de páginas e tipo de papel) e confira se as dimensões batem com `dist/robo-trade-go-binance-capa-print.pdf`.

## O que você precisa saber (pontos fáceis de esquecer)

- **Capa vs thumbnail**: você só envia a **capa**. O *thumbnail* (miniatura na loja) é gerado automaticamente pela Amazon a partir da capa. Não existe upload separado de thumbnail.
- **Capa do eBook ≠ capa do impresso**: o eBook usa só a frente (JPG 1.6:1). O paperback exige uma capa **wraparound** (contracapa + lombada + frente) em PDF, com sangria e lombada dependente do número de páginas.
- **ISBN**: o **Kindle eBook não precisa de ISBN**. O **paperback** recebe um ISBN grátis do KDP (ou você fornece o seu). O ISBN do eBook e do impresso são diferentes.
- **Lombada**: a largura da lombada = páginas × 0,002252" (papel branco). Livros finos (abaixo de ~100 páginas) podem não comportar texto na lombada; nesse caso ela fica lisa.
- **Sangria (bleed)**: o miolo é só texto, então **não usa sangria**. A **capa impressa usa sangria de 0,125"** em todas as bordas.
- **Royalties**: eBook sem KDP Select no Brasil = 35%. Paperback = 60% do preço de lista **menos o custo de impressão** (que depende de páginas/papel). Use o KDP pricing calculator para simular.
- **Disclosure de IA**: para publicar esta versão como está, marque conteúdo gerado por IA para texto e capa. Se houver revisão humana substancial e recriação própria da capa, reveja a política vigente do KDP (AI-generated vs AI-assisted).
- **Links úteis**: KDP Cover Calculator (`https://kdp.amazon.com/cover-calculator/`) e a Central de Ajuda do KDP para diretrizes de paperback.

## Decisão editorial para o primeiro upload

- Autor: Addo Del Grossi.
- Formatos KDP: Kindle eBook (EPUB) e paperback impresso (miolo 6×9 P&B + capa wraparound).
- Marketplace primário: Amazon Brasil.
- KDP Select: não inscrever no lançamento inicial.
- Preço inicial sugerido do eBook: R$ 9,90.
- Disclosure de IA: marcar texto e capa como conteúdo gerado por IA se publicar esta versão como está.

## Validar o código Go

```bash
cd codigo-robo-go-binance
go test ./...
```

Comandos públicos do robô:

```bash
go run ./cmd/robot price
go run ./cmd/robot klines
go run ./cmd/robot signal
```

Comandos de ordem exigem chaves da Binance Spot Testnet:

```bash
go run ./cmd/robot order-test BUY
BOT_ALLOW_TESTNET_ORDER=true go run ./cmd/robot testnet-order BUY
```

Se a API devolver HTTP 451, respeite as regras locais e os termos da Binance. O projeto continua útil para estudo e testes unitários mesmo sem acesso à API.

## Regerar os artefatos do livro

O gerador usa Python com `Pillow`, `python-docx`, `reportlab` e `pypdf`.

```bash
make build
# ou diretamente:
python3 scripts/build_artifacts.py
```

Ele recria:

- `assets/capa-robo-trade-go-binance.jpg` (capa Kindle)
- `dist/robo-trade-go-binance.epub`
- `dist/robo-trade-go-binance.docx`
- `dist/robo-trade-go-binance-print-6x9.pdf` (miolo de impressão)
- `dist/robo-trade-go-binance-capa-print.pdf` (capa wraparound do paperback)
- `dist/robo-trade-go-binance-revisao.pdf` (revisão de tela, não para upload)
- `dist/codigo-robo-go-binance.zip`

Para validar todos os artefatos (código Go, EPUB, DOCX e os arquivos de impressão):

```bash
make validate
```

## Aviso

Este material é educativo. Não é recomendação financeira, consultoria de investimento nem promessa de resultado. O código usa a Binance Spot Testnet por padrão e não inclui endpoint de produção no projeto principal.
