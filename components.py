import dash_bootstrap_components as dbc
from dash import html, dcc
import plotly.graph_objects as go
import plotly.express as px
from dash_iconify import DashIconify
import pandas as pd
import numpy as np


def addNavBar():
    return dbc.Nav(
        [
            dbc.NavItem(
                html.H1("Austin Animal Center", style={'Width': '100%', 'text-align': 'center', 'color': 'white'}))
        ], className='navbar navbar-expand-lg navbar-dark bg-primary', style={'justify-content': 'center'}
    )


def AddCard(title, val1=10, icn="noto:service-dog"):
    return dbc.Card(
        [dbc.CardHeader(title, className="card-header", style={'Padding': '1px'}),
         dbc.CardBody([dbc.Row([dbc.Col(DashIconify(icon=icn, height=40, width=40)), dbc.Col(html.H4(val1))])
                       ], className='card-body')
         ],
        style={'margin': '2px'}, className='card border-info mb-3'
    )


def addPieChart(labels, values, title):
    fig = go.Figure(data=[go.Pie(labels=labels, values=values, textfont_size=12,
                                 showlegend=False, hole=.4, textinfo='label+value+percent', )])

    fig.update_layout(
        title=title,
        paper_bgcolor='rgba(0,0,0,.03)',
    )
    return fig


def addBarChart(x, y, title):
    fig = px.bar(x=x, y=y, text_auto='.2s', color=x, color_continuous_scale=["red", "green", "blue"],
                 labels={'x': '', 'y': 'Count'})
    fig.update_traces(cliponaxis=False)
    fig.update(layout_showlegend=False)
    fig.update_layout(title=title, paper_bgcolor='rgba(0,0,0,.03)')

    return fig


def addHistoChart(animal_type, title):
    fig = px.histogram(x=animal_type['outcome_type'], y=animal_type['count'],
                       color=animal_type['animal_type'], barmode='group',
                       histfunc='avg',labels=dict(x="Animal Type", y="Count"))
    fig.update_layout(
        title=title,
        paper_bgcolor='rgba(0,0,0,.03)',
        uniformtext_minsize=8)
    return fig


def addLineChart(df):
    bar_df = df.groupby(['outcome_type', 'month'])['outcome_type'].count().to_frame('count').reset_index()
    Adoption = bar_df[bar_df['outcome_type'] == 'Adoption']

    Transfer = bar_df[bar_df['outcome_type'] == 'Transfer']
    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=Adoption['month'],
        y=Adoption['count'],
        name='Adoption',

    ))

    fig.add_trace(go.Scatter(
        x=Transfer['month'],
        y=Transfer['count'],
        name='Transfer',
    ))

    fig.update_xaxes(title_text='Month')
    fig.update_yaxes(title_text='Count')
    fig.update_traces(mode='lines+markers')
    fig.update_layout(title='Monthly Adoption vs Transfer Ratio',
                      legend=dict(y=0.5, traceorder='reversed', font_size=16), paper_bgcolor='rgba(0,0,0,.03)',
                      )

    return fig


def addDeadLineChart(df):
    bar_df = df.groupby(['outcome_type', 'month'])['outcome_type'].count().to_frame('count').reset_index()
    Died = bar_df[bar_df['outcome_type'] == 'Died']
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=Died['month'],
        y=Died['count'],
        name='Died',

    ))
    fig.update_xaxes(title_text='Month')
    fig.update_yaxes(title_text='Count')
    fig.update_traces(mode='lines+markers')
    fig.update_layout(title="Monthly Dead Ratio", legend=dict(y=0.5, traceorder='reversed', font_size=16),
                      paper_bgcolor='rgba(0,0,0,.03)')

    return fig


def addLineChart1(df):
    bar_df = df.groupby(['outcome_type', 'month'])['outcome_type'].count().to_frame('count').reset_index()
    Disposal = bar_df[bar_df['outcome_type'] == 'Disposal']
    Euthanasia = bar_df[bar_df['outcome_type'] == 'Euthanasia']
    Missing = bar_df[bar_df['outcome_type'] == 'Missing']
    Return_to_Owner = bar_df[bar_df['outcome_type'] == 'Return to Owner']
    Rto_Adopt = bar_df[bar_df['outcome_type'] == 'Rto-Adopt']
    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=Disposal['month'],
        y=Disposal['count'],
        name='Disposal',
    ))
    fig.add_trace(go.Scatter(
        x=Euthanasia['month'],
        y=Euthanasia['count'],
        name='Euthanasia',
    ))
    fig.add_trace(go.Scatter(
        x=Missing['month'],
        y=Missing['count'],
        name='Missing',
    ))
    fig.add_trace(go.Scatter(
        x=Return_to_Owner['month'],
        y=Return_to_Owner['count'],
        name='Return_to_Owner',
    ))
    fig.add_trace(go.Scatter(
        x=Rto_Adopt['month'],
        y=Rto_Adopt['count'],
        name='Rto_Adopt',
    ))
    fig.update_xaxes(title_text='Month')
    fig.update_yaxes(title_text='Count')
    fig.update_traces(mode='lines+markers')
    fig.update_layout(title='Monthly Disposal vs Euthanasia vs Missing vs Return to Owner vs RTO Adopt Ratio',
                      legend=dict(y=0.5, traceorder='reversed', font_size=16), paper_bgcolor='rgba(0,0,0,.03)')

    return fig


def addTab(df):
    animal_type = df.groupby('animal_type')['animal_type'].count()
    animal_out_type = df.groupby(['outcome_type'])['outcome_type'].count()
    tot_out_type = df.groupby(['outcome_type', 'animal_type'])['outcome_type'].count().to_frame('count').reset_index()
    tot_euthanasia = df[df['outcome_type'] == 'Euthanasia']
    tot_euthanasia = tot_euthanasia.groupby('outcome_subtype')['outcome_subtype'].count()

    bird_df = df[df['animal_type'] == 'Bird']
    bird_out_type = bird_df.groupby(['outcome_type'])['outcome_type'].count()
    top_breed_bird = bird_df['breed'].value_counts().head(5)
    bird_adoption = bird_df[bird_df['outcome_type'] == 'Adoption']
    TFAB = bird_adoption['breed'].value_counts().head(5)
    TFCB = bird_adoption['color'].value_counts().head(5)
    bird_dead = bird_df[bird_df['outcome_type'] == 'Died']
    TFDB = bird_dead['breed'].value_counts().head(5)

    cat_df = df[df['animal_type'] == 'Cat']
    cat_out_type = cat_df.groupby(['outcome_type'])['outcome_type'].count()
    sex_upon_outcome = cat_df.groupby(['sex_upon_outcome'])['sex_upon_outcome'].count()
    top_breed_cat = cat_df['breed'].value_counts().head(5)
    cat_adoption = cat_df[cat_df['outcome_type'] == 'Adoption']
    TFAC = cat_adoption['breed'].value_counts().head(5)
    TFCC = cat_adoption['color'].value_counts().head(5)
    cat_dead = cat_df[cat_df['outcome_type'] == 'Died']
    TFDC = cat_dead['breed'].value_counts().head(5)

    dog_df = df[df['animal_type'] == 'Dog']
    dog_out_type = dog_df.groupby(['outcome_type'])['outcome_type'].count()
    top_breed_dog = dog_df['breed'].value_counts().head(5)
    dog_adoption = dog_df[dog_df['outcome_type'] == 'Adoption']
    TFAD = dog_adoption['breed'].value_counts().head(5)
    TFCD = dog_adoption['color'].value_counts().head(5)
    dog_dead = dog_df[dog_df['outcome_type'] == 'Died']
    TFDD = dog_dead['breed'].value_counts().head(5)

    other_df = df[df['animal_type'] == 'Other']
    other_out_type = other_df.groupby(['outcome_type'])['outcome_type'].count()
    top_breed_other = other_df['breed'].value_counts().head(5)
    other_adoption = other_df[other_df['outcome_type'] == 'Adoption']
    TFAO = other_adoption['breed'].value_counts().head(5)
    TFCO = other_adoption['color'].value_counts().head(5)
    other_dead = other_df[other_df['outcome_type'] == 'Died']
    TFDO = other_dead['breed'].value_counts().head(5)

    return dbc.Tabs(
        ########## TAb 1
        [dbc.Tab([
            dbc.Row(html.H4('Total Number Of Animals', style={'Padding-left': '50px', 'color': 'white'}),
                    className='btn btn-success',
                    style={'border-radius': '5px', 'margin': '5px'}),
            dbc.Row([dbc.Col(dcc.Graph(
                figure=addPieChart(list(animal_type.to_dict().keys()), list(animal_type.to_dict().values()),
                                   'Total animals In Shelter'), style={'border-radius': '20px'}
            ), style={'margin': '5px', 'padding': '0px', 'border-radius': '20px'}, className='fig1'),
                dbc.Col(dcc.Graph(figure=addBarChart(list(animal_out_type.to_dict().keys()),
                                                     list(animal_out_type.to_dict().values()),
                                                     'Total Animals Depending on Outcome Type'),
                                  style={'border-radius': '5px',
                                         'background-color': 'rgba(0,0,0,.03)'}),
                        style={'margin': '5px', 'padding': '0px'},
                        className='fig1'),

            ], style={'margin': '5px'}),

            dbc.Row(html.H4('Animal type and Health Information', style={'Padding-left': '50px', 'color': 'white'}),
                    className='btn btn-info',
                    style={'border-radius': '5px', 'margin': '5px'}),
            dbc.Row(dbc.Col(dcc.Graph(figure=addHistoChart(tot_out_type, 'Total Animals Depending on Outcome Type and '
                                                                         'Animal Type'),
                                      style={'border-radius': '5px',
                                             'background-color': 'rgba(0,0,0,.03)'}
                                      ), style={'padding': '0px'}, className='fig1'
                            ),
                    style={'margin': '7px'}
                    ),
            dbc.Row(dbc.Col(dcc.Graph(figure=addBarChart(list(animal_out_type.to_dict().keys()),
                                                         list(animal_out_type.to_dict().values()),
                                                         'Total Number of Animals Depending on Outcome'),
                                      style={'border-radius': '5px',
                                             'background-color': 'rgba(0,0,0,.03)'}
                                      ), style={'padding': '0px'}, className='fig1'
                            ),
                    style={'margin': '7px'}
                    ),
            dbc.Row(html.H4('Monthly Adoption VS Transfer Ratio', style={'Padding-left': '50px', 'color': 'white'}),
                    className='btn btn-info',
                    style={'border-radius': '5px', 'margin': '5px'}),
            dbc.Row(
                dbc.Col(dcc.Graph(
                    figure=addLineChart(df)),
                    style={'background-color': 'rgba(0,0,0,.03)', 'padding': '0px', 'border-radius': '5px'}
                ), style={'margin': '7px'}, className='fig1'),
            dbc.Row(html.H4('Monthly Count of Animals Diseased and Missing',
                            style={'Padding-left': '50px', 'color': 'white'}),
                    className='btn btn-warning',
                    style={'border-radius': '5px', 'margin': '5px'}),
            dbc.Row(
                dbc.Col(dcc.Graph(figure=addLineChart1(df),
                                  ),
                        style={'background-color': 'rgba(0,0,0,.03)', 'padding': '0px', 'border-radius': '5px'},
                        ), style={'margin': '7px'}, className='fig1'),
            dbc.Row(html.H4('Monthly Death Ratio', style={'Padding-left': '50px', 'color': 'white'}),
                    className='btn btn-danger',
                    style={'border-radius': '5px', 'margin': '5px'}),
            dbc.Row(
                dbc.Col(dcc.Graph(figure=addDeadLineChart(df),
                                  style={'background-color': 'rgba(0,0,0,.03)'}
                                  ),
                        style={'background-color': 'rgba(0,0,0,.03)', 'padding': '0px', 'border-radius': '5px'}
                        ), style={'margin': '7px'}, className='fig1'),
            dbc.Row(html.H4('Animals Euthanasia Type and Count', style={'Padding-left': '50px', 'color': 'white'}),
                    className='btn btn-warning',
                    style={'border-radius': '5px', 'margin': '5px'}),
            dbc.Row(
                dbc.Col(dcc.Graph(figure=addBarChart(list(tot_euthanasia.to_dict().keys()),
                                                     list(tot_euthanasia.to_dict().values()), 'Total Animals '
                                                                                              'Dependig on '
                                                                                              'Euthanasia Type'),
                                  style={'background-color': 'rgba(0,0,0,.03)'}
                                  ),
                        style={'background-color': 'rgba(0,0,0,.03)', 'padding': '0px', 'border-radius': '5px'}
                        ), style={'margin': '7px'}, className='fig1'),
            dbc.Row(html.H4('Total Animals and Sex Ratio', style={'Padding-left': '50px', 'color': 'white'}),
                    className='btn btn-info',
                    style={'border-radius': '5px', 'margin': '5px'}),
            dbc.Row(
                dbc.Col(dcc.Graph(figure=addBarChart(list(sex_upon_outcome.to_dict().keys()),
                                                     list(sex_upon_outcome.to_dict().values()),
                                                     ''),
                                  style={'background-color': 'rgba(0,0,0,.03)'}
                                  ),
                        style={'background-color': 'rgba(0,0,0,.03)', 'padding': '0px', 'border-radius': '5px'}
                        ), style={'margin': '7px'}, className='fig1')
        ], label="Total Animals"),
            #### BIRDS ##################
            dbc.Tab([
                dbc.Row(html.H4('Top 5 Breeds of Birds in Shelter', style={'Padding-left': '50px', 'color': 'white'}),
                        className='btn btn-success',
                        style={'border-radius': '5px', 'margin': '5px', 'justify-content': 'right'}),
                dbc.Row([dbc.Col(dcc.Graph(figure=addPieChart(list(top_breed_bird.to_dict().keys()),
                                                              list(top_breed_bird.to_dict().values()),
                                                              'Top 5 Breeds of Birds'),
                                           style={'border-radius': '20px'}
                                           ), style={'margin': '5px', 'padding': '0px', 'border-radius': '20px'},
                                 className='fig1'),
                         dbc.Col(dcc.Graph(figure=addBarChart(list(TFAB.to_dict().keys()),
                                                              list(TFAB.to_dict().values()),
                                                              'Top 5 Adopted Breeds of Birds / Most Adopted Birds'),
                                           style={'border-radius': '5px',
                                                  'background-color': 'rgba(0,0,0,.03)'}),
                                 style={'margin': '5px', 'padding': '0px'},
                                 className='fig1'),
                         dbc.Col(dcc.Graph(figure=addBarChart(list(TFDB.to_dict().keys()),
                                                              list(TFDB.to_dict().values()),
                                                              'Top 5 Died Breeds'),
                                           style={'border-radius': '5px',
                                                  'background-color': 'rgba(0,0,0,.03)'}),
                                 style={'margin': '5px', 'padding': '0px'},
                                 className='fig1'),
                         dbc.Col(dcc.Graph(figure=addPieChart(list(TFCB.to_dict().keys()),
                                                              list(TFCB.to_dict().values()),
                                                              'Top 5 Adopted Birds Color / Most Favorites Color '),
                                           style={'border-radius': '5px',
                                                  'background-color': 'rgba(0,0,0,.03)', }),
                                 style={'margin': '5px', 'padding': '0px'},
                                 className='fig1')

                         ], style={'margin': '5px'}),
                dbc.Row(
                    html.H4('Birds Information Depending on Outcome', style={'Padding-left': '50px', 'color': 'white'}),
                    className='btn btn-info',
                    style={'border-radius': '5px', 'margin': '5px'}),
                dbc.Row(dbc.Col(dcc.Graph(figure=addBarChart(list(bird_out_type.to_dict().keys()),
                                                             list(bird_out_type.to_dict().values()),
                                                             'Total Birds Depending on Outcome Type'),
                                          style={'border-radius': '5px',
                                                 'background-color': 'rgba(0,0,0,.03)'}
                                          ), style={'padding': '0px'}, className='fig1'
                                ), style={'margin': '7px'}),
                dbc.Row(
                    html.H4('Monthly Birds Information Depending on Outcome',
                            style={'Padding-left': '50px', 'color': 'white'}),
                    className='btn btn-info',
                    style={'border-radius': '5px', 'margin': '5px'}),
                dbc.Row(
                    dbc.Col(dcc.Graph(
                        figure=addLineChart(bird_df)),
                        style={'background-color': 'rgba(0,0,0,.03)', 'padding': '0px', 'border-radius': '5px'}
                    ), style={'margin': '7px'}, className='fig1'),
                dbc.Row(html.H4('Monthly Count of Birds Diseased and Missing',
                                style={'Padding-left': '50px', 'color': 'white'}),
                        className='btn btn-warning',
                        style={'border-radius': '5px', 'margin': '5px'}),
                dbc.Row(
                    dbc.Col(dcc.Graph(figure=addLineChart1(bird_df)),
                            style={'background-color': 'rgba(0,0,0,.03)', 'padding': '0px', 'border-radius': '5px'},
                            ), style={'margin': '7px'}, className='fig1'),
                dbc.Row(html.H4('Monthly Death Ratio', style={'Padding-left': '50px', 'color': 'white'}),
                        className='btn btn-danger',
                        style={'border-radius': '5px', 'margin': '5px'}),
                dbc.Row(
                    dbc.Col(dcc.Graph(figure=addDeadLineChart(bird_df),
                                      style={'background-color': 'rgba(0,0,0,.03)'}
                                      ),
                            style={'background-color': 'rgba(0,0,0,.03)', 'padding': '0px', 'border-radius': '5px'}
                            ), style={'margin': '7px'}, className='fig1')

            ], label="Birds"),

            ##### Cat ########
            dbc.Tab([
                dbc.Row(html.H4('Top 5 Breeds of Cats in Shelter', style={'Padding-left': '50px', 'color': 'white'}),
                        className='btn btn-success',
                        style={'border-radius': '5px', 'margin': '5px', 'justify-content': 'right'}),
                dbc.Row([dbc.Col(dcc.Graph(figure=addPieChart(list(top_breed_cat.to_dict().keys()),
                                                              list(top_breed_cat.to_dict().values()),
                                                              'Top 5 Breeds'),
                                           style={'border-radius': '20px'}
                                           ), style={'margin': '5px', 'padding': '0px', 'border-radius': '20px'},
                                 className='fig1'),
                         dbc.Col(dcc.Graph(figure=addBarChart(list(TFAC.to_dict().keys()),
                                                              list(TFAC.to_dict().values()),
                                                              'Top 5 Adopted Breeds'),
                                           style={'border-radius': '5px',
                                                  'background-color': 'rgba(0,0,0,.03)'}),
                                 style={'margin': '5px', 'padding': '0px'},
                                 className='fig1'),
                         dbc.Col(dcc.Graph(figure=addBarChart(list(TFDC.to_dict().keys()),
                                                              list(TFDC.to_dict().values()),
                                                              'Top 5 Died Breeds'),
                                           style={'border-radius': '5px',
                                                  'background-color': 'rgba(0,0,0,.03)'}),
                                 style={'margin': '5px', 'padding': '0px'},
                                 className='fig1'),
                         dbc.Col(dcc.Graph(figure=addPieChart(list(TFCC.to_dict().keys()),
                                                              list(TFCC.to_dict().values()),
                                                              'Top 5 Adopted Birds Color / Most Favorites Color '),
                                           style={'border-radius': '5px',
                                                  'background-color': 'rgba(0,0,0,.03)', }),
                                 style={'margin': '5px', 'padding': '0px'},
                                 className='fig1')

                         ], style={'margin': '5px'}),
                dbc.Row(
                    html.H4('Cats Information Depending on Outcome', style={'Padding-left': '50px', 'color': 'white'}),
                    className='btn btn-info',
                    style={'border-radius': '5px', 'margin': '5px'}),
                dbc.Row(dbc.Col(dcc.Graph(figure=addBarChart(list(cat_out_type.to_dict().keys()),
                                                             list(cat_out_type.to_dict().values()),
                                                             'Total Birds Depending on Outcome Type'),
                                          style={'border-radius': '5px',
                                                 'background-color': 'rgba(0,0,0,.03)'}
                                          ), style={'padding': '0px'}, className='fig1'
                                ),
                        style={'margin': '7px'}),
                dbc.Row(
                    html.H4('Cats Information Depending on Outcome',
                            style={'Padding-left': '50px', 'color': 'white'}),
                    className='btn btn-info',
                    style={'border-radius': '5px', 'margin': '5px'}),
                dbc.Row(
                    dbc.Col(dcc.Graph(
                        figure=addLineChart(cat_df)),
                        style={'background-color': 'rgba(0,0,0,.03)', 'padding': '0px', 'border-radius': '5px'}
                    ), style={'margin': '7px'}, className='fig1'),
                dbc.Row(html.H4('Monthly Count of Cats Diseased and Missing',
                                style={'Padding-left': '50px', 'color': 'white'}),
                        className='btn btn-warning',
                        style={'border-radius': '5px', 'margin': '5px'}),
                dbc.Row(
                    dbc.Col(dcc.Graph(figure=addLineChart1(cat_df), ),
                            style={'background-color': 'rgba(0,0,0,.03)', 'padding': '0px', 'border-radius': '5px'},
                            ), style={'margin': '7px'}, className='fig1'),

                dbc.Row(html.H4('Monthly Death Ratio', style={'Padding-left': '50px', 'color': 'white'}),
                        className='btn btn-danger',
                        style={'border-radius': '5px', 'margin': '5px'}),
                dbc.Row(
                    dbc.Col(dcc.Graph(figure=addDeadLineChart(cat_df),
                                      style={'background-color': 'rgba(0,0,0,.03)'}
                                      ),
                            style={'background-color': 'rgba(0,0,0,.03)', 'padding': '0px', 'border-radius': '5px'}
                            ), style={'margin': '7px'}, className='fig1')

            ], label="Cats"),

            #### Dogs ##########
            dbc.Tab([
                dbc.Row(html.H4('Top 5 Breeds of Dogs in Shelter', style={'Padding-left': '50px', 'color': 'white'}),
                        className='btn btn-success',
                        style={'border-radius': '5px', 'margin': '5px', 'justify-content': 'right'}),
                dbc.Row([dbc.Col(dcc.Graph(figure=addPieChart(list(top_breed_dog.to_dict().keys()),
                                                              list(top_breed_dog.to_dict().values()),
                                                              'Top 5 Breeds'),
                                           style={'border-radius': '20px'}
                                           ), style={'margin': '5px', 'padding': '0px', 'border-radius': '20px'},
                                 className='fig1'),
                         dbc.Col(dcc.Graph(figure=addBarChart(list(TFAD.to_dict().keys()),
                                                              list(TFAD.to_dict().values()),
                                                              'Top 5 Adopted Breeds'),
                                           style={'border-radius': '5px',
                                                  'background-color': 'rgba(0,0,0,.03)'}),
                                 style={'margin': '5px', 'padding': '0px'},
                                 className='fig1'),
                         dbc.Col(dcc.Graph(figure=addBarChart(list(TFDD.to_dict().keys()),
                                                              list(TFDD.to_dict().values()),
                                                              'Top 5 Died Breeds'),
                                           style={'border-radius': '5px',
                                                  'background-color': 'rgba(0,0,0,.03)'}),
                                 style={'margin': '5px', 'padding': '0px'},
                                 className='fig1'),
                         dbc.Col(dcc.Graph(figure=addPieChart(list(TFCD.to_dict().keys()),
                                                              list(TFCD.to_dict().values()),
                                                              'Top 5 Adopted Birds Color / Most Favorites Color '),
                                           style={'border-radius': '5px',
                                                  'background-color': 'rgba(0,0,0,.03)', }),
                                 style={'margin': '5px', 'padding': '0px'},
                                 className='fig1')

                         ], style={'margin': '5px'}),
                dbc.Row(
                    html.H4('Dogs Information Depending on Outcome', style={'Padding-left': '50px', 'color': 'white'}),
                    className='btn btn-info',
                    style={'border-radius': '5px', 'margin': '5px'}),
                dbc.Row(dbc.Col(dcc.Graph(figure=addBarChart(list(dog_out_type.to_dict().keys()),
                                                             list(dog_out_type.to_dict().values()),
                                                             'Total Birds Depending on Outcome Type'),
                                          style={'border-radius': '5px',
                                                 'background-color': 'rgba(0,0,0,.03)'}
                                          ), style={'padding': '0px'}, className='fig1'),
                        style={'margin': '7px'}
                        ),
                dbc.Row(
                    html.H4('Dogs Information Depending on Outcome',
                            style={'Padding-left': '50px', 'color': 'white'}),
                    className='btn btn-info',
                    style={'border-radius': '5px', 'margin': '5px'}),
                dbc.Row(
                    dbc.Col(dcc.Graph(
                        figure=addLineChart(dog_df)),
                        style={'background-color': 'rgba(0,0,0,.03)', 'padding': '0px', 'border-radius': '5px'}
                    ), style={'margin': '7px'}, className='fig1'),
                dbc.Row(html.H4('Monthly Count of Dogs Diseased and Missing',
                                style={'Padding-left': '50px', 'color': 'white'}),
                        className='btn btn-warning',
                        style={'border-radius': '5px', 'margin': '5px'}),

                dbc.Row(
                    dbc.Col(dcc.Graph(figure=addLineChart1(dog_df),
                                      ),
                            style={'background-color': 'rgba(0,0,0,.03)', 'padding': '0px', 'border-radius': '5px'},
                            ), style={'margin': '7px'}, className='fig1'),
                dbc.Row(html.H4('Monthly Death Ratio', style={'Padding-left': '50px', 'color': 'white'}),
                        className='btn btn-danger',
                        style={'border-radius': '5px', 'margin': '5px'}),
                dbc.Row(
                    dbc.Col(dcc.Graph(figure=addDeadLineChart(dog_df),
                                      style={'background-color': 'rgba(0,0,0,.03)'}
                                      ),
                            style={'background-color': 'rgba(0,0,0,.03)', 'padding': '0px', 'border-radius': '5px'}
                            ), style={'margin': '7px'}, className='fig1')

            ], label="Dogs"),

            ########### Others #############
            dbc.Tab([
                dbc.Row(html.H4('Top 5 Breeds in Other Animals', style={'Padding-left': '50px', 'color': 'white'}),
                        className='btn btn-success',
                        style={'border-radius': '5px', 'margin': '5px'}),
                dbc.Row([dbc.Col(dcc.Graph(figure=addPieChart(list(top_breed_other.to_dict().keys()),
                                                              list(top_breed_other.to_dict().values()),
                                                              'Top 5 Breeds'),
                                           style={'border-radius': '20px'}
                                           ), style={'margin': '5px', 'padding': '0px', 'border-radius': '20px'},
                                 className='fig1'),
                         dbc.Col(dcc.Graph(figure=addBarChart(list(TFAO.to_dict().keys()),
                                                              list(TFAO.to_dict().values()),
                                                              'Top 5 Adopted Breeds'),
                                           style={'border-radius': '5px',
                                                  'background-color': 'rgba(0,0,0,.03)'}),
                                 style={'margin': '5px', 'padding': '0px'},
                                 className='fig1'),
                         dbc.Col(dcc.Graph(figure=addBarChart(list(TFDO.to_dict().keys()),
                                                              list(TFDO.to_dict().values()),
                                                              'Top 5 Died Breeds'),
                                           style={'border-radius': '5px',
                                                  'background-color': 'rgba(0,0,0,.03)'}),
                                 style={'margin': '5px', 'padding': '0px'},
                                 className='fig1'),
                         dbc.Col(dcc.Graph(figure=addPieChart(list(TFCO.to_dict().keys()),
                                                              list(TFCO.to_dict().values()),
                                                              'Top 5 Adopted Animals Color / Most Favorites Color '),
                                           style={'border-radius': '5px',
                                                  'background-color': 'rgba(0,0,0,.03)', }),
                                 style={'margin': '5px', 'padding': '0px'},
                                 className='fig1')

                         ], style={'margin': '5px'}),

                dbc.Row(html.H4('Animals Healths Info', style={'Padding-left': '50px', 'color': 'white'}),
                        className='btn btn-info',
                        style={'border-radius': '5px', 'margin': '5px'}),
                dbc.Row(dbc.Col(dcc.Graph(figure=addBarChart(list(other_out_type.to_dict().keys()),
                                                             list(other_out_type.to_dict().values()),
                                                             'Total Birds Depending on Outcome Type'),
                                          style={'border-radius': '5px',
                                                 'background-color': 'rgba(0,0,0,.03)'}
                                          ), style={'padding': '0px'}, className='fig1'
                                ),
                        style={'margin': '7px'}
                        ),
                dbc.Row(html.H4('Monthly Adoption Ratio', style={'Padding-left': '50px', 'color': 'white'}),
                        className='btn btn-warning',
                        style={'border-radius': '5px', 'margin': '5px'}),
                dbc.Row(
                    dbc.Col(dcc.Graph(
                        figure=addLineChart(other_df)),
                        style={'background-color': 'rgba(0,0,0,.03)', 'padding': '0px', 'border-radius': '5px'}
                    ), style={'margin': '7px'}, className='fig1'),
                dbc.Row(html.H4('Monthly Count of AAnimals Diseased and Missing',
                                style={'Padding-left': '50px', 'color': 'white'}),
                        className='btn btn-warning',
                        style={'border-radius': '5px', 'margin': '5px'}),
                dbc.Row(
                    dbc.Col(dcc.Graph(figure=addLineChart1(other_df),
                                      ),
                            style={'background-color': 'rgba(0,0,0,.03)', 'padding': '0px', 'border-radius': '5px'},
                            ), style={'margin': '7px'}, className='fig1'),
                dbc.Row(html.H4('Monthly Death Ratio', style={'Padding-left': '50px', 'color': 'white'}),
                        className='btn btn-danger',
                        style={'border-radius': '5px', 'margin': '5px'}),
                dbc.Row(
                    dbc.Col(dcc.Graph(figure=addDeadLineChart(other_df),
                                      style={'background-color': 'rgba(0,0,0,.03)'}
                                      ),
                            style={'background-color': 'rgba(0,0,0,.03)', 'padding': '0px', 'border-radius': '5px'}
                            ), style={'margin': '7px'}, className='fig1')

            ], label="Other"),

        ], style={'margin': '5px'}
    )
