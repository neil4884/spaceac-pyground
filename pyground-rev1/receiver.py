import serial
import os

dataType = {
    1: {'name': 'FREQUENCY', 'identifier': 'F', 'unit': 'MHz'},
    2: {'name': 'COUNT', 'identifier': 'C', 'unit': 'PACKETS'},
    3: {'name': 'LATITUDE', 'identifier': 'A', 'unit': 'DEG'},
    4: {'name': 'LONGITUDE', 'identifier': 'B', 'unit': 'DEG'},
    5: {'name': 'BAR_ALT', 'identifier': 'D', 'unit': 'm'},
    6: {'name': 'GPS_ALT', 'identifier': 'E', 'unit': 'm'},
    7: {'name': 'INT_TEMP', 'identifier': 'S', 'unit': 'DEG C'},
    8: {'name': 'EXT_TEMP', 'identifier': 'K', 'unit': 'DEG C'},
    9: {'name': 'GYR_X', 'identifier': 'R', 'unit': 'DEG'},
    10: {'name': 'GYR_Y', 'identifier': 'U', 'unit': 'DEG'},
    11: {'name': 'GYR_Z', 'identifier': 'Y', 'unit': 'DEG'},
    12: {'name': 'ACC_X', 'identifier': 'X', 'unit': 'm/s^2'},
    13: {'name': 'ACC_Y', 'identifier': 'N', 'unit': 'm/s^2'},
    14: {'name': 'ACC_Z', 'identifier': 'Z', 'unit': 'm/s^2'},
    15: {'name': 'EXT_PRES', 'identifier': 'V', 'unit': 'hPa'},
    16: {'name': 'SYS_TIME', 'identifier': 'T', 'unit': 'hms'},
    17: {'name': 'PM10_1', 'identifier': 'L', 'unit': 'ug/cm^3'},
    18: {'name': 'PM10_2', 'identifier': 'M', 'unit': 'ug/cm^3'},
    19: {'name': 'PM10_3', 'identifier': 'Q', 'unit': 'ug/cm^3'},
    20: {'name': 'BATT_VOL', 'identifier': 'O', 'unit': 'mV'},
    21: {'name': 'glat', 'identifier': 'a', 'unit': 'DEG'},
    22: {'name': 'glon', 'identifier': 'b', 'unit': 'DEG'},
    23: {'name': 'gx', 'identifier': 'x', 'unit': 'DEG'},
    24: {'name': 'gy', 'identifier': 'y', 'unit': 'DEG'},
    25: {'name': 'gz', 'identifier': 'z', 'unit': 'DEG'},
    26: {'name': 'a1', 'identifier': 'r', 'unit': 'm'}
}

mypath = os.path.abspath(os.path.dirname(__file__))


def comlist():
    comall = []
    for i in range(256):
        comtest = 'COM'+str(i)
        try:
            serial.Serial(comtest)
        except:
            # print("NO " + comtest)
            pass
        else:
            comall.append(comtest)
    return comall


def connect(comname):
    teensy = serial.Serial(comname, 9600, timeout=60)
    return teensy


def isconnect(device):
    try:
        device.close()
    except:
        return 0
    else:
        return 1


def read(hw):
    s = hw.read().decode('utf-8')
    s = s.replace('\r', '')
    s = s.replace('\n', '')
    s = s.replace(' ', '')
    return s


def isfloat(s):
    try:
        float(s)
        return 1
    except ValueError:
        return 0


def istime(s):
    if s.find(':'):
        return s


def clearstring():
    return ''


def isnull(s):
    if (isfloat(s)):
        if (float(s)==-2222):
            return ''
        else:
            return s
    elif s.find(':'):
        return s
    else:
        return s


def gearthlive():
    gearthlivepath = joinpath('gearthlive.kml')
    file = open(gearthlivepath, 'w')
    file.writelines('<?xml version="1.0" encoding="UTF-8"?>'
                    '<kml xmlns="http://www.opengis.net/kml/2.2" '
                    'xmlns:gx="http://www.google.com/kml/ext/2.2">'
                    '<NetworkLink><Link><href>'+'\n')
    file.writelines('gearthcoord.kml')
    file.writelines('</href><refreshMode>onInterval</refreshMode>'
                    '<refreshInterval>0.1</refreshInterval></Link>'
                    '<refreshInterval>0.1</refreshInterval><refreshMode>onInterval</refreshMode>'
                    '</NetworkLink></kml>')


def gearthcoord(coords,name):
    file = open(name,'w')
    file.writelines('<kml xmlns="http://www.opengis.net/kml/2.2" '
                    'xmlns:gx="http://www.google.com/kml/ext/2.2">'
                    '<Folder><name>Log</name><Placemark><name>PASSENGER-I PATH</name>'
                    '<styleUrl>#yellowLineGreenPoly</styleUrl><Style>'
                    '<LineStyle><color>ff00ffff</color><colorMode>normal</colorMode><width>4</width></LineStyle>'
                    '</Style><LineString><extrude>1</extrude><altitudeMode>absolute</altitudeMode><coordinates>'+'\n')
    file.writelines(coords)
    file.writelines('\n' + '</coordinates></LineString></Placemark></Folder></kml>')
    file.close()


def timeconvert(time):
    if len(time) == 6 and isfloat(time) and time.find('.') < 0:
        colontime = time[0:2] + ':' + time[2:4] + ':' + time[4:6]
        return colontime
    else:
        return time

def istime(s):
    if s.find(":") and len(s) == 8:
        return True
    return False
class Select:
    def __init__(self, text):
        self.pkg = text
        self.len = len(self.pkg)

    def pull(self, id):
        self.id = id
        self.idPos = self.pkg.find(self.id)
        self.endPos = self.pkg.find('$', self.idPos+1, self.len)
        if self.idPos >= 0 and self.endPos >= 0 and self.len >= 0:
            self.p = self.pkg[self.idPos+1:self.endPos]
            if isfloat(self.p):
                return str(self.p)
            elif istime(self.p):
                colontime = str("%02d" % (int(self.p[0:2])+7)) + self.p[2:]
                return colontime
            else:
                return '-2222'
        else:
            return '-2222'

def joinpath(name):
    folder = 'DATA/' + name
    path = os.path.join(mypath, folder)
    return str(path)


def namecheck(freq, i, datano = 1):
    livepath = joinpath('livepath.dat')
    gearthcoordpath = joinpath('gearthcoord')
    csvpath = joinpath('PSG')
    if i == 0 and os.path.isfile(livepath):
        os.remove(livepath)
    while True:
        fname = csvpath + str(freq) + '-' + str(datano) + '.CSV'
        valid = os.path.isfile(fname)
        gname = gearthcoordpath + str(datano) + '.kml'
        if valid:
            datano += 1
            continue
        else:
            if i != 0:
                datano -= 1
                fname = csvpath + str(freq) + '-' + str(datano) + '.CSV'
                gname = gearthcoordpath + str(datano) + '.kml'
            ls = [fname, gname]
            return ls


def readall(device, freq, i):
    pkg = ''
    carrier = ''
    coords = ''
    keyStart = '$PSG-I$'
    keyStop = '$PSG$'
    keyFreq = 'F' + str(freq)

    filename = namecheck(freq, i)[0]
    gfilename = namecheck(freq, i)[1]

    file = open(filename, 'a')

    livepath = joinpath('livepath.dat')
    gearthcoordpath = joinpath('gearthcoord.kml')

    try:
        while True:
            pkg += read(device)
            pkgStart = pkg.find(keyStart)
            pkgStop = pkg.find(keyStop)

            if pkgStart >= 0:
                pkg = pkg.replace('$PSG-I', '')
                if pkgStop:
                    pkg = pkg.replace('$PSG$', '')
                    if pkg[0] != 'F':
                        pkg = pkg[pkg.find(keyFreq):]
                    # if pkg.find(keyFreq) >= 0:
                    if Select(pkg).pull('F') == '433' or Select(pkg).pull('F') == '868' \
                            or Select(pkg).pull('F') == '915' or Select(pkg).pull('F') == '001':

                        if Select(pkg).pull('F') != '001':
                            print('PROMPT# ' + pkg)
                        argz = Select(pkg)
                        for key in dataType:
                            z = argz.pull(dataType[key]['identifier'])
                            if float(z) != -2222:
                                # print(dataType[key]['name'] + '\t\t' + timeconvert(argz.pull(dataType[key]['identifier'])) + '\t' + dataType[key]['unit'])
                                if dataType[key]['identifier'] == 'O':
                                    z = str(float(z)*6)
                                pass
                            carrier += isnull(timeconvert(z))
                            carrier += ','
                        file.writelines(carrier + '\n')
                        file.close()
                        if argz.pull('F') == '433' and float(argz.pull('A')) >= 0:
                            coords = coords + \
                                     argz.pull(dataType[4]['identifier']) + ',' + argz.pull(dataType[3]['identifier']) + ',' + \
                                     argz.pull(dataType[6]['identifier']) + '\n'

                            file2 = open(livepath, 'a')
                            file2.writelines(coords)
                            file2.close()

                            file2 = open(livepath, 'r')
                            allcoords = file2.readlines()

                            gearthcoord(allcoords, gfilename)
                            gearthcoord(allcoords, gearthcoordpath)
                        return pkg
                    else:
                        print('WRONG FREQUENCY!')
                        return '0'
    finally:
        # print('ERR2')
        return pkg

# EXAMPLE
# if __name__ == '__main__':
#     print(readall(connect(comlist()[0]),433))