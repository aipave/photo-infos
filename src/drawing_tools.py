from PIL import Image, ImageDraw, ImageFont, ImageOps

def prepare_image_for_drawing(img_path):
    try:
        img = Image.open(img_path)
        img = ImageOps.exif_transpose(img)
        return img
    except IOError:
        print(f"Error: Cannot open {img_path}. It may not be a valid image file.")
        return None

def draw_text_and_logo(img, info_text, logo, config):
    font_path = config['font']['path']
    font_size = config['font']['size']

    text_padding = config['text']['padding']
    logo_padding = config['logo']['padding']

    border_height = config['border']['height']
    border_width = config['border']['width']

    if config['basic']['size_rate_priority']:
        # Calculate dynamic sizes based on the image dimensions
        logo_padding = int(min(img.width, img.height) * config['basic']['logo_padding_size_rate'])
        text_padding = int(min(img.width, img.height) * config['basic']['text_padding_size_rate'])

        font_size = int(min(img.width, img.height) * config['basic']['font_size_rate'])

        border_height = int(min(img.width, img.height) * config['basic']['border_size_rate'])
        border_width = int(min(img.width, img.height) * config['basic']['border_size_rate'])

    draw = ImageDraw.Draw(img)
    try:
        font = ImageFont.truetype(font_path, font_size)
    except IOError:
        font = ImageFont.load_default()
        print("Failed to load custom font. Using default font.")

    # Measure text size
    bbox = draw.textbbox((0, 0), info_text, font=font)
    text_width, text_height = bbox[2] - bbox[0], bbox[3] - bbox[1]

    # Calculate border height based on the text and logo
    special_border_height = max(text_height, logo.height if logo else 0) + border_height

    # Calculate extra dimensions for borders
    extra_width = (config['border']['include_left'] + config['border']['include_right']) * border_width
    extra_height = (config['border']['include_top'] * border_height) + special_border_height

    # Create a new image to accommodate borders
    new_img = Image.new('RGB', (img.width + extra_width, img.height + extra_height), 'white')
    paste_position = (config['border']['include_left'] * border_width, config['border']['include_top'] * border_height)

    # Paste the original image into the new image
    new_img.paste(img, paste_position)

    # Logo and text positioning
    logo_x = paste_position[0] + logo_padding
    logo_y = img.height + paste_position[1] + (special_border_height - logo.height) // 2 if logo else 0
    text_x = logo_x + (logo.width + text_padding if logo else 0)
    text_y = img.height + paste_position[1] + (special_border_height - text_height) // 2

    # Draw logo if available
    if logo:
        new_img.paste(logo, (logo_x, logo_y), logo.split()[3] if logo.mode == 'RGBA' else None)

    # Draw text
    draw = ImageDraw.Draw(new_img)
    draw.text((text_x, text_y), info_text, font=font, fill='black')

    return new_img
