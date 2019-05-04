import pickle
import os

def findInfo(name):
    filepath = os.path.dirname(os.path.abspath(__file__))
    with open(filepath + '/janet_data.pickle', 'rb') as f:
        # The protocol version used is detected automatically, so we do not
        # have to specify it.
        data = pickle.load(f)


        isProfessor = None
        thisOffice = None
        thisQuote = None

        # getting length of list
        length = len(data)

        info = {}
        for i in range(length):
            if data[i]["name"] == name:
                info = data[i]
                break

        return info

print(findInfo("david august"))
