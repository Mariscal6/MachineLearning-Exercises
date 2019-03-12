from flask import Flask, render_template, request, make_response
from random import randint
from time import time

import datetime
import sklearn
from sklearn.externals import joblib

from operation import Operation

app = Flask(__name__)

@app.route("/")
def addition():
  op = Operation()
  op.v1 = randint(0, 100)
  op.v2 = randint(0, 100)
  op.timeStamp = time()
  return render_template("form.html", myOp = op)


@app.route("/doOperation", methods=['POST'])
def operation():
  result = int(request.form['value'])
  op = Operation()
  op.v1 = int(request.form['v1'])
  op.v2 = int(request.form['v2'])
  op.timeStamp = float(request.form['timeStamp'])

  if op.check(result):
    regr = joblib.load('regr.pkl')
    op.predict(regr)

    op.ellapsed = time() - op.timeStamp
    op.save() 
    return render_template("resultSimple.html", myOp = op) 
  else:
    return render_template("form.html", myOp = op)


@app.route("/exampleJQuery")
def example():
  return render_template("exampleJQuery.html")



app.debug = True

if __name__ == "__main__":
    app.run()
