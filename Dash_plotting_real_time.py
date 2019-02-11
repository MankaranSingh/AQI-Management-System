import pandas as pd
import datetime
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import sqlite3
 
conn = sqlite3.connect('data.sqlite')
query = "SELECT * FROM aqi_data;"
 
df = pd.read_sql_query(query,conn)

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)


app.layout = html.Div(children=[
    html.Div(children='''
        Select Arguements:
    '''),
     
    dcc.Dropdown(
                id='state',
                options=[{'label': i, 'value': i} for i in df.state.unique()],
                value='Punjab'
            ),
    dcc.Dropdown(
                id='city',
                options=[{'label': i, 'value': i} for i in df.city.unique()],
                value='Patiala'
            ),
    dcc.Dropdown(
                id='area',
                options=[{'label': i, 'value': i} for i in df.area.unique()],
                value='PremNagar'
            ),
    dcc.Dropdown(
                id='to_plot',
                options=[{'label': i, 'value': i} for i in ['aqi','humidity','temp' ,'CO','NO2','O3','PM10','PM25','SO2']],
                value='aqi'
            ),
    
    html.Div(id='output_graph'),
])

@app.callback(
    dash.dependencies.Output('output_graph', 'children'),
    [dash.dependencies.Input('state', 'value'),
     dash.dependencies.Input('city', 'value'),
     dash.dependencies.Input('area', 'value'),
     dash.dependencies.Input('to_plot', 'value')
     ])
def update_value(state,city,area,to_plot):

    conn = sqlite3.connect('data.sqlite')
    query = "SELECT * FROM aqi_data;"
 
    df = pd.read_sql_query(query,conn)
    
    state_df = df[df.state==str(state)]
    city_df = state_df[df.city==str(city)]
    area_df = city_df[df.area==str(area)]

    return dcc.Graph(
        id='figure',
        figure={
            'data': [
                {'y': area_df[str(to_plot)][-100:], 'type': 'bar', 'name': str(state)+', '+str(city)+ ', ' + str(area), 'title': str(to_plot)},
                {'y': area_df[str(to_plot)][-100:], 'type': 'line', 'name': str(state)+', '+str(city)+ ', ' + str(area), 'title': str(to_plot)},
            ],
            'layout': {
                'title': str(state)+', '+str(city)+', ' + str(area),
                'xaxis' :dict(
        title='Time',
        titlefont=dict(
            
            size=15,
            color='#7f7f7f'
        )
        )
    ,
    'yaxis':dict(
        title= str(to_plot),
        titlefont=dict(
            
            size=15,
            color='#7f7f7f'
        )
            )
                }})

if __name__ == '__main__':
    app.run_server(debug=True)
