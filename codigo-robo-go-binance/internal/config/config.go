package config

import (
	"errors"
	"fmt"
	"os"
	"strconv"
	"strings"
	"time"
)

type Config struct {
	APIKey            string
	APISecret         string
	Symbol            string
	Quantity          float32
	ShortWindow       int
	LongWindow        int
	AllowTestnetOrder bool
	Timeout           time.Duration
}

func Load() (Config, error) {
	cfg := Config{
		APIKey:            strings.TrimSpace(os.Getenv("BINANCE_API_KEY")),
		APISecret:         strings.TrimSpace(os.Getenv("BINANCE_API_SECRET")),
		Symbol:            getenv("BOT_SYMBOL", "BNBUSDT"),
		Quantity:          0.01,
		ShortWindow:       7,
		LongWindow:        25,
		AllowTestnetOrder: parseBool(os.Getenv("BOT_ALLOW_TESTNET_ORDER")),
		Timeout:           10 * time.Second,
	}

	if raw := strings.TrimSpace(os.Getenv("BOT_QUANTITY")); raw != "" {
		value, err := strconv.ParseFloat(raw, 32)
		if err != nil || value <= 0 {
			return Config{}, fmt.Errorf("BOT_QUANTITY invalido: %q", raw)
		}
		cfg.Quantity = float32(value)
	}

	if raw := strings.TrimSpace(os.Getenv("BOT_SHORT_WINDOW")); raw != "" {
		value, err := strconv.Atoi(raw)
		if err != nil || value <= 0 {
			return Config{}, fmt.Errorf("BOT_SHORT_WINDOW invalido: %q", raw)
		}
		cfg.ShortWindow = value
	}

	if raw := strings.TrimSpace(os.Getenv("BOT_LONG_WINDOW")); raw != "" {
		value, err := strconv.Atoi(raw)
		if err != nil || value <= 0 {
			return Config{}, fmt.Errorf("BOT_LONG_WINDOW invalido: %q", raw)
		}
		cfg.LongWindow = value
	}

	cfg.Symbol = strings.ToUpper(strings.ReplaceAll(strings.TrimSpace(cfg.Symbol), "/", ""))
	if cfg.Symbol == "" {
		return Config{}, errors.New("BOT_SYMBOL nao pode ficar vazio")
	}
	if cfg.ShortWindow >= cfg.LongWindow {
		return Config{}, errors.New("BOT_SHORT_WINDOW deve ser menor que BOT_LONG_WINDOW")
	}

	return cfg, nil
}

func (c Config) RequireKeys() error {
	if c.APIKey == "" || c.APISecret == "" {
		return errors.New("defina BINANCE_API_KEY e BINANCE_API_SECRET da Spot Testnet")
	}
	return nil
}

func (c Config) RequireOrderPermission() error {
	if !c.AllowTestnetOrder {
		return errors.New("ordem bloqueada: defina BOT_ALLOW_TESTNET_ORDER=true apenas na Spot Testnet")
	}
	return nil
}

func getenv(key, fallback string) string {
	value := strings.TrimSpace(os.Getenv(key))
	if value == "" {
		return fallback
	}
	return value
}

func parseBool(value string) bool {
	switch strings.ToLower(strings.TrimSpace(value)) {
	case "1", "true", "t", "yes", "y", "sim", "s":
		return true
	default:
		return false
	}
}
