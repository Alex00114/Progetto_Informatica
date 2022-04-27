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
import random

regioni = geopandas.read_file("/workspace/Progetto_Informatica/Reg01012021_g_WGS84.zip")
regioni_name = list(regioni["DEN_REG"])


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
    global mappa_regione, risposta

    if volte >=1:
        risposta = request.args["Scelta"]

    unico = random.sample(range(0, 19), 4)
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
        mappa_regione = regioni[regioni["DEN_REG"] == opz1]
    elif opzioni == 1:
        opz1 = regioni_name[j]
        opz2 = regioni_name[i]
        opz3 = regioni_name[l]
        opz4 = regioni_name[k]
        mappa_regione = regioni[regioni["DEN_REG"] == opz2]
    elif opzioni == 2:
        opz1 = regioni_name[k]
        opz2 = regioni_name[j]
        opz3 = regioni_name[i]
        opz4 = regioni_name[l]
        mappa_regione = regioni[regioni["DEN_REG"] == opz3]
    else:
        opz1 = regioni_name[l]
        opz2 = regioni_name[k]
        opz3 = regioni_name[j]
        opz4 = regioni_name[i]
        mappa_regione = regioni[regioni["DEN_REG"] == opz4]

    punteggio = 0
    if volte >=1:
        if risposta == mappa_regione["DEN_REG"]:
            punteggio = punteggio + 1

    volte = volte + 1
    return render_template("quiz_facile.html", opzione1 = opz1, opzione2 = opz2, opzione3 = opz3, opzione4 = opz4, score = punteggio, name = nick)
    
@app.route('/regione_png', methods=['GET'])
def regione_png():
    fig, ax = plt.subplots(figsize = (12,8))

    mappa_regione.to_crs(epsg=3857).plot(ax=ax, color="c", edgecolor = "k")
    contextily.add_basemap(ax=ax)
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')




if __name__ == '__main__':
  app.run(host='0.0.0.0', port=3246, debug=True)