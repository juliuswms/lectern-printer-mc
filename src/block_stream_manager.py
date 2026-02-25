import block_mapping

class block_stream_manager:
    # 1-based-index
    MAX_MAG_SIZE = 12
    MAG_COUNT = 4

    def __init__(self, raw_block_stream, self_assigned_palette):
        self.block_palette = self._get_palette(raw_block_stream, self_assigned_palette)
        self.block_stream = self._get_block_stream(raw_block_stream)

    def _get_palette(self, raw_block_stream, self_assigned):
        raw_palette = list(set(raw_block_stream))
        if(len(raw_palette) > (self.MAX_MAG_SIZE * self.MAG_COUNT)): raise Exception(f"More block types then slots available ({self.MAX_MAG_SIZE * self.MAG_COUNT})")
        change_matrix = self._get_change_matrix(raw_block_stream, raw_palette)        
        total_type_changes = self._get_total_type_changes()
        block_assignment = self._get_block_assignment_dict(raw_palette)
        cost = self._get_assignment_cost(change_matrix, block_assignment, raw_palette)
        print(cost)

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

    def _get_change_matrix(self, raw_block_stream, raw_palette):
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
    
    def _get_block_assignment_dict(self, block_types):
        block_dict = {}
        current_mag_index = 0
        current_lectern_index = 0 

        for type in block_types:
            block_dict[type] = current_mag_index
            current_lectern_index += 1

            if current_lectern_index == self.MAX_MAG_SIZE - 1: 
                current_lectern_index = 0
                current_mag_index += 1

        return block_dict

    def _get_assignment_cost(self, change_matrix, block_assignment_dict, block_types):
        cost = 0
        for i in range(len(change_matrix)):
            for j in range(len(change_matrix[0])):
                if change_matrix[i][j] == 0: continue
                i_mag_pos = block_assignment_dict[block_types[i]]
                j_mag_pos = block_assignment_dict[block_types[j]]
                cost += (i_mag_pos - j_mag_pos) % self.MAG_COUNT

        return cost

    def _get_total_type_changes(change_matrix, block_types):
        type_changes = []
        for i in range(len(change_matrix[0])):
            for j in range(len(change_matrix[0])):
                type_changes[i] += change_matrix[i][j]

        return type_changes