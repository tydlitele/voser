from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

import pyqtgraph as pg
import sys
from simulation import Simulator

import checkbox
import datamodel

# Subclass QMainWindow to customise your application's main window
class MainWindow(QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)


        sub1 = datamodel.Source(-1, 0, True, False, 0, 0)
        sub2 = datamodel.Source(1, 0, True, False, 0, 0)        
        initialList=[sub1, sub2]

        self.sourcesModel = datamodel.SourcesModel(initialList)

        self.simulator = Simulator();
        
        self.setWindowTitle("VOSER")
        #self.setGeometry(0,0,768,960)
        self.resize(760, 860)
        

        mainLayout = QVBoxLayout()
        
        toolbar = SimulatorToolbar(self.simulator)
        self.addToolBar(toolbar)
        self.viewer= GraphViewer(self.simulator)
        source_manager = SourceManager(self.sourcesModel)

        compute = lambda : self.simulator.compute(self.sourcesModel.getActiveSources())

        #print(self.sourcesModel.getActiveSources())

        compute_action = QAction(QIcon("./img/compute.png"), "compute grid", self)
        compute_action.triggered.connect(compute)
        '''
        compute = lambda sources=self.sourcesModel.getActiveSources(): self.simulator.compute(sources)
        '''
        compute_action.triggered.connect(self.viewer.plotResult)
        toolbar.addAction(compute_action)
        mainLayout.addWidget(self.viewer)
        mainLayout.addWidget(source_manager)
        


        widget = QWidget()
        widget.setLayout(mainLayout)
        self.setCentralWidget(widget)

        compute_action.trigger()


class SimulatorToolbar(QToolBar):
    def __init__(self, simulator, *args, **kwargs):
        super(SimulatorToolbar, self).__init__(*args, **kwargs)
        self.simulator = simulator
        self.setIconSize(QSize(32,32))


class SourceTableView(QTableView):
    def __init__(self, model, *args, **kwargs):
        super(SourceTableView, self).__init__(*args, **kwargs)
        self.sourcesModel = model

        self.setModel(self.sourcesModel)
        self.setItemDelegateForColumn(2, checkbox.CheckBoxDelegate(self))
        self.setItemDelegateForColumn(3, checkbox.CheckBoxDelegate(self))

        self.setColumnWidth(0, 20)
        self.setColumnWidth(1, 20)

        self.setColumnWidth(2, self.rowHeight(0))
        self.setColumnWidth(3, 10)


class SourceManager(QWidget):
    def __init__(self, model, *args, **kwargs):
        super(SourceManager, self).__init__(*args, **kwargs)
        self.setFixedHeight(300)
        self.setFixedWidth(600)
        self.sourcesModel = model;
        self.layout = QVBoxLayout()

        self.actionLayout = QHBoxLayout()

        self.addButton = QPushButton("add")
        self.delButton = QPushButton("remove")

        self.actionLayout.addWidget(self.addButton)
        self.actionLayout.addWidget(self.delButton)

        self.tableView = SourceTableView(self.sourcesModel)
        self.layout.addWidget(self.tableView)
        self.layout.addLayout(self.actionLayout)
        self.setLayout(self.layout)

        self.addButton.pressed.connect(self.addSource)
        self.delButton.pressed.connect(self.deleteSource)

    def addSource(self, source=None):
        self.sourcesModel.add()

    def deleteSource(self, indices=None):
        if not indices:
            indices = self.tableView.selectedIndexes()

        for i in indices:
            print("{}, {}".format(i.row(), i.column()))
        self.sourcesModel.delete(indices)

        pass



class GraphViewer(QWidget):
    def __init__(self, simulator, *args, **kwargs):
        super(QWidget, self).__init__(*args, **kwargs)
        self.resize(800, 600)
        self.simulator = simulator
        self.layout = QVBoxLayout()

        self.plt = pg.PlotItem(labels={'bottom': ('x', 'm'), 'left': ('y', 'm')})
        self.view = pg.ImageView(view=self.plt)

        self.layout.addWidget(self.view)
        self.setLayout(self.layout)
        self.view.setPredefinedGradient("thermal")

    def plotResult(self):


        #first prepare scale factor for axes
        x0, x1 = self.simulator.xRange()
        y0, y1 = self.simulator.yRange()
        xscale, yscale = (x1-x0) / self.simulator.xsamples, (y1-y0) / self.simulator.ysamples

    
        self.view.setImage(self.simulator.result.T, pos=[x0, y0], scale=[xscale, yscale])
        self.plt.setAspectLocked(True)
        self.view.show()
