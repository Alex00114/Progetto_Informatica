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


regioniData= pd.read_csv('/workspace/Progetto_Informatica/static/csv/regioni - Foglio1.csv')
coordinateReg = pd.read_csv('/workspace/Progetto_Informatica/static/csv/regioniCoord - Foglio1.csv')
coordinateProv = pd. read_csv('/workspace/Progetto_Informatica/static/csv/coorProv - Foglio1.csv')
Regioni = geopandas.read_file('/workspace/Progetto_Informatica/limits_IT_regions.geojson')
Province = geopandas.read_file('/workspace/Progetto_Informatica/limits_IT_provinces.geojson')
coordinateRegioniMerge = coordinateReg.merge(Regioni, how='inner', left_on='name', right_on='reg_name')
coorditateRegDatiMerge = coordinateRegioniMerge.merge(regioniData, how='inner', left_on='reg_name', right_on='Regione')
coordinateRegData = coordinateReg.merge(regioniData, how='inner', left_on='name', right_on='Regione')
coordinateProvinceMerge = coordinateProv.merge(Province, how='inner', left_on='Provincia', right_on='prov_name')

provdata = pd.read_csv('/workspace/Progetto_Informatica/ProvCM01012021_g_WGS84.zip')
print(provdata)

@app.route('/', methods=['GET'])
def mappaF():
  m = folium.Map(location=[41.2925, 12.5736], tiles="openstreetmap",zoom_start=6.3, min_zoom = 5)
  for index, row in coorditateRegDatiMerge.iterrows():
    iframe = folium.IFrame('Regione:' + str(row.loc['Regione']) + '<br>' + 'popolazione: ' + row.loc['Popolazione'] + '<br>' + 'Superficie km²: ' + str(row.loc['Superficie'])+ '<br>' + 'Densità abitanti/km²: ' + str(row.loc['Densità'])+ '<br>' + 'Numero Comuni: ' + str(row.loc['Numero_Comuni'])+ '<br>' + 'Numero Province: ' + str(row.loc['Numero_Province']))
    popup = folium.Popup(iframe, min_width=210, max_width=210)
    folium.Marker([row["lat"], row["lon"]], popup=popup).add_to(m)
    
  folium.GeoJson('/workspace/Progetto_Informatica/limits_IT_regions.geojson', name="geojson").add_to(m)
  folium.LayerControl().add_to(m)
  m.save('templates/map.html')
  return render_template('homeR.html')
  

@app.route('/map', methods=['GET'])
def png():\
    
    return render_template("map.html")

@app.route('/ricerca', methods=['GET'])
def ricerca():
  reg_lista = list(Regioni["reg_name"])
  Regione = request.args["Cerca"]
  regione_richiesta = Regioni[Regioni["reg_name"].str.contains(Regione)]
  regione_richiesta2 = coorditateRegDatiMerge[coorditateRegDatiMerge.reg_name.str.contains(Regione)]
  regione_richiesta_Data = regioniData[regioniData['Regione'].str.contains(Regione)]
  if Regione in reg_lista:
    latitudine = regione_richiesta2["lat"]
    longitudine = regione_richiesta2["lon"]
    m = folium.Map(location= [latitudine,longitudine], tiles="openstreetmap",zoom_start=9, min_zoom = 8)
    folium.GeoJson(regione_richiesta, name="geojson").add_to(m)

    folium.LayerControl().add_to(m)
    MousePosition().add_to(m)
    m.save('templates/mappaRichiesta.html')
    return render_template('cerca.html', table = regione_richiesta_Data.to_html())
  else:
    return '<h1>ERRORE</h1>'

@app.route('/mappaRichiesta', methods=['GET'])
def png2():
    
    return render_template("mappaRichiesta.html")






@app.route('/Province', methods=['GET'])
def Province1():
  m = folium.Map(location=[41.2925, 12.5736], tiles="openstreetmap",zoom_start=6.3, min_zoom = 5)
  for index, row in coordinateProvinceMerge.iterrows():
    folium.Marker([row["lat"], row["lon"]], popup=row['prov_name']).add_to(m)

  folium.GeoJson('/workspace/Progetto_Informatica/limits_IT_provinces.geojson', name="geojson").add_to(m)
  folium.LayerControl().add_to(m)
  m.save('templates/mappa.html')
  return render_template('province.html')

@app.route('/mappa', methods=['GET'])
def png3():\
    return render_template("mappa.html")

@app.route('/ricercaProv', methods=['GET'])
def ricercaProv():
  prov_lista = list(Province["prov_name"])
  
  Provincia = request.args["CercaProv"]
  
  if Provincia in prov_lista:
    provincia_richiesta = Province[Province["prov_name"].str.contains(Provincia)]
    provincia_richiesta2 = coordinateProvinceMerge[coordinateProvinceMerge.prov_name.str.contains(Provincia)]
    print(provincia_richiesta2)
    latitudine = provincia_richiesta2["lat"]
    longitudine = provincia_richiesta2["lon"]
    m = folium.Map(location= [latitudine,longitudine], tiles="openstreetmap",zoom_start=9, min_zoom = 8)
    folium.GeoJson(provincia_richiesta, name="geojson").add_to(m)

    folium.LayerControl().add_to(m)
    MousePosition().add_to(m)
    m.save('templates/mappaRichiestaProv.html')
    return render_template('cercaProv.html')
  else:
    return '<h1>ERRORE</h1>'

@app.route('/mappaRichiestaProv', methods=['GET'])
def png4():
    
    return render_template("mappaRichiestaProv.html")



if __name__ == '__main__':
  app.run(host='0.0.0.0', port=3246, debug=True)