import sys

from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5 import QtWidgets

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from ui_main import Ui_MainWindow
from ui_graph import Ui_GuiGraph
from ui_debug import Ui_GuiDebug
from ui_splashscreen import Ui_MainWindow as Ui_SplashScreen
from ui_functions import *
from myserial import *
from mygis import *
from mypcclock import *
import paho.mqtt.client as mqtt

CLIENT_NAME = 'P1'

BROKER_ADDRESS = 'ip.realneil4884.com'

GLOBAL_SPLASH_COUNTER = 0

com = ComPort()
my_dir = CreateDirectory()


class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.clear_field()

        def move_window(event):
            if UiFunctions.return_status(self) == 1:
                UiFunctions.maximize_restore(self)

            if event.buttons() == Qt.LeftButton:
                self.move(self.pos() + event.globalPos() - self.dragPos)
                self.dragPos = event.globalPos()
                event.accept()

        self.ui.TitleBar.mouseMoveEvent = move_window

        UiFunctions.ui_definitions(self)

        self.show()

    def mousePressEvent(self, event):
        self.dragPos = event.globalPos()
        
    def clear_field(self):
        self.setWindowTitle('PASSENGER-II Ground Control Station (MQTT Edition)')
        self.ui.lb_title.setText('PASSENGER-II Ground Control Station (MQTT Edition)')
        self.ui.val_packet.setText('None')
        self.ui.val_lat1.setText('None')
        self.ui.val_lon1.setText('None')
        self.ui.val_timesys.setText('None')
        self.ui.val_temp_ext.setText('None')
        self.ui.val_temp_int.setText('None')
        self.ui.val_humi.setText('None')
        self.ui.val_alt_bar.setText('None')
        self.ui.val_pres_ext.setText('None')
        self.ui.val_pres_int.setText('None')
        self.ui.val_ax.setText('None')
        self.ui.val_ay.setText('None')
        self.ui.val_az.setText('None')
        self.ui.val_gx.setText('None')
        self.ui.val_gy.setText('None')
        self.ui.val_gz.setText('None')
        self.ui.val_batt.setText('None')
        self.ui.val_pm25.setText('None')
        self.ui.val_pm100.setText('None')
        self.ui.val_lat2.setText('None')
        self.ui.val_lon2.setText('None')
        self.ui.val_latpc.setText('None')
        self.ui.val_lonpc.setText('None')
        self.ui.val_alt_pc.setText('None')
        self.ui.val_azimuth.setText('None')
        self.ui.val_elevation.setText('None')
        self.ui.val_timeelapsed.setText('None')
        self.ui.val_timepc.setText('None')
        self.ui.val_grounddist.setText('None')
        self.ui.val_alt_gps1.setText('None')
        self.ui.val_los.setText('None')
        self.ui.val_status.setText('PRELAUNCH')
        self.ui.val_grounddist.setText('None')
        self.ui.val_alt_rtg.setText('None')
        self.ui.val_sq.setText('None')
        self.ui.val_date.setText('BITCOIN 100K')

    def connect_button(self):
        self.ui.btn_scan.clicked.connect(Window.scan_port)
        self.ui.btn_connect.clicked.connect(Window.connect_port)
        self.ui.btn_disconnect.clicked.connect(Window.disconnect_port)
        self.ui.btn_debug.clicked.connect(Window.show_debug)
        self.ui.btn_resettimer.clicked.connect(Window.retime)
        self.ui.btn_graphopen.clicked.connect(Window.show_graph)
        self.ui.btn_graphclear.clicked.connect(Window.cleargraph)


class SplashScreen(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.ui = Ui_SplashScreen()
        self.ui.setupUi(self)

        self.ui.lb_title.setText(' ')

        SplashScreenFunctions.ui_definitions(self)

        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.progress)

        self.timer.start(10)

        self.show()

    def progress(self):
        global GLOBAL_SPLASH_COUNTER

        status_text = str(GLOBAL_SPLASH_COUNTER) + '%'

        if GLOBAL_SPLASH_COUNTER <= 17:
            self.ui.lb_status.setText('Loading Assets...\n' + status_text)

        elif GLOBAL_SPLASH_COUNTER <= 29:
            self.ui.lb_status.setText('Scanning all COM Ports...\n' + status_text)

        elif GLOBAL_SPLASH_COUNTER <= 42:
            self.ui.lb_status.setText('Connecting to WAREDTANAS...\n' + status_text)

        elif GLOBAL_SPLASH_COUNTER <= 54:
            self.ui.lb_status.setText('Verifying WAREDTANS...\n' + status_text)

        elif GLOBAL_SPLASH_COUNTER <= 64:
            self.ui.lb_status.setText('Verifying Devices...\n' + status_text)

        elif GLOBAL_SPLASH_COUNTER <= 75:
            self.ui.lb_status.setText('Preparing Interface...\n' + status_text)

        elif GLOBAL_SPLASH_COUNTER <= 100:
            self.ui.lb_status.setText('Done.\n' + status_text)

        else:
            self.timer.stop()
            Window.start_assets()
            self.close()

        GLOBAL_SPLASH_COUNTER += 1


class GraphWindow(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        self.ui = Ui_GuiGraph()

        self.set_pg()

        self.ui.setupUi(self)

        self.set_field()

        self.setWindowTitle('PASSENGER-II GCS Graph')

        self.ui.lb_title.setText('PASSENGER-II GCS Graph')

        def move_window(event):
            if GraphFunctions.return_status(self) == 1:
                GraphFunctions.maximize_restore(self)

            if event.buttons() == Qt.LeftButton:
                self.move(self.pos() + event.globalPos() - self.dragPos1)
                self.dragPos1 = event.globalPos()
                event.accept()

        self.ui.TitleBar.mouseMoveEvent = move_window

        GraphFunctions.ui_definitions(self)

        self.show()

    def mousePressEvent(self, event):
        self.dragPos1 = event.globalPos()

    def set_pg(self):
        pg.setConfigOption('background', (5, 24, 45))
        pg.setConfigOption('foreground', 'w')

    def set_field(self):
        self.ui.lbgraph_.setText('Altitude')
        self.ui.lbgraph_1.setText('Internal Temp')
        self.ui.lbgraph_2.setText('External Temp')
        self.ui.lbgraph_3.setText('External Pressure')
        self.ui.lbgraph_4.setText('Humidity')
        self.ui.lbgraph_5.setText('AX')
        self.ui.lbgraph_6.setText('AY')
        self.ui.lbgraph_7.setText('AZ')
        self.ui.lbgraph_8.setText('GPS Altitude')
        self.ui.lbgraph_9.setText('GX')
        self.ui.lbgraph_10.setText('GY')
        self.ui.lbgraph_11.setText('GZ')
        self.ui.lbgraph_12.setText('Battery Voltage')
        self.ui.lbgraph_13.setText('PM2.5')
        self.ui.lbgraph_14.setText('PM10.0')
        self.ui.lbgraph_15.setText('None')

class DebugWindow(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        self.ui = Ui_GuiDebug()
        self.ui.setupUi(self)

        self.setWindowTitle('PASSENGER-II GCS Debug')

        self.ui.lb_title.setText('PASSENGER-II GCS Debug')

        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)

        def move_window(event):
            if GraphFunctions.return_status(self) == 1:
                GraphFunctions.maximize_restore(self)

            if event.buttons() == Qt.LeftButton:
                self.move(self.pos() + event.globalPos() - self.dragPos2)
                self.dragPos2 = event.globalPos()
                event.accept()

        self.ui.TitleBar.mouseMoveEvent = move_window

        DebugFunctions.ui_definitions(self)

        self.show()

    def mousePressEvent(self, event):
        self.dragPos2 = event.globalPos()

    def connect_button(self):
        self.ui.btn_led.clicked.connect(Window.send_led)
        self.ui.btn_buzzer.clicked.connect(Window.send_buzzer)
        self.ui.btn_power_down.clicked.connect(Window.send_power)
        self.ui.btn_confirmation.clicked.connect(Window.send_confirm)


class Controller:
    global CLIENT_NAME
    global BROKER_ADDRESS

    def __init__(self):
        self.show_splash()
        self.mydata = ''

        self.cleargraph()

        self.client = mqtt.Client(CLIENT_NAME)
        try:
            self.client.connect(BROKER_ADDRESS)
        except:
            pass

    def show_splash(self):
        self.window_splash = QtWidgets.QMainWindow()
        self.ui_ui = SplashScreen()
        print('SPLASHSCREEN')

    def start_assets(self):
        self.show_debug()
        self.show_graph()
        self.show_ui()
        self.start_clock()
        self.start_serial()
        self.scan_port()

    def show_ui(self):
        self.window_ui = QtWidgets.QMainWindow()
        self.ui_ui = MainWindow()
        self.ui_ui.connect_button()
        print('MAIN WINDOW')

    def show_graph(self):
        self.window_graph = QtWidgets.QWidget()
        self.ui_graph = GraphWindow()
        print('GRAPH WINDOW')

    def show_debug(self):
        self.window_debug = QtWidgets.QWidget()
        self.ui_debug = DebugWindow()
        self.ui_debug.connect_button()
        print('DEBUG WINDOW')

    def start_clock(self):
        self.worker_time = ThreadTimer()
        self.worker_time.pc_time_carrier.connect(self.pc)
        self.worker_time.elapsed_time_carrier.connect(self.elapsed)
        self.worker_time.start()

    def retime(self):
        try:
            self.worker_time.terminate()

        except:
            pass

        self.worker_time.start()

    def start_serial(self):
        self.worker_serial = ThreadSerial()
        self.worker_serial.msg_carrier.connect(self.update_val)

    def scan_port(self):
        self.ui_ui.ui.combobox_comport.clear()
        self.ui_ui.ui.combobox_comport.addItems(com.list_ports()[1])
        print('SCANNED PORTS!')

    def connect_port(self):
        com.connect_port(self.ui_ui.ui.combobox_comport.currentText(), self.ui_ui.ui.combobox_baud.currentText())
        self.ui_ui.ui.lb_title.setText('PASSENGER-II Ground Control Station (MQTT Edition) - ' + com.my_port)
        self.worker_serial.start()

    def disconnect_port(self):
        try:
            self.worker_serial.terminate()
            print('Serial Thread killed!')

        except:
            print('Unable to kill Serial Thread!')
            pass
        com.disconnect_port()

    def pc(self, data):
        self.ui_ui.ui.val_timepc.setText(data)

    def elapsed(self, data):
        self.ui_ui.ui.val_timeelapsed.setText(data)

    def set_text(self, gui, data):
        try:
            gui.setText(data)
        except:
            pass

    def send_led(self):
        com.device.write(b'AXLXAA')

    def send_buzzer(self):
        com.device.write(b'AXBXAA')

    def send_power(self):
        com.device.write(b'AXPXAA')

    def send_confirm(self):
        com.device.write(b'AXCXAA')

    def updategraph(self, graphno, x, y):
        try:
            graphno.plot(x, y)
        except:
            pass

    def cleargraph(self):
        self.list0A = []
        self.list0B = []
        self.list0 = []
        self.list1 = []
        self.list2 = []
        self.list3 = []
        self.list4 = []
        self.list5 = []
        self.list6 = []
        self.list7 = []
        self.list8 = []
        self.list9 = []
        self.list10 = []
        self.list11 = []
        self.list12 = []
        self.list13 = []
        self.list14 = []
        self.list15 = []

    def appendgraph433(self):
        self.list0A.append(self.val_433packet)
        self.list0.append(self.val_433alt_bar)
        self.list1.append(self.val_433temp_int)
        self.list2.append(self.val_433temp_ext)
        self.list3.append(self.val_433pres_ext)
        self.list4.append(self.val_433humi)
        self.list5.append(self.val_433ax)
        self.list6.append(self.val_433ay)
        self.list7.append(self.val_433az)
        self.list8.append(self.val_433alt_gps)
        self.list9.append(self.val_433gx)
        self.list10.append(self.val_433gy)
        self.list11.append(self.val_433gz)

        self.list0A.remove(None)
        self.list0.remove(None)
        self.list1.remove(None)
        self.list2.remove(None)
        self.list3.remove(None)
        self.list4.remove(None)
        self.list5.remove(None)
        self.list6.remove(None)
        self.list7.remove(None)
        self.list8.remove(None)
        self.list9.remove(None)
        self.list10.remove(None)
        self.list11.remove(None)

    def appendgraph868(self):
        self.list0B.append(self.val_868packet)
        self.list12.append(self.val_868batt)
        self.list13.append(self.val_868ka)
        self.list14.append(self.val_868kb)

        self.list0B.remove(None)
        self.list12.remove(None)
        self.list13.remove(None)
        self.list14.remove(None)

    def plot433(self):
        self.updategraph(self.ui_graph.ui.plot_, self.list0A, self.list0)
        self.updategraph(self.ui_graph.ui.plot_1, self.list0A, self.list1)
        self.updategraph(self.ui_graph.ui.plot_2, self.list0A, self.list2)
        self.updategraph(self.ui_graph.ui.plot_3, self.list0A, self.list3)
        self.updategraph(self.ui_graph.ui.plot_4, self.list0A, self.list4)
        self.updategraph(self.ui_graph.ui.plot_5, self.list0A, self.list5)
        self.updategraph(self.ui_graph.ui.plot_6, self.list0A, self.list6)
        self.updategraph(self.ui_graph.ui.plot_7, self.list0A, self.list7)
        self.updategraph(self.ui_graph.ui.plot_8, self.list0A, self.list8)
        self.updategraph(self.ui_graph.ui.plot_9, self.list0A, self.list9)
        self.updategraph(self.ui_graph.ui.plot_10, self.list0A, self.list10)
        self.updategraph(self.ui_graph.ui.plot_11, self.list0A, self.list11)

    def plot868(self):
        self.updategraph(self.ui_graph.ui.plot_12, self.list0B, self.list12)
        self.updategraph(self.ui_graph.ui.plot_13, self.list0B, self.list13)
        self.updategraph(self.ui_graph.ui.plot_14, self.list0B, self.list14)

    def update_val(self, data):

        self.mydata = Select(data)

        if self.mydata.pull(DATA_DICTIONARY['FREQ']['identifier']) == '433' or self.mydata.pull(DATA_DICTIONARY['FREQ']['identifier']) == '868':
            self.val_433packet = self.mydata.pull(DATA_DICTIONARY['COUNT']['identifier'])
            self.val_433lat1 = self.mydata.pull(DATA_DICTIONARY['LAT']['identifier'])
            self.val_433lon1 = self.mydata.pull(DATA_DICTIONARY['LON']['identifier'])
            self.val_433timesys = self.mydata.pull(DATA_DICTIONARY['SYS_TIME']['identifier'])
            self.val_433temp_ext = self.mydata.pull(DATA_DICTIONARY['EXT_TEMP']['identifier'])
            self.val_433temp_int = self.mydata.pull(DATA_DICTIONARY['INT_TEMP']['identifier'])
            self.val_433humi = self.mydata.pull(DATA_DICTIONARY['INT_HUMI']['identifier'])
            self.val_433alt_bar = self.mydata.pull(DATA_DICTIONARY['ALT_BAR']['identifier'])
            self.val_433alt_gps = self.mydata.pull(DATA_DICTIONARY['ALT_GPS']['identifier'])
            self.val_433pres_ext = self.mydata.pull(DATA_DICTIONARY['EXT_PRES']['identifier'])
            self.val_433ax = self.mydata.pull(DATA_DICTIONARY['ACC_X']['identifier'])
            self.val_433ay = self.mydata.pull(DATA_DICTIONARY['ACC_Y']['identifier'])
            self.val_433az = self.mydata.pull(DATA_DICTIONARY['ACC_Z']['identifier'])
            self.val_433gx = self.mydata.pull(DATA_DICTIONARY['GYR_X']['identifier'])
            self.val_433gy = self.mydata.pull(DATA_DICTIONARY['GYR_Y']['identifier'])
            self.val_433gz = self.mydata.pull(DATA_DICTIONARY['GYR_Z']['identifier'])
            self.val_433query = self.mydata.pull(DATA_DICTIONARY['SYS_QUA']['identifier'])
            # try:
            #     self.client.publish('name', 'Tabiji')
            #     self.client.publish('lat', self.val_433lat1)
            #     self.client.publish('lon', self.val_433lon1)
            #     self.client.publish('alt_bar', self.val_433alt_bar)
            #     self.client.publish('alt_gps', self.val_433alt_gps)
            #     self.client.publish('packet', self.val_433packet)
            #     self.client.publish('int_temp', self.val_433temp_int)
            #     self.client.publish('ext_temp', self.val_433temp_ext)
            # except:
            #     pass

        elif self.mydata.pull(DATA_DICTIONARY['FREQ']['identifier']) == '868':
            self.val_868packet = self.mydata.pull(DATA_DICTIONARY['COUNT']['identifier'])
            self.val_868lat2 = self.mydata.pull(DATA_DICTIONARY['LAT']['identifier'])
            self.val_868lon2 = self.mydata.pull(DATA_DICTIONARY['LON']['identifier'])
            self.val_868lat3 = self.mydata.pull(DATA_DICTIONARY['LATS']['identifier'])
            self.val_868lon3 = self.mydata.pull(DATA_DICTIONARY['LONS']['identifier'])
            self.val_868alt_gps = self.mydata.pull(DATA_DICTIONARY['ALT_GPS']['identifier'])
            self.val_868timesys = self.mydata.pull(DATA_DICTIONARY['SYS_TIME']['identifier'])
            self.val_868temp_ext = self.mydata.pull(DATA_DICTIONARY['EXT_TEMP']['identifier'])
            self.val_868ka = self.mydata.pull(DATA_DICTIONARY['KA']['identifier'])
            self.val_868kb = self.mydata.pull(DATA_DICTIONARY['KB']['identifier'])
            self.val_868kc = self.mydata.pull(DATA_DICTIONARY['KC']['identifier'])
            self.val_868query = self.mydata.pull(DATA_DICTIONARY['SYS_QUA']['identifier'])
            self.val_868batt = self.mydata.pull(DATA_DICTIONARY['BATT']['identifier'])

        elif self.mydata.pull(DATA_DICTIONARY['FREQ']['identifier']) == 'DEF':
            self.val_pclat = self.mydata.pull(DATA_DICTIONARY['HOME_LAT']['identifier'])
            self.val_pclon = self.mydata.pull(DATA_DICTIONARY['HOME_LON']['identifier'])
            self.val_pcgx = "0"
            self.val_pcgy = "0"
            self.val_pcgz = "0"
            self.val_pcalt = self.mydata.pull(DATA_DICTIONARY['HOME_ALT']['identifier'])

            # try:
            #     self.client.publish('name', 'Takhli / GCS')
            #     self.client.publish('latdef', self.val_pclat)
            #     self.client.publish('londef', self.val_pclon)
            # except:
            #     pass

        if self.mydata.pull(DATA_DICTIONARY['FREQ']['identifier']) == '433' or self.mydata.pull(DATA_DICTIONARY['FREQ']['identifier']) == '868':
            self.ui_ui.ui.val_packet.setText(self.val_433packet)
            self.ui_ui.ui.val_timesys.setText(convert_time(self.val_433timesys))
            self.ui_ui.ui.val_lat1.setText(self.val_433lat1)
            self.ui_ui.ui.val_lon1.setText(self.val_433lon1)
            self.ui_ui.ui.val_temp_ext.setText(self.val_433temp_ext)
            # self.updategraph(self.ui_graph.ui.plot_1, self.val_433packet, self.val_868packet)
            self.ui_ui.ui.val_temp_int.setText(self.val_433temp_int)
            self.ui_ui.ui.val_humi.setText(self.val_433humi)
            self.ui_ui.ui.val_alt_bar.setText(self.val_433alt_bar)
            self.ui_ui.ui.val_pres_ext.setText(self.val_433pres_ext)
            self.ui_ui.ui.val_pres_int.setText('None')
            self.ui_ui.ui.val_ax.setText(self.val_433ax)
            self.ui_ui.ui.val_ay.setText(self.val_433ay)
            self.ui_ui.ui.val_az.setText(self.val_433az)
            self.ui_ui.ui.val_gx.setText(self.val_433gx)
            self.ui_ui.ui.val_gy.setText(self.val_433gy)
            self.ui_ui.ui.val_gz.setText(self.val_433gz)
            if self.val_433query == 'F':
                self.query_status = 'Normal'
                self.ui_debug.ui.lb_stat_query.setText('NORMAL OPERATION')
            elif self.val_433query == 'P':
                self.query_status = 'Revert'
                self.ui_debug.ui.lb_stat_query.setText('BACK TO NORMAL')
            elif self.val_433query == 'D':
                self.query_status = 'Power Down'
                self.ui_debug.ui.lb_stat_query.setText('POWER DOWN!')
            elif self.val_433query == 'R':
                self.query_status = 'Request'
                self.ui_debug.ui.lb_stat_query.setText('REQUEST SHUTDOWN')
            self.ui_ui.ui.val_sq.setText(self.query_status)

            # self.appendgraph433()
            # self.plot433()

        elif self.mydata.pull(DATA_DICTIONARY['FREQ']['identifier']) == '868':
            self.ui_ui.ui.val_lat2.setText(self.val_868lat2)
            self.ui_ui.ui.val_lon2.setText(self.val_868lon2)
            self.ui_ui.ui.val_batt.setText(self.val_868batt)

            # self.appendgraph868()
            # self.plot868()

        # try:
        #     self.coord = Coord("15.251", "100.336906", self.val_433lat1, self.val_433lon1,
        #                        "200", self.val_433alt_gps, self.val_pcgx, self.val_pcgy, self.val_pcgz)
        #
        # except:
        #     try:
        #         self.coord = Coord(self.val_pclat, self.val_pclon, self.val_868lat2, self.val_868lon2,
        #                            self.val_pcalt, self.val_433alt_gps, self.val_pcgx, self.val_pcgy, self.val_pcgz)
        #
        #     except:
        #         try:
        #             self.coord = Coord(self.val_pclat, self.val_pclon, self.val_868lat3, self.val_868lon3,
        #                                self.val_pcalt, self.val_433alt_gps, self.val_pcgx, self.val_pcgy, self.val_pcgz)
        #
        #         except:
        #             pass
        #
        #         else:
        #             self.ui_ui.ui.val_grounddist.setText(str(self.coord.dist()))
        #             self.ui_ui.ui.val_los.setText(str(self.coord.los()))
        #             self.ui_ui.ui.val_alt_gps1.setText(str(self.coord.alt))
        #
        #     else:
        #         self.ui_ui.ui.val_grounddist.setText(str(self.coord.dist()))
        #         self.ui_ui.ui.val_los.setText(str(self.coord.los()))
        #         self.ui_ui.ui.val_alt_gps1.setText(str(self.coord.alt))
        #
        # else:
        #     self.ui_ui.ui.val_grounddist.setText(str(self.coord.dist()))
        #     self.ui_ui.ui.val_los.setText(str(self.coord.los()))
        #     self.ui_ui.ui.val_alt_gps1.setText(str(self.coord.alt))


class ThreadSerial(QThread):
    msg_carrier = QtCore.pyqtSignal(object)

    def __init__(self, parent=None):
        self._isRunning = True
        super(ThreadSerial, self).__init__(parent)

    def __del__(self):
        self.wait()

    def run(self):
        print('THREAD SERIAL STARTED!')
        try:
            while True:
                s = ReadDevice(com.device, ['433', '868', 'DEF']).readall()
                argz = Select(s)
                if argz.pull(DATA_DICTIONARY['FREQ']['identifier']) != '' and argz.pull(
                        DATA_DICTIONARY['FREQ']['identifier']) != 'None':
                    print('Freq is ' + argz.pull(DATA_DICTIONARY['FREQ']['identifier']))
                    print('Data is ' + ConvertComma(s).show())
                    self.msg_carrier.emit(s)

                ConvertComma(s).write_csv(my_dir.path_csv)

                GoogleEarth(s).generate_file_live(my_dir.path_gearthlive)
                GoogleEarth(s).generate_file_coord(my_dir.path_livepath, my_dir.path_gearthcoord,
                                                   my_dir.path_coord)

        except:
            pass

    def stop(self):
        self._isRunning = False
        self.terminate()


class ThreadTimer(QThread):
    pc_time_carrier = QtCore.pyqtSignal(object)
    elapsed_time_carrier = QtCore.pyqtSignal(object)

    def __init__(self, parent=None):
        self._isRunning = True
        super(ThreadTimer, self).__init__(parent)

    def __del__(self):
        self.wait()

    def run(self):
        print('THREAD PC CLOCK STARTED!')
        clock = GetTime()
        while True:
            self.pc_time_carrier.emit(clock.time_pc())
            self.elapsed_time_carrier.emit(clock.time_elapsed())
            if Window.ui_ui.ui.val_status.text() != '':
                self.temp_text = Window.ui_ui.ui.val_status.text()

            if clock.stime.second % 2 == 0:
                Window.ui_ui.ui.val_status.setText('')

            else:
                Window.ui_ui.ui.val_status.setText(self.temp_text)

    def stop(self):
        self._isRunning = False
        self.terminate()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    Window = Controller()
    sys.exit(app.exec_())
