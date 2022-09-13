import os
from PIL import Image

def get_logo_path(camera_model, logo_config):
    camera_model = camera_model.lower()
    for brand, path in logo_config.items():
        if brand.lower() in camera_model:
            return path
    return logo_config['Default']

def load_logo(logo_path, logo_size):
    if logo_path is None or not os.path.exists(logo_path):
        print(f"Warning: Logo path is not provided or does not exist: {logo_path}")
        return None

    try:
        logo = Image.open(logo_path)
        logo.thumbnail((logo_size, logo_size), Image.LANCZOS)
        return logo
    except IOError as e:
        print(f"Unable to open or read logo file at {logo_path}: {e}")
        return None
