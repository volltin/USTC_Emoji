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

def draw_emoji(logo, emoji):
    output = Image.new('RGBA', (logo.size), (0, 0, 0, 0))

    # Find center
    x, y = logo.size
    x += X_OFFSET
    y += Y_OFFSET
    eX, eY = R, R
    center = (x/2 - eX/2, y/2 - eY/2, x/2 + eX/2, y/2 + eY/2)
    center = [int(i) for i in center]

    # Clear center
    draw = ImageDraw.Draw(logo)
    draw.ellipse(center, fill = (255, 255, 255))

    # Resize emoji
    emoji = emoji.resize((center[2] - center[0], center[3] - center[1]))

    # Draw emoji on logo
    output.paste(logo, (0,0))
    output.paste(emoji, center, mask=emoji)
    return output

def generate_all_emoji(logo, emoji_dir, output_dir, allow_range = None):
    import os
    for root, dirs, files in os.walk(emoji_dir):
        for name in files:
            try:
                emoji = Image.open(root + '/' + name)
                index, suffix = name.split('.')
                if allow_range and int(index) not in allow_range:
                    continue
                output = draw_emoji(logo, emoji)
                output.save(output_dir + '/' + index + ".jpg", "JPEG", quality=80, optimize=True, progressive=True)
            except:
                continue

if __name__ == "__main__":
    logo = Image.open(LOGO_FILE)

    generate_all_emoji(logo, EMOJI_DIR, OUTPUT_DIR, allow_range = range(700, 800))

