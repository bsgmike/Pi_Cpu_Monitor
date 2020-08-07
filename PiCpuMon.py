
try:
    from PyQt5.QtCore import Qt, QRectF, pyqtSignal, QT_VERSION_STR, QPoint, QDir, QDateTime, QTimer, \
        QThread, QObject, pyqtSlot, QRect, QPropertyAnimation, QAbstractTableModel, QSize

    from PyQt5.QtGui import QImage, QPixmap, QPainterPath, QPainter, QFont, QIcon, QPalette, QBrush, QPen, QFontMetrics, qRgba, QPaintEvent, QColor

    from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QTreeView, QFileSystemModel, QLineEdit, \
        QLabel, QFrame, QTextEdit,QHBoxLayout, QVBoxLayout, QMainWindow, QAction, QTableView, QTabWidget, \
        QMessageBox, QDialog, QComboBox, QStyleFactory, QCheckBox, QGridLayout, QGroupBox, QRadioButton, \
        QSizePolicy, QTableWidget, QSpinBox, QDateTimeEdit, QSlider, QScrollBar, QDial, QProgressBar, \
        QFileDialog, QScrollArea, QTextBrowser, QToolBar, QPlainTextEdit,QColorDialog
except ImportError:
        raise ImportError("ImageViewerQt: Requires PyQt5")

import sys
import pandas as pd
import random
import psutil
import time

import pickle
import numpy as np
from PIL import Image
from PIL.ImageQt import ImageQt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt


class MplCanvas(FigureCanvas):

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        # fig.tight_layout(pad=0.05)

        self.axes = fig.add_subplot(111)
        super(MplCanvas, self).__init__(fig)

class taskTimer():
    def __init__(self):
        self.startTime = 0
        self.elapsedtime = 0

    def start(self):
        self.startTime = time.time()

    def stop(self):
        self.elapsedtime = round((time.time() - self.startTime), 4)

    def getElaspedTimeStr(self):
        return str(self.elapsedtime) + " seconds"

class ResizableImageLabel(QLabel):
    def __init__(self, width, height):
        super(ResizableImageLabel, self).__init__()
        self.setAlignment(Qt.AlignLeft)
        self.setAlignment(Qt.AlignTop)
        # self.setMaximumHeight(480)
        # self.setMinimumHeight(480)
        # self.setMaximumWidth(640)
        self.setFixedWidth(width)
        self.setFixedHeight(height)
        self.setFrameStyle(QFrame.StyledPanel)
        self.showImageByPath("images\\python.png")

    def showImageByPath(self, path):

        if path:
            print("ImageLabel2:showImageByPath path = ", path)
            image = QImage(path)
            pp = QPixmap.fromImage(image)
            pixmapHeight = pp.height()
            labelHeight = self.height()
            if pixmapHeight < labelHeight:
                scalingFactor = float(pixmapHeight) / labelHeight
            else:
                scalingFactor = 1.0
            print(" Scaling factor = %f", scalingFactor)
            self.setPixmap(pp.scaled(
                self.size()*scalingFactor,
                Qt.KeepAspectRatio,
                Qt.SmoothTransformation))
            self.show()

    def showImage(self, image):

        pp = QPixmap.fromImage(image)
        pixmapHeight = pp.height()
        labelHeight = self.height()
        if pixmapHeight < labelHeight:
            scalingFactor = float(pixmapHeight) / labelHeight
        else:
            scalingFactor = 1.0
        print(" Scaling factor = ", scalingFactor)
        self.setPixmap(pp.scaled(
            self.size() * scalingFactor,
            Qt.KeepAspectRatio,
            Qt.SmoothTransformation))
        self.show()

class dataItem():
    def __init__(self, dataValue):
        self.data = pd.DataFrame({'data': [dataValue],
                       'timestamp': [pd.datetime.now()]})
    def get(self):
        return self.data

class dataFrame():
    def __init__(self):
        self.df = None
        self.maxsize = 300

    def append(self, dataItem):
        if self.df is None:
            self.df = dataItem.get()
        else:
            self.df = self.df.append(dataItem.get(), ignore_index=True)
            if self.df.shape[0] > self.maxsize:

                self.df.drop([0], inplace=True)
                # print(self.df)

    def get(self):
        return self.df


class PiCpuWidget(QWidget):
    def __init__(self):
        super(PiCpuWidget, self).__init__()


        self.topLevelLayout = QVBoxLayout()

        # self.canvas = MplCanvas(self, width=5, height=4, dpi=100)

        self.graphfigure = plt.figure()
        self.graphfigure.set_tight_layout(True)
        self.graphcanvas = FigureCanvas(self.graphfigure)

        self.topLevelLayout.addWidget(self.graphcanvas)
        self.setLayout(self.topLevelLayout)

        n_data = 50
        self.xdata = list(range(n_data))
        fred = psutil.virtual_memory()
        self.ydata = [fred.used for i in range(n_data)]
        self._plot_ref = None


        self.pandasdf = dataFrame()

        self.show()
        self.timer = QTimer()
        self.timer.setInterval(2000)
        self.timer.timeout.connect(self.pdPlot)
        self.timer.start()

    def setData(self, dataFrame):
        self.rawData = dataFrame
        self.dataView.setData(self.rawData)

    def update_plot(self):
        print("update graph")
        fred = psutil.virtual_memory()
        self.ydata = self.ydata[1:] + [fred.used,]

        pandasItem = dataItem(fred.used)
        self.pandasdf.append(pandasItem)
        # print(self.pandasdf.get())

        # Note: we no longer need to clear the axis.
        if self._plot_ref is None:
            # First time we have no plot reference, so do a normal plot.
            # .plot returns a list of line <reference>s, as we're
            # only getting one we can take the first element.
            plot_refs = self.canvas.axes.plot(self.xdata, self.ydata, 'r')
            self._plot_ref = plot_refs[0]
        else:
            # We have a reference, we can use it to update the data for that line.
            self._plot_ref.set_ydata(self.ydata)

        # Trigger the canvas to update and redraw.
        self.canvas.draw()

    def pdPlot(self):
        print('pdPlot')
        fred = psutil.virtual_memory()
        pandasItem = dataItem(fred.used)
        self.pandasdf.append(pandasItem)
        self.graphfigure.clear()
        ax = self.graphfigure.add_subplot(111)
        df = self.pandasdf.get()
        print(df.shape[0])

        if df is not None:
            df.plot(x='timestamp', y='data', ax=ax)
            ax.grid()
            ax.margins(0)
            self.graphcanvas.draw()



class PiCpuMonMainWin(QMainWindow):
    def __init__(self):
        super(PiCpuMonMainWin, self).__init__()
        self.cpuWidget = PiCpuWidget()
        #+++++++++++++++++++++++++++++++++++++++
        # Create the menu bar
        # +++++++++++++++++++++++++++++++++++++++
        closeAction = QAction("&Close and Exit", self)            #pyqt5
        closeAction.setShortcut("Ctrl+Q")
        closeAction.setStatusTip('Leave The App')
        closeAction.triggered.connect(self.close_application)

        colorSelectAction = QAction("&Select Graph BG Color", self)
        colorSelectAction.triggered.connect(self.selectGraphBGColor)

        self.statusBar()
        mainMenu = self.menuBar()
        # self.mainMenu=self.menuBar
        fileMenu = mainMenu.addMenu('&File')
        fileMenu.addAction(closeAction)

        graphMenu = mainMenu.addMenu('&Graph Options')
        graphMenu.addAction(colorSelectAction)
        self.resize(800, 600)
        self.setCentralWidget(self.cpuWidget)
        self.createToolbar()


    def createToolbar(self):
        closeAction = QAction(QIcon('icons/exit.png'), 'Close the application', self)  # pyqt5
        closeAction.triggered.connect(self.close_application)
        self.toolBar = self.addToolBar("PiCpuMon")
        toolbarLogo = ResizableImageLabel(378, 50)
        toolbarLogo.showImageByPath('icons/logo_1.png')

        self.toolBar.addAction(closeAction)
        spacer = QWidget()
        spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.toolBar.addWidget(spacer)
        self.toolBar.addWidget(toolbarLogo)
        self.toolBar.setIconSize(QSize(30, 30))

    def selectGraphBGColor(self):
        color = QColorDialog.getColor()
        # self.styleChoice.setStyleSheet("QWidget { background-color: %s}" % color.name())
        print("You selected ", str(color.getRgb()))
        print("You selected ", str(color.name()))
        # self.cpuWidget.graphView.setBGColor(color)

    def close_application(self):
        print("Exiting now...")
        sys.exit()


if __name__ == '__main__':
    app = QApplication(sys.argv)



    myCpuMon = PiCpuMonMainWin()
    myCpuMon.show()
    # plotdata = consolidated_data[consolidated_data.year == 2019]
    # print(consolidated_data[consolidated_data.Balance.isnull()])


    sys.exit(app.exec())