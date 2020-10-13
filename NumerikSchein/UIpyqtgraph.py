from mathFunct import *      #importing package relating to numeric project

import pyqtgraph as pg
from PyQt5 import QtWidgets, QtCore
from pyqtgraph import PlotWidget, plot
import sys  # We need sys so that we can pass argv to QApplication
import os

# #funtion to check for mouse events?!
# def mouseMoved(evt):
#   mousePoint = p.vb.mapSceneToView(evt[0])
#   label.setText("<span style='font-size: 14pt; color: white'> x = %0.2f, <span style='color: white'> y = %0.2f</span>" % (mousePoint.x(), mousePoint.y()))  
 

#creates a contained canvas in wich plots of any type can be added and configured
class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        self.graphWidget = pg.PlotWidget()
        self.setCentralWidget(self.graphWidget)

        self.x_default = [1,2,3,4,5,6,7,8,9,10]
        self.y_default = [30,32,34,32,33,31,29,32,35,45]
        
        #-----------------Background-----------------
        #set the background to white (w), blue (b),green(g), red(r), cyan(c)... 
        #or using hex notation as string: self.graphWidget.setBackground('#bbccaa') 
        #or RGB values as tuples: self.graphWidget.setBackground((100,50,255))
        self.graphWidget.setBackground('b') 
        
        #-----------------Add Title------------------    
        title= 'your title here'
        self.graphWidget.setTitle(title, color="b", size="30pt")
        
        #-----------------Add Axis Labels-------------
        #The position can be any one of 'left,'right','top','bottom'
        #Because the name font-size has a hyphen in it, you cannot pass it directly as a parameter, but must use the **dictionary method
        self.styles = {"color": "#f00", "font-size": "20px"}
        self.xAxisLabel="x-AxisName"
        self.yAxisLabel= "y-AxisName"
        
        self.graphWidget.setLabel("left", self.xAxisLabel, **self.styles)
        self.graphWidget.setLabel("bottom", self.yAxisLabel, **self.styles)
        
        #-----------------Add legend------------------
        # Adding a legend to a plot can be accomplished by calling .addLegend on the PlotWidget, however before this will work you need to provide a name for each line when calling .plot().
        lineOneName = "line 1"
        
        self.graphWidget.addLegend()
        
        #-----------------Add grid--------------------
        self.graphWidget.showGrid(x=True, y=True)
        
        #-----------------Line Style-----------------
        # assign color, width, style and symbols to created pen
        #styles: Qt.SolidLine, Qt.DashLine, Qt.DotLine, Qt.DashDotLine, Qt.DashDotDotLine
        penWidth = 7
        penStyle = QtCore.Qt.SolidLine
        
        #-----------------Set Axis Range-------------
        self.graphWidget.setXRange(0, 40, padding=0)
        self.graphWidget.setYRange(0, 120, padding=0)
        
        #-----------------adding Symbols
        #adding symbols like o(circular), s (square), t (triangular), d (Diamond), + (cross)
        #In addition to symbol you can also pass in symbolSize, symbolBrush and symbolPen paramete
        penSymbol = '+'
        
        #-----------------creating the new pen---------
        #create a new Qpen instance and pass it into the plot method
        pen = pg.mkPen(color=(255,0,10), width = penWidth, style = penStyle)

        # plot data: x, y values  
        #two plot multiple lines reacll plot with different dataset and content
        self.plotLine = self.graphWidget.plot(self.x_default, self.y_default,name = lineOneName, pen=pen, symbol=penSymbol)

        #------------------Updating the plot-------------
        #To update a line we need a reference to the line object: 
            #my_line_ref = graphWidget.plot(x, y)
        #updating plot through:
            #self.data_line.setData(self.x, self.y)
            
            #cross hair
        vLine = pg.InfiniteLine(angle=90, movable=False)
        hLine = pg.InfiniteLine(angle=0, movable=False)
        self.graphWidget.addItem(vLine, ignoreBounds=True)
        self.graphWidget.addItem(hLine, ignoreBounds=True)


        vb = graphWidget.vb

        def mouseMoved(evt):
            pos = evt[0]  ## using signal proxy turns original arguments into a tuple
            if p1.sceneBoundingRect().contains(pos):
                mousePoint = vb.mapSceneToView(pos)
                index = int(mousePoint.x())
                if index > 0 and index < len(data1):
                    label.setText("<span style='font-size: 12pt'>x=%0.1f,   <span style='color: red'>y1=%0.1f</span>,   <span style='color: green'>y2=%0.1f</span>" % (mousePoint.x(), data1[index], data2[index]))
                vLine.setPos(mousePoint.x())
                hLine.setPos(mousePoint.y())

        proxy = pg.SignalProxy(p1.scene().sigMouseMoved, rateLimit=60, slot=mouseMoved)
        #p1.scene().sigMouseMoved.connect(mouseMoved)

    def changeData(self, *args, **kwargs):
        [readSuccess,self.xAxisLabel, self.yAxisLabel, self.x_default, self.y_default]=readFunct.getData()
        
        if not readSuccess:
            print("Path was incorrect or file was empty")
            
        self.updateGraph()
            
    def updateGraph(self):
        
        self.graphWidget.setLabel("left", self.xAxisLabel, **self.styles)
        self.graphWidget.setLabel("bottom", self.yAxisLabel, **self.styles)
        
        self.plotLine.setData(self.x_default, self.y_default)
 
    
class MouseClickEvent(object):
    """
    Instances of this class are delivered to items in a :class:`GraphicsScene <pyqtgraph.GraphicsScene>` via their mouseClickEvent() method when the item is clicked. 
    
    
    """
    
    def __init__(self, pressEvent, double=False):
        self._scenePos = pressEvent.scenePos()

    def scenePos(self):
        """Return the current scene position of the mouse."""
        return Point(self._scenePos)
    
if __name__ == "__main__":
    def run_app():
        app = QtWidgets.QApplication(sys.argv)
        mainWin = MainWindow()
        
        mainWin.changeData()
        
        mainWin.show()
        app.exec_()
        
        
    run_app()
    
    



    

    