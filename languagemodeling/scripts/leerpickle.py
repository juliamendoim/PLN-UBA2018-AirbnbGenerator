import pickle
f = open('logs2','rb')
model = pickle.load(f)
f.close()