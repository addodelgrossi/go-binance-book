package runner

import (
	"context"
	"fmt"
	"strings"

	"github.com/binance/binance-connector-go/clients/spot/src/restapi/models"

	"github.com/exemplo/robo-go-binance/internal/binance"
	"github.com/exemplo/robo-go-binance/internal/config"
	"github.com/exemplo/robo-go-binance/internal/strategy"
)

type Runner struct {
	cfg    config.Config
	client *binance.Client
}

func New(cfg config.Config) Runner {
	return Runner{
		cfg:    cfg,
		client: binance.NewClient(cfg),
	}
}

func (r Runner) Price(ctx context.Context) error {
	price, err := r.client.Price(ctx, r.cfg.Symbol)
	if err != nil {
		return err
	}
	fmt.Printf("%s price: %.8f\n", r.cfg.Symbol, price)
	return nil
}

func (r Runner) Klines(ctx context.Context) error {
	limit := int32(r.cfg.LongWindow + 1)
	closes, err := r.client.ClosingPrices(ctx, r.cfg.Symbol, limit)
	if err != nil {
		return err
	}

	fmt.Printf("%s ultimos fechamentos de 1m:\n", r.cfg.Symbol)
	for i, closePrice := range closes {
		fmt.Printf("%02d %.8f\n", i+1, closePrice)
	}
	return nil
}

func (r Runner) Signal(ctx context.Context) error {
	limit := int32(r.cfg.LongWindow + 1)
	closes, err := r.client.ClosingPrices(ctx, r.cfg.Symbol, limit)
	if err != nil {
		return err
	}
	decision, err := strategy.MovingAverageSignal(closes, r.cfg.ShortWindow, r.cfg.LongWindow)
	if err != nil {
		return err
	}

	fmt.Printf("symbol: %s\n", r.cfg.Symbol)
	fmt.Printf("last_close: %.8f\n", decision.LastClose)
	fmt.Printf("short_sma_%d: %.8f\n", r.cfg.ShortWindow, decision.ShortSMA)
	fmt.Printf("long_sma_%d: %.8f\n", r.cfg.LongWindow, decision.LongSMA)
	fmt.Printf("signal: %s\n", decision.Signal)
	return nil
}

func (r Runner) OrderTest(ctx context.Context, sideText string) error {
	side, err := ParseSide(sideText)
	if err != nil {
		return err
	}
	if err := r.client.TestOrder(ctx, r.cfg, side); err != nil {
		return err
	}

	fmt.Printf("order-test OK: %s %s quantity %.8f\n", side, r.cfg.Symbol, r.cfg.Quantity)
	return nil
}

func (r Runner) TestnetOrder(ctx context.Context, sideText string) error {
	side, err := ParseSide(sideText)
	if err != nil {
		return err
	}
	if err := r.client.NewTestnetOrder(ctx, r.cfg, side); err != nil {
		return err
	}

	fmt.Printf("testnet-order executada: %s %s quantity %.8f\n", side, r.cfg.Symbol, r.cfg.Quantity)
	return nil
}

func ParseSide(value string) (models.NewOrderSideParameter, error) {
	switch strings.ToUpper(strings.TrimSpace(value)) {
	case "", "BUY", "COMPRA":
		return models.NewOrderSideParameterBuy, nil
	case "SELL", "VENDA":
		return models.NewOrderSideParameterSell, nil
	default:
		return "", fmt.Errorf("side invalido %q: use BUY ou SELL", value)
	}
}
