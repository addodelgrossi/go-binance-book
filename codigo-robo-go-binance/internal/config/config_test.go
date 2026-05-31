package config

import "testing"

func TestLoadDefaults(t *testing.T) {
	t.Setenv("BINANCE_API_KEY", "")
	t.Setenv("BINANCE_API_SECRET", "")
	t.Setenv("BOT_SYMBOL", "")
	t.Setenv("BOT_QUANTITY", "")
	t.Setenv("BOT_SHORT_WINDOW", "")
	t.Setenv("BOT_LONG_WINDOW", "")
	t.Setenv("BOT_ALLOW_TESTNET_ORDER", "")

	cfg, err := Load()
	if err != nil {
		t.Fatalf("Load() error = %v", err)
	}
	if cfg.Symbol != "BNBUSDT" {
		t.Fatalf("Symbol = %q, want BNBUSDT", cfg.Symbol)
	}
	if cfg.ShortWindow != 7 || cfg.LongWindow != 25 {
		t.Fatalf("windows = %d/%d, want 7/25", cfg.ShortWindow, cfg.LongWindow)
	}
	if cfg.AllowTestnetOrder {
		t.Fatal("AllowTestnetOrder = true, want false")
	}
}

func TestLoadCustomValues(t *testing.T) {
	t.Setenv("BOT_SYMBOL", "btc/usdt")
	t.Setenv("BOT_QUANTITY", "0.005")
	t.Setenv("BOT_SHORT_WINDOW", "3")
	t.Setenv("BOT_LONG_WINDOW", "8")
	t.Setenv("BOT_ALLOW_TESTNET_ORDER", "sim")

	cfg, err := Load()
	if err != nil {
		t.Fatalf("Load() error = %v", err)
	}
	if cfg.Symbol != "BTCUSDT" {
		t.Fatalf("Symbol = %q, want BTCUSDT", cfg.Symbol)
	}
	if cfg.Quantity != 0.005 {
		t.Fatalf("Quantity = %v, want 0.005", cfg.Quantity)
	}
	if !cfg.AllowTestnetOrder {
		t.Fatal("AllowTestnetOrder = false, want true")
	}
}

func TestShortWindowMustBeSmallerThanLongWindow(t *testing.T) {
	t.Setenv("BOT_SHORT_WINDOW", "10")
	t.Setenv("BOT_LONG_WINDOW", "10")

	if _, err := Load(); err == nil {
		t.Fatal("Load() error = nil, want validation error")
	}
}

func TestRequireOrderPermissionBlocksByDefault(t *testing.T) {
	cfg := Config{}
	if err := cfg.RequireOrderPermission(); err == nil {
		t.Fatal("RequireOrderPermission() error = nil, want blocked order error")
	}
}
