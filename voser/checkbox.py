from PyQt5 import QtGui, QtWidgets, QtCore

class CheckBoxDelegate(QtWidgets.QItemDelegate):
    """
    A delegate that places a fully functioning QCheckBox cell of the column to which it's applied.
    """
    def __init__(self, parent):
        QtWidgets.QItemDelegate.__init__(self, parent)

    def createEditor(self, parent, option, index):
        """
        Important, otherwise an editor is created if the user clicks in this cell.
        """
        return None

    def paint(self, painter, option, index):
        """
        Paint a checkbox without the label.
        """
        self.drawCheck(painter, option, option.rect, QtCore.Qt.Unchecked if int(index.data()) == 0 else QtCore.Qt.Checked)

    def editorEvent(self, event, model, option, index):
        '''
        Change the data in the model and the state of the checkbox
        if the user presses the left mousebutton and this cell is editable. Otherwise do nothing.
        '''
        if not int(index.flags() & QtCore.Qt.ItemIsEditable) > 0:
            return False

        if event.type() == QtCore.QEvent.MouseButtonRelease and event.button() == QtCore.Qt.LeftButton:
            # Change the checkbox-state
            self.setModelData(None, model, index)
            return True

        return False


    def setModelData (self, editor, model, index):
        '''
        The user wanted to change the old state in the opposite.
        '''
        model.setData(index, 1 if int(index.data()) == 0 else 0, QtCore.Qt.EditRole)
