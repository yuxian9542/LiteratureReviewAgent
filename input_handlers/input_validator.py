import os
import validators
from urllib.parse import urlparse
from pathlib import Path

class InputValidator:
    def __init__(self):
        self.supported_extensions = ['.pdf']
    
    def validate_input(self, input_str: str) -> dict:
        """Validate and classify input as URL or file path"""
        result = {
            'is_valid': False,
            'input_type': None,
            'path': None,
            'error': None
        }
        
        # Check if it's a URL
        if validators.url(input_str):
            result['input_type'] = 'url'
            result['path'] = input_str
            result['is_valid'] = self._validate_url(input_str)
            if not result['is_valid']:
                result['error'] = 'URL is not accessible or not a PDF'
        else:
            # Treat as file path
            result['input_type'] = 'file'
            result['path'] = input_str
            result['is_valid'] = self._validate_file_path(input_str)
            if not result['is_valid']:
                result['error'] = 'File does not exist or is not a PDF'
        
        return result
    
    def _validate_url(self, url: str) -> bool:
        """Basic URL validation"""
        parsed = urlparse(url)
        return parsed.scheme in ['http', 'https']
    
    def _validate_file_path(self, file_path: str) -> bool:
        """Validate local file path"""
        path = Path(file_path)
        return path.exists() and path.suffix.lower() in self.supported_extensions