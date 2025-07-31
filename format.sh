#!/bin/bash
# Markdown Formatter Script per Linux/Mac
# Formatta automaticamente tutti i file Markdown del progetto

echo "========================================"
echo "  Chinese Grammar Wiki - MD Formatter"
echo "========================================"
echo

# Controlla se Python è installato
if ! command -v python3 &> /dev/null; then
    echo "❌ ERRORE: Python3 non è installato"
    echo "Installa Python3 dal package manager del tuo sistema"
    exit 1
fi

# Controlla se siamo in un virtual environment
if [[ -n "$VIRTUAL_ENV" ]]; then
    echo "🐍 Virtual environment attivo: $(basename $VIRTUAL_ENV)"
else
    echo "ℹ️  Nessun virtual environment attivo"
    echo "💡 Considera di usare: python3 -m venv venv && source venv/bin/activate"
fi

# Controlla se il formatter esiste
if [[ ! -f "format_markdown.py" ]]; then
    echo "❌ ERRORE: format_markdown.py non trovato"
    echo "Assicurati di essere nella directory del progetto"
    exit 1
fi

echo "🔧 Formattazione in corso..."
echo

# Esegui il formatter con tutti i parametri passati
python3 format_markdown.py "$@"

echo
echo "✅ Formattazione completata!"

# Se non ci sono parametri, mostra un suggerimento
if [[ $# -eq 0 ]]; then
    echo
    echo "💡 Suggerimenti:"
    echo "  • Usa '--dry-run' per simulare senza modificare"
    echo "  • Usa 'B2/' per formattare solo il livello B2"
    echo "  • Usa '--help' per vedere tutte le opzioni"
fi
