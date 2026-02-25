import block_mapping

class block_stream_manager:
    def __init__(self, raw_block_stream, self_assigned_palette):
        self.block_palette = self._get_palette(raw_block_stream, self_assigned_palette)
        self.block_stream = self._get_block_stream(raw_block_stream)

    def _get_palette(self, raw_block_stream, self_assigned):
        raw_palette = list(set(raw_block_stream))
        if(len(raw_palette) > (self.MAX_MAG_SIZE * self.MAG_COUNT)): raise Exception(f"More block types then slots available ({self.MAX_MAG_SIZE * self.MAG_COUNT})")
        change_matrix = self._get_change_matrix(raw_block_stream, raw_palette)        



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
        
    def remove_block_at_index(self, index):
        if index < len(self.block_stream):
            self.block_stream.pop(index)
        else:
            print("Error removing block at index")

    def _get_change_matrix(raw_block_stream, raw_palette):
        last_block = raw_block_stream[0]
    
        block_type_index_dict = {t: i for i, t in enumerate(raw_palette)}
    
        n = len(raw_palette)
    
        change_matrix = [[0 for _ in range(n)] for _ in range(n)]
    
        for i in range(1, len(raw_block_stream)):
            curr = raw_block_stream[i]
            if last_block == curr:
                continue
            
            prev_idx = block_type_index_dict[last_block]
            curr_idx = block_type_index_dict[curr]
            change_matrix[prev_idx][curr_idx] += 1
    
            last_block = curr
    
        return change_matrix
