# Robo de Trade com Go e Binance Spot Testnet

Projeto educativo que acompanha o livro **Robos de Trade com Go e Binance para Iniciantes**.

Este codigo usa somente a Binance Spot Testnet. Ele nao e recomendacao financeira,
nao promete lucro e nao deve ser usado com dinheiro real sem uma revisao completa.

## Licenca

O codigo de exemplo deste diretorio usa a licenca MIT. O texto do livro,
a capa e os demais materiais editoriais do projeto permanecem com todos
os direitos reservados ao autor.

## Requisitos

- Go 1.26.x
- Conta na Binance Spot Testnet
- Chave e segredo da Spot Testnet para comandos de ordem

## Configuracao

Copie o exemplo de ambiente e preencha as chaves da Testnet:

```bash
cp .env.example .env
```

Depois exporte as variaveis no terminal:

```bash
export BINANCE_API_KEY="sua_chave"
export BINANCE_API_SECRET="seu_segredo"
export BOT_SYMBOL="BNBUSDT"
export BOT_QUANTITY="0.01"
export BOT_SHORT_WINDOW="7"
export BOT_LONG_WINDOW="25"
export BOT_ALLOW_TESTNET_ORDER="false"
```

## Comandos

```bash
go run ./cmd/robot price
go run ./cmd/robot klines
go run ./cmd/robot signal
go run ./cmd/robot order-test BUY
go run ./cmd/robot testnet-order BUY
```

`order-test` valida uma ordem na Testnet, mas nao executa a ordem.

`testnet-order` so executa uma ordem de mercado na Spot Testnet quando
`BOT_ALLOW_TESTNET_ORDER=true`. Esse bloqueio existe para evitar cliques
acidentais durante o aprendizado.

Se a API devolver HTTP 451, o servico provavelmente esta indisponivel para a
sua regiao ou ambiente. Respeite as regras locais e os termos da Binance; os
testes unitarios continuam funcionando sem acesso a API.

## Testes

```bash
go test ./...
```

Os testes unitarios cobrem:

- calculo de medias moveis;
- deteccao de cruzamento de medias;
- leitura de configuracao por variaveis de ambiente;
- bloqueio de ordem quando `BOT_ALLOW_TESTNET_ORDER` nao esta ativo.
