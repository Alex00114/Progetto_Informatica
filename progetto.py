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
import random
import pandas as pd 
import folium
from folium.plugins import MousePosition

regioni = geopandas.read_file("/workspace/Progetto_Informatica/Reg01012021_g_WGS84.zip")
regioni_name = list(regioni["DEN_REG"])

province = geopandas.read_file("/workspace/Progetto_Informatica/limits_IT_provinces.geojson")
province = province.to_crs(epsg=32632)
province_name = list(province["prov_name"])
valore_max = len(province_name)

regioniData= pd.read_csv('/workspace/Progetto_Informatica/static/csv/regioni - Foglio1.csv')
coordinateReg = pd.read_csv('/workspace/Progetto_Informatica/static/csv/regioniCoord - Foglio1.csv')
coordinateProv = pd. read_csv('/workspace/Progetto_Informatica/static/csv/coordonteGiusteProv - Foglio1.csv')
Regioni = geopandas.read_file('/workspace/Progetto_Informatica/limits_IT_regions.geojson')
coordinateRegioniMerge = coordinateReg.merge(Regioni, how='inner', left_on='name', right_on='reg_name')
coorditateRegDatiMerge = coordinateRegioniMerge.merge(regioniData, how='inner', left_on='reg_name', right_on='Regione')
coordinateRegData = coordinateReg.merge(regioniData, how='inner', left_on='name', right_on='Regione')
coordinateProvinceMerge = coordinateProv.merge(province, how='inner', left_on='Provincia', right_on='prov_name')
provdata = pd.read_csv('/workspace/Progetto_Informatica/static/csv/prov - Foglio1.csv')
coorditateProvDatiMerge = coordinateProvinceMerge.merge(provdata, how='inner', left_on='prov_name', right_on='Provinca')

dati = pd.read_csv("/workspace/Progetto_Informatica/static/csv/dati.csv")

volte = 0
domanda = 0
punteggio = 0

@app.route('/', methods=['GET', 'POST'])
def registrazione():
    global user

    if request.method == 'GET':
        return render_template('registrazione.html')
    else:
        nick = request.form.get("Nick")
        email = request.form.get("Email")
        password = request.form.get("Password")
        c_password = request.form.get("Cpassword")
        
    user = [{"nick": nick, "email": email, "password": password}]
    
    if password != c_password:
        return render_template('registrazione_errore.html')
    else:
        dati_append = dati.append(user,ignore_index=True)
        dati_append.to_csv("/workspace/Progetto_Informatica/static/csv/dati.csv",index=False)
        return render_template('login.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    global utente
    dati = pd.read_csv("/workspace/Progetto_Informatica/static/csv/dati.csv")
    if request.method == 'GET':
        return render_template('login.html')
    elif request.method == 'POST':
        utente  = request.form.get("Nick")
        password = request.form.get("Password")
        email = request.form.get("Email")
        for i, d in dati.iterrows():
            if email == d["email"] and password == d["password"] and utente == d["nick"]:  
                return redirect(url_for("home"))
                
        return render_template('login_errore.html', nome = utente)

@app.route('/home', methods=['GET'])
def home():
    global utente, volte, domanda, punteggio

    punteggio = 0
    domanda = 0
    volte = 0
    return render_template('home.html', nome = utente)

@app.route('/difficolta', methods=['GET'])
def difficolta():
    diff = request.args["Diff"]
    if diff == "Facile":
        return redirect(url_for("quiz_facile"))
    else:
        return redirect(url_for("quiz_difficile"))

@app.route('/quiz_facile', methods=['GET'])
def quiz_facile():
    global mappa_quiz, risposta, volte, punteggio, corretta, valore_max, regioni, domanda, regioni_name, reg_provincia, utente
    regioni_province = random.randint(0,1)

    if volte == 0:
        punteggio = 0

    if volte >=0:
        volte = volte + 1

    if volte >=2:
        risposta = request.args["Scelta"]
        if risposta in corretta:
            punteggio = punteggio + 1

    if regioni_province == 0:
        testo = "Indovina la Regione!"
        unico = random.sample(range(0, 20), 4)
        i = unico[0]
        j = unico[1]
        k = unico[2]
        l = unico[3]

        opzioni = random.randint(0, 3)
        if opzioni == 0:
            opz1 = regioni_name[i]
            opz2 = regioni_name[j]
            opz3 = regioni_name[k]
            opz4 = regioni_name[l]
            mappa_quiz = regioni[regioni["DEN_REG"] == opz1]
            corretta = opz1
        elif opzioni == 1:
            opz1 = regioni_name[j]
            opz2 = regioni_name[i]
            opz3 = regioni_name[l]
            opz4 = regioni_name[k]
            mappa_quiz = regioni[regioni["DEN_REG"] == opz2]
            corretta = opz2
        elif opzioni == 2:
            opz1 = regioni_name[k]
            opz2 = regioni_name[j]
            opz3 = regioni_name[i]
            opz4 = regioni_name[l]
            mappa_quiz = regioni[regioni["DEN_REG"] == opz3]
            corretta = opz3
        else:
            opz1 = regioni_name[l]
            opz2 = regioni_name[k]
            opz3 = regioni_name[j]
            opz4 = regioni_name[i]
            mappa_quiz = regioni[regioni["DEN_REG"] == opz4]
            corretta = opz4
    else:
        unico = random.sample(range(0, valore_max), 4)
        i = unico[0]
        j = unico[1]
        k = unico[2]
        l = unico[3]

        opzioni = random.randint(0, 3)
        if opzioni == 0:
            opz1 = province_name[i]
            opz2 = province_name[j]
            opz3 = province_name[k]
            opz4 = province_name[l]
            mappa_quiz = province[province["prov_name"] == opz1]
            corretta = opz1
        elif opzioni == 1:
            opz1 = province_name[j]
            opz2 = province_name[i]
            opz3 = province_name[l]
            opz4 = province_name[k]
            mappa_quiz = province[province["prov_name"] == opz2]
            corretta = opz2
        elif opzioni == 2:
            opz1 = province_name[k]
            opz2 = province_name[j]
            opz3 = province_name[i]
            opz4 = province_name[l]
            mappa_quiz = province[province["prov_name"] == opz3]
            corretta = opz3
        else:
            opz1 = province_name[l]
            opz2 = province_name[k]
            opz3 = province_name[j]
            opz4 = province_name[i]
            mappa_quiz = province[province["prov_name"] == opz4]
            corretta = opz4
        
        
        reg_provincia = mappa_quiz["reg_name"].values[0]        
        testo =  "La provincia appartiene alla regione " + str(reg_provincia)

    domanda = domanda + 1
    if volte >=11:
        return redirect(url_for("risultato_facile"))

    return render_template("quiz_facile.html", opzione1 = opz1, opzione2 = opz2, opzione3 = opz3, opzione4 = opz4, score = punteggio, text = testo, question = domanda, nome = utente)

@app.route('/quiz_difficile', methods=['GET'])
def quiz_difficile():
    global mappa_quiz, risposta, volte, punteggio, corretta, valore_max, regioni, domanda, utente
    regioni_province = random.randint(0,1)

    if volte == 0:
        punteggio = 0
        
    if volte >=0:
        volte = volte + 1

    if volte >=2:
        risposta = request.args["Scelta"]
        if risposta in corretta:
            punteggio = punteggio + 1

    if regioni_province == 0:
        testo = "Indovina la Regione!"
        unico = random.sample(range(0, 20), 4)
        i = unico[0]
        j = unico[1]
        k = unico[2]
        l = unico[3]

        opzioni = random.randint(0, 3)
        if opzioni == 0:
            opz1 = regioni_name[i]
            opz2 = regioni_name[j]
            opz3 = regioni_name[k]
            opz4 = regioni_name[l]
            mappa_quiz = regioni[regioni["DEN_REG"] == opz1]
            corretta = opz1
        elif opzioni == 1:
            opz1 = regioni_name[j]
            opz2 = regioni_name[i]
            opz3 = regioni_name[l]
            opz4 = regioni_name[k]
            mappa_quiz = regioni[regioni["DEN_REG"] == opz2]
            corretta = opz2
        elif opzioni == 2:
            opz1 = regioni_name[k]
            opz2 = regioni_name[j]
            opz3 = regioni_name[i]
            opz4 = regioni_name[l]
            mappa_quiz = regioni[regioni["DEN_REG"] == opz3]
            corretta = opz3
        else:
            opz1 = regioni_name[l]
            opz2 = regioni_name[k]
            opz3 = regioni_name[j]
            opz4 = regioni_name[i]
            mappa_quiz = regioni[regioni["DEN_REG"] == opz4]
            corretta = opz4
    else:
        unico = random.sample(range(0, valore_max), 4)
        i = unico[0]
        j = unico[1]
        k = unico[2]
        l = unico[3]

        opzioni = random.randint(0, 3)
        if opzioni == 0:
            opz1 = province_name[i]
            opz2 = province_name[j]
            opz3 = province_name[k]
            opz4 = province_name[l]
            mappa_quiz = province[province["prov_name"] == opz1]
            corretta = opz1
        elif opzioni == 1:
            opz1 = province_name[j]
            opz2 = province_name[i]
            opz3 = province_name[l]
            opz4 = province_name[k]
            mappa_quiz = province[province["prov_name"] == opz2]
            corretta = opz2
        elif opzioni == 2:
            opz1 = province_name[k]
            opz2 = province_name[j]
            opz3 = province_name[i]
            opz4 = province_name[l]
            mappa_quiz = province[province["prov_name"] == opz3]
            corretta = opz3
        else:
            opz1 = province_name[l]
            opz2 = province_name[k]
            opz3 = province_name[j]
            opz4 = province_name[i]
            mappa_quiz = province[province["prov_name"] == opz4]
            corretta = opz4
        
    
        testo =  "Indovina la Provincia!"
    domanda = domanda + 1
    if volte >=11:
        return redirect(url_for("risultato_difficile"))

    return render_template("quiz_difficile.html", opzione1 = opz1, opzione2 = opz2, opzione3 = opz3, opzione4 = opz4, score = punteggio, text = testo, question = domanda, nome = utente)
    
@app.route('/quiz_difficile2', methods=['GET'])
def quiz_difficile2():
    global mappa_quiz, risposta, volte, punteggio, corretta, valore_max, regioni, domanda, utente
    regioni_province = random.randint(0,1)

    if volte == 0:
        punteggio = 0

    if volte >=0:
        volte = volte + 1

    if volte >=2:
            punteggio = punteggio + 0

    if regioni_province == 0:
        testo = "Indovina la Regione!"
        unico = random.sample(range(0, 20), 4)
        i = unico[0]
        j = unico[1]
        k = unico[2]
        l = unico[3]

        opzioni = random.randint(0, 3)
        if opzioni == 0:
            opz1 = regioni_name[i]
            opz2 = regioni_name[j]
            opz3 = regioni_name[k]
            opz4 = regioni_name[l]
            mappa_quiz = regioni[regioni["DEN_REG"] == opz1]
            corretta = opz1
        elif opzioni == 1:
            opz1 = regioni_name[j]
            opz2 = regioni_name[i]
            opz3 = regioni_name[l]
            opz4 = regioni_name[k]
            mappa_quiz = regioni[regioni["DEN_REG"] == opz2]
            corretta = opz2
        elif opzioni == 2:
            opz1 = regioni_name[k]
            opz2 = regioni_name[j]
            opz3 = regioni_name[i]
            opz4 = regioni_name[l]
            mappa_quiz = regioni[regioni["DEN_REG"] == opz3]
            corretta = opz3
        else:
            opz1 = regioni_name[l]
            opz2 = regioni_name[k]
            opz3 = regioni_name[j]
            opz4 = regioni_name[i]
            mappa_quiz = regioni[regioni["DEN_REG"] == opz4]
            corretta = opz4
    else:
        unico = random.sample(range(0, valore_max), 4)
        i = unico[0]
        j = unico[1]
        k = unico[2]
        l = unico[3]

        opzioni = random.randint(0, 3)
        if opzioni == 0:
            opz1 = province_name[i]
            opz2 = province_name[j]
            opz3 = province_name[k]
            opz4 = province_name[l]
            mappa_quiz = province[province["prov_name"] == opz1]
            corretta = opz1
        elif opzioni == 1:
            opz1 = province_name[j]
            opz2 = province_name[i]
            opz3 = province_name[l]
            opz4 = province_name[k]
            mappa_quiz = province[province["prov_name"] == opz2]
            corretta = opz2
        elif opzioni == 2:
            opz1 = province_name[k]
            opz2 = province_name[j]
            opz3 = province_name[i]
            opz4 = province_name[l]
            mappa_quiz = province[province["prov_name"] == opz3]
            corretta = opz3
        else:
            opz1 = province_name[l]
            opz2 = province_name[k]
            opz3 = province_name[j]
            opz4 = province_name[i]
            mappa_quiz = province[province["prov_name"] == opz4]
            corretta = opz4
        
        testo =  "Indovina la Provincia!"
        
    domanda = domanda + 1
    if volte >=11:
        return redirect(url_for("risultato_difficile"))

    return render_template("quiz_difficile.html", opzione1 = opz1, opzione2 = opz2, opzione3 = opz3, opzione4 = opz4, score = punteggio, text = testo, question = domanda, nome = utente)

@app.route('/regione_png', methods=['GET'])
def regione_png():
    fig, ax = plt.subplots(figsize = (12,8), facecolor = "cyan")

    mappa_quiz.to_crs(epsg=3857).plot(ax=ax, color="deepskyblue", edgecolor = "k")
    contextily.add_basemap(ax=ax)
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')

@app.route('/risultato_facile', methods=['GET'])
def risultato_facile():
    global utente, volte, domanda, punteggio
    domanda = 0
    volte = 0

    if punteggio >= 0 and punteggio <= 4:
        testo = "La geografia non è proprio il tuo forte, forse dovresti concentrarti su altro"
        testo_link = "In caso tu voglia riprovare Clicca Qui!"
        return render_template('risultato_facileMale.html', user = utente, text= testo, text_link = testo_link, punti = int(punteggio))
    elif punteggio >= 5 and punteggio <= 7:
        testo = "Sicuramente la geografia non è la tua passione principale, ma sei comunque riuscito a totalizzare un punteggio discreto"
        testo_link = "Ti consigliamo di riprovare, puoi sicuramente fare di meglio!"
        return render_template('risultato_facileMedio.html', user = utente, text= testo, text_link = testo_link, punti = int(punteggio))
    else:
        testo = "Sei un vero asso per quanto riguarda la geografia dell'Italia"
        testo_link = "Ti consigliamo di metterti alla prova con la modalità difficile!"
        return render_template('risultato_facileBene.html', user = utente, text= testo, text_link = testo_link, punti = int(punteggio))


@app.route('/risultato_difficile', methods=['GET'])
def risultato_difficile():
    global utente, volte, domanda, punteggio
    domanda = 0
    volte = 0

    if punteggio >= 0 and punteggio <= 4:
        testo = "La geografia non è proprio il tuo forte, forse dovresti concentrarti su altro"
        testo_link = "Ti consigliamo vivamente di provare la modalità facile"
        return render_template('risultato_difficileMale.html', user = utente, text= testo, text_link = testo_link, punti = int(punteggio))
    elif punteggio >= 5 and punteggio <= 7:
        testo = "Sicuramente la geografia non è la tua passione principale, ma sei comunque riuscito a totalizzare un punteggio discreto"
        testo_link = "Ti consigliamo di riprovare, puoi sicuramente fare di meglio!"
        return render_template('risultato_difficileMedio.html', user = utente, text= testo, text_link = testo_link, punti = int(punteggio))
    else:
        testo = "Sei un vero asso per quanto riguarda la geografia dell'Italia"
        testo_link = "In caso tu voglia rigiocare Clicca Qui!"
        return render_template('risultato_difficileBene.html', user = utente, text= testo, text_link = testo_link, punti = int(punteggio))


@app.route('/explore', methods=['GET'])
def mappaF():
  m = folium.Map(location=[41.2925, 12.5736], tiles="openstreetmap",zoom_start=6.3, min_zoom = 5)
  for index, row in coorditateRegDatiMerge.iterrows():
    iframe = folium.IFrame('Regione:' + str(row.loc['Regione']) + '<br>' + 'popolazione: ' + row.loc['Popolazione'] + '<br>' + 'Superfice km²: ' + str(row.loc['Superficie'])+ '<br>' + 'Densità abitanti/km²: ' + str(row.loc['Densità'])+ '<br>' + 'Numero Comuni: ' + str(row.loc['Numero_Comuni'])+ '<br>' + 'Numero province: ' + str(row.loc['Numero_Province']))
    popup = folium.Popup(iframe, min_width=210, max_width=210)
    folium.Marker([row["lat"], row["lon"]], popup=popup).add_to(m)
    
  folium.GeoJson('/workspace/Progetto_Informatica/limits_IT_regions.geojson', name="geojson").add_to(m)
  folium.LayerControl().add_to(m)
  m.save('templates/map.html')
  return render_template('regioni.html')
  
@app.route('/map', methods=['GET'])
def png():\
    return render_template("map.html")

@app.route('/ricerca', methods=['GET'])
def ricerca():
  reg_lista = list(Regioni["reg_name"])
  reg_lista2 = [i.split('-', 1)[0] for i in reg_lista]

  Regione = request.args["Cerca"].title()
  regione_richiesta = Regioni[Regioni["reg_name"].str.contains(Regione)]
  regione_richiesta2 = coorditateRegDatiMerge[coorditateRegDatiMerge.reg_name.str.contains(Regione)]
  regione_richiesta_Data = regioniData[regioniData['Regione'].str.contains(Regione)]
  if Regione in reg_lista2 or Regione in reg_lista:
    latitudine = regione_richiesta2["lat"]
    longitudine = regione_richiesta2["lon"]
    m = folium.Map(location= [latitudine,longitudine], tiles="openstreetmap",zoom_start=9, min_zoom = 8)
    folium.GeoJson(regione_richiesta, name="geojson").add_to(m)

    folium.LayerControl().add_to(m)
    MousePosition().add_to(m)
    m.save('templates/mappaRichiesta.html')
    return render_template('cerca.html', table = regione_richiesta_Data.to_html())
  else:
    return render_template('regioni_errore.html')

@app.route('/mappaRichiesta', methods=['GET'])
def png2():
    return render_template("mappaRichiesta.html")

@app.route('/province', methods=['GET'])
def Province1():
  m = folium.Map(location=[41.2925, 12.5736], tiles="openstreetmap",zoom_start=6.3, min_zoom = 5)
  for index, row in coorditateProvDatiMerge.iterrows():
    iframe = folium.IFrame('Provincia:' + str(row.loc['Provinca']) + '<br>' + 'popolazione: ' + row.loc['Residenti'] + '<br>' + 'Superfice km²: ' + str(row.loc['Superfice'])+ '<br>' + 'numero comuni: ' + str(row.loc['numero comuni'])+ '<br>' + 'Sigla: ' + str(row.loc['Sigla']))
    popup = folium.Popup(iframe, min_width=175, max_width=175, min_height=300, max_height=300)
    folium.Marker([row["Lat"], row["Lon"]], popup=popup).add_to(m)

  folium.GeoJson('/workspace/Progetto_Informatica/limits_IT_provinces.geojson', name="geojson").add_to(m)
  folium.LayerControl().add_to(m)
  m.save('templates/mappa.html')
  return render_template('province.html')

@app.route('/mappa', methods=['GET'])
def png3():\
    return render_template("mappa.html")

@app.route('/ricercaProv', methods=['GET'])
def ricercaProv():
  prov_lista = list(province["prov_name"])
  
  Provincia = request.args["CercaProv"]
  
  if Provincia in prov_lista:
    provincia_richiesta = province[province["prov_name"].str.contains(Provincia)]
    provincia_richiesta2 = coordinateProvinceMerge[coordinateProvinceMerge.prov_name.str.contains(Provincia)]
    provincia_richiesta_Data = provdata[provdata['Provinca'].str.contains(Provincia)]
    print(provincia_richiesta2)
    latitudine = provincia_richiesta2["Lat"]
    longitudine = provincia_richiesta2["Lon"]
    m = folium.Map(location= [latitudine,longitudine], tiles="openstreetmap",zoom_start=9, min_zoom = 8)
    folium.GeoJson(provincia_richiesta, name="geojson").add_to(m)

    folium.LayerControl().add_to(m)
    MousePosition().add_to(m)
    m.save('templates/mappaRichiestaProv.html')
    return render_template('cercaProv.html', table = provincia_richiesta_Data.to_html())
  else:
    return render_template('province_errore.html')

@app.route('/mappaRichiestaProv', methods=['GET'])
def png4():
    return render_template("mappaRichiestaProv.html")

if __name__ == '__main__':
  app.run(host='0.0.0.0', port=3246, debug=True)