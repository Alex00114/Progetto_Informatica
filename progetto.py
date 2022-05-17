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

regioni = geopandas.read_file("/workspace/Progetto_Informatica/Reg01012021_g_WGS84.zip")
regioni_name = list(regioni["DEN_REG"])

province = geopandas.read_file("/workspace/Progetto_Informatica/limits_IT_provinces.geojson")
province = province.to_crs(epsg=32632)
province_name = list(province["prov_name"])
valore_max = len(province_name)

dati = pd.read_csv("/workspace/Progetto_Informatica/static/csv/dati.csv")

volte = 0
domanda = 0
punteggio = 0


@app.route('/', methods=['GET'])
def home():
    return render_template('home.html')

# @app.route('/accedi', methods=['GET'])
# def accedi():
#    return render_template('accedi.html')


@app.route('/registrazione', methods=['GET', 'POST'])
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
        return 'Le password non corrispondono'
    else:
        dati_append = dati.append(user,ignore_index=True)
        dati_append.to_csv("/workspace/Progetto_Informatica/static/csv/dati.csv",index=False)
        return render_template('login.html')

@app.route('/login', methods=['GET', 'POST'])
def login():

        if request.method == 'GET':
            return render_template('login.html')
        elif request.method == 'POST':
            password = request.form.get("Password")
            email = request.form.get("Email")
            for i, d in dati.iterrows():
                if email == d["email"] and password == d["password"]:  
                    return '<h1>Login</h1>'

            return '<h1>Errore</h1>'

@app.route('/difficolta', methods=['GET'])
def difficolta():
    diff = request.args["Diff"]
    if diff == "Facile":
        return redirect(url_for("quiz_facile"))
    else:
        return redirect(url_for("quiz_difficile"))

@app.route('/quiz_facile', methods=['GET'])
def quiz_facile():
    global mappa_quiz, risposta, volte, punteggio, corretta, valore_max, regioni, domanda, regioni_name, reg_provincia
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
        
        
        reg_provincia = mappa_quiz["reg_name"].values[0]        
        testo =  "La provincia appartiene alla regione " + str(reg_provincia)

    domanda = domanda + 1
    if volte >=11:
        return redirect(url_for("risultato_facile"))

    return render_template("quiz_facile.html", opzione1 = opz1, opzione2 = opz2, opzione3 = opz3, opzione4 = opz4, score = punteggio, text = testo, question = domanda)

@app.route('/quiz_difficile', methods=['GET'])
def quiz_difficile():
    global mappa_quiz, risposta, volte, punteggio, corretta, valore_max, regioni, domanda
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
        
        domanda = domanda + 1
        testo =  "Indovina la Provincia!"
    if volte >=11:
        return redirect(url_for("risultato_difficile"))

    return render_template("quiz_difficile.html", opzione1 = opz1, opzione2 = opz2, opzione3 = opz3, opzione4 = opz4, score = punteggio, text = testo, question = domanda)
    
@app.route('/quiz_difficile2', methods=['GET'])
def quiz_difficile2():
    global mappa_quiz, risposta, volte, punteggio, corretta, valore_max, regioni, domanda
    regioni_province = random.randint(0,1)

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
        
        domanda = domanda + 1
        testo =  "Indovina la Provincia!"
    if volte >=11:
        return redirect(url_for("risultato_difficile"))

    return render_template("quiz_difficile.html", opzione1 = opz1, opzione2 = opz2, opzione3 = opz3, opzione4 = opz4, score = punteggio, text = testo, question = domanda)

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