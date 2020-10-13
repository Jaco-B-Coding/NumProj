# -*- coding: utf-8 -*-
"""
Created on Tue Oct  6 09:21:58 2020

@author: Giampiero
"""

from __future__ import print_function

from mathFunct import *      #importing package relating to numeric project
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, NavigationToolbar2QT as NavigationToolbar
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from matplotlib.figure import Figure
from PyQt5 import QtCore, QtGui, QtWidgets
import sys

#function to allow zooming in and out within the axes
def zoom_factory(ax,base_scale = 2.):
    def zoom_fun(event):
        # get the current x and y limits
        cur_xlim = ax.get_xlim()
        cur_ylim = ax.get_ylim()
        cur_xrange = (cur_xlim[1] - cur_xlim[0])*.5
        cur_yrange = (cur_ylim[1] - cur_ylim[0])*.5
        xdata = event.xdata # get event x location
        ydata = event.ydata # get event y location
        if event.button == 'up':
            # deal with zoom in
            scale_factor = 1/base_scale
        elif event.button == 'down':
            # deal with zoom out
            scale_factor = base_scale
        else:
            # deal with something that should never happen
            scale_factor = 1
            print (event.button)
        # set new limits
        ax.set_xlim([xdata - cur_xrange*scale_factor,
                     xdata + cur_xrange*scale_factor])
        ax.set_ylim([ydata - cur_yrange*scale_factor,
                     ydata + cur_yrange*scale_factor])
        plt.draw() # force re-draw

    fig = ax.get_figure() # get the figure of interest
    # attach the call back
    fig.canvas.mpl_connect('scroll_event',zoom_fun)

    #return the function
    return zoom_fun

class Annotate(object):
    def __init__(self):
        self.ax = plt.gca()
        self.rect = Rectangle((0,0), 1, 1)
        self.x0 = 0
        self.y0 = 0
        self.x1 = 0
        self.y1 = 0
        self.ax.add_patch(self.rect)
        self.pressed = False
        self.released = False
        
        global xAxis, yAxis
        #self.axesChanged = False
        self.newXAxis = []
        self.newYAxis = []
        
        
        self.ax.figure.canvas.mpl_connect('button_release_event', self.on_release)
        self.ax.figure.canvas.mpl_connect('button_press_event', self.on_press)
        self.ax.figure.canvas.mpl_connect('motion_notify_event', self.on_motion)
    

    def on_press(self, event):
        # print ('press')
        self.x0 = event.xdata
        self.y0 = event.ydata
        
        self.pressed = True
        self.released = False

    def on_release(self, event):
        # print ('release')
        self.x1 = event.xdata
        self.y1 = event.ydata
        self.rect.set_width(self.x1 - self.x0)
        self.rect.set_height(self.y1 - self.y0)
        self.rect.set_xy((self.x0, self.y0))
        self.ax.figure.canvas.draw()
        
        self.pressed = False
        self.released = True
        
    def on_motion(self, event):
        
   
        self.x1 = event.xdata
        self.y1 = event.ydata
        
        if self.x1 == None:
            self.x1 = 0
            self.y1 = 0
        
        self.rect.set_width(self.x1 - self.x0)
        self.rect.set_height(self.y1 - self.y0)
        self.rect.set_xy((self.x0, self.y0))
        
            
        if self.pressed:
            self.ax.figure.canvas.draw()
    
    def keyEventHandler(self, event):
        
        self.newXAxis = xAxis
        self.newYAxis = yAxis
        
        print("Do you want to delete data outside of selected range? If so press d")
        print('you pressed', event.key)
        
        keyPressed = event.key
        
        if keyPressed == "d":
            
            self.axesChanged = True
        
            xMin = self.x0
            xMax = self.x1
            
            arrayloc = 0
            
            for i in self.newXAxis:
                if i < xMin:
                    self.newXAxis.pop(arrayloc)
                    self.newYAxis.pop(arrayloc)
                    
                elif i> xMax:
                    self.newXAxis.pop(arrayloc)
                    self.newYAxis.pop(arrayloc)
                    
            ++arrayloc
          
        print("xMin:%8.2f, xMax:%8.2f" %(self.x0, self.x1))
    
    def getNewAxes (self):
        
        return [self.newXAxis, self.newYAxis]
    
    def getChangeStatus(self):
        
        return True
            
def update_plot():
    
    fig.canvas.draw_idle()

def onclick(event):
    print('%s click: button=%d, x=%d, y=%d, xdata=%f, ydata=%f' %
          ('double' if event.dblclick else 'single', event.button,
           event.x, event.y, event.xdata, event.ydata))

    verticalLine(event.xdata)
    update_plot()

#funtion to draw single lines (or multiple) at given xCoords
def verticalLine(xcoords): 

    global lver
    
    if isinstance(xcoords,float):
        print("true")

        lver.set_xdata(xcoords)


app = QtWidgets.QApplication(sys.argv)

fig, ax = plt.subplots()

#get axis Data for first time 
[readSuccess,xAxisTitle, yAxisTitle, xAxis, yAxis]=readFunct.getData()

if not readSuccess:
    print("data file could not be found")
else:
    ax.plot(xAxis,yAxis)
    
#define objects to be used for first time
lver = ax.axvline (0)

#setting zoom function 
scale = 1.2
    
#starting loop for different program parts 
state_DataSel = True
state_Selection = False

#Loop for the selection of the important range

a = Annotate()
changed =False

while state_DataSel == True:
    # #pass min and max x values to data selection function
    # ax.fig.canvas.mpl_connect('key_press_event', a.keyEventHandler)
    cahanged = a.getChangeStatus()
    
    if changed == True:
        [xAxis, yAxis] = a.getNewAxes()
        ax.clear()
        #ax.plot(xAxis,yAxis)
        state_DataSel = False
        print ("exitingt the data range selection environment")
        
#Loop for the selection of "Knickpunkt"
while state_Selection == True:
    cid = fig.canvas.mpl_connect('button_press_event', onclick)
    f = zoom_factory(ax,base_scale = scale)
        
        
plt.show()