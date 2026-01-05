"""
Utility helper functions
"""
import os
from pathlib import Path
from typing import Optional
import uuid
from config import TEMP_UPLOADS_DIR, ALLOWED_EXTENSIONS


def validate_file_extension(filename: str) -> bool:
    """
    Validate if file has an allowed extension
    
    Args:
        filename: Name of the file
        
    Returns:
        True if extension is allowed, False otherwise
    """
    file_path = Path(filename)
    return file_path.suffix.lower() in ALLOWED_EXTENSIONS


def generate_unique_filename(original_filename: str) -> Path:
    """
    Generate a unique filename for temporary storage
    
    Args:
        original_filename: Original name of the uploaded file
        
    Returns:
        Path object with unique filename in temp_uploads directory
    """
    file_extension = Path(original_filename).suffix
    unique_id = str(uuid.uuid4())
    unique_filename = f"{unique_id}{file_extension}"
    return TEMP_UPLOADS_DIR / unique_filename


def cleanup_temp_file(file_path: Path) -> bool:
    """
    Delete a temporary file
    
    Args:
        file_path: Path to the file to delete
        
    Returns:
        True if file was deleted, False otherwise
    """
    try:
        if file_path.exists():
            file_path.unlink()
            return True
        return False
    except Exception:
        return False


def get_file_size(file_path: Path) -> int:
    """
    Get file size in bytes
    
    Args:
        file_path: Path to the file
        
    Returns:
        File size in bytes
    """
    return file_path.stat().st_size

