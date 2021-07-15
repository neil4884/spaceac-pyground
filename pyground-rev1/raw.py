import serial
import os


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

print(comlist())
print('PROMPT# Enter COM port: ')
comport = input()
# comport = 9
comname = 'COM' + str(comport)

teensy = serial.Serial(comname, 9600, timeout=60)
print('PROMPT# ' + teensy.name + ' is selected.')
print(type(teensy))

teensy.close()
teensy.open()

pkg = ''
carrier = ''
coords = ''
datano = 1
gearthno = 1

keyStart = '$PSG-I$'
keyStop = '$PSG$'
keyFreq = 'F' + str(input('Frequency: '))
csvName = ''

dataType = {
    'FREQUENCY': 'F',
    'COUNT': 'C',
    'LATITUDE': 'A',
    'LONGITUDE': 'B',
    'BAR_ALT': 'D',
    'GPS_ALT': 'E',
    'INT_TEMP': 'S',
    'EXT_TEMP': 'K',
    'GYR_X': 'R',
    'GYR_Y': 'U',
    'GYR_Z': 'Y',
    'ACC_X': 'X',
    'ACC_Y': 'N',
    'ACC_Z': 'Z',
    'MPXV': 'V',
    'SYS_TIME': 'T',
    'PM10_1': 'L',
    'PM10_2': 'M',
    'PM10_3': 'Q',
    'BATT_VOL': 'O'
}

dataUnit = {
    'FREQUENCY': 'MHz',
    'COUNT': '',
    'LATITUDE': 'DEG',
    'LONGITUDE': 'DEG',
    'BAR_ALT': 'm',
    'GPS_ALT': 'm',
    'INT_TEMP': 'DEG C',
    'EXT_TEMP': 'DEG C',
    'GYR_X': 'DEG',
    'GYR_Y': 'DEG',
    'GYR_Z': 'DEG',
    'ACC_X': 'm/s^2',
    'ACC_Y': 'm/s^2',
    'ACC_Z': 'm/s^2',
    'MPXV': 'm/s',
    'SYS_TIME': 'hms',
    'PM10_1': 'ug/cm^3',
    'PM10_2': 'ug/cm^3',
    'PM10_3': 'ug/cm^3',
    'BATT_VOL': 'mV'
}


def readteensy():
    s = teensy.read().decode('utf-8')
    s = s.replace('\r', '')
    s = s.replace('\n', '')
    return s


def isfloat(s):
    try:
        float(s)
        return 1
    except ValueError:
        return 0


def clearstring():
    return ''


def isnull(s):
    if (isfloat(s)):
        if (float(s)==-2222):
            return ''
        else:
            return s
    else:
        return s


def gearthlive(name):
    file = open('gearthlive.kml','w')
    file.writelines('<?xml version="1.0" encoding="UTF-8"?>'
                    '<kml xmlns="http://www.opengis.net/kml/2.2" '
                    'xmlns:gx="http://www.google.com/kml/ext/2.2">'
                    '<NetworkLink><Link><href>'+'\n')
    file.writelines(name)
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

class Select:
    def __init__(self, text):
        self.pkg = text
        self.len = len(self.pkg)

    def pull(self, id):
        try:
            self.id = id
            self.idPos = self.pkg.find(self.id)
            self.endPos = self.pkg.find('$', self.idPos+1, self.len)
            if self.endPos <= 0:
                return '-2222'
            if self.idPos >= 0 and self.endPos >= 0 and self.len >= 0:
                self.p = self.pkg[self.idPos+1:self.endPos]
                if isfloat(self.p):
                    return str(self.p)
                else:
                    return '-2222'
            else:
                return '-2222'
        except:
            return '-2222'
        finally:
            return '-2222'

    def timeconvert(self, time):
        if len(time) == 6 and isfloat(time) and time.find('.') < 0:
            ptime = time[0:2] + ':' + time[2:4] + ':' + time[4:6]
            return ptime
        else:
            return time


if __name__ == '__main__':
    while True:
        fname = 'PSGI' + keyFreq + '-' + str(datano) + '.CSV'
        valid = os.path.isfile(fname)
        gname = 'gearthcoord' + str(datano) + '.kml'
        if valid:
            filename = fname
            gfilename = gname
            datano += 1
            continue
        else:
            filename = fname
            gfilename = gname
            break

    gearthlive("gearthcoord.kml")

    while True:
        file = open(filename, 'a')

        pkg += readteensy()
        pkgStart = pkg.find(keyStart)
        pkgStop = pkg.find(keyStop)

        if (pkgStart >= 0):
            pkg = pkg.replace('$PSG-I', '')
            if (pkgStop):
                pkg = pkg.replace('$PSG$', '')
                if(pkg[0] != 'F'):
                    pkg = pkg[pkg.find(keyFreq):]
                if(pkg.find(keyFreq) >= 0):
                    print('PROMPT# ' + pkg)
                    argz = Select(pkg)
                    for key in dataType:
                        z = argz.pull(dataType[key])
                        if (float(z) != -2222):
                            print(key + '\t\t' + argz.timeconvert(argz.pull(dataType[key])) + '\t' + dataUnit[key])
                            pass
                        carrier += isnull(argz.timeconvert(argz.pull(dataType[key])))
                        carrier += ','
                    file.writelines(carrier + '\n')
                    file.close()
                    coords = coords + \
                             argz.pull(dataType['LONGITUDE']) + ',' + argz.pull(dataType['LATITUDE']) + ',' + \
                             argz.pull(dataType['GPS_ALT']) + '\n'
                    gearthcoord(coords, gfilename)
                    gearthcoord(coords, "gearthcoord.kml")
                    carrier = clearstring()
                    pkg = clearstring()

