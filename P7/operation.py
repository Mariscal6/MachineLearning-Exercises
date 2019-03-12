from pymongo.mongo_client import MongoClient
import datetime

class Operation():

    user = ""
    flytime = 0.0
    pressedtime = 0.0
    prediction = ""
    keytimes = ""

    def toTuple(self):

        self.keytimes = self.keytimes.split("-")
        self.keytimes.pop()
        for i in self.keytimes:
            i = float(i)
        
        return(self.flytime, self.pressedtime)+tuple(self.keytimes)+(self.user,)
    
    def predict(self,model):
        self.prediction = model.predict([self.toTuple()[:-1]])[0]
    
    def save(self):
	    op = {
	        "user": self.user,
	        "flytime": self.flytime,
	        "pressedtime": self.pressedtime,
                "keytimes": self.keytimes
	        }
	
	    client = MongoClient('localhost',27017)
	    db = client['myDB']
	    collection = db["additions"]
	    collection.insert(op)
