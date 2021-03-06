__author__= "uddipaan"



import random
import os
import sys
import math
import re






def compute_threshold(epsilon):
    ceiling = math.ceil
    x = pow(2.71,0.5)
    y = (1+1/epsilon)
    z = math.pow(y,2)
    final=3*x*z
    P = int(ceiling(final)) 
    return P

def computeiter_count(delta):
    ceiling = math.ceil
    ln = math.log
    a = 3/delta
    result = 35*ln(a)
    R= int(ceiling(result))
    return R


def find_median(c):

    if not c:    
        return 0
    else:
        srt = sorted(c)
        leng = len(srt)
        if not leng % 2:
            return int((srt[ leng / 2 ] + srt[ leng / 2 - 1]) / 2.0 )   # // is used in newer versions of python
        return int(srt[ leng / 2 ] )




def ApproxMcCore(filename,pivot,numVariables,numClauses):

    outputFileName = "file_with_var_:"+str(numVariables)+".txt"   #first check if the original file is solvable
    cmd="./sharpSAT "+str(filename)+" > "+str(outputFileName)
    os.system(cmd)
    f = open(outputFileName,'r')
    lines = f.readlines()
    f.close() 
    os.system('rm '+outputFileName)	
    res = lines[33]
	
    
    if res == 0:
	print("NO Solution")
	return 0
    else :
	S=int(res)

    if S < pivot or S == pivot :
	return S
		
    else:
	lg=math.log(pivot)  #now check with XOR constraints
	flr=math.floor
	l=flr(lg)
		
	i=l-1
	while(i == numVariables):
		i=i+1
		finalFileName= "file_with_hashes.cnf"
		outputFileName="tempfile.txt"
		addHash(initialFileName,finalFileName,numVariables,numClauses,i-l)
		cmd="./sharpSAT "+str(finalFileName)+" > "+str(outputFileName)
	
		os.system(cmd)
		f = open(outputFileName,'r')
    		lines = f.readlines()
    		f.close() 
		os.system('rm '+outputFileName)
		res = lines[33]
		#res_new = res.split()
		S=res
		
	if( S>pivot or S==0 ):
		return S
	else:
		return S*math.pow(2,i-1)



         







def addHash(initialFileName,finalFileName,numVariables,numClauses,numHash):
    hashClauses = ''
    for i in range(int(numHash)):
        varNum = 0
        randBits = findHashBits(numVariables,numHash)
        hashClauses = hashClauses+'x'
        needToNegate = False
        if (randBits[0] == '1'):
            needToNegate = True
        for j in range(1, numVariables+1):
            if (randBits[j] == '1'):
                varNum = varNum+1
                if (needToNegate):
                    hashClauses = hashClauses+'-'
                    needToNegate = False
                hashClauses = hashClauses+str(j)+' '
        hashClauses = hashClauses+' 0\n'
    f = open(initialFileName,'r')
    lines = f.readlines()
    f.close()
    f = open(finalFileName,'w')
    f.write('p cnf '+str(numVariables)+' '+str(numClauses+numHash)+'\n')
    for line in lines:
        f.write(str(line.strip())+'\n')
    if (numHash > 0):
        f.write(hashClauses)
    f.close()
	 
		


def findHashBits(numVariables,numHash):
    randBitsTotal = getBinary(numVariables+2*numHash)
    randBits=''
    for i in range(numVariables+1):
        xorResult = 0
        for j in range(numHash):
            xorResult = xorResult^int(randBitsTotal[i+j])
        randBits += str(xorResult)
    return randBits



def getBinary(binLen):
    byteLen = 1+binLen/8
    _random_source = open("/dev/urandom","rb")
    randBytes = _random_source.read(byteLen)
    _random_source.close()

    randInt = int(randBytes.encode("hex"),16)
    randBin = bin(randInt).zfill(binLen)
    return randBin[:binLen]


    

    
