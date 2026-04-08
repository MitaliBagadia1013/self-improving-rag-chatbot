"""
Main entry point to run the Streamlit application.
This file ensures proper Python path setup.
"""
import sys
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

if __name__ == "__main__":
    import streamlit.web.cli as stcli
    import sys

    # Run Streamlit with the app file
    sys.argv = ["streamlit", "run", "app/ui/streamlit_app.py"]
    sys.exit(stcli.main())
