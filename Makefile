PYTHON ?= python3
GO ?= go

.PHONY: build test validate status

build:
	$(PYTHON) scripts/build_artifacts.py

test:
	cd codigo-robo-go-binance && $(GO) test ./...

validate: test
	unzip -t dist/robo-trade-go-binance.epub >/dev/null
	unzip -t dist/robo-trade-go-binance.docx >/dev/null
	file assets/capa-robo-trade-go-binance.jpg dist/robo-trade-go-binance-revisao.pdf

status:
	git status --short
