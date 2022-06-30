import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from config_manager import load_config
from image_processing import process_all_images

def main():
    config = load_config('./config/config.yaml')
    process_all_images(config)

if __name__ == "__main__":
    main()