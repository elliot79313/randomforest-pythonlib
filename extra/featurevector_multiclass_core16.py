#-*- coding: UTF-8 -*-
import datetime
import math
import simplejson as json
import PublishHistory as ph
import argparse
def main(yyyy=2015, MM=4, DD=25, HH=0, khour=3, answer=False, history=7):

    history_tracking = history #days

    et = datetime.datetime(yyyy,MM,DD,HH,0,0)

    feature_selection = {'f1':True ,'f3': True, 'f5': True, 'f8': True, 'f4':False }

    #predict period:  
    #example:
    #     MM=8, DD=13, HH=0, k=6
    #     2014/08/12 18:00:00 ~ 2014/08/13 00:00:00
    print "Groud Truth:"
    target = ph.main(yyyy=et.year, MM=et.month, DD=et.day, HH=et.hour, khour=khour)
    seeds =  target.keys()
    print et, len(seeds)
    print

    et = et + datetime.timedelta(hours=-khour)

    prev_target = ph.main(yyyy=et.year, MM=et.month, DD=et.day, HH=et.hour, khour=khour)


    seeds =  target.keys()
    print et, len(prev_target.keys())
    print len(prev_target.keys())

    seeds.extend(prev_target.keys())
    dedupedSeed = set(seeds)
    print "Dedupe:",len(dedupedSeed)



    et = datetime.datetime(yyyy,MM,DD,HH,0,0)

    weekpages ={}
    for i in range(0,history_tracking):
        et = et + datetime.timedelta(hours=-24)
        print et
        prev_behavior = ph.main(yyyy=et.year, MM=et.month, DD=et.day, HH=et.hour, khour=khour)
        for key in  prev_behavior.keys():
            if key not in weekpages:
                weekpages[key] = prev_behavior[key]
            else:
                weekpages[key]["totallike"] = weekpages[key]["totallike"] + prev_behavior[key]["totallike"]
                weekpages[key]["totalpost"] = weekpages[key]["totalpost"] + prev_behavior[key]["totalpost"]


    print len(weekpages.keys())


    et = datetime.datetime(yyyy,MM,DD,HH,0,0)

    fulldaypages ={}
    for i in range(0,history_tracking*4):
        et = et + datetime.timedelta(hours=-6)
        print et
        prev_behavior = ph.main(yyyy=et.year, MM=et.month, DD=et.day, HH=et.hour, khour=khour)
        for key in  prev_behavior.keys():
            if key not in fulldaypages:
                fulldaypages[key] = prev_behavior[key]
            else:
                fulldaypages[key]["totallike"] = fulldaypages[key]["totallike"] + prev_behavior[key]["totallike"]
                fulldaypages[key]["totalpost"] = fulldaypages[key]["totalpost"] + prev_behavior[key]["totalpost"]


    print len(fulldaypages.keys())

    #-----------
    pagemeta = json.load(open("pagedata_core16.json"))

    print len(pagemeta.keys())

    #-----------
    
    
    sourecedate = "{:0>2d}".format(datetime.datetime.now().month) + "{:0>2d}".format(datetime.datetime.now().day)
    w = open("(2015_" + sourecedate + ")featuremulti_" + str(history_tracking) 
           + "day_M"+str(MM)+"_D"+str(DD)+"_H"+str(HH)+"_k" + str(khour) + ".csv","w")
    fw = open("(2015_" + sourecedate + ")featuremulti_" + str(history_tracking)
                + "day_M"+str(MM)+"_D"+str(DD)+"_H"+str(HH)+"_k" + str(khour) + "."
            + ("f1" if feature_selection['f1'] else "")
            + ("f3" if feature_selection['f3'] else "")
            + ("f4" if feature_selection['f4'] else "")
            + ("f5" if feature_selection['f5'] else "")
            + ("f8" if feature_selection['f8'] else "")
        +".csv","w")

    for seed in pagemeta.keys():
        record = []
        record.append(str(seed)) #page i   A

        if len(record) != 1: print "error0",len(record), record
        trainrecord = []
        if seed in target: #label 
            record.append(str(target[seed]["totallike"]))   #B
            record.append(str(target[seed]["totalpost"]))   #C
            if target[seed]["totallike"]>0:
                fw.write(str(int(math.log(target[seed]["totallike"],2)+1)))
                #fw.write(str(target[seed]["totallike"]))
            else:
                fw.write(str(0))
        else:
            record.append(str(0))
            record.append(str(0))
            fw.write(str(0))

        if len(record) != 3: print "error1",len(record), record
        if seed in prev_target: #likes and posts of the latest section
            record.append(str(prev_target[seed]["totallike"])) #F1       D
            record.append(str(prev_target[seed]["totalpost"])) #F2       E
            if feature_selection['f1']:
                trainrecord.append(str(prev_target[seed]["totallike"]))  

            #trainrecord.append(str(prev_target[seed]["totallike"]))  
        else:
            record.append(str(0))
            record.append(str(0))
            if feature_selection['f1']:
                trainrecord.append(str(0))  

        if len(record) != 5: print "error2",len(record)
        if seed in weekpages: #likes and posts at the same section in N days
            record.append(str(weekpages[seed]["totallike"])) #F3        F
            record.append(str(weekpages[seed]["totalpost"])) #F4        G
            if feature_selection['f3']:
                trainrecord.append(str(weekpages[seed]["totallike"]))  
            if feature_selection['f4']:
                trainrecord.append(str(weekpages[seed]["totalpost"]))  
        else:
            record.append(str(0))
            record.append(str(0))
            if feature_selection['f3']:
                trainrecord.append(str(0))  
            if feature_selection['f4']:
                trainrecord.append(str(0))  


        if len(record) != 7: print "error3",len(record)

        if seed in fulldaypages: #likes and posts in N days
            record.append(str(fulldaypages[seed]["totallike"])) #F5        H
            record.append(str(fulldaypages[seed]["totalpost"])) #F6        I

            if seed in weekpages:
                if fulldaypages[seed]["totallike"] - weekpages[seed]["totallike"] < 0:
                    raise ValueError('A very specific bad thing happened:'+ str(seed)+"," + 
                        str(fulldaypages[seed]["totallike"])+"-"+str(weekpages[seed]["totallike"]))

            if feature_selection['f5']:
                trainrecord.append(str(fulldaypages[seed]["totallike"]))  
        else:
            record.append(str(0))
            record.append(str(0))

            if feature_selection['f5']:
                trainrecord.append(str(0))  

        if len(record) != 9: print "error4"

        if seed in pagemeta: #fans and talking_about_count at crawling time
            if "likes" not in pagemeta[seed]:
                record.append(str(0))
                record.append(str(0))
            else:

                record.append(str(pagemeta[seed]["likes"])) #F7                   J
                record.append(str(pagemeta[seed]["talking_about_count"])) #F8     K
            #record.append(str(0))

            if feature_selection['f8']:
                if "likes" not in pagemeta[seed]:
                    trainrecord.append(str(0))  
                else:
                    trainrecord.append(str(pagemeta[seed]["talking_about_count"]))  
        else:
            print seed
            record.append(str(0))
            record.append(str(0))

            if feature_selection['f8']:
                trainrecord.append(str(0))  

        if len(record) != 11: print "error5"
        

        w.write(",".join(record)+"\n")

        fw.write(" " + " ".join([ str(i+1) + ":" + _val for i, _val in enumerate(trainrecord) ])+"\n")


    w.close()
    fw.close()



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Facebook Fan Page post schedular')
    parser.add_argument('--answer', dest='answer', action='store_true')
    parser.set_defaults(answer=False)
    parser.add_argument('-MM', type=int, action="store",dest="MM",help="Mode")
    parser.add_argument('-DD', type=int, action="store",dest="DD",help="Mode")
    parser.add_argument('-HH', type=int, action="store",dest="HH",help="Mode")
    parser.add_argument('-L', type=int, action="store",dest="L",help="back")
    parser.add_argument('-k', type=int, action="store",dest="k",help="Mode")

    parser.set_defaults(MM=4)
    parser.set_defaults(DD=20)
    parser.set_defaults(HH=0)
    parser.set_defaults(L=7)
    parser.set_defaults(k=1)

    args = parser.parse_args()
    #example 
    #python featurevector.py -MM 8 -DD 12 -HH 18 -k 6   
    main(yyyy=2015, MM=args.MM, DD=args.DD, HH=args.HH, khour=args.k, answer=args.answer, history=args.L)
