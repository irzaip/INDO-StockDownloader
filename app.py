import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import datetime
from datetime import datetime as dt
import prediction


app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = html.Div(children=[
    dbc.Row([
    html.H1('Prediksi harga saham'),
    dcc.Input(id='input', type='text'),
    dcc.DatePickerRange(
        id='dt-pick',
        min_date_allowed=dt(2010,1,1),
        max_date_allowed=datetime.datetime.now()-datetime.timedelta(days=-25),
        initial_visible_month=dt(2018, 1, 1),
        end_date=datetime.datetime.now()
    ),]),
    dbc.Row([
        dbc.Col([
                html.Div(id='output-graph')
            ], width="auto")
        ])
    ])

@app.callback(
    Output(component_id='output-graph', component_property='children'),
    [Input(component_id='input', component_property='value'),
    Input('dt-pick','start_date'),
    Input('dt-pick','end_date')]
)
def update_graph(input_data, start_date, end_date):
    
    start = start_date
    end = end_date

    try:
        (df,_,_,_,_) = prediction.predict(input_data, start, end)
    except:
        return ""

    return dcc.Graph(id='contoh',
            figure={
                'data': [{'x': df.index, 'y': df['Adj Close'], 
                            'type':'line', 
                            'name':'stock'},
                        {'x': df.index, 'y': df['F_reg'], 
                            'type': 'line', 
                            'name': 'f_reg'},
                        {'x': df.index, 'y': df['F_poly2'], 
                            'type': 'line', 
                            'name': 'f_poly2'},
                        {'x': df.index, 'y': df['F_poly3'], 
                            'type': 'line', 
                            'name': 'f_poly3'},
                        {'x': df.index, 'y': df['F_knn'], 
                            'type': 'line', 
                            'name': 'f_knn'},
                ],
                'layout': {
                    'title': input_data
                }
            }
        )



if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0')
