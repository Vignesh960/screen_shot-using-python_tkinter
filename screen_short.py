
# disable window title bar corner x click
# you need to supply your own exit button
from tkinter import *
from PIL import ImageTk, Image
import os
import datetime
import pyautogui
import matplotlib.widgets as widgets
from PIL import Image
import numpy as np

from tkinter.messagebox import showinfo
# PEP8: `import *` is not preferred
from tkinter import *
import tkinter as tk
from tkinter import messagebox
import tkinter as tk
import tkinter.ttk as ttk
import threading

import keyboard

class ProgressbarApp(threading.Thread):

    def __init__(self, max_value: int):
        self.max_value = max_value

        self.root = None
        self.pb = None

        threading.Thread.__init__(self)
        self.lock = threading.Lock()    # (1)
        self.lock.acquire()             # (2)
        self.start()

        # (1) Makes sure progressbar is fully loaded before executing anything
        with self.lock:
            return

    def close(self):
        self.root.quit()

    def run(self):

        self.root = tk.Tk()
        self.root.attributes('-disabled', True)

        self.pb = ttk.Progressbar(
            self.root, orient='horizontal', length=400, mode='determinate')
        self.pb['value'] = 0
        self.pb['maximum'] = self.max_value
        self.pb.pack()

        self.lock.release()             # (2) Will release lock when finished
        self.root.mainloop()

    def update(self, value: int):
        self.pb['value'] = value

# if __name__ == '__main__':
#     interval = 100000
#     my_pb = ProgressbarApp(interval)

#     for i in range(interval):
#         my_pb.update(i)

#     my_pb.close()

def take_bounded_screenshot(x1, y1, x2, y2):
    image = pyautogui.screenshot(region=(x1, y1, x2, y2))
    file_name = datetime.datetime.now().strftime("%f")
    os.makedirs(os.path.dirname('snips/'), exist_ok=True)
    image.save("snips/" + file_name + ".jpg")
    # image.show()
    # top = Toplevel(root)

    # im1 = ImageTk.PhotoImage(image)

    # # Add the image in the label widget
    # image1 = Label(top, image=im1)
    # image1.image = im1
    # image1.place(x=0, y=0)

class Application():
    def __init__(self, master):
        self.snip_surface = None
        self.master = master
        self.start_x = None
        self.start_y = None
        self.current_x = None
        self.current_y = None

        root.geometry('400x50+600+300')  # set new geometry
        root.title('Capture Snippet')
        root.resizable(False, False)
        icon = PhotoImage(file="icon2.png")
        root.iconphoto(False, icon)
        self.menu_frame = Frame(master)
        self.menu_frame.pack(fill=BOTH, expand=YES, padx=1, pady=1)

        self.buttonBar = Frame(self.menu_frame, bg="")
        self.buttonBar.pack()

        self.snipButton = Button(self.buttonBar, width=16, height=5,
                                 command=self.create_screen_canvas, background="light blue", text="Capture Screenshot", font=("Arial", 12), state=NORMAL)
        self.snipButton.pack()

        self.master_screen = Toplevel(root)
        self.master_screen.withdraw()
        self.master_screen.attributes("-transparent", "maroon3")
        self.picture_frame = Frame(self.master_screen, background="maroon3")
        self.picture_frame.pack(fill=BOTH, expand=YES)
        #print("iam status", self.snipButton.grab_status())

    def create_screen_canvas(self):
        self.master_screen.deiconify()
        root.withdraw()
        self.snip_surface = Canvas(
            self.picture_frame, cursor="cross", bg="grey11")
        self.snip_surface.pack(fill=BOTH, expand=YES)

        self.snip_surface.bind("<ButtonPress-1>", self.on_button_press)
        self.snip_surface.bind("<B1-Motion>", self.on_snip_drag)
        self.snip_surface.bind("<ButtonRelease-1>", self.on_button_release)

        self.master_screen.attributes('-fullscreen', True)
        self.master_screen.attributes('-alpha', .3)
        self.master_screen.lift()
        self.master_screen.attributes("-topmost", True)

    def esc_close(self):
        self.snip_surface.destroy()
        self.master_screen.withdraw()
        root.deiconify()

    def on_button_release(self, event):
        self.display_rectangle_position()

        if self.start_x <= self.current_x and self.start_y <= self.current_y:
            print("right down")
            take_bounded_screenshot(
                self.start_x, self.start_y, self.current_x - self.start_x, self.current_y - self.start_y)

        elif self.start_x >= self.current_x and self.start_y <= self.current_y:
            print("left down")
            take_bounded_screenshot(
                self.current_x, self.start_y, self.start_x - self.current_x, self.current_y - self.start_y)

        elif self.start_x <= self.current_x and self.start_y >= self.current_y:
            print("right up")
            take_bounded_screenshot(
                self.start_x, self.current_y, self.current_x - self.start_x, self.start_y - self.current_y)

        elif self.start_x >= self.current_x and self.start_y >= self.current_y:
            print("left up")
            take_bounded_screenshot(self.current_x, self.current_y,
                                    self.start_x - self.current_x, self.start_y - self.current_y)
        # elif self.start_x == None or self.current_x == None or self.start_y == None or self.current_y == None and keyboard.is_pressed("Esc"):
        #     self.snip_surface.destroy()
        #     self.master_screen.withdraw()
        #     root.deiconify()

        self.exit_screenshot_mode()
        return event

    def exit_screenshot_mode(self):
        self.snip_surface.destroy()
        self.master_screen.withdraw()
        root.deiconify()

    def on_button_press(self, event):
        # save mouse drag start position

        self.start_x = self.snip_surface.canvasx(event.x)
        self.start_y = self.snip_surface.canvasy(event.y)
        self.snip_surface.create_rectangle(
            0, 0, 1, 1, outline='red', width=3, fill="maroon3")

    def on_snip_drag(self, event):
        self.current_x, self.current_y = (event.x, event.y)
        # expand rectangle as you drag the mouse
        self.snip_surface.coords(
            1, self.start_x, self.start_y, self.current_x, self.current_y)

    def display_rectangle_position(self):
        # print(self.start_x)
        # print(self.start_y)
        # print(self.current_x)
        # print(self.current_y)
        pass

if __name__ == '__main__':
    root = Tk()
    app = Application(root)
    root.mainloop()



