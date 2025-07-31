# Markdown Formatter per Chinese Grammar Wiki

Questo tool automatizza la formattazione dei file Markdown del progetto Chinese Grammar Wiki, garantendo consistenza e qualità professionale.

## 🚀 Installazione e Utilizzo

### Requisiti

- Python 3.6 o superiore
- Nessuna dipendenza esterna richiesta

### Setup Ambiente Python (Raccomandato)

```bash

# Crea virtual environment

python3 -m venv venv

# Attiva virtual environment

# Linux/Mac:

source venv/bin/activate

# Windows:

venv\Scripts\activate

# Installa il progetto in modalità development (opzionale)

pip install -e .

# O installa con dipendenze di sviluppo

pip install -e .[dev]
```

### Utilizzo Base

```bash

# Formatta tutto il progetto

python format_markdown.py

# Formatta una directory specifica

python format_markdown.py B2/

# Formatta un singolo file

python format_markdown.py B2/parti-del-discorso/verbi.md

# Modalità dry-run (simula senza modificare)

python format_markdown.py --dry-run

# Solo directory principale (non ricorsivo)

python format_markdown.py --no-recursive B1/
```

### Scorciatoie

**Windows:**

```cmd

# Formatta tutto il progetto

format.bat

# Con parametri

format.bat B2/ --dry-run
```

**Linux/Mac (con Make):**

```bash

# Mostra tutti i comandi disponibili

make help

# Formatta tutto

make format

# Simula formattazione

make format-dry

# Formatta per livello

make format-b1
make format-b2
```

## 🔧 Funzionalità

### Correzioni Automatiche

1. **Headers**

- Aggiunge spaziatura corretta prima e dopo gli headers
- Rimuove spazi extra alla fine

2. **Tabelle**

- Normalizza la spaziatura delle celle
- Aggiunge righe vuote prima e dopo le tabelle
- Corregge l'allineamento

3. **Code Blocks**

- Aggiunge linguaggio ai code blocks vuoti
- Assicura spaziatura corretta

4. **Liste**

- Normalizza i marcatori delle liste (usa `-`)
- Corregge la numerazione delle liste ordinate
- Aggiunge spaziatura appropriata

5. **Punteggiatura Cinese**

- Converte `,` in `，` nei contesti cinesi
- Converte `.` in `。` alla fine di frasi cinesi

6. **Pinyin**

- Capitalizza correttamente i nomi nel pinyin
- Corregge errori di formattazione comuni

7. **Spaziatura Cinese**

- Aggiunge spazi tra caratteri cinesi e testo latino
- Mantiene corretta formattazione in parentesi

8. **Pulizia Generale**

- Rimuove spazi trailing
- Normalizza line endings
- Limita righe vuote consecutive

### Esempi di Correzioni

**Prima:**

```markdown

# Verbi

Testo 混合 text.

| Col1 | Col2 |
| --- | --- |
| Data1 | Data2 |

```

**Dopo:**

```markdown

# Verbi

Testo 混合 text。

| Col1 | Col2 |
| ------ | ------ |
| Data1 | Data2 |

```

## 📊 Output e Statistiche

Il formatter fornisce statistiche dettagliate:

```text
📊 STATISTICHE FORMATTAZIONE
============================================================
File processati: 168
File modificati: 23
Errori: 0

🔧 Fix applicati:
  • Headers Spacing: 45
  • Table Formatting: 12
  • Chinese Punctuation: 8
  • Pinyin Formatting: 3
  • Code Blocks: 7

✅ Tasso di successo: 100.0%
```

## ⚙️ Configurazione

Modifica `format_config.ini` per personalizzare il comportamento:

```ini
[formatting]
max_blank_lines = 2
header_spacing = true
format_tables = true
normalize_chinese_punctuation = true

[chinese]
add_spacing_around_chinese = true
convert_chinese_commas = true
```

## 🧪 Testing

Esegui i test per verificare che tutto funzioni:

```bash

# Esegui tutti i test

python test_formatter.py

# Con make

make test
```

## 📝 Best Practices

### Quando Usare il Formatter

1. **Prima di commit** - Assicura consistenza
2. **Dopo modifiche massive** - Normalizza il formato
3. **Periodicamente** - Mantiene la qualità

### Workflow Consigliato

```bash

# 1. Verifica cosa cambierebbe

python format_markdown.py --dry-run

# 2. Applica le modifiche

python format_markdown.py

# 3. Controlla i risultati

git diff

# 4. Commit se soddisfatto

git add .
git commit -m "docs: format markdown files"
```

## 🎯 Casi d'Uso Specifici

### Formattare Solo Certi Livelli

```bash

# Solo B2 (più recente e critico)

python format_markdown.py B2/

# Solo file modificati di recente

git diff --name-only HEAD~10 | grep "\.md$" | xargs python format_markdown.py
```

### Integrare in CI/CD

```yaml

# GitHub Actions esempio

- name: Format Markdown
  run: |
    python format_markdown.py --dry-run
    if [ $? -ne 0 ]; then
      echo "Markdown files need formatting"
      exit 1
    fi
```

### Backup e Sicurezza

Il formatter non crea backup automatici. Per sicurezza:

```bash

# Crea backup manuale

cp -r . ../backup/

# Oppure usa git

git add .
git commit -m "backup before formatting"

# Poi formatta

python format_markdown.py
```

## 🐛 Troubleshooting

### Problemi Comuni

**Errore: "File not found"**

```bash

# Verifica il percorso

ls -la format_markdown.py
python format_markdown.py --help
```

**Encoding errors**

```bash

# Il formatter usa UTF-8 automaticamente

# Se problemi persistono, controlla l'encoding del file

file -i nome_file.md
```

**Modifiche inaspettate**

```bash

# Usa sempre dry-run prima

python format_markdown.py --dry-run

# Controlla diff con git

git diff HEAD~1
```

### Debugging

Aggiungi verbose output modificando il codice:

```python

# In format_markdown.py, cambia

verbose = True  # invece di False
```

## 🤝 Contribuire

Per migliorare il formatter:

1. Aggiungi test in `test_formatter.py`
2. Implementa nuove regole di formattazione
3. Aggiorna la documentazione
4. Testa su file reali del progetto

### Aggiungere Nuove Regole

```python
def fix_new_rule(self, content: str) -> str:
    """Descrizione della nuova regola."""
    # Implementazione
    fixed_content = content  # ... logica

    self._track_fix('new_rule')
    return fixed_content
```

Poi aggiungi alla lista in `format_content()`.

---

*Questo formatter è stato creato specificamente per il progetto Chinese Grammar Wiki e le sue esigenze di formattazione per contenuti multilingue cinese-italiano.*
