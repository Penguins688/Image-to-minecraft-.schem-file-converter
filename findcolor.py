import json
from colormath.color_objects import sRGBColor, LabColor
from colormath.color_conversions import convert_color

block_colors = {
    "emerald_block": (34,181,115),
    "diamond_block": (93,217,217),
    "gold_block": (242,193,77),
    "iron_block": (200,200,200),
    "copper_block": (184,115,51),
    "redstone_block": (208,0,0),
    "lapis_block": (29,59,139),
    "netherite_block": (60,60,60),
    "stone": (125,125,125),
    "deepslate": (74,79,82),
    "quartz_block": (237,230,223),
    "obsidian": (26,15,43),
    "prismarine": (93,175,157),
    "dark_prismarine": (46,107,98),
    "sea_lantern": (221,246,244),
    "grass_block": (78,139,61),
    "sand": (227,217,166),
    "red_sand": (201,110,61),
    "ice": (174,227,245),
    "amethyst_block": (153,102,204),
    "sandstone": (255,232,194),
    "jungle_wood": (138,75,40),
    "acacia_wood": (199,127,74),
    "dark_oak_wood": (46,27,15),
    "pink_wool": (242,139,178),
    "black_wool": (29,29,29),
    "yellow_wool": (255,215,0),
    "cyan_wool": (0,206,209),
    "gray_wool": (112,128,144),
    "orange_wool": (255,69,0),
    "end_stone": (255,250,205),
    "pink_concrete": (255,209,220),
    "light_blue_concrete": (135,206,250),
    "lime_concrete": (144,238,144),
    "nether_brick": (139,0,0),
    "netherrack": (178,34,34),
    "moss_block": (85,107,47),
    "purple_concrete": (128,0,128),
    "magenta_wool": (218,112,214),
    "brown_wool": (160,82,45),
    "white_wool": (245,245,220),
    "blue_wool": (25,25,112),
    "carved_pumpkin": (255,165,0),
    "terracotta": (255,218,185),
    "andesite": (167,167,167),
    "diorite": (225,225,225),
    "granite": (194,126,106),
    "packed_ice": (176,224,230),
    "blue_ice": (173,216,230),
    "melon": (152,251,152),
    "sea_pickle": (127,255,212),
    "brick_block": (205,92,92),
    "birch_planks": (245,222,179),
    "spruce_planks": (139,69,19),
    "mangrove_planks": (210,105,30),
    "bamboo_mosaic": (124,252,0),
    "cherry_planks": (255,192,203),
    "hay_bale": (238,232,170),
    "bone_block": (255,255,224),
    "basalt": (75,78,87),
    "blackstone": (43,46,49),
    "glowstone": (251,245,208),
    "polished_deepslate": (112,128,144),
    "mud": (143,151,121),
    "podzol": (123,63,0),
    "polished_granite": (188,143,143),
    "stone_bricks": (158,158,158)
}

block_lab = {}
for block, (r,g,b) in block_colors.items():
    lab = convert_color(sRGBColor(r/255,g/255,b/255), LabColor)
    block_lab[block] = [lab.lab_l, lab.lab_a, lab.lab_b]

with open("block_lab.json", "w") as f:
    json.dump(block_lab, f, indent=4)

print("Saved block_lab.json")