from time import sleep

import block_stream_manager
import instruction_manager
import key_manager
import schematic_handler

SCHEMATIC_PATH = "./schematics/test-prints/saulgoodman3d.litematic"

if __name__ == "__main__":
    key_manager = key_manager.KeyManager()
    schematic = schematic_handler.SchematicHandler(SCHEMATIC_PATH)
    block_stream_manager = block_stream_manager.BlockStreamManager(
        schematic.blocklist, False
    )
    block_stream_manager.print_assignment()
    block_palette = block_stream_manager.block_palette
    instruction_manager = instruction_manager.InstructionManager()
    instructions = instruction_manager.generate_instructions(
        block_stream_manager.block_stream,
        block_stream_manager.block_palette,
        block_stream_manager.MAG_COUNT,
    )
    print(f"{len(instructions)} instructions")
    print(f"{len(schematic.blocklist)} blocks to print")
    print(f"{len(instructions) - len(schematic.blocklist)} mag changes")
    schematic.create_schematic_for_block_assigment(block_stream_manager.block_palette)
    sleep(3)
    key_manager.type_intructions(schematic.name, 0, "10,10", "2", instructions)
