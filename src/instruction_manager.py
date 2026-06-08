class InstructionManager:
    HOME_POS = 0
    MAG_CHANGE_POS = 1

    def __init__(self) -> None:
        pass

    def generate_instructions(self, block_stream, block_palette, mag_count):
        instructions = []
        current_mag = block_stream[0].mag_index

        for block in block_stream:
            if block.mag_index != current_mag:
                for _ in range((block.mag_index - current_mag) % mag_count):
                    instructions.append(self.MAG_CHANGE_POS)
                current_mag = block.mag_index
            instructions.append(block.lectern_index + 2)

        return instructions

    def print_instructions(self, instructions):
        for i in range(len(instructions)):
            print(instructions[i])
