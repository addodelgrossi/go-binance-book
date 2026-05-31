package binance

import (
	"context"
	"errors"
	"fmt"
	"strconv"
	"strings"

	spot "github.com/binance/binance-connector-go/clients/spot"
	"github.com/binance/binance-connector-go/clients/spot/src/restapi/models"
	"github.com/binance/binance-connector-go/common/v2/common"

	"github.com/exemplo/robo-go-binance/internal/config"
)

type Client struct {
	api *spot.BinanceSpotClient
}

func NewClient(cfg config.Config) *Client {
	restCfg := common.NewConfigurationRestAPI(
		common.WithBasePath(common.SpotRestApiTestnetUrl),
		common.WithTimeout(cfg.Timeout),
		common.WithRetries(2),
	)

	if cfg.APIKey != "" {
		common.WithApiKey(cfg.APIKey)(restCfg)
	}
	if cfg.APISecret != "" {
		common.WithApiSecret(cfg.APISecret)(restCfg)
	}

	return &Client{
		api: spot.NewBinanceSpotClient(spot.WithRestAPI(restCfg)),
	}
}

func (c *Client) Price(ctx context.Context, symbol string) (float64, error) {
	resp, err := c.api.RestApi.MarketAPI.TickerPrice(ctx).Symbol(symbol).Execute()
	if err != nil {
		return 0, annotateAPIError(err)
	}
	if resp.Data.TickerPriceResponse1 == nil {
		return 0, errors.New("resposta de preco inesperada")
	}

	price, err := strconv.ParseFloat(resp.Data.TickerPriceResponse1.GetPrice(), 64)
	if err != nil {
		return 0, fmt.Errorf("preco invalido: %w", err)
	}
	return price, nil
}

func (c *Client) ClosingPrices(ctx context.Context, symbol string, limit int32) ([]float64, error) {
	resp, err := c.api.RestApi.MarketAPI.Klines(ctx).
		Symbol(symbol).
		Interval(models.KlinesIntervalParameterInterval1m).
		Limit(limit).
		Execute()
	if err != nil {
		return nil, annotateAPIError(err)
	}

	closes := make([]float64, 0, len(resp.Data.Items))
	for _, candle := range resp.Data.Items {
		if len(candle.Items) < 5 || candle.Items[4].String == nil {
			return nil, errors.New("kline sem preco de fechamento")
		}
		closePrice, err := strconv.ParseFloat(*candle.Items[4].String, 64)
		if err != nil {
			return nil, fmt.Errorf("fechamento invalido: %w", err)
		}
		closes = append(closes, closePrice)
	}

	return closes, nil
}

func (c *Client) TestOrder(ctx context.Context, cfg config.Config, side models.NewOrderSideParameter) error {
	if err := cfg.RequireKeys(); err != nil {
		return err
	}

	_, err := c.api.RestApi.TradeAPI.OrderTest(ctx).
		Symbol(cfg.Symbol).
		Side(side).
		Type(models.NewOrderTypeParameterMarket).
		Quantity(cfg.Quantity).
		Execute()
	return annotateAPIError(err)
}

func (c *Client) NewTestnetOrder(ctx context.Context, cfg config.Config, side models.NewOrderSideParameter) error {
	if err := cfg.RequireKeys(); err != nil {
		return err
	}
	if err := cfg.RequireOrderPermission(); err != nil {
		return err
	}

	_, err := c.api.RestApi.TradeAPI.NewOrder(ctx).
		Symbol(cfg.Symbol).
		Side(side).
		Type(models.NewOrderTypeParameterMarket).
		Quantity(cfg.Quantity).
		Execute()
	return annotateAPIError(err)
}

func annotateAPIError(err error) error {
	if err == nil {
		return nil
	}
	if strings.Contains(err.Error(), "451") {
		return fmt.Errorf(
			"%w (HTTP 451: API indisponivel nesta regiao ou ambiente; respeite as regras locais e os termos da Binance)",
			err,
		)
	}
	return err
}
