import socket
import numpy
import cv2
import threading
import os

BUFFER_SIZE = 4096*10
currentPort = 50001

buf = b''

class capture():
    def __init__(self,port):
        self.port = port

    def recive(self):
        global buf
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            while True:
                s.bind(("0.0.0.0", self.port))
                try:
                    data,address = s.recvfrom(BUFFER_SIZE)
                    if not data:
                        break
                    buf = buf + data

                finally:
                    s.close()

                narray=numpy.frombuffer(buf,dtype='uint8')
                buf = b""
                return cv2.imdecode(narray,1)
    def show(self):
        while True:
            img = self.recive()
            cv2.imshow('Capture',img)
            if cv2.waitKey(100) & 0xFF == ord('q'):
                break
            img = ''

with socket.socket(socket.AF_INET,socket.SOCK_STREAM) as portInfo:
    portInfo.bind(("0.0.0.0",50000))
    portInfo.listen()
    print("aitayo")
    while True:
        (connection, client) = portInfo.accept()
        print("kita!")
        try:
            data = connection.recv(800)
            if data == b"OpenPortRequest":
                print('recive')
                connection.send(currentPort.to_bytes(2,"big"))
                cap = capture(currentPort)
                th = threading.Thread(target=cap.show)
                th.daemon = True
                th.start()

        finally:
            connection.close()