from pathlib import Path
import numpy as np


def read_spread(name, has_name=False):
    positions = []
    velocities = []
    masses = []
    colors = []
    data = Path(f"F:/Schule_Temp/Matura/Momentum Test/inner_planets/{name}").read_text().split()
    data.reverse()
    while len(data) > 0:
        if has_name is True:
            data.pop(-1)
        x = float(data.pop(-1))
        y = float(data.pop(-1))
        z = float(data.pop(-1))
        dx = float(data.pop(-1))
        dy = float(data.pop(-1))
        dz = float(data.pop(-1))
        mass = float(data.pop(-1))
        color1 = float(data.pop(-1))
        color2 = float(data.pop(-1))
        color3 = float(data.pop(-1))
        color = (color1, color2, color3)
        position = [x, y, z]
        velocity = [dx, dy, dz]
        positions.append(position)
        velocities.append(velocity)
        masses.append(mass)
        colors.append(color)
    return positions, velocities, masses, colors
