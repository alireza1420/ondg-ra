import os
import argparse
from pathlib import Path
from dotenv import load_dotenv
import google.generativeai as genai
import openai
from typing import Dict, Any

# Load environment variables
load_dotenv()

class AIModelHandler:
    def __init__(self, model_name: str):
        self.model_name = model_name
        self.setup_model()

    def setup_model(self):
        """Setup the appropriate AI model based on the model name."""
        if self.model_name.startswith('gemini'):
            genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
            self.model = genai.GenerativeModel(self.model_name)
            self.type = 'gemini'
        elif self.model_name.startswith('gpt'):
            openai.api_key = os.getenv("OPENAI_API_KEY")
            self.type = 'openai'
        else:
            raise ValueError(f"Unsupported model: {self.model_name}")

    def generate_response(self, prompt: str) -> str:
        """Generate response using the appropriate model."""
        if self.type == 'gemini':
            response = self.model.generate_content(prompt)
            return response.text
        elif self.type == 'openai':
            response = openai.chat.completions.create(
                model=self.model_name,
                messages=[{"role": "user", "content": prompt}]
            )
            return response.choices[0].message.content

class SimpleCodeAnalyzer:
    def __init__(self, directory: str, model_name: str):
        self.directory = Path(directory)
        self.ai_handler = AIModelHandler(model_name)
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
        """Analyze code using selected AI model."""
        try:
            prompt = f"""You are a code reviewer. Analyze this {file_data['language']} code and provide 3 key suggestions for improvement.
            Focus on:
            1. Code quality and best practices
            2. Potential bugs or issues
            3. Performance optimizations

            Code to analyze:
            {file_data['content']}"""

            response = self.ai_handler.generate_response(prompt)
            return {
                'path': file_data['path'],
                'suggestions': response
            }
        except Exception as e:
            return {
                'path': file_data['path'],
                'error': str(e)
            }

def get_available_models() -> Dict[str, str]:
    """Return available AI models and their descriptions."""
    return {
        'gemini-pro': 'Google Gemini Pro',
        'gemini-2.0-flash': 'Google Gemini 2.0 Flash',
        'gpt-4': 'OpenAI GPT-4',
        'gpt-3.5-turbo': 'OpenAI GPT-3.5 Turbo'
    }

def main():
    parser = argparse.ArgumentParser(description='AI Code Analyzer')
    parser.add_argument('directory', help='Directory to analyze')
    parser.add_argument('--output', '-o', help='Output file for results')
    args = parser.parse_args()

    # Display available models
    available_models = get_available_models()
    print("\nAvailable AI Models:")
    for model_id, description in available_models.items():
        print(f"- {model_id}: {description}")
    
    # Get user's model choice
    while True:
        model_choice = input("\nEnter the AI model to use: ").strip()
        if model_choice in available_models:
            break
        print("Invalid model choice. Please try again.")

    print(f"\n🔍 Starting Code Analysis (Using {available_models[model_choice]})")
    
    analyzer = SimpleCodeAnalyzer(args.directory, model_choice)
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