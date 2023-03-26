#Importer les bibliothèques nécessaires
import dash
from dash import  dcc
from dash import html
import pandas as pd
import plotly.graph_objs as go
from dash.dependencies import Output, Input
import dash_table

# Lire les données à partir du fichier csv

df = pd.read_csv('data_and_time.csv')
df.columns = ['Prix', 'Date']
volatility = df['Prix'].pct_change().std() * 100 # Calculer la volatilité des prix

df['Date'] = pd.to_datetime(df['Date'])
# Obtenir le dernier prix de 20h
last_price_20am = df[(df['Date'].dt.hour == 20)]['Prix'].iloc[-1]

# Obtenir le dernier prix de 14h
last_price_14am = df[(df['Date'].dt.hour == 14)]['Prix'].iloc[-1]


# Créer l'application Dash
app = dash.Dash(__name__)

# Créer le layout de l'application
app.layout = html.Div(
    children=[
        html.H1("Cours de l'or en fonction du temps"),
        dcc.Graph(id='scatter-plot'),
        dcc.Interval(id='interval-component', interval=1000*60, n_intervals=0),
        dash_table.DataTable(
            id='table',
            columns=[
                {'name': 'Volatility', 'id': 'volatility'},
                {'name': 'Open', 'id': 'open'},
                {'name': 'Closed', 'id': 'closed'}
            ],
            data=[
                {'volatility': volatility, 'open': last_price_14am, 'closed': last_price_20am},
            ]
        )
    ]
)

# Mettre à jour le graphique
@app.callback(Output('scatter-plot', 'figure'),
              [Input('interval-component', 'n_intervals')])
def update_graph(n):
    df = pd.read_csv('data_and_time.csv', names=['Prix', 'Date'], header=None)
    df['Date'] = pd.to_datetime(df['Date'])  # Convertir la colonne Date en datetime
    trace = go.Scatter(x=df['Date'], y=df['Prix'], mode='lines+markers')
    layout = go.Layout(
        xaxis=dict(title='Date'),
        yaxis=dict(title='Prix')
    )
    return {'data': [trace], 'layout': layout}

# Mettre à jour le tableau toutes les 24 heures
@app.callback(Output('table', 'data'),
              [Input('interval-component', 'n_intervals')])
def update_table(n):
    df = pd.read_csv('data_and_time.csv', names=['Prix', 'Date'], header=None)
    df['Date'] = pd.to_datetime(df['Date'])
	# Obtenir le dernier prix de 20h
    last_price_20am = df[(df['Date'].dt.hour == 20)]['Prix'].iloc[-1]

# Obtenir le dernier prix de 14h
    last_price_14am = df[(df['Date'].dt.hour == 14)]['Prix'].iloc[-1]
    
    volatility = df['Prix'].pct_change().std() * 100  # Calculer la volatilité des prix
    return [{'volatility': volatility, 'open': last_price_14am, 'closed': last_price_20am}]

# Lancer l'application
if __name__ == '__main__':
    app.run_server(host = "0.0.0.0", port=8050, debug=True)
