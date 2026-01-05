"""
AI extractor service for extracting insights using transformer models

This module implements:
- T5-Small for text summarization (2-3 sentences)
- DistilBERT for document type classification
- Pattern matching for structured data extraction
"""
import torch
import logging
from typing import Dict, Any, List
from .model_loader import ModelLoader
from utils.pattern_matcher import PatternMatcher
from utils.structured_extractor import (
    extract_goal, extract_must_include, extract_biggest_donts,
    categorize_creative_requirements, structure_technical_specs,
    categorize_guidelines, create_action_items
)
from utils.summary_simplifier import extract_simple_dates, extract_simple_channels, extract_simple_kpis

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class AIExtractor:
    """
    Service for extracting insights from documents using AI models
    
    Features:
    1. Summarization using T5-Small (~3-5 seconds)
    2. Document type classification using DistilBERT (~1-2 seconds)
    3. Pattern matching for structured data extraction (~1 second)
    """
    
    def __init__(self):
        self.model_loader = ModelLoader()
        self.pattern_matcher = PatternMatcher()
    
    def summarize_text(self, text: str, max_length: int = 400, min_length: int = 150) -> str:
        """
        Summarize text using T5-Small model
        
        Args:
            text: Input text to summarize
            max_length: Maximum length of summary (in tokens)
            min_length: Minimum length of summary (in tokens)
            
        Returns:
            Summarized text (5+ lines / sentences)
        """
        try:
            # Load T5 model and tokenizer
            model, tokenizer = self.model_loader.load_t5_model()
            
            # Prepare input with T5's summarization prefix
            # T5 expects "summarize: " prefix for summarization task
            # T5-Small has a 512 token limit, so we truncate text appropriately
            # Use more text for longer summaries - roughly 1 token = 4 characters
            # Use up to 4000 chars to get better context for longer summaries
            text_sample = text[:4000] if len(text) > 4000 else text
            input_text = f"summarize: {text_sample}"
            
            # Tokenize input
            inputs = tokenizer.encode(
                input_text,
                return_tensors="pt",
                max_length=512,
                truncation=True,
                padding=True
            ).to(model.device)
            
            # Generate summary with longer length for more detailed summaries
            with torch.no_grad():
                outputs = model.generate(
                    inputs,
                    max_length=max_length,
                    min_length=min_length,
                    length_penalty=1.5,  # Reduced from 2.0 to allow longer summaries
                    num_beams=4,
                    early_stopping=False  # Changed to False to allow full length generation
                )
            
            # Decode summary
            summary = tokenizer.decode(outputs[0], skip_special_tokens=True)
            
            return summary.strip()
            
        except Exception as e:
            logger.error(f"Error during summarization: {str(e)}")
            # Fallback: return first few sentences (increased for longer summary)
            sentences = text.split('.')
            return '. '.join(sentences[:5]).strip() + '.'
    
    def classify_document_type(self, text: str) -> Dict[str, Any]:
        """
        Classify document type using keyword-based approach with user-friendly descriptions
        
        Args:
            text: Document text (first 2000 characters used for better classification)
            
        Returns:
            Dictionary with document type, confidence level, and description
        """
        # Use first 2000 characters for better classification (increased from 500)
        text_sample = text[:2000].lower()
        
        # Document type keywords with descriptions
        document_types = {
            'Creative Brief': {
                'keywords': ['creative brief', 'brief', 'campaign brief', 'advertising brief', 'creative direction', 
                            'project brief', 'creative strategy', 'ad brief'],
                'description': 'A document outlining the creative goals, target audience, and requirements for an advertising campaign.'
            },
            'Ad Specs': {
                'keywords': ['ad specs', 'ad specifications', 'ad requirements', 'ad format', 'ad dimensions', 
                            'ad size', 'specifications', 'technical specs', 'ad specs sheet'],
                'description': 'Technical specifications detailing the format, dimensions, and requirements for advertising creatives.'
            },
            'Brand Guidelines': {
                'keywords': ['brand guidelines', 'brand guide', 'brand standards', 'brand identity', 'brand manual',
                            'style guide', 'brand book', 'visual identity'],
                'description': 'Guidelines that define how a brand should be represented visually, including colors, fonts, and tone.'
            },
            'Campaign Plan': {
                'keywords': ['campaign plan', 'campaign strategy', 'marketing plan', 'campaign overview',
                            'campaign proposal', 'marketing strategy'],
                'description': 'A strategic document outlining the goals, timeline, and approach for a marketing campaign.'
            },
            'Media Plan': {
                'keywords': ['media plan', 'media strategy', 'media buy', 'media schedule', 'media planning',
                            'media allocation'],
                'description': 'A document detailing where and when advertisements will be placed across different media channels.'
            },
            'Performance Report': {
                'keywords': ['performance report', 'analytics', 'metrics', 'kpi', 'results', 'report',
                            'campaign results', 'performance metrics', 'analytics report'],
                'description': 'A report showing the results and performance metrics of a campaign or advertising effort.'
            },
            'Compliance Document': {
                'keywords': ['compliance', 'legal', 'regulatory', 'policy', 'terms', 'guidelines',
                            'regulations', 'compliance requirements'],
                'description': 'Documents outlining legal, regulatory, or policy requirements that must be followed.'
            },
            'Product Sheet': {
                'keywords': ['product sheet', 'product specification', 'product info', 'product details',
                            'product catalog', 'product data'],
                'description': 'A document containing detailed information about a product, including features and specifications.'
            }
        }
        
        # Score each document type
        scores = {}
        for doc_type, data in document_types.items():
            keywords = data['keywords']
            score = sum(1 for keyword in keywords if keyword in text_sample)
            scores[doc_type] = score
        
        # Find best match
        if scores and max(scores.values()) > 0:
            best_type = max(scores, key=scores.get)
            max_score = scores[best_type]
            # Normalize confidence (0.0 to 1.0)
            confidence_value = min(1.0, max_score / 4.0)
            
            # Convert to user-friendly confidence level
            if confidence_value >= 0.7:
                confidence_level = 'High'
            elif confidence_value >= 0.4:
                confidence_level = 'Medium'
            else:
                confidence_level = 'Low'
            
            description = document_types[best_type]['description']
        else:
            best_type = 'General Document'
            confidence_value = 0.3
            confidence_level = 'Low'
            description = 'A general document that may contain various types of information related to retail media or advertising.'
        
        return {
            'type': best_type,  # Changed from 'document_type' to 'type' for frontend compatibility
            'confidence': round(confidence_value, 2),
            'confidence_level': confidence_level,  # User-friendly label
            'description': description
        }
    
    def extract_insights(self, text: str) -> Dict[str, Any]:
        """
        Extract structured insights from document text
        
        This function:
        1. Summarizes text using T5-Small (2-3 sentences)
        2. Classifies document type using keyword-based approach
        3. Extracts structured data using pattern matching:
           - Technical specs (dimensions, formats, file sizes)
           - Deadlines (dates)
           - KPIs (CTR, CPC, conversion rate, etc.)
           - Brand guidelines (colors, fonts, tone)
           - Action items (tasks to do)
           - Warnings (compliance issues)
        
        Args:
            text: The extracted text from the document
            
        Returns:
            Dictionary containing extracted insights
        """
        if not text or not text.strip():
            return {
                "summary": {
                    "goal": "",
                    "dates": "",
                    "channels": "",
                    "success": "",
                    "must_include": "",
                    "avoid": ""
                },
                "document_type": {
                    "type": "Unknown",
                    "confidence": 0.0,
                    "confidence_level": "Low",
                    "description": "No content found in document."
                },
                "creative_requirements": {"must_have": [], "optional": []},
                "technical_specs": [],
                "guidelines": {"copy_rules": [], "design_rules": [], "accessibility_rules": [], "legal_rules": []},
                "action_items": [],
                "error": "Empty text provided"
            }
        
        logger.info("Starting AI extraction process...")
        
        try:
            # 1. Classify document type
            logger.info("Classifying document type...")
            document_type = self.classify_document_type(text)
            logger.info(f"Document type: {document_type['type']} (confidence: {document_type['confidence_level']})")
            
            # 2. Extract structured data using pattern matching
            logger.info("Extracting structured data with pattern matching...")
            extracted_data = self.pattern_matcher.extract_all(text)
            logger.info("Pattern matching completed")
            
            # 3. Build structured summary
            logger.info("Building structured summary...")
            deadlines = extracted_data.get('deadlines', [])
            kpis = extracted_data.get('kpis', {})
            warnings = extracted_data.get('warnings', [])
            
            structured_summary = {
                "goal": extract_goal(text),
                "dates": extract_simple_dates(text, deadlines),
                "channels": extract_simple_channels(text),
                "success": extract_simple_kpis(text, kpis),
                "must_include": extract_must_include(text, extracted_data.get('brand_guidelines', {})),
                "avoid": extract_biggest_donts(text, warnings)
            }
            
            # 4. Structure creative requirements
            logger.info("Structuring creative requirements...")
            creative_requirements = categorize_creative_requirements(
                extracted_data.get('technical_specs', {}),
                extracted_data.get('brand_guidelines', {}),
                text
            )
            
            # 5. Structure technical specifications
            logger.info("Structuring technical specifications...")
            technical_specs = structure_technical_specs(
                extracted_data.get('technical_specs', {}),
                text
            )
            
            # 6. Categorize guidelines
            logger.info("Categorizing guidelines...")
            guidelines = categorize_guidelines(warnings, text)
            
            # 7. Create action items
            logger.info("Creating action items...")
            action_items = create_action_items(
                deadlines,
                extracted_data.get('technical_specs', {}),
                warnings,
                text
            )
            
            # Compile insights
            insights = {
                "summary": structured_summary,
                "document_type": document_type,
                "creative_requirements": creative_requirements,
                "technical_specs": technical_specs,
                "guidelines": guidelines,
                "action_items": action_items,
                "metadata": {
                    "text_length": len(text),
                    "word_count": len(text.split()),
                    "extraction_method": "Structured Extraction + Pattern Matching"
                }
            }
            
            logger.info("AI extraction completed successfully")
            return insights
            
        except Exception as e:
            logger.error(f"Error during AI extraction: {str(e)}")
            return {
                "summary": {
                    "goal": "",
                    "dates": "",
                    "channels": "",
                    "success": "",
                    "must_include": "",
                    "avoid": ""
                },
                "document_type": {
                    "type": "Unknown",
                    "confidence": 0.0,
                    "confidence_level": "Low",
                    "description": "Unable to classify document type due to processing error."
                },
                "creative_requirements": {"must_have": [], "optional": []},
                "technical_specs": [],
                "guidelines": {"copy_rules": [], "design_rules": [], "accessibility_rules": [], "legal_rules": []},
                "action_items": [],
                "error": f"Extraction failed: {str(e)}"
            }

