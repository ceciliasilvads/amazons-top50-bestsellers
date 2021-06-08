import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objects as go

#Importação e tratamento dos dados
df = pd.read_csv('/home/cecelhax/Área de Trabalho/bestsellers with categories.csv')
ur = df['User Rating'].value_counts().sort_index()
df_price_year = df[df['Price']>0].groupby(['Genre', 'Year'], as_index=False).agg({'Price': 'mean'}).round(1).sort_values('Year')
df_genre_rev_year = df.groupby(['Genre', 'Year'], as_index=False).agg({'Reviews': 'mean'}).astype({'Reviews':'int'}).sort_values('Year')

app = dash.Dash(__name__)

colors = {
    'background': '#ffffff',
    'text': '#000000'
}

fig1 = go.Figure(
    data=[
        go.Scatter(
            name = 'Fiction',
            x = df_price_year.query('Genre=="Fiction"')['Year'],
            y = df_price_year.query('Genre=="Fiction"')['Price'],
            marker_color = 'black',
        ),
        go.Scatter(
            name = 'Non Fiction',
            x = df_price_year.query('Genre=="Non Fiction"')['Year'],
            y = df_price_year.query('Genre=="Non Fiction"')['Price'],
            marker_color = 'orangered',
        ),
    ],
    layout = go.Layout(
        title = 'Preço médio dos gêneros por ano',
        title_x = 0.5,
        yaxis_title = 'Preço',
        xaxis_dtick = 1,
        xaxis_title = 'Ano'
        )
)

fig2 = go.Figure(
    data = [
        go.Scatter(
            name = 'Fiction',
            x = df_genre_rev_year.query('Genre=="Fiction"')['Year'],
            y = df_genre_rev_year.query('Genre=="Fiction"')['Reviews'],
            marker_color = 'black',
        ),
        go.Scatter(
            name = 'Non Fiction',
            x = df_genre_rev_year.query('Genre=="Non Fiction"')['Year'],
            y = df_genre_rev_year.query('Genre=="Non Fiction"')['Reviews'],
            marker_color = 'orangered',
        ),
    ],
    layout = go.Layout(
        title = 'Média de avaliações dos gêneros por ano',
        title_x = 0.5,
        yaxis_title = 'Avaliações',
        xaxis_dtick = 1
        )
)

app.layout = html.Div(style = {'backgroundColor': colors['background']}, children=[
    html.H1(
        children = 'Os 50 livros mais vendidos da Amazon de 2009 a 2019',
        style = {
            'textAlign': 'center',
            'color': colors['text']
        }
    ),
    html.H2(
        children = 'Visualização dos dados', 
        style = {
            'textAlign': 'center',
            'size': 25,
            'color': colors['text']
    }),
    dcc.Graph(
        figure = fig1
        
        ),
    dcc.Graph(
        figure = fig2
        
        )
])    
if __name__ == '__main__':
    app.run_server(debug=True)