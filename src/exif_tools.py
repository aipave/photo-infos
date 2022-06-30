import subprocess
import json
import datetime
from utils import clean_text
from logo_tools import get_logo_path

def get_exif_data(exiftool_path, image_path):
    command = [exiftool_path, '-j', image_path]
    result = subprocess.run(command, stdout=subprocess.PIPE, text=True)
    exif_data = json.loads(result.stdout)[0] if result.stdout else {}
    return parse_exif_data(exif_data)

def get_aperture_value(exif_data):
    f_number = exif_data.get('FNumber')
    if isinstance(f_number, tuple) and len(f_number) == 2:
        # Calculate the FNumber if it's in a tuple form (numerator, denominator)
        return f"f/{f_number[0]/f_number[1]:.1f}"
    elif isinstance(f_number, (float, int)):
        # Directly use the FNumber if it's a float or an int
        return f"f/{f_number:.1f}"
    else:
        return "Unknown Aperture"

def parse_exif_data(exif_data):
    return {
        'camera_model': exif_data.get('Model', 'Unknown Camera'),
        'lens_model': clean_text(exif_data.get('LensModel', 'Unknown Lens')),
        'datetime': exif_data.get('DateTimeOriginal', datetime.datetime.now().strftime("%Y:%m:%d %H:%M:%S")),
        'aperture': get_aperture_value(exif_data),
        'focal_length': exif_data.get('FocalLength', 'Unknown Focal Length'),
        'exposure_time': exif_data.get('ExposureTime', 'Unknown Exposure Time'),
        'iso': exif_data.get('ISO', 'Unknown ISO'),
        'white_balance': "Auto" if exif_data.get('WhiteBalance', 0) == 0 else "Custom",
        'gps_info': format_gps_data(exif_data)
    }

def format_gps_data(exif_data):
    """Extract and format GPS data for display from EXIF data."""
    gps_latitude = exif_data.get('GPSLatitude')
    gps_longitude = exif_data.get('GPSLongitude')
    gps_latitude_ref = exif_data.get('GPSLatitudeRef')
    gps_longitude_ref = exif_data.get('GPSLongitudeRef')

    if gps_latitude and gps_longitude and gps_latitude_ref and gps_longitude_ref:
        # Convert coordinates to degrees, minutes, seconds format
        def convert_to_degrees(value):
            """Convert GPS coordinates to a human-readable degree format."""
            d, m, s = value
            return d + (m / 60.0) + (s / 3600.0)

        lat = convert_to_degrees(gps_latitude)
        lon = convert_to_degrees(gps_longitude)
        lat_ref = "N" if gps_latitude_ref == 'N' else "S"
        lon_ref = "E" if gps_longitude_ref == 'E' else "W"

        return f"{lat}° {lat_ref}, {lon}° {lon_ref}"
    return "No GPS Data Available"

def format_info_text(camera_model, lens_model, datetime, aperture, focal_length, exposure_time, iso, white_balance, gps_info):
    """
    Formats the provided EXIF data into a readable string.

    :param camera_model: Camera model from EXIF data.
    :param lens_model: Lens model from EXIF data.
    :param datetime: Date and time the photo was taken from EXIF data.
    :param aperture: Aperture value from EXIF data.
    :param focal_length: Focal length from EXIF data.
    :param exposure_time: Exposure time from EXIF data.
    :param iso: ISO value from EXIF data.
    :param white_balance: White balance setting from EXIF data.
    :param gps_info: GPS information formatted from EXIF data.
    :return: Formatted string of all EXIF information.
    """
    return f"{camera_model} + {lens_model}\n{focal_length} {aperture} " \
           f"{exposure_time}s  ISO-{iso}\nWhite Balance: {white_balance}, " \
           f"Date: {datetime}, GPS: {gps_info}"
