#-*- coding: UTF-8 -*-
import datetime
import urllib, urllib2
import simplejson as json
import argparse

def main(k=100, seedfile="", ouputfile=""):

    print "Seed:", seedfile


    #read seed
    seed = open(seedfile)
    seedarr = []
    for line in seed:

        record = line.strip().split(",")[0:8]
        record[1] = int(float(record[1]))
        record[2] = int(float(record[2]))
        record[3] = int(float(record[3]))
        record[4] = int(float(record[4]))
        record[5] = int(float(record[5]))
        record[6] = int(float(record[6]))
        record[7] = int(float(record[7])) # likes and posts in N days
        seedarr.append(record)

    #record format: [pageid, accumulated like count, label, probability 1, probability 2]
    seedarr.sort(key=lambda x: x[7], reverse=True)

    #grouping
    mytmp = [0]
    w = open(ouputfile,"w")
    for i, row in enumerate(seedarr):

        mytmp[0] = mytmp[0] + row[1]
        print row
        if i % k ==0:
            print mytmp
            w.write( str(i) + "," +",".join([ str(int(x)) for x in mytmp])+"\n")

    w.write(str(i) + "," + ",".join([ str(int(x)) for x in mytmp])+"\n")

    w.close()
    return
    

if __name__ == "__main__":


    parser = argparse.ArgumentParser(description='Facebook Fan Page post schedular')
    parser.add_argument('-k', type=int, action="store",dest="k",help="Aggregation factor")
    parser.add_argument('-i', type=str, action="store",dest="i",help="Seedfile")
    parser.add_argument('-o', type=str, action="store",dest="o",help="Outputfile")
    parser.set_defaults(k=100)

    init = parser.parse_args()
    main(k=init.k, seedfile=init.i, ouputfile=init.o)    
    #main(yyyy=init.year, MM=init.month, DD=init.day, HH=init.hour)
    #example:
    # python plot_predict.py -k 100 -i "(2015_0302)feature_5day_M8_D13_H0_k3.csv" -p "(2015_0302)feature_5day_M8_D13_H0_k3.f3f5.csv.predict.out" -o "(2015_0302)feature_5day_M8_D13_H0_k3.f3f5.csv.aggre100.csv" 
