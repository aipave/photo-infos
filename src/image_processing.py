import os
import time
import threading
from multiprocessing import Pool
from config_manager import load_config
from exif_tools import format_gps_data, get_exif_data, format_info_text
from logo_tools import get_logo_path, load_logo
from drawing_tools import prepare_image_for_drawing, draw_text_and_logo

def add_exif_info_to_image(image_path, output_path, config):
    img = prepare_image_for_drawing(image_path)
    if img is None:
        return

    exif_data = get_exif_data(config['exiftool']['path'], image_path)
    if not exif_data:
        print("No EXIF data found")
        return

    logo_size = int(min(img.width, img.height) * config['basic']['logo_size_rate']) if config['basic']['size_rate_priority'] else config['logo']['size']
    logo_path = get_logo_path(exif_data['camera_model'], config['logo']['options'])
    logo = load_logo(logo_path, logo_size)

    info_text = format_info_text(
        exif_data['camera_model'],
        exif_data['lens_model'],
        exif_data['datetime'],
        exif_data['aperture'],
        exif_data['focal_length'],
        exif_data['exposure_time'],
        exif_data['iso'],
        exif_data['white_balance'],
        exif_data['gps_info']
    )
    #print(info_text)

    final_img = draw_text_and_logo(img, info_text, logo, config)
    final_img.save(output_path, quality=config['image']['output_quality'])
    #print(f"Saved modified image with EXIF info to {output_path}")

def process_all_images(config):
    input_folder_path = config['image']['input_folder']
    output_folder_path = config['image']['output_folder']
    os.makedirs(output_folder_path, exist_ok=True)

    start_time = time.time()  # Start timing

    if config['basic'].get('use_multithreading', False):  # Default to False if not specified
        # Prepare data for multithreading
        from queue import Queue
        def worker(q):
            while True:
                data = q.get()
                if data is None:
                    break
                image_path, output_path, config = data
                add_exif_info_to_image(image_path, output_path, config)
                print(f"Processed {output_path}")
                q.task_done()

        q = Queue()
        num_threads = config['basic'].get('thread_nums', 4)  # Number of threads to use(efault to 4 if not specified)
        threads = [threading.Thread(target=worker, args=(q,)) for _ in range(num_threads)]
        for t in threads:
            t.start()

        for filename in os.listdir(input_folder_path):
            if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
                image_path = os.path.join(input_folder_path, filename)
                output_path = os.path.join(output_folder_path, "EXIF_" + filename)
                q.put((image_path, output_path, config))

        q.join()  # Wait for all tasks to be finished

        for _ in threads:
            q.put(None)  # Signal to threads to exit
        for t in threads:
            t.join()
    else:
        # Single-threaded processing
        for filename in os.listdir(input_folder_path):
            if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
                image_path = os.path.join(input_folder_path, filename)
                output_path = os.path.join(output_folder_path, "EXIF_" + filename)
                add_exif_info_to_image(image_path, output_path, config)
                print(f"Processed {output_path}")

    end_time = time.time()  # End timing
    elapsed_time = end_time - start_time
    print(f"Total processing time: {elapsed_time:.2f} seconds")
