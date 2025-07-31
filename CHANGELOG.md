# Changelog - Markdown Formatter

## [1.0.1] - 2025-07-31

### Bug Fixes

- **Code Blocks**: Risolto bug critico che rimuoveva i tripli backticks di chiusura dei code blocks
- Il formatter ora gestisce correttamente apertura e chiusura dei code blocks
- Mantiene tutti i backticks di chiusura (```)
- Aggiunge correttamente il linguaggio `text` ai code blocks senza linguaggio specificato
- Aggiunge test specifici per prevenire regressioni future

### Technical Details

- Riscritto `fix_code_blocks()` per usare parsing line-by-line invece di regex complessi
- Rimosso uso di `re.DOTALL` che causava cattura eccessiva
- Aggiunta logica state-based per tracciare apertura/chiusura code blocks
- Migliorata gestione della spaziatura intorno ai code blocks

## [1.0.0] - 2025-07-31

### Features

- **Formatter completo** per file Markdown del Chinese Grammar Wiki
- **Correzione automatica** di headers, tabelle, liste, code blocks
- **Normalizzazione punteggiatura cinese** (`,` → `，`, `.` → `。`)
- **Formattazione pinyin** con capitalizzazione corretta
- **Spaziatura automatica** tra caratteri cinesi e latini
- **Setup Python completo** con virtual environment, requirements, tests
- **Cross-platform support** (Windows .bat, Linux/Mac .sh, Makefile)
- **Configurazione avanzata** tramite .ini file
- **Suite di test completa** per validazione funzionalità

### Infrastructure

- Virtual environment support
- Package installabile con pip
- CI/CD ready configuration
- Comprehensive .gitignore for Python projects
- Documentation completa
