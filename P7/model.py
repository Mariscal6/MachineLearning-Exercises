from operation import Operation
import pandas as pd
from sklearn import linear_model
from sklearn import ensemble
from sklearn.metrics import mean_squared_error
from sklearn.externals import joblib
from sklearn import preprocessing
import time

nObservations = 0
from pymongo.mongo_client import MongoClient


client = MongoClient('localhost', 27017)
db = client['myDB']
collection = db["additions"]



def train():
  global nObservations

  records = []
  for v  in collection.find({}):
      op = Operation()
      op.pressedtime = v["pressedtime"]
      op.flytime = v["flytime"]
      op.keytimes = v["keytimes"]
      op.user = v["user"]
      records.append(op.toTuple())
    

  features = ["flytime", "pressedtime"]

  for x in range(1,19):
      features.append("kt" + `x`)

  target = "user"  

  labels =  features + [target]
  print(labels)

  df = pd.DataFrame.from_records(records, columns = labels)
#  print ("Before filtering ", df.shape)
#
#  df = df[df.ellapsed < 10]
#
#  print ("After filtering ", df.shape)
#
#  if df.shape[0] <= nObservations:
#    return
#
#  nObservations = df.shape[0]

#LABEL ENCODER DE USUARIOS
  le = preprocessing.LabelEncoder()
  df[target] = le.fit_transform(df[target])

#MOSTRAR BASE DE DATOS
  print(df)

  params = {'n_estimators': 500, 'max_depth': 4}
  regr = ensemble.GradientBoostingClassifier(**params)

  X = df[features]
  y = df[target]
  regr  = regr.fit(X, y)


  prediction = regr.predict(X)
  print("Error", mean_squared_error(prediction, y))

  joblib.dump(regr, 'regr.pkl',  protocol=2)
  joblib.dump(le, 'labelenc.pkl', protocol=2)
  print("DUMP")
  return df.shape[0]

while True:
  train()
  time.sleep(3)

