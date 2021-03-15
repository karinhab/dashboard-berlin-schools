import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from dash_html_components.Div import Div
import plotly.express as px

import pandas as pd
import json


app = dash.Dash(__name__)

# Read data:
schulen = pd.read_csv(
    'data/schulen_complete.csv')
students = pd.read_excel(
    'data/eckdaten_2019_20_allg_bildende_schulen_berlin.xlsx')
activities = pd.read_csv(
    'data/activity-schools-BE.csv')
with open('data/districts.json') as f:
    districts = json.load(f)



def locate_schools_fig(schulen):
    #df = schulen.query("Bezirk == 'Friedrichshain-Kreuzberg'")
    fig = px.scatter_mapbox(schulen, lat="latitude", lon="longitude", hover_name="NAME",
                            hover_data={
                                'longitude': False,
                                'latitude': False,
                                'PLZ': True,
                                'Berliner Adresse': True,
                                'Internetadresse': True,
                                'eMail-Adresse': True,
                                'Telefonnummer': True},
                            color='Schultyp', zoom=10,
                            mapbox_style="open-street-map",
                            height=800)
    #fig.update_layout(margin={"r": 0, "t": 40, "l": 0, "b": 0})
    fig.update_traces(marker=dict(size=15),
                      selector=dict(mode='markers'))
    return fig


def get_treemap():
    fig = px.treemap(students,
                     path=[px.Constant(
                         'Berlin - Number of students per school-type and district'), 'Bezirk', 'Schulart'],
                     values='SchuelerInnen',
                     color='Schulart',
                     color_discrete_sequence=px.colors.qualitative.Bold)
    fig.update_layout(margin={"r": 16, "t": 16, "l": 16, "b": 16})
    return fig


def get_student_map():
    df = students.groupby('Bezirk').sum().reset_index()
    fig = px.choropleth_mapbox(df, geojson=districts, locations='Bezirk', color='SchuelerInnen',
                               color_continuous_scale="Turbo",
                               featureidkey='properties.name',
                               range_color=(20000, 45000),
                               mapbox_style="carto-positron",
                               zoom=9, center={"lat": 52.510000, "lon": 13.404954},
                               opacity=0.8,
                               labels={'SchuelerInnen': ''},
                               title='Total number of students per Berlin district',
                               height=600)
    return fig


def get_pie_activities():
    df = pd.DataFrame(activities.groupby('ag_cat')['id'].count()).reset_index()
    fig = px.pie(df, names='ag_cat', values='id',
                 title='Categories of activities at Berlin schools')
    return fig


def get_box_activities():
    df = df=pd.DataFrame(activities.groupby(['school','ag_name' ])['id'].count()).reset_index().groupby('school')['id'].count()
    fig = px.box(df, y="id", labels={'id':'no of activities per school'}, 
             title='Number of activities per school',
            width=400)
    return fig


def get_top_activities():
    df = pd.DataFrame(activities.groupby('ag_name')['id'].count(
    ).sort_values(ascending=False)).reset_index().head(30)
    fig = px.bar(df, x='ag_name', y='id', 
    title='TOP 30 school activities ',
    labels={'id':'no of schools offering activity', 'ag_name':''})
    return fig


app.layout = html.Div([

    html.H1(children='Schools of Berlin'),

    # =======================================================================
    #                           SECTION 1
    # =======================================================================
    html.Section([

        html.H2(children='ANALYSIS OF SCHOOL NUMBERS AND TYPES'),

        # ------------------------ Row 1 ------------------------
        html.Div([

            html.Div([

                html.Div([
                    dcc.Graph(
                        figure=px.pie(pd.DataFrame(schulen.groupby('Schultyp')['BSN'].count()).reset_index(),
                                      values='BSN',
                                      names='Schultyp',
                                      title='Share of schools per schooltype',
                                      hole=.5),
                        className="chart"
                    ),
                ], className="column w-50"),

                html.Div([
                    dcc.Graph(
                        figure=px.density_heatmap(schulen,
                                                  x="Bezirk",
                                                  y="Schultyp",
                                                  # height=700,
                                                  labels={
                                                      'Schultyp': '', 'Bezirk': ''},
                                                  title='Density of schooltypes per district'),
                        className="chart"
                    ),
                ], className="column w-50"),

            ], className="flex"),

        ], className="row-1"),

        # ------------------------ Row 2 ------------------------
        html.Div([

            html.Div([

                html.Div([
                    dcc.Graph(
                        figure=px.histogram(pd.DataFrame(schulen.groupby(['Traeger', 'Bezirk', 'Schultyp'])['BSN'].count()).reset_index(),
                                            x="Bezirk",
                                            y="BSN",
                                            color="Traeger",
                                            barmode='group',
                                            title='Private vs Public schools across the districts',
                                            hover_data=pd.DataFrame(schulen.groupby(['Traeger', 'Bezirk', 'Schultyp'])['BSN'].count()).reset_index().columns),
                        className="chart"
                    ),
                ], className="column w-50"),

                html.Div([
                    dcc.Graph(
                        figure=px.histogram(schulen[schulen['full_time_school'].isnull() != True],
                                            x='Bezirk',
                                            color='full_time_school',
                                            barmode='relative',
                                            labels={'full_time_school': ''},
                                            title='Number of schools with all-day supervision'),
                        className="chart"
                    ),
                ], className="column w-50"),

            ], className="flex"),

        ], className="row-2"),

        # ------------------------ Row 3 ------------------------
        html.Div([

            html.Div([

                html.Div([
                    dcc.Graph(
                        figure=px.choropleth_mapbox(schulen.groupby(['Bezirk', 'Schultyp']).count().reset_index(),
                                                    geojson=districts, locations='Bezirk', color='BSN',
                                                    color_continuous_scale="Turbo",
                                                    featureidkey='properties.name',
                                                    range_color=(0, 45),
                                                    mapbox_style="carto-positron",
                                                    zoom=8.7, center={"lat": 52.510000, "lon": 13.404954},
                                                    opacity=1,
                                                    labels={'BSN': ''},
                                                    title='Number of schools per Berlin district and schooltype',
                                                    height=600,
                                                    animation_frame='Schultyp'
                                                    ),
                        className="chart"
                    ),
                ], className="column w-50"),

                html.Div([
                    dcc.Graph(
                        figure=px.box(schulen.groupby(['Bezirk', 'PLZ']).agg(n=('BSN', 'count')).reset_index(drop=False).sort_values('Bezirk'),
                                      x='Bezirk',
                                      y="n",
                                      labels={'Bezirk': ''},
                                      title='Number of schools per PLZ within each district',
                                      height=600),
                                      
                        className="chart"
                    ),
                ], className="column w-50"),

            ], className="flex"),

        ], className="row-3"),

    ], className="section-1"),

    # =======================================================================
    #                           SECTION 2
    # =======================================================================
    html.Section([
        html.H2(children='SCHOOL SEARCH'),

        # ------------------------ Row 4 ------------------------
        html.Div([

            html.Div([
                html.Div([
                    html.Div([
                        dcc.Dropdown(
                            id='demo-dropdown',
                            options=[
                                {'label': 'Mitte', 'value': 'Mitte'},
                                {'label': 'Friedrichshain-Kreuzberg',
                                 'value': 'Friedrichshain-Kreuzberg'},
                                {'label': 'Pankow', 'value': 'Pankow'},
                                {'label': 'Charlottenburg-Wilmersdorf',
                                 'value': 'Charlottenburg-Wilmersdorf'},
                                {'label': 'Spandau', 'value': 'Spandau'},
                                {'label': 'Steglitz-Zehlendorf',
                                 'value': 'Steglitz-Zehlendorf'},
                                {'label': 'Tempelhof-Schöneberg',
                                 'value': 'Tempelhof-Schöneberg'},
                                {'label': 'Neukölln', 'value': 'Neukölln'},
                                {'label': 'Treptow-Köpenick',
                                 'value': 'Treptow-Köpenick'},
                                {'label': 'Marzahn-Hellersdorf',
                                 'value': 'Marzahn-Hellersdorf'},
                                {'label': 'Lichtenberg', 'value': 'Lichtenberg'},
                                {'label': 'Reinickendorf',
                                    'value': 'Reinickendorf'}
                            ],
                            value=''
                        ),
                        html.Div(id='dd-output-container')
                    ], className="dropdown-container")
                ], className="column w-100"),

            ], className="flex"),

        ], className="row-4"),

    ], className="section-2"),

    # =======================================================================
    #                           SECTION 3
    # =======================================================================
    html.Section([

        html.H2(children='Students'),

        # ------------------------ Row 5 ------------------------
        html.Div([

            html.Div([
                html.Div([
                    dcc.Graph(
                        figure=px.pie(pd.DataFrame(students.groupby('Schulart')['SchuelerInnen'].sum()).reset_index(),
                                      values='SchuelerInnen',
                                      names='Schulart',
                                      title='Share of students per schooltype',
                                      hole=.5),
                        className="chart"
                    ),
                ], className="column w-50"),

                html.Div([
                    dcc.Graph(
                        figure=get_treemap(),
                        className="chart"
                    ),
                ], className="column w-50"),

            ], className="flex"),

        ], className="row-5"),

        # ------------------------ Row 6 ------------------------
        html.Div([

            html.Div([

                html.Div([
                    dcc.Graph(
                        figure=get_student_map(),
                        className="chart"
                    ),
                ], className="column w-50"),

                html.Div([
                    dcc.Graph(
                        figure=px.bar(students,
                                      x="Traeger",
                                      y="SchuelerInnen",
                                      color='Schulart',
                                      animation_frame='Bezirk',
                                      barmode='group',
                                      title='Number of students per Schooltype',
                                      range_y=[0, 16000],
                                      height=600),
                        className="chart"
                    ),
                ], className="column w-50"),

            ], className="flex"),

        ], className="row-6"),

    ], className="section-3"),

    # =======================================================================
    #                           SECTION 4
    # =======================================================================
    html.Section([
        html.H2(children='Activities'),

        # ------------------------ Row 7 ------------------------
        html.Div([

            html.Div([

                html.Div([
                    dcc.Graph(
                        figure=get_pie_activities(),
                        className="chart"
                    ),
                ], className="column w-60"),

                html.Div([
                    dcc.Graph(
                        figure=get_box_activities(),
                        className="chart"
                    ),
                ], className="column w-40"),

            ], className="flex"),

        ], className="row-7"),

        # ------------------------ Row 8 ------------------------
        html.Div([

            html.Div([

                html.Div([
                    dcc.Graph(
                        figure=get_top_activities(),
                        className="chart"
                    ),
                ], className="column w-100"),

            ], className="flex"),

        ], className="row-8"),

    ], className="section-4"),



])


@app.callback(
    dash.dependencies.Output('dd-output-container', 'children'),
    [dash.dependencies.Input('demo-dropdown', 'value')]
)
def update_output(value):
    df = schulen

    if len(value) > 0:
        df = schulen.query("Bezirk == '" + value + "'")
    return dcc.Graph(figure=locate_schools_fig(df), className="chart")


if __name__ == '__main__':
    app.run_server(debug=True)
