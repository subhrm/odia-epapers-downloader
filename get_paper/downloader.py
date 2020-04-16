
from datetime import datetime
import requests
import tempfile
from PIL import Image


def get_pdf(date: datetime, paper_config):
    title = paper_config["name"]
    print("="*40)
    print("Down loading {}  for {}".format(title, str(date)[:10]))
    print("="*40)
    dl_date = "{:02d}{:02d}{:4d}".format(date.day, date.month, date.year)
    pages = download_pages(dl_date, paper_config["url_pattern"])

    fname = "{}-{:04d}-{:02d}-{:02d}.pdf".format(title, date.year, date.month, date.day)
    make_pdf(pages, fname)


def download_pages(date_str: str, url_pattern: str) -> [Image.Image]:

    print("Downlading for date ", date_str)

    pages = []
    page_num = 0
    while (True):
        page_num += 1
        url = url_pattern.format(date_str, date_str, page_num)
        try:
            img = get_img(url)
            pages.append(img)
        except Exception as ex:
            print(ex)
            break

    return pages


def get_img(url: str) -> Image.Image:

    resp = requests.get(url)

    if resp.status_code != 200:
        print("Can't dl ", url)
        raise Exception("Can't download")

    print("Dl'd ", url)

    temp_file = tempfile.TemporaryFile()
    temp_file.write(resp.content)
    temp_file.seek(0)
    img = Image.open(temp_file)
    img.load()
    # temp_file.close()

    img = img.convert("RGB")
    print("Converted to Img")
    return img


def make_pdf(pages: [Image.Image], fname: str):

    im1 = pages[0]
    im1.save(fname, save_all=True, append_images=pages[1:], quality=90)
    print("File saved as ", fname)
