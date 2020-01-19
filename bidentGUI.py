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
        
        self.guiSettings()
    
    def guiSettings(self):
        pass
    
    def showWelcomeWindow(self):
        pass


class WindowInterface(QWidget):
    
    def __init__(self, parent):
        super(WindowInterface, self).__init__()
        self.uiClass = parent
        self.coreClass = self.uiClass.parent()
        
        self.setMouseTracking(True)
        self.setAttribute(Qt.WA_Hover, True)
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.setAttribute(Qt.WA_NoSystemBackground)
        self.setWindowFlags(Qt.FramelessWindowHint)
    
    def setSkeleton(self, size, isResizable):
        self.isResizable = isResizable
        self.customSizeHint = size
        
        zLayout = QStackedLayout(self)
        if self.isResizable:
            zLayout.setSizeConstraint(QLayout.SetMinAndMaxSize)
        else:
            zLayout.setSizeConstraint(QLayout.SetFixedSize)
        
        zLayout.setContentsMargins(self.window().ui().borderMargin)
        zLayout.setSpacing(0)
        zLayout.setStackingMode(QStackedLayout.StackAll)
        print(zLayout.geometry().size())
        self.setLayout(zLayout)
        self.layout().activate()
        
        uiLayout = QVBoxLayout(self)
        uiLayout.setSpacing(0)
        uiLayout.setAlignment(Qt.AlignTop)
        
        self.title = Title(self)
        self.bar = Bar(self)
        
        uiLayout.addWidget(self.title)
        uiLayout.addStretch(1)
        uiLayout.addWidget(self.bar)
        
        bgLayout = QVBoxLayout(self)
        bgLayout.setSpacing(0)
        self.background = Background(self)
        bgLayout.addWidget(self.background)
        
        self.layout().addChildLayout(uiLayout)
        self.layout().addChildLayout(bgLayout)
        self.layout().activate()
        self.resize(size)
    
    def setBorders(self):
        boxTopLeft = QSize(-self.window().ui().border, -self.window().ui().border)
        boxTopRight = QSize(self.window().ui().border, -self.window().ui().border)
        boxBottomRight = QSize(self.window().ui().border, self.window().ui().border)
        boxBottomLeft = QSize(-self.window().ui().border, self.window().ui().border)
        boxTop = QSize(self.layout().contentsRect().width(), -self.window().ui().border)
        boxBottom = QSize(-self.layout().contentsRect().width(), self.window().ui().border)
        boxLeft = QSize(-self.window().ui().border, -self.layout().contentsRect().height())
        boxRight = QSize(self.window().ui().border, self.layout().contentsRect().height())
        
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
    
    def ui(self):
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
    
    def showMaximized(self):
        try:
            try:
                self.title.restore.clicked.disconnect()
            except:
                pass
            self.layout().setContentsMargins(0, 0, 0, 0)
            super(WI, self).showMaximized()
            self.title.restore.setIcon(QIcon(f"{scriptDir}\icon-restore.png"))
            self.title.restore.clicked.connect(self.window().showNormal)
        except:
            pass
    
    def showNormal(self):
        try:
            try:
                self.title.restore.clicked.disconnect()
            except:
                pass
            self.layout().setContentsMargins(self.window().ui().borderMargin)
            super(WI, self).showNormal()
            self.title.restore.setIcon(QIcon(f"{scriptDir}\icon-maximize.png"))
            self.title.restore.clicked.connect(self.window().showMaximized)
        except:
            pass
    
    def resizeEvent(self, event: QResizeEvent):
        self.background.updateGeometry()
        self.background.resize(self.layout().contentsRect().size())
    
    def sizeHint(self) -> QSize:
        return self.customSizeHint
    
    def maximumSize(self) -> QSize:
        return self.window().ui().availableSize + self.window().ui().borderSize
    
    def leaveEvent(self, event: QEvent):
        self.updateGeometry()


class UserLayer(QWidget):
    
    def __init__(self, parent=None):
        super(UserLayer, self).__init__(parent)


class ContentLayer():
    
    def __init__(self, parent=None):
        super(ContentLayer, self).__init__(parent)


class BackgroundLayerL(QLabel):
    
    def __init__(self, parent=None):
        super(BackgroundLayerL, self).__init__(parent)


class Background(QLabel):
    
    def __init__(self, parent=None):
        super(Background, self).__init__(parent)
        
        self.setMouseTracking(True)
        self.setAttribute(Qt.WA_Hover, True)
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.setAlignment(Qt.AlignTop | Qt.AlignHCenter)
        self.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
    
    def setupWelcomeLayout(self):
        welcomeBGPMR = QPixmap()
        welcomeBGPMR.load(f"{scriptDir}\welcomeBG.png")
        # welcomeBGPM = welcomeBGPMR.scaled(self.window().ui.getSize(12, 12),
        #                             Qt.KeepAspectRatioByExpanding,
        #                             Qt.SmoothTransformation)
        self.setPixmap(welcomeBGPMR)
    
    def setupMainLayout(self):
        mainBGPMR = QPixmap(1920, 1080)
        mainBGPMR.load(f"{scriptDir}\BG-Blur.jpg")
        # mainBGPM = mainBGPMR.scaled(self.window().ui().primaryScreen.availableSize(),
        #                             Qt.KeepAspectRatioByExpanding,
        #                             Qt.SmoothTransformation)
        self.setPixmap(mainBGPMR)
    
    def sizeHint(self) -> QSize:
        return self.parent().layout().contentsRect().size()


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
        self.avatar = self.avatarRaw.transformed(QTransform().translate(self.window().ui().border, 0))
        # self.avatar = QPixmap(self.sizeHint())
        # self.avatar.fill(self.avatarRaw.transformed(QTransform().translate(self.window().ui().border, 0)))
        # print(self.avatar.size())
        self.setPixmap(self.avatar)
    
    def initShadow(self):
        shadow = Shadow()
        shadow.setBlurRadius(self.window().ui().border)
        self.setGraphicsEffect(shadow)
    
    def sizeHint(self) -> QSize:
        return self.window().ui().getSize(4, 5)
    
    def minimumSize(self) -> QSize:
        return self.window().ui().getSize(4, 5)


class Title(QLabel):
    
    def __init__(self, parent=None):
        super(Title, self).__init__(parent)
        
        self.setMouseTracking(True)
        self.setAttribute(Qt.WA_Hover, True)
        self.setAutoFillBackground(True)
        self.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        
        self.oldPosition = None
    
    def setSkeleton(self):
        self.isMinimized = False
        
        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        self.setLayout(layout)
        self.layout().activate()
    
    def setupWelcomeLayout(self):
        self.isMinimized = True
        self.title = QLabel()
        self.spacer = QWidget()
        self.minimize = QPushButton()
        self.exit = QPushButton()
        
        self.title.setText(app.applicationName())
        self.title.setFixedSize(self.window().ui().getSize(3, 1) / 2)
        self.title.setObjectName("WelcomeProgramName")
        self.title.setIndent(int(self.window().ui().border / 2))
        
        self.minimize.setIcon(QIcon(f"{scriptDir}\icon-minimize.png"))
        self.minimize.setFixedSize(self.window().ui().getSize(2, 1) / 2)
        self.minimize.setIconSize(self.window().ui().getSize(1, 1) / 3)
        self.minimize.clicked.connect(self.setMinimized)
        
        self.exit.setObjectName("Exit")
        self.exit.setIcon(QIcon(f"{scriptDir}\icon-exit.png"))
        self.exit.setFixedSize(self.window().ui().getSize(2, 1) / 2)
        self.exit.setIconSize(self.window().ui().getSize(1, 1) / 3)
        self.exit.clicked.connect(lambda: app.quit())
        
        self.layout().addWidget(self.title, Qt.AlignTop)
        self.layout().addWidget(self.spacer)
        self.layout().addWidget(self.minimize)
        self.layout().addWidget(self.exit)
    
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
        self.title.setFixedSize(self.window().ui().getSize(7, 1))
        self.title.setIndent(self.window().ui().border)
        
        self.nick.setText(nickname)
        self.nick.setFixedSize(self.window().ui().getSize(20, 1))
        self.nick.setIndent(self.window().ui().border)
        self.nick.setObjectName("Nick")
        
        self.minimize.setIcon(QIcon(f"{scriptDir}\icon-minimize.png"))
        self.minimize.setFixedSize(self.window().ui().getSize(1, 1))
        self.minimize.setIconSize(2 * self.window().ui().getSize(1, 1) / 3)
        self.minimize.clicked.connect(self.setMinimized)
        
        self.restore.setIcon(QIcon(f"{scriptDir}\icon-maximize.png"))
        self.restore.setFixedSize(self.window().ui().getSize(1, 1))
        self.restore.setIconSize(2 * self.window().ui().getSize(1, 1) / 3)
        
        self.exit.setObjectName("Exit")
        self.exit.setIcon(QIcon(f"{scriptDir}\icon-exit.png"))
        self.exit.setFixedSize(self.window().ui().getSize(1, 1))
        self.exit.setIconSize(2 * self.window().ui().getSize(1, 1) / 3)
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
                         int(self.window().ui().getSize(30, 1).height() / 2))
        else:
            return QSize(self.window().layout().contentsRect().size().width(),
                         self.window().ui().getSize(30, 1).height())


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
        return self.window().ui().getSize(4, 1)


class Bar(QLabel):
    
    def __init__(self, parent=None):
        super(Bar, self).__init__(parent)
        
        self.setMouseTracking(True)
        self.setAttribute(Qt.WA_Hover, True)
        self.setAutoFillBackground(True)
        
        self.isMinimized = False
    
    def setSkeleton(self):
        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        self.setLayout(layout)
        self.layout().activate()
    
    def setupWelcomeLayout(self):
        self.isMinimized = True
    
    def setupMainLayout(self):
        self.isMinimized = False
        self.dotaBident = QPushButton()
        self.dotaBident.setIcon(QIcon(f"{scriptDir}\logo.ico"))
        self.dotaBident.setIconSize(self.window().ui().getSize(1, 1) * 8 / 9)
        self.dotaBident.setFixedSize(self.window().ui().getSize(1, 1))
        
        self.stratz = QPushButton()
        self.stratz.setIcon(QIcon(f"{scriptDir}\stratz.png"))
        self.stratz.setIconSize(self.window().ui().getSize(1, 1) * 8 / 9)
        self.stratz.setFixedSize(self.window().ui().getSize(1, 1))
        
        self.dota2 = QPushButton()
        self.dota2.setIcon(QIcon(f"{scriptDir}\dota2.png"))
        self.dota2.setIconSize(self.window().ui().getSize(1, 1) * 8 / 9)
        self.dota2.setFixedSize(self.window().ui().getSize(1, 1))
        
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
        self.update.setIconSize(self.window().ui().getSize(1, 1) * 8 / 9)
        self.update.setFixedSize(self.window().ui().getSize(1, 1))
        
        self.settings = QPushButton()
        self.settings.setIcon(QIcon(f"{scriptDir}\icon-settings.png"))
        self.settings.setIconSize(self.window().ui().getSize(1, 1) * 8 / 9)
        self.settings.setFixedSize(self.window().ui().getSize(1, 1))
        
        self.logout = QPushButton()
        self.logout.setIcon(QIcon(f"{scriptDir}\icon-logout.png"))
        self.logout.setIconSize(self.window().ui().getSize(1, 1) * 8 / 9)
        self.logout.setFixedSize(self.window().ui().getSize(1, 1))
        
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
        if self.isMinimized:
            return QSize(self.window().layout().contentsRect().size().width(),
                         int(self.window().ui().getSize(30, 1).height() / 2))
        else:
            return QSize(self.window().layout().contentsRect().size().width(),
                         self.window().ui().getSize(30, 1).height())
