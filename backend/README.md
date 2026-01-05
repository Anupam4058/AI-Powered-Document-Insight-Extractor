# Backend - AI-Powered Document Insight Extractor

FastAPI backend service for extracting structured insights from retail media documents using AI models.

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- pip

### Installation

```bash
# Navigate to backend directory
cd backend

# Create virtual environment (recommended)
python -m venv venv

# Activate virtual environment
# On Windows:
.\venv\Scripts\activate
# On Linux/Mac:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Start Server

```bash
# Using uvicorn
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# Or using Python module
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The server will start at: **http://localhost:8000**

### API Documentation

Once the server is running, visit:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 📁 Project Structure

```
backend/
├── main.py                 # FastAPI application entry point
├── config.py               # Configuration settings
├── requirements.txt        # Python dependencies
├── services/              # Core services
│   ├── document_parser.py # PDF/DOCX parsing
│   ├── ai_extractor.py    # AI-powered extraction
│   └── model_loader.py    # ML model loading
├── utils/                 # Utility functions
│   ├── helpers.py         # Helper functions
│   └── pattern_matcher.py # Pattern matching for data extraction
├── models/                # Model definitions
├── temp_uploads/          # Temporary file storage
└── test_documents/        # Test documents
```

## 🎯 Features

### Document Processing
- **PDF Parsing**: Extract text from PDF files using pdfplumber
- **DOCX Parsing**: Extract text from DOCX files using python-docx
- **File Validation**: Type and size validation (max 10MB)
- **Error Handling**: Comprehensive error handling for corrupted files

### AI-Powered Extraction
- **Text Summarization**: T5-Small model for 2-3 sentence summaries
- **Document Classification**: DistilBERT for document type classification
- **Pattern Matching**: Extract structured data:
  - Technical specifications (dimensions, formats, file sizes)
  - Deadlines and dates
  - KPIs (CTR, CPC, conversion rate, etc.)
  - Brand guidelines (colors, fonts, tone)
  - Action items
  - Compliance warnings

### API Endpoints

#### Health Check Endpoints
- `GET /` - Root endpoint with API information
- `GET /health` - Basic health check
- `GET /api/health` - Detailed API health check

#### Document Endpoints
- `POST /api/parse-document` - Parse document and extract text
- `POST /api/analyze` - Analyze document and return extracted text
- `POST /api/extract-insights` - Extract AI-powered insights

## 🔧 Configuration

### Environment Variables

Create a `.env` file in the `backend/` directory:

```env
# AI Model Configuration
T5_MODEL_NAME=t5-small
DISTILBERT_MODEL_NAME=distilbert-base-uncased
DEVICE=cpu  # or 'cuda' for GPU

# API Configuration
API_HOST=0.0.0.0
API_PORT=8000
```

### File Upload Settings

Configured in `config.py`:
- **Max File Size**: 10MB
- **Allowed Extensions**: `.pdf`, `.docx`
- **Temp Directory**: `temp_uploads/`

### CORS Configuration

CORS is configured in `main.py` to allow:
- `http://localhost:5173` (Vite dev server)
- `http://localhost:3000` (Alternative frontend port)

## 📦 Dependencies

### Core Dependencies
- `fastapi` - Web framework
- `uvicorn` - ASGI server
- `python-multipart` - File upload support
- `pdfplumber` - PDF parsing
- `python-docx` - DOCX parsing
- `transformers` - Hugging Face transformers
- `torch` - PyTorch for ML models
- `python-dotenv` - Environment variable management
- `sentencepiece` - Tokenizer for T5 model

See `requirements.txt` for complete list.

## 🧪 Testing

### Test Scripts

```bash
# Test document parser
python test_parser.py

# Test AI extraction
python test_ai_extraction.py

# Test model loader
python test_model_loader.py

# Test API endpoints
python test_endpoints.py
```

### Manual Testing

#### Using curl

```bash
# Health check
curl http://localhost:8000/api/health

# Parse document
curl -X POST "http://localhost:8000/api/parse-document" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@path/to/document.pdf"

# Extract insights
curl -X POST "http://localhost:8000/api/extract-insights" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@path/to/document.pdf"
```

#### Using Swagger UI

1. Start the server
2. Visit http://localhost:8000/docs
3. Use the interactive API documentation to test endpoints

### Testing Checklist

- [ ] Health endpoints return correct responses
- [ ] PDF files can be parsed
- [ ] DOCX files can be parsed
- [ ] File validation works (type and size)
- [ ] AI extraction returns structured data
- [ ] Error handling works for invalid files
- [ ] CORS allows frontend requests

## 🐛 Troubleshooting

### Port Already in Use

If port 8000 is in use:

```bash
uvicorn main:app --reload --port 8001
```

Update frontend `VITE_API_URL` accordingly.

### Model Loading Issues

**Symptoms**: Slow startup or model loading errors

**Solutions**:
1. Models are downloaded on first use (may take time)
2. Check internet connection for model downloads
3. Models are cached in `~/.cache/huggingface/`
4. Use `DEVICE=cpu` if GPU is not available

### Memory Issues

**Symptoms**: Out of memory errors

**Solutions**:
1. Use CPU instead of GPU: `DEVICE=cpu`
2. Process smaller files
3. Increase system RAM
4. Models load on first request (may take time)

### File Upload Errors

**Symptoms**: File upload fails

**Solutions**:
1. Check file size (max 10MB)
2. Check file type (only PDF and DOCX)
3. Verify `temp_uploads/` directory exists and is writable
4. Check backend logs for detailed errors

## 🔒 Security Considerations

### File Upload Security
- File type validation
- File size limits
- Temporary file cleanup
- No persistent file storage

### CORS
- Configured for specific origins
- Credentials allowed for authenticated requests
- Adjust origins for production deployment

### Environment Variables
- Sensitive configuration in `.env` file
- `.env` should not be committed to version control
- Use environment-specific configurations

## 📊 Performance

### Model Loading
- Models load on first request (~10-30 seconds)
- Models are cached after first load
- Subsequent requests are faster

### Processing Time
- Small files (< 1MB): ~5-10 seconds
- Medium files (1-5MB): ~10-30 seconds
- Large files (5-10MB): ~30-60 seconds

### Optimization Tips
1. Use GPU if available (`DEVICE=cuda`)
2. Process files in batches
3. Cache model instances
4. Use smaller models for faster processing

## 🚀 Deployment

### Production Deployment

1. **Set Environment Variables**:
   ```env
   DEVICE=cpu
   API_HOST=0.0.0.0
   API_PORT=8000
   ```

2. **Use Production Server**:
   ```bash
   uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
   ```

3. **Configure CORS**:
   Update `allow_origins` in `main.py` with production frontend URL

4. **Set Up Reverse Proxy**:
   Use nginx or similar for production deployment

### Docker Deployment (Optional)

```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

## 📝 API Response Format

### Extract Insights Response

```json
{
  "success": true,
  "message": "Insights extracted successfully",
  "summary": "Document summary...",
  "document_type": {
    "type": "Creative Brief",
    "confidence": 0.95
  },
  "creative_requirements": {
    "dimensions": ["1080x1080", "1200x628"],
    "formats": ["JPG", "PNG"],
    "file_sizes": ["5 MB"],
    "colors": ["#FF5733", "Blue"],
    "fonts": ["Arial", "Helvetica"],
    "tone": ["professional", "modern"]
  },
  "technical_specs": {...},
  "brand_guidelines": {...},
  "kpis": {...},
  "deadlines": [...],
  "action_items": [...],
  "warnings": [...],
  "file_metadata": {...}
}
```

## 🔗 Related Documentation

- Frontend documentation: `../frontend/README.md`
- Integration guide: `../INTEGRATION_QUICK_START.md`

## ✅ Status

**Backend**: ✅ Complete and ready for use

All features implemented:
- ✅ Document parsing (PDF/DOCX)
- ✅ AI-powered extraction
- ✅ Pattern matching
- ✅ Error handling
- ✅ API endpoints
- ✅ CORS configuration

---

**Version**: 1.0.0  
**Last Updated**: 2024

