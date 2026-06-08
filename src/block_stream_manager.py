import math
import random

import block_mapping


class BlockStreamManager:
    MAX_MAG_SIZE = 14  # 0 based index
    MAG_COUNT = 4  # 1 based index

    # raw_block_stream is the blocks that will be placed on after eatch other
    # self_assigned_palette determens if the block palette is already set or if it should minimize the mag
    def __init__(self, raw_block_stream, self_assigned_palette):
        self.raw_palette = self._get_palette(raw_block_stream, self_assigned_palette)

        change_matrix = self._get_change_matrix(raw_block_stream, self.raw_palette)
        block_assignment = self._get_block_assignment_dict(self.raw_palette)
        self.block_palette = self._optimize_block_assignment(
            block_assignment, change_matrix, self.raw_palette
        )
        self.block_stream = self._get_block_stream(raw_block_stream)

    # TODO: add functunalety for non self_assined block streams
    def _get_palette(self, raw_block_stream, self_assigned):
        raw_palette = list(set(raw_block_stream))
        if len(raw_palette) > (self.MAX_MAG_SIZE * self.MAG_COUNT):
            raise Exception(
                f"More block types then slots available ({self.MAX_MAG_SIZE * self.MAG_COUNT})"
            )
        return raw_palette

    def _get_block_stream(self, raw_block_stream):
        block_stream = []
        for block in raw_block_stream:
            if block in self.block_palette:
                block_stream.append(self.block_palette[block])
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

    def print_assignment(self):
        mags = {i: [] for i in range(self.MAG_COUNT)}
        for block_name, mapping in self.block_palette.items():
            mags[mapping.mag_index].append(mapping)

        for mag_idx in range(self.MAG_COUNT):
            print(f"--- Magazine {mag_idx + 1} ---")
            for m in sorted(mags[mag_idx], key=lambda x: x.lectern_index):
                print(f"  Slot {m.lectern_index + 1:2d}: {m.block_name}")
        print()

    def _get_change_matrix(self, raw_block_stream, pallet):
        last_block = raw_block_stream[0]

        block_type_index_dict = {t: i for i, t in enumerate(pallet)}

        n = len(pallet)

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
            block_dict[type] = block_mapping.BlockMapping(
                type, current_lectern_index, current_mag_index
            )
            current_lectern_index += 1

            if current_lectern_index == self.MAX_MAG_SIZE - 1:
                current_lectern_index = 0
                current_mag_index += 1

        return block_dict

    def _get_assignment_cost(self, change_matrix, block_assignment_dict, block_types):
        cost = 0
        for i in range(len(change_matrix)):
            for j in range(len(change_matrix[0])):
                if change_matrix[i][j] == 0:
                    continue
                i_mag_pos = block_assignment_dict[block_types[i]].mag_index
                j_mag_pos = block_assignment_dict[block_types[j]].mag_index
                steps = (j_mag_pos - i_mag_pos) % self.MAG_COUNT
                cost += change_matrix[i][j] * steps
        return cost

    def _get_total_type_changes(self, change_matrix, block_types):
        type_changes = [0] * len(change_matrix)
        for i in range(len(change_matrix)):
            for j in range(len(change_matrix[0])):
                type_changes[i] += change_matrix[i][j]
        return type_changes

    def _random_swap_in_block_assignment(self, block_assignment):
        new_assignment = {}
        for k, m in block_assignment.items():
            new_assignment[k] = block_mapping.BlockMapping(
                m.block_name, m.lectern_index, m.mag_index
            )

        keys = list(new_assignment.keys())

        a_key = random.choice(keys)
        a_mag = new_assignment[a_key].mag_index

        candidates = [k for k in keys if new_assignment[k].mag_index != a_mag]
        b_key = random.choice(candidates)

        a_map = new_assignment[a_key]
        b_map = new_assignment[b_key]
        a_map.mag_index, b_map.mag_index = b_map.mag_index, a_map.mag_index
        a_map.lectern_index, b_map.lectern_index = (
            b_map.lectern_index,
            a_map.lectern_index,
        )
        return new_assignment

    def _optimize_block_assignment(
        self, block_assignment, change_matrix, raw_palette, max_iterations=50000
    ):
        current_assignemt = block_assignment
        current_cost = self._get_assignment_cost(
            change_matrix, block_assignment, raw_palette
        )
        best_assignment = current_assignemt
        best_cost = current_cost

        T = 100.0
        T_min = 0.0001
        alpha = 0.9999

        iteration = 0
        while T > T_min and iteration < max_iterations:
            candidat = self._random_swap_in_block_assignment(current_assignemt)
            candidat_cost = self._get_assignment_cost(
                change_matrix, candidat, raw_palette
            )
            delta = candidat_cost - current_cost

            if delta <= 0 or random.random() < math.exp(-delta / T):
                current_assignemt = candidat
                current_cost = candidat_cost
                if current_cost < best_cost:
                    best_assignment = current_assignemt
                    best_cost = current_cost
                    print(f"Best cost: {best_cost} at {iteration}")

            T *= alpha
            iteration += 1

        return best_assignment
