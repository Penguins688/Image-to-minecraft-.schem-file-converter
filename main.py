import json
from nbt import nbt
from PIL import Image
from colormath.color_objects import sRGBColor, LabColor
from colormath.color_diff import delta_e_cie1976
from colormath.color_conversions import convert_color

with open("block_lab.json", "r") as f:
    block_lab_data = json.load(f)

block_lab = {block: LabColor(*vals) for block, vals in block_lab_data.items()}

def closest_block(rgb):
    """Find the closest block to a given RGB using LAB delta_e."""
    r, g, b = rgb
    lab1 = convert_color(sRGBColor(r/255, g/255, b/255, is_upscaled=False), LabColor)
    best_block = None
    best_dist = float("inf")
    for block, lab2 in block_lab.items():
        dist = delta_e_cie1976(lab1, lab2)
        if dist < best_dist:
            best_dist = dist
            best_block = block
    return best_block

def region_rms(im, x0, z0, block_size):
    """Compute RMS RGB of a block region starting at (x0, z0)."""
    pixels = [
        im.getpixel((x, z))
        for z in range(z0, min(z0 + block_size, im.height))
        for x in range(x0, min(x0 + block_size, im.width))
    ]
    n = len(pixels)
    if n == 0:
        return (0, 0, 0)
    r_rms = (sum(r**2 for r, _, _ in pixels) / n) ** 0.5
    g_rms = (sum(g**2 for _, g, _ in pixels) / n) ** 0.5
    b_rms = (sum(b**2 for _, _, b in pixels) / n) ** 0.5
    return (r_rms, g_rms, b_rms)

def image_to_schem(img_path, out_file="monalisa.schem", block_size=1):
    """Convert an image to a Minecraft schematic using RMS color per block region."""
    im = Image.open(img_path).convert("RGB")
    width, height = im.size

    nbtfile = nbt.NBTFile()
    nbtfile.name = "Schematic"

    nbtfile.tags.append(nbt.TAG_Int(name="Version", value=2))
    nbtfile.tags.append(nbt.TAG_Int(name="DataVersion", value=3105)) 
    nbtfile.tags.append(nbt.TAG_Short(name="Width", value=width // block_size))
    nbtfile.tags.append(nbt.TAG_Short(name="Height", value=1))
    nbtfile.tags.append(nbt.TAG_Short(name="Length", value=height // block_size))

    palette = nbt.TAG_Compound(name="Palette")
    palette_blocks = []
    palette_set = set()
    blockdata_list = []

    for z0 in range(0, height, block_size):
        for x0 in range(0, width, block_size):
            rgb = region_rms(im, x0, z0, block_size)
            closest = closest_block(rgb)

            if closest not in palette_set:
                palette_blocks.append(closest)
                palette_set.add(closest)
                palette[f"minecraft:{closest}"] = nbt.TAG_Int(len(palette_blocks) - 1)

            blockdata_list.append(palette_blocks.index(closest))

    nbtfile.tags.append(nbt.TAG_Int(name="PaletteMax", value=len(palette_blocks)))
    nbtfile.tags.append(palette)

    blockdata = nbt.TAG_Byte_Array(name="BlockData")
    blockdata.value = bytearray(blockdata_list)
    nbtfile.tags.append(blockdata)

    block_entities = nbt.TAG_List(name="BlockEntities", type=nbt.TAG_Compound)
    nbtfile.tags.append(block_entities)

    nbtfile.write_file(out_file)
    print(f"Saved {out_file}")

image_to_schem("image.png", block_size=1)