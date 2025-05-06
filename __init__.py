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
def commits_data():
    try:
        url = 'https://api.github.com/repos/OpenRSI/5MCSI_Metriques/commits'
        response = requests.get(url)
        response.raise_for_status()  # Déclenche une exception si erreur HTTP
        commits = response.json()

        minute_count = {}
        for commit in commits:
            date_str = commit.get("commit", {}).get("author", {}).get("date")
            if date_str:
                dt = datetime.strptime(date_str, '%Y-%m-%dT%H:%M:%SZ')
                minute = dt.strftime('%H:%M')
                minute_count[minute] = minute_count.get(minute, 0) + 1

        data = [{'minute': m, 'nb': c} for m, c in sorted(minute_count.items())]
        return jsonify(data=data)

    except Exception as e:
        # Affiche l'erreur dans la réponse pour t’aider à déboguer
        return jsonify(error=str(e)), 500

@app.route('/commits/')
def graph_commits():
    return render_template("commits.html")

  
  


 
if __name__ == "__main__":
  app.run(debug=True)
