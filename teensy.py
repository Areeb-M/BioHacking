import serial

connection = None


def connect(port=None, baudrate=19200):
    global connection
    try:
        connection = serial.Serial(port, baudrate)
    except:
        raise "Teensy controller not found."


def write(message):
    global connection
    connection.write(message)


def read():
    global connection
    return connection.read_all()


def sync():
    write(bytes([255, 0, 0, 0]))
    update = ''
    while update == '':
        update += str(read())

