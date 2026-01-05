"""
Test script for AI extraction functionality
Run this script to test the AI extraction on sample documents

Usage:
    python test_ai_extraction.py [file_path]
    
If no file path is provided, uses sample text from test document.
"""
import sys
import time
from pathlib import Path

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent))

from services.ai_extractor import AIExtractor
from services.document_parser import parse_document, DocumentParseError
import json
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)


def load_sample_text():
    """Load sample text from test document"""
    sample_file = Path(__file__).parent / "test_documents" / "sample_creative_brief.txt"
    if sample_file.exists():
        with open(sample_file, 'r', encoding='utf-8') as f:
            return f.read()
    else:
        # Fallback sample text
        return """
        CREATIVE BRIEF - Q4 RETAIL CAMPAIGN
        Brand: TechRetail Inc.
        Campaign: Holiday Shopping Season 2026
        
        TECHNICAL SPECIFICATIONS
        Ad Dimensions: 1200x628 pixels, 1080x1080 pixels
        File Formats: JPG, PNG, MP4
        Maximum file size: 10MB
        
        DEADLINES
        Creative concepts due: October 20, 2025
        Final assets due: October 25, 2025
        
        PERFORMANCE KPIs
        CTR: 2.5%, CPC: $0.75, Conversion Rate: 3.2%
        
        BRAND GUIDELINES
        Primary Color: #FF5733
        Font: Arial, 16pt
        Tone: Professional and friendly
        """


def test_ai_extraction(text: str, source: str = "sample text"):
    """Test AI extraction on provided text"""
    print(f"\n{'='*70}")
    print(f"Testing AI Extraction")
    print(f"Source: {source}")
    print(f"Text Length: {len(text)} characters, {len(text.split())} words")
    print(f"{'='*70}\n")
    
    extractor = AIExtractor()
    
    # Measure extraction time
    start_time = time.time()
    
    try:
        print("Starting extraction...")
        print("(First run may take longer as models download from Hugging Face)\n")
        
        insights = extractor.extract_insights(text)
        
        elapsed_time = time.time() - start_time
        
        # Display results
        print(f"\n{'='*70}")
        print("EXTRACTION RESULTS")
        print(f"{'='*70}\n")
        
        print(f"[TIME] Extraction Time: {elapsed_time:.2f} seconds\n")
        
        # Summary
        print("[SUMMARY]")
        print("-" * 70)
        print(insights.get('summary', 'N/A'))
        print()
        
        # Document Type
        doc_type = insights.get('document_type', {})
        print("[DOCUMENT TYPE]")
        print("-" * 70)
        print(f"   Type: {doc_type.get('document_type', 'Unknown')}")
        print(f"   Confidence: {doc_type.get('confidence', 0.0):.2%}")
        print()
        
        # Extracted Data
        extracted = insights.get('extracted_data', {})
        
        # Technical Specs
        tech_specs = extracted.get('technical_specs', {})
        if tech_specs:
            print("[TECHNICAL SPECIFICATIONS]")
            print("-" * 70)
            if tech_specs.get('dimensions'):
                print(f"   Dimensions: {', '.join(tech_specs['dimensions'])}")
            if tech_specs.get('formats'):
                print(f"   Formats: {', '.join(tech_specs['formats'])}")
            if tech_specs.get('file_sizes'):
                print(f"   File Sizes: {', '.join(tech_specs['file_sizes'])}")
            print()
        
        # Deadlines
        deadlines = extracted.get('deadlines', [])
        if deadlines:
            print("[DEADLINES]")
            print("-" * 70)
            for deadline in deadlines[:5]:  # Show first 5
                print(f"   {deadline['date']} ({deadline['type']})")
                if len(deadline.get('context', '')) > 0:
                    print(f"      Context: {deadline['context'][:80]}...")
            print()
        
        # KPIs
        kpis = extracted.get('kpis', {})
        if kpis:
            print("[KPIs]")
            print("-" * 70)
            for kpi_name, values in kpis.items():
                if values:
                    avg_value = sum(values) / len(values)
                    print(f"   {kpi_name.upper()}: {avg_value:.2f} (found {len(values)} occurrence(s))")
            print()
        
        # Brand Guidelines
        brand = extracted.get('brand_guidelines', {})
        if brand:
            print("[BRAND GUIDELINES]")
            print("-" * 70)
            if brand.get('colors'):
                print(f"   Colors: {', '.join(brand['colors'][:5])}")
            if brand.get('fonts'):
                print(f"   Fonts: {', '.join(brand['fonts'][:5])}")
            if brand.get('tone'):
                print(f"   Tone: {', '.join(brand['tone'])}")
            print()
        
        # Action Items
        actions = extracted.get('action_items', [])
        if actions:
            print("[ACTION ITEMS]")
            print("-" * 70)
            for i, action in enumerate(actions[:10], 1):  # Show first 10
                print(f"   {i}. {action[:100]}{'...' if len(action) > 100 else ''}")
            print()
        
        # Warnings
        warnings = extracted.get('warnings', [])
        if warnings:
            print("[WARNINGS]")
            print("-" * 70)
            for warning in warnings[:5]:  # Show first 5
                print(f"   [{warning.get('type', 'warning').upper()}] {warning.get('text', '')[:100]}...")
            print()
        
        # Metadata
        metadata = insights.get('metadata', {})
        if metadata:
            print("[METADATA]")
            print("-" * 70)
            for key, value in metadata.items():
                print(f"   {key}: {value}")
            print()
        
        # Full JSON output (optional)
        print(f"{'='*70}")
        print("Full JSON Output (for debugging):")
        print(f"{'='*70}")
        print(json.dumps(insights, indent=2, default=str))
        
        return True, insights, elapsed_time
        
    except Exception as e:
        elapsed_time = time.time() - start_time
        print(f"\n❌ ERROR: {str(e)}")
        print(f"Time elapsed: {elapsed_time:.2f} seconds")
        import traceback
        traceback.print_exc()
        return False, None, elapsed_time


def test_with_file(file_path: str):
    """Test AI extraction with a document file"""
    file_path = Path(file_path)
    
    if not file_path.exists():
        print(f"❌ File not found: {file_path}")
        return False
    
    try:
        print(f"Parsing document: {file_path.name}...")
        text = parse_document(file_path)
        print(f"✓ Document parsed successfully ({len(text)} characters)\n")
        
        return test_ai_extraction(text, source=str(file_path))
        
    except DocumentParseError as e:
        print(f"❌ Document parsing error: {e}")
        return False, None, 0
    except Exception as e:
        print(f"❌ Error: {e}")
        return False, None, 0


def performance_test():
    """Run performance test with sample text"""
    print(f"\n{'='*70}")
    print("PERFORMANCE TEST")
    print(f"{'='*70}\n")
    
    text = load_sample_text()
    
    times = []
    for i in range(3):
        print(f"Run {i+1}/3...")
        extractor = AIExtractor()
        start = time.time()
        insights = extractor.extract_insights(text)
        elapsed = time.time() - start
        times.append(elapsed)
        print(f"  Time: {elapsed:.2f} seconds\n")
    
    avg_time = sum(times) / len(times)
    min_time = min(times)
    max_time = max(times)
    
    print(f"{'='*70}")
    print("PERFORMANCE RESULTS:")
    print(f"{'='*70}")
    print(f"  Average: {avg_time:.2f} seconds")
    print(f"  Minimum: {min_time:.2f} seconds")
    print(f"  Maximum: {max_time:.2f} seconds")
    print()
    
    if avg_time > 10:
        print("⚠️  WARNING: Extraction is slower than expected (>10s)")
        print("   Consider optimizing model loading or text processing")
    elif avg_time < 5:
        print("✓ Performance is good (<5s average)")
    else:
        print("✓ Performance is acceptable (5-10s average)")


if __name__ == "__main__":
    print("AI Extraction Test Script")
    print("=" * 70)
    
    if len(sys.argv) > 1:
        # Test with provided file
        file_path = sys.argv[1]
        success, insights, elapsed = test_with_file(file_path)
        
        if success:
            print(f"\n[SUCCESS] Test completed successfully in {elapsed:.2f} seconds")
        else:
            print(f"\n[FAIL] Test failed after {elapsed:.2f} seconds")
            sys.exit(1)
    else:
        # Test with sample text
        print("\nNo file provided. Using sample text from test document.")
        print("Usage: python test_ai_extraction.py <file_path>")
        print("\nExample: python test_ai_extraction.py test_documents/sample_creative_brief.txt")
        print("\nOr test with a PDF/DOCX: python test_ai_extraction.py temp_uploads/sample.pdf\n")
        
        text = load_sample_text()
        success, insights, elapsed = test_ai_extraction(text, source="sample text")
        
        if success:
            print(f"\n✅ Test completed successfully in {elapsed:.2f} seconds")
            
            # Ask if user wants performance test
            print("\n" + "=" * 70)
            print("Run performance test? (y/n): ", end="")
            try:
                response = input().strip().lower()
                if response == 'y':
                    performance_test()
            except:
                pass
        else:
            print(f"\n❌ Test failed after {elapsed:.2f} seconds")
            sys.exit(1)

