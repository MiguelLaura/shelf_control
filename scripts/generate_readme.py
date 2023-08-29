# =============================================================================
# Script to generate README
# =============================================================================
#
from shelf_control.scraping import scraper_specific_book, scraper_top_1000
from docdocdoc.build import generate_readme


DOCS = [
    {
        "title": "scraping",
        "fns": [
            scraper_specific_book,
            scraper_top_1000,
        ],
    }
]

generate_readme(DOCS)
