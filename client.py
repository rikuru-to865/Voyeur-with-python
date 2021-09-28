import socket
import cv2

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FPS, 10)
cap.set(3,320)
cap.set(4,240)
ip = "" #server ip
BUFFER_SIZE = 4096
encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 30]
with socket.socket(socket.AF_INET,socket.SOCK_STREAM) as l:
    l.connect((ip,50000))
    l.send(b"OpenPortRequest")
    port = int.from_bytes(l.recv(800),'big')

with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        jpegstring=cv2.imencode('.jpg', frame,encode_param)[1].tobytes()

        s.sendto(jpegstring,(ip,int(port)))