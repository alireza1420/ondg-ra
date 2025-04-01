import os
import click
from pathlib import Path
from rich.console import Console
from rich.panel import Panel
from rich.syntax import Syntax
from dotenv import load_dotenv
import openai
from typing import List, Dict

# Load environment variables
load_dotenv()

# Initialize OpenAI client
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
console = Console()

class CodeAnalyzer:
    def __init__(self, directory: str):
        self.directory = Path(directory)
        self.supported_extensions = {
            '.py': 'python',
            '.js': 'javascript',
            '.ts': 'typescript',
            '.java': 'java',
            '.cpp': 'cpp',
            '.c': 'c',
            '.cs': 'csharp',
            '.go': 'go',
            '.rb': 'ruby',
            '.php': 'php'
        }

    def scan_directory(self) -> List[Dict]:
        """Scan directory for code files and analyze them."""
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
                        console.print(f"[red]Error reading {file_path}: {str(e)}[/red]")
        return code_files

    def analyze_code(self, file_data: Dict) -> Dict:
        """Analyze code using OpenAI API and return suggestions."""
        try:
            response = client.chat.completions.create(
                model="gpt-4-turbo-preview",
                messages=[
                    {"role": "system", "content": "You are an expert code reviewer. Analyze the code and provide specific suggestions for improvements, focusing on best practices, potential bugs, and performance optimizations."},
                    {"role": "user", "content": f"Analyze this {file_data['language']} code:\n\n{file_data['content']}"}
                ],
                temperature=0.7,
                max_tokens=1000
            )
            return {
                'path': file_data['path'],
                'suggestions': response.choices[0].message.content
            }
        except Exception as e:
            return {
                'path': file_data['path'],
                'error': str(e)
            }

@click.command()
@click.argument('directory', type=click.Path(exists=True))
@click.option('--output', '-o', type=click.Path(), help='Output file for the analysis results')
def analyze_codebase(directory: str, output: str):
    """Analyze code in the specified directory and provide AI-powered suggestions."""
    console.print(Panel.fit("🔍 Starting Code Analysis", title="Code Analyzer"))
    
    analyzer = CodeAnalyzer(directory)
    code_files = analyzer.scan_directory()
    
    if not code_files:
        console.print("[yellow]No supported code files found in the specified directory.[/yellow]")
        return

    console.print(f"\n[green]Found {len(code_files)} code files to analyze.[/green]")
    
    results = []
    for file_data in code_files:
        console.print(f"\n[blue]Analyzing: {file_data['path']}[/blue]")
        result = analyzer.analyze_code(file_data)
        results.append(result)
        
        # Display results
        if 'error' in result:
            console.print(f"[red]Error analyzing {result['path']}: {result['error']}[/red]")
        else:
            console.print(Panel(
                Syntax(result['suggestions'], "markdown", theme="monokai"),
                title=f"Suggestions for {result['path']}"
            ))

    # Save results to file if output path is specified
    if output:
        try:
            with open(output, 'w', encoding='utf-8') as f:
                for result in results:
                    f.write(f"\n=== {result['path']} ===\n")
                    if 'error' in result:
                        f.write(f"Error: {result['error']}\n")
                    else:
                        f.write(result['suggestions'] + "\n")
            console.print(f"\n[green]Results saved to {output}[/green]")
        except Exception as e:
            console.print(f"[red]Error saving results: {str(e)}[/red]")

if __name__ == '__main__':
    analyze_codebase() 