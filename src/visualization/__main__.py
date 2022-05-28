from dash import Dash, dcc, Output, Input, html
import src.sqlconnection
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd

sqlconnection = src.sqlconnection.connector
sqlquery = src.sqlconnection.sqlquery



app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
mytitle = dcc.Markdown(children='# Total 20 spenders')
mygraph = dcc.Graph(figure={})
dropdown = dcc.Dropdown(options=['Bar Plot', 'Pie Chart'],
                        value='Bar Plot',  # initial value displayed when page first loads
                        clearable=False)
app.layout = dbc.Container([mytitle, mygraph, dropdown])

@app.callback(
    Output(mygraph, component_property='figure'),
    Input(dropdown, component_property='value')
)
def update_graph(user_input):  # function arguments come from the component property of the Input
    with sqlconnection() as connection:
        rows = sqlquery(connection).revenueplotquery()
    df = pd.DataFrame(rows, columns=['mainorg', 'value'])
    if user_input == 'Bar Plot':
        fig = px.bar(data_frame=df, x="mainorg", y="value")

    elif user_input == 'Pie Chart':
        fig = px.pie(data_frame=df, values="value", names="mainorg")

    return fig  # returned objects are assigned to the component property of the Output

if __name__=='__main__':
    app.run_server(host= '0.0.0.0', port=8052)