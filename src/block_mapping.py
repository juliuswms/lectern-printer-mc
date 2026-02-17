class block_mapping:
    def __init__(self, block_name, lectern_index):
        self.block_name = block_name
        self.lectern_index = lectern_index

    def print(self):
        print(f"Block: {self.block_name}, Lectern Index: {self.lectern_index}")