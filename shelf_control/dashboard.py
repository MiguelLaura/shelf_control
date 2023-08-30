# =============================================================================
# Dashboard for top 1000
# =============================================================================
#
from dash import Dash, Input, Output, callback, dash_table, dcc, html
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px

from shelf_control.constants import BOOK_TOP_1000_COLUMNS_DASHBOARD

df_initial = pd.read_csv("data/top_1000.csv")
df_dashtable = pd.DataFrame(df_initial)

df_dashtable["initial_cover"] = df_dashtable["cover"]
df_dashtable["initial_title"] = df_dashtable["title"]
df_dashtable["cover"] = (
    "[!["
    + df_dashtable["title"]
    + "]("
    + df_dashtable["cover"]
    + ")]("
    + df_dashtable["cover"]
    + ")"
)
df_dashtable["title"] = (
    "[" + df_dashtable["title"] + "](" + df_dashtable["book_url"] + ")"
)
df_dashtable.drop("book_url", axis=1, inplace=True)

df_dashtable["dates"] = df_dashtable["dates"].str.replace("|", "\n\n")
df_dashtable["dates_country"] = df_dashtable["dates_country"].str.replace("|", "\n\n")

for elements in ["themes", "authors", "editors", "collections"]:
    df_dashtable[elements] = df_dashtable[elements].apply(lambda x: str(x).split("|"))
    df_dashtable["initial_" + elements] = df_dashtable[elements].apply(
        lambda x: "\n\n".join(x)
    )
    df_dashtable[elements + "_url"] = df_dashtable[elements + "_url"].apply(
        lambda x: str(x).split("|")
    )
    df_dashtable[elements] = df_dashtable.apply(
        lambda x: [
            "[" + element + "](" + element_url + ")"
            for element, element_url in zip(x[elements], x[elements + "_url"])
        ],
        axis=1,
    )
    df_dashtable[elements] = df_dashtable[elements].apply(lambda x: "\n\n".join(x))
    df_dashtable.drop(elements + "_url", axis=1, inplace=True)

df_explode_dates = pd.DataFrame(df_initial)
df_explode_dates["dates"] = df_explode_dates["dates"].apply(lambda x: str(x).split("|"))
df_explode_dates["dates_country"] = df_explode_dates["dates_country"].apply(
    lambda x: str(x).split("|")
)
df_explode_dates = df_explode_dates.explode(["dates", "dates_country"])

df_explode_themes = pd.DataFrame(df_initial)
df_explode_themes["themes"] = df_explode_themes["themes"].apply(
    lambda x: str(x).split("|")
)
df_explode_themes = df_explode_themes.explode("themes")

df_sorted_price = df_initial.sort_values(by="price")

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
            children=dbc.Container(
                [
                    dash_table.DataTable(
                        id="table",
                        data=df_dashtable.to_dict("records"),
                        columns=BOOK_TOP_1000_COLUMNS_DASHBOARD,
                        fixed_rows={"headers": True},
                        page_size=10,
                        css=[
                            {
                                "selector": ".dash-spreadsheet td div",
                                "rule": """
                                display: block;
                                overflow-y: hidden;
                            """,
                            }
                        ],
                        style_cell={
                            "textAlign": "center",
                            "minWidth": 175,
                            "maxWidth": 300,
                            "font-size": "14px",
                            "margin-top": "245px",
                        },
                        style_data={
                            "whiteSpace": "normal",
                            "height": "220px",
                            "lineHeight": "15px",
                        },
                        style_data_conditional=[
                            {
                                "if": {
                                    "column_id": "resume",
                                },
                                "textAlign": "left",
                            },
                        ],
                        style_header={
                            "textAlign": "center",
                            "font-weight": "bold",
                            "font-size": "14px",
                        },
                        style_table={
                            "overflowY": "auto",
                        },
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
                            for row in df_dashtable.to_dict("records")
                        ],
                        tooltip_duration=None,
                    ),
                    dbc.Alert(id="table_out"),
                ]
            ),
            className="spreadsheet",
        ),
        html.Div(
            children=[
                html.Div(
                    children=dcc.Graph(
                        figure=px.histogram(
                            df_explode_themes.groupby("themes")["readers_count"]
                            .sum()
                            .reset_index()
                            .sort_values(by="readers_count", ascending=False)[:10],
                            x="themes",
                            y="readers_count",
                        ),
                    ),
                    className="card",
                ),
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
                ),
            ],
            className="wrapper",
        ),
    ]
)


@callback(Output("table_out", "children"), Input("table", "active_cell"))
def update_graphs(active_cell):
    if active_cell:
        column = (
            "initial_" + active_cell["column_id"]
            if "initial_" + active_cell["column_id"] in df_dashtable.columns
            else active_cell["column_id"]
        )
        return df_dashtable[active_cell["row"] : active_cell["row"] + 1][column]
    else:
        return "Click the table"


if __name__ == "__main__":
    app.run_server(debug=True)
