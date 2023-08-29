# shelf_control

Booknode scraper and analyser (my playground to try things).

## Installing, contributioning and using

### Installing
```bash
git clone https://github.com/MiguelLaura/shelf_control.git
make deps
```

### Contributing

#### Changing the README.md

Make changes in [README.template.md](README.template.md) and, to generate the updated [README.md](README.md):
```bash
make readme
```

#### Changing the code

To check if there are any unused imports:
```bash
make lint
```

To format the code using `black`:
```bash
make format
```

Once the changes are done, to lint, format and generate the [README.md](README.md) all at once:
```bash
make
```

### Using

To scrape the top_1000:
```bash
python shelf_books/scraping.py
```

To use the dashboard:
```bash
python shelf_books/dashboard.py
```
And open [localhost:8050](http://localhost:8050) in a web browser.

## Ideas of things to do

* Scraping data from [Booknode](https://booknode.com)
    * Top 1000 ✓
        * Time: 14min24s
        * Memory: 1,7M
    * Specific book (✓)
    * Editor
    * Person
    * Author
* Analysing the data
    * Build a [dashboard](http://localhost:8050) (work in progress)
        * [Tutorial from realpython](https://realpython.com/python-dash/#deploy-your-dash-application-to-pythonanywhere)
        * [Tutorial from dash.plotly](https://dash.plotly.com/tutorial)
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
