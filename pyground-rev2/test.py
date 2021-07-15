import paho.mqtt.client as mqtt

CLIENT_NAME = 'P1'

BROKER_ADDRESS = 'ip.realneil4884.com'


class Mqtt:
    global CLIENT_NAME
    global BROKER_ADDRESS

    def __init__(self):
        self.client = mqtt.Client(CLIENT_NAME)
        self.client.connect(BROKER_ADDRESS)

    def send(self):
        self.client.publish('name', 'Tabiji')
        self.client.publish('lat', '13.49')
        self.client.publish('lon', '100.39')
        self.client.publish('alt_gps', '1123')
        self.client.publish('alt_bar', '1222')
        self.client.publish('int_temp', '40')
        self.client.publish('ext_temp', '-76')


if __name__ == '__main__':
    myqt = Mqtt()
    myqt.send()
