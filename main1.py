__author__= "uddipaan"


import math   #(for python less than or equal to version 2, use this import part)
import sys
import argparse     #argparser is a library
import time


from extra1 import *

#Usage
#parameter 1: Name of the problem file
#parameter 2: EPSILON value
#parameter 3: Minimum confidence


if __name__ == '__main__':
    if len(sys.argv)<1:
        print("Error. Quiting!!");
        exit(1);


    parser = argparse.ArgumentParser()
    parser.add_argument(dest='F',help="Name of the problem file")
    parser.add_argument(dest='epsilon',help="Epsilon value",type=float)
    parser.add_argument(dest='delta',help="Minimum Confidence",type=float)
    args, unknown = parser.parse_known_args() #using parse_known_args rather than parse_args enables the use of ArgumentParser in code within the scope of if __name__ 

    initialfilename = args.F
    epsilon = args.epsilon
    delta = args.delta

    

    start_time = time.time()
    counter=0
    C=[]
    th = compute_threshold(epsilon)
    pivot= 2 * th
    print "The Pivot is: "+str(pivot)
    t=computeiter_count(delta)
    print "The T is "+str(t)
    f = open(initialfilename,'r')
    lines = f.readlines()
    f.close()
    numVariables = 0
    numClauses = 0
    for line in lines:
        if (str(line.strip()[0:5]) == 'p cnf'):
            fields = line.strip().split(' ')
            numVariables = int(fields[2])
            numClauses = int(fields[3])
            break
    
    
    while (counter<t) :
        c=ApproxMcCore(initialfilename,pivot,numVariables,numClauses)
        counter = counter+1
        if c!=0:
            C.append(c)
    final_count=find_median(C) 
    X=final_count
    print("Time taken: %s seconds" % (time.time() - start_time))
    print "Operating on cnf file with 15 no. of variables and 46 no. of clauses! Please have patience!"
    print "The final result is "+str(X)
           
