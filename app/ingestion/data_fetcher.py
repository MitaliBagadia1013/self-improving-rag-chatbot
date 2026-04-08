"""
Data Fetcher Module - Automatically fetch PDFs from various sources
"""

import requests
import time
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import List, Dict, Optional
import logging
from urllib.parse import urlencode

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DataFetcher:
    def __init__(self, download_dir: str = "data/raw/downloaded_papers"):
        self.download_dir = Path(download_dir)
        self.download_dir.mkdir(parents=True, exist_ok=True)
        logger.info(f"📁 Download directory: {self.download_dir}")
    
    def fetch_from_arxiv(self, search_query: str, max_results: int = 10, category: Optional[str] = None) -> Dict:
        logger.info(f"🔍 Searching arXiv for: '{search_query}' (max {max_results})")
        try:
            base_url = "http://export.arxiv.org/api/query?"
            query = f"cat:{category}+AND+all:{search_query}" if category else f"all:{search_query}"
            params = {'search_query': query, 'start': 0, 'max_results': max_results, 'sortBy': 'relevance', 'sortOrder': 'descending'}
            url = base_url + urlencode(params)
            response = requests.get(url, timeout=30)
            response.raise_for_status()
            root = ET.fromstring(response.content)
            namespace = {'atom': 'http://www.w3.org/2005/Atom'}
            entries = root.findall('atom:entry', namespace)
            logger.info(f"✅ Found {len(entries)} papers")
            downloaded_files, failed_downloads = [], []
            for i, entry in enumerate(entries, 1):
                try:
                    title = entry.find('atom:title', namespace).text.strip().replace('\n', ' ')
                    pdf_link = None
                    for link in entry.findall('atom:link', namespace):
                        if link.get('title') == 'pdf':
                            pdf_link = link.get('href')
                            break
                    if not pdf_link:
                        failed_downloads.append({'title': title, 'reason': 'No PDF link'})
                        continue
                    safe_title = "".join(c for c in title if c.isalnum() or c in (' ', '-', '_'))[:100]
                    filename = f"arxiv_{i}_{safe_title}.pdf"
                    filepath = self.download_dir / filename
                    logger.info(f"⬇️ [{i}/{len(entries)}] {title[:60]}...")
                    if self._download_pdf(pdf_link, filepath):
                        downloaded_files.append(str(filepath))
                    else:
                        failed_downloads.append({'title': title, 'reason': 'Download failed'})
                    time.sleep(3)
                except Exception as e:
                    failed_downloads.append({'title': 'Unknown', 'reason': str(e)})
            return {'success': True, 'source': 'arxiv', 'query': search_query, 'downloaded_files': downloaded_files, 'failed': failed_downloads, 'total': len(downloaded_files), 'failed_count': len(failed_downloads)}
        except Exception as e:
            logger.error(f"❌ arXiv failed: {e}")
            return {'success': False, 'source': 'arxiv', 'error': str(e), 'downloaded_files': [], 'failed': [], 'total': 0}
    
    def fetch_from_urls(self, urls: List[str]) -> Dict:
        downloaded_files, failed_downloads = [], []
        for i, url in enumerate(urls, 1):
            try:
                filename = url.split('/')[-1] if url.endswith('.pdf') else f"url_{i}.pdf"
                filepath = self.download_dir / filename
                if self._download_pdf(url, filepath):
                    downloaded_files.append(str(filepath))
                else:
                    failed_downloads.append({'url': url, 'reason': 'Failed'})
                time.sleep(1)
            except Exception as e:
                failed_downloads.append({'url': url, 'reason': str(e)})
        return {'success': len(downloaded_files) > 0, 'source': 'direct_urls', 'downloaded_files': downloaded_files, 'failed': failed_downloads, 'total': len(downloaded_files), 'failed_count': len(failed_downloads)}
    
    def _download_pdf(self, url: str, filepath: Path) -> bool:
        try:
            response = requests.get(url, timeout=60, stream=True)
            response.raise_for_status()
            with open(filepath, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
            return filepath.exists() and filepath.stat().st_size > 0
        except:
            return False
    
    def get_new_pdfs_from_folder(self, folder_path: str) -> List[str]:
        folder = Path(folder_path)
        if not folder.exists():
            return []
        pdf_files = list(folder.glob("*.pdf")) + list(folder.glob("*.PDF"))
        return [str(f) for f in pdf_files]
