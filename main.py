from time import sleep
import threading
import multiprocessing

import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

from pynput.mouse import Controller, Button
from pynput.keyboard import Listener, Key, KeyCode

DELAY = 1.5
mouse = Controller()


class AutoClicker:
    def __init__(self, process_s, thread_s, ):
        self.delay = DELAY
        self.clicking = False
        self.process_enable = process_s
        self.thread_enable = thread_s
        self.TOGGLE_KEY = [{Key.shift, KeyCode(char='k')},
                           {Key.shift, KeyCode(char='K')}]
        self.current = set()
        print(self.process_enable, self.thread_enable)

    def clicker(self):
        while bool(self.thread_enable.value):  # CHECK FOR ENABLE
            if self.clicking:
                print('Clicking is true')
                mouse.click(Button.left, 1)
                sleep(self.delay)
            else:
                print('Clicking is not true')
                sleep(self.delay)
        else:
            print("clicker thread killed!")

    def on_press(self, key):
        if any([key in TOGGLE_KEYS for TOGGLE_KEYS in self.TOGGLE_KEY]):
            self.current.add(key)
            if any(all(k in self.current for k in TOGGLE_KEYS) for TOGGLE_KEYS in self.TOGGLE_KEY):
                if bool(self.thread_enable.value):  # REDUNDANT CHECK FOR ENABLE
                    self.clicking = not self.clicking
                else:
                    return False
        # if self.clicking:
        #     self.stat_proxy.set("AutoClicker is on")
        #
        # else:
        #     self.stat_proxy.set("AutoClicker is off, Press [k] to toggle")

    def on_release(self, key):
        if any([key in TOGGLE_KEYS for TOGGLE_KEYS in self.TOGGLE_KEY]):
            self.current.remove(key)

    def start_thread(self):
        print("Starting clicker thread")
        clicker_thread = threading.Thread(target=self.clicker)
        clicker_thread.start()

        print("Starting listener thread")
        with Listener(on_press=self.on_press, on_release=self.on_release) as self.listener:
            while bool(self.thread_enable.value) is True:  # CHECK FOR ENABLE
                pass
            else:
                self.listener.stop()  # Stop listener thread
            self.listener.join()
        print("Listener thread killed!")
        # End of process
        print("Process was killed")


def run_autoclicker():
    sleep(0.1)
    """Main function to handle Run button"""
    if process_status.value == 1:  # Checks for process state
        print("Killing process")
        thread_status.value = 0  # Stops clicker and listener thread
        process_status.value = 0
        tk_status.set("Autoclicker [Disabled]")
    else:
        print("Starting process")
        process_status.value = 1
        thread_status.value = 1

        auto_clicker_obj = AutoClicker(process_status, thread_status)
        # Autoclicker process to handle Listener and Clicker
        p1 = multiprocessing.Process(target=auto_clicker_obj.start_thread)
        p1.start()

        tk_status.set("Autoclicker [Enabled]")


def validate_time(time_delay):
    """Function for time validation"""
    global DELAY
    try:
        time_delay = float(time_delay)
        if time_delay > 0.1:
            DELAY = time_delay
            tk_status.set(f"Time delay set to {time_delay} sec(s)")
        else:
            tk_status.set(f"Time delay should be > 0.1")

    except ValueError:
        tk_status.set(f"Invalid Time Delay")


def on_closing():
    """Runs when window closes"""
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        if bool(process_status.value):
            print("Forcibly closing thread")
            thread_status.value = int(False)
            process_status.value = int(False)
        print("Closing Window")
        window.destroy()


if __name__ == "__main__":
    multiprocessing.freeze_support()
    process_status = multiprocessing.Value(
        'i', int(False))  # To access from different process
    thread_status = multiprocessing.Value(
        'i', int(False))  # To access from different process

    window = tk.Tk()

    # Variable string to update labels
    tk_delay = tk.StringVar()
    tk_status = tk.StringVar()

    tk_delay.set(str(DELAY))
    tk_status.set(f"Time delay set to {tk_delay.get()} sec(s)")

    # status_proxy, status_proxyListener = proxy.createProxy(tk_status)
    # status_proxyListener.listen()

    window.title('AutoClicker')
    window.geometry("400x300")
    window.resizable(False, False)

    style = ttk.Style()

    # Label and string_var to display status and delay settings
    ttk.Label(window, text="Status:", style='TLabel').place(x=30, y=30)
    ttk.Label(window, textvariable=tk_status,
              style='TLabel').place(x=110, y=30)

    ttk.Label(window, text="Time delay(sec):",
              style='TLabel').place(x=40, y=100)
    ttk.Entry(window, textvariable=tk_delay, font=(
        'calibre', 15, 'normal'), width=8, ).place(x=220, y=100)
    # Submit button
    ttk.Button(window, text="Submit", style='TButton', width=8, command=lambda: validate_time(tk_delay.get())) \
        .place(x=220, y=150)
    # Run
    ttk.Button(window, text="Listener", style='TButton', width=8, command=run_autoclicker) \
        .place(x=290, y=250)

    style.configure('TButton', font=(None, 15))
    style.configure('TLabel', font=(None, 15))

    # Close event
    window.protocol('WM_DELETE_WINDOW', on_closing)
    window.mainloop()
