# Simple AI Code Analyzer (MVP) - Gemini Version

A lightweight command-line tool that uses Google's Gemini AI to analyze code and suggest improvements. This MVP version focuses on core functionality and the most common programming languages.

## Features

- Scans directories for code files
- Supports Python, JavaScript, TypeScript, and Java
- AI-powered code suggestions using Gemini
- Simple command-line interface
- Option to save results to a file

## Installation

1. Install the required dependencies:
   ```bash
   pip install -r mvp_requirements.txt
   ```

2. Create a `.env` file in the project root and add your Gemini API key:
   ```
   GEMINI_API_KEY=your_api_key_here
   ```

## Usage

Basic usage:
```bash
python mvp_analyzer.py /path/to/your/code
```

Save results to a file:
```bash
python mvp_analyzer.py /path/to/your/code -o analysis_results.txt
```

## Requirements

- Python 3.7+
- Google Gemini API key
- Internet connection for AI analysis

## Note

This MVP version uses Google's Gemini Pro model for analysis. Make sure you have sufficient API credits and access to the Gemini API. 