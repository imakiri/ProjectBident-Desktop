from PyQt5 import QtCore


class Core(QtCore.QObject):
    
    def __init__(self, parent=None):
        super(Core, self).__init__(parent)
