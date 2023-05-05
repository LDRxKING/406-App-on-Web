import pandas as pd
import dash
import plotly.express as px
from dash import Dash, html, Input, Output, State, dcc, ctx
import dash_bootstrap_components as dbc
import csv
from pathlib import Path


dir_main=pathlib.Path(__file__).parent
file=dir_main/'USA_cars_dataset'


file_path = Path('C:/Users/switz/OneDrive/Desktop/Python Code/USA_cars_datasets.csv')

usa_cars_data= pd.read_csv(file_path)


usa_cars_data.head

name_columns_to_drop = [
    'vin',
    'color',
    'lot',
    'title_status',
    'model',
    'condition',
]

columns_to_drop = name_columns_to_drop

usa_cars_data.drop(columns=columns_to_drop,inplace=True)

usa_cars_data


layout_1 = html.Div([
    html.H1('Choropleth Map'),
    dcc.Graph(id='choropleth-map'),
    dcc.Dropdown(
        id='dropdownc',
        options=[{'label': brand, 'value': brand} for brand in usa_cars_data['brand'].unique()],
        placeholder='Select a brand'
    ),
    dcc.Link('Go to Scatter Plot', href='/second-page')
])

layout_2 = html.Div([
    html.H1('Scatter Plot'),
    dcc.Graph(id='scatter-plot'),
    dcc.Dropdown(
        id='dropdown',
        options=[{'label': brand, 'value': brand} for brand in usa_cars_data['brand'].unique()],
        placeholder='Select a brand'
    ),
    dcc.Link('Go to Choropleth Map', href='/')
])

app = Dash(__name__, external_stylesheets=[dbc.themes.VAPOR],use_pages=True,pages_folder='')
app.title='Multi-Page'



dash.register_page("First-page",path='/',layout=layout_1),
dash.register_page("second-page",layout=layout_2),


# map_dropdown=dcc.Dropdown(
#         id='dropdownc',
#         options=[{'label': brand, 'value': brand} for brand in usa_cars_data['brand'].unique()],
#         placeholder='Select a brand'
# )



app.layout = dbc.Container(
    children=[
      dbc.NavbarSimple(
        brand='Multi-Page Setup',
        children=[
            dbc.NavItem(dbc.NavLink('Page 1',href='/')),
            dbc.NavItem(dbc.NavLink('Page 2',href='/second-page')),
        ],
        color='primary',
        dark=True,
      ),
      dash.page_container,
    ],
    fluid=True,
    class_name='px-0',
)



@app.callback(
        Output('scatter-plot', 'figure'),
        Input('dropdown', 'value'))
def update_scatter_plot(selected_brand):
    if selected_brand is None:
        filtered_data = usa_cars_data
    else:
        filtered_data = usa_cars_data[usa_cars_data['brand'] == selected_brand]
    
    
    fig = px.scatter(filtered_data, 
        x='mileage', 
        y='price', 
        color='brand', 
        title='Mileage vs. Price by Brand',
        hover_data={'price': ':.2f', 'brand': True, 'mileage': True})
    
    return fig


@app.callback(
        Output('choropleth-map', 'figure'),
        Input('dropdownc', 'value'))
def update_choropleth_map(selected_brand):
    if selected_brand is None:
        filtered_data = usa_cars_data
    else:
        filtered_data = usa_cars_data[usa_cars_data['brand'] == selected_brand]
    

    figc = px.choropleth(filtered_data, locations='state', locationmode="USA-states", color='price', scope="usa", 
                        color_continuous_scale=px.colors.sequential.Plasma, title='Price by State and Brand', 
                        hover_data={'price': ':.2f', 'brand': True, 'state': True})
    
    return figc

states_list = ['AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'FL', 'GA', 'HI', 'ID', 'IL', 'IN', 'IA', 'KS', 'KY',
             'LA', 'ME', 'MD', 'MA', 'MI', 'MN', 'MS', 'MO', 'MT', 'NE', 'NV', 'NH', 'NJ', 'NM', 'NY', 'NC', 'ND', 'OH', 'OK',
               'OR', 'PA', 'RI', 'SC', 'SD', 'TN', 'TX', 'UT', 'VT', 'VA', 'WA', 'WV', 'WI', 'WY']


random_data = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25,
         26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50]

df = pd.DataFrame({'state': states_list, 'random_data': random_data})
df





if __name__ == '__main__':
    app.run_server(debug=True)





























