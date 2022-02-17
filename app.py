from dash import Dash, html, dcc, Input, Output
import altair as alt
import pandas as pd


# Read data
vg_df = pd.read_csv("vgsales.csv")
vg_df = vg_df.groupby(['Year']).mean()
vg_df['Year'] = vg_df.index

chart = alt.Chart(vg_df).mark_line().encode(
    x=alt.X("Year", title="Year"),
    y=alt.Y("NA_Sales", title="Sales (in millions)")
)
chart

# Setup app and layout/frontend
app = Dash(__name__,  external_stylesheets=['https://codepen.io/chriddyp/pen/bWLwgP.css'])
server = app.server

app.layout = html.Div([
    html.Div('Video Game Sales By Region', style={'color': 'black', 'fontSize': 35}),
    html.Iframe(
        id='line',
        style={'border-width': '0', 'width': '100%', 'height': '400px'}),
    dcc.Dropdown(
        id='xcol-widget',
        value='NA_Sales',  # REQUIRED to show the plot on the first page load
        options=[{'label': col, 'value': col} for col in ['NA_Sales', 'EU_Sales', 'JP_Sales', 'Other_Sales',
       'Global_Sales']])])

# Set up callbacks/backend
@app.callback(
    Output('line', 'srcDoc'),
    Input('xcol-widget', 'value'))
def plot_altair(xcol):
    chart = alt.Chart(vg_df).mark_line().encode(
        x=alt.X("Year", title="Year"),
        y=alt.Y(xcol, title="Sales (in millions)")).interactive()
    return chart.to_html()

if __name__ == '__main__':
    app.run_server(debug=True)