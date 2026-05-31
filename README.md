# Robôs de Trade com Go e Binance para Iniciantes

Repositório do livro **Robôs de Trade com Go e Binance para Iniciantes** e do projeto Go que acompanha o ebook.

O livro é um guia educativo em português do Brasil para criar um robô simples usando Go, Binance Spot Testnet e uma estratégia de cruzamento de médias móveis. Ele foi pensado como um primeiro teste de publicação na Amazon KDP, sem promessa de lucro e sem operação com dinheiro real.

## Retomando o projeto

Se você abrir este repositório em uma nova conversa com Codex/ChatGPT ou em outro editor, comece por:

1. `docs/CONTEXTO_DO_PROJETO.md`
2. `docs/PUBLICACAO_KDP.md`
3. `docs/VALIDACAO.md`
4. `manuscrito/robo-trade-go-binance-manuscrito.md`

O arquivo de contexto guarda as decisões principais, estado atual, limitações conhecidas e próximos passos para não depender do histórico desta conversa.

## Estrutura

- `manuscrito/`: fonte principal do livro em Markdown.
- `dist/`: artefatos finais para revisão/publicação: EPUB, DOCX, PDF e ZIP do código.
- `assets/`: capa em JPG 1600x2560.
- `kdp/`: metadados sugeridos para cadastro no KDP.
- `codigo-robo-go-binance/`: projeto Go do robô educativo.
- `scripts/`: gerador local de EPUB/DOCX/PDF/capa/ZIP.
- `docs/`: contexto, checklist de publicação, validação e roadmap.

## Artefatos principais

- EPUB KDP: `dist/robo-trade-go-binance.epub`
- DOCX para revisão/Kindle Create: `dist/robo-trade-go-binance.docx`
- PDF de revisão: `dist/robo-trade-go-binance-revisao.pdf`
- Capa: `assets/capa-robo-trade-go-binance.jpg`
- Metadados KDP: `kdp/metadados-kdp.md`
- Código compactado: `dist/codigo-robo-go-binance.zip`

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

O gerador usa Python com `Pillow`, `python-docx` e `reportlab`.

```bash
python3 scripts/build_artifacts.py
```

Ele recria:

- `assets/capa-robo-trade-go-binance.jpg`
- `dist/robo-trade-go-binance.epub`
- `dist/robo-trade-go-binance.docx`
- `dist/robo-trade-go-binance-revisao.pdf`
- `dist/codigo-robo-go-binance.zip`

## Aviso

Este material é educativo. Não é recomendação financeira, consultoria de investimento nem promessa de resultado. O código usa a Binance Spot Testnet por padrão e não inclui endpoint de produção no projeto principal.
