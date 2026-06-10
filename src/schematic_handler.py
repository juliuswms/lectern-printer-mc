import string

import litemapy
from litemapy import TileEntity
from litemapy.minecraft import BlockState
from nbtlib.tag import Byte, Compound, Int, List, String


class SchematicHandler:
    def __init__(self, path):
        self.pattern_region = self.load_region(path)
        self.name = litemapy.Schematic.load(path).name
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
                    blocklist.append(
                        self.pattern_region.getblock(
                            int(x_region), int(z_region), int(y_region)
                        ).blockid
                    )
        return blocklist

    def get_blocks_for_row(self, row_index):
        blocks = []
        for y in range(self.pattern_region.length):
            blocks.append(
                self.pattern_region.getblock(row_index, 0, y).blockid
            )  # TODO: Check for air block
        return blocks

    def create_schematic_for_block_assigment(  # TODO: generate respecting needed block amounts
        self, block_assigment, output_path="./schematics/output"
    ):
        mags = {}
        for block_name, mapping in block_assigment.items():
            mags.setdefault(mapping.mag_index, []).append(mapping)

        for mag_index, mappings in mags.items():
            mappings.sort(key=lambda m: m.lectern_index)

            if not mappings:
                continue

            n = len(mappings)
            region = litemapy.Region(0, 0, 0, 4, 1, n)

            for i, entry in enumerate(mappings):
                z = i
                block_name = entry.block_name

                region.setblock(0, 0, z, BlockState(block_name))

                region.setblock(1, 0, z, BlockState("minecraft:shulker_box"))
                region.tile_entities.append(self._make_shulker_te(1, 0, z, block_name))

                region.setblock(
                    2,
                    0,
                    z,
                    BlockState(
                        "minecraft:chest",
                        type="left",
                        facing="north",
                        waterlogged="false",
                    ),
                )
                region.setblock(
                    3,
                    0,
                    z,
                    BlockState(
                        "minecraft:chest",
                        type="right",
                        facing="north",
                        waterlogged="false",
                    ),
                )

                region.tile_entities.append(self._make_chest_te(2, 0, z, block_name))
                region.tile_entities.append(self._make_chest_te(3, 0, z, block_name))

            schem = region.as_schematic(
                name=f"Magazine {mag_index + 1}",
                author="Map Printer",
                description=f"Blocks for magazine {mag_index + 1}",
                mc_version=4189,
            )
            schem.save(f"{output_path}_mag{mag_index + 1}.litematic")

        return 0

    def _make_te_items(self, block_name):
        items = List[Compound]([])
        for s in range(27):
            item = Compound()
            item["Slot"] = Byte(s)
            item["id"] = String(block_name)
            item["count"] = Int(64)
            items.append(item)
        return items

    def _make_container_entries(self, block_name):
        entries = List[Compound]([])
        for s in range(27):
            entry = Compound()
            entry["slot"] = Int(s)
            entry["item"] = Compound(
                {
                    "id": String(block_name),
                    "count": Int(64),
                }
            )
            entries.append(entry)
        return entries

    def _make_shulker_item(self, block_name):
        components = Compound()
        components["minecraft:container"] = self._make_container_entries(block_name)

        item = Compound()
        item["Slot"] = Byte(0)
        item["id"] = String("minecraft:shulker_box")
        item["count"] = Int(1)
        item["components"] = components
        return item

    def _make_shulker_te(self, x, y, z, block_name):
        nbt = Compound()
        nbt["id"] = String("minecraft:shulker_box")
        nbt["x"] = Int(x)
        nbt["y"] = Int(y)
        nbt["z"] = Int(z)
        nbt["Items"] = self._make_te_items(block_name)
        return TileEntity(nbt)

    def _make_chest_te(self, x, y, z, block_name):
        shulker_items = List[Compound]([])
        for s in range(27):
            item = self._make_shulker_item(block_name)
            item["Slot"] = Byte(s)
            shulker_items.append(item)

        nbt = Compound()
        nbt["id"] = String("minecraft:chest")
        nbt["x"] = Int(x)
        nbt["y"] = Int(y)
        nbt["z"] = Int(z)
        nbt["Items"] = shulker_items
        return TileEntity(nbt)
