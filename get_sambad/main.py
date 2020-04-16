
from datetime import datetime
from .downloader import get_pdf

def main():
    pages = get_pdf(datetime.today())