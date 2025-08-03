#!/usr/bin/env python3
"""
Development utility for testing different prompts
"""
import sys
import os
import click
import json
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from prompts import PromptTemplates, PromptVersion, get_prompt
from prompts.config import prompt_config
from agents import LiteratureReviewAgent
from parsers.pdf_parser import PDFParser
from utils import clean_text

@click.group()
def cli():
    """Development tools for prompt experimentation"""
    pass

@cli.command()
def list_prompts():
    """List all available prompt templates"""
    click.echo("=== Built-in Prompt Versions ===")
    for version in PromptVersion:
        click.echo(f"\n{version.value}:")
        templates = PromptTemplates(version)
        for task in ['summary', 'key_findings', 'methodology', 'contributions', 'limitations']:
            try:
                prompt = templates.get_prompt(task, text="[SAMPLE TEXT]")
                lines = prompt.strip().split('\n')
                first_line = lines[0].strip() if lines else ""
                click.echo(f"  {task}: {first_line[:60]}...")
            except:
                click.echo(f"  {task}: [Not available]")
    
    click.echo("\n=== Custom Configurations ===")
    configs = prompt_config.list_configurations()
    for config_name in configs:
        click.echo(f"\n{config_name}:")
        tasks = prompt_config.list_tasks(config_name)
        for task in tasks:
            if task != 'system':
                try:
                    prompt = prompt_config.get_custom_prompt(config_name, task, text="[SAMPLE TEXT]")
                    lines = prompt.strip().split('\n')
                    first_line = lines[0].strip() if lines else ""
                    click.echo(f"  {task}: {first_line[:60]}...")
                except:
                    click.echo(f"  {task}: [Error loading]")

@cli.command()
@click.argument('task', type=click.Choice(['summary', 'key_findings', 'methodology', 'contributions', 'limitations']))
@click.option('--version', type=click.Choice(['v1_basic', 'v2_detailed', 'v3_structured', 'experimental']), 
              default='v2_detailed')
@click.option('--custom', help='Use custom configuration instead of built-in version')
@click.option('--text', help='Sample text to use in prompt (or provide via stdin)')
def show_prompt(task, version, custom, text):
    """Show the actual prompt that would be sent to the AI"""
    
    if not text:
        if not sys.stdin.isatty():
            text = sys.stdin.read().strip()
        else:
            text = "This is sample text for the academic paper analysis."
    
    try:
        if custom:
            prompt = prompt_config.get_custom_prompt(custom, task, text=text)
            click.echo(f"=== Custom Configuration: {custom} ===")
        else:
            version_map = {
                'v1_basic': PromptVersion.V1_BASIC,
                'v2_detailed': PromptVersion.V2_DETAILED,
                'v3_structured': PromptVersion.V3_STRUCTURED,
                'experimental': PromptVersion.EXPERIMENTAL
            }
            prompt_version = version_map[version]
            prompt = get_prompt(task, prompt_version, text=text)
            click.echo(f"=== Built-in Version: {version} ===")
        
        click.echo(f"Task: {task}")
        click.echo("=" * 60)
        click.echo(prompt)
        click.echo("=" * 60)
        click.echo(f"Character count: {len(prompt)}")
        
    except Exception as e:
        click.echo(f"Error: {e}", err=True)

@cli.command()
@click.argument('pdf_file')
@click.option('--task', type=click.Choice(['summary', 'key_findings', 'methodology', 'contributions', 'limitations']),
              default='summary')
@click.option('--version1', default='v2_detailed', help='First prompt version to compare')
@click.option('--version2', default='v3_structured', help='Second prompt version to compare')
@click.option('--custom1', help='First custom configuration to compare')
@click.option('--custom2', help='Second custom configuration to compare')
@click.option('--output', help='Save comparison to JSON file')
def compare_prompts(pdf_file, task, version1, version2, custom1, custom2, output):
    """Compare two different prompt configurations on the same PDF"""
    
    # Extract text from PDF
    try:
        parser = PDFParser()
        text = parser.extract_text(pdf_file)
        metadata = parser.extract_metadata(pdf_file)
        cleaned_text = clean_text(text)
        
        if not cleaned_text:
            click.echo("Error: Could not extract text from PDF", err=True)
            return
            
        click.echo(f"Extracted {len(cleaned_text)} characters from {pdf_file}")
        
    except Exception as e:
        click.echo(f"Error processing PDF: {e}", err=True)
        return
    
    # Prepare configurations
    configs = []
    
    if custom1:
        configs.append(("custom", custom1, custom1))
    else:
        configs.append(("builtin", version1, version1))
    
    if custom2:
        configs.append(("custom", custom2, custom2))
    else:
        configs.append(("builtin", version2, version2))
    
    results = {}
    
    # Test each configuration
    for config_type, config_name, display_name in configs:
        click.echo(f"\nTesting {display_name}...")
        
        try:
            if config_type == "custom":
                agent = LiteratureReviewAgent(custom_config=config_name)
            else:
                version_map = {
                    'v1_basic': PromptVersion.V1_BASIC,
                    'v2_detailed': PromptVersion.V2_DETAILED,
                    'v3_structured': PromptVersion.V3_STRUCTURED,
                    'experimental': PromptVersion.EXPERIMENTAL
                }
                prompt_version = version_map.get(config_name, PromptVersion.V2_DETAILED)
                agent = LiteratureReviewAgent(prompt_version=prompt_version)
            
            # Get specific task result
            from langchain.text_splitter import RecursiveCharacterTextSplitter
            text_splitter = RecursiveCharacterTextSplitter(chunk_size=3000, chunk_overlap=200)
            chunks = text_splitter.split_text(cleaned_text)
            
            if task == 'summary':
                result = agent._generate_summary(chunks)
            elif task == 'key_findings':
                result = agent._extract_key_findings(chunks)
            elif task == 'methodology':
                result = agent._extract_methodology(chunks)
            elif task == 'contributions':
                result = agent._extract_contributions(chunks)
            elif task == 'limitations':
                result = agent._extract_limitations(chunks)
            
            results[display_name] = {
                'config_type': config_type,
                'config_name': config_name,
                'task': task,
                'result': result,
                'result_length': len(str(result))
            }
            
            click.echo(f"✓ Completed {display_name}")
            
        except Exception as e:
            click.echo(f"✗ Error with {display_name}: {e}")
            results[display_name] = {
                'config_type': config_type,
                'config_name': config_name,
                'task': task,
                'error': str(e)
            }
    
    # Display results
    click.echo("\n" + "="*80)
    click.echo("COMPARISON RESULTS")
    click.echo("="*80)
    
    for config_name, result in results.items():
        click.echo(f"\n--- {config_name} ---")
        if 'error' in result:
            click.echo(f"ERROR: {result['error']}")
        else:
            click.echo(f"Result length: {result['result_length']} characters")
            click.echo("Preview:")
            result_str = str(result['result'])
            preview = result_str[:300] + "..." if len(result_str) > 300 else result_str
            click.echo(preview)
    
    # Save to file if requested
    if output:
        comparison_data = {
            'pdf_file': pdf_file,
            'task': task,
            'timestamp': str(click.DateTime()),
            'results': results
        }
        
        with open(output, 'w') as f:
            json.dump(comparison_data, f, indent=2)
        
        click.echo(f"\nComparison saved to {output}")

@cli.command()
@click.argument('config_name')
def create_custom_config(config_name):
    """Create a new custom prompt configuration file"""
    
    config_file = Path(f"prompts/{config_name}.yaml")
    
    if config_file.exists():
        if not click.confirm(f"Configuration {config_name}.yaml already exists. Overwrite?"):
            return
    
    template = f"""# Custom Prompt Configuration: {config_name}
# Edit these prompts to experiment with different approaches

{config_name}:
  system: "You are an expert academic researcher analyzing scientific papers."
  
  summary: |
    Provide a comprehensive summary of this academic paper.
    Focus on the main research question, approach, and key findings.
    
    Text: {{text}}
  
  key_findings: |
    Extract the key findings from this academic paper.
    Return them as a list of bullet points, focusing on concrete results.
    
    Text: {{text}}
  
  methodology: |
    Extract and summarize the methodology used in this research.
    Focus on experimental design, data collection, and analysis methods.
    
    Text: {{text}}
  
  contributions: |
    Identify the main contributions of this research paper.
    List them as bullet points, focusing on novel insights and methods.
    
    Text: {{text}}
  
  limitations: |
    Identify the limitations of this research and any suggested future work.
    List them as bullet points.
    
    Text: {{text}}
"""
    
    config_file.parent.mkdir(exist_ok=True)
    with open(config_file, 'w') as f:
        f.write(template)
    
    click.echo(f"Created {config_file}")
    click.echo(f"Edit the file to customize your prompts, then use: --custom-prompts {config_name}")

if __name__ == '__main__':
    cli()