import numpy as np
import random
from .. import config


class Body:
    def __init__(self, mass=0, position=0, velocity=0):  # values 0 for random
        if type(position) not in (int, list) or type(velocity) not in (int, list) or type(mass) != int:
            raise RuntimeError('Invalid input for body generation')
        if type(position) == int:
            if not position == 0:
                raise RuntimeError('non-zero integer inputted for position generation')
            x = random.randrange(config.position_range[0][0], config.position_range[0][1])
            y = random.randrange(config.position_range[1][0], config.position_range[1][1])
            z = random.randrange(config.position_range[2][0], config.position_range[2][1])
            position = [float(x), float(y), float(z)]
        if type(velocity) == int:
            if not velocity == 0:
                raise RuntimeError('non-zero integer inputted for velocity generation')
            x = random.randrange(config.velocity_range[0][0], config.velocity_range[0][1])
            y = random.randrange(config.velocity_range[1][0], config.velocity_range[1][1])
            z = random.randrange(config.velocity_range[2][0], config.velocity_range[2][1])
            velocity = [float(x), float(y), float(z)]
        if mass == 0:
            mass = random.randrange(config.mass_range[0], config.mass_range[1])
        self.position = np.array(position)
        self.velocity = np.array(velocity)
        self.mass = mass

    def properties(self):
        x = "mass:\t\t" + str(self.mass) + "\nposition\t" + str(self.position) + "\nveloctiy\t" + str(self.velocity)
        return x


if __name__ == "__main__":
    print("This Program shouldn't be run as the main program, it's meant to be imported.")
    print("Since you ran this anyway, though, it will run some tests on the class")
    body = Body()
    print(body.position)
    print(body.velocity)
    print(body.mass)
