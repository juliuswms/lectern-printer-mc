import block_mapping

class block_stream_manager:
    def __init__(self, raw_block_stream, self_assigned_palette):
        self.block_palette = self._get_palette(raw_block_stream, self_assigned_palette)
        self.block_stream = self._get_block_stream(raw_block_stream)

    def _get_palette(self, raw_block_stream, self_assigned):
        raw_palette = list(set(raw_block_stream))
        palette = []

        if len(raw_palette) > 15:
            print("Error: More than 15 unique blocks in the schematic. Please reduce the number of unique blocks to 15 or less.")
            exit(1)

        if not self_assigned:
            for i in range(len(raw_palette)):
                block = raw_palette[i]
                palette.append(block_mapping.block_mapping(block, i + 1))
            return palette
        else:
            pass # TODO: Way to assign blocks to lectern indices manually

    def _get_block_stream(self, raw_block_stream):
        block_stream = []
        for block in raw_block_stream:
            for mapping in self.block_palette:
                if mapping.block_name == block:
                    block_stream.append(mapping)
                    break
        return block_stream
        
    def get_block_at_index(self, index):
        if index < len(self.block_stream):
            return self.block_stream[index]
        else:
            print("Error getting block at index")
            return None
        
    def get_lectern_index_at_index(self, index):
        if index < len(self.block_stream):
            return self.block_stream[index].lectern_index
        else:
            print("Error getting lectern index at index")
            return None