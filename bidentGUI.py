import sys
import os
import time
import math
from PySide2.QtWinExtras import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtNetwork import *


class GUI(QObject):
    
    def __init__(self, parent):
        super(GUI, self).__init__(parent)
        
        self.setGeometry()
        
    def setGeometry(self):
        self.primaryScreen = QGuiApplication.primaryScreen()
        self.availableSize = self.primaryScreen.availableSize()
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
    
        temporaryBlockSizeFactor = divmod(tmp_w_min, (self.baseBlockSize[0] * 60))
    
        if temporaryBlockSizeFactor[1] != 0:
            if isCurBiggerThanBlockComp:
                self.block = temporaryBlockSizeFactor[0] + 1
            else:
                self.block = temporaryBlockSizeFactor[0]
        else:
            self.block = temporaryBlockSizeFactor[0]
            
        self.dBlock = 2 * self.block
    
    def indent(self):
        return self.block
    
    def indentSize(self):
        return QSize(self.block, self.block)
    
    def border(self):
        return self.dBlock
    
    def borderMargin(self):
        return QMargins(self.dBlock, self.dBlock, self.dBlock, self.dBlock)
    
    def borderSize(self):
        return 2 * QSize(self.dBlock, self.dBlock)
    
    def borderPosition(self):
        return QPoint(self.dBlock, self.dBlock)

    def screenCenter(self, size: QSize):
        screenCenter = QPoint(self.availableSize.width(), self.availableSize.height()) / 2
        sizePoint = QPoint(size.width(), size.height())
        return screenCenter - sizePoint / 2

    def getSize(self, width, height):
        return QSize(int(self.baseBlockSize[0] * self.block * width),
                     int(self.baseBlockSize[1] * self.block * height))
    
    def getWidth(self, width):
        return int(self.baseBlockSize[0] * self.block * width)
    
    def getHeight(self, height):
        return int(self.baseBlockSize[1] * self.block * height)
    
    def showWelcomeWindow(self):
        self.welcomeWindow = Window(self)
        self.welcomeWindow.setWindow('welcome', self.getSize(40, 30), False)
        self.welcomeWindow.setShadow()
        self.welcomeWindow.show()


class Window(QWidget):
    
    def __init__(self, parent):
        super(Window, self).__init__()
        self.uiClass = parent
        self.coreClass = self.uiClass.parent()
        
        self.setMouseTracking(True)
        self.setAttribute(Qt.WA_Hover, True)
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.setAttribute(Qt.WA_NoSystemBackground)
        self.setWindowFlags(Qt.FramelessWindowHint)
 
    def setWindow(self, type, size, isResizable):
        self.isResizable = isResizable
        self.customSizeHint = size
        
        self.setObjectName(type)
        self.setContentsMargins(self.window().gui().borderMargin())
        
        zLayout = QStackedLayout(self)
        zLayout.setContentsMargins(self.window().gui().borderMargin())
        zLayout.setSpacing(0)
        zLayout.setStackingMode(QStackedLayout.StackAll)

        if type == 'main':
            self.avatar = Avatar()
            self.layout().addWidget(self.avatar)
        else:
            pass
        self.control = ControlLayer(type, self)
        self.content = ContentLayer(type, self)
        self.background = Background(self)
        # self.background = BackgroundLayerL(type, self)
        
        self.layout().addWidget(self.control)
        self.layout().addWidget(self.content)
        self.layout().addWidget(self.background)

        self.layout().activate()

        if self.isResizable:
            self.setBorders()
        else:
            pass
        
    def setShadow(self):
        self.shadow = Shadow()
        self.shadow.setBlurRadius(self.window().gui().border())
        self.setGraphicsEffect(self.shadow)

    def setBorders(self):
        boxTopLeft = QSize(-self.window().gui().border(), -self.window().gui().border())
        boxTopRight = QSize(self.window().gui().border(), -self.window().gui().border())
        boxBottomRight = QSize(self.window().gui().border(), self.window().gui().border())
        boxBottomLeft = QSize(-self.window().gui().border(), self.window().gui().border())
        boxTop = QSize(self.layout().contentsRect().width(), -self.window().gui().border())
        boxBottom = QSize(-self.layout().contentsRect().width(), self.window().gui().border())
        boxLeft = QSize(-self.window().gui().border(), -self.layout().contentsRect().height())
        boxRight = QSize(self.window().gui().border(), self.layout().contentsRect().height())
        
        self.borderTopLeft = QRect(self.layout().contentsRect().topLeft(), boxTopLeft)
        self.borderTopRight = QRect(self.layout().contentsRect().topRight(), boxTopRight)
        self.borderBottomLeft = QRect(self.layout().contentsRect().bottomLeft(), boxBottomLeft)
        self.borderBottomRight = QRect(self.layout().contentsRect().bottomRight(), boxBottomRight)
        
        self.borderTop = QRect(self.layout().contentsRect().topLeft(), boxTop)
        self.borderRight = QRect(self.layout().contentsRect().topRight(), boxRight)
        self.borderBottom = QRect(self.layout().contentsRect().bottomRight(), boxBottom)
        self.borderLeft = QRect(self.layout().contentsRect().bottomLeft(), boxLeft)
    
    def resetBorderBox(self):
        self.onTopLeft = False
        self.onTopRight = False
        self.onBottomLeft = False
        self.onBottomRight = False
        self.onTop = False
        self.onBottom = False
        self.onLeft = False
        self.onRight = False
    
    def gui(self):
        return self.uiClass
    
    def core(self):
        return self.coreClass
    
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton and self.isResizable:
            if self.borderTopLeft.contains(event.pos()):
                self.setCursor(Qt.SizeFDiagCursor)
                self.onTopLeft = True
                self.oldPosition = self.window().geometry().topLeft()
            elif self.borderTopRight.contains(event.pos()):
                self.setCursor(Qt.SizeBDiagCursor)
                self.onTopRight = True
                self.oldPosition = self.window().geometry().topRight()
            elif self.borderBottomLeft.contains(event.pos()):
                self.setCursor(Qt.SizeBDiagCursor)
                self.onBottomLeft = True
                self.oldPosition = self.window().geometry().bottomLeft()
            elif self.borderBottomRight.contains(event.pos()):
                self.setCursor(Qt.SizeFDiagCursor)
                self.onBottomRight = True
                self.oldPosition = self.window().geometry().bottomRight()
            elif self.borderTop.contains(event.pos()):
                self.setCursor(Qt.SizeVerCursor)
                self.onTop = True
                self.oldPosition = QPoint(event.globalPos().x(), self.window().geometry().top())
            elif self.borderBottom.contains(event.pos()):
                self.setCursor(Qt.SizeVerCursor)
                self.onBottom = True
                self.oldPosition = QPoint(event.globalPos().x(), self.window().geometry().bottom())
            elif self.borderLeft.contains(event.pos()):
                self.setCursor(Qt.SizeHorCursor)
                self.onLeft = True
                self.oldPosition = QPoint(self.window().geometry().left(), event.globalPos().y())
            elif self.borderRight.contains(event.pos()):
                self.setCursor(Qt.SizeHorCursor)
                self.onRight = True
                self.oldPosition = QPoint(self.window().geometry().right(), event.globalPos().y())
            else:
                self.resetBorderBox()
                self.setCursor(Qt.ArrowCursor)
            
            self.onBottomRightRegion = self.onRight or self.onBottomRight or self.onBottom
            self.onTopLeftRegion = self.onTopLeft or self.onTop or self.onLeft
            
            if self.onBottomRightRegion or self.onTopLeftRegion or self.onBottomLeft or self.onTopRight:
                self.oldMousePosition = event.globalPos()
                self.borderDelta = self.oldPosition - event.globalPos()
                self.oldWindow = self.window().geometry()
            else:
                pass
            
            if self.onBottomRightRegion:
                self.minPosition = - QPoint(1, 1) + self.window().geometry().topLeft() + \
                                   QPoint(self.minimumSize().width(), self.minimumSize().height())
                self.maxPosition = - QPoint(1, 1) + self.window().geometry().topLeft() + \
                                   QPoint(self.maximumSize().width(), self.maximumSize().height())
            elif self.onTopLeftRegion:
                self.minPosition = QPoint(1, 1) + self.window().geometry().bottomRight() - \
                                   QPoint(self.minimumSize().width(), self.minimumSize().height())
                self.maxPosition = QPoint(1, 1) + self.window().geometry().bottomRight() - \
                                   QPoint(self.maximumSize().width(), self.maximumSize().height())
            elif self.onBottomLeft:
                self.minPosition = QPoint(1, -1) + self.window().geometry().topRight() + \
                                   QPoint(-self.minimumSize().width(), self.minimumSize().height())
                self.maxPosition = QPoint(1, -1) + self.window().geometry().topRight() + \
                                   QPoint(-self.maximumSize().width(), self.maximumSize().height())
            elif self.onTopRight:
                self.minPosition = QPoint(-1, 1) + self.window().geometry().bottomLeft() + \
                                   QPoint(self.minimumSize().width(), -self.minimumSize().height())
                self.maxPosition = QPoint(-1, 1) + self.window().geometry().bottomLeft() + \
                                   QPoint(self.maximumSize().width(), -self.maximumSize().height())
            else:
                pass
        else:
            pass
    
    def mouseReleaseEvent(self, event):
        self.oldMousePosition = None
        self.resetBorderBox()
        self.setBorders()
    
    def mouseMoveEvent(self, event: QMouseEvent):
        if self.isResizable:
            if self.borderTopLeft.contains(event.pos()):
                self.setCursor(Qt.SizeFDiagCursor)
            elif self.borderTopRight.contains(event.pos()):
                self.setCursor(Qt.SizeBDiagCursor)
            elif self.borderBottomLeft.contains(event.pos()):
                self.setCursor(Qt.SizeBDiagCursor)
            elif self.borderBottomRight.contains(event.pos()):
                self.setCursor(Qt.SizeFDiagCursor)
            elif self.borderTop.contains(event.pos()):
                self.setCursor(Qt.SizeVerCursor)
            elif self.borderBottom.contains(event.pos()):
                self.setCursor(Qt.SizeVerCursor)
            elif self.borderLeft.contains(event.pos()):
                self.setCursor(Qt.SizeHorCursor)
            elif self.borderRight.contains(event.pos()):
                self.setCursor(Qt.SizeHorCursor)
            elif self.layout().contentsRect().contains(event.pos()):
                self.setCursor(Qt.ArrowCursor)
            else:
                self.setCursor(Qt.ArrowCursor)
            
            if self.oldMousePosition:
                if self.onBottomRightRegion:
                    isXMin = event.globalPos().x() < self.minPosition.x()
                    isYMin = event.globalPos().y() < self.minPosition.y()
                    isXMax = event.globalPos().x() > self.maxPosition.x()
                    isYMax = event.globalPos().y() > self.maxPosition.y()
                elif self.onTopLeftRegion:
                    isXMin = event.globalPos().x() > self.minPosition.x()
                    isYMin = event.globalPos().y() > self.minPosition.y()
                    isXMax = event.globalPos().x() < self.maxPosition.x()
                    isYMax = event.globalPos().y() < self.maxPosition.y()
                elif self.onBottomLeft:
                    isXMin = event.globalPos().x() > self.minPosition.x()
                    isYMin = event.globalPos().y() < self.minPosition.y()
                    isXMax = event.globalPos().x() < self.maxPosition.x()
                    isYMax = event.globalPos().y() > self.maxPosition.y()
                elif self.onTopRight:
                    isXMin = event.globalPos().x() < self.minPosition.x()
                    isYMin = event.globalPos().y() > self.minPosition.y()
                    isXMax = event.globalPos().x() > self.maxPosition.x()
                    isYMax = event.globalPos().y() < self.maxPosition.y()
                else:
                    pass
                
                if isXMin:
                    deltaX = self.minPosition.x() - self.oldPosition.x()
                elif isXMax:
                    deltaX = self.maxPosition.x() - self.oldPosition.x()
                else:
                    deltaX = event.globalPos().x() - self.oldMousePosition.x()
                if isYMin:
                    deltaY = self.minPosition.y() - self.oldPosition.y()
                elif isYMax:
                    deltaY = self.maxPosition.y() - self.oldPosition.y()
                else:
                    deltaY = event.globalPos().y() - self.oldMousePosition.y()
                
                if self.onTopLeft:
                    self.setGeometry(QRect(
                        QPoint(self.oldWindow.topLeft().x() + deltaX,
                               self.oldWindow.topLeft().y() + deltaY),
                        QSize(self.oldWindow.size().width() - deltaX,
                              self.oldWindow.size().height() - deltaY)
                    ))
                elif self.onTopRight:
                    self.setGeometry(QRect(
                        QPoint(self.oldWindow.topLeft().x(),
                               self.oldWindow.topLeft().y() + deltaY),
                        QSize(self.oldWindow.size().width() + deltaX,
                              self.oldWindow.size().height() - deltaY)
                    ))
                elif self.onBottomLeft:
                    self.setGeometry(QRect(
                        QPoint(self.oldWindow.topLeft().x() + deltaX,
                               self.oldWindow.topLeft().y()),
                        QSize(self.oldWindow.size().width() - deltaX,
                              self.oldWindow.size().height() + deltaY)
                    ))
                elif self.onBottomRight:
                    self.setGeometry(QRect(
                        QPoint(self.oldWindow.topLeft()),
                        QSize(self.oldWindow.size().width() + deltaX,
                              self.oldWindow.size().height() + deltaY)
                    ))
                elif self.onTop:
                    self.setGeometry(QRect(
                        QPoint(self.oldWindow.topLeft().x(),
                               self.oldWindow.topLeft().y() + deltaY),
                        QSize(self.oldWindow.size().width(),
                              self.oldWindow.size().height() - deltaY)
                    ))
                elif self.onBottom:
                    self.setGeometry(QRect(
                        QPoint(self.oldWindow.topLeft()),
                        QSize(self.oldWindow.size().width(),
                              self.oldWindow.size().height() + deltaY)
                    ))
                elif self.onLeft:
                    self.setGeometry(QRect(
                        QPoint(self.oldWindow.topLeft().x() + deltaX,
                               self.oldWindow.topLeft().y()),
                        QSize(self.oldWindow.size().width() - deltaX,
                              self.oldWindow.size().height())
                    ))
                elif self.onRight:
                    self.setGeometry(QRect(
                        QPoint(self.oldWindow.topLeft()),
                        QSize(self.oldWindow.size().width() + deltaX,
                              self.oldWindow.size().height())
                    ))
                else:
                    pass
                
                if self.onBottomRightRegion or self.onTopLeftRegion:
                    pass
                else:
                    pass
            else:
                pass
        else:
            pass
    
    # def showMaximized(self):
    #     try:
    #         try:
    #             self.title.restore.clicked.disconnect()
    #         except:
    #             pass
    #         self.layout().setContentsMargins(0, 0, 0, 0)
    #         super(WI, self).showMaximized()
    #         self.title.restore.setIcon(QIcon(f"{scriptDir}\icon-restore.png"))
    #         self.title.restore.clicked.connect(self.window().showNormal)
    #     except:
    #         pass
    #
    # def showNormal(self):
    #     try:
    #         try:
    #             self.title.restore.clicked.disconnect()
    #         except:
    #             pass
    #         self.layout().setContentsMargins(self.window().gui().borderMargin)
    #         super(WI, self).showNormal()
    #         self.title.restore.setIcon(QIcon(f"{scriptDir}\icon-maximize.png"))
    #         self.title.restore.clicked.connect(self.window().showMaximized)
    #     except:
    #         pass
    
    def sizeHint(self) -> QSize:
        return self.customSizeHint
    
    def maximumSize(self) -> QSize:
        return self.window().gui().availableSize + self.window().gui().borderSize
    
    def leaveEvent(self, event: QEvent):
        self.updateGeometry()


class ControlLayer(QWidget):
    
    def __init__(self, type, parent=None):
        super(ControlLayer, self).__init__(parent)
        self.type = type
        self.setMouseTracking(True)
        
        self.initLayer()
        
    def initLayer(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(0)
        layout.setAlignment(Qt.AlignTop)
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)
        
        if self.type == 'welcome':
            self.setupWelcomeLayout()
        elif self.type == 'main':
            self.setupMainLayout()
        else:
            pass
    
        
        
    def setupWelcomeLayout(self):
        self.title = Title('welcome', self)
        self.bar = Bar('welcome', self)
        self.title.setupWelcomeLayout()
        self.bar.setupWelcomeLayout()
    
        self.layout().addWidget(self.title)
        self.layout().addStretch(1)
        self.layout().addWidget(self.bar)
    
    def setupMainLayout(self):
        pass
    

class ContentLayer(QWidget):

    def __init__(self, type, parent=None):
        super(ContentLayer, self).__init__(parent)
        self.type = type

        self.initLayer()

    def initLayer(self):
        layout = QHBoxLayout(self)
        layout.setSpacing(0)
        layout.setAlignment(Qt.AlignTop)
        layout.setContentsMargins(0, 0, 0, 0)

        self.setLayout(layout)

        if self.type == 'welcome':
            self.setupWelcomeLayout()

    def setupWelcomeLayout(self):
        margin = QMargins(self.window().gui().getWidth(4),
                          self.window().gui().getHeight(5),
                          self.window().gui().getWidth(4),
                          self.window().gui().getHeight(5)
                          )
        self.layout().setContentsMargins(margin)

        tabWidget = TabWidget()
        tabWidget.addTab(QWidget(), QIcon('G:\job\projects\prid1\data\dota2.png'), 'Dota 2')
        tabWidget.addTab(QWidget(), QIcon(), 'Black Desert Online')
        self.layout().addWidget(tabWidget)
        
        # tabBar = TabBarV(self)
        # tabBar.setMouseTracking(True)
        # tabBar.setAttribute(Qt.WA_Hover, True)
        #
        # tabBar.addTab('Dota 2')
        # tabBar.addTab('Black Desert Online')
        # self.layout().addWidget(tabBar)
        



class TabWidget(QTabWidget):
    
    def __init__(self, *args, **kwargs):
        QTabWidget.__init__(self, *args, **kwargs)
        self.setTabBar(TabBarV(self))
        self.setTabPosition(QTabWidget.West)

class TabBarV(QTabBar):
    
    def __init__(self, parent=None):
        super(TabBarV, self).__init__(parent)
        
    
    def tabSizeHint(self, index):
        # s = QTabBar.tabSizeHint(self, index)
        # s.transpose()
        # return s
        return self.window().gui().getSize(12, 2)
    
    
    def paintEvent(self, event):
        painter = QStylePainter(self)
        opt = QStyleOptionTab()

        for i in range(self.count()):
            self.initStyleOption(opt, i)
            painter.drawControl(QStyle.CE_TabBarTabShape, opt)
            painter.save()

            s = opt.rect.size()
            s.transpose()
            r = QRect(QPoint(), s)
            r.moveCenter(opt.rect.center())
            opt.rect = r

            c = self.tabRect(i).center()
            painter.translate(c)
            painter.rotate(90)
            painter.translate(-c)
            painter.drawControl(QStyle.CE_TabBarTabLabel, opt);
            painter.restore()
            

class BackgroundLayerL(QLabel):
    
    def __init__(self, type, parent=None):
        super(BackgroundLayerL, self).__init__(parent)
        self.type = type


class Background(QLabel):
    
    def __init__(self, parent=None):
        super(Background, self).__init__(parent)
        
        self.setMouseTracking(True)
        self.setAttribute(Qt.WA_Hover, True)
        self.setAlignment(Qt.AlignTop | Qt.AlignHCenter)
        self.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        
        self.setupWelcomeLayout()
    
    def setupWelcomeLayout(self):
        welcomeBGPMR = QPixmap()
        dir = self.window().core().dir()
        welcomeBGPMR.load(f"{dir}\data\welcomeBG.png")
        welcomeBGPM = welcomeBGPMR.scaled(self.window().sizeHint(),
                                    Qt.KeepAspectRatioByExpanding,
                                    Qt.SmoothTransformation)
        self.setPixmap(welcomeBGPM)
    
    def setupMainLayout(self):
        mainBGPMR = QPixmap(1920, 1080)
        mainBGPMR.load(f"{scriptDir}\BG-Blur.jpg")
        # mainBGPM = mainBGPMR.scaled(self.window().ui().primaryScreen.availableSize(),
        #                             Qt.KeepAspectRatioByExpanding,
        #                             Qt.SmoothTransformation)
        self.setPixmap(mainBGPMR)
    
    # def sizeHint(self) -> QSize:
    #     return self.parent().layout().contentsRect().size()


class Shadow(QGraphicsDropShadowEffect):
    
    def __init__(self, parent=None):
        super(Shadow, self).__init__(parent)
        
        self.setColor(QColor(0, 0, 0, 255))
        self.setOffset(0, 0)


class RefIcon(QLabel):
    
    def __init__(self, parent=None):
        super(RefIcon, self).__init__(parent)


class Avatar(QLabel):
    
    def __init__(self, parent=None):
        super(Avatar, self).__init__(parent)
        
        self.setObjectName("MainWindow.Avatar")
        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.setStyleSheet('background: rgba(0, 255, 255, 63);')
        
        self.initPixmap()
        self.initShadow()
        self.resize(self.sizeHint())
    
    def initPixmap(self):
        avatarRaw = QPixmap()
        avatarRaw.load(f"{scriptDir}\\avatar.png")
        self.avatarRaw = avatarRaw.scaled(self.sizeHint(),
                                          Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.avatar = self.avatarRaw.transformed(QTransform().translate(self.window().gui().border(), 0))
        # self.avatar = QPixmap(self.customSizeHint())
        # self.avatar.fill(self.avatarRaw.transformed(QTransform().translate(self.window().ui().block, 0)))
        # print(self.avatar.size())
        self.setPixmap(self.avatar)
    
    def initShadow(self):
        shadow = Shadow()
        shadow.setBlurRadius(self.window().gui().border)
        self.setGraphicsEffect(shadow)
    
    def sizeHint(self) -> QSize:
        return self.window().gui().getSize(4, 5)
    
    def minimumSize(self) -> QSize:
        return self.window().gui().getSize(4, 5)


class Title(QWidget):
    
    def __init__(self, type, parent=None):
        super(Title, self).__init__(parent)
        self.type = type
        self.setMouseTracking(True)
        self.setAttribute(Qt.WA_Hover, True)
        self.setAutoFillBackground(True)
        self.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        self.oldPosition = None
        
        self.initLayout()
        
    def initLayout(self):
        hLayout = QHBoxLayout()
        hLayout.setContentsMargins(0, 0, 0, 0)
        hLayout.setSpacing(0)
        self.setContentsMargins(0, 0, 0, 0)
        self.setLayout(hLayout)
        self.layout().activate()

    def setupWelcomeLayout(self):
        dir = self.window().core().dir()
        
        self.title = QLabel()
        self.spacer = QWidget()
        self.minimize = QPushButton()
        self.exit = QPushButton()
        
        self.title.setText(self.window().core().applicationName())
        self.title.setFixedSize(self.window().gui().getSize(3, 1))
        self.title.setIndent(int(self.window().gui().indent()))
        
        self.minimize.setIcon(QIcon(f"{dir}\data\icon-minimize.png"))
        self.minimize.setFixedSize(self.window().gui().getSize(2, 1))
        self.minimize.setIconSize(self.window().gui().getSize(1, 1) - self.window().gui().indentSize())
        self.minimize.clicked.connect(self.setMinimized)
        
        self.exit.setObjectName("Exit")
        self.exit.setIcon(QIcon(f"{dir}\data\icon-exit.png"))
        self.exit.setFixedSize(self.window().gui().getSize(2, 1))
        self.exit.setIconSize(self.window().gui().getSize(1, 1) - self.window().gui().indentSize())
        self.exit.clicked.connect(lambda: self.window().core().quit())
        
        self.layout().addWidget(self.title, Qt.AlignTop)
        self.layout().addWidget(self.spacer)
        self.layout().addWidget(self.minimize)
        self.layout().addWidget(self.exit, Qt.AlignCenter)
    
    def setupMainLayout(self):
        self.isMinimized = False
        self.title = QLabel()
        self.avatar = Avatar(self)
        self.nick = QLabel()
        self.minimize = QPushButton()
        self.restore = QPushButton()
        self.exit = QPushButton()
        self.spacerL = QWidget()
        self.spacerR = QWidget()
        
        self.title.setText(app.applicationName())
        self.title.setFixedSize(self.window().gui().getSize(14, 2))
        self.title.setIndent(self.window().gui().border())
        
        self.nick.setText(nickname)
        self.nick.setFixedSize(self.window().gui().getSize(40, 2))
        self.nick.setIndent(self.window().gui().border())
        self.nick.setObjectName("Nick")
        
        self.minimize.setIcon(QIcon(f"{scriptDir}\icon-minimize.png"))
        self.minimize.setFixedSize(self.window().gui().getSize(2, 2))
        self.minimize.setIconSize(self.window().gui().getSize(2, 2) / 3)
        self.minimize.clicked.connect(self.setMinimized)
        
        self.restore.setIcon(QIcon(f"{scriptDir}\icon-maximize.png"))
        self.restore.setFixedSize(self.window().gui().getSize(1, 1))
        self.restore.setIconSize(self.window().gui().getSize(2, 2) / 3)
        
        self.exit.setObjectName("Exit")
        self.exit.setIcon(QIcon(f"{scriptDir}\icon-exit.png"))
        self.exit.setFixedSize(self.window().gui().getSize(1, 1))
        self.exit.setIconSize(self.window().gui().getSize(2, 2) / 3)
        self.exit.clicked.connect(lambda: app.quit())
        
        self.layout().addWidget(self.title)
        self.layout().addWidget(self.spacerL)
        self.layout().addWidget(self.avatar)
        self.layout().addWidget(self.nick)
        self.layout().addWidget(self.spacerR)
        self.layout().addWidget(self.minimize)
        self.layout().addWidget(self.restore)
        self.layout().addWidget(self.exit)
    
    def setMinimized(self):
        self.window().showMinimized()
    
    def enterEvent(self, event: QEvent):
        self.setCursor(Qt.ArrowCursor)
    
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.oldPosition = event.globalPos()
            self.currentWindowPosition = self.window().geometry().topLeft()
        else:
            pass
    
    def mouseReleaseEvent(self, event):
        self.oldPosition = None
    
    def mouseMoveEvent(self, event: QMouseEvent):
        if self.oldPosition:
            deltaX = event.globalPos().x() - self.oldPosition.x()
            deltaY = event.globalPos().y() - self.oldPosition.y()
            self.window().move(QPoint(self.currentWindowPosition.x() + deltaX,
                                      self.currentWindowPosition.y() + deltaY))
        else:
            pass
    
    def sizeHint(self) -> QSize:
        if self.isMinimized:
            return QSize(self.window().layout().contentsRect().size().width(),
                         self.window().gui().getHeight(1))
        else:
            return QSize(self.window().layout().contentsRect().size().width(),
                         self.window().gui().getHeight(2))

    def paintEvent(self, event):
        painter = QPainter(self)
        option = QStyleOption()
        option.initFrom(self)
        self.style().drawPrimitive(QStyle.PE_Widget, option, painter, self)


class TabBar(QTabBar):
    
    def __init__(self, parent=None):
        super(TabBar, self).__init__(parent)
        
        self.setMouseTracking(True)
        self.setAttribute(Qt.WA_Hover, True)
        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.setShape(QTabBar.RoundedNorth)
        
        self.initTabs()
    
    def initTabs(self):
        self.addTab("Profile")
        self.addTab("Graph")
        self.addTab("League")
        self.addTab("History")
    
    def tabSizeHint(self, index: int) -> QSize:
        return self.window().gui().getSize(4, 1)


class Bar(QWidget):
    
    def __init__(self, type, parent=None):
        super(Bar, self).__init__(parent)
        self.type = type
        self.setMouseTracking(True)
        self.setAttribute(Qt.WA_Hover, True)
        self.initLayer()
        
    def initLayer(self):
        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        self.setLayout(layout)
    
    def setupWelcomeLayout(self):
        self.version = QLabel(f'v.{self.window().core().applicationVersion()}')
        self.spacer = QWidget()
        self.author = QLabel('imakiteki')

        # self.version.setAlignment(Qt.AlignLeft)
        self.version.setIndent(self.window().gui().indent())
        
        self.author.setAlignment(Qt.AlignRight|Qt.AlignVCenter)
        self.author.setIndent(self.window().gui().indent())
        
        self.layout().addWidget(self.version)
        self.layout().addWidget(self.spacer)
        self.layout().addWidget(self.author)
    
    def setupMainLayout(self):
        self.isMinimized = False
        self.dotaBident = QPushButton()
        self.dotaBident.setIcon(QIcon(f"{scriptDir}\logo.ico"))
        self.dotaBident.setIconSize(self.window().gui().getSize(1, 1) * 8 / 9)
        self.dotaBident.setFixedSize(self.window().gui().getSize(1, 1))
        
        self.stratz = QPushButton()
        self.stratz.setIcon(QIcon(f"{scriptDir}\stratz.png"))
        self.stratz.setIconSize(self.window().gui().getSize(1, 1) * 8 / 9)
        self.stratz.setFixedSize(self.window().gui().getSize(1, 1))
        
        self.dota2 = QPushButton()
        self.dota2.setIcon(QIcon(f"{scriptDir}\dota2.png"))
        self.dota2.setIconSize(self.window().gui().getSize(1, 1) * 8 / 9)
        self.dota2.setFixedSize(self.window().gui().getSize(1, 1))
        
        self.tabs = TabBar()
        
        # self.profile = QPushButton()
        # self.profile.setText("Profile")
        # self.profile.setFixedSize(self.window().ui().getSize(3, 1))
        #
        # self.graph = QPushButton()
        # self.graph.setText("Graph")
        # self.graph.setFixedSize(self.window().ui().getSize(3, 1))
        #
        # self.league = QPushButton()
        # self.league.setText("League")
        # self.league.setFixedSize(self.window().ui().getSize(3, 1))
        #
        # self.history = QPushButton()
        # self.history.setText("History")
        # self.history.setFixedSize(self.window().ui().getSize(3, 1))
        
        self.update = QPushButton()
        self.update.setIcon(QIcon(f"{scriptDir}\icon-refresh.png"))
        self.update.setIconSize(self.window().gui().getSize(1, 1) * 8 / 9)
        self.update.setFixedSize(self.window().gui().getSize(1, 1))
        
        self.settings = QPushButton()
        self.settings.setIcon(QIcon(f"{scriptDir}\icon-settings.png"))
        self.settings.setIconSize(self.window().gui().getSize(1, 1) * 8 / 9)
        self.settings.setFixedSize(self.window().gui().getSize(1, 1))
        
        self.logout = QPushButton()
        self.logout.setIcon(QIcon(f"{scriptDir}\icon-logout.png"))
        self.logout.setIconSize(self.window().gui().getSize(1, 1) * 8 / 9)
        self.logout.setFixedSize(self.window().gui().getSize(1, 1))
        
        self.spacerL = QWidget()
        self.spacerR = QWidget()
        
        self.layout().addWidget(self.dotaBident, Qt.AlignLeft, Qt.AlignTop)
        self.layout().addWidget(self.stratz, Qt.AlignLeft, Qt.AlignTop)
        self.layout().addWidget(self.dota2, Qt.AlignLeft, Qt.AlignTop)
        self.layout().addWidget(self.spacerL)
        self.layout().addWidget(self.tabs, Qt.AlignCenter, Qt.AlignTop)
        # self.layout().addWidget(self.profile, Qt.AlignHCenter, Qt.AlignTop)
        # self.layout().addWidget(self.graph, Qt.AlignHCenter, Qt.AlignTop)
        # self.layout().addWidget(self.league, Qt.AlignHCenter, Qt.AlignTop)
        # self.layout().addWidget(self.history, Qt.AlignHCenter, Qt.AlignTop)
        self.layout().addWidget(self.spacerR)
        self.layout().addWidget(self.update, Qt.AlignRight, Qt.AlignTop)
        self.layout().addWidget(self.settings, Qt.AlignRight, Qt.AlignTop)
        self.layout().addWidget(self.logout, Qt.AlignRight, Qt.AlignTop)
    
    def sizeHint(self) -> QSize:
        if self.type == 'welcome':
            return QSize(self.window().layout().contentsRect().size().width(),
                         self.window().gui().getHeight(1))
        else:
            return QSize(self.window().layout().contentsRect().size().width(),
                         self.window().gui().getHeight(2))

    def paintEvent(self, event):
        painter = QPainter(self)
        option = QStyleOption()
        option.initFrom(self)
        self.style().drawPrimitive(QStyle.PE_Widget, option, painter, self)