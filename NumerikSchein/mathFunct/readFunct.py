# -*- coding: utf-8 -*-
"""
Created on Sat Sep  5 16:41:36 2020

@author: Giampiero
"""

import matplotlib.pyplot as plt
from os import path

def getData(pathName="Dat1.txt"):
    
    #deklarationsteil
    global xArray 
    global yArray
    
    global xAxisTitle
    global YAxisTitle
    
    xArray = []
    yArray = []
    xWert = 0
    yWert = 0
    
    success = True
    
    #if the path exists read the axis titles and the data
    #return success if happened correctly
    if path.exists(pathName):
        
        with open(pathName) as fobj_in:
            with open(pathName) as fobj_out:
            
                count=0
            
                while True:
                
                    line = fobj_in.readline()
                
                    line = line.strip()
                
                    if not line:
                        if count == 0:
                            success = False
                        break
                
                    if not count:
                        (xAxisTitle, YAxisTitle)=line.split('\t')
                    
                    else:
                        (xWert, yWert)=line.split()
                    
                    xArray += [float(xWert)]
                    yArray += [float(yWert)]
                    
                    count +=1  
                
    else:
        success = False
        
    
    return [success, xAxisTitle, YAxisTitle, xArray, yArray]
