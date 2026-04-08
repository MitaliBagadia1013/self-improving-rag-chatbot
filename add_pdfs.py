#!/usr/bin/env python3
"""
Simple script to add and process new PDFs into the chatbot.

Usage:
    python add_pdfs.py                          # Process all PDFs in data/raw/
    python add_pdfs.py path/to/paper.pdf        # Process a specific PDF
    python add_pdfs.py ~/Downloads/*.pdf        # Process multiple PDFs
"""

import sys
import shutil
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from app.ingestion.pipeline import ingest_single_pdf, ingest_corpus


def main():
    print("🚀 PDF Ingestion Helper")
    print("=" * 50)
    
    # Get PDF paths from command line or use data/raw/
    if len(sys.argv) > 1:
        # User provided specific PDFs
        pdf_paths = sys.argv[1:]
        
        # Copy to data/raw/ first
        raw_dir = project_root / "data" / "raw"
        raw_dir.mkdir(parents=True, exist_ok=True)
        
        for pdf_path in pdf_paths:
            pdf_path = Path(pdf_path)
            if pdf_path.exists() and pdf_path.suffix.lower() == '.pdf':
                dest = raw_dir / pdf_path.name
                print(f"📄 Copying {pdf_path.name} to data/raw/...")
                shutil.copy(pdf_path, dest)
            else:
                print(f"⚠️  Skipping {pdf_path} (not a valid PDF)")
    
    # Process all PDFs in data/raw/
    raw_dir = project_root / "data" / "raw"
    
    print(f"\n📁 Processing PDFs from: {raw_dir}")
    print("-" * 50)
    
    results = ingest_corpus(str(raw_dir))
    
    # Show results
    print("\n" + "=" * 50)
    print("📊 RESULTS:")
    print("=" * 50)
    
    successful = [r for r in results if r.get('status') in ['processed', 'skipped']]
    failed = [r for r in results if r.get('status') == 'failed']
    skipped = [r for r in results if r.get('status') == 'skipped']
    
    print(f"✅ Successfully processed: {len([r for r in results if r.get('status') == 'processed'])}")
    print(f"⏭️  Already existed (skipped): {len(skipped)}")
    print(f"❌ Failed: {len(failed)}")
    
    if skipped:
        print("\n📋 Skipped (already in database):")
        for r in skipped:
            print(f"   - {r.get('title', 'Unknown')}")
    
    if failed:
        print("\n❌ Failed:")
        for r in failed:
            file_name = Path(r.get('file', 'Unknown')).name
            print(f"   - {file_name}: {r.get('error', 'Unknown error')}")
    
    print("\n" + "=" * 50)
    print("🎉 Done! You can now:")
    print("   1. Start the chatbot: streamlit run app/ui/streamlit_app.py")
    print("   2. Or if already running, just refresh the page!")
    print("=" * 50)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)
