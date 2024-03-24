# =============================================================================
# Scraper for top 1000
# =============================================================================
#
import csv
import re
from time import sleep

from bs4 import BeautifulSoup
import requests
from tqdm import tqdm

from shelf_control.constants import BOOK_TOP_1000_FIELDNAMES, CATEGORIES_NAMES

BASE_URL = "https://booknode.com"
NOTES_RE = re.compile(r"Noté \d{0,2}\/10 par (\d+) Booknautes?")
DATES_RE = re.compile(r"\d{4}-\d{2}-\d{2}")


def scraper_top_1000(page_nb=1):
    """
    Generator yielding the info for each book in the top 1000 most liked books on Booknode.

    Args:
        page_nb (int, optional): page number to start from.

    Yields:
        dict: books data
    """
    top_1000_url = BASE_URL + "/decouverte/top-1000-booknode?page="
    position = 1
    for page in tqdm(range(page_nb, 11), desc=" number of pages", position=0):
        url_books = top_1000_url + str(page)
        headers = {"User-Agent": "Mozilla/5.0"}
        res_books = requests.get(url_books, headers=headers)

        if res_books.status_code > 400 and res_books.status_code < 600:
            print("\nstatus_code in top 1000:", res_books.status_code, url_books)
            yield "error"

        soup_books = BeautifulSoup(res_books.text, "html.parser")
        books = soup_books.find_all("div", class_="row book")

        for book in tqdm(
            books,
            desc=" number of books in the page",
            position=1,
            leave=False,
            total=100,
        ):
            url_book = book.find("a", class_="main_cover_link").get("href")
            result = scraper_specific_book(url_book)

            if result == "error":
                yield result

            result["position"] = position
            position += 1
            yield result

        sleep(0.5)


def scraper_specific_book(url_book):
    """
    Function to scrape the info for a specific book on Booknode.

    Args:
        url_book (str): the url of the book on Booknode.

    Returns:
        dict: book data
    """
    headers = {"User-Agent": "Mozilla/5.0"}
    res_book = requests.get(url_book, headers=headers)

    if res_book.status_code > 400 and res_book.status_code < 600:
        print("\nstatus_code in specific book:", res_book, url_book)
        return "error"

    soup_book = BeautifulSoup(res_book.text, "html.parser")

    result = {}

    result["book_url"] = url_book

    result["title"] = soup_book.find("h1", itemprop="name").text

    result["cover"] = (
        soup_book.find("a", class_="main-cover physical-cover")
        .select_one("img")
        .get("src")
    )

    authors_list = [
        " ".join(author.text.split())
        for author in soup_book.find_all("li", itemprop="author")
    ]
    result["authors"] = "|".join(authors_list)
    authors_url_list = [
        author.find("a").get("href")
        for author in soup_book.find_all("li", itemprop="author")
    ]
    result["authors_url"] = "|".join(authors_url_list)

    result["price"] = (
        soup_book.find("span", class_="price").text.replace(" €", "")
        if soup_book.find("span", class_="price")
        else None
    )

    # Number of people who graded the book with the indice+1
    # For example, if the list is
    # ['1', '3', '5', '6', '17', '46', '2', '5', '65', '56']
    # 1 person graded it 1/10, 3 graded it 2/10, etc.
    notes = NOTES_RE.findall(
        soup_book.find("span", class_="detail-global-rating").get("data-content")
    )
    for note in range(10):
        result["count_note_%s" % (note + 1)] = notes[note] if notes else 0

    resume_block = soup_book.find("span", class_="actual-text")
    if resume_block:
        result["resume"] = " ".join(resume_block.text[6:].split())

    # Number of people who put the book in a specific category, in order
    # ['Diamant', 'Or', 'Argent', 'Bronze', 'Lu aussi', 'En train de lire', 'Pas apprécié', 'Envies', 'PAL']
    # For example, if the list is
    # ['2396', '1267', '648', '377', '652', '179', '158', '4449', '1833']
    # 2396 person put it in the Diamant category, 1267 put it in the Or category, etc.
    categories_count_list = [
        readers.text[:-9].replace(" ", "")
        for readers in soup_book.find_all("div", class_="readercount")
    ]
    for nb, category in enumerate(CATEGORIES_NAMES):
        result[category] = categories_count_list[nb]
    result["readers_count"] = sum(int(nb) for nb in categories_count_list[:-2])

    themes_block = soup_book.find("div", class_="col-sm-12 hidden-xs").find(
        "div", class_="panel-body"
    )
    result["themes"] = " ".join(themes_block.text.split()).replace(" - ", "|")
    themes_url_list = [
        theme_url.get("href") for theme_url in themes_block.find_all("a")
    ]
    result["themes_url"] = "|".join(themes_url_list)

    dates_block = soup_book.find_all("div", class_="fm-right-box fm-side-col")
    if len(dates_block) >= 3:
        dates_block = [date.text for date in dates_block[2].find_all("li")]
        dates_list = [DATES_RE.search(date).group(0) for date in dates_block]
        result["dates"] = "|".join(dates_list)
        # Info on country and format
        dates_country_list = [
            " ".join(DATES_RE.sub("", country).split()) for country in dates_block
        ]
        result["dates_country"] = "|".join(dates_country_list)

    editors_collections_block = soup_book.find("h3", string="Editeurs")
    if editors_collections_block:
        editors_collections_block = (
            editors_collections_block.find_parent().find_parent().find_all("li")
        )
        editors_collections_list = [
            editor_collection.find("a").get("title")
            for editor_collection in editors_collections_block
        ]
        editors_collections_url_list = [
            BASE_URL + editor_collection.find("a").get("href")
            for editor_collection in editors_collections_block
        ]

        collections_list = [
            collection
            for collection in editors_collections_list
            if "Collection" in collection
        ]
        collections_url_list = [
            collection
            for collection in editors_collections_url_list
            if "/collection/" in collection
        ]

        editors_list = [
            editor
            for editor in editors_collections_list
            if editor not in collections_list
        ]
        editors_url_list = [
            editor_url
            for editor_url in editors_collections_url_list
            if editor_url not in collections_url_list
        ]
        result["editors"] = "|".join(editors_list)
        result["editors_url"] = "|".join(editors_url_list)
        result["collections"] = "|".join(collections_list)
        result["collections_url"] = "|".join(collections_url_list)

    return result


if __name__ == "__main__":
    # print(scraper_specific_book('https://booknode.com/mens_moi_jusquau_bout_du_monde_03431561'))
    with open("data/top_1000.csv", "w") as f:
        fieldnames = BOOK_TOP_1000_FIELDNAMES
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for result in scraper_top_1000():
            if result == "error":
                break
            writer.writerow(result)
