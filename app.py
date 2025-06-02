import dash
app = dash.Dash(__name__, assets_folder="assets",suppress_callback_exceptions=True )
application = app.server

app.title = 'Stock Analysis'
application = app.server