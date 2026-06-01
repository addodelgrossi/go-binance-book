# Contexto do Projeto

Este documento existe para retomar o projeto sem depender do histórico da conversa original.

## Objetivo

Criar um livro curto em português do Brasil para testar publicação na Amazon KDP:

- Tema: robô de trade educativo com Go e Binance.
- Público: iniciante total, estilo "para iniciantes".
- Formato: Markdown como fonte; **Kindle eBook** (EPUB) e **paperback impresso** (miolo PDF 6×9 P&B + capa wraparound PDF) como entregas KDP; DOCX para Kindle Create e PDF 5×8 para revisão de tela.
- Tamanho: ~57 páginas no miolo 6×9 (acima do mínimo de 24 do KDP).
- Código: projeto Go separado, usando Binance Spot Testnet e o conector oficial da Binance para Spot em Go.

O livro não deve prometer lucro, não deve recomendar investimento e não deve orientar uso com dinheiro real.

## Estado atual

O projeto já contém:

- Manuscrito em `manuscrito/robo-trade-go-binance-manuscrito.md`.
- EPUB em `dist/robo-trade-go-binance.epub`.
- DOCX em `dist/robo-trade-go-binance.docx`.
- PDF de revisão em `dist/robo-trade-go-binance-revisao.pdf` (5×8, com capa, só leitura de tela).
- Miolo de impressão em `dist/robo-trade-go-binance-print-6x9.pdf` (6×9 P&B, sem capa).
- Capa wraparound do paperback em `dist/robo-trade-go-binance-capa-print.pdf`.
- Capa em `assets/capa-robo-trade-go-binance.jpg`, com tema visual configurável em `assets/cover/cover_theme.json`.
- Metadados KDP em `kdp/metadados-kdp.md`.
- Código Go em `codigo-robo-go-binance/`.
- Script de geração em `scripts/build_artifacts.py` e specs de impressão em `scripts/print_specs.py`.

O PDF de revisão tem 75 páginas (5×8). O miolo de impressão tem 57 páginas (6×9); a lombada calculada (papel branco) é ~0,128", abaixo de 80 páginas, então a lombada fica lisa. A capa Kindle é JPG 1600x2560 e a capa wraparound tem ~12,38×9,25".

## Decisões importantes

- Autor definido: `Addo Del Grossi`.
- O código usa `common.SpotRestApiTestnetUrl`.
- O projeto principal não inclui endpoint de produção da Binance.
- A estratégia é cruzamento de médias móveis simples.
- Comandos CLI do robô: `price`, `klines`, `signal`, `order-test`, `testnet-order`.
- `order-test` valida uma ordem sem executar.
- `testnet-order` só executa quando `BOT_ALLOW_TESTNET_ORDER=true`.
- Variáveis principais: `BINANCE_API_KEY`, `BINANCE_API_SECRET`, `BOT_SYMBOL`, `BOT_QUANTITY`, `BOT_SHORT_WINDOW`, `BOT_LONG_WINDOW`, `BOT_ALLOW_TESTNET_ORDER`.
- A dependência principal é `github.com/binance/binance-connector-go/clients/spot v1.8.0`.
- O livro menciona Go 1.26.x.

## Validação já feita

Comando principal:

```bash
make validate
```

Valida:

- `go test ./...` dentro de `codigo-robo-go-binance`.
- Integridade ZIP do EPUB.
- XML interno do EPUB.
- Integridade ZIP do DOCX.
- Tipo da capa e do PDF.
- Testes das specs de impressão (`scripts/test_print_specs.py`).
- Conformidade dos artefatos de impressão: trim do miolo (6×9), contagem mínima de páginas e dimensão da capa vs fórmula da lombada (`scripts/validate_print.py`).

Validações observadas:

- Testes Go passaram.
- EPUB descompacta sem erro.
- EPUB passou na validação XML local.
- DOCX descompacta sem erro.
- PDF foi gerado com 75 páginas.

Limitação:

- `epubcheck` não estava instalado no ambiente atual; a validação XML local foi executada.
- O render visual automático do DOCX via LibreOffice não foi feito porque `soffice` não estava instalado no ambiente original.

## API Binance e HTTP 451

No ambiente original, chamadas públicas para a Binance Spot Testnet retornaram HTTP 451.

Isso foi tratado no código com uma mensagem explicativa. Não tente contornar regras regionais ou termos da Binance. O projeto continua útil para estudar arquitetura, Go, testes, configuração e publicação KDP mesmo quando a API não está acessível.

## Como trabalhar no livro

Editar primeiro:

```text
manuscrito/robo-trade-go-binance-manuscrito.md
```

Depois regenerar:

```bash
make build
```

Ou, se o Python do sistema não tiver dependências:

```bash
/Users/addo/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 scripts/build_artifacts.py
```

Revalidar:

```bash
make validate
```

## Como trabalhar no código

Entrar na pasta:

```bash
cd codigo-robo-go-binance
```

Rodar testes:

```bash
go test ./...
```

Rodar comandos públicos:

```bash
go run ./cmd/robot price
go run ./cmd/robot klines
go run ./cmd/robot signal
```

Comandos com ordem exigem chaves da Spot Testnet:

```bash
go run ./cmd/robot order-test BUY
BOT_ALLOW_TESTNET_ORDER=true go run ./cmd/robot testnet-order BUY
```

Nunca commitar `.env`.

## Antes de publicar no KDP

1. Confirmar `Addo Del Grossi` como autor final em todos os artefatos.
2. Revisar texto inteiro.
3. Abrir EPUB no Kindle Previewer.
4. Conferir blocos de código em tela pequena.
5. Conferir capa em miniatura.
6. Publicar EPUB direto no primeiro lançamento.
7. Revisar `kdp/metadados-kdp.md`.
8. Marcar disclosure de IA para texto e capa se publicar esta versão como está.
9. Não inscrever no KDP Select no primeiro lançamento.

## Próximos passos recomendados

- Fazer revisão humana de linguagem e técnica.
- Rodar o projeto em ambiente onde a Spot Testnet esteja disponível, se desejado.
- Conferir a página de direitos autorais e a licença MIT do código.
- Criar release no GitHub com os arquivos de `dist/`.

## Prompt curto para retomar com Codex

Use este texto se abrir uma nova conversa:

```text
Estou no repo /Users/addo/jobs/addodelgrossi/go-binance-book. Leia README.md e docs/CONTEXTO_DO_PROJETO.md primeiro. Este repo contém um livro KDP em português sobre robô de trade educativo com Go e Binance Spot Testnet, mais um projeto Go acompanhante. Preserve o foco educativo, Testnet, sem promessa financeira e sem endpoint de produção. Antes de editar, rode git status. Para validar, use make validate.
```
