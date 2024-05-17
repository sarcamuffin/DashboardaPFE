import dash
from dash import dcc, html
import pandas as pd
import plotly.express as px

colors = {
    'background': '#ffffff',
    'text': '#000000',
    'plotly': ['#FFB600', '#EB8C00', '#D04A02', '#DB536A', '#E0311E', '#000000']
}

# Reading data files
try:
    df = pd.read_csv('data.csv', delimiter=';')
    mapping_df = pd.read_excel('Mapping_noms_variables_sphinx.xlsx')
except Exception as e:
    print(f"Error reading files: {e}")

# Creating mapping dictionary and renaming columns
try:
    column_mapping = dict(zip(mapping_df['Anciens Noms'], mapping_df['Nouveaux Noms']))
    df.rename(columns=column_mapping, inplace=True)
except Exception as e:
    print(f"Error mapping columns: {e}")

# Filtering data for a specific client
try:
    client_name = 'emi'
    df_emi = df[df['Clien_Name'] == client_name]
except Exception as e:
    print(f"Error filtering data for client '{client_name}': {e}")

# Defining columns to exclude and include
excluded_columns = [
    "Clien_Name", "Secteur", "axe-reglement", "reglement", "CLE",
    "DATE_SAISIE", "DATE_ENREG", "DATE_MODIF", "TEMPS_SAISIE", "ORIGINE_SAISIE",
    "LANG_SAISIE", "APPAREIL_SAISIE", "PROGRESSION", "DERNIERE_QUESTION_SAISIE"
]
included_columns = [col for col in df_emi.columns if col not in excluded_columns]

# Calculating average scores for themes
themes = set(col.split(' -')[0] for col in included_columns if '-' in col)
try:
    for theme in themes:
        theme_cols = [col for col in included_columns if col.startswith(theme)]
        if theme_cols:
            df[theme + ' Moyenne'] = df[theme_cols].mean(axis=1)
except Exception as e:
    print(f"Error calculating theme averages: {e}")

# Preparing data for plots
try:
    data_for_plot = df[[theme + ' Moyenne' for theme in themes]].mean().reset_index()
    data_for_plot.columns = ['Theme', 'Moyenne']
except Exception as e:
    print(f"Error preparing data for plots: {e}")

# Creating visualizations
fig_bar = px.bar(data_for_plot, x='Theme', y='Moyenne', title='Moyenne de Maturité par Thème', range_y=[0, 5])
fig_scatter = px.scatter(data_for_plot, x='Theme', y='Moyenne', color='Moyenne', size='Moyenne',
                         title='Scatter Plot de Maturité par Thème', color_continuous_scale=colors['plotly'])
fig_box = px.box(data_for_plot, y='Moyenne', x='Theme', title='Box Plot de Maturité par Thème', color_discrete_sequence=colors['plotly'])
fig_hist = px.histogram(data_for_plot, x='Moyenne', nbins=20, title='Histogramme de Maturité', color_discrete_sequence=colors['plotly'])
fig_heatmap = px.imshow(df[[theme + ' Moyenne' for theme in themes]].corr(), labels={'x': 'Theme', 'y': 'Theme', 'color': 'Correlation'},
                        x=[theme + ' Moyenne' for theme in themes], y=[theme + ' Moyenne' for theme in themes],
                        title='Heatmap de Corrélation entre Thèmes', color_continuous_scale=colors['plotly'])
fig_radar = px.line_polar(data_for_plot, r='Moyenne', theta='Theme', line_close=True,
                          title='Radar Chart de Maturité par Thème', color_discrete_sequence=colors['plotly'])

# App layout
app = dash.Dash(__name__)
app.layout = html.Div(style={'backgroundColor': colors['background']}, children=[
    html.H1('Dashboard avec Graphiques', style={'textAlign': 'center', 'color': colors['text']}),
    dcc.Graph(figure=fig_bar),
    dcc.Graph(figure=fig_scatter),
    dcc.Graph(figure=fig_box),
    dcc.Graph(figure=fig_hist),
    dcc.Graph(figure=fig_heatmap),
    dcc.Graph(figure=fig_radar)
])

if __name__ == '__main__':
    app.run_server(debug=True)
