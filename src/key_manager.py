import json
import math
import os
import time

from pynput.keyboard import Controller, Key


class KeyManager:
    INPUT_DELAY = 0.001
    CHAR_MAPPING_FILEPATH = os.path.join(
        os.path.dirname(__file__), "..", "char-mapping.json"
    )

    def __init__(self):
        self.is_homed = False
        self.last_page = 0
        self.logging = False
        self.keyboard = Controller()
        self.Key = Key
        with open(self.CHAR_MAPPING_FILEPATH) as f:
            self._mapping = json.load(f)

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
        time.sleep(self.INPUT_DELAY)
        self.keyboard.tap(self.Key.page_up)

    def move(self, key, count):
        for _ in range(count):
            start_time = time.time() * 1000
            self.keyboard.tap(key)
            time.sleep(self.INPUT_DELAY)
            if self.logging:
                print(f"Pressing {key} took {time.time() * 1000 - start_time} ms")

    def type_intructions(
        self,
        print_name,
        print_est,
        print_delays,
        print_pause_delay,
        instructions,
        max_page_chars=1023,
    ):
        self.keyboard.type(f"name={print_name}")
        self.keyboard.tap(self.Key.enter)
        self.keyboard.type(f"est={print_est}")
        self.keyboard.tap(self.Key.enter)
        self.keyboard.type(f"delays={print_delays}")
        self.keyboard.tap(self.Key.enter)
        self.keyboard.type(f"pdelay={print_pause_delay}")
        self.keyboard.tap(self.Key.enter)
        self.keyboard.tap(self.Key.page_down)

        num_pages = math.ceil(len(instructions) / max_page_chars)
        time.sleep(0.2)
        for i in range(num_pages):
            page_string = ""
            start = i * max_page_chars
            end = min(start + max_page_chars, len(instructions))
            for idx in range(start, end):
                page_string += self._int_to_char(instructions[idx])
            self.keyboard.type(page_string)
            time.sleep(0.2)
            self.keyboard.tap(self.Key.page_down)
            time.sleep(0.05)

    def _int_to_char(self, num):
        return self._mapping[num]
