import json
import math
import os
import subprocess
import time


class KeyManager:
    MAX_PAGE_CHARS = 1023
    INPUT_DELAY = 0.001
    CHAR_MAPPING_FILEPATH = os.path.join(
        os.path.dirname(__file__), "..", "char-mapping.json"
    )

    def __init__(self):
        self.is_homed = False
        self.last_page = 0
        self.logging = False
        with open(self.CHAR_MAPPING_FILEPATH) as f:
            self._mapping = json.load(f)

    # TODO: reimplement script-based printing

    def type_instructions(
        self,
        print_name,
        print_est,
        print_delays,
        print_pause_delay,
        instructions,
        book=0,
    ):
        self._paste_string(
            f"name={print_name}\nest={print_est}\ndelays={print_delays}\npdelay={print_pause_delay}\nbook={book}"
        )

        time.sleep(0.1)
        num_pages = math.ceil(len(instructions) / self.MAX_PAGE_CHARS)
        if book > num_pages / 99:
            raise Exception(
                f"Book requested is out of range. Book: {book} was requested but {math.ceil(num_pages / 99)} are needed."
            )
        subprocess.run(["ydotool", "key", "109:1", "109:0"])
        time.sleep(2)
        start_page = (book + 1) * 99
        for start_page in range(num_pages):
            page_string = ""
            start = start_page * self.MAX_PAGE_CHARS
            end = min(start + self.MAX_PAGE_CHARS, len(instructions))
            for idx in range(start, end):
                page_string += self._int_to_char(instructions[idx])
            self._paste_string(page_string)
            time.sleep(0.09)
            subprocess.run(["ydotool", "key", "109:1", "109:0"])
            time.sleep(0.09)

    def _int_to_char(self, num):
        return self._mapping[num]

    def _paste_string(self, text):
        subprocess.run(["wl-copy"], input=text.encode("utf-8"))
        time.sleep(0.03)
        subprocess.run(["ydotool", "key", "29:1", "47:1", "47:0", "29:0"])  # Ctrl+V
