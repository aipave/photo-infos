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
        return "Blk. Aperture"

def parse_exif_data(exif_data):
    return {
        'camera_model': exif_data.get('Model', 'Blk. Camera'),
        'lens_model': clean_text(exif_data.get('LensModel', 'Blk. Lens')),
        'datetime': exif_data.get('DateTimeOriginal', datetime.datetime.now().strftime("%Y:%m:%d %H:%M:%S")),
        'aperture': get_aperture_value(exif_data),
        'focal_length': exif_data.get('FocalLength', 'Blk. Length'),
        'exposure_time': exif_data.get('ExposureTime', 'Blk. Exposure Time'),
        'iso': exif_data.get('ISO', 'Blk.'),
        'white_balance': "Auto" if exif_data.get('WhiteBalance', 0) == 0 else "Custom",
        'gps_info': format_gps_data(exif_data)
    }

def extract_gps_lat_and_long(gps_data):
    """Extract and format GPS latitude and longitude from EXIF data."""
    latitude, longitude = gps_data
    lat = format_gps_coordinate_dms(latitude)
    lon = format_gps_coordinate_dms(longitude)
    return (lat, lon)

def format_gps_coordinate_dms(coord):
    """Convert raw GPS coordinate (tuple of tuples) to human-readable format."""
    # Assumes coordinates are in the form of ((degrees, 1), (minutes, 1), (seconds, 1))
    degrees, minutes, seconds = coord
    d = degrees[0] / degrees[1]
    m = minutes[0] / minutes[1]
    s = seconds[0] / seconds[1]
    return f"{d}°{m}'{s}\""

def format_gps_coordinate(coord):
    """ Format individual GPS coordinate based on semicolon-separated degrees, minutes, seconds. """
    degrees, minutes, seconds, direction = coord.split(';')
    formatted = f"{degrees}°{minutes}'{seconds}\"{direction}"
    return formatted

def format_gps_data(exif_data):
    """Extract and format GPS data for display from EXIF data."""
    # Try to handle a simple 'GPSPosition' string format first
    if 'GPSPosition' in exif_data:
        gps_position = exif_data['GPSPosition']
        lat, lon = gps_position.split()  # Assuming format "34;0;0N 118;0;0W"
        lat = format_gps_coordinate(lat)
        lon = format_gps_coordinate(lon)
    elif 'GPSLatitude' in exif_data and 'GPSLongitude' in exif_data:
        # Handle standard EXIF format
        lat, lon = extract_gps_lat_and_long((exif_data['GPSLatitude'], exif_data['GPSLongitude']))
    elif 'GPSAltitude' in exif_data:
        altitude_value = exif_data['GPSAltitude'].split()[0]
        return f"Alt/{altitude_value}"
    else:
        return 'Blk.'

    gps_latitude_ref = exif_data.get('GPSLatitudeRef', 'N')
    gps_longitude_ref = exif_data.get('GPSLongitudeRef', 'E')
    lat_ref = "N" if gps_latitude_ref == 'N' else "S"
    lon_ref = "E" if gps_longitude_ref == 'E' else "W"

    return f"{lat}° {lat_ref}, {lon}° {lon_ref}, Alt:{exif_data['GPSAltitude']}"


def extract_gps_lat_and_long(gps_data):
    """Extract and format GPS latitude and longitude from EXIF data."""
    latitude, longitude = gps_data
    lat = format_gps_coordinate_dms(latitude)
    lon = format_gps_coordinate_dms(longitude)
    return (lat, lon)

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
