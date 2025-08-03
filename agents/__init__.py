from typing import Dict, List, Optional
from openai import OpenAI
from langchain.text_splitter import RecursiveCharacterTextSplitter
from config import config
from prompts import get_prompt, PromptVersion
from prompts.config import prompt_config

class LiteratureReviewAgent:
    def __init__(self, prompt_version: PromptVersion = PromptVersion.V2_DETAILED, custom_config: Optional[str] = None):
        if not config.validate_api_key():
            raise ValueError("OpenAI API key not found. Please set OPENAI_API_KEY environment variable.")
        
        self.client = OpenAI(api_key=config.openai_api_key)
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=config.chunk_size,
            chunk_overlap=config.chunk_overlap,
            separators=["\n\n", "\n", ". ", " ", ""]
        )
        self.prompt_version = prompt_version
        self.custom_config = custom_config
    
    def analyze_paper(self, text: str, metadata: Dict) -> Dict:
        """Analyze academic paper and extract key information"""
        
        # Split text into manageable chunks
        chunks = self.text_splitter.split_text(text)
        
        # Extract different aspects of the paper
        analysis = {
            'summary': self._generate_summary(chunks),
            'key_findings': self._extract_key_findings(chunks),
            'methodology': self._extract_methodology(chunks),
            'contributions': self._extract_contributions(chunks),
            'limitations': self._extract_limitations(chunks),
            'metadata': metadata
        }
        
        return analysis
    
    def _generate_summary(self, chunks: List[str]) -> str:
        """Generate a comprehensive summary of the paper"""
        # Use first few chunks for summary (usually abstract and introduction)
        summary_text = " ".join(chunks[:3])
        
        prompt = self._get_prompt("summary", text=summary_text)
        return self._call_openai(prompt)
    
    def _extract_key_findings(self, chunks: List[str]) -> List[str]:
        """Extract key findings from the paper"""
        # Focus on results and conclusion sections
        relevant_chunks = chunks[-3:] if len(chunks) > 3 else chunks
        combined_text = " ".join(relevant_chunks)
        
        prompt = self._get_prompt("key_findings", text=combined_text)
        response = self._call_openai(prompt)
        return self._parse_bullet_points(response)
    
    def _extract_methodology(self, chunks: List[str]) -> str:
        """Extract methodology information"""
        # Look for methodology in middle chunks
        method_chunks = chunks[1:-1] if len(chunks) > 2 else chunks
        combined_text = " ".join(method_chunks)
        
        prompt = self._get_prompt("methodology", text=combined_text)
        return self._call_openai(prompt)
    
    def _extract_contributions(self, chunks: List[str]) -> List[str]:
        """Extract main contributions of the paper"""
        # Use all chunks but focus on abstract and conclusion
        key_chunks = [chunks[0]] + chunks[-2:] if len(chunks) > 2 else chunks
        combined_text = " ".join(key_chunks)
        
        prompt = self._get_prompt("contributions", text=combined_text)
        response = self._call_openai(prompt)
        return self._parse_bullet_points(response)
    
    def _extract_limitations(self, chunks: List[str]) -> List[str]:
        """Extract limitations and future work suggestions"""
        # Focus on conclusion and discussion sections
        conclusion_chunks = chunks[-2:] if len(chunks) > 1 else chunks
        combined_text = " ".join(conclusion_chunks)
        
        prompt = self._get_prompt("limitations", text=combined_text)
        response = self._call_openai(prompt)
        return self._parse_bullet_points(response)
    
    def _get_prompt(self, task: str, **kwargs) -> str:
        """Get prompt for a specific task using current configuration"""
        try:
            if self.custom_config:
                return prompt_config.get_custom_prompt(self.custom_config, task, **kwargs)
            else:
                return get_prompt(task, self.prompt_version, **kwargs)
        except Exception as e:
            # Fallback to basic prompt if configuration fails
            return f"Analyze this text for {task}: {kwargs.get('text', '')}"
    
    def _call_openai(self, prompt: str) -> str:
        """Make API call to OpenAI"""
        try:
            system_prompt = self._get_system_prompt()
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=config.max_tokens,
                temperature=config.temperature
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            return f"Error in API call: {str(e)}"
    
    def _get_system_prompt(self) -> str:
        """Get system prompt based on current configuration"""
        try:
            if self.custom_config:
                return prompt_config.get_custom_prompt(self.custom_config, "system")
            else:
                return get_prompt("system", self.prompt_version)
        except Exception:
            return "You are an expert academic researcher analyzing scientific papers."
    
    def _parse_bullet_points(self, text: str) -> List[str]:
        """Parse bullet points from AI response"""
        lines = text.split('\n')
        bullet_points = []
        
        for line in lines:
            line = line.strip()
            if line.startswith(('"', '-', '*', '1.', '2.', '3.', '4.', '5.')):
                # Remove bullet point markers
                cleaned = line.lstrip('"-* ').lstrip('123456789. ')
                if cleaned:
                    bullet_points.append(cleaned)
        
        return bullet_points if bullet_points else [text]