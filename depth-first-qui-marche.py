#encoding:utf-8
'''
Created on 2015-09-25

@author: Francois
'''
from __future__ import division
from random import random
limit = 950000000
size = 9
total = 0
timeout = False

def isLegalInRow(config,line,col,num):
    for i in range(size):
        if(config[line][i] == num):
            return False
    return True

def isLegalInCol(config,line,col,num):
    for i in range(size):
        if(config[i][col]  == num):
            return False
    return True
    
def isLegalInBox(config,line,col,num):
    hBox = col - col % 3
    vBox = line - line % 3
    for i in range(3):
        for j in range(3):
            if(config[i+vBox][j+hBox] == num):
                return False
    return True
    
def isLegal(config,line,col,num):
    return (isLegalInRow(config,line,col,num) and 
            isLegalInCol(config,line,col,num) and 
            isLegalInBox(config,line,col,num))
    
def getPossibleNumbers(config,line,col):
    possibleNumbers = [1,2,3,4,5,6,7,8,9]
    
    for i in range(size):
        x = config[line][i]
        if(x in possibleNumbers):
            possibleNumbers.remove(x)
            
    for i in range(size):
        x = config[i][col]
        if(x in possibleNumbers):
            possibleNumbers.remove(x)
    
    hBox = col - col % 3
    vBox = line - line % 3
    
    for i in range(3):
        for j in range(3):
            x = config[i+vBox][j+hBox]
            if(x in possibleNumbers):
                possibleNumbers.remove(x)
                
    return possibleNumbers

def depthFirst(config):
    global timeout
    timeout= False
    nbNoeud = 0
    global total
    total = 0
    result = recursiveDepthFirst(config,nbNoeud)
    print (str(total),"visités")
    return result
    
def recursiveDepthFirst(config,nodesVisited):
    import sys
    global total
    global timeout
    sys.setrecursionlimit(1000)
    global limit
    complete = True
    i = j = 0
    
    #check for a 0 in the matrix. This also gives us the i,j coordinates of the first 0 we find
    while(complete and j < size and i < size): 
        complete = config[i][j] != 0
        if(complete):
            i += 1
            if(i % size == 0):
                j += 1
                i = 0
    if(complete):
        return True
    
    if(total > limit):
        timeout = True
        return False
    
#     for num in range(1,size+1):
#         if (isLegal(config, i, j, num)):
#             config[i][j] = num
#             total += 1
#             if (recursiveDepthFirst(config,nodesVisited+1)):
#                 return True
# 
#             config[i][j] = 0
        
        
    possibleNumbers = getPossibleNumbers(config,i,j)
    if(possibleNumbers == []):
        return False
    for n in possibleNumbers:
        config[i][j] = n
        total += 1
        if(recursiveDepthFirst(config,nodesVisited+1)==True):
            return True
        config[i][j] = 0
                                  
    return False

def readConfigs(filename):
    allLines =  [line.rstrip('\n') for line in open(filename)]
    allConfigs = []
    
    for line in allLines:
        i = j = 0
        aConfig = [[0 for a in range(size)] for b in range(size)]
        for x in line:
            aConfig[i][j] = int(x) #fill the matrix column by column
            j += 1
            if(j % size == 0):
                i += 1
                j = 0
        allConfigs.append(aConfig)
        
    return allConfigs         

def ppSudokuMat(config):
    for i in range(size):
        if(i % 3 == 0):
            print ("|-----------------------|") 
        for j in range(size):
            if(j % 3 == 0):
                print ("| ",end='')
            print (str(config[i][j])+" ",end='')
        print ("|\n",end='')
    print ("-------------------------")
    
if __name__ == '__main__':
    import time
    initConfigs = readConfigs('100sudoku.txt')
    dfConfigs = list(initConfigs) #clone the configurations to avoid altering them
#    ppSudokuMat(dfConfigs[0])
    start = time.time()
    complete = 0
    for conf in dfConfigs:
        result = depthFirst(conf) #work on the copy
        if(not timeout):
            complete += 1
            ppSudokuMat(conf)
    print (time.time()-start)
    print(complete)