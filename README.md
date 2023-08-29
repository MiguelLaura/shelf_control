# shelf_control

Booknode scraper and analyser (my playground to try things).

## Ideas of things to do

* Scraping data from `https://booknode.com`
    * Top 1000 ✓
        * Time: 14min24s
        * Memory: 1,7M
    * Specific book (✓)
    * Editor
    * Person
    * Author
* Analysing the data
    * Build a dashboard (`http://localhost:8050`) (work in progress)
        * Tutorial: `https://realpython.com/python-dash/#deploy-your-dash-application-to-pythonanywhere`
* Use machine learning to determine the themes of each resume (unsupervised and supervised learning possible)
* Build a recommandation system
* Output a graph of the books using the themes

## Improvements

* Use the progress bar from `minet`
* Build an interface to use the scraping commands
* Add tests when usefull
* Check how to properly stop dash

## Usage

* [scraping](#scraping)
  * [scraper_specific_book](#scraper_specific_book)
  * [scraper_top_1000](#scraper_top_1000)

---

### scraping

#### scraper_specific_book

Function to scrape the info for a specific book on Booknode.

*Arguments*

* **url_book** *str* - the url of the book on Booknode.

*Returns*

*dict* - book data

#### scraper_top_1000

Generator yielding the info for each book in the top 1000 most liked books on Booknode.

*Arguments*

* **page_nb** *int, optional* - page number to start from.

*Yields*

*dict* - books data
