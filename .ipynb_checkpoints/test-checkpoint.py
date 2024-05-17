import dash
from dash import dcc, html
import plotly.express as px
import pandas as pd

# Load your data here
data = pd.read_csv('C:\\Users\\HP\\Desktop\\pfetest\\data.csv', delimiter=';')

# Assuming 'GCA_A_1' and 'GCA_A_2' are valid columns for demonstration
# Define color sequence for the theme
colors = ['orange', 'yellow', 'pink', 'red']

# Bar Chart - Assuming 'GCA_A_1' values categorized by 'Client_name'
fig_bar = px.bar(data, x='Client_name', y='GCA_A_1', title='Scores by Client',
                 color='Client_name', color_discrete_sequence=px.colors.qualitative.Pastel)

# Pie Chart - Assuming 'Secteur' is a categorical column
fig_pie = px.pie(data, names='Secteur', values='GCA_A_1', title='Sector Breakdown',
                 color_discrete_sequence=[colors[0], colors[1], colors[2]])

# Line Chart - Assuming 'DATE_SAISIE' can be parsed as datetime and shows progression of 'GCA_A_1'
data['DATE_SAISIE'] = pd.to_datetime(data['DATE_SAISIE'])
fig_line = px.line(data, x='DATE_SAISIE', y='GCA_A_1', title='Progression Over Time',
                   color_discrete_sequence=[colors[3]])

# Scatter Chart - Comparing 'GCA_A_1' vs 'GCA_A_2'
fig_scatter = px.scatter(data, x='GCA_A_1', y='GCA_A_2', title='Comparison of GCA Scores',
                         color_discrete_sequence=colors)

# Create Dash application
app = dash.Dash(__name__)
app.layout = html.Div(children=[
    html.H1(children='Interactive Client Dashboard'),
    html.Div(className='row', children=[
        dcc.Graph(id='bar-chart', figure=fig_bar),
        dcc.Graph(id='pie-chart', figure=fig_pie)
    ]),
    html.Div(className='row', children=[
        dcc.Graph(id='line-chart', figure=fig_line),
        dcc.Graph(id='scatter-chart', figure=fig_scatter)
    ])
])

if __name__ == '__main__':
    app.run_server(debug=True)
s