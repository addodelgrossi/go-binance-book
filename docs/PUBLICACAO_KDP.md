# Checklist de Publicação KDP

## Antes do upload

- Confirmar que o autor final é `Addo Del Grossi` em manuscrito, capa, EPUB, DOCX, PDF e metadados KDP.
- Revisar o manuscrito em `manuscrito/robo-trade-go-binance-manuscrito.md`.
- Abrir `dist/robo-trade-go-binance.epub` no Kindle Previewer.
- Conferir sumário, blocos de código, acentos e quebras em tela pequena.
- Conferir `assets/capa-robo-trade-go-binance.jpg` em miniatura.
- Confirmar que não há promessa de lucro ou recomendação financeira.
- Conferir que o livro fala sempre em Spot Testnet no código principal.

## Upload sugerido (Kindle eBook)

- Manuscrito principal: `dist/robo-trade-go-binance.epub`.
- Capa: `assets/capa-robo-trade-go-binance.jpg`.
- Descrição, subtítulo e palavras-chave: `kdp/metadados-kdp.md`.
- Marketplace primário: Amazon Brasil.
- KDP Select: não inscrever no primeiro lançamento.
- Preço inicial sugerido: R$ 9,90.
- Royalty esperada no Brasil sem KDP Select: 35%.
- Alternativa futura: importar `dist/robo-trade-go-binance.docx` no Kindle Create e exportar KPF.

## Upload sugerido (Paperback impresso)

- Opções de impressão: papel branco, interior preto e branco, trim 6×9 pol.
- Miolo: `dist/robo-trade-go-binance-print-6x9.pdf` (sem capa embutida).
- Capa: `dist/robo-trade-go-binance-capa-print.pdf` (wraparound com lombada/sangria).
- ISBN: usar o ISBN grátis fornecido pelo KDP (diferente do eBook).
- Conferir no Visualizador de Impressão do KDP: margens, gutter, lombada e sangria.
- Boa prática: gerar o template oficial no KDP Cover Calculator (trim + páginas + papel) e comparar com a capa gerada.
- Royalty: 60% do preço de lista menos o custo de impressão (ver KDP pricing calculator).

## Disclosure de IA

Para publicar esta versão como está, marque disclosure de conteúdo gerado por IA para texto e capa. Se houver reescrita, revisão humana substancial e recriação própria da capa, confira a política atual do KDP para diferenciar AI-generated de AI-assisted.

## Última revisão editorial

- Ler a introdução e o aviso de risco.
- Rodar `go test ./...` dentro de `codigo-robo-go-binance`.
- Verificar que `.env` não foi commitado.
- Confirmar que o README do código explica HTTP 451 e Testnet.
- Rodar `make validate` e confirmar que a validação XML do EPUB e a validação de impressão (trim, páginas, lombada) passam.
- Fazer preview final no KDP antes de publicar (Kindle Previewer para o eBook; Visualizador de Impressão para o paperback).
