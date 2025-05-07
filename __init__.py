from flask import Flask, render_template_string, render_template, jsonify
from flask import render_template
from flask import json
from datetime import datetime
from urllib.request import urlopen
import sqlite3
import requests 
                                                                                                                                       
app = Flask(__name__)                                                                                                                  
                                                                                                                                       
@app.route('/')
def hello_world():
    return render_template('hello.html') #comm2
  
@app.route("/contact/")
def MaPremiereAPI():
    return render_template("contact.html")


@app.route('/tawarano/')
def meteo():
    response = urlopen('https://samples.openweathermap.org/data/2.5/forecast?lat=0&lon=0&appid=xxx')
    raw_content = response.read()
    json_content = json.loads(raw_content.decode('utf-8'))
    results = []
    for list_element in json_content.get('list', []):
        dt_value = list_element.get('dt')
        temp_day_value = list_element.get('main', {}).get('temp') - 273.15  # Kelvin -> °C
        results.append({'Jour': dt_value, 'temp': temp_day_value})
    return jsonify(results=results)

@app.route("/rapport/")
def mongraphique():
    return render_template("graphique.html")

@app.route("/histogramme/")
def histogramme():
    return render_template("histogramme.html")

@app.route('/commits-data/')
def get_commits_data():
    # Requête à l'API GitHub pour obtenir la liste des commits du dépôt
    response = urlopen('https://api.github.com/repos/MassinissaBEY/5MCSI_Metriques/commits')
    raw_content = response.read()
    commits_data = json.loads(raw_content.decode('utf-8'))
    
    # Dictionnaire pour compter le nombre de commits par minute
    commit_minutes = {}
    
    # Analyse des dates des commits et regroupement à la minute près
    for commit in commits_data:
        commit_date = commit.get('commit', {}).get('author', {}).get('date')
        if commit_date:
            # Conversion de la chaîne de date en objet datetime
            date_object = datetime.strptime(commit_date, '%Y-%m-%dT%H:%M:%SZ')
            
            # Clé représentant l'instant à la minute près
            minute_key = f"{date_object.year}-{date_object.month:02d}-{date_object.day:02d} {date_object.hour:02d}:{date_object.minute:02d}"
            
            # Incrémentation du compteur pour cette minute
            if minute_key in commit_minutes:
                commit_minutes[minute_key] += 1
            else:
                commit_minutes[minute_key] = 1
    
    # Transformation des données en liste de dictionnaires pour l'affichage
    result = []
    for minute, count in commit_minutes.items():
        result.append({"minute": minute, "count": count})
    
    # Tri des résultats par ordre chronologique
    result = sorted(result, key=lambda x: x["minute"])
    
    return jsonify(results=result)

@app.route('/commits/')
def graph_commits():
    return render_template("commits.html")

  
  


 
if __name__ == "__main__":
  app.run(debug=True)
