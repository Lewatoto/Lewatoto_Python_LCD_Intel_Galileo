#!/usr/bin/python

#
# based on code from lrvick and LiquidCrystal
# lrvic - https://github.com/lrvick/raspi-hd44780/blob/master/hd44780.py
# LiquidCrystal - https://github.com/arduino/Arduino/blob/master/libraries/LiquidCrystal/LiquidCrystal.cpp
# Adafruit_CharLCD - https://github.com/adafruit/Adafruit-Raspberry-Pi-Python-Code/blob/legacy/Adafruit_CharLCD/Adafruit_CharLCD.py
#

from time import sleep

class Lewatoto_CharLCD(object):

    # Commands
    LCD_CLEARDISPLAY        = 0x01
    LCD_RETURNHOME          = 0x02
    LCD_ENTRYMODESET        = 0x04
    LCD_DISPLAYCONTROL      = 0x08
    LCD_CURSORSHIFT         = 0x10
    LCD_FUNCTIONSET         = 0x20
    LCD_SETCGRAMADDR        = 0x40
    LCD_SETDDRAMADDR        = 0x80

    # flags for display entry mode
    LCD_ENTRYRIGHT          = 0x00
    LCD_ENTRYLEFT           = 0x02
    LCD_ENTRYSHIFTINCREMENT = 0x01
    LCD_ENTRYSHIFTDECREMENT = 0x00

    # flags for display on/off control
    LCD_DISPLAYON           = 0x04
    LCD_DISPLAYOFF          = 0x00
    LCD_CURSORON            = 0x02
    LCD_CURSOROFF           = 0x00
    LCD_BLINKON             = 0x01
    LCD_BLINKOFF            = 0x00

    # flags for display/cursor shift
    LCD_DISPLAYMOVE         = 0x08
    LCD_CURSORMOVE          = 0x00

    # flags for display/cursor shift
    LCD_DISPLAYMOVE         = 0x08
    LCD_CURSORMOVE          = 0x00
    LCD_MOVERIGHT           = 0x04
    LCD_MOVELEFT            = 0x00

    # flags for function set
    LCD_8BITMODE            = 0x10
    LCD_4BITMODE            = 0x00
    LCD_2LINE               = 0x08
    LCD_1LINE               = 0x00
    LCD_5x10DOTS            = 0x04
    LCD_5x8DOTS             = 0x00

    def __init__(self, pin_rs=2, pin_e=3, pins_db=[7,6,5,4], mraa=None):
        if not mraa:
            import mraa

	    self.pin_rs = pin_rs
	    self.pin_e = pin_e
	    self.pins_db = pins_db

        self.pin_rs = mraa.Gpio(self.pin_rs)
        self.pin_e = mraa.Gpio(self.pin_e)

        for x in range(4):
            self.pins_db[x]= mraa.Gpio(self.pins_db[x])

        self.pin_rs.dir(mraa.DIR_OUT)
        self.pin_e.dir(mraa.DIR_OUT)

        for y in range(4):
            self.pins_db[y].dir(mraa.DIR_OUT)

	    self.pin_rs.write(0)
	    self.pin_e.write(0)
	    for pin in range(4):
            self.pins_db[pin].write(0)

        self.write4bits(0x33)  # initialization
        self.write4bits(0x32)  # initialization
        self.write4bits(0x28)  # 2 line 5x7 matrix
        self.write4bits(0x0E)  # turn cursor off 0x0E
	    self.write4bits(0x06)  # shift cursor right

        self.displaycontrol = self.LCD_DISPLAYON | self.LCD_CURSOROFF | self.LCD_BLINKOFF

        self.displayfunction = self.LCD_4BITMODE | self.LCD_1LINE | self.LCD_5x8DOTS
        self.displayfunction |= self.LCD_2LINE

        # Initialize to default text direction (for romance languages)
        self.displaymode = self.LCD_ENTRYLEFT | self.LCD_ENTRYSHIFTDECREMENT
        self.write4bits(self.LCD_ENTRYMODESET | self.displaymode)  # set the entry mode

    def begin(self, cols, lines):
        if (lines > 1):
            self.numlines = lines
            self.displayfunction |= self.LCD_2LINE

    def home(self):
        self.write4bits(self.LCD_RETURNHOME)  # set cursor position to zero
        self.delayMicroseconds(3000) # this command takes a long time!

    def clear(self):
        self.write4bits(self.LCD_CLEARDISPLAY)  # command to clear display
        self.delayMicroseconds(3000)  # 3000 microsecond sleep, clearing the display takes a long time

    def write4bits(self, bits, char_mode=0):
        """ Send command to LCD """
        self.delayMicroseconds(1000)
        bits = bin(bits)[2:].zfill(8)
        self.pin_rs.write(char_mode)
        for pin in range(4):
            self.pins_db[pin].write(0)
	    for i in range(4):
            if bits[i] == "1":
                self.pins_db[i].write(1)
	    self.pulseEnable()
        for pin in range(4):
            self.pins_db[pin].write(0)
        for i in range(4, 8):
            if bits[i] == "1":
                self.pins_db[i-4].write(1)
        self.pulseEnable()

    def delayMicroseconds(self, microseconds):
        seconds = microseconds / float(1000000)
        sleep(seconds)

    def pulseEnable(self):
        self.pin_e.write(0)
        self.delayMicroseconds(1)
        self.pin_e.write(1)
        self.delayMicroseconds(1)
        self.pin_e.write(0)
        self.delayMicroseconds(1)

    def message(self, text):
        """ Send string to LCD. Newline wraps to second line"""
        for char in text:
            if char == '\n':
                self.write4bits(0xC0)  # next line
            else:
                self.write4bits(ord(char), 1)

if __name__ == '__main__':
    lcd = Lewatoto_CharLCD()
    lcd.clear()
    lcd.message(" ¡ Hola\n  Mundo !")
