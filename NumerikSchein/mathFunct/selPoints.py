# -*- coding: utf-8 -*-
"""
Created on Sat Sep 12 08:31:47 2020

@author: Giampiero
"""

# import numpy as np
# import matplotlib.pyplot as plt

# class PointBrowser(object):
#     """
#     Click on a point to select and highlight it -- the data that
#     generated the point will be shown in the lower axes.  Use the 'n'
#     and 'p' keys to browse through the next and previous points
#     """

#     def __init__(self, figRef = plt.figure(), axs_ref= plt.figure.add_subplot(111), row=1, columns=1):
#         self.lastind = 0
#         #plot('o', ms=12, alpha=0.4, color='yellow', visible=False)
    
#         self.selected = figRef
#         axs_ref.plot([xs[0]], [ys[0]],'o', ms=12, alpha=0.4, color='yellow', visible=False)

#     def onpress(self, event):
#         if self.lastind is None:
#             return
#         if event.key not in ('n', 'p'):
#             return
#         if event.key == 'n':
#             inc = 1
#         else:
#             inc = -1

#         self.lastind += inc
#         self.lastind = np.clip(self.lastind, 0, len(xs) - 1)
#         self.update()

import numpy as np


class PointBrowser(object):
    """
    Click on a point to select and highlight it -- the data that
    generated the point will be shown in the lower axes.  Use the 'n'
    and 'p' keys to browse through the next and previous points
    """

    def __init__(self, subPlotNumber, figRef, axRef1 , xRef, yRef, lineRef):
        
        self.fig = figRef
        self.lastind = 0
        self.ax1 = axRef1
        #self.ax2 = axRef2
        #self.axes[1] = axesArray[1]
        self.xs = xRef
        self.ys = yRef
        self.line = lineRef

        self.text = self.ax1.text(0.05, 0.95, 'selected: none',
                            transform= self.ax1.transAxes, va='top')
        self.selected, = self.ax1.plot(self.xs, self.ys, 'o', ms=12, alpha=0.4,
                                 color='yellow', visible=False)

    def onpress(self, event):
        if self.lastind is None:
            return
        if event.key not in ('n', 'p'):
            return
        if event.key == 'n':
            inc = 1
        else:
            inc = -1

        self.lastind += inc
        self.lastind = np.clip(self.lastind, 0, len(self.xs) - 1)
        self.update()

    def onpick(self, event):

        if event.artist != self.line:
            return True

        N = len(event.ind)
        if not N:
            return True

        # the click locations
        x = event.mouseevent.xdata
        y = event.mouseevent.ydata

        distances = np.hypot(x - self.xs[event.ind], y - self.ys[event.ind])
        indmin = distances.argmin()
        dataind = event.ind[indmin]

        self.lastind = dataind
        self.update()

    def update(self):
        if self.lastind is None:
            return

        dataind = self.lastind

        self.ax2.cla()

        self.ax2.text(0.05, 0.9, 'mu=%1.3f\nsigma=%1.3f' % (self.xs[dataind], self.ys[dataind]),
                 transform=self.axes[1].transAxes, va='top')
        self.ax2.set_ylim(-0.5, 1.5)
        self.selected.set_visible(True)
        self.selected.set_data(self.xs[dataind], self.ys[dataind])

        self.text.set_text('selected: %d' % dataind)
        self.fig.canvas.draw()


# if __name__ == '__main__':
#     import matplotlib.pyplot as plt
#     # Fixing random state for reproducibility
#     np.random.seed(19680801)

#     X = np.random.rand(100, 200)
#     xs = np.mean(X, axis=1)
#     ys = np.std(X, axis=1)

#     fig, (ax, ax2) = plt.subplots(2, 1)
#     ax.set_title('click on point to plot time series')
#     line, = ax.plot(xs, ys, 'o', picker=5)  # 5 points tolerance

#     browser = PointBrowser()

#     fig.canvas.mpl_connect('pick_event', browser.onpick)
#     fig.canvas.mpl_connect('key_press_event', browser.onpress)

#     plt.show()