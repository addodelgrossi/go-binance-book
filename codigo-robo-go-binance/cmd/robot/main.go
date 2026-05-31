package main

import (
	"context"
	"fmt"
	"os"

	"github.com/exemplo/robo-go-binance/internal/config"
	"github.com/exemplo/robo-go-binance/internal/runner"
)

func main() {
	if err := run(os.Args[1:]); err != nil {
		fmt.Fprintln(os.Stderr, "erro:", err)
		os.Exit(1)
	}
}

func run(args []string) error {
	if len(args) == 0 {
		printUsage()
		return nil
	}

	cfg, err := config.Load()
	if err != nil {
		return err
	}

	ctx, cancel := context.WithTimeout(context.Background(), cfg.Timeout)
	defer cancel()

	app := runner.New(cfg)
	switch args[0] {
	case "price":
		return app.Price(ctx)
	case "klines":
		return app.Klines(ctx)
	case "signal":
		return app.Signal(ctx)
	case "order-test":
		return app.OrderTest(ctx, argOrDefault(args, 1, "BUY"))
	case "testnet-order":
		return app.TestnetOrder(ctx, argOrDefault(args, 1, "BUY"))
	case "help", "-h", "--help":
		printUsage()
		return nil
	default:
		printUsage()
		return fmt.Errorf("comando desconhecido: %s", args[0])
	}
}

func argOrDefault(args []string, index int, fallback string) string {
	if len(args) <= index {
		return fallback
	}
	return args[index]
}

func printUsage() {
	fmt.Println(`Robo educativo para Binance Spot Testnet

Uso:
  go run ./cmd/robot price
  go run ./cmd/robot klines
  go run ./cmd/robot signal
  go run ./cmd/robot order-test BUY
  go run ./cmd/robot testnet-order BUY

Variaveis:
  BINANCE_API_KEY
  BINANCE_API_SECRET
  BOT_SYMBOL=BNBUSDT
  BOT_QUANTITY=0.01
  BOT_SHORT_WINDOW=7
  BOT_LONG_WINDOW=25
  BOT_ALLOW_TESTNET_ORDER=false`)
}
