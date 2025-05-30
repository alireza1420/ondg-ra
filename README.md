# AI Code Analyzer

A command-line tool that uses AI to analyze code and suggest improvements. This tool can scan entire codebases and provide detailed suggestions for code improvements, potential bugs, and best practices.

## Features

- Scans entire directories for code files
- Supports multiple programming languages
- AI-powered code analysis and suggestions
- Beautiful command-line interface
- Option to save results to a file

## Supported Languages

- Python (.py)
- JavaScript (.js)
- TypeScript (.ts)
- Java (.java)
- C++ (.cpp)
- C (.c)
- C# (.cs)
- Go (.go)
- Ruby (.rb)
- PHP (.php)

## Installation

1. Clone this repository
2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Create a `.env` file in the project root and add your OpenAI API key:
   ```
   OPENAI_API_KEY=your_api_key_here
   ```

## Usage

Basic usage:
```bash
python code_analyzer.py /path/to/your/code
```

Save results to a file:
```bash
python code_analyzer.py /path/to/your/code -o analysis_results.txt
```

## Example Output

The tool will display:
- Number of files found
- Analysis progress for each file
- Detailed suggestions for improvements
- Any errors encountered during analysis

## Requirements

- Python 3.7+
- OpenAI API key
- Internet connection for AI analysis

## Note

This tool uses the OpenAI API for code analysis. Make sure you have sufficient API credits and are aware of the associated costs. #   o n d g - r a  
 