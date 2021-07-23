
import dash
import pandas as pd
import plotly.express as px
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from jupyter_dash import JupyterDash
import plotly.graph_objects as go
import json
from urllib.request import urlopen



df2012 = pd.read_csv('https://raw.githubusercontent.com/JulianMay97/tables/7e125507341f7f2d6d0e1aa8f1ebfe6937d76122/2012.csv')
df2019 = pd.read_csv('https://raw.githubusercontent.com/JulianMay97/tables/7e125507341f7f2d6d0e1aa8f1ebfe6937d76122/2019%20(1).csv')
df2020 = pd.read_csv('https://raw.githubusercontent.com/JulianMay97/tables/7e125507341f7f2d6d0e1aa8f1ebfe6937d76122/2020.csv')
df2012z = pd.read_csv('https://raw.githubusercontent.com/JulianMay97/tables/7e125507341f7f2d6d0e1aa8f1ebfe6937d76122/2012z.csv')
df2019z = pd.read_csv('https://raw.githubusercontent.com/JulianMay97/tables/7e125507341f7f2d6d0e1aa8f1ebfe6937d76122/2019z.csv')
df2012 = df2012.dropna()
df2019 = df2019.dropna()
df2020 = df2020.dropna()
df2012z = df2012z.dropna()
df2019z = df2019z.dropna()
df2012 = df2012.rename(columns={'2012': 'categ'})
df2019 = df2019.rename(columns={'2019': 'categ'})
df2020 = df2020.rename(columns={'2020': 'categ'})
df2012z = df2012z.rename(columns={'2012z': 'categ2'})
df2019z = df2019z.rename(columns={'2019z': 'categ2'})
frames = [df2012, df2019, df2020]
df = pd.concat(frames, keys=["2012", "2019", "2020"])
frames2 = [df2012z, df2019z]
df2 = pd.concat(frames2, keys=["2012", "2019"])
#jsonurl = urlopen("https://raw.githubusercontent.com/JulianMay97/tables/7e125507341f7f2d6d0e1aa8f1ebfe6937d76122/3_mittel.geo.json")
#geojson = json.loads(jsonurl.read())

with urlopen('https://raw.githubusercontent.com/JulianMay97/tables/7e125507341f7f2d6d0e1aa8f1ebfe6937d76122/3_mittel.geo.json') as response:
  geojson = json.load(response)

app = JupyterDash(__name__, external_stylesheets=[dbc.themes.GRID, dbc.themes.BOOTSTRAP])
server = app.server


# Function fot the 2 small displays
def updateCards(year, state, df, typecateg):
    if year and state:
        try:
            dfCards = df.loc[year, ['categ', state]]
            dfCards = dfCards[dfCards['categ'] == typecateg].drop('categ', axis=1)
            result = dfCards.dropna(axis=1).astype(int).sum(axis=1)
            result = result.tolist()[0]
        except:
            result = 0
    elif year and not state:
        try:
            dfCards = df.loc[year, :]
            dfCards = dfCards[dfCards['categ'] == typecateg].drop('categ', axis=1)
            result = dfCards.dropna(axis=1).astype(int).sum(axis=1)
            result = result.tolist()[0]
        except:
            result = 0
    elif not year and state:
        try:
            dfCards = df[['categ', state]]
            dfCards = dfCards[dfCards['categ'] == typecateg].drop('categ', axis=1)
            result = dfCards.dropna(axis=1).astype(int).sum(axis=0)
            result = result.tolist()[0]
        except:
            result = 0
    else:
        try:
            dfCards = df.loc[:, :]
            dfCards = dfCards[dfCards['categ'] == typecateg].drop('categ', axis=1)
            result = dfCards.dropna(axis=1).astype(int).sum(axis=1)
            result = sum(result.tolist())
        except:
            result = 0
    return result


# Dropdown Selections
YearDropdown = [
    html.Div([
        dcc.Dropdown(
            id='year-dropdown',
            placeholder="Select a year",
            options=[
                {'label': '2012', 'value': '2012'},
                {'label': '2019', 'value': '2019'},
                {'label': '2020', 'value': '2020'},
            ], ),
    ],
        style={"width": "90%", "padding-left": 0},
    ),
]

StateDropdown = [
    html.Div([
        dcc.Dropdown(
            id='state-dropdown',
            placeholder="Select a state",
            options=[
                {'label': 'Baden Württemberg', 'value': 'Baden Württemberg'},
                {'label': 'Bayern', 'value': 'Bayern'},
                {'label': 'Berlin', 'value': 'Berlin'},
                {'label': 'Brandenburg', 'value': 'Brandenburg'},
                {'label': 'Bremen', 'value': 'Bremen'},
                {'label': 'Hamburg', 'value': 'Hamburg'},
                {'label': 'Hessen', 'value': 'Hessen'},
                {'label': 'Mecklenburg-Vorpommern', 'value': 'Mecklenburg-Vorpommern'},
                {'label': 'Niedersachsen', 'value': 'Niedersachsen'},
                {'label': 'Nordrhein Westpfalen', 'value': 'Nordrhein Westpfalen'},
                {'label': 'Rheinland-Pfalz', 'value': 'Rheinland-Pfalz'},
                {'label': 'Saarland', 'value': 'Saarland'},
                {'label': 'Sachsen', 'value': 'Sachsen'},
                {'label': 'Sachsen-Anhalt', 'value': 'Sachsen-Anhalt'},
                {'label': 'Schleswig-Holstein', 'value': 'Schleswig-Holstein'},
                {'label': 'Thüringen', 'value': 'Thüringen'},
            ],
        ),
    ],
        style={"width": "90%", "padding-left": 0},
    ),
]

# Positioning with Columns and Rows
app.layout = html.Div(
    [
        dbc.Row(
            [
                dbc.Col(
                    [
                        dbc.Row(
                            [dbc.Col(StateDropdown, md=6),
                             dbc.Col(YearDropdown, md=6)], style={'margin-left': 5, 'padding-bottom': 30}),
                        # dbc.Row(YearDropdown)
                        dbc.Row(dcc.Graph(id="map", style={'margin-left': 30}), ),
                    ], width=4
                ),

                dbc.Col(
                    [
                        dbc.Row(
                            [
                                # dbc.Col(html.H4(id='selected'), style={"text-align": "center"}),
                            ]
                        ),

                        dbc.Row(
                            [dbc.Col(dcc.Graph(id='student-per-year'), md=4),
                             dbc.Col(dcc.Graph(id='student-first-year'), md=4),
                             dbc.Col(id='supervisionratio', md=4),
                             # dbc.Col(id='studentsperinstitution', md=2)
                             ], style={'margin-top': 10}
                        ),

                        dbc.Row(
                            [dbc.Col(),
                             dbc.Col(),
                             dbc.Col(dbc.Col(id='studentsperinstitution', md=13))
                             ], style={'margin-top': -150, 'margin-bottom': 50}
                        ),

                        dbc.Row(
                            [dbc.Col(dcc.Graph(id='barGraph'), md=6),
                             dbc.Col(dcc.Graph(id='barGraph3'), md=6),
                             ], style={'margin-top': 10}
                        ),

                        dbc.Row(
                            [dbc.Col(dcc.Graph(id='pieChart'), md=3),
                             dbc.Col(dcc.Graph(id='pieChart2'), md=3),
                             dbc.Col(dcc.Graph(id='barGraph2'), md=4),
                             ], style={'margin-top': 10}
                        ),

                    ], width=8
                ),
            ], no_gutters=True,
            justify="around",
        )
    ], style={'backgroundColor': "#DCDCDC", 'padding-top': 30, },  # Or whatever number suits your needs
)


# Amount of students
@app.callback(
    dash.dependencies.Output('student-per-year', 'figure'),
    [dash.dependencies.Input('year-dropdown', 'value'),
     dash.dependencies.Input('state-dropdown', 'value'),
     ])
def update_confirmed(year, state):
    dfbar = df.copy()
    for i in dfbar.index:
        if "female" not in dfbar.loc[i, 'categ']:
            x = dfbar.loc[i, 'categ']
            dfbar.loc[i, 'Gender'] = 'all'
        elif dfbar.loc[i, 'categ'] == "female":
            dfbar.loc[i, 'Gender'] = 'female'
            dfbar.loc[i, 'categ'] = dfbar.loc[i, 'categ'] + " " + x
    dfbar = dfbar[dfbar['categ'].isin([
        'students 2012', 'female students 2012', 'students 2019', 'female students 2019', 'students 2020',
        'female students 2020'

    ])]
    dfbar.reset_index(inplace=True)

    if year and state:
        dfbar = dfbar[dfbar['level_0'] == year]
        dfbar = dfbar[['level_0', "level_1", 'categ', 'Gender', state]]
        dfbar.drop('level_1', inplace=True, axis=1)
        dfbar = dfbar.set_index(['level_0', 'categ', 'Gender']).fillna(0)
        dfbar = dfbar.astype(int).sum(axis=1)
        dfbar = dfbar.to_frame()
        dfbar.reset_index(inplace=True)
    elif year and not state:
        dfbar = dfbar[dfbar['level_0'] == year]
        dfbar.drop('level_1', inplace=True, axis=1)
        dfbar = dfbar.set_index(['level_0', 'categ', 'Gender']).fillna(0)
        dfbar = dfbar.astype(int).sum(axis=1)
        dfbar = dfbar.to_frame()
        dfbar.reset_index(inplace=True)
    elif not year and state:
        dfbar = dfbar[['level_0', "level_1", 'categ', 'Gender', state]]
        print(dfbar)
        dfbar.drop('level_1', inplace=True, axis=1)
        # dfbar.drop('level_2', inplace=True, axis=2)
        dfbar = dfbar.set_index(['level_0', 'categ', 'Gender']).fillna(0)
        dfbar = dfbar.astype(int).sum(axis=1)
        dfbar = dfbar.to_frame()
        dfbar.reset_index(inplace=True)

    else:
        dfbar = df.copy()
        for i in dfbar.index:
            if "female" not in dfbar.loc[i, 'categ']:
                x = dfbar.loc[i, 'categ']
                dfbar.loc[i, 'Gender'] = 'all'
            elif dfbar.loc[i, 'categ'] == "female":
                dfbar.loc[i, 'Gender'] = 'female'
                dfbar.loc[i, 'categ'] = dfbar.loc[i, 'categ'] + " " + x
        dfbar = dfbar[dfbar['categ'].isin([
            'students 2012', 'female students 2012', 'students 2019', 'female students 2019', 'students 2020',
            'female students 2020'
        ])]

        dfbar.fillna(0, inplace=True)
        dfbar[['Baden Württemberg', 'Bayern', 'Berlin', 'Brandenburg',
               'Bremen', 'Hamburg', 'Hessen', 'Mecklenburg-Vorpommern',
               'Niedersachsen', 'Nordrhein Westpfalen', 'Rheinland-Pfalz', 'Saarland',
               'Sachsen', 'Sachsen-Anhalt', 'Schleswig-Holstein', 'Thüringen']] = dfbar[
            ['Baden Württemberg', 'Bayern', 'Berlin', 'Brandenburg',
             'Bremen', 'Hamburg', 'Hessen', 'Mecklenburg-Vorpommern',
             'Niedersachsen', 'Nordrhein Westpfalen', 'Rheinland-Pfalz', 'Saarland',
             'Sachsen', 'Sachsen-Anhalt', 'Schleswig-Holstein', 'Thüringen']].astype(int)

        dfbar = dfbar.groupby(['categ', 'Gender']).sum().sum(axis=1).to_frame()
        dfbar.reset_index(inplace=True)

    Subjects = ['2012', '2019', '2020']

    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=Subjects,
        y=dfbar[dfbar['Gender'] == 'all'].iloc[:, -1].values,
        name='Total',
        text=dfbar[dfbar['Gender'] == 'all'].iloc[:, -1].values,
        textposition='auto',
        texttemplate='%{text:.2s}',
        marker_color='rgb(55, 83, 109)'
    ))
    fig.add_trace(go.Bar(
        x=Subjects,
        y=dfbar[dfbar['Gender'] == 'female'].iloc[:, -1].values,
        name='female',
        text=dfbar[dfbar['Gender'] == 'female'].iloc[:, -1].values,
        textposition='auto',
        texttemplate='%{text:.2s}',
        marker_color='rgb(26, 118, 255)'
    ))

    # Here we modify the tickangle of the xaxis, resulting in rotated labels.
    # fig.update_layout(barmode='group', xaxis_tickangle=-45)
    fig.update_layout(
        title='Anzahl der Studenten pro Jahr',
        xaxis_tickfont_size=11,
        yaxis=dict(
            title='Amount',
            titlefont_size=12,
            tickfont_size=11,
        ),
        legend=dict(
            x=0,
            y=1.0,
            bgcolor='rgba(255, 255, 255, 0)',
            bordercolor='rgba(255, 255, 255, 0)'
        ),
        showlegend=False,
        barmode='group',
        bargap=0.15,  # gap between bars of adjacent location coordinates.
        bargroupgap=0.1,  # gap between bars of the same location coordinate.
        width=350,
        height=300
    )

    return fig


# Amount of Students in the first year
@app.callback(
    dash.dependencies.Output('student-first-year', 'figure'),
    [dash.dependencies.Input('year-dropdown', 'value'),
     dash.dependencies.Input('state-dropdown', 'value'),
     ])
def update_confirmed(year, state):
    dfbar = df.copy()
    for i in dfbar.index:
        if "female" not in dfbar.loc[i, 'categ']:
            x = dfbar.loc[i, 'categ']
            dfbar.loc[i, 'Gender'] = 'all'
        elif dfbar.loc[i, 'categ'] == "female":
            dfbar.loc[i, 'Gender'] = 'female'
            dfbar.loc[i, 'categ'] = dfbar.loc[i, 'categ'] + " " + x
    dfbar = dfbar[dfbar['categ'].isin([
        '1.year 2012', 'female 1.year 2012', '1.year 2019', 'female 1.year 2019', '1.year 2020', 'female 1.year 2020'

    ])]
    dfbar.reset_index(inplace=True)

    if year and state:
        dfbar = dfbar[dfbar['level_0'] == year]
        dfbar = dfbar[['level_0', "level_1", 'categ', 'Gender', state]]
        dfbar.drop('level_1', inplace=True, axis=1)
        dfbar = dfbar.set_index(['level_0', 'categ', 'Gender']).fillna(0)
        dfbar = dfbar.astype(int).sum(axis=1)
        dfbar = dfbar.to_frame()
        dfbar.reset_index(inplace=True)
    elif year and not state:
        dfbar = dfbar[dfbar['level_0'] == year]
        dfbar.drop('level_1', inplace=True, axis=1)
        dfbar = dfbar.set_index(['level_0', 'categ', 'Gender']).fillna(0)
        dfbar = dfbar.astype(int).sum(axis=1)
        dfbar = dfbar.to_frame()
        dfbar.reset_index(inplace=True)
    elif not year and state:
        dfbar = dfbar[['level_0', "level_1", 'categ', 'Gender', state]]
        dfbar.drop('level_1', inplace=True, axis=1)
        dfbar = dfbar.set_index(['level_0', 'categ', 'Gender']).fillna(0)
        dfbar = dfbar.astype(int).sum(axis=1)
        dfbar = dfbar.to_frame()
        dfbar.reset_index(inplace=True)

    else:
        dfbar = df.copy()
        for i in dfbar.index:
            if "female" not in dfbar.loc[i, 'categ']:
                x = dfbar.loc[i, 'categ']
                dfbar.loc[i, 'Gender'] = 'all'
            elif dfbar.loc[i, 'categ'] == "female":
                dfbar.loc[i, 'Gender'] = 'female'
                dfbar.loc[i, 'categ'] = dfbar.loc[i, 'categ'] + " " + x
        dfbar = dfbar[dfbar['categ'].isin([
            '1.year 2012', 'female 1.year 2012', '1.year 2019', 'female 1.year 2019', '1.year 2020',
            'female 1.year 2020'
        ])]

        dfbar.fillna(0, inplace=True)
        dfbar[['Baden Württemberg', 'Bayern', 'Berlin', 'Brandenburg',
               'Bremen', 'Hamburg', 'Hessen', 'Mecklenburg-Vorpommern',
               'Niedersachsen', 'Nordrhein Westpfalen', 'Rheinland-Pfalz', 'Saarland',
               'Sachsen', 'Sachsen-Anhalt', 'Schleswig-Holstein', 'Thüringen']] = dfbar[
            ['Baden Württemberg', 'Bayern', 'Berlin', 'Brandenburg',
             'Bremen', 'Hamburg', 'Hessen', 'Mecklenburg-Vorpommern',
             'Niedersachsen', 'Nordrhein Westpfalen', 'Rheinland-Pfalz', 'Saarland',
             'Sachsen', 'Sachsen-Anhalt', 'Schleswig-Holstein', 'Thüringen']].astype(int)

        dfbar = dfbar.groupby(['categ', 'Gender']).sum().sum(axis=1).to_frame()
        dfbar.reset_index(inplace=True)

    Subjects = ['2012', '2019', '2020']

    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=Subjects,
        y=dfbar[dfbar['Gender'] == 'all'].iloc[:, -1].values,
        name='Total',
        text=dfbar[dfbar['Gender'] == 'all'].iloc[:, -1].values,
        textposition='auto',
        texttemplate='%{text:.2s}',
        marker_color='rgb(55, 83, 109)'
    ))
    fig.add_trace(go.Bar(
        x=Subjects,
        y=dfbar[dfbar['Gender'] == 'female'].iloc[:, -1].values,
        name='female',
        text=dfbar[dfbar['Gender'] == 'female'].iloc[:, -1].values,
        textposition='auto',
        texttemplate='%{text:.2s}',
        marker_color='rgb(26, 118, 255)'
    ))

    # Here we modify the tickangle of the xaxis, resulting in rotated labels.
    # fig.update_layout(barmode='group', xaxis_tickangle=-45)
    fig.update_layout(
        title='Anzahl der Studenten (1. Semester)',
        xaxis_tickfont_size=11,
        yaxis=dict(
            title='Amount',
            titlefont_size=12,
            tickfont_size=11,
        ),
        legend=dict(
            x=0,
            y=1.0,
            bgcolor='rgba(255, 255, 255, 0)',
            bordercolor='rgba(255, 255, 255, 0)'
        ),
        showlegend=False,
        barmode='group',
        bargap=0.15,  # gap between bars of adjacent location coordinates.
        bargroupgap=0.1,  # gap between bars of the same location coordinate.
        width=350,
        height=300
    )

    return fig


# Supervision Ratio
@app.callback(
    dash.dependencies.Output('supervisionratio', 'children'),
    [dash.dependencies.Input('year-dropdown', 'value'),
     dash.dependencies.Input('state-dropdown', 'value'),
     ])
def update_confirmed(year, state):
    card_content = [
        # dbc.CardHeader("Workers"),
        dbc.CardBody(
            [
                html.H6(

                    "Geschriebene Klausuren",
                    className="card-text",
                ),
                html.H4(updateCards(year, state, df, 'writtenexams'), className="card-title"),

            ],
        ),
    ]

    return dbc.Col(dbc.Card(card_content, style={"text-align": "center"}, color="light"))


# Students per Institutions
@app.callback(
    dash.dependencies.Output('studentsperinstitution', 'children'),
    [dash.dependencies.Input('year-dropdown', 'value'),
     dash.dependencies.Input('state-dropdown', 'value'),
     ])
def update_confirmed(year, state):
    card_content = [
        # dbc.CardHeader("Educational workers"),
        dbc.CardBody(
            [
                html.H6(

                    "Students/ University Ration",
                    className="card-text",
                ),
                html.H4(updateCards(year, state, df, 'studentsperinstitution'), className="card-title"),

            ]
        )
    ]
    return dbc.Col(dbc.Card(card_content, style={"text-align": "center"}, color="light"))


# Choropleth Map
@app.callback(
    dash.dependencies.Output('map', 'figure'),
    [dash.dependencies.Input('year-dropdown', 'value')])
def update_map(year):
    dfMap = df.copy()
    dfMap = dfMap[dfMap["categ"].isin(['supervisionratio'])]
    if not year:
        dfMap = dfMap.loc[:, :]
        title = "Relation Professoren pro Student"
    else:
        dfMap = dfMap.loc[year, :]
        title = "Professoren pro Student im Jahr {}".format(year)
    dfMap = dfMap.drop('categ', axis=1)
    dfMap = dfMap.dropna(axis=1).astype(int).sum(axis=0)
    dfMap = dfMap.to_frame()

    dfMap['cities'] = dfMap.index
    dfMap.rename(columns={0: 'value'}, inplace=True)
    dfMap['cities'] = dfMap['cities'].apply(lambda x: x.replace(" ", "-"))
    dfMap['cities'] = dfMap['cities'].apply(lambda x: x.replace("Nordrhein-Westpfalen", "Nordrhein-Westfalen"))

    # geojson = json.load(open("3_mittel.geo.json","r", encoding='utf-8'))
    state_id_map = {}
    for feature in geojson["features"]:
        feature["id"] = feature["properties"]["id"]
        state_id_map[feature["properties"]["name"]] = feature["id"]
    dfMap["id"] = dfMap["cities"].apply(lambda x: state_id_map[x])

    fig = px.choropleth(
        dfMap,
        locations="id",
        geojson=geojson,
        color="value",
        title=title,
        color_continuous_scale='PuBu',
        projection="mercator"
    )

    fig.update_geos(fitbounds="locations", visible=False)
    fig.update_layout(title_x=0.5, coloraxis_showscale=False)
    fig.update_layout(height=600, width=500, margin={"r": 0, "l": 0, "b": 0})
    return fig


# Subjects seperated by Federal States
@app.callback(
    dash.dependencies.Output('barGraph', 'figure'),
    [dash.dependencies.Input('year-dropdown', 'value'),
     dash.dependencies.Input('state-dropdown', 'value'),
     ])
def update_confirmed(year, state):
    dfbar = df.copy()
    for i in dfbar.index:
        if "female" not in dfbar.loc[i, 'categ']:
            x = dfbar.loc[i, 'categ']
            dfbar.loc[i, 'Gender'] = 'all'
        elif dfbar.loc[i, 'categ'] == "female":
            dfbar.loc[i, 'Gender'] = 'female'
            dfbar.loc[i, 'categ'] = dfbar.loc[i, 'categ'] + " " + x
    dfbar = dfbar[dfbar['categ'].isin([
        'Maths', 'female Maths',
        'economics', 'female economics', 'languages', 'female languages',
        'medicine/sport', 'female medicine/sport', 'engineering', 'female engineering',
        'education', 'female education', 'rest', 'female rest'
    ])]
    dfbar.reset_index(inplace=True)

    if year and state:
        dfbar = dfbar[dfbar['level_0'] == year]
        dfbar = dfbar[['level_0', "level_1", 'categ', 'Gender', state]]
        dfbar.drop('level_1', inplace=True, axis=1)
        dfbar = dfbar.set_index(['level_0', 'categ', 'Gender']).fillna(0)
        dfbar = dfbar.astype(int).sum(axis=1)
        dfbar = dfbar.to_frame()
        dfbar.reset_index(inplace=True)
    elif year and not state:
        dfbar = dfbar[dfbar['level_0'] == year]
        dfbar.drop('level_1', inplace=True, axis=1)
        dfbar = dfbar.set_index(['level_0', 'categ', 'Gender']).fillna(0)
        dfbar = dfbar.astype(int).sum(axis=1)
        dfbar = dfbar.to_frame()
        dfbar.reset_index(inplace=True)
    elif not year and state:
        dfbar = dfbar[['level_0', "level_1", 'categ', 'Gender', state]]
        dfbar.drop('level_1', inplace=True, axis=1)
        dfbar = dfbar.set_index(['level_0', 'categ', 'Gender']).fillna(0)
        dfbar = dfbar.astype(int).sum(axis=1)
        dfbar = dfbar.to_frame()
        dfbar.reset_index(inplace=True)
    else:
        dfbar = df.copy()
        for i in dfbar.index:
            if "female" not in dfbar.loc[i, 'categ']:
                x = dfbar.loc[i, 'categ']
                dfbar.loc[i, 'Gender'] = 'all'
            elif dfbar.loc[i, 'categ'] == "female":
                dfbar.loc[i, 'Gender'] = 'female'
                dfbar.loc[i, 'categ'] = dfbar.loc[i, 'categ'] + " " + x
        dfbar = dfbar[dfbar['categ'].isin([
            'Maths', 'female Maths',
            'economics', 'female economics', 'languages', 'female languages',
            'medicine/sport', 'female medicine/sport', 'engineering', 'female engineering',
            'education', 'female education', 'rest', 'female rest'
        ])]

        dfbar.fillna(0, inplace=True)
        dfbar[['Baden Württemberg', 'Bayern', 'Berlin', 'Brandenburg',
               'Bremen', 'Hamburg', 'Hessen', 'Mecklenburg-Vorpommern',
               'Niedersachsen', 'Nordrhein Westpfalen', 'Rheinland-Pfalz', 'Saarland',
               'Sachsen', 'Sachsen-Anhalt', 'Schleswig-Holstein', 'Thüringen']] = dfbar[
            ['Baden Württemberg', 'Bayern', 'Berlin', 'Brandenburg',
             'Bremen', 'Hamburg', 'Hessen', 'Mecklenburg-Vorpommern',
             'Niedersachsen', 'Nordrhein Westpfalen', 'Rheinland-Pfalz', 'Saarland',
             'Sachsen', 'Sachsen-Anhalt', 'Schleswig-Holstein', 'Thüringen']].astype(int)

        dfbar = dfbar.groupby(['categ', 'Gender']).sum().sum(axis=1).to_frame()
        dfbar.reset_index(inplace=True)

    Subjects = ['Mathe & Naturwissenschaften', 'Rechtswissenschaften', 'Geisteswissenschaften', 'Medizin & Sport',
                'Ingenieurwesen', 'Rest']

    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=Subjects,
        y=dfbar[dfbar['Gender'] == 'all'].iloc[:, -1].values,
        name='Total',
        text=dfbar[dfbar['Gender'] == 'all'].iloc[:, -1].values,
        textposition='auto',
        texttemplate='%{text:.2s}',
        marker_color='rgb(55, 83, 109)'
    ))
    fig.add_trace(go.Bar(
        x=Subjects,
        y=dfbar[dfbar['Gender'] == 'female'].iloc[:, -1].values,
        name='female',
        text=dfbar[dfbar['Gender'] == 'female'].iloc[:, -1].values,
        textposition='auto',
        texttemplate='%{text:.2s}',
        marker_color='rgb(26, 118, 255)'
    ))

    # Here we modify the tickangle of the xaxis, resulting in rotated labels.
    # fig.update_layout(barmode='group', xaxis_tickangle=-45)
    fig.update_layout(
        title='Anzahl der Studenten nach Fachbereich',
        xaxis_tickfont_size=11,
        yaxis=dict(
            title='Amount',
            titlefont_size=12,
            tickfont_size=11,
        ),
        legend=dict(
            x=0,
            y=1.0,
            bgcolor='rgba(255, 255, 255, 0)',
            bordercolor='rgba(255, 255, 255, 0)'
        ),
        showlegend=False,
        barmode='group',
        bargap=0.3,  # gap between bars of adjacent location coordinates.
        bargroupgap=0,  # gap between bars of the same location coordinate.
        xaxis={'categoryorder': 'total ascending'},
        width=600,
        height=350
    )

    return fig


# Money invested for the different Subjects seperated by Federal States
@app.callback(
    dash.dependencies.Output('barGraph2', 'figure'),
    [dash.dependencies.Input('year-dropdown', 'value'),
     dash.dependencies.Input('state-dropdown', 'value'),
     ])
def update_confirmed(year, state):
    dfbar = df.copy()
    for i in dfbar.index:
        if "female" not in dfbar.loc[i, 'categ']:
            x = dfbar.loc[i, 'categ']
            dfbar.loc[i, 'Gender'] = 'all'
        elif dfbar.loc[i, 'categ'] == "female":
            dfbar.loc[i, 'Gender'] = 'female'
            dfbar.loc[i, 'categ'] = dfbar.loc[i, 'categ'] + " " + x
    dfbar = dfbar[dfbar['categ'].isin([
        'MMaths', 'Meconomics', 'Mlanguages', 'Mmedicine/sport', 'Mengineering', 'Mrest'
    ])]
    dfbar.reset_index(inplace=True)

    if year and state:
        dfbar = dfbar[dfbar['level_0'] == year]
        dfbar = dfbar[['level_0', "level_1", 'categ', 'Gender', state]]
        dfbar.drop('level_1', inplace=True, axis=1)
        dfbar = dfbar.set_index(['level_0', 'categ', 'Gender']).fillna(0)
        dfbar = dfbar.astype(int).sum(axis=1)
        dfbar = dfbar.to_frame()
        dfbar.reset_index(inplace=True)
    elif year and not state:
        dfbar = dfbar[dfbar['level_0'] == year]
        dfbar.drop('level_1', inplace=True, axis=1)
        dfbar = dfbar.set_index(['level_0', 'categ', 'Gender']).fillna(0)
        dfbar = dfbar.astype(int).sum(axis=1)
        dfbar = dfbar.to_frame()
        dfbar.reset_index(inplace=True)
    elif not year and state:
        dfbar = dfbar[['level_0', "level_1", 'categ', 'Gender', state]]
        dfbar.drop('level_1', inplace=True, axis=1)
        dfbar = dfbar.set_index(['level_0', 'categ', 'Gender']).fillna(0)
        dfbar = dfbar.astype(int).sum(axis=1)
        dfbar = dfbar.to_frame()
        dfbar.reset_index(inplace=True)

    else:
        dfbar = df.copy()
        for i in dfbar.index:
            if "female" not in dfbar.loc[i, 'categ']:
                x = dfbar.loc[i, 'categ']
                dfbar.loc[i, 'Gender'] = 'all'
            elif dfbar.loc[i, 'categ'] == "female":
                dfbar.loc[i, 'Gender'] = 'female'
                dfbar.loc[i, 'categ'] = dfbar.loc[i, 'categ'] + " " + x
        dfbar = dfbar[dfbar['categ'].isin([
            'MMaths', 'Meconomics', 'Mlanguages', 'Mmedicine/sport', 'Mengineering', 'Mrest'
        ])]

        dfbar.fillna(0, inplace=True)
        dfbar[['Baden Württemberg', 'Bayern', 'Berlin', 'Brandenburg',
               'Bremen', 'Hamburg', 'Hessen', 'Mecklenburg-Vorpommern',
               'Niedersachsen', 'Nordrhein Westpfalen', 'Rheinland-Pfalz', 'Saarland',
               'Sachsen', 'Sachsen-Anhalt', 'Schleswig-Holstein', 'Thüringen']] = dfbar[
            ['Baden Württemberg', 'Bayern', 'Berlin', 'Brandenburg',
             'Bremen', 'Hamburg', 'Hessen', 'Mecklenburg-Vorpommern',
             'Niedersachsen', 'Nordrhein Westpfalen', 'Rheinland-Pfalz', 'Saarland',
             'Sachsen', 'Sachsen-Anhalt', 'Schleswig-Holstein', 'Thüringen']].astype(int)

        dfbar = dfbar.groupby(['categ', 'Gender']).sum().sum(axis=1).to_frame()
        dfbar.reset_index(inplace=True)

    Subjects = ['Mathe & Naturwissenschaften', 'Rechtswissenschaften', 'Geisteswissenschaften', 'Medizin & Sport',
                'Ingenieurwesen', 'Rest']

    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=Subjects,
        y=dfbar[dfbar['Gender'] == 'all'].iloc[:, -1].values,
        name='Total',
        text=dfbar[dfbar['Gender'] == 'all'].iloc[:, -1].values,
        textposition='auto',
        texttemplate='%{text:.2s}',
        marker_color='rgb(55, 83, 109)',
    ))
    fig.add_trace(go.Bar(
        x=Subjects,
        y=dfbar[dfbar['Gender'] == 'female'].iloc[:, -1].values,
        name='female',
        text=dfbar[dfbar['Gender'] == 'female'].iloc[:, -1].values,
        textposition='auto',
        texttemplate='%{text:.2s}',
        marker_color='rgb(26, 118, 255)'
    ))

    # Here we modify the tickangle of the xaxis, resulting in rotated labels.
    # fig.update_layout(barmode='group', xaxis_tickangle=-45)
    fig.update_layout(
        title='Gelder für die Fachbereiche',
        xaxis_tickfont_size=11,
        yaxis=dict(
            # title='Amount',
            titlefont_size=12,
            tickfont_size=11,
        ),
        legend=dict(
            x=0,
            y=1.0,
            bgcolor='rgba(255, 255, 255, 0)',
            bordercolor='rgba(255, 255, 255, 0)'
        ),
        showlegend=False,
        barmode='group',
        bargap=0.3,  # gap between bars of adjacent location coordinates.
        bargroupgap=0,  # gap between bars of the same location coordinate.
        xaxis={'categoryorder': 'total ascending'},
        width=500,
        height=300
    )

    return fig


# Graduations
@app.callback(
    dash.dependencies.Output('barGraph3', 'figure'),
    dash.dependencies.Input('year-dropdown', 'value'))
def update_confirmed(year):
    dfbar = df2.copy()
    for i in dfbar.index:
        if "female" not in dfbar.loc[i, 'categ2']:
            x = dfbar.loc[i, 'categ2']
            dfbar.loc[i, 'Gender'] = 'all'
        elif dfbar.loc[i, 'categ2'] == "female":
            dfbar.loc[i, 'Gender'] = 'female'
            dfbar.loc[i, 'categ2'] = dfbar.loc[i, 'categ2'] + " " + x
    dfbar = dfbar[dfbar['categ2'].isin([
        'Maths', 'female Maths', 'economics', 'female economics', 'languages', 'female languages',
        'medicine/sport', 'female medicine/sport', 'engineering', 'female engineering', 'rest', 'female rest'
    ])]
    dfbar.reset_index(inplace=True)

    if year:
        dfbar = dfbar[dfbar['level_0'] == year]
        dfbar.drop('level_1', inplace=True, axis=1)
        dfbar = dfbar.set_index(['level_0', 'categ2', 'Gender']).fillna(0)
        dfbar = dfbar.astype(int).sum(axis=1)
        dfbar = dfbar.to_frame()
        dfbar.reset_index(inplace=True)
    else:
        dfbar = dfbar[['level_0', "level_1", 'categ2', 'Gender']]
        dfbar.drop('level_1', inplace=True, axis=1)
        dfbar = dfbar.set_index(['level_0', 'categ2', 'Gender']).fillna(0)
        dfbar = dfbar.astype(int).sum(axis=1)
        dfbar = dfbar.to_frame()
        dfbar.reset_index(inplace=True)

        dfbar = dfbar.groupby(['categ2', 'Gender']).sum().sum(axis=1).to_frame()
        dfbar.reset_index(inplace=True)
        print(dfbar)

    Subjects = ['Mathe & Naturwissenschaften', 'Rechtswissenschaften', 'Geisteswissenschaften', 'Medizin & Sport',
                'Ingenieurwesen', 'Rest']

    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=Subjects,
        y=dfbar[dfbar['Gender'] == 'all'].iloc[:, -1].values,
        name='Total',
        text=dfbar[dfbar['Gender'] == 'all'].iloc[:, -1].values,
        # orientation='h',
        offsetgroup=1,
        # color=plswork,
        textposition='auto',
        texttemplate='%{text:.2s}',
        marker_color='rgb(55, 83, 109)',
    ))

    fig.add_trace(go.Bar(
        x=Subjects,
        y=dfbar[dfbar['Gender'] == 'female'].iloc[:, -1].values,
        name='female',
        text=dfbar[dfbar['Gender'] == 'female'].iloc[:, -1].values,
        # orientation='h',
        offsetgroup=2,
        # color=plswork,
        textposition='auto',
        texttemplate='%{text:.2s}',
        marker_color='rgb(26, 118, 255)'
    ))

    # Here we modify the tickangle of the xaxis, resulting in rotated labels.
    # fig.update_layout(barmode='group', xaxis_tickangle=-45)
    fig.update_layout(
        title='Abschlüsse',
        xaxis_tickfont_size=11,
        yaxis=dict(
            # title='Amount',
            titlefont_size=12,
            tickfont_size=11,
        ),
        legend=dict(
            x=0,
            y=1.0,
            bgcolor='rgba(255, 255, 255, 0)',
            bordercolor='rgba(255, 255, 255, 0)'
        ),
        showlegend=False,
        barmode='group',
        bargap=0.3,  # gap between bars of adjacent location coordinates.
        bargroupgap=0,  # gap between bars of the same location coordinate.
        xaxis={'categoryorder': 'category ascending'},
        width=530,
        height=350
    )

    return fig


@app.callback(
    dash.dependencies.Output('pieChart', 'figure'),
    [dash.dependencies.Input('year-dropdown', 'value'),
     dash.dependencies.Input('state-dropdown', 'value'),
     ])
def update_confirmed(year, state):
    if year and state:
        dfpie = df.copy()
        dfpie = dfpie[dfpie['categ'].isin([
            'Einnahmen', '3. Gelder'
        ])]
        dfpie.reset_index(inplace=True)
        dfpie = dfpie[['level_0', 'categ', state]]
        # dfpie.reset_index(inplace=True)
        # dfpie = dfpie.drop(columns=['level_1'],axis=1)
        dfpie = dfpie[dfpie['level_0'] == year]
        fig = px.pie(dfpie, values=state, names='categ', title='Finanzen')
    elif state and not year:
        dfpie = df.copy()
        dfpie = dfpie[dfpie['categ'].isin([
            'Einnahmen', '3. Gelder'
        ])]
        dfpie.reset_index(inplace=True)

        dfpie = dfpie[['categ', state]]
        dfpie[state] = dfpie[state].astype(int)
        dfpie = dfpie.groupby('categ').sum()
        fig = px.pie(dfpie, values=state, names=dfpie.index, title='Finanzen')


    elif not state and year:
        dfpie = df.copy()
        dfpie = dfpie[dfpie['categ'].isin([
            'Einnahmen', '3. Gelder'
        ])]
        dfpie.reset_index(inplace=True)
        dfpie = dfpie[dfpie['level_0'] == year]
        dfpie.drop(['level_0', 'level_1'], axis=1, inplace=True)
        dfpie = dfpie.groupby('categ').sum().astype(int).sum(axis=1)
        fig = px.pie(values=dfpie.values, names=dfpie.index, title='Finanzen')

    else:
        dfpie = df.copy()
        dfpie = dfpie[dfpie['categ'].isin([
            'Einnahmen', '3. Gelder'
        ])]
        dfpie.set_index('categ', inplace=True)
        dfpie = dfpie.astype(int)
        dfpie = dfpie.groupby('categ').sum().sum(axis=1)
        dfpie

        fig = px.pie(values=dfpie.values, names=dfpie.index, title='Finanzen')

    fig.update_traces(textposition='inside', textinfo='percent+label',
                      marker_colors=['rgb(30,144,255)', 'rgb(135,206,250)'])
    fig.update_layout(height=300, width=300, margin={"r": 50, "l": 50, "b": 50}, showlegend=False, title_x=0.5)
    return fig


@app.callback(
    dash.dependencies.Output('pieChart2', 'figure'),
    [dash.dependencies.Input('year-dropdown', 'value'),
     dash.dependencies.Input('state-dropdown', 'value'),
     ])
def update_confirmed(year, state):
    if year and state:
        dfpie = df.copy()
        dfpie = dfpie[dfpie['categ'].isin([
            'Wissenschaftliches Personal', 'Verwaltungs Personal'
        ])]
        dfpie.reset_index(inplace=True)
        dfpie = dfpie[['level_0', 'categ', state]]
        # dfpie.reset_index(inplace=True)
        # dfpie = dfpie.drop(columns=['level_1'],axis=1)
        dfpie = dfpie[dfpie['level_0'] == year]
        fig = px.pie(dfpie, values=state, names='categ', title='Fachkräfte')
    elif state and not year:
        dfpie = df.copy()
        dfpie = dfpie[dfpie['categ'].isin([
            'Wissenschaftliches Personal', 'Verwaltungs Personal'
        ])]
        dfpie.reset_index(inplace=True)

        dfpie = dfpie[['categ', state]]
        dfpie[state] = dfpie[state].astype(int)
        dfpie = dfpie.groupby('categ').sum()
        fig = px.pie(dfpie, values=state, names=dfpie.index, title='Fachkräfte')


    elif not state and year:
        dfpie = df.copy()
        dfpie = dfpie[dfpie['categ'].isin([
            'Wissenschaftliches Personal', 'Verwaltungs Personal'
        ])]
        dfpie.reset_index(inplace=True)
        dfpie = dfpie[dfpie['level_0'] == year]
        dfpie.drop(['level_0', 'level_1'], axis=1, inplace=True)
        dfpie = dfpie.groupby('categ').sum().astype(int).sum(axis=1)
        fig = px.pie(values=dfpie.values, names=dfpie.index, title='Fachkräfte')

    else:
        dfpie = df.copy()
        dfpie = dfpie[dfpie['categ'].isin([
            'Wissenschaftliches Personal', 'Verwaltungs Personal'
        ])]
        dfpie.set_index('categ', inplace=True)
        dfpie = dfpie.astype(int)
        dfpie = dfpie.groupby('categ').sum().sum(axis=1)
        dfpie

        fig = px.pie(values=dfpie.values, names=dfpie.index, title='Fachkräfte')

    fig.update_traces(textposition='inside', textinfo='percent+label',
                      marker_colors=['rgb(30,144,255)', 'rgb(135,206,250)'])
    fig.update_layout(height=300, width=300, margin={"r": 50, "l": 50, "b": 50}, showlegend=False, title_x=0.5)
    return fig


if __name__ == '__main__':
    app.run_server(host='0.0.0.0',port=5000,debug=False)