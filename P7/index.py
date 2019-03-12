from flask import Flask, render_template, request, make_response
from random import randint
from time import time

import datetime
import sklearn
from sklearn.externals import joblib

from operation import Operation


app = Flask(__name__)

@app.route("/")
def main():
    return render_template("main.html")

@app.route("/renderloginsencillo", methods=['GET','POST'])
def renderloginsencillo():
    op = Operation()
    return render_template("loginsencillo.html", myOp = op)

@app.route("/renderlogindificil", methods=['GET','POST'])
def renderlogindificil():
    op = Operation()
    return render_template("logindificil.html", myOp = op)

@app.route("/rendertrain", methods=['GET','POST'])
def rendetrain():
    op = Operation()
    return render_template("train.html", myOp = op)

@app.route("/loginsencillo", methods=['POST'])
def loginsencillo():
    op = Operation()
    op.user = request.form['login']
    op.pressedtime = float(request.form['pressedtime'])
    op.flytime = float(request.form['onflytime'])
    op.keytimes = request.form['keytimes']
    
    regr = joblib.load('regr.pkl')
    op.predict(regr)
    
    le = joblib.load('labelenc.pkl')

    if(le.inverse_transform([op.prediction])[0] == op.user):    
        return render_template("accepted.html", myOp = op)
    else:
        return render_template("notaccepted.html", myOp = op)

@app.route("/logindificil", methods=['POST'])
def logindificil():
    op = Operation()
    op.pressedtime = float(request.form['pressedtime'])
    op.flytime = float(request.form['onflytime'])
    op.keytimes = request.form['keytimes']
    
    regr = joblib.load('regr.pkl')
    op.predict(regr)

    le = joblib.load('labelenc.pkl')

    op.prediction = le.inverse_transform([op.prediction])[0]

    return render_template("prediccion.html", myOp = op)

@app.route("/train", methods=['POST'])
def train():
    op = Operation()
    op.user = request.form['login']
    op.pressedtime = float(request.form['pressedtime'])
    op.flytime = float(request.form['onflytime'])
    op.keytimes = request.form['keytimes']
    op.save()

    return render_template("train.html", myOp = op)


app.debug = True
if __name__ == "__main__":
    app.run()
