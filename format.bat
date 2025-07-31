@echo off
REM Markdown Formatter Script per Windows
REM Formatta automaticamente tutti i file Markdown del progetto

echo ========================================
echo   Chinese Grammar Wiki - MD Formatter
echo ========================================
echo.

REM Controlla se Python è installato
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERRORE: Python non e' installato o non e' nel PATH
    echo Installa Python da https://python.org
    pause
    exit /b 1
)

REM Controlla se siamo in un virtual environment
if defined VIRTUAL_ENV (
    echo 🐍 Virtual environment attivo: %VIRTUAL_ENV%
) else (
    echo ℹ️  Nessun virtual environment attivo
    echo 💡 Considera di usare: python -m venv venv && venv\Scripts\activate
)

REM Esegui il formatter
echo Formattazione in corso...
echo.

python format_markdown.py %*

echo.
echo Formattazione completata!
echo.

REM Se chiamato senza parametri, fai una pausa
if "%~1"=="" (
    pause
)
