from machine import Pin,PWM #importing PIN and PWM
from time import sleep
import network
import socket

# Defining motor pins
motor1=Pin(10,Pin.OUT)
motor2=Pin(11,Pin.OUT)
motor3=Pin(12,Pin.OUT)
motor4=Pin(13,Pin.OUT)

# Defining enable pins and PWM object
enable1=PWM(Pin(6))
enable2=PWM(Pin(7))

# Defining frequency for enable pins
enable1.freq(1000)
enable2.freq(1000)

# Setting maximum duty cycle for maximum speed (0 to 65025)
enable1.duty_u16(65025)
enable2.duty_u16(65025)

ssid = 'WIFI_SSID' #Your Wifi SSID
password = 'WIFI_PASSWORD' #Your Wifi Password


# Forward
def move_forward():
    motor1.high()
    motor2.low()
    motor3.low()
    motor4.high()
    
# Backward
def move_backward():
    motor1.low()
    motor2.high()
    motor3.high()
    motor4.low()
    
#Turn Right
def turn_right():
    motor1.low()
    motor2.high()
    motor3.low()
    motor4.high()
    
#Turn Left
def turn_left():
    motor1.high()
    motor2.low()
    motor3.high()
    motor4.low()
    
#Stop
def stop():
    print("stop")
    motor1.low()
    motor2.low()
    motor3.low()
    motor4.low()
    
def connect():
    #Connect to WLAN
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, password)
    while wlan.isconnected() == False:
        print('Waiting for connection...')
        sleep(1)
    ip = wlan.ifconfig()[0]
    print(f'Connected on {ip}')
    return ip

def open_socket(ip):
    # Open a socket
    address = (ip, 80)
    connection = socket.socket()
    connection.bind(address)
    connection.listen(1)
    return connection

def webpage(state):
    # UI Template HTML for Robot Control
    html = f"""
            <!DOCTYPE html>
            <html>
            <head>
            <title>Pico Hash Control</title>
            <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.4.1/css/bootstrap.min.css">
            </head>
            <body>
            <div class="container">
            <h1 class="text-center" style="color:#4287f5">Hash Robotics</h1>
            <div class="row">
            <h2 class="text-center" style="color:#42c8f5">Wifi Controlled Robot</h2>
            <div style="padding:10px" class="col-sm-12">
            <div class="col-sm-4"></div>
            <div class="col-sm-4"><form action="./move_forward"><input class="btn btn-success btn-lg btn-block" type="submit" value="Move Forward" /></form></div>
            <div class="col-sm-4"></div>
            </div>
            <div style="padding:10px" class="col-sm-12">
            <div class="col-sm-4"><form action="./turn_left"><input class="btn btn-success btn-lg btn-block" type="submit" value="Turn Left" /></form></div>
            <div class="col-sm-4"><form action="./stop"><input class="btn btn-success btn-lg btn-block" type="submit" value="Stop" /></form></div>
            <div class="col-sm-4"><form action="./turn_right"><input class="btn btn-success btn-lg btn-block" type="submit" value="Turn Right" /></form></div>
            </div>
            <div style="padding:10px" class="col-sm-12">
            <div class="col-sm-4"></div>
            <div class="col-sm-4"><form action="./move_backward"><input class="btn btn-success btn-lg btn-block" type="submit" value="Move Backward" /></form></div>
            <div class="col-sm-4"></div>
            </div>
            </div>
            </div>
            </body>
            </html>
            """
    return str(html)
    
def serve(connection):
    #Start a web server
    state = ''
    while True:
        client = connection.accept()[0]
        request = client.recv(1024)
        request = str(request)
        try:
            request = request.split()[1]
        except IndexError:
            pass
        if request == '/move_forward?':
            print("move_forward")
            move_forward()
            sleep(2)
            stop()
        elif request =='/move_backward?':
            print("move_backward")
            move_backward()
            sleep(2)
            stop()
        elif request =='/turn_right?':
            print("turn_right")
            turn_right()       
            sleep(1)
            stop()
        elif request =='/turn_left?':
            print("turn_left")
            turn_left()       
            sleep(1)
            stop()
        elif request =='/stop?':
            stop()
            print("stop")
         
        html = webpage(state)
        client.send(html)
        client.close()


#Begin
try:
    ip = connect()
    connection = open_socket(ip)
    serve(connection)
except KeyboardInterrupt:
    machine.reset()

    