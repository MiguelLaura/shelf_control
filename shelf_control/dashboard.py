from dash import Dash, dcc, html
import pandas as pd


data = pd.read_csv("data/top_1000.csv").sort_values(by="price")

external_stylesheets = [
    {
        "href": (
            "https://fonts.googleapis.com/css2?family=Lato:wght@400;700&display=swap"
        ),
        "rel": "stylesheet",
    },
]

app = Dash(__name__, external_stylesheets=external_stylesheets)
app.title = "Books Analytics: Understand Your Books!"

app.layout = html.Div(
    children=[
        html.Div(
            children=[
                html.P(children="📖", className="header-emoji"),
                html.H1(children="Books Analytics", className="header-title"),
                html.P(
                    children="Analyze the number of books readers depending on the price of the book.",
                    className="header-description",
                ),
            ],
            className="header",
        ),
        html.Div(
            children=[
                html.Div(
                    children=dcc.Graph(
                        id="readers-chart",
                        config={"displayModeBar": True, "displaylogo": False},
                        figure={
                            "data": [
                                {
                                    "x": data["price"],
                                    "y": data["readers_count"],
                                    "type": "lines",
                                    "hovertemplate": ("%{x:.2f}<extra></extra>€"),
                                },
                            ],
                            "layout": {
                                "title": {
                                    "text": "Books Readers depending on Price",
                                    "x": 0.05,
                                    "xanchor": "left",
                                },
                                "xaxis": {"ticksuffix": "€", "fixedrange": False},
                                "yaxis": {"fixedrange": False},
                                "colorway": ["#17b897"],
                            },
                        },
                    ),
                    className="card",
                )
            ],
            className="wrapper",
        ),
    ]
)

if __name__ == "__main__":
    app.run_server(debug=True)
