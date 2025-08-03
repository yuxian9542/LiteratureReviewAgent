import re
import logging
from typing import List, Dict, Optional
from datetime import datetime

def setup_logging(log_level: str = "INFO") -> logging.Logger:
    """Setup logging configuration"""
    logging.basicConfig(
        level=getattr(logging, log_level.upper()),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler('literature_review.log')
        ]
    )
    return logging.getLogger(__name__)

def clean_text(text: str) -> str:
    """Clean and normalize extracted text"""
    if not text:
        return ""
    
    # Remove excessive whitespace
    text = re.sub(r'\s+', ' ', text)
    
    # Remove page numbers and headers/footers patterns
    text = re.sub(r'\n\s*\d+\s*\n', '\n', text)
    text = re.sub(r'\n\s*Page \d+.*?\n', '\n', text, flags=re.IGNORECASE)
    
    # Remove common PDF artifacts
    text = re.sub(r'[^\x00-\x7F]+', ' ', text)  # Remove non-ASCII characters
    text = re.sub(r'\x0c', '\n', text)  # Replace form feed with newline
    
    # Clean up line breaks
    text = re.sub(r'\n{3,}', '\n\n', text)  # Multiple line breaks to double
    text = re.sub(r'(\w)-\n(\w)', r'\1\2', text)  # Join hyphenated words
    
    return text.strip()

def extract_sections(text: str) -> Dict[str, str]:
    """Extract common paper sections from text"""
    sections = {}
    text_lower = text.lower()
    
    # Common section patterns
    section_patterns = {
        'abstract': [r'abstract\s*\n', r'summary\s*\n'],
        'introduction': [r'introduction\s*\n', r'1\.\s*introduction'],
        'methodology': [r'methodology\s*\n', r'methods\s*\n', r'experimental\s+design'],
        'results': [r'results\s*\n', r'findings\s*\n'],
        'discussion': [r'discussion\s*\n'],
        'conclusion': [r'conclusion\s*\n', r'conclusions\s*\n'],
        'references': [r'references\s*\n', r'bibliography\s*\n']
    }
    
    for section_name, patterns in section_patterns.items():
        for pattern in patterns:
            match = re.search(pattern, text_lower)
            if match:
                start_pos = match.start()
                
                # Find the end of this section (start of next section or end of text)
                next_section_start = len(text)
                for other_section, other_patterns in section_patterns.items():
                    if other_section != section_name:
                        for other_pattern in other_patterns:
                            other_match = re.search(other_pattern, text_lower[start_pos + 100:])
                            if other_match:
                                potential_end = start_pos + 100 + other_match.start()
                                if potential_end < next_section_start:
                                    next_section_start = potential_end
                
                section_text = text[start_pos:next_section_start].strip()
                if len(section_text) > 50:  # Only include substantial sections
                    sections[section_name] = section_text
                break
    
    return sections

def estimate_reading_time(text: str, words_per_minute: int = 250) -> int:
    """Estimate reading time in minutes"""
    word_count = len(text.split())
    return max(1, word_count // words_per_minute)

def extract_keywords(text: str, max_keywords: int = 10) -> List[str]:
    """Extract potential keywords from text (simple implementation)"""
    # Remove common stop words
    stop_words = {
        'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 
        'of', 'with', 'by', 'is', 'are', 'was', 'were', 'be', 'been', 'have',
        'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could', 'should',
        'may', 'might', 'must', 'can', 'this', 'that', 'these', 'those',
        'we', 'they', 'he', 'she', 'it', 'our', 'their', 'his', 'her', 'its'
    }
    
    # Extract words
    words = re.findall(r'\b[a-zA-Z]{3,}\b', text.lower())
    
    # Filter stop words and count frequency
    word_freq = {}
    for word in words:
        if word not in stop_words and len(word) > 3:
            word_freq[word] = word_freq.get(word, 0) + 1
    
    # Get most frequent words
    sorted_words = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)
    return [word for word, freq in sorted_words[:max_keywords]]

def format_file_size(size_bytes: int) -> str:
    """Format file size in human readable format"""
    if size_bytes == 0:
        return "0 B"
    
    size_names = ["B", "KB", "MB", "GB"]
    i = 0
    while size_bytes >= 1024 and i < len(size_names) - 1:
        size_bytes /= 1024
        i += 1
    
    return f"{size_bytes:.1f} {size_names[i]}"

def validate_output_format(output_format: str) -> bool:
    """Validate output format"""
    valid_formats = ['text', 'markdown', 'json']
    return output_format.lower() in valid_formats

def get_file_extension_from_format(output_format: str) -> str:
    """Get appropriate file extension for output format"""
    format_extensions = {
        'text': '.txt',
        'markdown': '.md', 
        'json': '.json'
    }
    return format_extensions.get(output_format.lower(), '.txt')

class ProgressTracker:
    """Simple progress tracker for long operations"""
    
    def __init__(self, total_steps: int, description: str = "Processing"):
        self.total_steps = total_steps
        self.current_step = 0
        self.description = description
        self.start_time = datetime.now()
    
    def update(self, step_description: Optional[str] = None):
        """Update progress"""
        self.current_step += 1
        progress = (self.current_step / self.total_steps) * 100
        
        elapsed = datetime.now() - self.start_time
        
        status = f"{self.description}: {progress:.1f}% ({self.current_step}/{self.total_steps})"
        if step_description:
            status += f" - {step_description}"
        
        print(f"\r{status}", end="", flush=True)
        
        if self.current_step >= self.total_steps:
            print(f"\nCompleted in {elapsed.total_seconds():.1f} seconds")
    
    def finish(self):
        """Mark as finished"""
        if self.current_step < self.total_steps:
            self.current_step = self.total_steps
            elapsed = datetime.now() - self.start_time
            print(f"\nCompleted in {elapsed.total_seconds():.1f} seconds")