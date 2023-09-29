import socket
import random
import time

from PIL import Image

HOST = 'localhost'
PORT = 10108
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((HOST, PORT))
DELAY_PER_PIXEL_S= 0.001

def pixel(x, y, r, g, b, a=255):
    # print('pixel')
    time.sleep(DELAY_PER_PIXEL_S)
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

width = 1920
height = 1080


def worm(x, y, n, r, g, b):
    global sock
    while n:
        pixel(x, y, r, g, b, 25)
        x += random.randint(0, 2) - 1
        y += random.randint(0, 2) - 1
        n -= 1

image_options = ['brucon_2023_logo.png', 'brucon_2023_logo.png', 'brucon_2023_logo.png', 'ko-lab.png', 'brucon_2023_logo.png', 'brucon_2023_logo.png', 'ko-lab.png',
                 'brucon_2023_logo.png', 'brucon_2023_logo.png', 'brucon_2023_logo.png', 'ko-lab.png', 'brucon_2023_logo.png', 'brucon_2023_logo.png', 'ko-lab.png',
                 'troll.png']
print('starting')
i=0
while True:
    print('starting loop '+str(i))
    i=i+1
    black = random.randint(0, 1) > 0
    image_choice = random.randint(0, len(image_options));
    try:
        im = Image.open(image_options[image_choice]).convert('RGB')
        im.thumbnail((150, 150), Image.LANCZOS)
        x_offset = random.randint(0, width - 256)
        y_offset = random.randint(0, height - 256)
        _, _, w, h = im.getbbox()
        for x in range(w):
            for y in range(h):
                if black:
                    r, g, b = (10, 10, 10)
                else:
                    r, g, b = im.getpixel((x, y))
                if (r + g + b > 0) or black:
                    pixel(x + x_offset, y + y_offset, r, g, b)

        worm(random.randint(0, width), random.randint(0, height), 30000, random.randint(0, 255),
             random.randint(0, 255),
             random.randint(0, 255))
    except Exception as e:
        print('Sock send error')
        print(e)
        sock.close()
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((HOST, PORT))
    time.sleep(1)
