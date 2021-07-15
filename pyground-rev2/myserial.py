import serial
import serial.tools.list_ports as serial_port
import os

from psg_dictionary import *


DATA_DICTIONARY = PSG2  # CHANGE TO PSG2
OLD_DICTIONARY = PSG1

GLOBAL_PATH = os.path.abspath(os.path.dirname(__file__))


# ComPort() ONLY ONCE!
class ComPort:
    def __init__(self):
        self.port_name = []
        self.port_full_name = []
        self.port_list = self.list_ports
        self.full_name = ''
        self.my_port = ''

    def list_ports(self):
        self.port_list = []
        self.port_name = []
        self.port_full_name = []

        self.port_list = serial_port.comports()

        for self.port in self.port_list:
            self.port_name.append(self.port.device)
            self.full_name = str(self.port.device) + \
                ' (' + str(self.port.manufacturer) + \
                ' ' + str(self.port.product) + ')'
            self.port_full_name.append(self.full_name)

        return self.port_name, self.port_full_name

    def connect_port(self, full_name, baud):
        self.my_port = ''
        temp_port, temp_name = self.list_ports()
        for i in range(len(temp_port)):
            if full_name == temp_name[i]:
                self.my_port = temp_port[i]
                break

            else:
                self.my_port = ''

        try:
            self.device = serial.Serial(self.my_port, baudrate=int(baud), timeout=60)

        except:
            print('CANNOT CONNECT TO PORT OR THE PORT IS ALREADY CONNECTED!')
            pass

    def disconnect_port(self):
        try:
            if self.device.isOpen():
                self.device.close()
                print('PORT CLOSED!')
            else:
                print('ALREADY DISCONNECTED!')

        except:
            print('CANNOT DISCONNECT!')
            pass


# Select(input_text) EVERY TIME TO RUN!
class Select:
    def __init__(self, input_text):
        self.data = input_text
        self.len = len(self.data)
        self.selected_attr = ''
        self.id_pos = 0
        self.end_pos = 0

    def pull(self, identifier):
        self.id_pos = self.data.find(identifier)
        self.end_pos = self.data.find('$', self.id_pos + len(identifier), self.len)

        if self.id_pos >= 0 and self.end_pos >= 0 and self.len >= 0:
            self.selected_attr = self.data[self.id_pos + len(identifier): self.end_pos]
            if is_float(self.selected_attr):
                return self.selected_attr

            elif (identifier == 'ST' or identifier == 'T') and \
                    (is_timestamp(self.selected_attr) or is_time(self.selected_attr)):
                time_offset = 0
                self.selected_attr = convert_time(self.selected_attr)
                return str("%02d" % (int(self.selected_attr[0:2]) + time_offset)) + self.selected_attr[2:]

            elif identifier == 'SQ':
                return self.selected_attr

            elif identifier == "CH":
                return self.selected_attr

            else:
                return 'None'

        else:
            return 'None'


# ReadDevice(device, frequency) EVERY TIME TO READ!
class ReadDevice:
    def __init__(self, device, frequency):
        global DATA_DICTIONARY
        self.dictionary = DATA_DICTIONARY

        self.device = device
        self.frequency = frequency
        self.pkg = ''

        self.key_start = '$PSG2$'
        self.key_stop = '$2GSP$'

        self.avail_freq = ['433', '868', '915', '001', '002', '003', 'DEF']

    def readall(self):
        s = ''
        while True:
            s += read(self.device)

            s_start = s.find(self.key_start)
            s_stop = s.find(self.key_stop)

            if s_start >= 0 and s_stop > 0:
                s = s.replace(self.key_stop, '$')

                if not s[0:2] == self.dictionary['FREQ']['identifier']:
                    s = s[s.find(self.dictionary['FREQ']['identifier']):]

                argz = Select(s)

                if argz.pull(self.dictionary['FREQ']['identifier']) in self.avail_freq and \
                        argz.pull(self.dictionary['FREQ']['identifier']) in self.frequency:
                    for key in self.dictionary:
                        if not argz.pull(self.dictionary[key]['identifier']) == 'None':
                            # print(
                            #     self.dictionary[key]['name'] + '\t\t' +
                            #     argz.pull(self.dictionary[key]['identifier']) + '\t\t' +
                            #     self.dictionary[key]['unit'])

                            pass

                    return s

                else:
                    return ''


# ConvertComma(data) EVERY TIME TO CONVERT!
class ConvertComma:
    def __init__(self, s):
        global DATA_DICTIONARY
        self.dictionary = DATA_DICTIONARY

        self.pkg = Select(s)
        self.output = ''
        self.blank = ''

        self.convert()

    def convert(self):
        if not (self.pkg == 'None' or self.pkg == ''):
            for key in self.dictionary:
                if not self.pkg.pull(self.dictionary[key]['identifier']) == 'None':
                    self.output += self.pkg.pull(self.dictionary[key]['identifier'])
                self.output += ','
                self.blank += ','

            if self.output == self.blank:
                self.output = ''

            return self.output
        else:
            return ''

    def write_csv(self, file_dir):
        if not self.output == '':
            with open(file_dir, 'a') as file:
                file.writelines(strip(self.output) + '\n')
            return self.output
        else:
            return 'FAILED!'

    def show(self):
        return self.output


# GoogleEarth(lat, lon, alt) EVERY TIME TO GENERATE!
class GoogleEarth:
    def __init__(self, s):
        global DATA_DICTIONARY
        self.dictionary = DATA_DICTIONARY

        argz = Select(s)
        self.lat = argz.pull(self.dictionary['LAT']['identifier'])
        self.lon = argz.pull(self.dictionary['LON']['identifier'])
        self.alt = argz.pull(self.dictionary['ALT_GPS']['identifier'])

        self.coord = self.lon + ',' + self.lat + ',' + self.alt + '\n'

    def generate_file_live(self, full_path):
        valid = os.path.exists(full_path)
        if not (valid or self.coord.find('None') >= 0):
            with open(full_path, 'w') as file:
                file.writelines('<?xml version="1.0" encoding="UTF-8"?>'
                                '<kml xmlns="http://www.opengis.net/kml/2.2" '
                                'xmlns:gx="http://www.google.com/kml/ext/2.2">'
                                '<NetworkLink><Link><href>' + '\n')
                file.writelines('gearthcoord.kml')
                file.writelines('\n' + '</href><refreshMode>onInterval</refreshMode>'
                                '<refreshInterval>0.1</refreshInterval></Link>'
                                '<refreshInterval>0.1</refreshInterval><refreshMode>onInterval</refreshMode>'
                                '</NetworkLink></kml>')

    def generate_file_coord(self, livepath, full_path, save_path):
        if not self.coord.find('None') >= 0:
            str_open = [(
                '<kml xmlns="http://www.opengis.net/kml/2.2" '
                'xmlns:gx="http://www.google.com/kml/ext/2.2">'
                '<Folder><name>Log</name><Placemark><name>PASSENGER-I SIM PATH'
                '</name><Style><LineStyle><color>ff00ffff</color>'
                '<colorMode>normal</colorMode><width>3</width>'
                '</LineStyle><PolyStyle><color>99000000</color>'
                '<fill>1</fill></PolyStyle></Style><LineString><extrude>1</extrude>'
                '<altitudeMode>absolute</altitudeMode><coordinates>' + '\n')]
            str_close = [('\n' + '</coordinates></LineString></Placemark></Folder></kml>')]

            with open(livepath, 'a') as file:
                file.writelines(self.coord)

            with open(livepath, 'r') as file, open(full_path, 'w') as file2, open(save_path, 'w') as file3:
                all_coords = file.readlines()
                str_open.extend(all_coords)
                str_open.extend(str_close)

                file2.writelines(str_open)
                file3.writelines(str_open)


# CreateDirectory() ONLY ONCE!
class CreateDirectory:
    def __init__(self):
        global GLOBAL_PATH
        self.global_path = GLOBAL_PATH

        self.name_csv = 'PSG2-DATA'
        self.name_coord = 'gearthcoord'

        self.name_livepath = 'livepath.dat'
        self.name_gearthcoord = 'gearthcoord.kml'
        self.name_gearthlive = 'gearthlive.kml'

        self.path_csv = ''
        self.path_coord = ''
        self.path_livepath = self.make_abs_path(self.name_livepath)
        self.path_gearthcoord = self.make_abs_path(self.name_gearthcoord)
        self.path_gearthlive = self.make_abs_path(self.name_gearthlive)

        self.renew_path()

        self.check_path()

        pass

    def make_abs_path(self, file_name):
        folder = 'DATA/' + file_name
        path = os.path.join(self.global_path, folder)
        return str(path)

    def check_path(self, datano=1):
        self.check_foler()

        while True:
            self.path_csv = self.make_abs_path(self.name_csv) + str(datano) + '.CSV'
            self.path_coord = self.make_abs_path(self.name_coord) + str(datano) + '.kml'
            valid = os.path.isfile(self.path_csv)
            if not valid:
                break
            else:
                datano += 1

    @staticmethod
    def check_foler():
        if not os.path.exists('DATA'):
            os.makedirs('DATA')

    def renew_path(self):
        if os.path.isfile(self.path_livepath):
            os.remove(self.path_livepath)

        if os.path.isfile(self.path_gearthcoord):
            os.remove(self.path_gearthcoord)


def is_float(s):
    try:
        float(s)
        return True
    except ValueError:
        return False


def is_time(s):
    if len(s) == 8 and s.find(':'):
        return True
    else:
        return False


def is_timestamp(s):
    if len(s) == 6 and is_float(s) and s.find('.') < 0:
        return True
    else:
        return False


def is_data(s):
    if not s.find('None'):
        return True
    else:
        return False


def convert_time(s):
    if len(s) == 6 and is_float(s) and s.find('.') < 0:
        colon_time = s[0:2] + ':' + s[2:4] + ':' + s[4:6]
        return colon_time
    else:
        return s


def read(device):
    s = device.read().decode('utf-8')
    s = strip(s)
    return s


def strip(s):
    return s.replace('\r', '').replace('\n', '').replace(' ', '')


def update_plot(widget, x, y):
    widget.plot(x, y, pen='y', symbol='o', symbolPen='y', symbolBrush='w', )


def clear_plot(widget):
    widget.clear()


if __name__ == '__main__':
    comm = ComPort()
    comm.connect_port('COM254 (Electronic Team None)', 9600)
    comm.disconnect_port()
    comm.disconnect_port()
