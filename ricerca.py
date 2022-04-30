from flask import Flask, render_template, request, send_file, make_response, url_for, Response
app = Flask(__name__)
import io
import geopandas
import contextily
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import folium
import pandas as pd 
regioni = pd.read_csv('/workspace/Progetto_Informatica/static/csv/regioni - Foglio1.csv')

@app.route('/', methods=['GET'])
def ricerca():
    f = folium.Figure(width=2000, height=1000)
    m = folium.Map(location=[41.2925, 12.5736], tiles="openstreetmap",zoom_start=6, min_zoom = 5).add_to(f)
    
    return m._repr_html_()

    










if __name__ == '__main__':
  app.run(host='0.0.0.0', port=3246, debug=True)