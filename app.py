# Copyright 2017 Jacques Berger
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for
from flask_sqlalchemy import SQLAlchemy
from .database import Database
from flask import g

app = Flask(__name__, template_folder="templates", static_folder="static")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
db = SQLAlchemy(app)


class Horaire(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    matricule = db.Column(db.String(6))
    code_de_projet = db.Column(db.String(15))
    date_publication = db.Column(db.String)
    duree = db.Column(db.Integer)


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        g._database = Database()
    return g._database


@app.errorhandler(404)
def page_not_found(error):
    return render_template("404.html"), 404


@app.route('/', methods=["GET", "POST"])
def formulaire():
    if request.method == "GET":
        return render_template("accueil.html")
    else:
        matricule_id = request.form["matricule_id"]
        date_du_jour = request.form["date_du_jour"]

        if matricule_id == "" or date_du_jour == "":
            error = "Veuillez insérer votre matricule."
            return render_template("accueil.html", error=error)
        else:
            return redirect(url_for('get_horaire', matricule_id=matricule_id, date_du_jour=date_du_jour))


@app.route('/<matricule_id>/<date_du_jour>')
def get_horaire(matricule_id, date_du_jour):
    db = get_db()
    heures = db.get_horaire(matricule_id, date_du_jour)

    return render_template("heures.html", matricule_id=matricule_id, date_du_jour=date_du_jour, heures=heures)


@app.route('/effacer', )
def delete_horaire():
    id = request.form["id"]
    matricule_id = request.form["matricule_id"]
    date_du_jour = request.form["date_du_jour"]
    db = get_db()
    db.delete_horaire(id)

    return redirect(url_for('get_horaire', matricule_id=matricule_id, date_du_jour=date_du_jour))


@app.route('/modifier', methods=["POST"])
def set_horaire():
    id = request.form["id"]
    matricule_id = request.form["matricule_id"]
    date_du_jour = request.form["date_du_jour"]
    db = get_db()
    db.set_horaire(id)

    return redirect(url_for('get_horaire', matricule_id=matricule_id, date_du_jour=date_du_jour))


@app.route('/inserer', methods=["POST"])
def insert_horaire():
    matricule_id = request.form["matricule_id"]
    date_du_jour = request.form["date_du_jour"]
    code_de_projet = request.form["code_de_projet"]
    duree = request.form["duree"]

    # Valider le formulaire et gérer les erreurs
    if (code_de_projet == "" or len(code_de_projet) > 15) or (duree == "" or type(duree) == 'int'):
        error = "Veuillez respecter les conditions du formulaire!"
        return redirect(url_for('get_horaire', matricule_id=matricule_id, date_du_jour=date_du_jour))

    db = get_db()
    db.create_horaire(matricule_id, code_de_projet, date_du_jour, duree)
    return redirect(url_for('get_horaire', matricule_id=matricule_id, date_du_jour=date_du_jour))
