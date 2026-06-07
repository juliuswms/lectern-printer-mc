from time import sleep

import block_stream_manager as bsm
import key_manager as km
import schematic_handler as sh

# white = 1
# light gray = 2
# dark gray = 3
# black = 4
# brown = 5
# red = 6
# orange = 7
# yellow = 8
# light green = 9
# green = 10
# cyan = 11
# light blue = 12
# blue = 13
# purple = 14
# pink = 15

SCHEMATIC_PATH = "./schematics/test-prints/saulgoodman3d.litematic"

if __name__ == "__main__":
    keyboard_manager = km.KeyManager()
    schematic = sh.SchematicHandler(SCHEMATIC_PATH)
    block_stream_manager = bsm.BlockStreamManager(schematic.blocklist, False)
    print(
        f"Width: {schematic.width}, Height: {schematic.height}, Length: {schematic.length}"
    )

    print(
        f"Goto index: {block_stream_manager.get_lectern_index_at_index(0)} for block: {block_stream_manager.get_block_at_index(0).block_name}"
    )
    input("Press Enter to start printing...")
    for block in block_stream_manager.block_stream:
        print(block)
    keyboard_manager.is_homed = True
    keyboard_manager.last_page = block_stream_manager.get_lectern_index_at_index(0)
    sleep(2)
    block_stream_manager.remove_block_at_index(0)
    for block in block_stream_manager.block_stream:
        print(f"Printing: {block.block_name} with Lectern-Index {block.lectern_index}")
        keyboard_manager.goto_page(block.lectern_index)
        sleep(0.35)
