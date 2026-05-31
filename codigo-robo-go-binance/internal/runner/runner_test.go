package runner

import (
	"testing"

	"github.com/binance/binance-connector-go/clients/spot/src/restapi/models"
)

func TestParseSide(t *testing.T) {
	tests := map[string]models.NewOrderSideParameter{
		"":       models.NewOrderSideParameterBuy,
		"BUY":    models.NewOrderSideParameterBuy,
		"compra": models.NewOrderSideParameterBuy,
		"SELL":   models.NewOrderSideParameterSell,
		"venda":  models.NewOrderSideParameterSell,
	}

	for input, want := range tests {
		got, err := ParseSide(input)
		if err != nil {
			t.Fatalf("ParseSide(%q) error = %v", input, err)
		}
		if got != want {
			t.Fatalf("ParseSide(%q) = %s, want %s", input, got, want)
		}
	}
}

func TestParseSideRejectsInvalidInput(t *testing.T) {
	if _, err := ParseSide("HOLD"); err == nil {
		t.Fatal("ParseSide(HOLD) error = nil, want error")
	}
}
