"""
myexample.py

created by dromakin as 01.11.2020
Project iBeacon
"""

__author__ = 'dromakin'
__maintainer__ = 'dromakin'
__credits__ = ['dromakin', ]
__status__ = 'Development'
__version__ = '20201101'

import datetime
import sys
import os
import time

from PIL import Image, ImageDraw, ImageFont

from lib.waveshare_epd import epd2in7
from gpiozero import Button

# import logging
# import traceback

from forex_python.converter import CurrencyCodes


# 264×176
class Display:

    def __init__(self, price=None, currency=None) -> None:

        self.price = self.check_price(price)

        self.currency = self.check_currency(currency)

        c = CurrencyCodes()
        self.currency_code = c.get_symbol(self.currency)

        super().__init__()

    @staticmethod
    def check_price(price=None) -> str:
        price_ = None
        if isinstance(price, str):
            price_ = price

        if isinstance(price, int):
            price_ = str(price)

        if isinstance(price, float):
            price_ = "{:.2f}".format(price)

        if price is None:
            price_ = "0.0"

        return price_

    @staticmethod
    def check_currency(currency=None) -> str:
        currency_ = None

        if currency is None:
            currency_ = "RUB"

        if currency.isupper() is True:
            currency_ = currency

        return currency_




def main():
    picdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'pic')

    epd = epd2in7.EPD()
    epd.init()
    epd.Clear(0xFF)
    # epd.Init_4Gray()

    # For simplicity, the arguments are explicit numerical coordinates
    image = Image.new('1', (epd2in7.EPD_HEIGHT, epd2in7.EPD_WIDTH), 255)  # 255: clear the image with white
    draw = ImageDraw.Draw(image)
    # font = ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeMonoBold.ttf', 18)
    font24 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 24)
    font18 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 18)
    font35 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 35)

    font = font24

    c = CurrencyCodes()

    draw.line((29, 0, 29, 176), fill=0)

    draw.rectangle((0, 0, 29, 36), fill=0)
    draw.text((5, 4), c.get_symbol('RUB'), font=font, fill=255)
    draw.text((5, 44), "$", font=font, fill=0)
    draw.text((5, 88), c.get_symbol('EUR'), font=font, fill=0)
    draw.text((5, 132), c.get_symbol('GBP'), font=font, fill=0)

    # epd.display_4Gray(epd.getbuffer_4Gray(image))
    epd.display(epd.getbuffer(image))

    # draw.text((10, ), 'e-Paper demo', font=font, fill=0)
    # draw.text((10, 50), 'e-Paper demo', font=font, fill=0)
    # draw.rectangle((0, 76, 176, 96), fill=0)
    # draw.text((18, 80), 'Hello world!', font=font, fill=255)
    # draw.line((10, 130, 10, 180), fill=0)
    # draw.line((10, 130, 50, 130), fill=0)
    # draw.line((50, 130, 50, 180), fill=0)
    # draw.line((10, 180, 50, 180), fill=0)
    # draw.line((10, 130, 50, 180), fill=0)
    # draw.line((50, 130, 10, 180), fill=0)
    # draw.arc((90, 190, 150, 250), 0, 360, fill=0)
    # draw.chord((90, 120, 150, 180), 0, 360, fill=0)
    # draw.rectangle((10, 200, 50, 250), fill=0)

    # epd.display(epd.getbuffer(image))

    # display images
    # epd.display_frame(epd.get_frame_buffer(Image.open('monocolor.bmp')))

    epd.sleep()

    epd.Dev_exit()


if __name__ == '__main__':
    main()
