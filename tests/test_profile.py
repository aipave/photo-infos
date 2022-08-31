import os
import sys
import cProfile

# Adjust the path to include the 'src' directory where your modules are located
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))
from config_manager import load_config
from image_processing import process_all_images

# Assuming this script is located in the .test/ directory and resources are one level up
def main():
    config = {
        'basic': {
            'use_multithreading': True,
            'thread_nums': 16
        },
        'image': {
            'input_folder': "/mnt/f/COSER/test",
            'output_folder': "/mnt/f/COSER/processed",
            'output_quality': 100
        },
        'exiftool': {
            'path': '/mnt/e/Working2/scan_code2.0/A1-photograph/semi-utils/exiftool/exiftool'
        },
        'logo': {
            'options': {
                'NIKON': '../resources/logos/nikon.png',
                'Canon': '../resources/logos/canon.png',
                'SONY': '../resources/logos/sony.png'
            },
            'size': 100
        },
        'font': {
            'path': '../resources/fonts/Lato-Bold.ttf',
            'size': 27,
            'color': '#000000'
        },
        'text': {
            'padding': 20,
            'background_color': '#FFFFFF'
        },
        'border': {
            'height': 50,
            'width': 50,
            'color': '#FFFFFF',
            'include_top': True,
            'include_bottom': True,
            'include_left': True,
            'include_right': True
        }
    }

    process_all_images(config)

if __name__ == '__main__':
    cProfile.run('main()')