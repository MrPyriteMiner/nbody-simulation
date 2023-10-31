import numpy as np
import math
import pygame
import matplotlib.pyplot as plt

ts_factor = 1


def dist(b1, b2):
    connector = b2.position - b1.position
    distance = math.sqrt(connector.dot(connector))
    if distance == 0:
        raise RuntimeError("Distance between bodies was 0...", b2.position, b1.position, connector, distance)
    return distance, connector


class Body:
    def __init__(self):
        self.position = np.array((0, 0, 0))
        self.velocity = np.array((0, 0, 0))
        self.mass = 10**10
        self.acceleration = np.array((0, 0, 0))


class Universe:
    def __init__(self):
        body_list = []
        for i in range(2):
            x = Body()
            body_list.append(x)
            body_list[i].position = np.array((0., i*100, 0.))
            body_list[i].velocity = np.array((10*(i-1), 0., 0.))
        body_list[0].velocity = np.array((4, 0.5, 0.))
        self.bodies = body_list
        self.time = 0
        self.stepcount = 0
        self.timescale = 1

    def step(self):
        self.set_timescale()
        for body in self.bodies:
            body.acceleration = np.array((0., 0., 0.))
            for b in self.bodies:
                if b != body:
                    distance, connector = dist(body, b)
                    body.acceleration += b.mass * G * connector / (distance**3)
        for body in self.bodies:
            body.velocity += body.acceleration * self.timescale*ts_factor
            body.position += body.velocity * self.timescale*ts_factor
        self.stepcount += 1
        self.time += self.timescale*ts_factor

    def set_timescale(self):
        distance_threshold = 10**3
        minimum_distance = distance_threshold
        for body in self.bodies:
            for b in self.bodies:
                if b != body:
                    distance = dist(b, body)[0]
                    if distance < minimum_distance:
                        minimum_distance = distance
        self.timescale = 1*((minimum_distance/distance_threshold)**2)

    def energy(self):
        gravitational_energy = 0
        kinetic_energy = 0
        for body in self.bodies:
            for b in self.bodies:
                if body != b:
                    distance = dist(body, b)
                    gravitational_energy -= b.mass * body.mass * G / distance[0]
            kinetic_energy += 0.5 * body.mass * body.velocity.dot(body.velocity)
        return 0.5*gravitational_energy, kinetic_energy

    def momentum(self):
        total_momentum = np.array((0., 0., 0.))
        for body in self.bodies:
            total_momentum += body.velocity * body.mass
        return total_momentum


def draw(sim):
    surface = pygame.display.set_mode((WIDTH, HEIGHT))
    center = [0, 0, 0]
    scaling = 1
    for x in sim.bodies:
        color = (255, 0, 0)
        pygame.draw.circle(surface, color,
                           (x.position[0]/scaling+HEIGHT/2-center[0]/scaling,
                            x.position[1]/scaling+WIDTH/2-center[1]/scaling),
                           abs(x.mass**(1/3))/scaling/300)
    pygame.display.update()


if __name__ == "__main__":
    G = (6.6743*10**-11)/(10**-4)
    HEIGHT = 900
    WIDTH = 900
    verse = Universe()
    kinetic_energy_list = []
    potential_energy_list = []
    total_energy_list = []
    momentum_list = []
    total_stepcount = 15
    while verse.time < total_stepcount:
        verse.step()
        print(verse.time)
        if verse.stepcount % (50*4) == 0:
            draw(verse)
        pot, kin = verse.energy()
        kinetic_energy_list += [kin]
        potential_energy_list += [pot]
        total_energy_list += [kin + pot]
        current_momentum = verse.momentum()
        momentum_list += [current_momentum]
        if verse.time % (math.floor(total_stepcount)/100) == 0:
            print(str(math.floor(verse.stepcount * 100/total_stepcount)) + "%")
    helper_array = np.arange(len(kinetic_energy_list))
    kinetic_energy_array = np.array(kinetic_energy_list)
    potential_energy_array = np.array(potential_energy_list)
    total_energy_array = np.array(total_energy_list)
    momentum_array = np.array(momentum_list)
    print(len(total_energy_array), len(momentum_array), len(kinetic_energy_array), len(potential_energy_array), len(helper_array))
    # plt.plot(helper_array, kinetic_energy_array)
    # plt.plot(helper_array, potential_energy_array)
    # plt.plot(helper_array, total_energy_array)
    # plt.show()
    # plt.plot(helper_array, momentum_array)
    # plt.show()

    if len(total_energy_list) > 1000:
        while len(total_energy_list) % 1000 != 0:
            total_energy_list.pop(-1)
            kinetic_energy_list.pop(-1)
            potential_energy_list.pop(-1)
            momentum_list.pop(-1)
    length = max(int(len(total_energy_list)/1000), 1)
    array_12 = np.array(total_energy_list[::length])
    array_1 = np.array(kinetic_energy_list[::length])
    array_2 = np.array(potential_energy_list[::length])
    array_momentum = np.array(momentum_list[::length])
    array_helper = []
    print(length)
    for i in range(len(array_12)):
        array_helper += [i * 10]
    array_numbering = np.array(array_helper)
    plt.plot(array_numbering, array_12, label="Total Energy")
    plt.plot(array_numbering, array_1, label="Kinetic Energy")
    plt.plot(array_numbering, array_2, label="Potential Energy")
    plt.show()
    plt.plot(array_numbering, array_momentum, label="Momentum")
    plt.show()
    plt.plot(array_numbering, array_12)
    plt.show()
    array_12 -= min(array_12)
    plt.plot(array_12)
    plt.show()

