# Checklist de Publicação KDP

## Antes do upload

- Trocar `[Nome do Autor]` pelo nome real ou pseudônimo escolhido.
- Revisar o manuscrito em `manuscrito/robo-trade-go-binance-manuscrito.md`.
- Abrir `dist/robo-trade-go-binance.epub` no Kindle Previewer.
- Conferir sumário, blocos de código, acentos e quebras em tela pequena.
- Conferir `assets/capa-robo-trade-go-binance.jpg` em miniatura.
- Confirmar que não há promessa de lucro ou recomendação financeira.
- Conferir que o livro fala sempre em Spot Testnet no código principal.

## Upload sugerido

- Manuscrito principal: `dist/robo-trade-go-binance.epub`.
- Alternativa para Kindle Create: importar `dist/robo-trade-go-binance.docx` e exportar KPF.
- Capa: `assets/capa-robo-trade-go-binance.jpg`.
- Descrição, subtítulo e palavras-chave: `kdp/metadados-kdp.md`.

## Disclosure de IA

Se o texto, a capa ou partes substanciais deles forem usados como gerados por IA, marque o disclosure de conteúdo gerado por IA no KDP. Se houver reescrita, revisão humana substancial e validação técnica próprias, confira a política atual do KDP para diferenciar AI-generated de AI-assisted.

## Última revisão editorial

- Ler a introdução e o aviso de risco.
- Rodar `go test ./...` dentro de `codigo-robo-go-binance`.
- Verificar que `.env` não foi commitado.
- Confirmar que o README do código explica HTTP 451 e Testnet.
- Fazer preview final no KDP antes de publicar.
