import pygetwindow as gw
import time
import keymanager

# Placeholder block list (you can replace this with the actual block data later)
# Each tuple represents (block_name, page_number, count)
block_list = [
    ("red", 2, 3),  # 3 red blocks from page 2
    ("blue", 5, 1),  # 1 blue block from page 5
    ("white", 10, 1),  # 1 white block from page 10
    ("black", 3, 5)   # 59999999999 black blocks from page 3
]

if __name__ == "__main__":
    time.sleep(3)
    key_mgr = keymanager.key_manager(is_homed=False, last_page=1)
    key_mgr.goto_page(15)
    time.sleep(1)
    key_mgr.goto_page(1)
    time.sleep(1)
    key_mgr.trigger()
    time.sleep(1)
    key_mgr.goto_page(2)
    time.sleep(1)

