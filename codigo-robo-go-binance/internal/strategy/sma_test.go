package strategy

import "testing"

func TestSMA(t *testing.T) {
	got, err := SMA([]float64{10, 20, 30, 40}, 3)
	if err != nil {
		t.Fatalf("SMA() error = %v", err)
	}
	if got != 30 {
		t.Fatalf("SMA() = %v, want 30", got)
	}
}

func TestMovingAverageSignalBuy(t *testing.T) {
	decision, err := MovingAverageSignal([]float64{10, 10, 10, 10, 20}, 2, 4)
	if err != nil {
		t.Fatalf("MovingAverageSignal() error = %v", err)
	}
	if decision.Signal != SignalBuy {
		t.Fatalf("Signal = %s, want BUY", decision.Signal)
	}
}

func TestMovingAverageSignalSell(t *testing.T) {
	decision, err := MovingAverageSignal([]float64{20, 20, 20, 20, 10}, 2, 4)
	if err != nil {
		t.Fatalf("MovingAverageSignal() error = %v", err)
	}
	if decision.Signal != SignalSell {
		t.Fatalf("Signal = %s, want SELL", decision.Signal)
	}
}

func TestMovingAverageSignalHold(t *testing.T) {
	decision, err := MovingAverageSignal([]float64{10, 11, 12, 13, 14}, 2, 4)
	if err != nil {
		t.Fatalf("MovingAverageSignal() error = %v", err)
	}
	if decision.Signal != SignalHold {
		t.Fatalf("Signal = %s, want HOLD", decision.Signal)
	}
}

func TestMovingAverageSignalNeedsEnoughData(t *testing.T) {
	if _, err := MovingAverageSignal([]float64{1, 2, 3}, 2, 4); err == nil {
		t.Fatal("MovingAverageSignal() error = nil, want enough data error")
	}
}
