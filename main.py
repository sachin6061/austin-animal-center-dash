from dash import Dash, html, dcc
import dash_bootstrap_components as dbc
import components as c
import pandas as pd
import numpy as np

df = pd.read_csv('aac_shelter_outcomes.csv')
# df = df[df['animal_type'] != 'Livestock']
df['datetime'] = pd.to_datetime(df['datetime'], dayfirst=True)
df['month'] = df['datetime'].dt.strftime('%Y-%m')
animal_type = df.groupby('animal_type')['animal_type'].count()
tot_birds = animal_type['Bird']
tot_cats = animal_type['Cat']
tot_dogs = animal_type['Dog']
tot_others = animal_type['Other']
tot_animals = tot_cats + tot_others + tot_dogs + tot_birds

app = Dash(external_stylesheets=[dbc.themes.ZEPHYR, dbc.icons.FONT_AWESOME])

app.layout = html.Div(
    [c.addNavBar(), dbc.Row([dbc.Col(c.AddCard('Total Animals', tot_animals, 'emojione-v1:monkey')),
                             dbc.Col(c.AddCard('Birds', tot_birds, "twemoji:bird"))
                                , dbc.Col(c.AddCard('Cats', tot_cats, 'emojione:cat')),
                             dbc.Col(c.AddCard('Dogs', tot_dogs)),
                             dbc.Col(c.AddCard('Others', tot_others, "emojione:rabbit"))]),
     html.Div(c.addTab(df))], className='main', style={'margin': '2px'})

if __name__ == '__main__':
    app.run_server(debug=False)
