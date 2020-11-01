#import collections
from PyQt5 import QtCore
from PyQt5.QtCore import Qt
from recordclass import recordclass


#Source = collections.namedtuple('Source', ['x', 'y', 'active', 'invert', 'delay', 'gain'])
#Would you belive that? namedtuple is suggested as struct replacement, but is immutable

Source = recordclass('Source', ['x', 'y', 'active', 'invert', 'delay', 'gain'])

class SourcesModel(QtCore.QAbstractTableModel):
    def __init__(self, sources=None, *args, **kwargs):
        super(SourcesModel, self).__init__(*args, **kwargs)
        self.sources = sources or []

        '''self.setHeaderData(0, QtCore.Qt.Horizontal, "X")
        self.setHeaderData(1, QtCore.Qt.Horizontal, "Y")
        self.setHeaderData(2, QtCore.Qt.Horizontal, "active")
        '''
    def headerData(self, section, orientation, role):
        if role == Qt.DisplayRole:

            if orientation == Qt.Horizontal:
                return ["X", "Y", "on", "p", "delay", "gain"][section]
            if orientation == Qt.Vertical:
                return str(section)

    def data(self, index, role):
        if role == Qt.DisplayRole:
            return self.sources[index.row()][index.column()]
        if role == Qt.EditRole:
            return self.sources[index.row()][index.column()]



    def setData(self, index, value, role):
        if role == Qt.EditRole:
            self.sources[index.row()][index.column()] = value
        if (self.sources[index.row()][index.column()] == value):
            self.dataChanged.emit(index, index)
            return True
        return False
            

    def rowCount(self, index):
        return len(self.sources)

    def columnCount(self, index):
        return 6

    def add(self, source=None):
        self.sources.append(source or Source(0, 0, True, False, 0, 0))
        self.layoutChanged.emit()

    def delete(self, indices):
        row_set = set()
        if type(indices)==list:
            for index in indices:
                print(type(index))
                row_set.add(index.row())

        else:
            row_set.add(indices.row())

        if row_set:
            row_indices = list(row_set)
            row_indices.sort(reverse=True)
            print(row_indices)
            for  row_index in row_indices:
                del self.sources[row_index]
            self.layoutChanged.emit()

    def flags(self, index):
        if (2 == index.column() or index.column() == 3):
            return Qt.ItemIsEnabled | Qt.ItemIsSelectable | Qt.ItemIsEditable# | Qt.ItemIsCheckable
        return Qt.ItemIsEnabled | Qt.ItemIsSelectable | Qt.ItemIsEditable




