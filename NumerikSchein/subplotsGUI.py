# -*- coding: utf-8 -*-
"""
Created on Fri Sep 11 16:25:56 2020

@author: Giampiero
"""
from __future__ import print_function

from mathFunct import *      #importing package relating to numeric project

from matplotlib.lines import Line2D
from matplotlib.patches import Rectangle
from matplotlib.text import Text
from matplotlib.image import AxesImage

import sys
import matplotlib
matplotlib.use('Qt5Agg')

from PyQt5 import QtCore, QtGui, QtWidgets

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, NavigationToolbar2QT as NavigationToolbar
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.figure import Figure


class MplCanvas(FigureCanvasQTAgg):

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        
        rows=2
        columns=1
        
        #Create a figure within the canvas with two subplots one underneath the oter one
        self.fig = plt.figure()
        super(MplCanvas, self).__init__(self.fig)
        
        self.axes=self.fig.subplots(rows,columns)

        

class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        
        #define canvas to plot to
        self.canvas = MplCanvas(self, width=5, height=4, dpi=100)
        self.setCentralWidget(self.canvas)

        #start with random plots
        #define x/ y default Data
        self.xArray=[0,1,2,3,4]
        self.yArray=[1,1,20,3,40]
        
        #self.canvas.axes[0].plot(self.xArray, self.yArray, 'o')
        self.canvas.axes[0].set_title('subplot 1')
        self.canvas.axes[0].set_xlabel('xLabel')
        self.canvas.axes[0].set_ylabel('yLabel')
        
        #self.canvas.axes[1].plot(self.xArray, self.yArray, '--') #to be removed once set to non default value by update fct
        self.canvas.axes[1].set_xlabel('xLabel2')
        self.canvas.axes[1].set_title('subplot 2')
        self.canvas.axes[1].set_ylabel('yLabel2')
       
        # We need to store a reference to the plotted line 
        # somewhere, so we can apply the updated data to it.
        self._plot_ref = None
    
        #change data to read data from file
        self.changeData()
        self.update_plot() 
            
        # Create toolbar, passing canvas as first parament, parent (self, the MainWindow) as second.
        toolbar = NavigationToolbar(self.canvas, self)

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(toolbar)
        layout.addWidget(self.canvas)

        # Create a placeholder widget to hold our toolbar and canvas.
        widget = QtWidgets.QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)
        
    def update_plot(self):
       
        # Note: we no longer need to clear the axis.       
        if self._plot_ref is None:
            # First time we have no plot reference, so do a normal plot.
            # .plot returns a list of line <reference>s, as we're
            # only getting one we can take the first element.
            plot_refs = self.canvas.axes[0].plot(self.xArray, self.yArray, 'r')
            self._plot_ref = plot_refs[0]
        else:
            # We have a reference, we can use it to update the data for that line.
            #here just done for the yAxis
            self._plot_ref.set_ydata(self.xArray, self.yArray)

        # Trigger the canvas to update and redraw.
        self.canvas.draw()
        
    def changeData(self, *args, **kwargs):
        [readSuccess,self.xAxisLabel, self.yAxisLabel, self.xArray, self.yArray]=readFunct.getData()
        
        if not readSuccess:
            print("Path was incorrect or file was empty")
            
def onclick(event):
    print(event.xdata, event.ydata)
    
app = QtWidgets.QApplication(sys.argv)
w = MainWindow()

#create references to pass to the selection class
current_figure = plt.gcf()
# ax_ref = w.canvas.axes[0]
# line_ref, = w.canvas.axes[0].plot(w.xArray, w.yArray, 'o', picker=5)

#figRef, axesArray , xRef, yRef, lineRef)
#browser = selPoints.PointBrowser(2, fig_ref,ax_ref,w.xArray, w.yArray, line_ref )

current_figure.canvas.mpl_connect('button_press_event', onclick)
#w.canvas.fig.canvas.mpl_connect('key_press_event', browser.onpress)
app.exec_()