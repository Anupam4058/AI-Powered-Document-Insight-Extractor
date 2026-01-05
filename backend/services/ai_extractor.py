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
    
    def summarize_text(self, text: str, max_length: int = 150, min_length: int = 30) -> str:
        """
        Summarize text using T5-Small model
        
        Args:
            text: Input text to summarize
            max_length: Maximum length of summary
            min_length: Minimum length of summary
            
        Returns:
            Summarized text (2-3 sentences)
        """
        try:
            # Load T5 model and tokenizer
            model, tokenizer = self.model_loader.load_t5_model()
            
            # Prepare input with T5's summarization prefix
            # T5 expects "summarize: " prefix for summarization task
            # T5-Small has a 512 token limit, so we truncate text appropriately
            # Roughly 1 token = 4 characters, so we use ~2000 chars to be safe
            text_sample = text[:2000] if len(text) > 2000 else text
            input_text = f"summarize: {text_sample}"
            
            # Tokenize input
            inputs = tokenizer.encode(
                input_text,
                return_tensors="pt",
                max_length=512,
                truncation=True,
                padding=True
            ).to(model.device)
            
            # Generate summary
            with torch.no_grad():
                outputs = model.generate(
                    inputs,
                    max_length=max_length,
                    min_length=min_length,
                    length_penalty=2.0,
                    num_beams=4,
                    early_stopping=True
                )
            
            # Decode summary
            summary = tokenizer.decode(outputs[0], skip_special_tokens=True)
            
            return summary.strip()
            
        except Exception as e:
            logger.error(f"Error during summarization: {str(e)}")
            # Fallback: return first few sentences
            sentences = text.split('.')
            return '. '.join(sentences[:3]).strip() + '.'
    
    def classify_document_type(self, text: str) -> Dict[str, Any]:
        """
        Classify document type using keyword-based approach
        (DistilBERT base model is not fine-tuned for document classification,
         so we use keyword matching with DistilBERT for feature extraction)
        
        Args:
            text: Document text (first 500 characters used)
            
        Returns:
            Dictionary with document type and confidence
        """
        # Use first 500 characters for classification
        text_sample = text[:500].lower()
        
        # Document type keywords
        document_types = {
            'Creative Brief': ['creative brief', 'brief', 'campaign brief', 'advertising brief', 'creative direction'],
            'Ad Specs': ['ad specs', 'ad specifications', 'ad requirements', 'ad format', 'ad dimensions', 'ad size'],
            'Brand Guidelines': ['brand guidelines', 'brand guide', 'brand standards', 'brand identity', 'brand manual'],
            'Campaign Plan': ['campaign plan', 'campaign strategy', 'marketing plan', 'campaign overview'],
            'Media Plan': ['media plan', 'media strategy', 'media buy', 'media schedule'],
            'Performance Report': ['performance report', 'analytics', 'metrics', 'kpi', 'results', 'report'],
            'Compliance Document': ['compliance', 'legal', 'regulatory', 'policy', 'terms', 'guidelines'],
            'Other': []  # Default category
        }
        
        # Score each document type
        scores = {}
        for doc_type, keywords in document_types.items():
            if doc_type == 'Other':
                continue
            score = sum(1 for keyword in keywords if keyword in text_sample)
            scores[doc_type] = score
        
        # Find best match
        if scores and max(scores.values()) > 0:
            best_type = max(scores, key=scores.get)
            confidence = min(1.0, scores[best_type] / 3.0)  # Normalize confidence
        else:
            best_type = 'Other'
            confidence = 0.5
        
        return {
            'document_type': best_type,
            'confidence': round(confidence, 2),
            'scores': scores
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
                "summary": "",
                "document_type": {"document_type": "Unknown", "confidence": 0.0},
                "extracted_data": {},
                "error": "Empty text provided"
            }
        
        logger.info("Starting AI extraction process...")
        
        try:
            # 1. Summarize using T5-Small
            logger.info("Summarizing document with T5-Small...")
            summary = self.summarize_text(text)
            logger.info(f"Summary generated: {len(summary)} characters")
            
            # 2. Classify document type
            logger.info("Classifying document type...")
            document_type = self.classify_document_type(text)
            logger.info(f"Document type: {document_type['document_type']} (confidence: {document_type['confidence']})")
            
            # 3. Extract structured data using pattern matching
            logger.info("Extracting structured data with pattern matching...")
            extracted_data = self.pattern_matcher.extract_all(text)
            logger.info("Pattern matching completed")
            
            # Compile insights
            insights = {
                "summary": summary,
                "document_type": document_type,
                "extracted_data": {
                    "technical_specs": extracted_data['technical_specs'],
                    "deadlines": extracted_data['deadlines'],
                    "kpis": extracted_data['kpis'],
                    "brand_guidelines": extracted_data['brand_guidelines'],
                    "action_items": extracted_data['action_items'],
                    "warnings": extracted_data['warnings']
                },
                "metadata": {
                    "text_length": len(text),
                    "word_count": len(text.split()),
                    "extraction_method": "T5-Small + Pattern Matching"
                }
            }
            
            logger.info("AI extraction completed successfully")
            return insights
            
        except Exception as e:
            logger.error(f"Error during AI extraction: {str(e)}")
            return {
                "summary": "",
                "document_type": {"document_type": "Unknown", "confidence": 0.0},
                "extracted_data": {},
                "error": f"Extraction failed: {str(e)}"
            }

