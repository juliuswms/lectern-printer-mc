import key_manager
from time import sleep
keyboard_manager = key_manager.keymanager()
keyboard_manager.logging = True
while True:
    index = int(input("Enter page index: "))
    sleep(1)
    keyboard_manager.goto_page(index)