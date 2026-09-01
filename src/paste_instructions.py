import argparse
import math
from time import sleep

import block_stream_manager
import instruction_manager
import key_manager
import schematic_handler

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--Path", help="Path to the schematic")
    parser.add_argument(
        "-m",
        "--Mag_Count",
        help="Number of mags that are used in the Lectern Printer (1-based Index)",
        default=4,
    )
    parser.add_argument(
        "--Seed",
        type=int,
        default=None,
        help="Add a seed to make generation deterministic. Usefull while testing",
    )
    parser.add_argument(
        "-pd",
        "--Pause_delay",
        type=int,
        default=2,
        help="Delay between instructions and going back to home",
    )  # TODO: Rename to instruction delay
    parser.add_argument(
        "-d",
        "--Delays",
        default="10,10",
        help="Delay between going to home and the next instruction",
    )  # TODO: Rename to pause delay
    parser.add_argument(
        "-b",
        "--Book",
        type=int,
        default=None,
        help="Adjust which book is printed if more then one is needed. ONLY USE WHEN ALSO SETING --Seed",
    )
    args = parser.parse_args()

    if args.Path:
        schematic = schematic_handler.SchematicHandler(args.Path)
    else:
        raise Exception("No Path to schematic. Use -p or --Path.")
    km = key_manager.KeyManager()
    bsm = block_stream_manager.BlockStreamManager(
        schematic.blocklist, mag_count=int(args.Mag_Count), seed=args.Seed
    )
    bsm.print_assignment()
    block_palette = bsm.block_palette
    im = instruction_manager.InstructionManager()
    instructions = im.generate_instructions(
        bsm.block_stream,
        bsm.block_palette,
        bsm.MAG_COUNT,
    )
    print(f"{len(instructions)} instructions")
    print(f"{len(schematic.blocklist)} blocks to print")
    print(f"{len(instructions) - len(schematic.blocklist)} mag changes")
    schematic.create_schematic_for_block_assignment(bsm.block_palette)
    print(
        f"Print is starting at mag index (0-based): {bsm.block_stream[0].mag_index}"
    )
    block_count = len(schematic.blocklist)
    mag_changes = len(instructions) - len(schematic.blocklist)
    est_gt = (
        (block_count * 10) + (block_count * 2) + (mag_changes * 4) + (mag_changes * 20)
    )
    print(f"Estimated print time: {est_gt}gt's ({est_gt / 20 / 60}min) ({est_gt / 20 / 60 / 60}h)")
    print("Press any key to start 3 second countdown till instructions are pasted")
    input()
    sleep(3)
    if args.Book:
        km.type_instructions(
            schematic.name,
            est_gt,
            args.Delays,
            args.Pause_delay,
            instructions,
            book=args.Book,
        )
    else:
        num_pages = math.ceil(len(instructions) / km.MAX_PAGE_CHARS)
        total_num_of_books = math.ceil(num_pages / 99)
        for i in range(total_num_of_books):
            km.type_instructions(
                schematic.name,
                est_gt,
                args.Delays,
                args.Pause_delay,
                instructions,
                book=i,
            )
            if i == total_num_of_books - 1:
                break
            print("Press enter to print next book")
            input()
            sleep(3)
