import network
import time
import socket
from machine import Pin, ADC
from time import sleep_ms
import gc

SSID = "CLUB"
PWD = "K8BXKUG4MFS"

adc = ADC(35)
temp = "-"


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
    html = (
        """<html> <head><title>ESP Web Server</title><meta content="width=device-width, initial-scale=1" name=viewport><!-- <meta http-equiv="refresh" content="5;URL=/"> --><style type=text/css>html{font-family:sans-serif;margin:0 auto;text-align:center;background-color:black}h1{color:#5c91f1;padding:2vh}h2{color:white}p{font-size:1.5rem;color:white}strong{color:red}span{color:green}</style></head> <body> <h1>ESP Web Server</h1> <h2>LM35: </h2> <p><strong>Temperatura:</strong>%s</p>ºC <script type=text/javascript>console.log("micropython")</script> </body> </html>""" % temp
    )
    return html


do_connect()
create_ap()

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(("", 80))
s.listen(5)


while True:
    try:
        temp = adc.read_uv() * 0.0001
    except:
        temp = "-"
    conn, addr = s.accept()
    print("Got a connection from %s" % str(addr))
    request = conn.recv(1024)
    request = str(request)
    print("Content = %s" % request)
    response = web_page()
    conn.send("HTTP/1.1 200 OK\n")
    conn.send("Content-Type: text/html\n")
    conn.send("Connection: close\n\n")
    conn.sendall(response)
    conn.close()
    sleep_ms(50)
    gc.collect()


# https://github.com/micropython/micropython-lib/tree/master
