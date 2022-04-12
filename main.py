
"""
the next libraries are used for
drawing a rectangle over the screen,
taking a screenshot,
doing the ocr over the image, 
and sending the text to the clipboard.
"""
from webbrowser import get
import pyautogui
import time
import pyperclip
import pytesseract
from PIL import Image
import win32gui, win32api, win32con
from win32api import GetSystemMetrics
import os
"""
these are some parameters for the rectangle
"""
m=win32gui.GetCursorPos()
dc = win32gui.GetDC(0)
red = win32api.RGB(255, 0, 0) # Red

"""
the next method will draw a selection rectangle
over the screen when the user presses the print screen
key, which will follow the mouse movement, then when the user
presses the left mouse button, the screenshot will be taken. 
"""
def listen_for_keypress():
    while True:
        if win32api.GetAsyncKeyState(win32con.VK_SNAPSHOT):#print screen key
            m=win32gui.GetCursorPos()
            x1, y1 = pyautogui.position()
            while True:
                n=win32gui.GetCursorPos()
                time.sleep(0.1)
                win32gui.InvalidateRect(0,None,True)#refresh screen
                #back=[]
                for i in range((n[0]-m[0])//4):
                    win32gui.SetPixel(dc, m[0]+4*i, m[1], red)
                    win32gui.SetPixel(dc, m[0]+4*i, n[1], red)
                for i in range((n[1]-m[1])//4):
                    win32gui.SetPixel(dc, m[0], m[1]+4*i, red)
                    win32gui.SetPixel(dc, n[0], m[1]+4*i, red)

                if win32api.GetAsyncKeyState(win32con.VK_LBUTTON):#left mouse button
                    x2, y2 = pyautogui.position()
                    """
                    the next code will swap the x1 and x2 values if x1 is greater than x2
                    and the same for y1 and y2.
                    """
                    if x1 > x2:
                        x1, x2 = x2, x1
                    if y1 > y2:
                        y1, y2 = y2, y1
        
                    take_screenshot(x1, y1, x2, y2)
                    break

"""
the next method will check if screenshot folder exists,
if not, it will create it.
"""
def create_folder():
    if not os.path.exists("screenshots"):
        os.makedirs("screenshots")
"""
the next method will save the screenshot using 4 coordinates
and will save it inside a local  folder named screenshots
with the current time and will do the ocr over the image
and will send the text to the clipboard.
"""
def take_screenshot(x1, y1, x2, y2):
    create_folder()
    current_time = time.strftime("%H-%M-%S")
    try:
        pyautogui.screenshot("screenshots/" + 'screenshot' + current_time + ".png", region=(x1, y1, x2 - x1, y2 - y1))
        image = Image.open("screenshots/" + 'screenshot' + current_time + ".png")
        pytesseract.pytesseract.tesseract_cmd = r'.\redist\tesseract.exe'
        text = pytesseract.image_to_string(image)
        pyperclip.copy(text)   
    except:
        pass
     

"""
this is the main execution of the program, surrounded by a try and except
"""
try:
    listen_for_keypress()
except:
    pass


