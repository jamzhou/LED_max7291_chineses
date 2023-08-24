#!/usr/bin/env python
# -*- coding: utf-8 -*-

from luma.led_matrix.device import max7219
from luma.core.interface.serial import spi, noop
from luma.core.render import canvas
from luma.core.virtual import viewport
from PIL import ImageFont
from luma.core.virtual import viewport
from luma.core.sprite_system import framerate_regulator


font_path = '/home/pi/quan.ttf'


def str_to_pixel_data(words):
    data = []
    font = ImageFont.truetype('E:/Software/Fonts/quan.ttf', 8)
    char_hex_list = []
    img_core = font.getmask(words, '1')
    h, w = img_core.size
    for i in range(h):
        v = 0
        for j in range(w):
            value = img_core[h * j + i]
            if value > 0:
                v = v + 2**j
        char_hex_list.append(v)
        if len(char_hex_list) == 8:
            data.append(char_hex_list)
            char_hex_list = []
    while len(char_hex_list) < 8:
        char_hex_list.append(0x00)
    data.append(char_hex_list)
    return data


if __name__ == '__main__':
    message = 'Hello,中文'  # the message that you want to show on LED
    is_roll = True  # let the message roll on LED
    # create matrix device
    serial = spi(port=0, device=0, gpio=noop())
    device = max7219(serial, cascaded=4, block_orientation=-90, rotate=0, blocks_arranged_in_reverse_order=False)
    
    # adjust LED brightness (0-255)
    # device.contrast(1)


    data = str_to_pixel_data(message)
    x = device.width if is_roll else 0
    y = 0
    virtual = viewport(device, width=8*len(data) + device.width + device.width, height=device.height)
    with canvas(virtual) as draw:
        for c in data:
            for byte in c:
                for j in range(8):
                    if byte & 0x01 > 0:
                        draw.point((x, y + j), fill='white')
                    byte >>= 1
                x += 1

    if is_roll:
        regulator = framerate_regulator(20) # control the speed of rolling
        while True:
            i = 0
            while i <= 8*len(data) + device.width:
                with regulator:
                    virtual.set_position((i, 0))
                    i += 1

