package strategy

import (
	"errors"
	"fmt"
)

type Signal string

const (
	SignalBuy  Signal = "BUY"
	SignalSell Signal = "SELL"
	SignalHold Signal = "HOLD"
)

type Decision struct {
	Signal      Signal
	ShortSMA    float64
	LongSMA     float64
	PrevShortMA float64
	PrevLongMA  float64
	LastClose   float64
}

func SMA(values []float64, window int) (float64, error) {
	if window <= 0 {
		return 0, errors.New("janela da media deve ser maior que zero")
	}
	if len(values) < window {
		return 0, fmt.Errorf("precisa de %d valores, recebeu %d", window, len(values))
	}

	start := len(values) - window
	var sum float64
	for _, value := range values[start:] {
		sum += value
	}
	return sum / float64(window), nil
}

func MovingAverageSignal(closes []float64, shortWindow, longWindow int) (Decision, error) {
	if shortWindow <= 0 || longWindow <= 0 {
		return Decision{}, errors.New("janelas devem ser maiores que zero")
	}
	if shortWindow >= longWindow {
		return Decision{}, errors.New("janela curta deve ser menor que janela longa")
	}
	if len(closes) < longWindow+1 {
		return Decision{}, fmt.Errorf("precisa de pelo menos %d fechamentos", longWindow+1)
	}

	previous := closes[:len(closes)-1]
	current := closes

	prevShort, err := SMA(previous, shortWindow)
	if err != nil {
		return Decision{}, err
	}
	prevLong, err := SMA(previous, longWindow)
	if err != nil {
		return Decision{}, err
	}
	shortSMA, err := SMA(current, shortWindow)
	if err != nil {
		return Decision{}, err
	}
	longSMA, err := SMA(current, longWindow)
	if err != nil {
		return Decision{}, err
	}

	decision := Decision{
		Signal:      SignalHold,
		ShortSMA:    shortSMA,
		LongSMA:     longSMA,
		PrevShortMA: prevShort,
		PrevLongMA:  prevLong,
		LastClose:   closes[len(closes)-1],
	}

	switch {
	case prevShort <= prevLong && shortSMA > longSMA:
		decision.Signal = SignalBuy
	case prevShort >= prevLong && shortSMA < longSMA:
		decision.Signal = SignalSell
	}

	return decision, nil
}
