import random
import numpy as np
import math
import decimal


ctx = decimal.Context()

ctx.prec = 30


def make_belt(amount, tilt_range=0., eccentricity_range=0.):
    G = 6.6743 * 10 ** -11
    sun_mass = 1988500000000000000000000000000
    positions = []
    velocities = []
    masses = []
    r_range = (308170000000, 489190000000)
    while len(masses) < amount:
        r = random.randrange(r_range[0], r_range[1])
        theta = random.randrange(0, 628)/100
        a = G * sun_mass / r**2
        x = r * math.cos(theta)
        y = r * math.sin(theta)
        z = 0.
        position = [x, y, z]
        abort = False
        print(len(masses))
        for pos in positions:
            dist = np.array(pos) - np.array(position)
            dist = dist.dot(dist)
            if dist < (9000000000000/amount)**2:
                print("aborted")
                abort = True
        if abort is False:
            eccentricity = random.randrange(0, 1_000_000)
            eccentricity = eccentricity_range*(1-(abs(eccentricity)**(1/2)/1000))  # makes distribution of eccentricities more realistic
            multiplier = 1/(1-eccentricity)
            print(multiplier, "multiplier")
            print(eccentricity, "eccentricity")
            phi = random.randrange(-1_000_000, 1_000_000)
            phi = np.sign(phi)*(tilt_range*(1-abs(phi)**(1/2)/1000))  # makes distribution of tilts more realistic
            print(phi, "phi")
            dr = math.sqrt(a*r)*multiplier
            dx = dr*math.cos(theta-math.pi/2)
            dy = dr*math.sin(theta-math.pi/2)
            dz = 0
            # Apply tilt now
            dz = dr*math.sin(phi)
            dx *= math.cos(phi)
            dy *= math.cos(phi)
            velocity = [dx, dy, dz]
            velocities.append(velocity)
            positions.append(position)
            mass = random.randrange(1, 1000)
            mass = 11 - mass**(1/3)
            mass = 10**(mass+7)
            masses.append(mass)
    return positions, velocities, masses


if __name__ == "__main__":
    how_many = 300
    pos_list, vel_list, mass_list = make_belt(how_many, 2*math.pi/45, 0.0)
    with open("spread5.txt", "w") as file:
        for i in range(how_many):
            mass = ctx.create_decimal(repr(mass_list[i]))
            mass = format(mass, 'f')
            file.write(f"Asteroid: {pos_list[i][0]} {pos_list[i][1]} {pos_list[i][2]} {vel_list[i][0]} {vel_list[i][1]} {vel_list[i][2]} {mass} 100 100 100\n")
        # file.write("0 0 0 0 0 0 1988500000000000000000000000000 255 255 0")
