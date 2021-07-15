from myserial import *
from mygis import *
from mypcclock import *
import paho.mqtt.client as mqtt

CLIENT_NAME = 'P1'

BROKER_ADDRESS = 'ip.realneil4884.com'

if __name__ == '__main__':
    com = ComPort()
    print(com.list_ports())
    com.connect_port('COM6 (Microsoft None)', 9600)

    my_path = CreateDirectory()

    while True:
        try:
            s = ReadDevice(com.device, ['433', '868']).readall()
            argz = Select(s)
            if argz.pull(DATA_DICTIONARY['FREQ']['identifier']) != '' and argz.pull(DATA_DICTIONARY['FREQ']['identifier']) != 'None':
                print('Freq is ' + argz.pull(DATA_DICTIONARY['FREQ']['identifier']))
                print('Data is ' + ConvertComma(s).show())

            ConvertComma(s).write_csv(my_path.path_csv)

            GoogleEarth(s).generate_file_live(my_path.path_gearthlive)
            GoogleEarth(s).generate_file_coord(my_path.path_livepath, my_path.path_gearthcoord, my_path.path_coord)

                client.publish('ext_temp', self.val_433temp_ext)
                client.publish('int_temp', self.val_433temp_int)

        except:
            pass

