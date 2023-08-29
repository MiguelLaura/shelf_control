# =============================================================================
# Dashboard for top 1000
# =============================================================================
#
from dash import Dash, dash_table, dcc, html
import pandas as pd

from constants import BOOK_TOP_1000_COLUMNS_DASHBOARD

df = pd.read_csv("data/top_1000.csv")
df["cover"] = "![" + df["title"] + "](" + df["cover"] + ")"
df["title"] = "[" + df["title"] + "](" + df["book_url"] + ")"
df.drop("book_url", axis=1, inplace=True)

df_sorted_price = df.sort_values(by="price")

external_stylesheets = [
    {
        "href": (
            "https://fonts.googleapis.com/css2?family=Lato:wght@400;700&display=swap"
        ),
        "rel": "stylesheet",
    },
]

app = Dash(__name__, external_stylesheets=external_stylesheets)
app.title = "Books Analytics: Understand Book Trends!"

app.layout = html.Div(
    children=[
        html.Div(
            children=[
                html.P(children="📖", className="header-emoji"),
                html.H1(children="Books Analytics", className="header-title"),
                html.P(
                    children="Analyse books data from Booknode top 1000",
                    className="header-description",
                ),
            ],
            className="header",
        ),
        html.Div(
            children=dash_table.DataTable(
                id="table",
                data=df.to_dict("records"),
                columns=BOOK_TOP_1000_COLUMNS_DASHBOARD,
                fixed_rows={"headers": True},
                page_size=10,
                style_cell={
                    "textAlign": "center",
                    "minWidth": 175,
                    "overflow": "hidden",
                    "textOverflow": "ellipsis",
                    "maxWidth": 300,
                },
                style_data={
                    "whiteSpace": "normal",
                    "height": "220px",
                    "lineHeight": "15px",
                },
                css=[
                    {
                        "selector": ".dash-spreadsheet td div",
                        "rule": """
                            line-height: 15px;
                            height: 220px;
                            display: block;
                            overflow-y: hidden;
                        """,
                    }
                ],
                style_header={
                    "textAlign": "center",
                    "font-weight": "bold",
                    "font-size": "14px",
                },
                style_table={
                    "overflowY": "auto",
                },
                style_data_conditional=[
                    {
                        "if": {
                            "column_id": "resume",
                        },
                        "textAlign": "left",
                    },
                ],
                tooltip_data=[
                    {
                        column: {"value": str(value), "type": "markdown"}
                        for column, value in row.items()
                        if column
                        in [
                            "resume",
                            "editors",
                            "editors_url",
                            "collections",
                            "collections_url",
                        ]
                    }
                    for row in df.to_dict("records")
                ],
                tooltip_duration=None,
            ),
            className="spreadsheet",
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
                                    "x": df_sorted_price["price"],
                                    "y": df_sorted_price["readers_count"],
                                    "type": "lines",
                                    "hovertemplate": ("%{x:.2f}<extra></extra>€"),
                                }
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
