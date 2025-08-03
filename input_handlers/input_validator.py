import os
import validators
import requests
import tempfile
from urllib.parse import urlparse
from pathlib import Path
from typing import Optional

class InputValidator:
    def __init__(self):
        self.supported_extensions = ['.pdf']
    
    def validate_input(self, input_str: str) -> dict:
        """Validate and classify input as URL or file path"""
        result = {
            'is_valid': False,
            'input_type': None,
            'path': None,
            'error': None,
            'temp_file': None
        }
        
        # Check if it's a URL
        if validators.url(input_str):
            result['input_type'] = 'url'
            result['path'] = input_str
            validation_result = self._validate_and_download_url(input_str)
            result['is_valid'] = validation_result['is_valid']
            result['temp_file'] = validation_result.get('temp_file')
            if not result['is_valid']:
                result['error'] = validation_result.get('error', 'URL is not accessible or not a PDF')
        else:
            # Treat as file path
            result['input_type'] = 'file'
            result['path'] = input_str
            result['is_valid'] = self._validate_file_path(input_str)
            if not result['is_valid']:
                result['error'] = 'File does not exist or is not a PDF'
        
        return result
    
    def _validate_and_download_url(self, url: str) -> dict:
        """Validate URL and download PDF if valid"""
        parsed = urlparse(url)
        if parsed.scheme not in ['http', 'https']:
            return {'is_valid': False, 'error': 'Invalid URL scheme'}
        
        try:
            # Make a HEAD request first to check content type
            head_response = requests.head(url, timeout=10, allow_redirects=True)
            content_type = head_response.headers.get('content-type', '').lower()
            
            # Check if it's a PDF
            if 'application/pdf' not in content_type:
                # Some servers don't set proper content-type, so also check URL extension
                if not url.lower().endswith('.pdf'):
                    return {'is_valid': False, 'error': 'URL does not point to a PDF file'}
            
            # Download the PDF to a temporary file
            response = requests.get(url, timeout=30, stream=True)
            response.raise_for_status()
            
            # Create temporary file
            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.pdf')
            
            # Download in chunks
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    temp_file.write(chunk)
            
            temp_file.close()
            
            # Verify the downloaded file is actually a PDF
            if self._validate_file_path(temp_file.name):
                return {'is_valid': True, 'temp_file': temp_file.name}
            else:
                # Clean up invalid file
                os.unlink(temp_file.name)
                return {'is_valid': False, 'error': 'Downloaded file is not a valid PDF'}
                
        except requests.exceptions.RequestException as e:
            return {'is_valid': False, 'error': f'Error downloading URL: {str(e)}'}
        except Exception as e:
            return {'is_valid': False, 'error': f'Unexpected error: {str(e)}'}
    
    def _validate_file_path(self, file_path: str) -> bool:
        """Validate local file path"""
        path = Path(file_path)
        if not path.exists():
            return False
        
        if path.suffix.lower() not in self.supported_extensions:
            return False
        
        # Basic PDF header check
        try:
            with open(file_path, 'rb') as f:
                header = f.read(4)
                return header == b'%PDF'
        except Exception:
            return False
    
    def cleanup_temp_file(self, temp_file_path: Optional[str]):
        """Clean up temporary file if it exists"""
        if temp_file_path and os.path.exists(temp_file_path):
            try:
                os.unlink(temp_file_path)
            except Exception:
                pass  # Ignore cleanup errors