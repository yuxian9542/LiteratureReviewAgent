import json
from typing import Dict, List
from datetime import datetime

class AnalysisFormatter:
    """Format and output analysis results in various formats"""
    
    def __init__(self):
        pass
    
    def format_analysis(self, analysis: Dict, output_format: str = "text") -> str:
        """Format analysis results in specified format"""
        if output_format.lower() == "json":
            return self._format_json(analysis)
        elif output_format.lower() == "markdown":
            return self._format_markdown(analysis)
        else:
            return self._format_text(analysis)
    
    def _format_text(self, analysis: Dict) -> str:
        """Format analysis as plain text"""
        output = []
        output.append("=" * 60)
        output.append("LITERATURE REVIEW ANALYSIS")
        output.append("=" * 60)
        output.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        output.append("")
        
        # Metadata
        if 'metadata' in analysis:
            metadata = analysis['metadata']
            output.append("DOCUMENT METADATA:")
            output.append("-" * 20)
            output.append(f"Pages: {metadata.get('num_pages', 'Unknown')}")
            if metadata.get('metadata'):
                for key, value in metadata['metadata'].items():
                    output.append(f"{key}: {value}")
            output.append("")
        
        # Summary
        if 'summary' in analysis:
            output.append("SUMMARY:")
            output.append("-" * 20)
            output.append(analysis['summary'])
            output.append("")
        
        # Key Findings
        if 'key_findings' in analysis:
            output.append("KEY FINDINGS:")
            output.append("-" * 20)
            findings = analysis['key_findings']
            if isinstance(findings, list):
                for i, finding in enumerate(findings, 1):
                    output.append(f"{i}. {finding}")
            else:
                output.append(findings)
            output.append("")
        
        # Methodology
        if 'methodology' in analysis:
            output.append("METHODOLOGY:")
            output.append("-" * 20)
            output.append(analysis['methodology'])
            output.append("")
        
        # Contributions
        if 'contributions' in analysis:
            output.append("MAIN CONTRIBUTIONS:")
            output.append("-" * 20)
            contributions = analysis['contributions']
            if isinstance(contributions, list):
                for i, contribution in enumerate(contributions, 1):
                    output.append(f"{i}. {contribution}")
            else:
                output.append(contributions)
            output.append("")
        
        # Limitations
        if 'limitations' in analysis:
            output.append("LIMITATIONS & FUTURE WORK:")
            output.append("-" * 20)
            limitations = analysis['limitations']
            if isinstance(limitations, list):
                for i, limitation in enumerate(limitations, 1):
                    output.append(f"{i}. {limitation}")
            else:
                output.append(limitations)
            output.append("")
        
        return "\n".join(output)
    
    def _format_markdown(self, analysis: Dict) -> str:
        """Format analysis as Markdown"""
        output = []
        output.append("# Literature Review Analysis")
        output.append(f"*Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*")
        output.append("")
        
        # Metadata
        if 'metadata' in analysis:
            metadata = analysis['metadata']
            output.append("## Document Metadata")
            output.append(f"- **Pages:** {metadata.get('num_pages', 'Unknown')}")
            if metadata.get('metadata'):
                for key, value in metadata['metadata'].items():
                    output.append(f"- **{key}:** {value}")
            output.append("")
        
        # Summary
        if 'summary' in analysis:
            output.append("## Summary")
            output.append(analysis['summary'])
            output.append("")
        
        # Key Findings
        if 'key_findings' in analysis:
            output.append("## Key Findings")
            findings = analysis['key_findings']
            if isinstance(findings, list):
                for finding in findings:
                    output.append(f"- {finding}")
            else:
                output.append(findings)
            output.append("")
        
        # Methodology
        if 'methodology' in analysis:
            output.append("## Methodology")
            output.append(analysis['methodology'])
            output.append("")
        
        # Contributions
        if 'contributions' in analysis:
            output.append("## Main Contributions")
            contributions = analysis['contributions']
            if isinstance(contributions, list):
                for contribution in contributions:
                    output.append(f"- {contribution}")
            else:
                output.append(contributions)
            output.append("")
        
        # Limitations
        if 'limitations' in analysis:
            output.append("## Limitations & Future Work")
            limitations = analysis['limitations']
            if isinstance(limitations, list):
                for limitation in limitations:
                    output.append(f"- {limitation}")
            else:
                output.append(limitations)
            output.append("")
        
        return "\n".join(output)
    
    def _format_json(self, analysis: Dict) -> str:
        """Format analysis as JSON"""
        # Add timestamp
        analysis_with_timestamp = {
            "timestamp": datetime.now().isoformat(),
            **analysis
        }
        return json.dumps(analysis_with_timestamp, indent=2, ensure_ascii=False)
    
    def save_analysis(self, analysis: Dict, filepath: str, output_format: str = "text"):
        """Save analysis to file"""
        formatted_content = self.format_analysis(analysis, output_format)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(formatted_content)
    
    def print_analysis(self, analysis: Dict, output_format: str = "text"):
        """Print analysis to console"""
        formatted_content = self.format_analysis(analysis, output_format)
        print(formatted_content)