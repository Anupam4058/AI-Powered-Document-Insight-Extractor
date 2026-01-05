"""
Quick script to check if models are downloaded and cached
"""
import time
from services.model_loader import ModelLoader
from pathlib import Path
import os

def check_cache_size():
    """Check the size of the Hugging Face cache"""
    # Check multiple possible cache locations
    possible_dirs = [
        Path.home() / '.cache' / 'huggingface',
        Path.home() / '.cache' / 'huggingface' / 'transformers',
        Path.home() / '.cache' / 'huggingface' / 'hub',
    ]
    
    # Also check Windows AppData location
    appdata = os.getenv('APPDATA', '')
    if appdata:
        possible_dirs.extend([
            Path(appdata) / '.cache' / 'huggingface',
            Path(appdata) / '.cache' / 'huggingface' / 'transformers',
        ])
    
    total_size = 0
    file_count = 0
    found_dir = None
    
    for cache_dir in possible_dirs:
        if cache_dir.exists():
            found_dir = cache_dir
            for root, dirs, files in os.walk(cache_dir):
                for file in files:
                    file_path = Path(root) / file
                    try:
                        total_size += file_path.stat().st_size
                        file_count += 1
                    except:
                        pass
            break
    
    size_mb = total_size / (1024 * 1024)
    if found_dir:
        return size_mb, f"{file_count} files in {found_dir}"
    else:
        return 0, "Cache directory not found"

def main():
    print("=" * 60)
    print("Model Download Status Check")
    print("=" * 60)
    
    # Check cache
    cache_size, cache_info = check_cache_size()
    print(f"\nHugging Face Cache:")
    print(f"  Size: {cache_size:.2f} MB")
    print(f"  Files: {cache_info}")
    
    if cache_size < 100:
        print("  Status: Models likely NOT downloaded yet")
    elif cache_size < 300:
        print("  Status: One model may be downloaded")
    else:
        print("  Status: Models appear to be downloaded")
    
    # Test loading speed
    print(f"\nTesting Model Load Times:")
    print("-" * 60)
    
    loader = ModelLoader()
    
    # Test T5-Small
    print("Loading T5-Small...")
    start = time.time()
    try:
        t5_model, t5_tokenizer = loader.load_t5_model()
        t5_time = time.time() - start
        print(f"  [OK] Loaded in {t5_time:.2f} seconds")
        if t5_time < 5:
            print(f"  [OK] CACHED (would take ~5 min if downloading)")
        else:
            print(f"  [WARN] May still be downloading...")
    except Exception as e:
        print(f"  [ERROR] Error: {e}")
        t5_time = None
    
    # Test DistilBERT
    print("\nLoading DistilBERT...")
    start = time.time()
    try:
        distil_model, distil_tokenizer = loader.load_distilbert_model()
        distil_time = time.time() - start
        print(f"  [OK] Loaded in {distil_time:.2f} seconds")
        if distil_time < 5:
            print(f"  [OK] CACHED (would take ~5 min if downloading)")
        else:
            print(f"  [WARN] May still be downloading...")
    except Exception as e:
        print(f"  [ERROR] Error: {e}")
        distil_time = None
    
    # Summary
    print(f"\n{'=' * 60}")
    print("Summary:")
    print(f"{'=' * 60}")
    
    if t5_time and t5_time < 5 and distil_time and distil_time < 5:
        print("[SUCCESS] BOTH MODELS ARE DOWNLOADED AND CACHED")
        print("\nYou're all set! Models will load quickly on future runs.")
    elif t5_time and t5_time < 5:
        print("[PARTIAL] T5-Small: Cached")
        print("[PARTIAL] DistilBERT: May still be downloading")
    elif distil_time and distil_time < 5:
        print("[PARTIAL] T5-Small: May still be downloading")
        print("[PARTIAL] DistilBERT: Cached")
    else:
        print("[WARN] Models may still be downloading")
        print("   First download takes ~5 minutes per model")
        print("   Check your internet connection if this persists")

if __name__ == "__main__":
    main()

