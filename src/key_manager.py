import math
import time

INPUT_DELAY = 0.001


class KeyManager:
    def __init__(self):
        from pynput.keyboard import Controller, Key

        self.is_homed = False
        self.last_page = 0
        self.logging = False
        self.keyboard = Controller()
        self.Key = Key

    def home(self):
        self.move(self.Key.page_up, 15)
        self.is_homed = True
        self.last_page = 0

    def goto_page(self, page_number):
        if not self.is_homed:
            self.home()

        diff = page_number - self.last_page
        key = self.Key.page_down if diff > 0 else self.Key.page_up
        if self.logging:
            print(
                f"Moving to page {page_number} from {self.last_page}, diff: {diff}, key: {key}"
            )
        if diff != 0:
            self.move(key, abs(diff))
        else:
            self.trigger()
        self.last_page = page_number

    def trigger(self):
        self.keyboard.tap(self.Key.page_down)
        time.sleep(INPUT_DELAY)
        self.keyboard.tap(self.Key.page_up)

    def move(self, key, count):
        for _ in range(count):
            start_time = time.time() * 1000
            self.keyboard.tap(key)
            time.sleep(INPUT_DELAY)
            if self.logging:
                print(f"Pressing {key} took {time.time() * 1000 - start_time} ms")

    def type_intructions(self, instructions, max_page_chars=266):
        self.keyboard.type("name=test")
        self.keyboard.tap(self.Key.enter)
        self.keyboard.type("est=100")
        self.keyboard.tap(self.Key.enter)
        self.keyboard.type("delays=10,10")
        self.keyboard.tap(self.Key.enter)
        self.keyboard.type("pdelay=2")
        self.keyboard.tap(self.Key.page_down)

        num_pages = math.ceil(len(instructions) / max_page_chars)
        for i in range(num_pages):
            page_string = ""
            start = i * max_page_chars
            end = min(start + max_page_chars, len(instructions))
            for idx in range(start, end):
                page_string += self._int_to_hex(instructions[idx])
            self.keyboard.type(page_string)
            self.keyboard.tap(self.Key.page_down)

    def _int_to_hex(self, num):
        if num >= 0 and num <= 9:
            return f"{num}"
        if num == 10:
            return "A"
        if num == 11:
            return "B"
        if num == 12:
            return "C"
        if num == 13:
            return "D"
        if num == 14:
            return "E"
        if num == 15:
            return "F"

        return "X"
