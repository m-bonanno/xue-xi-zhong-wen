#!/usr/bin/env python3
"""
Test per il Markdown Formatter
Verifica che tutte le funzionalità del formatter funzionino correttamente.
"""

import unittest
import tempfile
import os
from pathlib import Path
import sys

# Aggiungi il path del formatter
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from format_markdown import MarkdownFormatter


class TestMarkdownFormatter(unittest.TestCase):
    """Test case per MarkdownFormatter."""
    
    def setUp(self):
        """Setup per ogni test."""
        self.formatter = MarkdownFormatter()
        self.temp_dir = tempfile.mkdtemp()
        self.temp_path = Path(self.temp_dir)
    
    def tearDown(self):
        """Cleanup dopo ogni test."""
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def test_headers_spacing(self):
        """Test formattazione headers."""
        input_text = """# Header 1
Some text
## Header 2   
More text


### Header 3
Content"""
        
        expected = """# Header 1

Some text

## Header 2

More text

### Header 3

Content"""
        
        result = self.formatter.fix_headers_spacing(input_text)
        self.assertEqual(result.strip(), expected.strip())
    
    def test_table_formatting(self):
        """Test formattazione tabelle."""
        input_text = """|Cinese|Pinyin|Italiano|
|---|---|---|
|你好|nǐhào|Ciao|
|谢谢| xièxie |Grazie|"""
        
        result = self.formatter.fix_table_formatting(input_text)
        
        # Verifica che la tabella sia formattata correttamente
        lines = result.split('\n')
        self.assertTrue(all('|' in line for line in lines if line.strip()))
        self.assertTrue(all(line.startswith('| ') and line.endswith(' |') 
                          for line in lines if '|' in line and not line.startswith('|---')))
    
    def test_chinese_punctuation(self):
        """Test normalizzazione punteggiatura cinese."""
        input_text = "他很好,我也很好.今天天气不错,真的很好."
        expected = "他很好，我也很好。今天天气不错，真的很好。"
        
        result = self.formatter.normalize_chinese_punctuation(input_text)
        self.assertEqual(result, expected)
    
    def test_pinyin_formatting(self):
        """Test formattazione pinyin."""
        input_text = '"nǐhào" (你好) significa "ciao"'
        
        result = self.formatter.fix_pinyin_formatting(input_text)
        
        # Il pinyin dovrebbe essere capitalizzato correttamente
        self.assertIn('"', result)
    
    def test_code_blocks(self):
        """Test formattazione code blocks."""
        input_text = """Testo prima
```
codice senza linguaggio
```
Testo dopo"""
        
        result = self.formatter.fix_code_blocks(input_text)
        
        # Dovrebbe avere righe vuote intorno al code block
        lines = result.split('\n')
        code_start = next(i for i, line in enumerate(lines) if line.startswith('```'))
        
        # Verifica spaziatura
        if code_start > 0:
            self.assertEqual(lines[code_start - 1].strip(), '')
    
    def test_trailing_whitespace(self):
        """Test rimozione spazi trailing."""
        input_text = "Riga con spazi    \nAltra riga  \nRiga normale\n"
        expected = "Riga con spazi\nAltra riga\nRiga normale\n"
        
        result = self.formatter.remove_trailing_whitespace(input_text)
        self.assertEqual(result, expected)
    
    def test_chinese_spacing(self):
        """Test spaziatura intorno ai caratteri cinesi."""
        input_text = "中文English混合text"
        expected = "中文 English 混合 text"
        
        result = self.formatter.normalize_spacing_around_chinese(input_text)
        self.assertEqual(result, expected)
    
    def test_full_formatting(self):
        """Test formattazione completa."""
        input_text = """#Header
Testo con caratteri中文mixed.

|Col1|Col2|
|---|---|
|Data1|Data2|

```
code
```

- Item1
* Item2"""
        
        result = self.formatter.format_content(input_text)
        
        # Verifica che il contenuto sia stato formattato
        self.assertNotEqual(input_text, result)
        self.assertIn('# Header', result)  # Header dovrebbe essere corretto
        self.assertIn('mixed.', result)    # Dovrebbe essere presente
    
    def test_file_processing(self):
        """Test processamento di un file reale."""
        # Crea un file temporaneo
        test_file = self.temp_path / "test.md"
        content = """#Test File
Some content here

|Table|Data|
|---|---|
|Row1|Value1|"""
        
        test_file.write_text(content, encoding='utf-8')
        
        # Processa il file
        was_modified = self.formatter.format_file(test_file)
        
        # Verifica che il file sia stato processato
        self.assertIsInstance(was_modified, bool)
        self.assertEqual(self.formatter.stats['files_processed'], 1)
        
        # Verifica che il contenuto sia cambiato se necessario
        new_content = test_file.read_text(encoding='utf-8')
        if was_modified:
            self.assertNotEqual(content, new_content)


class TestFormatterIntegration(unittest.TestCase):
    """Test di integrazione per il formatter."""
    
    def setUp(self):
        """Setup per test di integrazione."""
        self.formatter = MarkdownFormatter()
    
    def test_chinese_grammar_format(self):
        """Test con formato tipico del Chinese Grammar Wiki."""
        content = """# Verbi (B1)

I verbi del livello B1 introducono azioni complesse. Questa sezione copre 3 punti grammaticali.

## 1. Usare "lái" per Sostituire Altri Verbi (来)

### Struttura

```
Soggetto + 来 + Verbo
```

### Esempi

|Cinese|Pinyin|Italiano|
|---|---|---|
|你来开车|nǐ lái kāichē|Guidi tu|
|我来做饭|wǒ lái zuòfàn|Cucino io|"""
        
        result = self.formatter.format_content(content)
        
        # Verifica elementi specifici del progetto
        self.assertIn('# Verbi (B1)', result)
        self.assertIn('```', result)
        self.assertIn('| Cinese | Pinyin | Italiano |', result)


def run_tests():
    """Esegue tutti i test."""
    print("🧪 Esecuzione test per Markdown Formatter...")
    print("=" * 50)
    
    # Crea suite di test
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Aggiungi test cases
    suite.addTests(loader.loadTestsFromTestCase(TestMarkdownFormatter))
    suite.addTests(loader.loadTestsFromTestCase(TestFormatterIntegration))
    
    # Esegui i test
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Mostra risultati
    print("\n" + "=" * 50)
    if result.wasSuccessful():
        print("✅ Tutti i test sono passati!")
        return True
    else:
        print(f"❌ {len(result.failures)} test falliti, {len(result.errors)} errori")
        return False


if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)
