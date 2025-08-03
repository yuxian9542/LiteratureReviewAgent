"""
Prompt templates and configurations for Literature Review Agent
"""
from typing import Dict, Any
from enum import Enum

class PromptVersion(Enum):
    V1_BASIC = "v1_basic"
    V2_DETAILED = "v2_detailed"
    V3_STRUCTURED = "v3_structured"
    EXPERIMENTAL = "experimental"

class PromptTemplates:
    """Centralized prompt template management"""
    
    def __init__(self, version: PromptVersion = PromptVersion.V2_DETAILED):
        self.version = version
        self.templates = self._load_templates()
    
    def _load_templates(self) -> Dict[str, Dict[str, str]]:
        """Load prompt templates based on version"""
        return {
            PromptVersion.V1_BASIC.value: self._get_v1_templates(),
            PromptVersion.V2_DETAILED.value: self._get_v2_templates(),
            PromptVersion.V3_STRUCTURED.value: self._get_v3_templates(),
            PromptVersion.EXPERIMENTAL.value: self._get_experimental_templates(),
        }
    
    def get_prompt(self, task: str, **kwargs) -> str:
        """Get formatted prompt for specific task"""
        template = self.templates[self.version.value].get(task)
        if not template:
            raise ValueError(f"No template found for task: {task}")
        
        return template.format(**kwargs)
    
    def _get_v1_templates(self) -> Dict[str, str]:
        """Basic prompt templates - simple and direct"""
        return {
            "system": "You are an expert academic researcher analyzing scientific papers.",
            
            "summary": """
            Please provide a comprehensive summary of this academic paper excerpt.
            Focus on the main research question, approach, and key findings.
            
            Text: {text}
            """,
            
            "key_findings": """
            Extract the key findings from this academic paper excerpt.
            Return them as a list of bullet points.
            
            Text: {text}
            """,
            
            "methodology": """
            Extract and summarize the methodology used in this research.
            Focus on experimental design and methods.
            
            Text: {text}
            """,
            
            "contributions": """
            Identify the main contributions of this research paper.
            List them as bullet points.
            
            Text: {text}
            """,
            
            "limitations": """
            Identify the limitations of this research.
            List them as bullet points.
            
            Text: {text}
            """
        }
    
    def _get_v2_templates(self) -> Dict[str, str]:
        """Detailed prompt templates - more specific instructions"""
        return {
            "system": "You are an expert academic researcher with deep knowledge in literature analysis. Provide detailed, accurate, and well-structured responses.",
            
            "summary": """
            Analyze this academic paper excerpt and provide a comprehensive summary in 3-4 paragraphs.
            
            Structure your response as follows:
            1. Research context and motivation
            2. Methodology and approach
            3. Key findings and results
            4. Implications and significance
            
            Focus on:
            - Main research question and objectives
            - Novel contributions to the field
            - Practical applications
            - Scientific rigor and validity
            
            Text: {text}
            """,
            
            "key_findings": """
            Extract the key findings from this academic paper excerpt.
            Focus on concrete results, discoveries, and measurable outcomes.
            
            Format as bullet points, each containing:
            - The specific finding
            - Supporting evidence or data when available
            - Statistical significance if mentioned
            
            Avoid:
            - Methodology descriptions
            - Background information
            - Speculation or interpretations
            
            Text: {text}
            """,
            
            "methodology": """
            Extract and summarize the research methodology from this paper.
            
            Include details about:
            - Study design (experimental, observational, etc.)
            - Sample size and participant characteristics
            - Data collection methods and instruments
            - Analysis techniques and statistical methods
            - Controls and variables
            - Timeline and procedures
            
            Present in a clear, structured format that another researcher could understand and potentially replicate.
            
            Text: {text}
            """,
            
            "contributions": """
            Identify the main contributions of this research paper to the scientific field.
            
            Consider:
            - Novel theoretical insights
            - New methodological approaches
            - Empirical discoveries
            - Practical applications
            - Tools, datasets, or frameworks introduced
            - Challenges to existing paradigms
            
            For each contribution, briefly explain why it's significant and how it advances the field.
            
            Text: {text}
            """,
            
            "limitations": """
            Identify the limitations of this research and any suggested future work.
            
            Look for:
            - Acknowledged limitations by the authors
            - Methodological constraints
            - Sample size or scope limitations
            - Generalizability concerns
            - Technical or resource constraints
            - Suggestions for future research directions
            
            Distinguish between explicit limitations mentioned by authors and potential limitations you can infer.
            
            Text: {text}
            """
        }
    
    def _get_v3_templates(self) -> Dict[str, str]:
        """Structured prompt templates - with specific output formats"""
        return {
            "system": """You are an expert academic researcher specializing in literature analysis. 
            Provide responses in the exact format requested, using clear structure and academic language.
            Always base your analysis strictly on the provided text.""",
            
            "summary": """
            Analyze this academic paper excerpt and provide a structured summary.
            
            OUTPUT FORMAT:
            **Research Question**: [1-2 sentences]
            **Methodology**: [2-3 sentences about approach]
            **Key Results**: [2-3 sentences about main findings]
            **Significance**: [1-2 sentences about implications]
            
            REQUIREMENTS:
            - Use only information from the provided text
            - Be concise but comprehensive
            - Use academic language
            - Highlight novel aspects
            
            TEXT TO ANALYZE:
            {text}
            """,
            
            "key_findings": """
            Extract key findings using this exact format:
            
            FINDING 1: [Specific result]
            - Evidence: [Supporting data/observation]
            - Significance: [Why this matters]
            
            FINDING 2: [Specific result]
            - Evidence: [Supporting data/observation]
            - Significance: [Why this matters]
            
            [Continue for all significant findings]
            
            INSTRUCTIONS:
            - Only include findings explicitly stated in the text
            - Focus on quantitative results when available
            - Avoid methodology or background information
            - Maximum 5 findings
            
            TEXT: {text}
            """,
            
            "methodology": """
            Extract methodology information in this structured format:
            
            STUDY DESIGN: [Type of study]
            PARTICIPANTS/SAMPLE: [Who/what was studied]
            DATA COLLECTION: [How data was gathered]
            ANALYSIS METHODS: [Statistical/analytical approaches]
            CONTROLS: [What was controlled for]
            
            Only include information explicitly mentioned in the text.
            If a section is not mentioned, write "Not specified in excerpt"
            
            TEXT: {text}
            """,
            
            "contributions": """
            List contributions using this format:
            
            CONTRIBUTION 1: [Brief title]
            Description: [What was contributed]
            Impact: [How it advances the field]
            
            CONTRIBUTION 2: [Brief title]
            Description: [What was contributed]
            Impact: [How it advances the field]
            
            REQUIREMENTS:
            - Focus on novel contributions only
            - Base on explicit claims in the text
            - Maximum 4 contributions
            - Avoid restating existing knowledge
            
            TEXT: {text}
            """,
            
            "limitations": """
            Extract limitations in this format:
            
            AUTHOR-ACKNOWLEDGED LIMITATIONS:
            • [Limitation 1 as stated by authors]
            • [Limitation 2 as stated by authors]
            
            METHODOLOGICAL CONSTRAINTS:
            • [Constraint 1 from the methodology]
            • [Constraint 2 from the methodology]
            
            FUTURE WORK SUGGESTIONS:
            • [Suggestion 1 for future research]
            • [Suggestion 2 for future research]
            
            Only include items explicitly mentioned in the text.
            If a category has no items, write "None mentioned in excerpt"
            
            TEXT: {text}
            """
        }
    
    def _get_experimental_templates(self) -> Dict[str, str]:
        """Experimental prompt templates - for testing new approaches"""
        return {
            "system": "You are an AI research assistant. Provide detailed analysis with confidence scores.",
            
            "summary": """
            [EXPERIMENTAL PROMPT - Chain of Thought]
            
            Let me analyze this paper step by step:
            
            Step 1: Identify the core research question
            Step 2: Understand the methodology 
            Step 3: Extract key results
            Step 4: Assess significance
            
            Now provide a comprehensive summary addressing each step:
            
            Text: {text}
            """,
            
            "key_findings": """
            [EXPERIMENTAL PROMPT - Confidence Scoring]
            
            Extract findings and rate your confidence in each extraction:
            
            For each finding, provide:
            - Finding: [What was found]
            - Confidence: [High/Medium/Low]
            - Evidence strength: [Strong/Moderate/Weak]
            - Quote: [Relevant text excerpt if available]
            
            Text: {text}
            """,
            
            # Add more experimental templates as needed
        }

# Global instance with default version
default_prompts = PromptTemplates()

# Helper functions for easy access
def get_prompt(task: str, version: PromptVersion = None, **kwargs) -> str:
    """Get a formatted prompt for the specified task"""
    if version:
        templates = PromptTemplates(version)
        return templates.get_prompt(task, **kwargs)
    return default_prompts.get_prompt(task, **kwargs)

def set_default_version(version: PromptVersion):
    """Set the default prompt version globally"""
    global default_prompts
    default_prompts = PromptTemplates(version)