"""
Pattern matching utility for extracting structured data from documents

This module uses regex patterns and keyword matching to extract:
- Technical specs (dimensions, formats, file size)
- Deadlines (dates mentioned)
- KPIs (CTR, CPC, conversion rate, etc.)
- Brand guidelines (colors, fonts, tone)
- Action items (what needs to be done)
- Warnings (compliance issues)

No heavy models needed - fast pattern matching only.
"""
import re
from typing import Dict, List, Any, Optional
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class PatternMatcher:
    """Utility class for extracting structured data using pattern matching"""
    
    def __init__(self):
        # Compile regex patterns for better performance
        self._compile_patterns()
    
    def _compile_patterns(self):
        """Compile all regex patterns for reuse"""
        # Dimensions: 1080x1080, 1200x628, 1920x1080, etc.
        self.dimension_pattern = re.compile(
            r'\b(\d{3,5})\s*[x×]\s*(\d{3,5})\b',
            re.IGNORECASE
        )
        
        # File formats: JPG, PNG, PDF, MP4, etc.
        self.format_pattern = re.compile(
            r'\b(?:format|file type|extension):\s*([A-Z0-9]{2,5})\b',
            re.IGNORECASE
        )
        
        # File sizes: 5MB, 10 MB, 2.5MB, etc.
        self.file_size_pattern = re.compile(
            r'\b(\d+(?:\.\d+)?)\s*(MB|KB|GB|mb|kb|gb)\b',
            re.IGNORECASE
        )
        
        # Dates: January 15, 2026, 01/15/2026, 2026-01-15, etc.
        self.date_patterns = [
            re.compile(r'\b(?:January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{1,2},?\s+\d{4}\b', re.IGNORECASE),
            re.compile(r'\b\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b'),
            re.compile(r'\b\d{4}[/-]\d{1,2}[/-]\d{1,2}\b'),
            re.compile(r'\b(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\.?\s+\d{1,2},?\s+\d{4}\b', re.IGNORECASE),
        ]
        
        # Deadline keywords
        self.deadline_keywords = [
            'deadline', 'due by', 'due date', 'submit before', 'submit by',
            'deliver by', 'delivery date', 'must be received by', 'needed by',
            'required by', 'final date', 'cutoff date', 'closing date'
        ]
        
        # KPI patterns: CTR, CPC, CPM, conversion rate, etc.
        self.kpi_patterns = [
            re.compile(r'\b(?:CTR|Click-Through Rate|click through rate):\s*(\d+(?:\.\d+)?)\s*%?\b', re.IGNORECASE),
            re.compile(r'\b(?:CPC|Cost Per Click):\s*\$?(\d+(?:\.\d+)?)\b', re.IGNORECASE),
            re.compile(r'\b(?:CPM|Cost Per Mille|Cost Per Thousand):\s*\$?(\d+(?:\.\d+)?)\b', re.IGNORECASE),
            re.compile(r'\b(?:conversion rate|conversion):\s*(\d+(?:\.\d+)?)\s*%?\b', re.IGNORECASE),
            re.compile(r'\b(?:ROAS|Return on Ad Spend):\s*(\d+(?:\.\d+)?)\b', re.IGNORECASE),
            re.compile(r'\b(?:CPA|Cost Per Acquisition):\s*\$?(\d+(?:\.\d+)?)\b', re.IGNORECASE),
            re.compile(r'\b(?:impressions|impression count):\s*(\d+(?:,\d{3})*(?:\.\d+)?)\b', re.IGNORECASE),
            re.compile(r'\b(?:clicks|click count):\s*(\d+(?:,\d{3})*(?:\.\d+)?)\b', re.IGNORECASE),
        ]
        
        # Color patterns: hex codes, RGB, color names
        self.color_patterns = [
            re.compile(r'\b#([0-9A-Fa-f]{6}|[0-9A-Fa-f]{3})\b'),  # Hex colors
            re.compile(r'\bRGB\((\d+),\s*(\d+),\s*(\d+)\)\b', re.IGNORECASE),
            re.compile(r'\b(?:color|primary color|brand color):\s*([A-Za-z]+(?:\s+[A-Za-z]+)?)\b', re.IGNORECASE),
        ]
        
        # Font patterns
        self.font_patterns = [
            re.compile(r'\b(?:font|typeface|font family):\s*([A-Za-z\s]+(?:,\s*[A-Za-z\s]+)?)\b', re.IGNORECASE),
            re.compile(r'\b(?:font size|font-size|text size):\s*(\d+(?:pt|px)?)\b', re.IGNORECASE),
        ]
        
        # Tone keywords
        self.tone_keywords = [
            'professional', 'casual', 'friendly', 'formal', 'playful', 'serious',
            'energetic', 'calm', 'bold', 'subtle', 'modern', 'traditional',
            'innovative', 'trustworthy', 'luxury', 'affordable'
        ]
        
        # Action item patterns
        self.action_patterns = [
            re.compile(r'\b(?:action|task|todo|to do|must|should|need to|required to):\s*(.+?)(?:\.|$)', re.IGNORECASE),
            re.compile(r'[-•*]\s*(.+?)(?:\.|$)', re.MULTILINE),  # Bullet points
        ]
        
        # Warning/compliance keywords
        self.warning_keywords = [
            'warning', 'compliance', 'must comply', 'required by law',
            'legal requirement', 'regulatory', 'prohibited', 'not allowed',
            'violation', 'penalty', 'fine', 'restriction', 'mandatory'
        ]
    
    def extract_technical_specs(self, text: str) -> Dict[str, Any]:
        """Extract technical specifications from text"""
        specs = {
            'dimensions': [],
            'formats': [],
            'file_sizes': []
        }
        
        # Extract dimensions
        dimension_matches = self.dimension_pattern.findall(text)
        for match in dimension_matches:
            width, height = match
            specs['dimensions'].append(f"{width}x{height}")
        
        # Extract formats
        format_matches = self.format_pattern.findall(text)
        specs['formats'].extend([f.upper() for f in format_matches])
        
        # Also look for common format mentions
        common_formats = ['JPG', 'JPEG', 'PNG', 'PDF', 'MP4', 'MOV', 'GIF', 'SVG', 'WEBP']
        text_upper = text.upper()
        for fmt in common_formats:
            if fmt in text_upper and fmt not in specs['formats']:
                # Check if it's mentioned in context (not just random letters)
                pattern = re.compile(rf'\b{fmt}\b', re.IGNORECASE)
                if pattern.search(text):
                    specs['formats'].append(fmt)
        
        # Extract file sizes
        size_matches = self.file_size_pattern.findall(text)
        for size, unit in size_matches:
            specs['file_sizes'].append(f"{size} {unit.upper()}")
        
        return specs
    
    def extract_deadlines(self, text: str) -> List[Dict[str, str]]:
        """Extract deadlines and dates from text"""
        deadlines = []
        
        # Find all dates
        all_dates = []
        for pattern in self.date_patterns:
            all_dates.extend(pattern.findall(text))
        
        # Find deadline context around dates
        text_lower = text.lower()
        for date_str in all_dates:
            # Check if date is near deadline keywords
            date_index = text.lower().find(date_str.lower())
            if date_index != -1:
                # Look for deadline keywords in surrounding context (100 chars)
                context_start = max(0, date_index - 100)
                context_end = min(len(text), date_index + len(date_str) + 100)
                context = text_lower[context_start:context_end]
                
                is_deadline = any(keyword in context for keyword in self.deadline_keywords)
                
                if is_deadline or len(deadlines) == 0:  # Include first date even without keyword
                    deadlines.append({
                        'date': date_str,
                        'type': 'deadline' if is_deadline else 'mentioned_date',
                        'context': text[max(0, date_index - 50):date_index + len(date_str) + 50].strip()
                    })
        
        return deadlines
    
    def extract_kpis(self, text: str) -> Dict[str, List[float]]:
        """Extract KPIs and metrics from text"""
        kpis = {}
        
        for pattern in self.kpi_patterns:
            matches = pattern.findall(text)
            if matches:
                # Extract KPI name from pattern
                pattern_str = pattern.pattern
                if 'CTR' in pattern_str or 'Click-Through' in pattern_str:
                    kpi_name = 'CTR'
                elif 'CPC' in pattern_str or 'Cost Per Click' in pattern_str:
                    kpi_name = 'CPC'
                elif 'CPM' in pattern_str:
                    kpi_name = 'CPM'
                elif 'conversion' in pattern_str:
                    kpi_name = 'conversion_rate'
                elif 'ROAS' in pattern_str:
                    kpi_name = 'ROAS'
                elif 'CPA' in pattern_str:
                    kpi_name = 'CPA'
                elif 'impressions' in pattern_str:
                    kpi_name = 'impressions'
                elif 'clicks' in pattern_str:
                    kpi_name = 'clicks'
                else:
                    kpi_name = 'unknown'
                
                # Convert to float and store
                values = [float(m.replace(',', '')) for m in matches]
                if kpi_name not in kpis:
                    kpis[kpi_name] = []
                kpis[kpi_name].extend(values)
        
        return kpis
    
    def extract_brand_guidelines(self, text: str) -> Dict[str, Any]:
        """Extract brand guidelines (colors, fonts, tone) from text"""
        guidelines = {
            'colors': [],
            'fonts': [],
            'tone': []
        }
        
        # Extract colors
        # Hex colors
        hex_matches = self.color_patterns[0].findall(text)
        guidelines['colors'].extend([f"#{h}" for h in hex_matches])
        
        # RGB colors
        rgb_matches = self.color_patterns[1].findall(text)
        for r, g, b in rgb_matches:
            guidelines['colors'].append(f"RGB({r}, {g}, {b})")
        
        # Color names
        color_matches = self.color_patterns[2].findall(text)
        guidelines['colors'].extend([c.strip() for c in color_matches if len(c.strip()) < 30])
        
        # Extract fonts
        font_matches = self.font_patterns[0].findall(text)
        guidelines['fonts'].extend([f.strip() for f in font_matches if len(f.strip()) < 50])
        
        font_size_matches = self.font_patterns[1].findall(text)
        if font_size_matches:
            guidelines['fonts'].extend([f"{size}pt" for size in font_size_matches])
        
        # Extract tone
        text_lower = text.lower()
        for tone in self.tone_keywords:
            if tone in text_lower:
                # Check if it's in a brand/tone context
                tone_index = text_lower.find(tone)
                if tone_index != -1:
                    context = text[max(0, tone_index - 30):tone_index + len(tone) + 30].lower()
                    if any(keyword in context for keyword in ['tone', 'voice', 'style', 'brand', 'guideline']):
                        if tone not in guidelines['tone']:
                            guidelines['tone'].append(tone)
        
        return guidelines
    
    def extract_action_items(self, text: str) -> List[str]:
        """Extract action items and tasks from text"""
        action_items = []
        
        # Use action patterns
        for pattern in self.action_patterns:
            matches = pattern.findall(text)
            for match in matches:
                item = match.strip() if isinstance(match, str) else match[0].strip() if match else ""
                if item and len(item) > 10 and len(item) < 200:  # Reasonable length
                    # Clean up the item
                    item = re.sub(r'^\s*[-•*]\s*', '', item)  # Remove leading bullets
                    item = re.sub(r'\s+', ' ', item)  # Normalize whitespace
                    if item not in action_items:
                        action_items.append(item)
        
        return action_items[:20]  # Limit to 20 items
    
    def extract_warnings(self, text: str) -> List[Dict[str, str]]:
        """Extract warnings and compliance issues from text"""
        warnings = []
        
        text_lower = text.lower()
        sentences = re.split(r'[.!?]\s+', text)
        
        for sentence in sentences:
            sentence_lower = sentence.lower()
            # Check if sentence contains warning keywords
            for keyword in self.warning_keywords:
                if keyword in sentence_lower:
                    warnings.append({
                        'type': 'compliance' if 'compliance' in sentence_lower or 'legal' in sentence_lower else 'warning',
                        'text': sentence.strip(),
                        'keyword': keyword
                    })
                    break  # Only add once per sentence
        
        return warnings
    
    def extract_all(self, text: str) -> Dict[str, Any]:
        """Extract all structured data from text"""
        return {
            'technical_specs': self.extract_technical_specs(text),
            'deadlines': self.extract_deadlines(text),
            'kpis': self.extract_kpis(text),
            'brand_guidelines': self.extract_brand_guidelines(text),
            'action_items': self.extract_action_items(text),
            'warnings': self.extract_warnings(text)
        }

