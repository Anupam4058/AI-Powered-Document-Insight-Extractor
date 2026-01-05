"""
Configuration and settings for the application
"""
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Base directory
BASE_DIR = Path(__file__).parent

# Upload settings
TEMP_UPLOADS_DIR = BASE_DIR / "temp_uploads"
TEMP_UPLOADS_DIR.mkdir(exist_ok=True)

# File upload settings
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB
ALLOWED_EXTENSIONS = {".pdf", ".docx"}

# AI Model settings
# Model 1: T5-Small for text summarization
T5_MODEL_NAME = os.getenv("T5_MODEL_NAME", "t5-small")
# Model 2: DistilBERT for document classification
DISTILBERT_MODEL_NAME = os.getenv("DISTILBERT_MODEL_NAME", "distilbert-base-uncased")
# Legacy support
MODEL_NAME = os.getenv("MODEL_NAME", DISTILBERT_MODEL_NAME)
DEVICE = os.getenv("DEVICE", "cpu")  # 'cpu' or 'cuda'

# Model cache directory (Hugging Face transformers will cache here by default)
# Default location: ~/.cache/huggingface/transformers
# Can be overridden with HF_HOME environment variable

# API settings
API_HOST = os.getenv("API_HOST", "0.0.0.0")
API_PORT = int(os.getenv("API_PORT", "8000"))

