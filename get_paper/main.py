
from datetime import datetime
from .downloader import get_pdf
from .config import papers

def main():
    for paper_config in papers:
        get_pdf(datetime.today(), paper_config)