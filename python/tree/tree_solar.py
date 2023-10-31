import numpy as np
import math
import pygame
import matplotlib.pyplot as plt
from pathlib import Path
import time as timer
from body_maker import make_tree_spread
from spread_reader_special import read_spread

threshold = 2**2
timescale = 1
ts_factor = 2**-36
smallest_distance = 2**62


def dist(b1, b2):
    connector = b2.position - b1.position
    distance = math.sqrt(connector.dot(connector))
    if distance == 0:
        raise RuntimeError("Distance between bodies was 0...", b2.position, b1.position, connector, distance)
    return distance, connector


def abs_dist(p1, p2):
    connector = p2 - p1
    distance = (connector.dot(connector))**0.5
    return distance, connector


class Node:
    def __init__(self, position, bodies, depth, size):
        self.bodies = bodies
        self.position = position
        self.depth = depth
        self.size = size
        center_of_mass = np.array((0., 0., 0.))
        total_mass = 0
        if len(self.bodies) > 0:
            for body in self.bodies:
                center_of_mass += body.mass * body.position
                total_mass += body.mass
            center_of_mass /= total_mass
            self.mass = total_mass
            self.center_of_mass = center_of_mass
            if len(self.bodies) > 1:
                self.children = []
                partition = self.partition()
                if self.depth > 100:
                    raise RuntimeError("Depth limit exceeded.")
                for i in range(8):
                    pos = self.position - np.array((self.size/4, self.size/4, self.size/4))
                    if i % 2 == 1:
                        pos += np.array((self.size/2, 0., 0.))
                    if i % 4 == 2 or i % 4 == 3:
                        pos += np.array((0., self.size/2, 0.))
                    if i >= 4:
                        pos += np.array((0., 0., self.size/2))
                    new_node = Node(pos, partition[i], self.depth+1, self.size/2)
                    self.children.append(new_node)

    def partition(self):
        partitioned_list = [[], [], [], [], [], [], [], []]
        for body in self.bodies:
            index = 0
            if body.position[0] > self.position[0]:
                index += 1
            if body.position[1] > self.position[1]:
                index += 2
            if body.position[2] > self.position[2]:
                index += 4
            partitioned_list[index].append(body)
        return partitioned_list

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

    def step(self):
        global timescale
        global smallest_distance
        smallest_distance = 2**62
        for body in self.bodies:
            body.acceleration = self.get_acceleration(body)
        distance_threshold = 10**3
        timescale = 1*((smallest_distance/distance_threshold)**2)
        for body in self.bodies:
            body.velocity += body.acceleration * timescale * ts_factor
            body.position += body.velocity * timescale * ts_factor

    def get_acceleration(self, body):
        global smallest_distance
        if len(self.bodies) == 0:
            return np.zeros(3)
        acceleration_sum = np.zeros(3)
        distance, connector = abs_dist(self.center_of_mass, body.position)
        if len(self.bodies) == 1:
            if self.bodies[0] == body:
                return np.zeros(3)
            if distance < smallest_distance:
                smallest_distance = distance
            return -G * self.mass * connector / (distance**3)
        ratio = distance / self.size
        if ratio < threshold:
            for child in self.children:
                acceleration_sum += child.get_acceleration(body)
            return acceleration_sum
        if distance < smallest_distance:
            smallest_distance = distance
        return -G * self.mass * connector / (distance**3)  # maybe add counter for how many operations saved by adding len(self.bodies)-1 to some counter?


class Body:
    def __init__(self):
        self.position = np.array((0., 0., 0.))
        self.velocity = np.array((0., 0., 0.))
        self.mass = 10**14
        self.acceleration = np.array((0., 0., 0.))
        self.color = (255, 0, 0)


def draw(sim):
    surface = pygame.display.set_mode((WIDTH, HEIGHT))
    center = [0, 0, 0]
    scaling = 1.2*10**9
    for x in sim.bodies:
        pygame.draw.circle(surface, x.color,
                           (x.position[0]/scaling+HEIGHT/2-center[0]/scaling,
                            x.position[1]/scaling+WIDTH/2-center[1]/scaling),
                           abs(x.mass**(1/13)/30)+1)
    pygame.display.update()


def get_size(bodies):  # makes sure all bodies are within a node
    max_x, max_y, max_z = bodies[0].position
    min_x, min_y, min_z = max_y, max_y, max_z
    for body in bodies:
        min_x = min(min_x, body.position[0])
        max_x = max(max_x, body.position[0])
        min_y = min(min_y, body.position[1])
        max_y = max(max_y, body.position[1])
        min_z = min(min_z, body.position[2])
        max_z = max(max_z, body.position[2])
    size = max(max_z - min_z, max_y - min_y, max_y - min_x)
    position = [(max_x + min_x)/2, (max_y + min_y)/2, (max_z + min_z)/2]
    return size+1, position  # + 1 just to make sure it's *really* inside it and not just on an edge --> avoids edge case


def make_bodies(number_of_bodies):
    body_list = []
    for i in range(number_of_bodies):
        x = Body()
        x.position = np.array((160*i-80, 0., 0.))
        x.velocity = np.array((0., 6*i-3, 0.))
        body_list.append(x)
    for body in body_list:
        print(body.position)
    return body_list


def make_bodies_using_maker(param1=0, param2=0, param3=0, param4=0):
    positions, velocities, masses, colors = read_spread(param1, param2)
    body_list = []
    for i in range(len(positions)):
        x = Body()
        x.position = np.array(positions[i])
        x.velocity = np.array(velocities[i])
        x.mass = masses[i]
        x.color = colors[i]
        body_list.append(x)
    return body_list


if __name__ == "__main__":
    G = (6.6743*10**-11)
    HEIGHT = 900
    WIDTH = 900
    kinetic_energy_list = []
    potential_energy_list = []
    total_energy_list = []
    momentum_list = []
    total_time = 10**7.6
    stepcount = 0
    time = 0
    last_time = 0
    bodi_es = make_bodies_using_maker("spread.txt", False)
    bodi_es += make_bodies_using_maker("spread3.txt", True)
    size1, pos1 = get_size(bodi_es)
    verse = Node(bodies=bodi_es, position=np.array(pos1), depth=0, size=size1)
    start = timer.time()
    draw(verse)
    while time < total_time:
        size1, pos1 = get_size(verse.bodies)
        stepcount += 1
        verse = Node(bodies=verse.bodies, position=np.array(pos1), size=size1, depth=0)
        verse.step()
        time += timescale * ts_factor
        if stepcount % (1) == 0:
            draw(verse)
        if time > last_time + total_time/1000:
            last_time = time
            pot, kin = verse.energy()
            kinetic_energy_list += [kin]
            potential_energy_list += [pot]
            total_energy_list += [kin+pot]
            current_momentum = verse.momentum()
            momentum_list += [current_momentum]
            print(str(math.floor(time * 1000/total_time)/10) + "%")
    end = timer.time()
    print(f"{end - start} seconds")
    helper_array = np.arange(len(kinetic_energy_list))
    kinetic_energy_array = np.array(kinetic_energy_list)
    potential_energy_array = np.array(potential_energy_list)
    total_energy_array = np.array(total_energy_list)
    momentum_array = np.array(momentum_list)
    mini = min(total_energy_array)
    total_delta_energy = total_energy_array - mini
    with open("delta.txt", "w") as file:
        for val in total_delta_energy:
            file.write(f"{val} ")
    print(len(total_energy_array), len(momentum_array), len(kinetic_energy_array), len(potential_energy_array), len(helper_array))
    print(max(total_delta_energy) - min(total_delta_energy))
    print(f"{(max(total_delta_energy) - min(total_delta_energy)) * 100 / max(total_energy_array)} % loss")
    x = []
    y = []
    z = []
    for i in range(len(momentum_array)):
        arr = momentum_array[i]
        x.append(arr[0])
        y.append(arr[1])
        z.append(arr[2])
    mx = min(x)
    my = min(y)
    mz = min(z)
    x -= mx
    y -= my
    z -= mz
    if mx == 0:
        mx = 2**-62
    if my == 0:
        my = 2**-62
    if mz == 0:
        mz = 2**-62
    print(f"x: {max(x)*100/mx}% loss; y: {max(y)*100/my}% loss; z: {max(z)*100/mz}% loss")
    plt.plot(helper_array, kinetic_energy_array)
    plt.plot(helper_array, potential_energy_array)
    plt.plot(helper_array, total_energy_array)
    plt.show()
    plt.plot(helper_array, momentum_array)
    plt.show()
    plt.plot(helper_array, total_energy_array)
    plt.show()
    plt.plot(helper_array, total_delta_energy)
    plt.show()
    plt.plot(x)
    plt.show()
    plt.plot(y)
    plt.show()
    plt.plot(z)
    plt.show()
