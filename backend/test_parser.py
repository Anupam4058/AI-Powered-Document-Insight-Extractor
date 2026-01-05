"""
Test script for document parser
Run this script to test the document parser with sample files
"""
import sys
from pathlib import Path

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent))

from services.document_parser import parse_document, DocumentParseError
from utils.helpers import validate_file_extension


def test_parser(file_path: str):
    """Test the document parser with a file"""
    file_path = Path(file_path)
    
    print(f"\n{'='*60}")
    print(f"Testing: {file_path.name}")
    print(f"{'='*60}")
    
    # Validate extension
    if not validate_file_extension(file_path.name):
        print(f"[ERROR] Invalid file extension. Supported: .pdf, .docx")
        return False
    
    # Check if file exists
    if not file_path.exists():
        print(f"[ERROR] File not found: {file_path}")
        return False
    
    try:
        # Parse document
        print(f"Parsing document...")
        text = parse_document(file_path)
        
        # Display results
        print(f"[SUCCESS] Successfully extracted text!")
        print(f"\nStatistics:")
        print(f"   - Character count: {len(text)}")
        print(f"   - Word count: {len(text.split())}")
        print(f"   - Line count: {len(text.splitlines())}")
        
        # Show preview
        print(f"\nText Preview (first 500 characters):")
        print(f"{'-'*60}")
        preview = text[:500] + "..." if len(text) > 500 else text
        print(preview)
        print(f"{'-'*60}")
        
        return True
        
    except FileNotFoundError as e:
        print(f"[ERROR] File Not Found: {e}")
        return False
    except ValueError as e:
        print(f"[ERROR] ValueError: {e}")
        return False
    except DocumentParseError as e:
        print(f"[ERROR] Parse Error: {e}")
        return False
    except Exception as e:
        print(f"[ERROR] Unexpected Error ({type(e).__name__}): {e}")
        return False


def test_edge_cases():
    """Test edge cases"""
    print(f"\n{'='*60}")
    print("Testing Edge Cases")
    print(f"{'='*60}")
    
    test_cases = [
        # (test_name, file_path, should_fail)
        ("Non-existent file", Path("temp_uploads/nonexistent.pdf"), True),
        ("Invalid extension", Path("temp_uploads/test.txt"), True),
    ]
    
    for test_name, file_path, should_fail in test_cases:
        print(f"\nTest: {test_name}")
        try:
            text = parse_document(file_path)
            if should_fail:
                print(f"[FAIL] Expected failure but succeeded!")
            else:
                print(f"[PASS] Extracted {len(text)} characters")
        except Exception as e:
            if should_fail:
                print(f"[PASS] Expected error ({type(e).__name__}): {str(e)[:50]}")
            else:
                print(f"[FAIL] Unexpected error: {e}")


if __name__ == "__main__":
    print("Document Parser Test Script")
    print("=" * 60)
    
    # Test with provided file path
    if len(sys.argv) > 1:
        file_path = sys.argv[1]
        test_parser(file_path)
    else:
        print("\nUsage: python test_parser.py <file_path>")
        print("\nExample:")
        print("  python test_parser.py temp_uploads/sample.pdf")
        print("  python test_parser.py temp_uploads/sample.docx")
        
        # Test edge cases
        test_edge_cases()
        
        print("\n" + "="*60)
        print("Note: To test with actual files, provide a file path as argument")
        print("="*60)
