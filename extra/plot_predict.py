#-*- coding: UTF-8 -*-
import datetime
import urllib, urllib2
import simplejson as json
import argparse

def compare(item1, item2):
    a = item1[:]
    a.reverse()
    b = item2[:]
    b.reverse()

    for i in range(len(a)-3):
	#print a[i]
	if a[i]< b[i]:
	    return -1
	elif a[i] > b[i]:
	    return 1

    return 0

def main(k=100, seedfile="", predictfile="", ouputfile=""):

    print "Seed:", seedfile
    print "Predict:", predictfile


    #read seed
    seed = open(seedfile)
    seedarr = []
    pages = {}
    for line in seed:

        record = line.strip().split(",")[0:2]
        record[1] = int(float(record[1]))
        seedarr.append(record)
	pages[record[0]] = line
    #read predicted label
    predict = open(predictfile)
    predictlines = predict.readlines()
    predictheader = predictlines[0].strip().split(" ")
    
    numberoneidx = predictheader.index("1")
    print "1:", numberoneidx
    #print predictlines
    lineidx = 0
    numberofclass = len(predictheader)
    for line in predictlines[1:]:
         record = line.strip().split(" ")[0:numberofclass]
	 score = 0
	 for i in range(numberofclass): 
             record[i] = float(record[i])  
	     if i > 0:
	        score = score + (i-1) * record[i]
	 record.append(score)
	 seedarr[lineidx].append(line)
         seedarr[lineidx].extend(record)
	 #print seedarr[lineidx]
         lineidx = lineidx + 1

    print len(seedarr), len(predictlines[1:])

    #record format: [pageid, accumulated post count, label, probability 1, probability 2]
    #seedarr.sort(key=lambda x: x[numberoneidx+2], reverse=True)
    #seedarr.sort(key=lambda x: x[2], reverse=True)
    seedarr.sort(cmp=compare, reverse=True)
    #print seedarr[0]
    #print seedarr[0][-1]
    #seedarr.sort(key=lambda x: x[-1] , reverse=True)

    wsort = open(predictfile+".rest","w") 
    mysum =0
    for i, row in enumerate(seedarr):
	mysum = mysum + row[1]
	wsort.write(pages[row[0]])
    #	wsort.write(str(row[0]) + " " + str(row[1]) + " " + row[2])
    wsort.close()
    #grouping
	
    mytmp = [0]
    w = open(ouputfile,"w")
    for i, row in enumerate(seedarr):

        mytmp[0] = mytmp[0] + row[1]
        #print row[0:3]
        if i % k ==0:
            print mytmp
            w.write( str(i) + "," +",".join([ str(int(x)) for x in mytmp])+"\n")

    w.write(str(i) + "," + ",".join([ str(int(x)) for x in mytmp])+"\n")

    w.close()
    print mytmp, mysum
    return
    

if __name__ == "__main__":


    parser = argparse.ArgumentParser(description='Facebook Fan Page post schedular')
    parser.add_argument('-k', type=int, action="store",dest="k",help="Aggregation factor")
    parser.add_argument('-i', type=str, action="store",dest="i",help="Seedfile")
    parser.add_argument('-p', type=str, action="store",dest="p",help="Predictfile")
    parser.add_argument('-o', type=str, action="store",dest="o",help="Outputfile")
    parser.set_defaults(k=100)

    init = parser.parse_args()
    main(k=init.k, seedfile=init.i, predictfile=init.p, ouputfile=init.o)    
    #main(yyyy=init.year, MM=init.month, DD=init.day, HH=init.hour)
    #example:
    # python plot_predict.py -k 100 -i "(2015_0302)feature_5day_M8_D13_H0_k3.csv" -p "(2015_0302)feature_5day_M8_D13_H0_k3.f3f5.csv.predict.out" -o "(2015_0302)feature_5day_M8_D13_H0_k3.f3f5.csv.aggre100.csv" 
