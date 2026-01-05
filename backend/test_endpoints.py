"""
Test script for FastAPI endpoints
Tests all Phase 4 endpoints to verify they work correctly
"""
import requests
import sys
from pathlib import Path

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent))

BASE_URL = "http://localhost:8000"


def test_health_endpoints():
    """Test health check endpoints"""
    print("=" * 70)
    print("Testing Health Check Endpoints")
    print("=" * 70)
    
    # Test root endpoint
    try:
        response = requests.get(f"{BASE_URL}/")
        print(f"\n[GET /]")
        print(f"  Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"  Response: {data}")
            print(f"  [PASS] Root endpoint working")
        else:
            print(f"  [FAIL] Unexpected status code")
            return False
    except Exception as e:
        print(f"  [ERROR] {e}")
        return False
    
    # Test /health endpoint
    try:
        response = requests.get(f"{BASE_URL}/health")
        print(f"\n[GET /health]")
        print(f"  Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"  Response: {data}")
            print(f"  [PASS] Health endpoint working")
        else:
            print(f"  [FAIL] Unexpected status code")
            return False
    except Exception as e:
        print(f"  [ERROR] {e}")
        return False
    
    # Test /api/health endpoint
    try:
        response = requests.get(f"{BASE_URL}/api/health")
        print(f"\n[GET /api/health]")
        print(f"  Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"  Response: {data}")
            print(f"  [PASS] API health endpoint working")
        else:
            print(f"  [FAIL] Unexpected status code")
            return False
    except Exception as e:
        print(f"  [ERROR] {e}")
        return False
    
    return True


def test_analyze_endpoint():
    """Test /api/analyze endpoint"""
    print("\n" + "=" * 70)
    print("Testing /api/analyze Endpoint")
    print("=" * 70)
    
    # Check if test document exists
    test_file = Path(__file__).parent / "test_documents" / "sample_creative_brief.txt"
    
    if not test_file.exists():
        print("\n[SKIP] No test file found. Create a PDF or DOCX file to test.")
        print("       Place it in: backend/test_documents/")
        return None
    
    # For now, we can't test with .txt files
    # User needs to provide a PDF or DOCX
    print("\n[INFO] To test /api/analyze endpoint:")
    print("       1. Start the server: uvicorn main:app --reload")
    print("       2. Use Swagger UI: http://localhost:8000/docs")
    print("       3. Or use curl/Postman with a PDF or DOCX file")
    print("\n       Example curl command:")
    print('       curl -X POST "http://localhost:8000/api/analyze" \\')
    print('         -H "accept: application/json" \\')
    print('         -H "Content-Type: multipart/form-data" \\')
    print('         -F "file=@path/to/your/document.pdf"')
    
    return None


def test_server_running():
    """Check if server is running"""
    try:
        response = requests.get(f"{BASE_URL}/health", timeout=2)
        return response.status_code == 200
    except:
        return False


def main():
    print("FastAPI Endpoints Test Script")
    print("=" * 70)
    
    # Check if server is running
    print("\nChecking if server is running...")
    if not test_server_running():
        print("[ERROR] Server is not running!")
        print("\nPlease start the server first:")
        print("  cd backend")
        print("  .\\venv\\Scripts\\Activate.ps1")
        print("  uvicorn main:app --reload --port 8000")
        print("\nThen run this test script again.")
        sys.exit(1)
    
    print("[OK] Server is running\n")
    
    # Test health endpoints
    health_ok = test_health_endpoints()
    
    # Test analyze endpoint (informational)
    test_analyze_endpoint()
    
    # Summary
    print("\n" + "=" * 70)
    print("Test Summary")
    print("=" * 70)
    
    if health_ok:
        print("[SUCCESS] All health check endpoints are working!")
        print("\nAvailable endpoints:")
        print("  - GET  /              - Root endpoint")
        print("  - GET  /health        - Health check")
        print("  - GET  /api/health     - API health check (Phase 4)")
        print("  - POST /api/analyze    - Analyze document (Phase 4)")
        print("  - POST /api/parse-document - Parse document")
        print("  - POST /api/extract-insights - Extract AI insights")
        print("\nInteractive API docs: http://localhost:8000/docs")
    else:
        print("[FAIL] Some endpoints are not working correctly")
        sys.exit(1)


if __name__ == "__main__":
    main()

