import os
from pathlib import Path
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='[%(asctime)s] %(levelname)s: %(message)s')

list_of_files = [
    "src/__init__.py",
    "src/helper.py",
    "src/prompt.py",
    ".env",
    "requirements.in",
    "requirements.txt",
    "pyproject.toml",
    "app.py",
    "research/trials.ipynb"
]

def create_files():
    """
    Create a list of files in the current directory.
    """
    for file in list_of_files:
        file_path = Path(file)
        if not file_path.exists():
            file_path.parent.mkdir(parents=True, exist_ok=True)  # Create parent directories if they don't exist
            
            try:
                file_path.touch()
                logging.info(f"Created file: {file}")
            except Exception as e:
                logging.error(f"Failed to create {file}: {e}")

        else:
            logging.info(f"File already exists: {file}")
    logging.info("File creation process completed.")


if __name__ == "__main__":
    create_files()