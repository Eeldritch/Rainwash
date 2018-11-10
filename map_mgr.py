"""Handles all movement and map creation"""

def get_direction(interpret, x, y):
    """Interprets direction based on input"""
    if interpret == "N":
        y += 1
        return x, y
    if interpret == "E":
        x += 1
        return x, y
    if interpret == "S":
        y -= 1
        return x, y
    if interpret == "W":
        x -= 1
        return x, y
    else:
        return x, y
def container_coords(container_map, coords):
    """Pulls containers from the saved container map"""
    for x in container_map:
        if x == coords:
            return x

