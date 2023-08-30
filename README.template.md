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
python -m shelf_control.scraping
```

To use the dashboard:
```bash
python -m shelf_control.dashboard
```
And open [localhost:8050](http://localhost:8050) in a web browser.

## Ideas of things to do

* Scraping data from [Booknode](https://booknode.com)
    * Top 1000 ✓
        * Time: 29min23s
        * Memory: 1,8M
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

{toc}
{docs}