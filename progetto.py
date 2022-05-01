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

regioni = geopandas.read_file("/workspace/Progetto_Informatica/Reg01012021_g_WGS84.zip")
regioni = regioni.to_crs(epsg=3857)
regioni_name = list(regioni["DEN_REG"])

province = geopandas.read_file("/workspace/Progetto_Informatica/templates/georef-italy-provincia-millesime.geojson")
province = province.to_crs(epsg=3857)
province.drop_duplicates(subset=["prov_name"])
province_name = list(province["prov_name"])
valore_max = len(province_name)

volte = 0
punteggio = 0


@app.route('/', methods=['GET'])
def home():
    return render_template('home.html')

@app.route('/registrazione', methods=['GET'])
def registrazione():
    return render_template('registrazione.html')

@app.route('/difficolta', methods=['GET'])
def difficolta():
    global nick, sesso

    nick = request.args["Name"]
    sesso = request.args["Sex"]
    return render_template('difficolta.html')

@app.route('/quiz_facile', methods=['GET'])
def quiz_facile():
    global mappa_quiz, risposta, volte, punteggio, corretta, valore_max
    regioni_province = random.randint(0,1)

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
        reg_provincia = regioni[regioni.contains(mappa_quiz.geometry.squeeze())]
        reg_provincia = 
        print(reg_provincia)
        testo = "Indovina la Provincia appartenente alla Regione " + ""

    if volte >=11:
        return redirect(url_for("risultato_facile"))

    return render_template("quiz_facile.html", opzione1 = opz1, opzione2 = opz2, opzione3 = opz3, opzione4 = opz4, score = punteggio, name = nick, text = testo)
    
@app.route('/regione_png', methods=['GET'])
def regione_png():
    fig, ax = plt.subplots(figsize = (12,8))

    mappa_quiz.to_crs(epsg=3857).plot(ax=ax, color="c", edgecolor = "k")
    contextily.add_basemap(ax=ax)
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')

@app.route('/risultato_facile', methods=['GET'])
def risultato_facile():
    return render_template('risultato_facile.html')


if __name__ == '__main__':
  app.run(host='0.0.0.0', port=3246, debug=True)