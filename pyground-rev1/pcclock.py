from datetime import datetime
import time

starttime = time.time()


class gettime:

    def settime(self):
        global starttime
        starttime = time.time()

    def updatetime(self):
        stime = datetime.now().time()
        if stime.second % 2 == 0:
            timestp = str('%02d' % stime.hour) + ' ' + str('%02d' % stime.minute) + \
                      ' ' + str('%02d' % stime.second) + '.' + str(stime.microsecond)[0:2]
        else:
            timestp = str('%02d' % stime.hour) + ':' + str('%02d' % stime.minute) + \
                      ':' + str('%02d' % stime.second) + '.' + str(stime.microsecond)[0:2]
        time.sleep(0.01)
        return timestp

    def timeelapsed(self):
        delta = time.time() - starttime
        second = delta % 60
        microsecond = str(datetime.now().time().microsecond)[0:2]
        minute = delta / 60
        minute = minute % 60
        hour = minute / 60

        if int(second) % 2 == 0:
            timestp = str('%02d' % hour) + ' ' + str('%02d' % minute) + \
                      ' ' + str('%02d' % second) + '.' + microsecond
        else:
            timestp = str('%02d' % hour) + ':' + str('%02d' % minute) + \
                      ':' + str('%02d' % second) + '.' + microsecond
        time.sleep(0.01)

        return timestp