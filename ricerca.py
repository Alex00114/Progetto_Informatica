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



ProvinceGeo = geopandas.read_file('/workspace/Progetto_Informatica/templates/georef-italy-provincia-millesime.geojson')
ProvinceGeo.drop_duplicates(subset=["prov_name"])
province_name = list(ProvinceGeo["prov_name"])
coordinateReg = pd.read_csv('/workspace/Progetto_Informatica/static/csv/regioniCoord - Foglio1.csv')
Regioni = geopandas.read_file('/workspace/Progetto_Informatica/limits_IT_regions.geojson')
coordinateRegioniMerge = coordinateReg.merge(Regioni, how='inner', left_on='name', right_on='reg_name')

@app.route('/', methods=['GET'])
def mappaF():
  m = folium.Map(location=[41.2925, 12.5736], tiles="openstreetmap",zoom_start=6.3, min_zoom = 5)
  folium.GeoJson('/workspace/Progetto_Informatica/limits_IT_regions.geojson', name="geojson").add_to(m)
  folium.LayerControl().add_to(m)
  MousePosition().add_to(m)
  m.save('templates/map.html')


  return render_template('homeR.html')

@app.route('/map', methods=['GET'])
def png():
    
    return render_template("map.html")

@app.route('/ricerca', methods=['GET'])
def ricerca():
  reg_lista = list(Regioni["reg_name"])
  Regione7 = request.args["Cerca"]
  regione_richiesta = coordinateRegioniMerge[coordinateRegioniMerge.reg_name.str.contains(Regione7)]
  if Regione7 in reg_lista:
    latitudine = regione_richiesta["lat"]
    longitudine = regione_richiesta["lon"]
    m = folium.Map(location= [latitudine,longitudine], tiles="openstreetmap",zoom_start=9, min_zoom = 8)
    folium.LayerControl().add_to(m)
    MousePosition().add_to(m)
    m.save('templates/mappaRichiesta.html')
    return render_template('cerca.html')
  else:
    return '<h1>ERRORE</h1>'

@app.route('/mappaRichiesta', methods=['GET'])
def png2():
    
    return render_template("mappaRichiesta.html")








if __name__ == '__main__':
  app.run(host='0.0.0.0', port=3246, debug=True)