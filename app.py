import dash
from dash import dcc
from dash import html
from dash import dash_table
import plotly.express as px
import pandas as pd
from pandas.io.formats import style
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import json

theme = dbc.themes.FLATLY

with open('static/colors.json') as f:
    colors = json.loads(f.read())

# create dataframes
df_scoreboard = pd.read_csv("data/yahoo_fantasy.csv")
df_weekly_averages = pd.read_csv('data/yahoo_weekly_averages.csv')
df_season_totals = pd.read_csv('data/yahoo_season_totals.csv')

# rename columns
df_weekly_averages = df_weekly_averages.rename(
    columns={
        'TEAM_NAME': 'Team',
        'AVG_FG_PERCENT': 'FG%',
        'AVG_FT_PERCENT': 'FT%',
        'AVG_THREES': '3P',
        'AVG_PTS': 'PTS',
        'AVG_REB': 'REB',
        'AVG_AST': 'AST',
        'AVG_STL': 'STL',
        'AVG_BLK': 'BLK',
        'AVG_TO': 'TO'
    }
)

# format percentages
df_weekly_averages['FG%'] = df_weekly_averages['FG%'].multiply(
    100).map('{:,.2f}%'.format)
df_weekly_averages['FT%'] = df_weekly_averages['FT%'].multiply(
    100).map('{:,.2f}%'.format)

# stop plotly from rendering weeks as decimal number on the x-axis
df_scoreboard["WEEK"] = [str(w) for w in df_scoreboard["WEEK"]]

# define categories for the drop downs
categories = ['FGM', 'FGA', 'FG_PERCENT', 'FTM', 'FTA', 'FT_PERCENT',
              'THREES', 'PTS', 'REB', 'AST', 'STL', 'BLK', 'TO']


# instantiate app
app = dash.Dash(external_stylesheets=[theme], meta_tags=[
    {"name": "viewport", "content": "width=device-width, initial-scale=1"},
],
    title='NBA Fanalytics')

application = app.server


# create the html layout
app.layout = html.Div(
    [
        dbc.Nav(
        [
            dbc.NavItem(dbc.NavLink("Active", active=True, href="#")),
            dbc.NavItem(dbc.NavLink("A link", href="#")),
            dbc.NavItem(dbc.NavLink("Another link", href="#")),
            dbc.NavItem(dbc.NavLink("Disabled", disabled=True, href="#")),
            dbc.DropdownMenu(
                [dbc.DropdownMenuItem("Item 1"),
                 dbc.DropdownMenuItem("Item 2")],
                label="Dropdown",
                nav=True,
            ),

        ],
        fill=True,
        card=True,
        pills=True
    ),
        html.H1(
            "NBA Fanalytics"
    ),
        html.Div(
            [
                html.Div(
                    [
                        html.Label("Pick a stat"),
                        dcc.Dropdown(
                            id="category-dropdown",
                            options=[
                                {"label": s, "value": s} for s in categories
                            ],
                            className="dropdown",
                        ),
                    ]
                )
            ],
            className="row",
    ),
        html.Div(dcc.Graph(id="stat-over-time"), className="chart"),
        html.Div([
            html.H4(children='Weekly Category Averages'),
            dash_table.DataTable(
                data=df_weekly_averages.to_dict('records'),
                columns=[{'id': c, 'name': c}
                         for c in df_weekly_averages.columns],
                style_header={
                    'backgroundColor': f"{colors['Gunmetal']}",
                    'color': f"{colors['Burnt Sienna']}",
                    'font-weight': 'bold',
                    'padding': '5px'
                },
                style_data={
                    'backgroundColor': f"{colors['Gunmetal']}",
                    'color': 'white',
                    'padding': '5px',
                    'text-align': 'left'
                },
                sort_action="native",
                sort_mode="multi",
                column_selectable="single",
                page_action="native",
                style_table={'overflowX': 'auto'},
            )
        ])
    ],
    className="container",
)


# callbacks for the dropdown and chart rendering
@app.callback(
    Output("stat-over-time", "figure"),
    # Output("stat-table","figure"),
    Input("category-dropdown", "value")
)
def update_figure(selected_category):

    if selected_category not in categories:
        selected_category = 'PTS'

    fig = px.line(
        df_scoreboard,
        x="WEEK",
        y=f"{selected_category}",
        color="TEAM_NAME",
        markers=True
    )

    # fig.update_layout(
    #     plot_bgcolor=colors["background"],
    #     paper_bgcolor=colors["background"],
    #     font_color=colors["text"],
    # )

    return fig


if __name__ == "__main__":
    app.run_server(debug=True)
