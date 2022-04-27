from flask import Flask, render_template, request, send_file, make_response, url_for, Response,branca, jinja2, requests.
app = Flask(__name__)
import io
import geopandas
import contextily
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

regioni = geopandas.read_file("/workspace/Flask/Reg01012021_g_WGS84.zip")
province = geopandas.read_file("/workspace/Flask/ProvCM01012021_g_WGS84.zip")
comuni = geopandas.read_file("/workspace/Flask/Com01012021_g_WGS84.zip")

@app.route('/', methods=['GET'])
def homeR():
    return render_template('homeR.html')

@app.route('/ricerca', methods=['GET'])
def ricerca():
    










if __name__ == '__main__':
  app.run(host='0.0.0.0', port=3246, debug=True)