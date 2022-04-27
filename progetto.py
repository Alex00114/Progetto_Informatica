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


@app.route('/', methods=['GET'])
def home():
    return render_template('home.html')

@app.route('/registrazione', methods=['GET'])
def registrazione():
    return render_template('registrazione.html')

@app.route('/quiz', methods=['GET'])
def quiz():
    global nick, sesso, mappa_regione
    nick = request.args["Name"]
    sesso = request.args["Sex"]
    regioni_name = list(regioni["DEN_REG"])
    i = random.randint(0, 19)
    j = random.randint(0, 19)
    if j == i:
        j = random.randint(0, 19)
    k = random.randint(0, 19)
    if k == j or k == i:
        k = random.randint(0, 19)
    l = random.randint(0, 19)
    if l == j or l == i or l == k:
        l = random.randint(0, 19)
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
    return render_template("quiz.html", opzione1 = opz1, opzione2 = opz2, opzione3 = opz3, opzione4 = opz4)
    
@app.route('/regione_png', methods=['GET'])
def regione_png():
    fig, ax = plt.subplots(figsize = (12,8))

    mappa_regione.to_crs(epsg=3857).plot(ax=ax, color="c", edgecolor = "k")
    contextily.add_basemap(ax=ax)
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')

@app.route('/quiz2', methods=['GET'])
def quiz2():
    return render_template('quiz2.html')


if __name__ == '__main__':
  app.run(host='0.0.0.0', port=3246, debug=True)