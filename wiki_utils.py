#!/usr/bin/env python3
"""
Utilità per Chinese Grammar Wiki
Script completo per automazione e controllo qualità del progetto.
"""

import os
import sys
import argparse
import subprocess
import re
from pathlib import Path
from collections import defaultdict, Counter


class WikiUtils:
    """Utilità varie per il Chinese Grammar Wiki."""
    
    def __init__(self):
        self.project_root = Path.cwd()
        self.stats = defaultdict(int)
    
    def check_project_health(self):
        """Controlla lo stato generale del progetto."""
        print("🏥 CONTROLLO SALUTE PROGETTO")
        print("=" * 50)
        
        # Controlla struttura directory
        self._check_directory_structure()
        
        # Controlla file Markdown
        self._check_markdown_files()
        
        # Controlla links interni
        self._check_internal_links()
        
        # Controlla pinyin consistency
        self._check_pinyin_consistency()
        
        # Statistiche finali
        self._print_health_stats()
    
    def _check_directory_structure(self):
        """Verifica la struttura delle directory."""
        print("\n📁 Struttura Directory:")
        
        expected_dirs = ['A1', 'A2', 'B1', 'B2']
        for level in expected_dirs:
            level_dir = self.project_root / level
            if level_dir.exists():
                md_count = len(list(level_dir.rglob('*.md')))
                print(f"  ✅ {level}: {md_count} file Markdown")
                self.stats[f'{level}_files'] = md_count
            else:
                print(f"  ❌ {level}: Directory mancante")
    
    def _check_markdown_files(self):
        """Controlla i file Markdown per problemi comuni."""
        print("\n📝 File Markdown:")
        
        all_md_files = list(self.project_root.rglob('*.md'))
        self.stats['total_md_files'] = len(all_md_files)
        
        empty_files = []
        large_files = []
        
        for md_file in all_md_files:
            try:
                size = md_file.stat().st_size
                if size == 0:
                    empty_files.append(md_file)
                elif size > 50000:  # > 50KB
                    large_files.append(md_file)
            except:
                pass
        
        print(f"  📊 Totale file: {len(all_md_files)}")
        if empty_files:
            print(f"  ⚠️  File vuoti: {len(empty_files)}")
            for f in empty_files[:3]:  # Mostra solo i primi 3
                print(f"    • {f}")
        
        if large_files:
            print(f"  📈 File grandi (>50KB): {len(large_files)}")
            for f in large_files[:3]:
                print(f"    • {f}")
    
    def _check_internal_links(self):
        """Controlla i link interni del progetto."""
        print("\n🔗 Link Interni:")
        
        all_md_files = list(self.project_root.rglob('*.md'))
        broken_links = []
        
        # Pattern per link Markdown
        link_pattern = r'\[([^\]]+)\]\(([^)]+)\)'
        
        for md_file in all_md_files:
            try:
                content = md_file.read_text(encoding='utf-8')
                links = re.findall(link_pattern, content)
                
                for link_text, link_url in links:
                    # Verifica solo link relativi (non URL esterni)
                    if not link_url.startswith(('http', 'https', 'mailto', '#')):
                        target_path = md_file.parent / link_url
                        if not target_path.exists():
                            broken_links.append((md_file, link_url))
            except:
                pass
        
        if broken_links:
            print(f"  ❌ Link rotti: {len(broken_links)}")
            for source, link in broken_links[:5]:  # Mostra solo i primi 5
                print(f"    • {source.name} -> {link}")
        else:
            print("  ✅ Nessun link rotto trovato")
    
    def _check_pinyin_consistency(self):
        """Controlla la consistenza del pinyin."""
        print("\n🔤 Consistenza Pinyin:")
        
        all_md_files = list(self.project_root.rglob('*.md'))
        
        # Pattern per pinyin senza toni
        toneless_pattern = r'"([a-z]{2,}(?:\s+[a-z]{2,})*)"'
        potential_issues = []
        
        for md_file in all_md_files:
            try:
                content = md_file.read_text(encoding='utf-8')
                matches = re.findall(toneless_pattern, content)
                
                for match in matches:
                    # Controlla se sembra pinyin senza toni
                    if self._looks_like_toneless_pinyin(match):
                        potential_issues.append((md_file, match))
            except:
                pass
        
        if potential_issues:
            print(f"  ⚠️  Possibili pinyin senza toni: {len(potential_issues)}")
            for source, pinyin in potential_issues[:5]:
                print(f"    • {source.name}: '{pinyin}'")
        else:
            print("  ✅ Pinyin sembra consistente")
    
    def _looks_like_toneless_pinyin(self, text):
        """Determina se un testo sembra pinyin senza toni."""
        # Lista di sillabe pinyin comuni senza toni
        common_toneless = {
            'ni', 'hao', 'ma', 'bu', 'shi', 'wo', 'ta', 'de', 'le', 'zai',
            'you', 'yi', 'ge', 'dao', 'lai', 'qu', 'shang', 'xia', 'kan',
            'ting', 'shuo', 'yao', 'yong', 'hen', 'dou', 'ren', 'jia'
        }
        
        words = text.lower().split()
        return any(word in common_toneless for word in words)
    
    def _print_health_stats(self):
        """Stampa statistiche sulla salute del progetto."""
        print("\n📊 RIEPILOGO STATISTICHE:")
        print(f"  • File Markdown totali: {self.stats['total_md_files']}")
        
        total_level_files = sum(
            self.stats[f'{level}_files'] 
            for level in ['A1', 'A2', 'B1', 'B2'] 
            if f'{level}_files' in self.stats
        )
        print(f"  • File per livello: {total_level_files}")
        
        for level in ['A1', 'A2', 'B1', 'B2']:
            if f'{level}_files' in self.stats:
                print(f"    - {level}: {self.stats[f'{level}_files']}")
    
    def count_grammar_points(self):
        """Conta i punti grammaticali in ogni livello."""
        print("📈 CONTEGGIO PUNTI GRAMMATICALI")
        print("=" * 50)
        
        levels = ['A1', 'A2', 'B1', 'B2']
        total_points = 0
        
        for level in levels:
            level_dir = self.project_root / level
            if not level_dir.exists():
                print(f"❌ Directory {level} non trovata")
                continue
            
            points = self._count_points_in_level(level_dir)
            total_points += points
            print(f"{level}: {points} punti grammaticali")
        
        print(f"\n🎯 TOTALE: {total_points} punti grammaticali")
        return total_points
    
    def _count_points_in_level(self, level_dir):
        """Conta i punti grammaticali in un livello."""
        points = 0
        
        # Pattern per identificare punti grammaticali
        patterns = [
            r'^##\s+\d+\.',  # ## 1. Titolo
            r'^###\s+\d+\.',  # ### 1. Titolo
        ]
        
        for md_file in level_dir.rglob('*.md'):
            try:
                content = md_file.read_text(encoding='utf-8')
                for pattern in patterns:
                    matches = re.findall(pattern, content, re.MULTILINE)
                    points += len(matches)
            except:
                pass
        
        return points
    
    def find_duplicates(self):
        """Trova possibili duplicati o sovrapposizioni."""
        print("🔍 RICERCA DUPLICATI")
        print("=" * 50)
        
        all_md_files = list(self.project_root.rglob('*.md'))
        
        # Raccoglie titoli e pattern
        titles = defaultdict(list)
        chinese_phrases = defaultdict(list)
        
        for md_file in all_md_files:
            try:
                content = md_file.read_text(encoding='utf-8')
                
                # Estrai titoli
                title_matches = re.findall(r'^#+\s+(.+)$', content, re.MULTILINE)
                for title in title_matches:
                    titles[title.strip()].append(md_file)
                
                # Estrai frasi cinesi
                chinese_matches = re.findall(r'[\u4e00-\u9fff]{2,}', content)
                for phrase in chinese_matches:
                    if len(phrase) >= 3:  # Solo frasi di 3+ caratteri
                        chinese_phrases[phrase].append(md_file)
            except:
                pass
        
        # Trova duplicati
        duplicate_titles = {title: files for title, files in titles.items() if len(files) > 1}
        common_phrases = {phrase: files for phrase, files in chinese_phrases.items() if len(files) > 3}
        
        if duplicate_titles:
            print(f"📝 Titoli duplicati: {len(duplicate_titles)}")
            for title, files in list(duplicate_titles.items())[:3]:
                print(f"  • '{title}' in:")
                for f in files[:2]:
                    print(f"    - {f}")
        
        if common_phrases:
            print(f"🔤 Frasi comuni (>3 file): {len(common_phrases)}")
            for phrase, files in list(common_phrases.items())[:3]:
                print(f"  • '{phrase}' in {len(files)} file")
    
    def validate_tables(self):
        """Valida le tabelle Markdown."""
        print("📊 VALIDAZIONE TABELLE")
        print("=" * 50)
        
        all_md_files = list(self.project_root.rglob('*.md'))
        table_issues = []
        
        for md_file in all_md_files:
            try:
                content = md_file.read_text(encoding='utf-8')
                lines = content.split('\n')
                
                for i, line in enumerate(lines):
                    if '|' in line and line.count('|') >= 2:
                        # È una riga di tabella
                        columns = line.count('|') - 1
                        
                        # Controlla se è header
                        if (i + 1 < len(lines) and 
                            '|' in lines[i + 1] and 
                            '-' in lines[i + 1]):
                            
                            # Controlla consistenza colonne
                            separator_cols = lines[i + 1].count('|') - 1
                            if columns != separator_cols:
                                table_issues.append((md_file, i + 1, 'Inconsistent columns'))
            except:
                pass
        
        if table_issues:
            print(f"❌ Problemi tabelle: {len(table_issues)}")
            for file, line, issue in table_issues[:5]:
                print(f"  • {file.name}:{line} - {issue}")
        else:
            print("✅ Tutte le tabelle sembrano valide")


def main():
    """Funzione principale."""
    parser = argparse.ArgumentParser(
        description="Utilità per Chinese Grammar Wiki",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument(
        'command',
        choices=['health', 'count', 'duplicates', 'tables', 'all'],
        help='Comando da eseguire'
    )
    
    args = parser.parse_args()
    
    # Inizializza utilità
    utils = WikiUtils()
    
    print("🧰 WIKI UTILITIES - Chinese Grammar Wiki")
    print("=" * 60)
    
    if args.command == 'health':
        utils.check_project_health()
    elif args.command == 'count':
        utils.count_grammar_points()
    elif args.command == 'duplicates':
        utils.find_duplicates()
    elif args.command == 'tables':
        utils.validate_tables()
    elif args.command == 'all':
        utils.check_project_health()
        print("\n")
        utils.count_grammar_points()
        print("\n")
        utils.find_duplicates()
        print("\n")
        utils.validate_tables()
    
    print("\n✅ Analisi completata!")


if __name__ == "__main__":
    main()
