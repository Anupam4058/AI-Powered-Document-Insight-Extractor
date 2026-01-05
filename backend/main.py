"""
FastAPI server entry point for Document Insight Extractor
"""
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pathlib import Path
import logging

from services.document_parser import parse_document, DocumentParseError
from services.ai_extractor import AIExtractor
from utils.helpers import validate_file_extension, generate_unique_filename, cleanup_temp_file, get_file_size
from config import TEMP_UPLOADS_DIR, MAX_FILE_SIZE

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="AI-Powered Document Insight Extractor",
    description="Extract structured insights from retail media documents",
    version="1.0.0"
)

# Configure CORS
# Get allowed origins from environment variable or use defaults
import os
ALLOWED_ORIGINS = os.getenv(
    "ALLOWED_ORIGINS",
    "http://localhost:5173,http://localhost:3000"
).split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,  # Supports both local dev and production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "message": "AI-Powered Document Insight Extractor API",
        "status": "running",
        "version": "1.0.0"
    }


@app.get("/health")
async def health():
    """Health check endpoint"""
    return {"status": "healthy"}


@app.get("/api/health")
async def api_health():
    """
    API health check endpoint
    
    Returns:
        JSON response with API status and version information
    """
    return {
        "status": "healthy",
        "service": "AI-Powered Document Insight Extractor",
        "version": "1.0.0",
        "endpoints": {
            "parse": "/api/parse-document",
            "analyze": "/api/analyze",
            "extract_insights": "/api/extract-insights"
        }
    }


@app.post("/api/parse-document")
async def parse_document_endpoint(file: UploadFile = File(...)):
    """
    Parse a document (PDF or DOCX) and extract text
    
    Args:
        file: Uploaded file (PDF or DOCX)
        
    Returns:
        JSON response with extracted text and metadata
    """
    temp_file_path = None
    
    try:
        # Validate file extension
        if not validate_file_extension(file.filename):
            raise HTTPException(
                status_code=400,
                detail=f"Unsupported file format. Supported formats: .pdf, .docx"
            )
        
        # Generate unique filename for temporary storage
        temp_file_path = generate_unique_filename(file.filename)
        
        # Save uploaded file temporarily
        with open(temp_file_path, "wb") as buffer:
            content = await file.read()
            
            # Check file size
            if len(content) > MAX_FILE_SIZE:
                cleanup_temp_file(temp_file_path)
                raise HTTPException(
                    status_code=400,
                    detail=f"File size exceeds maximum allowed size of {MAX_FILE_SIZE / (1024*1024):.1f}MB"
                )
            
            buffer.write(content)
        
        # Parse the document
        try:
            extracted_text = parse_document(temp_file_path)
            
            # Get file size
            file_size = get_file_size(temp_file_path)
            
            return JSONResponse(
                status_code=200,
                content={
                    "success": True,
                    "filename": file.filename,
                    "file_size": file_size,
                    "file_type": Path(file.filename).suffix.lower(),
                    "text_length": len(extracted_text),
                    "word_count": len(extracted_text.split()),
                    "text": extracted_text,
                    "message": "Document parsed successfully"
                }
            )
            
        except DocumentParseError as e:
            raise HTTPException(status_code=400, detail=f"Document parsing error: {str(e)}")
        except ValueError as e:
            raise HTTPException(status_code=400, detail=f"Invalid document: {str(e)}")
        except FileNotFoundError as e:
            raise HTTPException(status_code=404, detail=str(e))
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")
    
    finally:
        # Clean up temporary file
        if temp_file_path and temp_file_path.exists():
            cleanup_temp_file(temp_file_path)


@app.post("/api/analyze")
async def analyze_document_endpoint(file: UploadFile = File(...)):
    """
    Analyze a document (PDF or DOCX) and extract text
    
    This endpoint:
    1. Validates file type and size
    2. Saves file temporarily
    3. Parses the document to extract text
    4. Returns extracted text with metadata
    
    Args:
        file: Uploaded file (PDF or DOCX)
        
    Returns:
        JSON response with extracted text and metadata
        
    Raises:
        HTTPException: If file validation fails or parsing errors occur
    """
    temp_file_path = None
    
    try:
        # Validate file extension
        if not validate_file_extension(file.filename):
            raise HTTPException(
                status_code=400,
                detail=f"Unsupported file format. Supported formats: .pdf, .docx"
            )
        
        # Generate unique filename for temporary storage
        temp_file_path = generate_unique_filename(file.filename)
        
        # Save uploaded file temporarily
        with open(temp_file_path, "wb") as buffer:
            content = await file.read()
            
            # Check file size
            if len(content) > MAX_FILE_SIZE:
                cleanup_temp_file(temp_file_path)
                raise HTTPException(
                    status_code=400,
                    detail=f"File size exceeds maximum allowed size of {MAX_FILE_SIZE / (1024*1024):.1f}MB"
                )
            
            buffer.write(content)
        
        # Parse the document
        try:
            logger.info(f"Analyzing document: {file.filename}")
            extracted_text = parse_document(temp_file_path)
            
            if not extracted_text or not extracted_text.strip():
                raise HTTPException(
                    status_code=400,
                    detail="Document contains no extractable text"
                )
            
            # Get file size
            file_size = get_file_size(temp_file_path)
            
            logger.info(f"Document analyzed successfully: {len(extracted_text)} characters extracted")
            
            return JSONResponse(
                status_code=200,
                content={
                    "success": True,
                    "filename": file.filename,
                    "file_size": file_size,
                    "file_type": Path(file.filename).suffix.lower(),
                    "text_length": len(extracted_text),
                    "word_count": len(extracted_text.split()),
                    "text": extracted_text,
                    "message": "Document analyzed successfully"
                }
            )
            
        except DocumentParseError as e:
            error_msg = f"Unable to parse document. The file may be corrupted or in an unsupported format. Error: {str(e)}"
            logger.error(f"Document parsing error for {file.filename}: {str(e)}")
            raise HTTPException(status_code=400, detail=error_msg)
        except ValueError as e:
            error_msg = f"Invalid document: {str(e)}. Please ensure the file is a valid PDF or DOCX document."
            logger.error(f"Value error for {file.filename}: {str(e)}")
            raise HTTPException(status_code=400, detail=error_msg)
        except FileNotFoundError as e:
            error_msg = f"File not found: {str(e)}. Please try uploading the file again."
            logger.error(f"File not found: {str(e)}")
            raise HTTPException(status_code=404, detail=error_msg)
        
    except HTTPException:
        raise
    except Exception as e:
        error_msg = "An unexpected error occurred. Please try again or contact support if the problem persists."
        logger.error(f"Unexpected error during document analysis: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=error_msg)
    
    finally:
        # Clean up temporary file
        if temp_file_path and temp_file_path.exists():
            cleanup_temp_file(temp_file_path)


@app.post("/api/extract-insights")
async def extract_insights_endpoint(file: UploadFile = File(...)):
    """
    Parse a document and extract AI-powered insights
    
    This endpoint:
    1. Parses the document (PDF or DOCX)
    2. Summarizes using T5-Small (2-3 sentences)
    3. Classifies document type
    4. Extracts structured data using pattern matching:
       - Technical specs (dimensions, formats, file sizes)
       - Deadlines (dates)
       - KPIs (CTR, CPC, conversion rate, etc.)
       - Brand guidelines (colors, fonts, tone)
       - Action items (tasks to do)
       - Warnings (compliance issues)
    
    Args:
        file: Uploaded file (PDF or DOCX)
        
    Returns:
        JSON response with extracted insights
    """
    temp_file_path = None
    
    try:
        # Validate file extension
        if not file.filename:
            raise HTTPException(
                status_code=400,
                detail="No file provided. Please upload a PDF or DOCX file."
            )
        
        if not validate_file_extension(file.filename):
            file_ext = Path(file.filename).suffix.lower() if file.filename else "unknown"
            raise HTTPException(
                status_code=400,
                detail=f"Unsupported file format '{file_ext}'. Please upload a PDF (.pdf) or DOCX (.docx) file."
            )
        
        # Generate unique filename for temporary storage
        temp_file_path = generate_unique_filename(file.filename)
        
        # Save uploaded file temporarily
        with open(temp_file_path, "wb") as buffer:
            content = await file.read()
            
            # Check if file is empty
            if len(content) == 0:
                cleanup_temp_file(temp_file_path)
                raise HTTPException(
                    status_code=400,
                    detail="Uploaded file is empty. Please upload a valid PDF or DOCX file."
                )
            
            # Check file size
            file_size_mb = len(content) / (1024 * 1024)
            if len(content) > MAX_FILE_SIZE:
                cleanup_temp_file(temp_file_path)
                max_size_mb = MAX_FILE_SIZE / (1024 * 1024)
                raise HTTPException(
                    status_code=400,
                    detail=f"File size ({file_size_mb:.2f}MB) exceeds maximum allowed size of {max_size_mb:.1f}MB. Please upload a smaller file."
                )
            
            buffer.write(content)
        
        # Parse the document
        try:
            logger.info(f"Parsing document: {file.filename}")
            extracted_text = parse_document(temp_file_path)
            
            if not extracted_text or not extracted_text.strip():
                raise HTTPException(
                    status_code=400,
                    detail="Document contains no extractable text. Please ensure the document has readable content."
                )
            
            # Extract insights using AI
            logger.info("Starting AI extraction...")
            extractor = AIExtractor()
            insights = extractor.extract_insights(extracted_text)
            
            # Check if extraction failed
            if "error" in insights:
                raise HTTPException(
                    status_code=500,
                    detail=f"AI extraction failed: {insights.get('error', 'Unknown error')}. Please try again."
                )
            
            # Get file size
            file_size = get_file_size(temp_file_path)
            
            # Build structured response (insights already has new structure)
            response_data = {
                "success": True,
                "message": "Insights extracted successfully",
                "summary": insights.get("summary", {
                    "goal": "",
                    "dates": [],
                    "channels": [],
                    "primary_kpis": [],
                    "key_constraints": []
                }),
                "document_type": insights.get("document_type", {}),
                "creative_requirements": insights.get("creative_requirements", {"must_have": [], "optional": []}),
                "technical_specs": insights.get("technical_specs", []),
                "guidelines": insights.get("guidelines", {
                    "copy_rules": [],
                    "design_rules": [],
                    "accessibility_rules": [],
                    "legal_rules": []
                }),
                "action_items": insights.get("action_items", []),
                "file_metadata": {
                    "filename": file.filename,
                    "file_size": file_size,
                    "file_type": Path(file.filename).suffix.lower(),
                    "text_length": len(extracted_text),
                    "word_count": len(extracted_text.split())
                },
                "metadata": insights.get("metadata", {})
            }
            
            logger.info("AI extraction completed successfully")
            
            return JSONResponse(
                status_code=200,
                content=response_data
            )
            
        except DocumentParseError as e:
            error_msg = f"Unable to parse document. The file may be corrupted or in an unsupported format. Error: {str(e)}"
            logger.error(f"Document parsing error for {file.filename}: {str(e)}")
            raise HTTPException(status_code=400, detail=error_msg)
        except ValueError as e:
            error_msg = f"Invalid document: {str(e)}. Please ensure the file is a valid PDF or DOCX document."
            logger.error(f"Value error for {file.filename}: {str(e)}")
            raise HTTPException(status_code=400, detail=error_msg)
        except FileNotFoundError as e:
            error_msg = f"File not found: {str(e)}. Please try uploading the file again."
            logger.error(f"File not found: {str(e)}")
            raise HTTPException(status_code=404, detail=error_msg)
        except Exception as e:
            error_msg = "An error occurred during AI extraction. Please try again or contact support if the problem persists."
            logger.error(f"AI extraction error for {file.filename}: {str(e)}", exc_info=True)
            raise HTTPException(status_code=500, detail=error_msg)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")
    
    finally:
        # Clean up temporary file
        if temp_file_path and temp_file_path.exists():
            cleanup_temp_file(temp_file_path)
