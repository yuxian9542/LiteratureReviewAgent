#!/usr/bin/env python3
import click
from input_handlers.input_validator import InputValidator
from parsers.pdf_parser import PDFParser

@click.command()
@click.option('--input', '-i', required=True, help='PDF file path or URL')
@click.option('--output', '-o', help='Output file for summary')
def main(input, output):
    """Academic Paper Summarization Agent"""
    
    # Validate input
    validator = InputValidator()
    validation_result = validator.validate_input(input)
    
    if not validation_result['is_valid']:
        click.echo(f"Error: {validation_result['error']}")
        return
    
    click.echo(f"Processing {validation_result['input_type']}: {input}")
    
    # For now, just test PDF parsing with local files
    if validation_result['input_type'] == 'file':
        parser = PDFParser()
        text = parser.extract_text(input)
        metadata = parser.extract_metadata(input)
        
        if text:
            click.echo(f"Successfully extracted {len(text)} characters from PDF")
            click.echo(f"Document has {metadata['num_pages']} pages")
            if output:
                with open(output, 'w') as f:
                    f.write(text)
                click.echo(f"Text saved to {output}")
        else:
            click.echo("Failed to extract text from PDF")
    else:
        click.echo("URL processing not yet implemented")

if __name__ == '__main__':
    main()