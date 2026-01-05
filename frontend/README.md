# Frontend - AI-Powered Document Insight Extractor

React + TypeScript frontend application for extracting structured insights from retail media documents.

## 🚀 Quick Start

### Prerequisites
- Node.js (v18 or higher)
- npm or yarn

### Installation

```bash
# Install dependencies
npm install

# Start development server
npm run dev
```

The application will be available at `http://localhost:5173`

### Build for Production

```bash
# Build the application
npm run build

# Preview production build
npm run preview
```

## 📁 Project Structure

```
frontend/
├── src/
│   ├── api/              # Backend API integration
│   │   └── api.ts        # API calls and error handling
│   ├── components/       # Reusable UI components
│   │   ├── FileUploader.tsx
│   │   ├── ProcessingIndicator.tsx
│   │   └── ResultsDisplay.tsx
│   ├── pages/            # Page components
│   │   └── MainPage.tsx # Main application page
│   ├── utils/           # Helper functions
│   │   ├── fileValidation.ts
│   │   └── helpers.ts
│   ├── styles/          # CSS files
│   ├── App.tsx          # Root component
│   └── main.tsx         # Entry point
├── public/              # Static assets
└── package.json         # Dependencies
```

## 🎯 Features

### File Upload
- **Drag & Drop**: Drag files directly onto the upload area
- **Click to Browse**: Click the upload area to select files
- **File Validation**: 
  - Only PDF and DOCX files accepted
  - Maximum file size: 10MB
  - Real-time validation feedback

### Processing
- **Visual Feedback**: Animated spinner during processing
- **Status Messages**: Clear indication of processing steps
- **Estimated Time**: Shows estimated processing time based on file size

### Results Display
- **Summary**: AI-generated document summary
- **Document Type**: Classification with confidence score
- **Structured Data**:
  - Creative Requirements (dimensions, formats, colors, fonts, tone)
  - Technical Specifications
  - Brand Guidelines
  - KPIs (Key Performance Indicators)
  - Deadlines (with formatted dates)
  - Action Items (with priority indicators)
  - Warnings (with severity levels)
- **Download**: Export results as JSON file

### Connection Status
- Real-time backend connection monitoring
- Visual status indicator (green/red badge)
- Automatic reconnection detection

## 🔧 Configuration

### API URL

By default, the frontend connects to `http://localhost:8000`. To change this, create a `.env` file:

```env
VITE_API_URL=http://your-backend-url:8000
```

### Environment Variables

Create `frontend/.env`:
```env
VITE_API_URL=http://localhost:8000
```

## 🧪 Testing

### Manual Testing

1. **Start Backend Server** (in separate terminal):
   ```bash
   cd ../backend
   uvicorn main:app --reload --port 8000
   ```

2. **Start Frontend**:
   ```bash
   npm run dev
   ```

3. **Test Flow**:
   - Open `http://localhost:5173`
   - Verify "Backend Connected" badge appears
   - Upload a PDF or DOCX file
   - Click "Extract Insights"
   - Wait for processing
   - Verify results display correctly
   - Download JSON results

### Testing Checklist

- [ ] File upload works (drag-and-drop and click)
- [ ] File validation works (type and size)
- [ ] Processing indicator displays correctly
- [ ] Results display in all sections
- [ ] Download JSON functionality works
- [ ] Connection status updates correctly
- [ ] Error handling works (try with backend stopped)
- [ ] Responsive design works on mobile/tablet

## 🐛 Troubleshooting

### Backend Not Connecting

**Symptoms**: Red "Backend Disconnected" badge

**Solutions**:
1. Verify backend is running on port 8000
2. Check `VITE_API_URL` in `.env` file
3. Verify CORS is configured in backend

### CORS Errors

**Symptoms**: Console shows CORS errors

**Solutions**:
1. Verify backend CORS allows `http://localhost:5173`
2. Check backend `main.py` CORS configuration
3. Restart backend server

### File Upload Fails

**Symptoms**: Error message appears after clicking "Extract Insights"

**Solutions**:
1. Check file size (must be under 10MB)
2. Check file type (only PDF and DOCX supported)
3. Check browser console for errors
4. Verify backend is running and accessible

## 📦 Dependencies

### Core Dependencies
- `react` - UI library
- `react-dom` - React DOM renderer
- `tailwindcss` - CSS framework

### Development Dependencies
- `typescript` - Type safety
- `vite` - Build tool
- `eslint` - Code linting

## 🎨 Styling

The application uses **Tailwind CSS** for styling. All styles are utility-based and responsive.

## 🔌 API Integration

### Endpoints Used

- `GET /api/health` - Health check
- `POST /api/extract-insights` - Extract insights from document

### Error Handling

The frontend includes comprehensive error handling:
- Network errors (connection refused, timeout)
- HTTP errors (400, 404, 500)
- File validation errors
- User-friendly error messages

### Request Timeout

- File processing: 5 minutes
- Health checks: 5 seconds

## 📱 Responsive Design

The application is fully responsive:
- **Desktop**: Two-column layout (upload | results)
- **Tablet**: Responsive grid layout
- **Mobile**: Single column stack

## 🚀 Deployment

### Build for Production

```bash
npm run build
```

This creates a `dist/` folder with optimized production files.

### Deploy to Static Hosting

The built files in `dist/` can be deployed to:
- Vercel
- Netlify
- GitHub Pages
- Any static file hosting service

### Environment Variables for Production

Set `VITE_API_URL` to your production backend URL before building.

## 📝 Development

### Code Structure

- **Components**: Reusable UI components in `src/components/`
- **Pages**: Full page components in `src/pages/`
- **API**: Backend integration in `src/api/`
- **Utils**: Helper functions in `src/utils/`

### TypeScript

The project uses TypeScript for type safety. All components and functions are fully typed.

### Linting

```bash
npm run lint
```

## 🔗 Related Documentation

- Backend documentation: `../backend/README.md`
- Integration guide: `../INTEGRATION_QUICK_START.md`

## ✅ Status

**Frontend**: ✅ Complete and ready for use

All features implemented:
- ✅ File upload with validation
- ✅ Processing indicator
- ✅ Results display
- ✅ JSON download
- ✅ Connection status monitoring
- ✅ Error handling
- ✅ Responsive design

---

**Version**: 1.0.0  
**Last Updated**: 2024
