import sys
import os
import time
import math
from PySide2.QtWinExtras import *
from PySide2.QtCore import (Qt, Slot, Signal, SIGNAL, QPoint, QSize, QRect, QCoreApplication, QObject, QEvent, QByteArray, QPointF, QFile, QIODevice,
                            QTextStream, QMargins)

from PySide2.QtGui import (QDesktopServices, QIcon, QFont, QPixmap, QColor, QPicture, QMouseEvent, QPalette, QShowEvent,
                         QFocusEvent, QHideEvent, QResizeEvent, QPolygon, QHoverEvent, QCursor, QLinearGradient,
                         QBrush, QScreen, QGuiApplication, QRegion, QPainter, QPaintEvent, QPaintDevice, QTransform,
                           QGradient, QPaintDeviceWindow, QOpenGLShader, QOpenGLShaderProgram)
from PySide2.QtWidgets import (QLabel, QApplication, QMainWindow, QWidget, QSizePolicy, QAbstractButton, QHBoxLayout, QGridLayout,
                             QGraphicsDropShadowEffect, QGraphicsBlurEffect, QPushButton, QLayout, QLayoutItem, QTabWidget, QTabBar,
                             QVBoxLayout, QBoxLayout, QGraphicsDropShadowEffect, QToolButton, QRubberBand, QGraphicsScene,
                               QGraphicsView, QSpacerItem, QOpenGLWidget, QStackedLayout)


class UI(QObject):
    
    def __init__(self, parent):
        super(UI, self).__init__(parent)
        
        self.setGeometry()
    
    def setGeometry(self):
        self.primaryScreen = QGuiApplication.primaryScreen()
        self.availableSize = self.primaryScreen.availableSize()
        self.screenCenter = QPoint(self.availableSize.width(), self.availableSize.height()) / 2
        self.baseBlockSize = (4, 3)
        screenRatio = self.primaryScreen.geometry().width() / self.primaryScreen.geometry().height()
        blockRatio = self.baseBlockSize[0] / self.baseBlockSize[1]
        compositionRatio = 1
        
        isCurBiggerThanBlockComp = screenRatio > blockRatio * compositionRatio
        
        if isCurBiggerThanBlockComp:
            tmp_h_min = int(self.primaryScreen.geometry().height())
            tmp_w_min = int(self.primaryScreen.geometry().height() * blockRatio * compositionRatio)
        else:
            tmp_w_min = int(self.primaryScreen.geometry().width())
            tmp_h_min = int(self.primaryScreen.geometry().width() / (blockRatio * compositionRatio))
        
        temporaryBlockSizeFactor = divmod(tmp_w_min, (self.baseBlockSize[0] * 30))
        
        if temporaryBlockSizeFactor[1] != 0:
            if isCurBiggerThanBlockComp:
                self.border = temporaryBlockSizeFactor[0] + 1
            else:
                self.border = temporaryBlockSizeFactor[0]
        else:
            self.border = temporaryBlockSizeFactor[0]
        
        self.borderMargin = QMargins(self.border, self.border, self.border, self.border)
        self.borderSize = 2 * QSize(self.border, self.border)
        self.borderPosition = QPoint(self.border, self.border)
    
    def getSize(self, sizeTemplateX, sizeTemplateY):
        return QSize(int(self.baseBlockSize[0] * self.border * sizeTemplateX),
                     int(self.baseBlockSize[1] * self.border * sizeTemplateY))
    
    def setupWelcomeWindow(self):
        self.welcomeWindow = WindowInterface(self)
        self.welcomeWindow.setFixedSize(self.getSize(12, 12) + self.borderSize)
        

class WindowInterface(QWidget):
    
    def __init__(self, parent):
        super(WindowInterface, self).__init__()
        self.uiClass = parent
        self.coreClass = self.uiClass.parent()
    
    def ui(self):
        return self.uiClass
    
    def core(self):
        return self.coreClass


class UserLayer(QWidget):
    
    def __init__(self, parent=None):
        super(UserLayer, self).__init__(parent)


class ContentLayer():
    
    def __init__(self, parent=None):
        super(ContentLayer, self).__init__(parent)


class BackgroundLayerL(QLabel):
    
    def __init__(self, parent=None):
        super(BackgroundLayerL, self).__init__(parent)