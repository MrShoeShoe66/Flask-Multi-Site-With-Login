from threading import Thread
import os

def start_api():
    os.system('python files/api.py')

def start_web():
    os.system('python files/web.py')

def start_status():
    os.system('python files/status.py')

api = Thread(target=start_api)

web = Thread(target=start_web)

status = Thread(target=start_status)

api.start()

web.start()

status.start()