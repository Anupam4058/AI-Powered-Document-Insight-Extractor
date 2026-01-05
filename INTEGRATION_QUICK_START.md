# Full Application Quick Start Guide

## 🚀 Running the Complete Application

### Step 1: Start Backend Server

```bash
# Navigate to backend directory
cd backend

# Activate virtual environment (if using one)
# On Windows:
.\venv\Scripts\activate
# On Mac/Linux:
source venv/bin/activate

# Start the FastAPI server
uvicorn main:app --reload --port 8000
```

**Expected Output**:
```
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

### Step 2: Start Frontend Server

Open a **new terminal**:

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies (if not already done)
npm install

# Start the development server
npm run dev
```

**Expected Output**:
```
  VITE v7.x.x  ready in xxx ms

  ➜  Local:   http://localhost:5173/
  ➜  Network: use --host to expose
```

### Step 3: Open Application

1. Open your browser
2. Navigate to: `http://localhost:5173`
3. You should see:
   - "AI-Powered Document Insight Extractor" header
   - "Backend Connected" green badge (if backend is running)
   - Upload area on the left
   - Results area on the right

### Step 4: Test the Application

1. **Upload a Document**:
   - Drag and drop a PDF or DOCX file onto the upload area
   - OR click the upload area to browse for a file
   - File must be under 10MB

2. **Extract Insights**:
   - Click the "Extract Insights" button
   - Wait for processing (you'll see a loading spinner)
   - Results will appear in the right panel

3. **Download Results**:
   - Scroll through the results
   - Click "Download Results as JSON" button
   - JSON file will download with all extracted insights

## 🔍 Verification Checklist

- [ ] Backend server running on port 8000
- [ ] Frontend server running on port 5173
- [ ] "Backend Connected" badge appears (green)
- [ ] Can upload PDF files
- [ ] Can upload DOCX files
- [ ] Processing indicator shows during upload
- [ ] Results display correctly
- [ ] Can download JSON results
- [ ] No console errors in browser

## 🐛 Troubleshooting

### Backend Not Connecting

**Symptoms**: Red "Backend Disconnected" badge

**Solutions**:
1. Verify backend is running: Check terminal for server logs
2. Check port: Backend should be on port 8000
3. Check URL: Frontend expects `http://localhost:8000`
4. Check CORS: Verify backend CORS allows `http://localhost:5173`

### CORS Errors

**Symptoms**: Console shows CORS errors

**Solutions**:
1. Verify backend `main.py` has CORS middleware configured
2. Check allowed origins include `http://localhost:5173`
3. Restart backend server after CORS changes

### File Upload Fails

**Symptoms**: Error message appears after clicking "Extract Insights"

**Solutions**:
1. Check file size (must be under 10MB)
2. Check file type (only PDF and DOCX supported)
3. Check backend logs for processing errors
4. Verify backend models are loaded (check backend terminal)

### Results Not Displaying

**Symptoms**: Processing completes but no results shown

**Solutions**:
1. Check browser console for errors
2. Check network tab for API response
3. Verify backend returned valid JSON
4. Check backend logs for extraction errors

## 📝 Environment Variables

### Frontend (Optional)

Create `frontend/.env`:
```env
VITE_API_URL=http://localhost:8000
```

### Backend (Optional)

Create `backend/.env`:
```env
T5_MODEL_NAME=t5-small
DISTILBERT_MODEL_NAME=distilbert-base-uncased
DEVICE=cpu
```

## 🧪 Testing

For comprehensive testing, see:
- `frontend/README.md` - Frontend documentation and testing guide
- `backend/README.md` - Backend documentation and testing guide

## 📚 Documentation

- **Frontend**: `frontend/README.md` - Complete frontend documentation
- **Backend**: `backend/README.md` - Complete backend documentation
- **Integration**: This file - Quick start guide for full application

## ✅ Success Indicators

When everything is working:
- ✅ Green "Backend Connected" badge
- ✅ File uploads successfully
- ✅ Processing completes without errors
- ✅ Results display in organized sections
- ✅ JSON download works
- ✅ No console errors

---

**Status**: ✅ Application Ready for Use

