from operation import Operation
import pandas as pd
from sklearn import linear_model
from sklearn import ensemble
from sklearn.metrics import mean_squared_error
from sklearn.externals import joblib
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
      op.v1 = v["v1"]
      op.v2 = v["v2"]
      op.ellapsed = v["ellapsed"] 
      records.append(op.toTuple())

  features = ["v1", "v2", "isEven", "isZero", "nDigits", "carryOn"]
  target = "ellapsed"

  labels =  features + [target]
  df = pd.DataFrame.from_records(records, columns = labels)
  print ("Before filtering ", df.shape)

  df = df[df.ellapsed < 10]

  print ("After filtering ", df.shape)

  if df.shape[0] <= nObservations:
    return

  nObservations = df.shape[0]

  params = {'n_estimators': 500, 'max_depth': 4, 'min_samples_split': 2,
            'learning_rate': 0.01, 'loss': 'ls'}
  regr = ensemble.GradientBoostingRegressor(**params)

  X = df[features]
  y = df[target]
  regr  = regr.fit(X, y)


  prediction = regr.predict(X)
  print("Error", mean_squared_error(prediction, y))

  joblib.dump(regr, 'regr.pkl',  protocol=2)
  print("DUMP")
  return df.shape[0]

while True:
  train()
  time.sleep(3)

