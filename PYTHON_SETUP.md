# File Python Aggiunti al Progetto

Questi file sono stati aggiunti per supportare l'ambiente di sviluppo Python:

## File di Configurazione Python

### 📦 Package e Dipendenze
- **`setup.py`** - Setup script tradizionale per il package Python
- **`pyproject.toml`** - Configurazione moderna Python (PEP 518)
- **`requirements.txt`** - Dipendenze di produzione (attualmente vuoto)
- **`requirements-dev.txt`** - Dipendenze di sviluppo
- **`MANIFEST.in`** - Specifica quali file includere nel package

### 🔧 Script e Utilità
- **`format.sh`** - Script bash per Linux/Mac (equivalente a format.bat)
- **`format.bat`** - Script batch per Windows (aggiornato)
- **`Makefile`** - Makefile aggiornato con comandi Python

### 🚫 File Esclusi
- **`.gitignore`** - Aggiornato con regole complete per Python

## Comandi Utili

### Setup Iniziale
```bash
# Crea virtual environment
python3 -m venv venv

# Attiva (Linux/Mac)
source venv/bin/activate

# Attiva (Windows)
venv\Scripts\activate

# Installa in modalità development
pip install -e .
```

### Con Make (Linux/Mac)
```bash
make venv          # Crea virtual environment
make install       # Installa progetto
make install-dev   # Installa con deps di sviluppo
make test          # Esegue test
```

### Testing
```bash
python test_formatter.py    # Test diretti
pytest                     # Se pytest è installato
```

## Benefici

1. **Isolamento**: Virtual environment previene conflitti di dipendenze
2. **Riproducibilità**: Requirements files garantiscono stesso ambiente
3. **Portabilità**: Setup funziona su Windows, Linux e Mac
4. **Standard**: Segue le best practices Python moderne
5. **CI/CD Ready**: Configurazione pronta per automazione

## Note

- **Nessuna dipendenza esterna richiesta** per uso base
- **Requirements-dev** necessario solo per sviluppo avanzato
- **Setup.py e pyproject.toml** permettono installazione come package
- **Script .sh/.bat** facilitano uso cross-platform

Il progetto mantiene la semplicità originale ma aggiunge robustezza per sviluppo professionale.
