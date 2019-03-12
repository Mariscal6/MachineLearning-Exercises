from pymongo.mongo_client import MongoClient
import datetime

class Operation():

    v1 = 0
    v2 = 0
    ellapsed = 0
    timeStamp = 0
    prediction = 0


    def check(self, v):
        return self.v1 + self.v2 == v

    def toString(self):
        return str(self.v1) + " + " + str(self.v2)

    def toTuple(self):
        return (self.v1, self.v2, self.isEven(), 
                self.isZero(), self.digitNumber(), 
                self.carryOn(), self.ellapsed)
    
    def predict(self, model):
        self.prediction = model.predict([self.toTuple()[:-1]])[0]

    def isEven(self):
        return self.v1 % 2 == 0 and self.v2 % 2 == 0

    def isZero(self):
        return self.v1 % 10 == 0 or self.v2 % 10 == 0

    def digitNumber(self):
        d1 = 2
        if self.v1 < 10:
            d1 = 1
        d2 = 2
        if self.v2 < 10:
            d2 = 1
        return d1 + d2

    def carryOn(self):
        return (self.v1 % 10 + self.v2 % 10) > 10

    def save(self):
        op = {
            "v1": self.v1,
            "v2": self.v2,
            "ellapsed": self.ellapsed
        }

        client = MongoClient('localhost', 27017)
        db = client['myDB']
        collection = db["additions"]
        collection.insert(op)




