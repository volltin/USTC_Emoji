from __future__ import print_function

from PIL import Image, ImageDraw

# USTC logo image
LOGO_FILE = './ustcblue.jpg'

# Emoji images (if filename is "%d.*", you can add allow_range)
EMOJI_DIR = './emoji/'

# Output dir
OUTPUT_DIR = './output'

# Offset for drawing
X_OFFSET = 10
Y_OFFSET = 30

# Center circle size
R = 310

# Caches for rotated logos
ROTATED_LOGOS = {}

def draw_emoji(logo, emoji, rotation = 0):
    import math
    output = Image.new('RGB', (logo.size), (255, 255, 255))

    # Find center
    x, y = logo.size
    x += X_OFFSET
    y += Y_OFFSET
    cx, cy = x / 2, y / 2
    ex, ey = R, R
    center = (cx - ex / 2, cy - ey / 2, cx + ex / 2, cy + ey / 2)
    center = [int(i) for i in center]

    # Clear center
    draw = ImageDraw.Draw(logo)
    draw.ellipse(center, fill=(255, 255, 255))

    if rotation in ROTATED_LOGOS:
        # Take the logo from caches
        logo_canvas = ROTATED_LOGOS[rotation]
    else:
        # Set the canvas for drawing logo
        logo_canvas = Image.new('RGB', (x * 3, y * 3), (255, 255, 255))
        logo_canvas.paste(logo, (x, y))

        # Rotate logo
        r_cos, r_sin = math.cos(math.radians(rotation)), math.sin(math.radians(rotation))
        dx, dy = x + cx - r_cos * cx + r_sin * cy, y + cy - r_sin * cx - r_cos * cy
        matrix = (r_cos, -r_sin, dx, r_sin, r_cos, dy)
        logo_canvas = logo_canvas.transform((x, y), method=Image.AFFINE, data=matrix)
        ROTATED_LOGOS[rotation] = logo_canvas

    # Resize emoji
    emoji = emoji.resize((center[2] - center[0], center[3] - center[1]))

    # Draw emoji on logo
    output.paste(logo_canvas, (0, 0))
    output.paste(emoji, center, mask=emoji)
    return output

def generate_all_emoji(logo, emoji_dir, output_dir, allow_range=None, rotation_sequence=None):
    import os
    for root, dirs, files in os.walk(emoji_dir):
        i, length = 0, len(files)
        for name in files:
            i += 1
            try:
                print("Generating:", i, '/', length)
                emoji = Image.open(root + '/' + name)
                index, suffix = name.split('.')
                if allow_range and int(index) not in allow_range: continue
                output = draw_emoji(logo, emoji)
                output.save(output_dir + '/' + index + ".jpg", "JPEG",
                            quality=80, optimize=True, progressive=True)
                if rotation_sequence is not None:
                    outputs = [draw_emoji(logo, emoji, rot) for rot in rotation_sequence]
                    output.save(output_dir + '/' + index + ".gif", "GIF",
                                save_all=True, loop=0, duration=50, append_images=outputs)
            except:
                continue

if __name__ == "__main__":
    logo = Image.open(LOGO_FILE)

    rotations = range(18, 360, 18)

    generate_all_emoji(logo, EMOJI_DIR, OUTPUT_DIR, allow_range=range(700, 800), rotation_sequence=rotations)
