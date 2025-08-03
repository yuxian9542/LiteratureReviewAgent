#!/usr/bin/env python3
import click
import os
from input_handlers.input_validator import InputValidator
from parsers.pdf_parser import PDFParser
from agents import LiteratureReviewAgent
from prompts import PromptVersion
from prompts.config import prompt_config
from summarizers import AnalysisFormatter
from utils import setup_logging, clean_text, ProgressTracker, validate_output_format, get_file_extension_from_format
from config import config

@click.command()
@click.option('--input', '-i', required=True, help='PDF file path or URL')
@click.option('--output', '-o', help='Output file for analysis')
@click.option('--format', '-f', default='text', help='Output format: text, markdown, json')
@click.option('--analyze', is_flag=True, help='Perform AI-powered analysis (requires OpenAI API key)')
@click.option('--verbose', '-v', is_flag=True, help='Enable verbose logging')
@click.option('--prompt-version', type=click.Choice(['v1_basic', 'v2_detailed', 'v3_structured', 'experimental']), 
              default='v2_detailed', help='Prompt version to use')
@click.option('--custom-prompts', help='Use custom prompt configuration (e.g., custom_v1, experimental_roleplay)')
@click.option('--list-prompts', is_flag=True, help='List available prompt configurations and exit')
def main(input, output, format, analyze, verbose, prompt_version, custom_prompts, list_prompts):
    """Academic Paper Summarization and Analysis Agent"""
    
    # Handle prompt listing
    if list_prompts:
        click.echo("Available prompt configurations:")
        click.echo("\nBuilt-in versions:")
        for version in PromptVersion:
            click.echo(f"  - {version.value}")
        
        click.echo("\nCustom configurations:")
        configs = prompt_config.list_configurations()
        if configs:
            for config_name in configs:
                tasks = prompt_config.list_tasks(config_name)
                click.echo(f"  - {config_name} (tasks: {', '.join(tasks)})")
        else:
            click.echo("  (none found)")
        return
    
    # Setup logging
    log_level = "DEBUG" if verbose else "INFO"
    logger = setup_logging(log_level)
    
    # Validate output format
    if not validate_output_format(format):
        click.echo(f"Error: Invalid output format '{format}'. Valid formats: text, markdown, json")
        return
    
    # Initialize progress tracker
    total_steps = 4 if analyze else 2
    progress = ProgressTracker(total_steps, "Literature Review")
    
    try:
        # Step 1: Validate input
        progress.update("Validating input")
        validator = InputValidator()
        validation_result = validator.validate_input(input)
        
        if not validation_result['is_valid']:
            click.echo(f"Error: {validation_result['error']}")
            return
        
        click.echo(f"Processing {validation_result['input_type']}: {input}")
        
        # Determine which file to process
        file_to_process = validation_result.get('temp_file') or validation_result['path']
        
        # Step 2: Extract text and metadata
        progress.update("Extracting text from PDF")
        parser = PDFParser()
        text = parser.extract_text(file_to_process)
        metadata = parser.extract_metadata(file_to_process)
        
        if not text:
            click.echo("Failed to extract text from PDF")
            return
        
        # Clean the extracted text
        cleaned_text = clean_text(text)
        
        click.echo(f"Successfully extracted {len(cleaned_text)} characters from PDF")
        click.echo(f"Document has {metadata['num_pages']} pages")
        
        if analyze:
            # Check if API key is available
            if not config.validate_api_key():
                click.echo("Error: OpenAI API key not found. Set OPENAI_API_KEY environment variable or use --analyze=false for text extraction only.")
                return
            
            # Step 3: Initialize AI agent with prompt configuration
            progress.update("Initializing AI analysis")
            try:
                # Convert prompt version string to enum
                version_map = {
                    'v1_basic': PromptVersion.V1_BASIC,
                    'v2_detailed': PromptVersion.V2_DETAILED,
                    'v3_structured': PromptVersion.V3_STRUCTURED,
                    'experimental': PromptVersion.EXPERIMENTAL
                }
                prompt_ver = version_map.get(prompt_version, PromptVersion.V2_DETAILED)
                
                agent = LiteratureReviewAgent(
                    prompt_version=prompt_ver,
                    custom_config=custom_prompts
                )
                
                if custom_prompts:
                    click.echo(f"Using custom prompt configuration: {custom_prompts}")
                else:
                    click.echo(f"Using prompt version: {prompt_version}")
            except Exception as e:
                click.echo(f"Error initializing AI agent: {e}")
                return
            
            # Step 4: Perform analysis
            progress.update("Analyzing paper with AI")
            try:
                analysis_result = agent.analyze_paper(cleaned_text, metadata)
                click.echo("Analysis completed successfully!")
            except Exception as e:
                click.echo(f"Error during analysis: {e}")
                return
            
            # Format and output results
            formatter = AnalysisFormatter()
            
            if output:
                # Save to file
                if not output.endswith(get_file_extension_from_format(format)):
                    output += get_file_extension_from_format(format)
                
                formatter.save_analysis(analysis_result, output, format)
                click.echo(f"Analysis saved to {output}")
            else:
                # Print to console
                formatter.print_analysis(analysis_result, format)
        
        else:
            # Just extract text without analysis
            if output:
                with open(output, 'w', encoding='utf-8') as f:
                    f.write(cleaned_text)
                click.echo(f"Text saved to {output}")
            else:
                click.echo("\n" + "="*50)
                click.echo("EXTRACTED TEXT")
                click.echo("="*50)
                click.echo(cleaned_text[:1000] + "..." if len(cleaned_text) > 1000 else cleaned_text)
        
        progress.finish()
        
    except KeyboardInterrupt:
        click.echo("\nOperation cancelled by user.")
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        click.echo(f"Error: {e}")
    finally:
        # Clean up temporary files
        if validation_result.get('temp_file'):
            validator.cleanup_temp_file(validation_result['temp_file'])

if __name__ == '__main__':
    main()