import socket
import random
import time

from PIL import Image

HOST = 'localhost'
PORT = 10108
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((HOST, PORT))


def pixel(x, y, r, g, b, a=255):
    global sock
    if a == 255:
        sock.send(bytes('PX %d %d %02x%02x%02x\n' % (x, y, r, g, b), 'utf-8'))
    else:
        sock.send(bytes('PX %d %d %02x%02x%02x%02x\n' % (x, y, r, g, b, a), 'utf-8'))


# A few helper functions:

def rect(x, y, w, h, r, g, b):
    for i in range(x, x + w):
        for j in range(y, y + h):
            pixel(i, j, r, g, b)


rect(0, 0, 100, 100, 100, 100, 100)


def worm(x=512, y=512, n=1000000, r=255, g=255, b=255):
    global sock
    try:
        while n:
            pixel(x, y, r, g, b, 25)
            x += random.randint(0, 2) - 1
            y += random.randint(0, 2) - 1
            n -= 1
    except Exception as e:
        print('Sock send error')
        print(e)
        sock.close()
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((HOST, PORT))


while True:
    im = Image.open('test.png').convert('RGB')
    im.thumbnail((256, 256), Image.LANCZOS)
    x_offset = random.randint(0, 1024 - 256)
    y_offset = random.randint(0, 1024 - 256)
    _, _, w, h = im.getbbox()
    for x in range(w):
        for y in range(h):
            r, g, b = im.getpixel((x, y))
            if r + g + b > 0:
                pixel(x + x_offset, y + y_offset, r, g, b)

    worm(random.randint(0, 1024), random.randint(0, 1024), 1000000, random.randint(0, 255), random.randint(0, 255),
         random.randint(0, 255))
