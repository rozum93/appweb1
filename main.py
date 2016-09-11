from flask import Flask, render_template, redirect, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import statistics

app = Flask(__name__)
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
    organizacja = db.Column(db.String)
    czas = db.Column(db.Integer)
    spotkania = db.Column(db.Integer)
    tematyka = db.Column(db.Integer)

    def __init__(self, email, rok, lata, organizacja, czas, spotkania, tematyka):
        self.email = email
        self.rok = rok
        self.lata = lata
        self.organizacja = organizacja
        self.czas = czas
        self.spotkania = spotkania
        self.tematyka = tematyka

db.create_all()

@app.route("/")
def index():
    return render_template('witaj.html')

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

    czas = [0, 0, 0, 0]
    spotkania = [0, 0, 0, 0, 0]
    tematyka =  [0, 0, 0, 0, 0, 0, 0, 0]

    for el in fd_list:
        czas[el.czas-1] =+ 1
        spotkania[el.spotkania-1] =+ 1
        tematyka[el.tematyka-1] =+ 1



    print(spotkania)
    timeData = [["Kilka godzin w roku", czas[0]], ["Kilka godzin w miesiacu", czas[1]], ["Kilka godzin w tygodniu", czas[2]], ["Kilka godzin dziennie", czas[3]]]
    meetingsData = [["Kilka razy w tygodniu", spotkania[0]], ["Raz w tygodniu", spotkania[1]], ["Kilka razy w miesiacu", spotkania[2]], ["Raz w miesiacu", spotkania[3]], ["Mniej niz raz w miesiacu", spotkania[4]]]
    topicData = [["Naukowo-techniczna", tematyka[0]], ["Soft-skills", tematyka[1]], ["Artystyczna", tematyka[2]], ["Sportowa", tematyka[3]], ["Kulturalno-rozrywkowa", tematyka[4]], ["Samorzadowa", tematyka[5]], ["Wolontariat/Pomoc spoleczna", tematyka[6]], ["Inna", tematyka[7]]]


    print(timeData)
    return render_template('wyniki.html', timeData=timeData, meetingsData=meetingsData, topicData=topicData)


@app.route("/save", methods=['POST'])
def save():
    # Get data from FORM
    email = request.form['email']
    rok = request.form['rok']
    lata = request.form['lata']
    organizacja = request.form['organizacja']
    czas = request.form['czas']
    spotkania = request.form['spotkania']
    tematyka = request.form['tematyka']


    # Save the data
    fd = Dane(email, rok, lata, organizacja, czas, spotkania, tematyka)
    db.session.add(fd)
    db.session.commit()

    return redirect('/')


if __name__ == "__main__":
    app.debug = True
    app.run()