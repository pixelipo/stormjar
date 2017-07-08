import json
from machine import Pin
from neopixel import NeoPixel
import time


with open('config.json', 'r') as f:
    CONF = json.load(f)

# Pin setup
PIN_LED = Pin(CONF['pin']['led'], Pin.OUT)
PIN_PUMP = Pin(CONF['pin']['pump'], Pin.OUT)
PIN_FOG = Pin(CONF['pin']['fog'], Pin.OUT)
PIN_SWITCH = Pin(CONF['pin']['switch'], Pin.IN)

# Neopixel setup
PIXEL = NeoPixel(PIN_LED, CONF['led']['count'])

# Set max brighness as percentage
PIXEL_MAX = CONF['led']['brightness']

# Set auto-off time and sleep duration
# default: 60*15 and 60*45
AUTO_OFF = 15 * 60 * 1000  # miliseconds
# AUTO_SLEEP = time.sleep(2700)  # seconds


# Convert DarkSky weather types to supported weather types
def set_type(argument):
    switcher = {
        'clear': clear(),
        'clear-day': clear(),
        'clear-night': clear(),
        'wind': clear(),
        'rain': rain(),
        'sleet': rain(),
        'snow': snow(),
        'fog': cloud(),
        'cloudy': cloud(),
        'partly-cloudy-day': cloud(),
        'partly-cloudy-night': cloud()
    }
    return switcher.get(argument, "clear")


def http_get(host, path, use_stream=True):
    import socket
    import ssl

    addr = socket.getaddrinfo(host, 443)[0][-1]
    s = socket.socket()
    s.connect(addr)
    s = ssl.wrap_socket(s)

    if use_stream:
        s.write(bytes('GET /%s HTTP/1.0\r\nHost: %s\r\n\r\n' % (path, host), 'utf-8'))
        l = s.read(20000)
    else:
        s.send(bytes('GET /%s HTTP/1.0\r\nHost: %s\r\n\r\n' % (path, host), 'utf-8'))
        l = s.recv(20000)
    response, content = l.split(b"\r\n\r\n")
    s.close()
    return str(content, 'utf-8')


def get_weather(lat, lon):
    now = time.localtime().tm_hour
    hour = 8 - now
    if now > 8:
        hour += 24

    # DarkSky URL contructor
    host = "api.darksky.net"
    path = "forecast/" + (CONF['secret']) + "/" + lat + "," + lon + "?exclude=minutely,currently,daily,flags&units=si"
    # Fetch DarkSky data
    resp = http_get(host, path)
    data = json.loads(resp)

    # Get 8AM forecast; TODO: smarter way to use weather data
    eight = data['hourly']['data'][hour]['icon']
    sixteen = data['hourly']['data'][hour + 8]['icon']
    print(eight, sixteen)
    return set_type(eight)


def clear():
    effect_go = time.time()
    PIN_LED.on()
    while time.time() < (effect_go + AUTO_OFF):
        color_wipe(255, 170, 0)

    PIN_LED.off()
    clear_led()

    return "Awesome weather!"


def rain():
    PIN_LED.on()
    PIN_PUMP.on()
    lightning_strobe(200, 200, 255)
    return "Take umbrella!"


def snow():
    PIN_LED.on()
    lightning_strobe(255, 255, 255)
    return "Oooh - snowtime!"


def cloud():
    PIN_LED.on()
    PIN_FOG.on()
    color_wipe(155, 155, 255)
    return "Leave umbrella at home."


# Neopixel wipe color across display a pixel at a time
def color_wipe(red, green, blue, wait=80):
    for i in range(CONF['led']['count']):
        PIXEL[i] = [round(red * PIXEL_MAX), round(green * PIXEL_MAX), round(blue * PIXEL_MAX)]
        PIXEL.write()
        time.sleep_ms(wait)


# Neopixel wipe white across display a pixel at a time very quickly
def lightning_strobe(red, green, blue):
    StrobeTime = [5, 20, 3, 8, 5, 10]
    for i in range(0, len(StrobeTime)):
        for j in range(CONF['led']['count']):
            if i % 2 == 0:
                PIXEL[j] = (0, 0, 0)
            else:
                PIXEL[j] = (int(red * PIXEL_MAX), int(green * PIXEL_MAX), int(blue * PIXEL_MAX))

            PIXEL.write()
            time.sleep_ms(i)


# Neopixel clear pixels
def clear_led():
    for i in range(CONF['led']['count']):
        PIXEL[i] = (0, 0, 0)

    PIXEL.write()


def main_loop():
    import webrepl
    webrepl.start()
    while 1 == 1:
        get_weather(CONF['lat'], CONF['lon'])
        time.sleep(600)


# Initiate main loop
main_loop()
