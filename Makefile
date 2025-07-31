# Makefile per Chinese Grammar Wiki
# Automatizza la formattazione e le operazioni comuni

.PHONY: help format format-dry check format-b1 format-b2 format-a1 format-a2 lint stats install install-dev test clean venv

# Default target
help:
	@echo "Chinese Grammar Wiki - Comandi disponibili:"
	@echo ""
	@echo "  make format       - Formatta tutti i file Markdown"
	@echo "  make format-dry   - Simula la formattazione senza modifiche"
	@echo "  make format-b1    - Formatta solo i file B1"
	@echo "  make format-b2    - Formatta solo i file B2"
	@echo "  make format-a1    - Formatta solo i file A1"
	@echo "  make format-a2    - Formatta solo i file A2"
	@echo "  make check        - Controlla la formattazione senza modificare"
	@echo "  make lint         - Esegue linting dei file Markdown"
	@echo "  make stats        - Mostra statistiche del progetto"
	@echo "  make test         - Esegue i test Python"
	@echo "  make install      - Installa il progetto in modalità development"
	@echo "  make install-dev  - Installa con dipendenze di sviluppo"
	@echo "  make venv         - Crea virtual environment"
	@echo "  make clean        - Pulisce file temporanei"
	@echo ""

# Formatta tutti i file
format:
	@echo "🔧 Formattazione di tutti i file Markdown..."
	python format_markdown.py

# Dry run - mostra cosa verrebbe fatto
format-dry:
	@echo "🧪 Simulazione formattazione (dry run)..."
	python format_markdown.py --dry-run

# Controlla formattazione
check: format-dry

# Formatta per livello
format-b1:
	@echo "🔧 Formattazione file B1..."
	python format_markdown.py B1/

format-b2:
	@echo "🔧 Formattazione file B2..."
	python format_markdown.py B2/

format-a1:
	@echo "🔧 Formattazione file A1..."
	python format_markdown.py A1/

format-a2:
	@echo "🔧 Formattazione file A2..."
	python format_markdown.py A2/

# Linting con markdownlint (se installato)
lint:
	@echo "🔍 Controllo qualità Markdown..."
	@if command -v markdownlint >/dev/null 2>&1; then \
		markdownlint **/*.md || echo "⚠️  Alcuni file hanno problemi di linting"; \
	else \
		echo "ℹ️  markdownlint non installato. Installa con: npm install -g markdownlint-cli"; \
	fi

# Statistiche del progetto
stats:
	@echo "📊 Statistiche del progetto:"
	@echo ""
	@echo "File Markdown per livello:"
	@find . -name "*.md" -path "./A1/*" | wc -l | xargs echo "  A1:"
	@find . -name "*.md" -path "./A2/*" | wc -l | xargs echo "  A2:"
	@find . -name "*.md" -path "./B1/*" | wc -l | xargs echo "  B1:"
	@find . -name "*.md" -path "./B2/*" | wc -l | xargs echo "  B2:"
	@echo ""
	@echo "Totale file Markdown:"
	@find . -name "*.md" | wc -l
	@echo ""
	@echo "Righe di codice:"
	@find . -name "*.md" -exec cat {} \; | wc -l

# Pulizia file temporanei
clean:
	@echo "🧹 Pulizia file temporanei..."
	@find . -name "*.bak" -delete 2>/dev/null || true
	@find . -name "*~" -delete 2>/dev/null || true
	@find . -name "*.tmp" -delete 2>/dev/null || true
	@echo "✅ Pulizia completata"

# Target per CI/CD
ci-check: format-dry lint test

# Python environment management
venv:
	@echo "🐍 Creazione virtual environment..."
	python3 -m venv venv
	@echo "✅ Virtual environment creato in ./venv"
	@echo "🔧 Attiva con: source venv/bin/activate (Linux/Mac) o venv\\Scripts\\activate (Windows)"

install:
	@echo "📦 Installazione progetto in modalità development..."
	pip install -e .

install-dev:
	@echo "📦 Installazione con dipendenze di sviluppo..."
	pip install -e .[dev]
	pip install -r requirements-dev.txt

# Testing
test:
	@echo "🧪 Esecuzione test Python..."
	python3 test_formatter.py
