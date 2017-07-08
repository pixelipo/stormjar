import network
import json
import socket


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


def http_get(url, port=80):
    proto, _, host, path = url.split('/', 3)
    if proto == "https:":
        import ussl
        port = 443
    addr = socket.getaddrinfo(host, port)[0][-1]
    s = socket.socket()
    s.connect(addr)
    if proto == "https:":
        s = ussl.wrap_socket(s)
    s.send(bytes('GET /%s HTTP/1.0\r\nHost: %s\r\n\r\n' % (path, host), 'utf8'))
    while True:
        data = s.recv(100)
        if data:
            print(str(data, 'utf8'), end='')
        else:
            break
    s.close()


do_connect()
