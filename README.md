# Image Processing Tool

This tool processes images by adding EXIF data overlays, and can automatically detect and apply camera-specific logos based on EXIF information. It utilizes a Python script that leverages `PIL` (Python Imaging Library) and `exiftool` for image manipulation and metadata extraction.

## Project Structure

```
project_root/
├── config/
│ └── config.yaml # Configuration settings for paths and styles
├── data/
│ ├── input/ # Folder for input images
│ └── output/ # Folder for processed images
├── resources/
│ ├── logos/ # Logos for different camera brands
│ │ ├── nikon.png
│ │ ├── canon.png
│ │ └── sony.png
│ └── fonts/ # Custom fonts
│ └── Lato-Bold.ttf
├── install.sh # Installation script to setup environment
├── main.py # Main script to run the tool
└── requirements.txt # Python dependencies
```
## Configuration (`config.yaml`)

The configuration file (`config.yaml`) specifies paths and settings used by the script:

- **basic**:
  - `true/false`
  - `threads_number`
- **Image Paths:**
  - `input_folder`: Path to the folder containing images to process.
  - `output_folder`: Path where processed images will be saved.
  - `output_quality`: Quality of the output images.

- **Exiftool Path:**
  - `path`: Path to the `exiftool` executable. 
    - download from: https://www.exiftool.org/
    - e.g. `tar -xzvf Image-ExifTool-xx.xx.tar.gz`

- **Logo Settings:**
  - `options`: Dictionary mapping camera brands to their respective logo files.
  - `size`: Size to which logos should be resized.

- **Font Settings:**
  - `path`: Path to the font file.
  - `size`: Font size for text overlays.
  - `color`: Color of the text.

- **Text Settings:**
  - `padding`: Padding around text in the image.
  - `background_color`: Background color for text box.

- **Border Settings:**
  - `height`: Height of the border around the image.
  - `width`: Width of the border.
  - `color`: Color of the border.
  - `include_top`, `include_bottom`, `include_left`, `include_right`: Booleans to include borders on each side of the image.

## Setup and Installation

1. Clone the repository or download the source code.
2. Ensure Python 3 is installed on your system.
3. Run the installation script to set up the environment:

   ```bash
   ./install.sh
   ```
   
## Running the Tool

Execute the main.py script from the root of the project directory:

```bash
python main.py
```

## Contributions and Issues

Contributions are welcome via pull requests. Please file issues via GitHub's issue tracker if you encounter any problems.

## Star Growth Chart

The following chart shows the growth in stars over time for our project.
