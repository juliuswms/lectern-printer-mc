import pydirectinput
import threading
import time

class key_manager:
    is_homed = False
    last_page = 0
    #pydirectinput.calibrate_real_sleep_minimum(runs=10, verbose=True)
    pydirectinput.PAUSE = None
    pydirectinput.MINIMUM_SLEEP_IDEAL = 1e-06

    def __init__(self, is_homed=False, last_page=0):
        self.is_homed = is_homed
        self.last_page = last_page

    def home(self):
        print("homing...")
        pydirectinput.press('pageup', presses=15, interval=0, delay=0, duration=0, _pause=False)
        self.is_homed = True
        self.last_page = 0
    
    def goto_page(self, page_number):
        if not self.is_homed:
            self.home()
        print("going to page: ", page_number)
        def thread_task(direction):
            print(direction)
            if direction:
                pydirectinput.press('pagedown', interval=0, delay=0, duration=0, _pause=False)
            else:
                pydirectinput.press('pageup', interval=0, delay=0, duration=0, _pause=False)
        if page_number > self.last_page:
            #pydirectinput.press('pagedown', presses=page_number - self.last_page, interval=0, delay=0, duration=0, _pause=False)
            threads = [threading.Thread(target=thread_task(True)) for _ in range(page_number - self.last_page)]

            for thread in threads:
                thread.start()
                #time.sleep(0.001)

            for thread in threads:
                thread.join()
        else:
            #pydirectinput.press('pageup', presses=self.last_page - page_number, interval=0, delay=0, duration=0, _pause=False)
            threads = [threading.Thread(target=thread_task(False)) for _ in range(self.last_page - page_number)]

            for thread in threads:
                thread.start()

            for thread in threads:
                thread.join()
        self.last_page = page_number

    

    def trigger(self):
        pydirectinput.press('pageup', interval=0, delay=0, duration=0, _pause=False)
        pydirectinput.press('pagedown', interval=0, delay=0, duration=0, _pause=False)