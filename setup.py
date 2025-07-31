#!/usr/bin/env python3
"""
Setup script for Chinese Grammar Wiki Formatter
"""

from setuptools import setup, find_packages
import os

# Read README for long description
readme_path = os.path.join(os.path.dirname(__file__), 'FORMATTER_README.md')
try:
    with open(readme_path, 'r', encoding='utf-8') as f:
        long_description = f.read()
except FileNotFoundError:
    long_description = "Markdown formatter for Chinese Grammar Wiki project"

setup(
    name="chinese-grammar-wiki-formatter",
    version="1.0.0",
    description="Markdown formatter specifically designed for Chinese Grammar Wiki",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Chinese Grammar Wiki Team",
    author_email="",
    url="https://github.com/m-bonanno/xue-xi-zhong-wen",
    
    # Package configuration
    packages=find_packages(),
    py_modules=["format_markdown", "wiki_utils", "test_formatter"],
    
    # Dependencies
    install_requires=[
        # Currently no external dependencies
    ],
    
    # Development dependencies
    extras_require={
        'dev': [
            'pytest>=6.2.0',
            'pytest-cov>=2.12.0',
            'black>=21.0.0',
            'flake8>=3.9.0',
            'mypy>=0.812',
        ]
    },
    
    # Console scripts
    entry_points={
        'console_scripts': [
            'format-md=format_markdown:main',
            'wiki-utils=wiki_utils:main',
        ],
    },
    
    # Classifiers
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Education",
        "Topic :: Documentation",
        "Topic :: Text Processing :: Markup",
        "Topic :: Software Development :: Documentation",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Operating System :: OS Independent",
        "Natural Language :: Chinese (Simplified)",
        "Natural Language :: Italian",
        "Natural Language :: English",
    ],
    
    # Python version requirement
    python_requires=">=3.6",
    
    # Include additional files
    include_package_data=True,
    package_data={
        '': ['*.ini', '*.md', '*.txt'],
    },
    
    # Project URLs
    project_urls={
        'Bug Reports': 'https://github.com/m-bonanno/xue-xi-zhong-wen/issues',
        'Source': 'https://github.com/m-bonanno/xue-xi-zhong-wen',
        'Documentation': 'https://github.com/m-bonanno/xue-xi-zhong-wen/blob/main/FORMATTER_README.md',
    },
)
