from main import *
from pyqtgraph import PlotWidget
import pyqtgraph as pg

GLOBAL_STATE = 0
GLOBAL_STATE_GRAPH = 0
GLOBAL_STATE_DEBUG = 0


class UiFunctions(MainWindow):
    def maximize_restore(self):
        global GLOBAL_STATE
        status = GLOBAL_STATE

        if status == 0:
            self.showMaximized()
            GLOBAL_STATE = 1

            self.ui.verticalLayout.setContentsMargins(0, 0, 0, 0)
            self.ui.btn_maximize.setToolTip('Restore')

        else:
            GLOBAL_STATE = 0
            self.showNormal()
            self.resize(self.width(), self.height())
            self.ui.verticalLayout.setContentsMargins(10, 10, 10, 10)
            self.ui.btn_maximize.setToolTip('Maximize')

    def ui_definitions(self):
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

        self.shadow = QGraphicsDropShadowEffect(self)
        self.shadow.setBlurRadius(20)
        self.shadow.setXOffset(0)
        self.shadow.setYOffset(0)
        self.shadow.setColor(QColor(0, 0, 0, 100))

        self.ui.Background.setGraphicsEffect(self.shadow)

        self.ui.btn_maximize.clicked.connect(lambda: UiFunctions.maximize_restore(self))
        self.ui.btn_minimize.clicked.connect(lambda: self.showMinimized())
        self.ui.btn_close.clicked.connect(lambda: self.close())

        self.sizegrip = QSizeGrip(self.ui.frame_grip)
        self.sizegrip.setStyleSheet('QSizeGrip {width: 30px; height: 30px; margin: 5px}')
        self.sizegrip.setToolTip('Resize Window')

    def return_status(self):
        return GLOBAL_STATE


class SplashScreenFunctions(SplashScreen):
    def ui_definitions(self):
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

        self.shadow = QGraphicsDropShadowEffect(self)
        self.shadow.setBlurRadius(20)
        self.shadow.setXOffset(0)
        self.shadow.setYOffset(0)
        self.shadow.setColor(QColor(0, 0, 0, 100))

        self.ui.Splashscreen.setGraphicsEffect(self.shadow)


class GraphFunctions(GraphWindow):
    def maximize_restore(self):
        global GLOBAL_STATE_GRAPH
        status = GLOBAL_STATE_GRAPH

        if status == 0:
            self.showMaximized()
            GLOBAL_STATE_GRAPH = 1

            self.ui.horizontalLayout.setContentsMargins(0, 0, 0, 0)
            self.ui.btn_maximize.setToolTip('Restore')

        else:
            GLOBAL_STATE_GRAPH = 0
            self.showNormal()
            self.resize(self.width(), self.height())
            self.ui.horizontalLayout.setContentsMargins(10, 10, 10, 10)
            self.ui.btn_maximize.setToolTip('Maximize')

    def ui_definitions(self):
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

        self.shadow = QGraphicsDropShadowEffect(self)
        self.shadow.setBlurRadius(20)
        self.shadow.setXOffset(0)
        self.shadow.setYOffset(0)
        self.shadow.setColor(QColor(0, 0, 0, 100))

        self.ui.Background.setGraphicsEffect(self.shadow)

        self.ui.btn_maximize.clicked.connect(lambda: UiFunctions.maximize_restore(self))
        self.ui.btn_minimize.clicked.connect(lambda: self.showMinimized())
        self.ui.btn_close.clicked.connect(lambda: self.close())

        self.sizegrip = QSizeGrip(self.ui.frame_grip_2)
        self.sizegrip.setStyleSheet('QSizeGrip {width: 30px; height: 30px; margin: 5px}')
        self.sizegrip.setToolTip('Resize Window')

    def return_status(self):
        return GLOBAL_STATE_GRAPH


class DebugFunctions(DebugWindow):
    def maximize_restore(self):
        global GLOBAL_STATE_DEBUG
        status = GLOBAL_STATE_DEBUG

        if status == 0:
            self.showMaximized()
            GLOBAL_STATE_DEBUG = 1

            self.ui.horizontalLayout.setContentsMargins(0, 0, 0, 0)
            self.ui.btn_maximize.setToolTip('Restore')

        else:
            GLOBAL_STATE_DEBUG = 0
            self.showNormal()
            self.resize(self.width(), self.height())
            self.ui.horizontalLayout.setContentsMargins(10, 10, 10, 10)
            self.ui.btn_maximize.setToolTip('Maximize')

    def ui_definitions(self):

        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)

        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

        self.shadow = QGraphicsDropShadowEffect(self)
        self.shadow.setBlurRadius(20)
        self.shadow.setXOffset(0)
        self.shadow.setYOffset(0)
        self.shadow.setColor(QColor(0, 0, 0, 100))

        self.ui.Background.setGraphicsEffect(self.shadow)

        self.ui.btn_close.clicked.connect(lambda: self.close())

        self.sizegrip = QSizeGrip(self.ui.frame_grip_2)
        self.sizegrip.setStyleSheet('QSizeGrip {width: 30px; height: 30px; margin: 5px}')
        self.sizegrip.setToolTip('Resize Window')

    def return_status(self):
        return GLOBAL_STATE_DEBUG
