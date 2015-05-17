#-*- coding: UTF-8 -*-
#/usr/bin/env python
import argparse
import pickle
from sklearn.ensemble import RandomForestClassifier

def read(testpath):
    X=[];Y=[];
    f = open(testpath)
    for line in f:
        elem = line.strip().split(" ")
        Y.append(int(elem[0]))
        X.append([ float(x.split(":")[1])  for x in elem[1:]])

    return (X, Y)


def predict(testpath, modelpath, outputpath):

    (X, Y) = read(testpath)
    clf = pickle.load(open(modelpath, "r"))
    pred = clf.predict(X)
    prob = clf.predict_proba(X)
    w= open(outputpath,"w")
    w.write("labels "+ " ".join([ str(x) for x in clf.classes_ ]) +"\n")

    count = 0 
    for i in range(0, len(pred)):
        #print prob[i]
        w.write(str(pred[i])+" "+" ".join([ str(x) for x in prob[i] ])+"\n")
        if float(pred[i])== float(Y[i]): count = count + 1

    accu = float(count)/len(Y) * 100
    print "Accuracy=", ('%.2f' % accu) 

    w.close()


    print "Done"

if __name__ == "__main__":


    
    parser = argparse.ArgumentParser(description='Lib RandomForest Toolkit (Predict)')
    parser.add_argument('-i', type=str, action="store",dest="i",help="Testing file path")
    parser.add_argument('-b', type=bool, action="store",dest="b",help="Enable Probability")
    parser.add_argument('-m', type=str, action="store",dest="m",help="Model file path")
    parser.add_argument('-o', type=str, action="store",dest="o",help="Predict file path")

    parser.set_defaults(b=True)

    init = parser.parse_args()

    predict(init.i, init.m, init.o)
