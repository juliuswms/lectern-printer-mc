import litemapy

class schematic_handler:
    def __init__(self, path):
        self.pattern_region = self.load_region(path)
        self.width = self.pattern_region.width
        self.height = self.pattern_region.height
        self.length = self.pattern_region.length
        self.blocklist = self._get_blocklist()

    def load_region(self, file_path):
        return list(litemapy.Schematic.load(file_path).regions.values())[0]

    def _get_blocklist(self):
        blocklist = []

        for x in range(abs(self.width)):
            for z in range(abs(self.height)):
                for y in range(abs(self.length) - 1, -1, -1):
                    x_region = (self.width / abs(self.width)) * x
                    z_region = (self.height / abs(self.height)) * z
                    y_region = (self.length / abs(self.length)) * y
                    blocklist.append(self.pattern_region.getblock(int(x_region), int(z_region), int(y_region)).blockid)
        return blocklist

    def get_blocks_for_row(self, row_index):
        blocks = []
        for y in range(self.pattern_region.length):
            blocks.append(self.pattern_region.getblock(row_index, 0, y).blockid) # TODO: Check for air block
        return blocks