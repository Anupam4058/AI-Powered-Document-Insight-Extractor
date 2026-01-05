"""
Model loader service for loading and managing transformer models

This module handles:
- T5-Small model for text summarization
- DistilBERT model for document classification
- Automatic model downloading from Hugging Face on first run
- Local model caching (handled by Hugging Face transformers library)
- Error handling for download failures
"""
from transformers import (
    AutoTokenizer, 
    AutoModelForSequenceClassification,
    T5ForConditionalGeneration,
    T5Tokenizer
)
import torch
import logging
from typing import Tuple, Optional
from config import T5_MODEL_NAME, DISTILBERT_MODEL_NAME, DEVICE

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ModelLoader:
    """
    Singleton class to manage model loading and caching
    
    Handles two models:
    1. T5-Small: For text summarization (242 MB)
    2. DistilBERT: For document classification (268 MB)
    
    Models are automatically downloaded from Hugging Face on first use
    and cached locally in ~/.cache/huggingface/transformers
    """
    
    _instance = None
    _t5_tokenizer: Optional[T5Tokenizer] = None
    _t5_model: Optional[T5ForConditionalGeneration] = None
    _distilbert_tokenizer: Optional[AutoTokenizer] = None
    _distilbert_model: Optional[AutoModelForSequenceClassification] = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ModelLoader, cls).__new__(cls)
        return cls._instance
    
    def load_t5_model(self) -> Tuple[T5ForConditionalGeneration, T5Tokenizer]:
        """
        Load T5-Small model for text summarization
        
        Model Details:
        - Purpose: Summarize long documents to 2-3 sentences
        - Size: 242 MB (lightweight)
        - Speed: ~3-5 seconds per document
        - Input format: "summarize: [document text]"
        - Output: Summary string
        
        Returns:
            Tuple of (model, tokenizer)
            
        Raises:
            Exception: If model download or loading fails
        """
        if self._t5_model is None or self._t5_tokenizer is None:
            try:
                logger.info(f"Loading T5-Small model ({T5_MODEL_NAME})...")
                logger.info("First-time use: Model will be downloaded from Hugging Face (~5 min)")
                
                # Load tokenizer and model
                # Auto-downloads from Hugging Face if not cached locally
                # Caches in ~/.cache/huggingface/transformers by default
                self._t5_tokenizer = T5Tokenizer.from_pretrained(
                    T5_MODEL_NAME,
                    cache_dir=None  # Uses default Hugging Face cache directory
                )
                self._t5_model = T5ForConditionalGeneration.from_pretrained(
                    T5_MODEL_NAME,
                    cache_dir=None  # Uses default Hugging Face cache directory
                )
                
                # Move model to device (CPU or CUDA)
                self._t5_model.to(DEVICE)
                self._t5_model.eval()  # Set to evaluation mode
                
                logger.info(f"T5-Small model loaded successfully on {DEVICE}")
                
            except ConnectionError as e:
                error_msg = (
                    f"Failed to download T5-Small model: {str(e)}\n"
                    "Please check your internet connection and try again."
                )
                logger.error(error_msg)
                raise Exception(error_msg)
            except Exception as e:
                error_msg = f"Error loading T5-Small model: {str(e)}"
                logger.error(error_msg)
                raise Exception(error_msg)
        
        return self._t5_model, self._t5_tokenizer
    
    def load_distilbert_model(self) -> Tuple[AutoModelForSequenceClassification, AutoTokenizer]:
        """
        Load DistilBERT model for document classification
        
        Model Details:
        - Purpose: Detect document type (Creative Brief, Ad Specs, etc.)
        - Size: 268 MB (lightweight)
        - Speed: ~1-2 seconds per document
        - Input: First 500 characters of document
        - Output: Document type + confidence score
        
        Returns:
            Tuple of (model, tokenizer)
            
        Raises:
            Exception: If model download or loading fails
        """
        if self._distilbert_model is None or self._distilbert_tokenizer is None:
            try:
                logger.info(f"Loading DistilBERT model ({DISTILBERT_MODEL_NAME})...")
                logger.info("First-time use: Model will be downloaded from Hugging Face (~5 min)")
                
                # Load tokenizer and model
                # Auto-downloads from Hugging Face if not cached locally
                # Caches in ~/.cache/huggingface/transformers by default
                self._distilbert_tokenizer = AutoTokenizer.from_pretrained(
                    DISTILBERT_MODEL_NAME,
                    cache_dir=None  # Uses default Hugging Face cache directory
                )
                self._distilbert_model = AutoModelForSequenceClassification.from_pretrained(
                    DISTILBERT_MODEL_NAME,
                    cache_dir=None  # Uses default Hugging Face cache directory
                )
                
                # Move model to device (CPU or CUDA)
                self._distilbert_model.to(DEVICE)
                self._distilbert_model.eval()  # Set to evaluation mode
                
                logger.info(f"DistilBERT model loaded successfully on {DEVICE}")
                
            except ConnectionError as e:
                error_msg = (
                    f"Failed to download DistilBERT model: {str(e)}\n"
                    "Please check your internet connection and try again."
                )
                logger.error(error_msg)
                raise Exception(error_msg)
            except Exception as e:
                error_msg = f"Error loading DistilBERT model: {str(e)}"
                logger.error(error_msg)
                raise Exception(error_msg)
        
        return self._distilbert_model, self._distilbert_tokenizer
    
    def get_t5_model(self) -> T5ForConditionalGeneration:
        """Get the loaded T5-Small model (lazy loading)"""
        if self._t5_model is None:
            self.load_t5_model()
        return self._t5_model
    
    def get_t5_tokenizer(self) -> T5Tokenizer:
        """Get the loaded T5-Small tokenizer (lazy loading)"""
        if self._t5_tokenizer is None:
            self.load_t5_model()
        return self._t5_tokenizer
    
    def get_distilbert_model(self) -> AutoModelForSequenceClassification:
        """Get the loaded DistilBERT model (lazy loading)"""
        if self._distilbert_model is None:
            self.load_distilbert_model()
        return self._distilbert_model
    
    def get_distilbert_tokenizer(self) -> AutoTokenizer:
        """Get the loaded DistilBERT tokenizer (lazy loading)"""
        if self._distilbert_tokenizer is None:
            self.load_distilbert_model()
        return self._distilbert_tokenizer
    
    # Legacy methods for backward compatibility
    def load_model(self):
        """
        Legacy method: Load DistilBERT model (for backward compatibility)
        """
        return self.load_distilbert_model()
    
    def get_model(self):
        """Legacy method: Get DistilBERT model (for backward compatibility)"""
        return self.get_distilbert_model()
    
    def get_tokenizer(self):
        """Legacy method: Get DistilBERT tokenizer (for backward compatibility)"""
        return self.get_distilbert_tokenizer()

