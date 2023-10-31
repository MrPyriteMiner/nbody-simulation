from pathlib import Path
import numpy as np


def read_spread():
    positions = []
    velocities = []
    data = Path("F:/Schule_Temp/Matura/Momentum Test/spread.txt").read_text().split()
    data.reverse()
    while len(data) > 0:
        x = float(data.pop(-1))
        y = float(data.pop(-1))
        z = float(data.pop(-1))
        dx = float(data.pop(-1))
        dy = float(data.pop(-1))
        dz = float(data.pop(-1))
        position = [x, y, z]
        velocity = [dx, dy, dz]
        positions.append(position)
        velocities.append(velocity)
    return positions, velocities