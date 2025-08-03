"""
Prompt configuration loader and manager
"""
import yaml
import json
import os
from typing import Dict, Any, Optional
from pathlib import Path

class PromptConfig:
    """Load and manage prompt configurations from files"""
    
    def __init__(self, config_dir: Optional[str] = None):
        self.config_dir = Path(config_dir) if config_dir else Path(__file__).parent
        self.custom_prompts = self._load_custom_prompts()
    
    def _load_custom_prompts(self) -> Dict[str, Any]:
        """Load custom prompts from YAML/JSON files"""
        prompts = {}
        
        # Load YAML files
        yaml_files = self.config_dir.glob("*.yaml")
        for yaml_file in yaml_files:
            try:
                with open(yaml_file, 'r', encoding='utf-8') as f:
                    data = yaml.safe_load(f)
                    prompts.update(data)
            except Exception as e:
                print(f"Warning: Could not load {yaml_file}: {e}")
        
        # Load JSON files
        json_files = self.config_dir.glob("*.json")
        for json_file in json_files:
            try:
                with open(json_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    prompts.update(data)
            except Exception as e:
                print(f"Warning: Could not load {json_file}: {e}")
        
        return prompts
    
    def get_custom_prompt(self, config_name: str, task: str, **kwargs) -> str:
        """Get a custom prompt from configuration files"""
        if config_name not in self.custom_prompts:
            raise ValueError(f"Configuration '{config_name}' not found")
        
        config = self.custom_prompts[config_name]
        if task not in config:
            raise ValueError(f"Task '{task}' not found in configuration '{config_name}'")
        
        template = config[task]
        return template.format(**kwargs)
    
    def list_configurations(self) -> list:
        """List available prompt configurations"""
        return list(self.custom_prompts.keys())
    
    def list_tasks(self, config_name: str) -> list:
        """List available tasks for a configuration"""
        if config_name not in self.custom_prompts:
            return []
        return list(self.custom_prompts[config_name].keys())
    
    def reload(self):
        """Reload prompt configurations from files"""
        self.custom_prompts = self._load_custom_prompts()

# Global instance
prompt_config = PromptConfig()