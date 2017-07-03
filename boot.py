import network
import json


def do_connect():
    wlan = network.WLAN(network.STA_IF)
    if not wlan.isconnected():
        with open('config.json', 'r') as f:
            config = json.load(f)

        print('connecting to network...')
        wlan.active(True)
        wlan.connect(config['network']['ssid'], config['network']['pass'])
        while not wlan.isconnected():
            pass
    print('network config:', wlan.ifconfig())


do_connect()
