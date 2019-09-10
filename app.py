import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import datetime
import prediction


app = dash.Dash()

app.layout = html.Div(children=[
    html.H1('Prediksi harga saham'),
    dcc.Input(id='input', type='text'),
    html.Div(id='output-graph')
])

@app.callback(
    Output(component_id='output-graph', component_property='children'),
    [Input(component_id='input', component_property='value')]
)
def update_graph(input_data):
    
    start = datetime.datetime(2019,1,1)
    end = datetime.datetime.now()

    try:
        (df,_,_,_,_) = prediction.predict(input_data, start, end)
    except:
        return ""

    return dcc.Graph(id='contoh',
            figure={
                'data': [{'x': df.index, 'y': df['Adj Close'], 'type':'line', 'name':'stock'},
                        {'x': df.index, 'y': df['F_reg'], 'type': 'line', 'name': 'f_reg'},
                        {'x': df.index, 'y': df['F_poly2'], 'type': 'line', 'name': 'f_poly2'},
                        {'x': df.index, 'y': df['F_poly3'], 'type': 'line', 'name': 'f_poly3'},
                        {'x': df.index, 'y': df['F_knn'], 'type': 'line', 'name': 'f_knn'},
                ],
                'layout': {
                    'title': input_data
                }
            }
        )



if __name__ == '__main__':
    app.run_server(debug=True)
