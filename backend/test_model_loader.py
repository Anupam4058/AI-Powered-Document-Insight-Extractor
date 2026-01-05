"""
Test script for model loader
Run this script to test model loading and verify downloads work correctly

Note: First run will download models from Hugging Face (~5 minutes each)
Subsequent runs will use cached models (much faster)
"""
import sys
from pathlib import Path

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent))

from services.model_loader import ModelLoader
import logging

# Configure logging to see download progress
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)


def test_t5_model():
    """Test T5-Small model loading"""
    print(f"\n{'='*60}")
    print("Testing T5-Small Model (Summarization)")
    print(f"{'='*60}")
    
    try:
        loader = ModelLoader()
        print("Loading T5-Small model...")
        print("(First run: Will download ~242 MB from Hugging Face)")
        
        model, tokenizer = loader.load_t5_model()
        
        print(f"[SUCCESS] T5-Small model loaded successfully!")
        print(f"   - Model type: {type(model).__name__}")
        print(f"   - Tokenizer type: {type(tokenizer).__name__}")
        print(f"   - Model device: {next(model.parameters()).device}")
        
        # Test tokenizer
        test_text = "summarize: This is a test document for summarization."
        tokens = tokenizer.encode(test_text, return_tensors="pt", max_length=512, truncation=True)
        print(f"   - Tokenizer test: Encoded {len(tokens[0])} tokens")
        
        return True
        
    except Exception as e:
        print(f"[ERROR] Failed to load T5-Small model: {e}")
        return False


def test_distilbert_model():
    """Test DistilBERT model loading"""
    print(f"\n{'='*60}")
    print("Testing DistilBERT Model (Classification)")
    print(f"{'='*60}")
    
    try:
        loader = ModelLoader()
        print("Loading DistilBERT model...")
        print("(First run: Will download ~268 MB from Hugging Face)")
        
        model, tokenizer = loader.load_distilbert_model()
        
        print(f"[SUCCESS] DistilBERT model loaded successfully!")
        print(f"   - Model type: {type(model).__name__}")
        print(f"   - Tokenizer type: {type(tokenizer).__name__}")
        print(f"   - Model device: {next(model.parameters()).device}")
        
        # Test tokenizer
        test_text = "This is a creative brief for a new advertising campaign."
        tokens = tokenizer.encode(test_text, return_tensors="pt", max_length=512, truncation=True)
        print(f"   - Tokenizer test: Encoded {len(tokens[0])} tokens")
        
        return True
        
    except Exception as e:
        print(f"[ERROR] Failed to load DistilBERT model: {e}")
        return False


def test_singleton():
    """Test that ModelLoader is a singleton"""
    print(f"\n{'='*60}")
    print("Testing Singleton Pattern")
    print(f"{'='*60}")
    
    loader1 = ModelLoader()
    loader2 = ModelLoader()
    
    if loader1 is loader2:
        print("[SUCCESS] ModelLoader is a singleton (same instance)")
        return True
    else:
        print("[ERROR] ModelLoader is not a singleton (different instances)")
        return False


def test_lazy_loading():
    """Test that models are loaded lazily"""
    print(f"\n{'='*60}")
    print("Testing Lazy Loading")
    print(f"{'='*60}")
    
    try:
        loader = ModelLoader()
        
        # Access tokenizer first (should trigger model load)
        print("Accessing T5 tokenizer (should trigger model load)...")
        tokenizer = loader.get_t5_tokenizer()
        print(f"[SUCCESS] T5 tokenizer accessed: {type(tokenizer).__name__}")
        
        # Access model (should use already loaded model)
        print("Accessing T5 model (should use cached model)...")
        model = loader.get_t5_model()
        print(f"[SUCCESS] T5 model accessed: {type(model).__name__}")
        
        return True
        
    except Exception as e:
        print(f"[ERROR] Lazy loading test failed: {e}")
        return False


if __name__ == "__main__":
    print("Model Loader Test Script")
    print("=" * 60)
    print("\nThis script will test model loading functionality.")
    print("First run will download models from Hugging Face (~5 min each).")
    print("Subsequent runs will use cached models (much faster).")
    print("\nPress Ctrl+C to cancel if needed.\n")
    
    results = []
    
    # Test singleton pattern
    results.append(("Singleton Pattern", test_singleton()))
    
    # Test lazy loading
    results.append(("Lazy Loading", test_lazy_loading()))
    
    # Test T5 model
    results.append(("T5-Small Model", test_t5_model()))
    
    # Test DistilBERT model
    results.append(("DistilBERT Model", test_distilbert_model()))
    
    # Summary
    print(f"\n{'='*60}")
    print("Test Summary")
    print(f"{'='*60}")
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "PASS" if result else "FAIL"
        print(f"  {status}: {test_name}")
    
    print(f"\nTotal: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n[SUCCESS] All tests passed! Model loader is working correctly.")
    else:
        print("\n[FAIL] Some tests failed. Please check the errors above.")

