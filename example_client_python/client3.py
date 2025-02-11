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
    block = random.randint(0, 1) > 0
    image_choice = random.randint(0, len(image_options));
    try:
        im = Image.open(image_options[image_choice]).convert('RGB')
        imageSize = random.randint(50, 250)
        im.thumbnail((imageSize, imageSize), Image.LANCZOS)
        x_offset = random.randint(0, width - 256)
        y_offset = random.randint(0, height - 256)
        _, _, w, h = im.getbbox()
        blockR = random.randint(0, 255)
        blockG = random.randint(0, 255)
        blockB = random.randint(0, 255)
        for x in range(w):
            for y in range(h):
                if block:
                    r, g, b = (blockR, blockG, blockB)
                else:
                    r, g, b = im.getpixel((x, y))
                if (r + g + b > 0) or block:
                    pixel(x + x_offset, y + y_offset, r, g, b)

        wormLen = random.randint(1000,100000)
        worm(random.randint(0, width), random.randint(0, height), wormLen, random.randint(0, 255),
             random.randint(0, 255),
             random.randint(0, 255))
    except Exception as e:
        print('Sock send error')
        print(e)
        sock.close()
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((HOST, PORT))
    time.sleep(1)
