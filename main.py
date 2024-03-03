import network
import socket
from time import sleep
import machine
import PicoRobotics
board = PicoRobotics.KitronikPicoRobotics()

# Yes, these could be in another file. But on the Pico! So no more secure. :)
ssid = ''
password = ''

def move_forward(speed):
    board.motorOn(1, 'f', speed)
    board.motorOn(2, 'f', speed)
    
def move_backward(speed):
    board.motorOn(1, 'r', speed)
    board.motorOn(2, 'r', speed)

def move_stop():
    board.motorOff(1)
    board.motorOff(2)
    board.motorOff(3)
    board.motorOff(4)

def move_left(speed):
    board.motorOn(1, 'f', speed)
    board.motorOn(2, 'r', speed)

def move_right(speed):    
    board.motorOn(2, 'f', speed)
    board.motorOn(1, 'r', speed)

def arm_up(speed):
    board.motorOn(3, 'f', speed)
    
def arm_down(speed):
    board.motorOn(3, 'b', speed)

def gripper_open(speed):
    board.motorOn(4, 'f', speed)
    
def gripper_close(speed):
    board.motorOn(4, 'b', speed)
    
    #Stop the robot as soon as possible
move_stop()
    
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

def webpage():
    #Template HTML
    html = f"""
            <!DOCTYPE html>
            <html>
            <head>
            <title>Kitronik Robot Control</title>
            </head>
            <center><b>
            <form action="./forward">
            <input type="submit" value="Forward" style="height:120px; width:120px" />
            </form>
            <table><tr>
            <td><form action="./left">
            <input type="submit" value="Left" style="height:120px; width:120px" />
            </form></td>
            <td><form action="./stop">
            <input type="submit" value="Stop" style="height:120px; width:120px" />
            </form></td>
            <td><form action="./right">
            <input type="submit" value="Right" style="height:120px; width:120px" />
            </form></td>
            </tr></table>
            <form action="./back">
            <input type="submit" value="Back" style="height:120px; width:120px" />
            </form>
            <table><tr>
            <td><form action="./up"><input type="submit" value="Up" style="height:120px; width:120px" />
            </form></td>
            <td><form action="./down"><input type="submit" value="Down" style="height:120px; width:120px" />
            </form></td>
            <td><form action="./open"><input type="submit" value="Open" style="height:120px; width:120px" />
            </form></td>
            <td><form action="./close"><input type="submit" value="Close" style="height:120px; width:120px" />
            </form></td>
            </center>
            </body>
            </html>
            """
    return str(html)

def serve(connection):
    #Start web server
    while True:
        client = connection.accept()[0]
        request = client.recv(1024)
        request = str(request)
        try:
            request = request.split()[1]
        except IndexError:
            pass
        if request == '/forward?':
            move_forward(50)
        elif request =='/left?':
            move_left(50)
        elif request =='/stop?':
            move_stop()
        elif request =='/right?':
            move_right(50)
        elif request =='/back?':
            move_backward(50)
        elif request =='/up?':
            arm_up(50)
        elif request =='/down?':
            arm_down(50)
        elif request =='/open?':
            gripper_open(50)
        elif request =='/close?':
            gripper_close(50)
        html = webpage()
        client.send(html)
        client.close()

try:
    ip = connect()
    connection = open_socket(ip)
    serve(connection)
except KeyboardInterrupt:
    machine.reset()

    
