#-*- coding: UTF-8 -*-
#/usr/bin/env python
import argparse
import pickle
from sklearn.ensemble import RandomForestClassifier
import math

def read(trainpath):
    X=[];Y=[];
    f = open(trainpath)
    for line in f:
        elem = line.strip().split(" ")
	y = int(float(elem[0]))
	x = [ float(x.split(":")[1])  for x in elem[1:]]
	if y ==0 and math.fsum(x) > 0: continue #remove the sigular point
        Y.append(y)
        X.append(x)

    return (X, Y)


def train(trainpath, modelpath):

    (X, Y) = read(trainpath)
    print "Training Size:", len(X)
    clf = RandomForestClassifier(n_estimators=20,n_jobs=4,verbose=1)
    clf.fit(X,Y)
    pickle.dump(clf, open(modelpath, "w"))
    print "Done"

if __name__ == "__main__":


    
    parser = argparse.ArgumentParser(description='Lib RandomForest Toolkit (Train)')
    parser.add_argument('-i', type=str, action="store",dest="i",help="Training file path")
    parser.add_argument('-o', type=str, action="store",dest="o",help="Model file path")
    init = parser.parse_args()

    parser.set_defaults(o=init.i+".randomforest.model")

    init = parser.parse_args()

    train(init.i, init.o)
