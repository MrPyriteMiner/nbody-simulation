from .body import Body
from .. import config
import math
import numpy as np


def f_g(m1, xyz1, m2, xyz2):  # Force of Gravity
    delta_r = xyz2 - xyz1  # calculates vector between the two
    d = magnitude(delta_r)
    force = m1*m2*config.G*delta_r/(d**3)  # calculates the force of gravity between the two objects
    return force


def magnitude(vector):
    return math.sqrt(vector.dot(vector))


def distance(v1, v2):
    v = v2-v1
    return magnitude(v)


def a_g(body1, body2):  # acceleration --> just calls the force function and divides by the mass
    acceleration = f_g(body1.mass, body1.position, body2.mass, body2.position)/body1.mass
    return acceleration


class Universe:
    def __init__(self, generate_bodies=False, bodies=[], time=0, stepcount=0):
        self.bodies = bodies
        self.time = time
        self.stepcount = stepcount
        if generate_bodies is True:
            self.generate_bodies()

    def generate_bodies(self):
        for i in range(config.body_count):
            temp_body = Body()
            self.bodies += [temp_body]

    def energy(self):
        gravitational_potential_energy = 0
        kinetic_energy = 0
        for x in self.bodies:
            for y in self.bodies:
                if x != y:
                    e = config.G*x.mass*y.mass/distance(x.position, y.position)
                    gravitational_potential_energy += e
        for x in self.bodies:
            e = 0.5*x.mass*(magnitude(x.velocity)**2)
            kinetic_energy += e
        return -0.5*gravitational_potential_energy, kinetic_energy

    def momentum(self):
        total_momentum = np.array((0., 0., 0.))
        for x in self.bodies:
            total_momentum += x.mass * x.velocity
        return total_momentum

    def step(self):
        timescale = config.timescale
        for x in self.bodies:
            for y in self.bodies:
                dist = distance(x.position, y.position)
                if x != y and dist < config.distance_threshold*timescale:
                    timescale = (dist/config.distance_threshold)**config.timescale_exponent
        for body in self.bodies:
            body.acceleration = np.array((0., 0., 0.))
            for b in self.bodies:
                if b != body:
                    body.acceleration += a_g(body, b)
        for body in self.bodies:
            body.position += body.velocity * 0.5 * timescale
            body.velocity += body.acceleration * timescale
            body.position += body.velocity * 0.5 * timescale
        self.stepcount += 1
        self.time += timescale  # counter for time passed
        self.stepcount += 1  # counter for how many times this function has been run


if __name__ == "__main__":
    print("This Program shouldn't be run as the main program, it's meant to be imported.")
    print("Since you ran this anyway, though, it will run some tests on the class")
    bod = Body()
    print(bod.position)
    print(bod.velocity)
    print(bod.mass)
