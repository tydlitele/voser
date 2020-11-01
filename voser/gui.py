from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

import pyqtgraph as pq

import sys
from simulation import Simulator


# Subclass QMainWindow to customise your application's main window
class MainWindow(QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        self.simulator = Simulator();
        
        self.setWindowTitle("VOSER")
        

        mainLayout = QVBoxLayout()
        
        toolbar = SimulatorToolbar(self.simulator)
        self.addToolBar(toolbar)
        self.viewer= GraphViewer(self.simulator)
        source_manager = SourceManager(self.simulator.getSourcesModel());


        compute_grid_action = QAction(QIcon("img/grid.png"), "compute grid", self)
        compute_grid_action.triggered.connect(self.simulator.computeGrid)
        compute_grid_action.triggered.connect(self.viewer.plotResult)

        toolbar.addAction(compute_grid_action)
        mainLayout.addWidget(self.viewer)
        mainLayout.addWidget(source_manager)
        


        widget = QWidget()
        widget.setLayout(mainLayout)
        self.setCentralWidget(widget)

        compute_grid_action.trigger()


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
        self.setIndexWidget(self.sourcesModel.index(1,2), QCheckBox())

class SourceManager(QWidget):
    def __init__(self, model, *args, **kwargs):
        super(SourceManager, self).__init__(*args, **kwargs)
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
        self.simulator = simulator
        self.layout = QVBoxLayout()
        self.plot_widget = pq.ImageView()
        self.layout.addWidget(self.plot_widget)
        self.setLayout(self.layout)
        self.plot_widget.setPredefinedGradient("thermal")

    def plotResult(self):
        self.plot_widget.setImage(self.simulator.result_db)
        self.plot_widget.show()


