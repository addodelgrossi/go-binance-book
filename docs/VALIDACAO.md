# Notas de Validação

## Código Go

O projeto foi validado com:

```bash
cd codigo-robo-go-binance
go test ./...
```

Resultado esperado: testes unitários passam para configuração, estratégia e parser de comandos.

## API Binance

Os comandos públicos `price`, `klines` e `signal` usam a Binance Spot Testnet. No ambiente onde os artefatos foram gerados, a API retornou HTTP 451. O código foi ajustado para exibir uma mensagem clara:

```text
HTTP 451: API indisponivel nesta regiao ou ambiente; respeite as regras locais e os termos da Binance
```

Isso não invalida os testes unitários nem o valor educativo do projeto. Para executar chamadas reais, use um ambiente/região em que a Spot Testnet esteja disponível e respeite os termos da Binance.

## Livro

Validações feitas:

- EPUB descompacta sem erros.
- DOCX descompacta sem erros.
- PDF de revisão gerado com 72 páginas.
- Capa gerada em JPG 1600x2560.
- DOCX passou auditoria de acessibilidade sem achados.

Limitação conhecida:

- O render visual automático do DOCX via LibreOffice não foi executado porque `soffice` não estava instalado no ambiente original.

## Segurança

- O projeto principal usa `common.SpotRestApiTestnetUrl`.
- Não há endpoint `api.binance.com` de produção no código principal.
- `.env` está ignorado no Git.
- `testnet-order` exige `BOT_ALLOW_TESTNET_ORDER=true`.
