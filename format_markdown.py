#!/usr/bin/env python3
"""
Markdown Formatter per Chinese Grammar Wiki
Formatta automaticamente i file Markdown del progetto secondo standard consistenti.
"""

import os
import re
import sys
import argparse
from pathlib import Path
from typing import List, Tuple, Optional


class MarkdownFormatter:
    """Formatter per file Markdown con regole specifiche per il progetto Chinese Grammar Wiki."""
    
    def __init__(self):
        self.stats = {
            'files_processed': 0,
            'files_modified': 0,
            'errors': 0,
            'fixes_applied': {}
        }
    
    def format_file(self, file_path: Path) -> bool:
        """
        Formatta un singolo file Markdown.
        
        Args:
            file_path: Percorso del file da formattare
            
        Returns:
            True se il file è stato modificato, False altrimenti
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                original_content = f.read()
            
            formatted_content = self.format_content(original_content)
            
            if original_content != formatted_content:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(formatted_content)
                self.stats['files_modified'] += 1
                print(f"✅ Formattato: {file_path}")
                return True
            else:
                print(f"✓ Già corretto: {file_path}")
                return False
                
        except Exception as e:
            print(f"❌ Errore nel processare {file_path}: {e}")
            self.stats['errors'] += 1
            return False
        finally:
            self.stats['files_processed'] += 1
    
    def format_content(self, content: str) -> str:
        """
        Applica tutte le regole di formattazione al contenuto.
        
        Args:
            content: Contenuto originale del file
            
        Returns:
            Contenuto formattato
        """
        # Lista delle regole di formattazione da applicare
        rules = [
            self.fix_headers_spacing,
            self.fix_table_formatting,
            self.fix_code_blocks,
            self.fix_list_formatting,
            self.normalize_chinese_punctuation,
            self.fix_pinyin_formatting,
            self.fix_line_endings,
            self.remove_trailing_whitespace,
            self.normalize_spacing_around_chinese
        ]
        
        formatted = content
        for rule in rules:
            formatted = rule(formatted)
        
        return formatted
    
    def fix_headers_spacing(self, content: str) -> str:
        """Corregge la spaziatura intorno agli headers."""
        lines = content.split('\n')
        formatted_lines = []
        
        i = 0
        while i < len(lines):
            line = lines[i]
            
            # Salta le righe vuote se stiamo aspettando un header
            if line.strip() == '' and i + 1 < len(lines):
                # Guarda avanti per vedere se c'è un header
                next_non_empty = i + 1
                while (next_non_empty < len(lines) and 
                       lines[next_non_empty].strip() == ''):
                    next_non_empty += 1
                
                if (next_non_empty < len(lines) and 
                    re.match(r'^#{1,6}[^#]', lines[next_non_empty])):
                    # C'è un header in arrivo, salta le righe vuote per ora
                    i += 1
                    continue
            
            # Se la riga è un header
            if re.match(r'^#{1,6}[^#]', line):
                # Prima sistema headers senza spazio dopo #
                line = re.sub(r'^(#{1,6})([^\s#])', r'\1 \2', line)
                line = line.rstrip()  # Rimuovi spazi extra alla fine
                
                # Aggiungi riga vuota prima se necessario (non all'inizio del file)
                if (len(formatted_lines) > 0 and formatted_lines[-1].strip() != ''):
                    formatted_lines.append('')
                
                formatted_lines.append(line)
                
                # Controlla se c'è contenuto dopo (non header)
                next_idx = i + 1
                while (next_idx < len(lines) and 
                       lines[next_idx].strip() == ''):
                    next_idx += 1
                
                # Se c'è contenuto dopo l'header, aggiungi una riga vuota
                if next_idx < len(lines):
                    formatted_lines.append('')
                
                i += 1
            else:
                # Non è un header, aggiungi così com'è
                formatted_lines.append(line)
                i += 1
        
        self._track_fix('headers_spacing')
        return '\n'.join(formatted_lines)
    
    def fix_table_formatting(self, content: str) -> str:
        """Migliora la formattazione delle tabelle."""
        lines = content.split('\n')
        formatted_lines = []
        in_table = False
        
        for i, line in enumerate(lines):
            if '|' in line and line.strip().startswith('|') and line.strip().endswith('|'):
                # È una riga di tabella
                if not in_table:
                    # Prima riga di tabella - aggiungi spazio prima se necessario
                    if i > 0 and formatted_lines[-1].strip() != '':
                        formatted_lines.append('')
                    in_table = True
                
                # Formatta la riga della tabella
                formatted_line = self._format_table_row(line)
                formatted_lines.append(formatted_line)
                
            elif in_table and line.strip() == '':
                # Riga vuota in tabella - mantieni
                formatted_lines.append(line)
                
            else:
                # Non è una riga di tabella
                if in_table:
                    # Fine tabella - aggiungi spazio dopo se necessario
                    if line.strip() != '':
                        formatted_lines.append('')
                    in_table = False
                formatted_lines.append(line)
        
        self._track_fix('table_formatting')
        return '\n'.join(formatted_lines)
    
    def _format_table_row(self, line: str) -> str:
        """Formatta una singola riga di tabella."""
        # Rimuovi spazi extra intorno ai pipe
        parts = [part.strip() for part in line.split('|')]
        
        # Ricostruisci la riga con spaziatura consistente
        if len(parts) > 2:  # Ha contenuto effettivo
            formatted = '| ' + ' | '.join(parts[1:-1]) + ' |'
            return formatted
        return line
    
    def fix_code_blocks(self, content: str) -> str:
        """Migliora la formattazione dei blocchi di codice."""
        lines = content.split('\n')
        formatted_lines = []
        in_code_block = False
        
        for i, line in enumerate(lines):
            # Identifica apertura/chiusura code block
            if line.startswith('```'):
                if not in_code_block:
                    # Apertura code block
                    in_code_block = True
                    
                    # Aggiungi riga vuota prima se necessario
                    if (i > 0 and formatted_lines and 
                        formatted_lines[-1].strip() != ''):
                        formatted_lines.append('')
                    
                    # Specifica linguaggio se mancante
                    if line.strip() == '```':
                        line = '```text'
                    
                    formatted_lines.append(line)
                else:
                    # Chiusura code block
                    in_code_block = False
                    formatted_lines.append(line)
                    
                    # Aggiungi riga vuota dopo se necessario
                    if (i + 1 < len(lines) and 
                        lines[i + 1].strip() != ''):
                        formatted_lines.append('')
            else:
                # Riga normale o contenuto code block
                formatted_lines.append(line)
        
        self._track_fix('code_blocks')
        return '\n'.join(formatted_lines)
    
    def fix_list_formatting(self, content: str) -> str:
        """Migliora la formattazione delle liste."""
        lines = content.split('\n')
        formatted_lines = []
        
        for i, line in enumerate(lines):
            # Lista non ordinata
            if re.match(r'^\s*[-*+]\s', line):
                # Normalizza a trattini
                line = re.sub(r'^\s*[-*+]\s', '- ', line)
                
                # Assicura spazio prima della lista se necessario
                if (i > 0 and formatted_lines and 
                    formatted_lines[-1].strip() != '' and 
                    not re.match(r'^\s*[-*+]\s', formatted_lines[-1])):
                    formatted_lines.append('')
            
            # Lista ordinata
            elif re.match(r'^\s*\d+\.\s', line):
                # Normalizza la numerazione
                indent = len(line) - len(line.lstrip())
                number = re.match(r'^\s*(\d+)', line).group(1)
                content_match = re.match(r'^\s*\d+\.\s*(.*)', line)
                if content_match:
                    line = ' ' * indent + f"{number}. {content_match.group(1)}"
                
                # Assicura spazio prima della lista se necessario
                if (i > 0 and formatted_lines and 
                    formatted_lines[-1].strip() != '' and 
                    not re.match(r'^\s*\d+\.\s', formatted_lines[-1])):
                    formatted_lines.append('')
            
            formatted_lines.append(line)
        
        self._track_fix('list_formatting')
        return '\n'.join(formatted_lines)
    
    def normalize_chinese_punctuation(self, content: str) -> str:
        """Normalizza la punteggiatura cinese."""
        # Sostituisci virgole inglesi con cinesi in contesti cinesi
        content = re.sub(r'([\u4e00-\u9fff]),(?=[\u4e00-\u9fff])', r'\1，', content)
        
        # Sostituisci punti inglesi con cinesi alla fine di frasi cinesi
        # Ma NON convertire ellissi (due o più punti consecutivi)
        content = re.sub(r'([\u4e00-\u9fff])\.(?!\.)', r'\1。', content)
        
        self._track_fix('chinese_punctuation')
        return content
    
    def fix_pinyin_formatting(self, content: str) -> str:
        """Corregge errori comuni nel pinyin."""
        # Capitalizza i nomi propri nel pinyin tra virgolette
        def capitalize_pinyin(match):
            pinyin = match.group(1)
            # Capitalizza solo la prima parola
            words = pinyin.split()
            if words:
                words[0] = words[0].capitalize()
            return f'"{" ".join(words)}"'
        
        content = re.sub(r'"([a-z][a-z\s]+?)"(?=\s*\([\u4e00-\u9fff])', capitalize_pinyin, content)
        
        self._track_fix('pinyin_formatting')
        return content
    
    def fix_line_endings(self, content: str) -> str:
        """Normalizza i line endings."""
        # Converte tutti i line endings in \n
        content = content.replace('\r\n', '\n').replace('\r', '\n')
        
        # Rimuove righe vuote multiple (max 2 consecutive)
        content = re.sub(r'\n{3,}', '\n\n', content)
        
        self._track_fix('line_endings')
        return content
    
    def remove_trailing_whitespace(self, content: str) -> str:
        """Rimuove spazi trailing da ogni riga."""
        lines = content.split('\n')
        cleaned_lines = [line.rstrip() for line in lines]
        
        self._track_fix('trailing_whitespace')
        return '\n'.join(cleaned_lines)
    
    def normalize_spacing_around_chinese(self, content: str) -> str:
        """Normalizza la spaziatura intorno al testo cinese."""
        # Aggiungi spazio tra caratteri cinesi e caratteri latini
        content = re.sub(r'([\u4e00-\u9fff])([a-zA-Z])', r'\1 \2', content)
        content = re.sub(r'([a-zA-Z])([\u4e00-\u9fff])', r'\1 \2', content)
        
        # Non aggiungere spazi dentro le parentesi con caratteri cinesi
        content = re.sub(r'\(\s*([\u4e00-\u9fff][^)]*?)\s*\)', r'(\1)', content)
        
        self._track_fix('chinese_spacing')
        return content
    
    def _track_fix(self, fix_type: str):
        """Traccia i tipi di fix applicati."""
        self.stats['fixes_applied'][fix_type] = self.stats['fixes_applied'].get(fix_type, 0) + 1
    
    def format_directory(self, directory: Path, recursive: bool = True) -> None:
        """
        Formatta tutti i file Markdown in una directory.
        
        Args:
            directory: Directory da processare
            recursive: Se processare le sottodirectory
        """
        if not directory.exists():
            print(f"❌ Directory non trovata: {directory}")
            return
        
        pattern = '**/*.md' if recursive else '*.md'
        md_files = list(directory.glob(pattern))
        
        if not md_files:
            print(f"ℹ️ Nessun file Markdown trovato in {directory}")
            return
        
        print(f"🔍 Trovati {len(md_files)} file Markdown in {directory}")
        print()
        
        for file_path in sorted(md_files):
            self.format_file(file_path)
    
    def print_stats(self):
        """Stampa le statistiche finali."""
        print("\n" + "="*60)
        print("📊 STATISTICHE FORMATTAZIONE")
        print("="*60)
        print(f"File processati: {self.stats['files_processed']}")
        print(f"File modificati: {self.stats['files_modified']}")
        print(f"Errori: {self.stats['errors']}")
        
        if self.stats['fixes_applied']:
            print("\n🔧 Fix applicati:")
            for fix_type, count in sorted(self.stats['fixes_applied'].items()):
                print(f"  • {fix_type.replace('_', ' ').title()}: {count}")
        
        success_rate = ((self.stats['files_processed'] - self.stats['errors']) / 
                       max(self.stats['files_processed'], 1) * 100)
        print(f"\n✅ Tasso di successo: {success_rate:.1f}%")


def main():
    """Funzione principale."""
    parser = argparse.ArgumentParser(
        description="Formatter per file Markdown del Chinese Grammar Wiki",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Esempi d'uso:
  python format_markdown.py                    # Formatta tutto il progetto
  python format_markdown.py B2/                # Formatta solo la directory B2
  python format_markdown.py B2/README.md       # Formatta un singolo file
  python format_markdown.py --no-recursive B1/ # Solo file nella directory principale
        """
    )
    
    parser.add_argument(
        'path',
        nargs='?',
        default='.',
        help='Percorso del file o directory da formattare (default: directory corrente)'
    )
    
    parser.add_argument(
        '--no-recursive',
        action='store_true',
        help='Non processare le sottodirectory ricorsivamente'
    )
    
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Mostra cosa verrebbe fatto senza effettuare modifiche'
    )
    
    args = parser.parse_args()
    
    # Inizializza il formatter
    formatter = MarkdownFormatter()
    
    if args.dry_run:
        print("🧪 MODALITÀ DRY-RUN - Nessuna modifica verrà effettuata\n")
    
    # Determina se è un file o directory
    path = Path(args.path)
    
    if path.is_file():
        if path.suffix.lower() == '.md':
            if not args.dry_run:
                formatter.format_file(path)
            else:
                print(f"Verrebbe formattato: {path}")
        else:
            print(f"❌ {path} non è un file Markdown")
            sys.exit(1)
    elif path.is_dir():
        if not args.dry_run:
            formatter.format_directory(path, recursive=not args.no_recursive)
        else:
            pattern = '**/*.md' if not args.no_recursive else '*.md'
            md_files = list(path.glob(pattern))
            print(f"Verrebbero formattati {len(md_files)} file:")
            for file_path in sorted(md_files):
                print(f"  • {file_path}")
    else:
        print(f"❌ Percorso non valido: {path}")
        sys.exit(1)
    
    # Stampa statistiche finali
    if not args.dry_run:
        formatter.print_stats()


if __name__ == "__main__":
    main()
