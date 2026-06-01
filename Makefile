BUNDLED_PYTHON := $(HOME)/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3
PYTHON ?= $(if $(wildcard $(BUNDLED_PYTHON)),$(BUNDLED_PYTHON),python3)
GO ?= go

.PHONY: build test validate status

build:
	$(PYTHON) scripts/build_artifacts.py

test:
	cd codigo-robo-go-binance && $(GO) test ./...

validate: test
	cd scripts && $(PYTHON) -m unittest test_print_specs
	unzip -t dist/robo-trade-go-binance.epub >/dev/null
	$(PYTHON) scripts/validate_epub_xml.py dist/robo-trade-go-binance.epub
	unzip -t dist/robo-trade-go-binance.docx >/dev/null
	file assets/capa-robo-trade-go-binance.jpg dist/robo-trade-go-binance-revisao.pdf
	$(PYTHON) scripts/validate_print.py
	@if command -v epubcheck >/dev/null 2>&1; then \
		epubcheck dist/robo-trade-go-binance.epub; \
	else \
		echo "epubcheck nao instalado; validacao XML local executada"; \
	fi

status:
	git status --short
