import network
import time
import socket

# "TP-HOME"
# "KUxdqn8&rNdf8*"
SSID = "Sakeri"
PWD = "URIYELFER09012010"


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
    ap.config(ssid="ESP-AP",password="password")  # set the SSID of the access point
    ap.config(max_clients=8)  # set how many clients can connect to the network
    while not ap.active():
        pass
    print('Connection successful')
    print(ap.ifconfig())


def web_page():

    html = (
        """<html><head> <title>ESP Web Server</title> <meta name="viewport" content="width=device-width, initial-scale=1">
    <link rel="icon" href="data:,"> <style>html{font-family: Helvetica; display:inline-block; margin: 0px auto; text-align: center;}
    h1{color: #0F3376; padding: 2vh;}p{font-size: 1.5rem;}.button{display: inline-block; background-color: #e7bd3b; border: none; 
    border-radius: 4px; color: white; padding: 16px 40px; text-decoration: none; font-size: 30px; margin: 2px; cursor: pointer;}
    .button2{background-color: #4286f4;}</style></head><body> <h1>ESP Web Server</h1> 
    <p>GPIO state: <strong>"""
        + "XXX"
        + """</strong></p><p><a href="/?led=on"><button class="button">ON</button></a></p>
    <p><a href="/?led=off"><button class="button button2">OFF</button></a></p></body></html>"""
    )
    return html


do_connect()
create_ap()

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(("", 80))
s.listen(5)

while True:
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

# https://github.com/micropython/micropython-lib/tree/master
