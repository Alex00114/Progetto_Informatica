from flask import Flask, render_template, request, send_file, make_response, url_for, Response, redirect
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
from folium.plugins import MousePosition


regioni = pd.read_csv('/workspace/Progetto_Informatica/static/csv/regioni - Foglio1.csv')
ProvinceGeo = geopandas.read_file('/workspace/Progetto_Informatica/templates/georef-italy-provincia-millesime.geojson')
ProvinceGeo.drop_duplicates(subset=["prov_name"])
province_name = list(ProvinceGeo["prov_name"])



@app.route('/', methods=['GET'])
def ricerca():
  m = folium.Map(location=[41.2925, 12.5736], tiles="openstreetmap",zoom_start=6.3, min_zoom = 5)
  folium.GeoJson('/workspace/Progetto_Informatica/limits_IT_regions.geojson', name="geojson").add_to(m)
  folium.LayerControl().add_to(m)
  MousePosition().add_to(m)

  m.save('templates/map.html')
  return render_template('homeR.html')

@app.route('/map', methods=['GET'])
def png():
    
    return render_template("map.html")

@app.route('/Province', methods=['GET'])
def Province():
  m = folium.Map(location=[41.2925, 12.5736], tiles="openstreetmap",zoom_start=6.3, min_zoom = 5)
  folium.GeoJson('/workspace/Progetto_Informatica/limits_IT_provinces.geojson', name="geojson").add_to(m)
  folium.LayerControl().add_to(m)
  MousePosition().add_to(m)

  m.save('templates/mappa.html')
  return render_template('homeR.html')

@app.route('/mappa', methods=['GET'])
def map_png():
    
    return render_template("mappa.html")
    





if __name__ == '__main__':
  app.run(host='0.0.0.0', port=3246, debug=True)