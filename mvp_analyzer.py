import os
import argparse
from pathlib import Path
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables
load_dotenv()

class SimpleCodeAnalyzer:
    def __init__(self, directory: str):
        self.directory = Path(directory)
        # Configure Gemini API
        genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
        self.model = genai.GenerativeModel('gemini-pro')
        # Focus on most common languages for MVP
        self.supported_extensions = {
            '.py': 'python',
            '.js': 'javascript',
            '.ts': 'typescript',
            '.java': 'java'
        }

    def scan_directory(self):
        """Scan directory for code files."""
        code_files = []
        for root, _, files in os.walk(self.directory):
            for file in files:
                file_path = Path(root) / file
                if file_path.suffix in self.supported_extensions:
                    try:
                        with open(file_path, 'r', encoding='utf-8') as f:
                            content = f.read()
                        code_files.append({
                            'path': str(file_path),
                            'content': content,
                            'language': self.supported_extensions[file_path.suffix]
                        })
                    except Exception as e:
                        print(f"Error reading {file_path}: {str(e)}")
        return code_files

    def analyze_code(self, file_data):
        """Analyze code using Gemini API."""
        try:
            prompt = f"""You are a code reviewer. Analyze this {file_data['language']} code and provide 3 key suggestions for improvement.
            Focus on:
            1. Code quality and best practices
            2. Potential bugs or issues
            3. Performance optimizations

            Code to analyze:
            {file_data['content']}"""

            response = self.model.generate_content(prompt)
            return {
                'path': file_data['path'],
                'suggestions': response.text
            }
        except Exception as e:
            return {
                'path': file_data['path'],
                'error': str(e)
            }

def main():
    parser = argparse.ArgumentParser(description='Simple AI Code Analyzer (Gemini Version)')
    parser.add_argument('directory', help='Directory to analyze')
    parser.add_argument('--output', '-o', help='Output file for results')
    args = parser.parse_args()

    print("🔍 Starting Code Analysis (Using Gemini)")
    
    analyzer = SimpleCodeAnalyzer(args.directory)
    code_files = analyzer.scan_directory()
    
    if not code_files:
        print("No supported code files found.")
        return

    print(f"\nFound {len(code_files)} code files to analyze.")
    
    results = []
    for file_data in code_files:
        print(f"\nAnalyzing: {file_data['path']}")
        result = analyzer.analyze_code(file_data)
        results.append(result)
        
        if 'error' in result:
            print(f"Error analyzing {result['path']}: {result['error']}")
        else:
            print("\nSuggestions:")
            print(result['suggestions'])
            print("-" * 50)

    if args.output:
        try:
            with open(args.output, 'w', encoding='utf-8') as f:
                for result in results:
                    f.write(f"\n=== {result['path']} ===\n")
                    if 'error' in result:
                        f.write(f"Error: {result['error']}\n")
                    else:
                        f.write(result['suggestions'] + "\n")
            print(f"\nResults saved to {args.output}")
        except Exception as e:
            print(f"Error saving results: {str(e)}")

if __name__ == '__main__':
    main() 