import network
import time
import socket
from machine import Pin
from time import sleep_ms
import gc

gc.collect()

SSID = ""
PWD = ""


def do_connect():
    import network

    wlan = network.WLAN(network.WLAN.IF_STA)
    wlan.active(True)
    if not wlan.isconnected():
        print("connecting to network...")
        wlan.connect(SSID, PWD)
        while not wlan.isconnected():
            print(".", end="")
            time.sleep(0.1)
    print()
    print("Connected to: ", SSID, "network config:", wlan.ifconfig())


def create_ap():
    ap = network.WLAN(network.WLAN.IF_AP)  # create access-point interface
    ap.active(True)  # activate the interface
    # set the SSID of the access point
    ap.config(ssid="ESP-AP", password="password")
    ap.config(max_clients=8)  # set how many clients can connect to the network
    while not ap.active():
        pass
    print('Connection successful')
    print(ap.ifconfig())


def web_page():
    gpio_state = ""
    if led.value():
        gpio_state = "ON"
    else:
        gpio_state = "OFF"
    html = (
        """<html><head><title>ESP Web Server</title><meta content="width=device-width, initial-scale=1" name="viewport"/><link href="data:," rel="icon"/><style type="text/css">html{font-family:sans-serif;margin:0 auto;text-align:center;background-color:black}h1,h2{color:#f7f7f7}p{font-size:1.5rem}.button{display:inline-block;background-color:#e7bd3b;border:0;border-radius:4px;color:white;padding:16px 40px;text-decoration:none;font-size:30px;margin:2px;cursor:pointer}.button2{background-color:#4286f4}</style></head><body><h1>ESP Web Server</h1><p>GPIO state: <strong>%s</strong></p><p><a href="/?led=on"><button class="button">ON</button></a></p><p><a href="/?led=off"><button class="button button2">OFF</button></a></p><script type="text/javascript"></script></body></html>""" % gpio_state
    )
    return html


# do_connect()
create_ap()

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(("", 80))
s.listen(5)

led = Pin(26, Pin.OUT)
led.value(0)

while True:
    conn, addr = s.accept()
    print("Got a connection from %s" % str(addr))
    request = conn.recv(1024)
    request = str(request)
    print("Content = %s" % request)
    led_on = request.find('on')
    led_off = request.find('off')
    print("led on value: %s" % led_on )
    print("led off value: %s" % led_off )
    if led_on != -1:
        led.value(1)
    if led_off != -1:
        led.value(0)
    response = web_page()
    conn.send("HTTP/1.1 200 OK\n")
    conn.send("Content-Type: text/html\n")
    conn.send("Connection: close\n\n")
    conn.sendall(response)
    conn.close()
    sleep_ms(50)

# https://github.com/micropython/micropython-lib/tree/master
