# AI Assistant (MVP)

A versatile command-line tool that can perform both code analysis and job search using various AI models. This MVP version supports multiple AI providers and provides two main functionalities.

## Features

### 1. Code Analysis
- Scans directories for code files
- Supports Python, JavaScript, TypeScript, and Java
- AI-powered code suggestions
- Focuses on:
  - Code quality and best practices
  - Potential bugs or issues
  - Performance optimizations

### 2. Job Search
- AI-powered job search and analysis
- Customizable search preferences:
  - Job Type (Software Engineer, Full Stack, etc.)
  - Seniority Level (Entry to Architect)
  - Work Type (Remote, Hybrid, On-site)
  - Location (optional)
- Generates detailed job postings
- Saves results to CSV format

## Installation

1. Install the required dependencies:
   ```bash
   pip install -r mvp_requirements.txt
   ```

2. Create a `.env` file in the project root and add your API keys:
   ```
   GEMINI_API_KEY=your_gemini_key
   OPENAI_API_KEY=your_openai_key
   ```

## Usage

Run the assistant:
```bash
python mvp_analyzer.py
```

The program will:
1. Show available AI models
2. Let you choose between:
   - Code Analysis
   - Job Search

### Code Analysis Mode
```bash
python mvp_analyzer.py -o analysis_results.txt
```
- Enter the directory to analyze when prompted
- Results will be saved to the specified output file

### Job Search Mode
```bash
python mvp_analyzer.py -o job_postings.csv
```
- Select your job preferences when prompted
- Results will be saved as a CSV file

## Available AI Models

- Google Gemini Pro
- Google Gemini 2.0 Flash
- OpenAI GPT-4
- OpenAI GPT-3.5 Turbo

## Job Types Supported

1. Software Engineer
2. Full Stack Developer
3. Frontend Developer
4. Backend Developer
5. DevOps Engineer
6. Data Engineer
7. Machine Learning Engineer
8. Mobile Developer

## Requirements

- Python 3.7+
- API keys for selected AI providers
- Internet connection for AI analysis

## Note

This MVP version uses AI to generate job postings. In a production environment, you would want to integrate with actual job board APIs for real job listings. 