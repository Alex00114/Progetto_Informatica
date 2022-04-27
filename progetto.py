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
    global nick, sesso
    nick = request.args["Name"]
    sesso = request.args["Sex"]
    i = random.randint(0, 19)
    regioni_name = list(regioni["DEN_REG"])
    regione = regioni_name[i]
    mappa_regione = regioni[regioni["DEN_REG"] == regione]
    return render_template("quiz.html", text = regione)
    






if __name__ == '__main__':
  app.run(host='0.0.0.0', port=3246, debug=True)