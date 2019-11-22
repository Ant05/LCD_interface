import socket
import fcntl
import struct
import netifaces as ni
import time
import I2C_LCD_driver

fontdata0 = [

        [0x1F, 0x1F, 0x18, 0x18, 0x18, 0x18, 0x18, 0x18],#0 upper left

        [0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00],#1 null

        [0x1F, 0x1F, 0x03, 0x03, 0x03, 0x03, 0x03, 0x03],#2 per right

        [0x03, 0x03, 0x03, 0x03, 0x03, 0x03, 0x03, 0x03],#3 center right

        [0x18, 0x18, 0x18, 0x18, 0x18, 0x18, 0x18, 0x18],#4 center left

        [0x18, 0x18, 0x18, 0x18, 0x18, 0x18, 0x1F, 0x1F],#5 bottom left

        [0x1F, 0x1F, 0x1F, 0x1F, 0x1F, 0x1F, 0x1F, 0x1F],#6 Full

        [0x03, 0x03, 0x03, 0x03, 0x03, 0x03, 0x1F, 0x1F],#7 bottom right
]

displayPosition = [0x80, 0xC0, 0x94, 0xD4]

#FIRST POSITION IN LCD_DISPLAY_STRING AND IN OTHER LCD FUNCTIONS IS RAWS, THE SECOND IS COLUMNS,
#RAWS STARTS AT 1, COLUMNS STARTS AT 0

mylcd =  I2C_LCD_driver.lcd()

class Menu:#to create a menu with an input string list
    def __init__(self, list): # "list" is the string list input
        self.list = list
        self.shiftCounter = -1

    def display(self, shiftCounter):
        i = 0 #index Counter
        rawsCounter = 1
        shiftList = [None, None, None, None]

        while i < 4:
            shiftList[i] = self.list[i + shiftCounter]
            i = i + 1

        while rawsCounter < 5:
            mylcd.lcd_display_string(shiftList[rawsCounter - 1], rawsCounter, 0)
            rawsCounter = rawsCounter + 1


    def displayCursor(self, cursor):
        OutOfIndexState = 0
        a = 0
        mylcd.lcd_load_custom_chars(fontdata0)


        if cursor < 0:
            cursor = 0
            OutOfIndexState = +1

        if cursor > 3:
            if len(self.staticList) < 4:
                cursor = 3
                #cursor = cursor - 1OutOfIndexState = -1

            if cursor < len(self.staticList):
                a = a + 1
                OutOfIndexState  = 5
            else:
                pass


        mylcd.lcd_write(displayPosition[cursor - a])
        mylcd.lcd_write_char(6)
        return OutOfIndexState

    def run(self, cursor):
        self.display(self.shiftCounter)
        self.displayPointer(cursor)
        if self.displayPointer(cursor) == 5:
            if self.shiftCounter < len(self.staticList) - 4:
                self.shiftCounter = self.shiftCounter + 1

            else:
                self.shiftCounter = self.shiftCounter
            self.run(cursor)

    def read(self, btnState, cursor):#return encoder button status on the current raw(using pointer)
        state = -1

        if btnState == 0:
            state = cursor
        else:
            state = -1

        return state

class DynamicMenu:
    def __init__(self, staticList):
        self.staticList = staticList
        self.shiftCounter = -1

    def displayStatic(self, shiftCounter):
        i = 0 #index Counter
        rawsCounter = 1
        shiftStaticList = [None, None, None, None]


        while i < 4:
            shiftStaticList[i] = self.staticList[i + shiftCounter]
            i = i + 1

        while rawsCounter < 5:
            mylcd.lcd_display_string(shiftStaticList[rawsCounter - 1], rawsCounter, 0)
            rawsCounter = rawsCounter + 1

    def displayDynamic(self, dynamicList, shiftCounter):
        i = 0
        rawsCounter = 1
        shiftDynamicList = [None, None, None, None]
        if len(self.staticList) != len(dynamicList):
            print("Error: dynamicList must have same size as initial list!")


        while i < 4:
            shiftDynamicList[i] = dynamicList[i + shiftCounter]
            i = i + 1


        while rawsCounter < 5:
            mylcd.lcd_display_string(shiftDynamicList[rawsCounter - 1], rawsCounter, 13)
            rawsCounter = rawsCounter + 1


    def displayCursor(self, cursor):
        OutOfIndexState = 0
        a = 0
        mylcd.lcd_load_custom_chars(fontdata0)


        if cursor < 0:
            cursor = 0
            OutOfIndexState = +1

        if cursor > 3:
            if len(self.staticList) < 4:
                cursor = 3
                #cursor = cursor - 1OutOfIndexState = -1

            if cursor < len(self.staticList):
                a = a + 1
                OutOfIndexState  = 5
            else:
                pass


        mylcd.lcd_write(displayPosition[cursor - a])
        mylcd.lcd_write_char(6)
        return OutOfIndexState

    def run(self, dynamicList, cursor):
        self.displayStatic(self.shiftCounter)
        self.displayDynamic(dynamicList, self.shiftCounter)
        self.displayCursor(cursor)
        if self.displayCursor(cursor) == 5:
            if self.shiftCounter < len(self.staticList) - 4:
                self.shiftCounter = self.shiftCounter + 1

            else:
                self.shiftCounter = self.shiftCounter
            self.run(dynamicList, cursor)

    def read(self, btnState, cursor):#return encoder button status on the current raw(using cursor)
        state = -1

        if btnState == 0:
            state = cursor
        else:
            state = -1

        return state



class SquareImage:#to create the different square simbol, take type for the component type and state for its state
    def __init__(self, type, state):
        self.type = type
        self.state = state

    def display(self):
        if(self.state == "ON" and self.type == "printer" ):
            mylcd.lcd_load_custom_chars(fontdata0) #display the rectangle with the "P" letter inside
            mylcd.lcd_write(0x81)
            mylcd.lcd_write_char(0)
            mylcd.lcd_write_char(1)
            mylcd.lcd_write_char(2)
            mylcd.lcd_write(0xC1)
            mylcd.lcd_write_char(4)
            mylcd.lcd_write(0xC3)
            mylcd.lcd_write_char(3)
            mylcd.lcd_write(0x95)
            mylcd.lcd_write_char(5)
            mylcd.lcd_write_char(1)
            mylcd.lcd_write_char(7)
            mylcd.lcd_display_string("P", 2, 2)
        if (self.state == "OFF" and self.type == "printer" ):
            mylcd.lcd_load_custom_chars(fontdata0) #display nothing in the rectangle area(using null char)
            mylcd.lcd_write(0x81)
            mylcd.lcd_write_char(1)
            mylcd.lcd_write_char(1)
            mylcd.lcd_write_char(1)
            mylcd.lcd_write(0xC1)
            mylcd.lcd_write_char(1)
            mylcd.lcd_write(0xC3)
            mylcd.lcd_write_char(1)
            mylcd.lcd_write(0x95)
            mylcd.lcd_write_char(1)
            mylcd.lcd_write_char(1)
            mylcd.lcd_write_char(1)
        if (self.state == "ON" and self.type == "light"):
            mylcd.lcd_load_custom_chars(fontdata0)#display the rectangle with the "L" letter inside
            mylcd.lcd_write(0x86)
            mylcd.lcd_write_char(0)
            mylcd.lcd_write_char(1)
            mylcd.lcd_write_char(2)
            mylcd.lcd_write(0xC6)
            mylcd.lcd_write_char(4)
            mylcd.lcd_write(0xC8)
            mylcd.lcd_write_char(3)
            mylcd.lcd_write(0x9A)
            mylcd.lcd_write_char(5)
            mylcd.lcd_write_char(1)
            mylcd.lcd_write_char(7)
            mylcd.lcd_display_string("L", 2, 7)
        if (self.state == "OFF" and self.type == "light"):
            mylcd.lcd_load_custom_chars(fontdata0) #display nothing in the rectangle area(using null char)
            mylcd.lcd_write(0x86)
            mylcd.lcd_write_char(1)
            mylcd.lcd_write_char(1)
            mylcd.lcd_write_char(1)
            mylcd.lcd_write(0xC6)
            mylcd.lcd_write_char(1)
            mylcd.lcd_write(0xC8)
            mylcd.lcd_write_char(1)
            mylcd.lcd_write(0x9A)
            mylcd.lcd_write_char(1)
            mylcd.lcd_write_char(1)
            mylcd.lcd_write_char(1)
        if (self.state == "ON" and self.type == "cam"):
            mylcd.lcd_load_custom_chars(fontdata0)#display the rectangle with the "C" letter inside
            mylcd.lcd_write(0x8B)
            mylcd.lcd_write_char(0)
            mylcd.lcd_write_char(1)
            mylcd.lcd_write_char(2)
            mylcd.lcd_write(0xCB)
            mylcd.lcd_write_char(4)
            mylcd.lcd_write(0xCD)
            mylcd.lcd_write_char(3)
            mylcd.lcd_write(0x9F)
            mylcd.lcd_write_char(5)
            mylcd.lcd_write_char(1)
            mylcd.lcd_write_char(7)
            mylcd.lcd_display_string("C", 2, 12)
        if (self.state == "OFF" and self.type == "cam"):
            mylcd.lcd_load_custom_chars(fontdata0) #display nothing in the rectangle area(using null char)
            mylcd.lcd_write(0x8B)
            mylcd.lcd_write_char(1)
            mylcd.lcd_write_char(1)
            mylcd.lcd_write_char(1)
            mylcd.lcd_write(0xCB)
            mylcd.lcd_write_char(1)
            mylcd.lcd_write(0xCD)
            mylcd.lcd_write_char(1)
            mylcd.lcd_write(0x9F)
            mylcd.lcd_write_char(1)
            mylcd.lcd_write_char(1)
            mylcd.lcd_write_char(1)
        if (self.state == "ON" and self.type == "buzzer"):
            mylcd.lcd_load_custom_chars(fontdata0)#display the rectangle with the "B" letter inside
            mylcd.lcd_write(0x90)
            mylcd.lcd_write_char(0)
            mylcd.lcd_write_char(1)
            mylcd.lcd_write_char(2)
            mylcd.lcd_write(0xD0)
            mylcd.lcd_write_char(4)
            mylcd.lcd_write(0xD2)
            mylcd.lcd_write_char(3)
            mylcd.lcd_write(0xA4)
            mylcd.lcd_write_char(5)
            mylcd.lcd_write_char(1)
            mylcd.lcd_write_char(7)
            mylcd.lcd_display_string("B", 2, 17)
        if (self.state == "OFF" and self.type == "buzzer"):
            mylcd.lcd_load_custom_chars(fontdata0) #display nothing in the rectangle area(using null char)
            mylcd.lcd_write(0x90)
            mylcd.lcd_write_char(1)
            mylcd.lcd_write_char(1)
            mylcd.lcd_write_char(1)
            mylcd.lcd_write(0xD0)
            mylcd.lcd_write_char(1)
            mylcd.lcd_write(0xD2)
            mylcd.lcd_write_char(1)
            mylcd.lcd_write(0xA4)
            mylcd.lcd_write_char(1)
            mylcd.lcd_write_char(1)
            mylcd.lcd_write_char(1)

class standByScreen: #standby screen shows what component is actually active and displays bed and box temperature
    def __init__ (self, temp1, temp2, State0, State1, State2, State3):
        self.temp1 = temp1
        self.temp2 = temp2
        self.State0 = State0
        self.State1 = State1
        self.State2 = State2
        self.State3 = State3
    def display(self): #val is the same as the Menu class

        printerimage = SquareImage("printer", self.State0)
        printerimage.display()
        lightimage = SquareImage("light", self.State1)
        lightimage.display()
        camimage = SquareImage("cam", self.State2)
        camimage.display()
        buzzerimage = SquareImage("buzzer", self.State3)
        buzzerimage.display()
        mylcd.lcd_display_string("H:"+str(self.temp1), 4, 1)
        mylcd.lcd_display_string("B:"+str(self.temp2), 4, 15)
        printTime(4, 7, True)

def voidstring():
    voidString = "                    "
    return voidString

def clear():#clear() call the lcd_clear function of I2C_lcd_driver
    mylcd.lcd_clear()

def IpAdress(): #shows the pi ip adress
    ni.ifaddresses('wlan0')
    ip = ni.ifaddresses('wlan0')[ni.AF_INET][0]['addr']
    return ip  # should print "192.168.100.37"import socket

def printTime(posR, posC, shift): #Print time, "shift" argument used to display hours like "12::50" or "12:50"
    if (shift == False):
        mylcd.lcd_display_string(time.strftime("%H:%M"),posR,posC)
    else:
        mylcd.lcd_display_string(time.strftime("%H::%M"),posR,posC)
