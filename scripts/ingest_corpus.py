import sys
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from pprint import pprint
from app.core.config import settings
from app.ingestion.pipeline import ingest_corpus


if __name__ == "__main__":
    results = ingest_corpus(str(settings.raw_data_dir))
    pprint(results)