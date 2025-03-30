# utils/coordinate_utils.py
import math

def haversine_distance(coord1, coord2):
    """Returns distance in meters between two (lat, lon) pairs."""
    from haversine import haversine, Unit
    return haversine(coord1, coord2, unit=Unit.METERS)
