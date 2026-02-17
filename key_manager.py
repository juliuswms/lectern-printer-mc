from pynput.keyboard import Key, Controller
import time

class keymanager:
    def __init__(self):
        self.is_homed = False
        self.last_page = 0
        self.logging = False
        self.keyboard = Controller()

    def home(self):
        self.move(Key.page_up, 15)
        self.is_homed = True
        self.last_page = 0

    def goto_page(self, page_number):
        if not self.is_homed:
            self.home()

        diff = page_number - self.last_page
        key = Key.page_down if diff > 0 else Key.page_up
        if self.logging:
            print(f"Moving to page {page_number} from {self.last_page}, diff: {diff}, key: {key}")
        if diff != 0:
            self.move(key, abs(diff))
        else:
            self.trigger()
        self.last_page = page_number
    
    def trigger(self):
        self.keyboard.tap(Key.page_down)
        time.sleep(0.1)
        self.keyboard.tap(Key.page_up)

    def move(self, key, count):
        for _ in range(count):
            start_time = time.time() * 1000
            self.keyboard.tap(key)
            time.sleep(0.1)
            if self.logging:
                print(f"Pressing {key} took {time.time() * 1000 - start_time} ms")
