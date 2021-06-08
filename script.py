import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import matplotlib.pyplot as plt
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import seaborn as sns

#Dados
df = pd.read_csv('/home/cecelhax/Área de Trabalho/bestsellers with categories.csv')
df_genre_year = df.groupby(['Genre', 'Year'], as_index=False).agg({'Name': 'count'}).rename(columns={'Name': 'count'}).sort_values('Year')
ur = df['User Rating'].value_counts().sort_index()
df_price_year = df[df['Price']>0].groupby(['Genre', 'Year'], as_index=False).agg({'Price': 'mean'}).round(1).sort_values('Year')
df_genre_rev_year = df.groupby(['Genre', 'Year'], as_index=False).agg({'Reviews': 'mean'}).astype({'Reviews':'int'}).sort_values('Year')

#Importação de CSS
#external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

#Criação da aplicação
app = dash.Dash(__name__)

#Definição de cores
colors = {
    'background': '#ffffff',
    'text': '#000000'
}

#grafico
fig = make_subplots(
                rows=2,
                cols=2,
                column_widths=[0.5, 0.5],
                row_heights=[0.7, 0.3],
                vertical_spacing=0.08,
                specs=[[{'colspan': 2}, {}],
                        [{'type': 'xy'}, None]],
                subplot_titles=['Divisão de generos por ano']
            )     
fig.add_trace(
        go.Bar(
            name="Non Fiction",
            x=df_genre_year[df_genre_year['Genre']=='Non Fiction']['Year'],
            y=df_genre_year[df_genre_year['Genre']=='Non Fiction']['count'],
            marker_color='orangered',
            offsetgroup=0
        ),
    row=1,
    col=1
            )
fig.add_trace(
        go.Bar(
            name="Fiction",
            x=df_genre_year[df_genre_year['Genre']=='Fiction']['Year'],
            y=df_genre_year[df_genre_year['Genre']=='Fiction']['count'],
            marker_color='black',
            offsetgroup=1
        ),
    row=1,
    col=1
    )
fig.update_xaxes(dtick=1, row=1, col=1)
fig.update_layout(template='simple_white', height=500)
fig.update_xaxes(visible=False, row=2, col=1)
fig['layout']['annotations'][0].update(x=0.5, y=1.05)

#grafico2
fig2 = go.Figure(
    data = [
        go.Scatter(
            name='Fiction',
            x=df_price_year.query('Genre=="Fiction"')['Year'],
            y=df_price_year.query('Genre=="Fiction"')['Price'],
            marker_color='black',
        ),
        go.Scatter(
            name='Non Fiction',
            x=df_price_year.query('Genre=="Non Fiction"')['Year'],
            y=df_price_year.query('Genre=="Non Fiction"')['Price'],
            marker_color='orangered',
        ),
    ],
    layout = go.Layout(
        template='seaborn',
        title='Average Price by Genre per Year',
        title_x=0.5,
        yaxis_title='Price, $',
        xaxis_dtick=1,
        xaxis_title='Year'
        )
)
#grafico3
fig3 = go.Figure(
    data=[
        go.Scatter(
            name='Fiction',
            x=df_genre_rev_year.query('Genre=="Fiction"')['Year'],
            y=df_genre_rev_year.query('Genre=="Fiction"')['Reviews'],
            marker_color='black',
        ),
        go.Scatter(
            name='Non Fiction',
            x=df_genre_rev_year.query('Genre=="Non Fiction"')['Year'],
            y=df_genre_rev_year.query('Genre=="Non Fiction"')['Reviews'],
            marker_color='orangered',
        ),
    ],
    layout=go.Layout(
        template='seaborn',
        title='Average Reviews by Genre per Year',
        title_x=0.5,
        yaxis_title='Reviews',
        xaxis_dtick=1
        )
)

app.layout = html.Div(style={'backgroundColor': colors['background']}, children=[
    html.H1(
        children='Os 50 livros mais vendidos da Amazon de 2009 a 2019',
        style={
            'textAlign': 'center',
            'color': colors['text']
        }
    ),

    html.H2(children='Exploratory data analisys', style={
        'textAlign': 'center',
        'size': 25,
        'color': colors['text']
    }),
    dcc.Graph(
        figure = fig
        
        ),
    dcc.Graph(
        figure = fig2
        
        ),
    dcc.Graph(
        figure = fig3
        
        )
])    
if __name__ == '__main__':
    app.run_server(debug=True)