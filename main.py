from flask import Flask, render_template, redirect, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import statistics

app = Flask(__name__)
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///dane.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = 'True'

db = SQLAlchemy(app)

class Dane(db.Model):
    __tablename__ = 'dane'
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.now)
    email = db.Column(db.String, nullable=False)
    rok = db.Column(db.Integer)
    lata = db.Column(db.String)
    czas = db.Column(db.Integer)
    spotkania = db.Column(db.Integer)
    tematyka = db.Column(db.Integer)

    def __init__(self, email, rok, lata, czas, spotkania, tematyka):
        self.email = email
        self.rok = rok
        self.lata = lata
        self.czas = czas
        self.spotkania = spotkania
        self.tematyka = tematyka

db.create_all()


@app.route("/")
def index():
    return render_template('index.html')

@app.route("/form")
def show_form():
    return render_template('form.html')

@app.route("/raw")
def show_raw():
    fd = db.session.query(Dane).all()
    return render_template('raw.html', dane=fd)


@app.route("/wyniki")
def show_result():
    fd_list = db.session.query(Dane).all()

    czas = []
    spotkania = []
    tematyka = []

    for el in fd_list:
        czas.append(int(el.czas))
        spotkania.append(int(el.spotkania))
        tematyka.append(int(el.tematyka))

    if len(czas) > 0:
        mean_czas = statistics.mean(czas)
    else:
       mean_czas = 0

    if len(spotkania) > 0:
        mean_spotkania = statistics.mean(spotkania)
    else:
        mean_spotkania = 0

    if len(tematyka) > 0:
        mean_tematyka = statistics.mean(tematyka)
    else:
        mean_tematyka = 0

    # Prepare data for google charts
    data = [['Python skill', mean_czas], ['Flask skill', mean_spotkania], ['Tematyka', mean_tematyka]]

    return render_template('wyniki.html', data=data)


@app.route("/save", methods=['POST'])
def save():
    # Get data from FORM
    email = request.form['email']
    rok = request.form['rok']
    lata = request.form['lata']
    czas = request.form['czas']
    spotkania = request.form['spotkania']
    tematyka = request.form['tematyka']


    # Save the data
    fd = Dane(email, rok, lata, czas, spotkania, tematyka)
    db.session.add(fd)
    db.session.commit()

    return redirect('/')


if __name__ == "__main__":
    app.debug = True
    app.run()