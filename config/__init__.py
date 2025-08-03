import os
from typing import Optional
from dotenv import load_dotenv
from pydantic import BaseModel

load_dotenv()

class Config(BaseModel):
    openai_api_key: Optional[str] = None
    max_tokens: int = 4000
    temperature: float = 0.3
    chunk_size: int = 3000
    chunk_overlap: int = 200
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if not self.openai_api_key:
            self.openai_api_key = os.getenv('OPENAI_API_KEY')
    
    def validate_api_key(self) -> bool:
        return self.openai_api_key is not None and len(self.openai_api_key) > 0

config = Config()