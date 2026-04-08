"""
Document Manager UI - User-friendly interface for fetching and managing PDFs

This is the "control panel" where users can:
1. Fetch papers from arXiv
2. Download from URLs
3. View downloaded documents
4. Process documents into the system

Think of this as the "dashboard" for your document library!
"""

import sys
from pathlib import Path

# Add project root to Python path (so we can import our modules)
project_root = Path(__file__).parent.parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

import streamlit as st
from app.ingestion.data_fetcher import DataFetcher
from app.ingestion.pipeline import IngestionPipeline
import time


def render_document_manager():
    """
    Main function that renders the Document Manager interface.
    
    This creates the entire UI with tabs for different data sources.
    """
    
    # ========================================
    # HEADER
    # ========================================
    st.title("📥 Document Manager")
    st.markdown("""
    Automatically fetch and process PDFs from various sources. No more manual downloads! 🚀
    """)
    st.markdown("---")
    
    # ========================================
    # INITIALIZE COMPONENTS
    # ========================================
    
    # Create DataFetcher instance (the brain that fetches PDFs)
    fetcher = DataFetcher()
    
    # Create IngestionPipeline instance (processes PDFs into the system)
    pipeline = IngestionPipeline()
    
    
    # ========================================
    # TABS FOR DIFFERENT SOURCES
    # ========================================
    
    # Create 4 tabs for different data sources
    tab1, tab2, tab3, tab4 = st.tabs([
        "🔬 arXiv Papers",      # Scientific papers
        "🔗 Direct URLs",       # Download from links
        "📁 Folder Upload",     # Bulk upload
        "📊 View Documents"     # See what's downloaded
    ])
    
    
    # ========================================
    # TAB 1: ARXIV PAPERS
    # ========================================
    
    with tab1:
        st.subheader("🔬 Fetch Papers from arXiv")
        st.markdown("""
        **arXiv** is a free repository of scientific papers (computer science, physics, math, etc.)
        
        **Example searches:**
        - "retrieval augmented generation"
        - "transformers attention mechanism"
        - "BERT language model"
        - "neural networks"
        """)
        
        # Create two columns for layout
        col1, col2 = st.columns([2, 1])
        
        with col1:
            # Input: What to search for
            search_query = st.text_input(
                "🔍 Search Query",
                placeholder="e.g., retrieval augmented generation",
                help="Enter keywords to search for papers"
            )
        
        with col2:
            # Input: How many papers to fetch
            max_results = st.number_input(
                "📊 Max Results",
                min_value=1,
                max_value=100,
                value=10,
                help="How many papers to download (1-100)"
            )
        
        # Optional: Category filter
        category = st.selectbox(
            "📂 Category (Optional)",
            options=[
                "All Categories",
                "cs.AI - Artificial Intelligence",
                "cs.CL - Computation and Language",
                "cs.LG - Machine Learning",
                "cs.CV - Computer Vision",
                "cs.IR - Information Retrieval"
            ]
        )
        
        # Extract category code (e.g., "cs.AI")
        category_code = None if category == "All Categories" else category.split(" - ")[0]
        
        # Checkbox: Auto-process after download
        auto_process = st.checkbox(
            "✅ Automatically process after download",
            value=True,
            help="If checked, PDFs will be chunked, embedded, and stored in Qdrant automatically"
        )
        
        st.markdown("---")
        
        # FETCH BUTTON
        if st.button("🚀 Fetch & Process", type="primary", key="arxiv_fetch"):
            if not search_query:
                st.error("❌ Please enter a search query!")
            else:
                # Show what we're doing
                st.info(f"🔍 Searching arXiv for: **{search_query}** (max {max_results} results)")
                
                # Create progress bar
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                # STEP 1: Fetch PDFs
                status_text.text("⬇️ Downloading papers from arXiv...")
                progress_bar.progress(20)
                
                result = fetcher.fetch_from_arxiv(
                    search_query=search_query,
                    max_results=max_results,
                    category=category_code
                )
                
                progress_bar.progress(50)
                
                # Show results
                if result['success'] and result['total'] > 0:
                    st.success(f"✅ Successfully downloaded {result['total']} papers!")
                    
                    # Show downloaded files
                    with st.expander("📄 Downloaded Files"):
                        for i, filepath in enumerate(result['downloaded_files'], 1):
                            filename = Path(filepath).name
                            st.write(f"{i}. {filename}")
                    
                    # Show failed downloads if any
                    if result['failed_count'] > 0:
                        with st.expander(f"⚠️ Failed Downloads ({result['failed_count']})"):
                            for failed in result['failed']:
                                st.write(f"- {failed.get('title', 'Unknown')}: {failed.get('reason', 'Unknown error')}")
                    
                    # STEP 2: Auto-process if enabled
                    if auto_process and result['downloaded_files']:
                        status_text.text("🔄 Processing documents (chunking, embedding, storing)...")
                        progress_bar.progress(70)
                        
                        # Process each downloaded file
                        for filepath in result['downloaded_files']:
                            try:
                                pipeline.process_pdf(filepath)
                            except Exception as e:
                                st.warning(f"⚠️ Error processing {Path(filepath).name}: {e}")
                        
                        progress_bar.progress(100)
                        status_text.text("✅ All done!")
                        st.success("🎉 Documents downloaded and processed successfully!")
                    else:
                        progress_bar.progress(100)
                        status_text.text("✅ Download complete!")
                        st.info("ℹ️ Documents downloaded but not processed. Enable auto-process or use the ingestion script.")
                
                else:
                    st.error(f"❌ Failed to fetch papers: {result.get('error', 'Unknown error')}")
                    progress_bar.progress(0)
    
    
    # ========================================
    # TAB 2: DIRECT URLS
    # ========================================
    
    with tab2:
        st.subheader("🔗 Download from Direct URLs")
        st.markdown("""
        Paste PDF URLs (one per line) to download them all at once.
        
        **Example URLs:**
        ```
        https://arxiv.org/pdf/1706.03762.pdf
        https://arxiv.org/pdf/2005.11401.pdf
        https://arxiv.org/pdf/1810.04805.pdf
        ```
        """)
        
        # Text area for URLs (one per line)
        urls_input = st.text_area(
            "📋 PDF URLs (one per line)",
            height=200,
            placeholder="https://example.com/paper1.pdf\nhttps://example.com/paper2.pdf\n...",
            help="Paste PDF URLs, one per line"
        )
        
        # Auto-process checkbox
        auto_process_urls = st.checkbox(
            "✅ Automatically process after download",
            value=True,
            key="auto_process_urls",
            help="If checked, PDFs will be chunked, embedded, and stored in Qdrant automatically"
        )
        
        st.markdown("---")
        
        # DOWNLOAD BUTTON
        if st.button("⬇️ Download All", type="primary", key="url_download"):
            # Parse URLs (split by newlines and filter empty lines)
            urls = [url.strip() for url in urls_input.split('\n') if url.strip()]
            
            if not urls:
                st.error("❌ Please enter at least one URL!")
            else:
                st.info(f"⬇️ Downloading {len(urls)} PDFs...")
                
                # Create progress bar
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                # STEP 1: Download PDFs
                status_text.text(f"⬇️ Downloading {len(urls)} PDFs from URLs...")
                
                result = fetcher.fetch_from_urls(urls)
                
                progress_bar.progress(50)
                
                # Show results
                if result['total'] > 0:
                    st.success(f"✅ Successfully downloaded {result['total']} PDFs!")
                    
                    # Show downloaded files
                    with st.expander("📄 Downloaded Files"):
                        for i, filepath in enumerate(result['downloaded_files'], 1):
                            filename = Path(filepath).name
                            st.write(f"{i}. {filename}")
                    
                    # Show failed downloads if any
                    if result['failed_count'] > 0:
                        with st.expander(f"⚠️ Failed Downloads ({result['failed_count']})"):
                            for failed in result['failed']:
                                st.write(f"- {failed.get('url', 'Unknown')}: {failed.get('reason', 'Unknown error')}")
                    
                    # STEP 2: Auto-process if enabled
                    if auto_process_urls and result['downloaded_files']:
                        status_text.text("🔄 Processing documents...")
                        progress_bar.progress(70)
                        
                        for filepath in result['downloaded_files']:
                            try:
                                pipeline.process_pdf(filepath)
                            except Exception as e:
                                st.warning(f"⚠️ Error processing {Path(filepath).name}: {e}")
                        
                        progress_bar.progress(100)
                        status_text.text("✅ All done!")
                        st.success("🎉 Documents downloaded and processed successfully!")
                    else:
                        progress_bar.progress(100)
                        status_text.text("✅ Download complete!")
                
                else:
                    st.error("❌ All downloads failed!")
                    progress_bar.progress(0)
    
    
    # ========================================
    # TAB 3: FOLDER UPLOAD
    # ========================================
    
    with tab3:
        st.subheader("📁 Bulk Upload from Folder")
        st.markdown("""
        **Two options for bulk uploads:**
        
        1. **Manual Upload:** Use the file uploader below (good for small batches)
        2. **Folder Monitoring:** Drop PDFs in `data/raw/inbox/` and they'll be detected
        """)
        
        # Option 1: File uploader (Streamlit's built-in component)
        st.markdown("### Option 1: Upload Files")
        uploaded_files = st.file_uploader(
            "Choose PDF files",
            type=['pdf'],
            accept_multiple_files=True,
            help="Select one or more PDF files to upload"
        )
        
        if uploaded_files:
            st.info(f"📄 {len(uploaded_files)} files selected")
            
            if st.button("📤 Upload & Process", type="primary", key="upload_files"):
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                uploaded_paths = []
                
                # Save each uploaded file
                for i, uploaded_file in enumerate(uploaded_files):
                    # Save to download directory
                    filepath = fetcher.download_dir / uploaded_file.name
                    
                    with open(filepath, 'wb') as f:
                        f.write(uploaded_file.getbuffer())
                    
                    uploaded_paths.append(str(filepath))
                    
                    progress = int((i + 1) / len(uploaded_files) * 50)
                    progress_bar.progress(progress)
                    status_text.text(f"📤 Uploading {i + 1}/{len(uploaded_files)}...")
                
                st.success(f"✅ Uploaded {len(uploaded_paths)} files!")
                
                # Process files
                status_text.text("🔄 Processing documents...")
                for i, filepath in enumerate(uploaded_paths):
                    try:
                        pipeline.process_pdf(filepath)
                        progress = 50 + int((i + 1) / len(uploaded_paths) * 50)
                        progress_bar.progress(progress)
                    except Exception as e:
                        st.warning(f"⚠️ Error processing {Path(filepath).name}: {e}")
                
                progress_bar.progress(100)
                status_text.text("✅ All done!")
                st.success("🎉 Files uploaded and processed!")
        
        st.markdown("---")
        
        # Option 2: Folder monitoring
        st.markdown("### Option 2: Monitor Folder")
        
        inbox_folder = "data/raw/inbox"
        inbox_path = Path(inbox_folder)
        
        # Create inbox folder if it doesn't exist
        inbox_path.mkdir(parents=True, exist_ok=True)
        
        st.info(f"📁 Drop PDFs in: `{inbox_folder}/`")
        
        if st.button("🔍 Scan Inbox Folder", key="scan_inbox"):
            pdf_files = fetcher.get_new_pdfs_from_folder(inbox_folder)
            
            if pdf_files:
                st.success(f"✅ Found {len(pdf_files)} PDFs in inbox!")
                
                with st.expander("📄 Files Found"):
                    for i, filepath in enumerate(pdf_files, 1):
                        filename = Path(filepath).name
                        st.write(f"{i}. {filename}")
                
                if st.button("🔄 Process All", key="process_inbox"):
                    progress_bar = st.progress(0)
                    status_text = st.empty()
                    
                    for i, filepath in enumerate(pdf_files):
                        try:
                            status_text.text(f"🔄 Processing {i + 1}/{len(pdf_files)}...")
                            pipeline.process_pdf(filepath)
                            progress = int((i + 1) / len(pdf_files) * 100)
                            progress_bar.progress(progress)
                        except Exception as e:
                            st.warning(f"⚠️ Error processing {Path(filepath).name}: {e}")
                    
                    status_text.text("✅ All done!")
                    st.success("🎉 All files processed!")
            else:
                st.info(f"📭 No PDFs found in `{inbox_folder}/`")
    
    
    # ========================================
    # TAB 4: VIEW DOCUMENTS
    # ========================================
    
    with tab4:
        st.subheader("📊 Downloaded Documents")
        st.markdown("View all documents in the download directory.")
        
        # Get list of downloaded PDFs
        download_dir = Path("data/raw/downloaded_papers")
        
        if download_dir.exists():
            pdf_files = list(download_dir.glob("*.pdf"))
            
            if pdf_files:
                st.success(f"📚 Found {len(pdf_files)} documents")
                
                # Display as a table
                import pandas as pd
                
                # Create dataframe with file info
                file_data = []
                for pdf_file in pdf_files:
                    file_data.append({
                        "Filename": pdf_file.name,
                        "Size (KB)": f"{pdf_file.stat().st_size / 1024:.1f}",
                        "Modified": pd.to_datetime(pdf_file.stat().st_mtime, unit='s').strftime('%Y-%m-%d %H:%M')
                    })
                
                df = pd.DataFrame(file_data)
                st.dataframe(df, use_container_width=True)
                
                # Option to clear all downloads
                st.markdown("---")
                
                if st.button("🗑️ Clear All Downloads", type="secondary"):
                    if st.checkbox("⚠️ Are you sure? This cannot be undone!"):
                        for pdf_file in pdf_files:
                            pdf_file.unlink()
                        st.success("✅ All downloads cleared!")
                        st.rerun()
            
            else:
                st.info("📭 No documents downloaded yet. Use the tabs above to fetch papers!")
        
        else:
            st.info("📁 Download directory not found. It will be created when you fetch your first document.")
    
    
    # ========================================
    # FOOTER
    # ========================================
    st.markdown("---")
    st.caption("""
    💡 **Tips:**
    - arXiv papers are always free and open access
    - Use specific keywords for better search results
    - Enable auto-process to save time
    - Check the Analytics dashboard to see your document count
    """)


# ========================================
# RUN THE UI
# ========================================

if __name__ == "__main__":
    """
    This runs when file is executed directly.
    For testing the UI component.
    """
    render_document_manager()
