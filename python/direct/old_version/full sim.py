import numpy as np
from utility.objects.body import Body
from utility.objects.universe import *
from utility import config
import pygame
import time
import sys
import matplotlib.pyplot as plt


def draw(sim):
    surface = pygame.display.set_mode((config.WIDTH, config.HEIGHT))
    scaling = config.scaling_default
    color_scaling = config.color_scaling_default
    center = [0, 0, 0]
    if config.do_centering is True:
        new_center = np.array((0, 0, 0))
        for x in sim.bodies:
            new_center = new_center + x.position
        new_center = new_center/len(sim.bodies)
        center = new_center
    if config.do_scaling is True:
        for x in sim.bodies:
            if abs(x.position[0]-center[0])/scaling > config.scaling_border*config.WIDTH/2:
                scaling = abs(x.position[0]-center[0])/(config.scaling_border*config.WIDTH/2)
            if abs(x.position[1]-center[1])/scaling > config.scaling_border*config.WIDTH/2:
                scaling = abs(x.position[1]-center[1])/(config.scaling_border*config.WIDTH/2)
    if config.do_color_scaling is True:
        for x in sim.bodies:
            if abs(x.position[2]-center[2])/color_scaling > 127:
                color_scaling = abs(x.position[2]-center[2])/127

    for x in sim.bodies:
        z_pos = (x.position[2]-center[0])/math.sqrt(abs(x.position[2]))  # takes negative root of z coordinate
        if z_pos > 127:  # These lines catch stuff that would otherwise cause color errors
            z_pos = 127
        if z_pos < -127:
            z_pos = -127
        r = 0
        g = 127-z_pos/config.color_scaling_default
        b = 127+z_pos/config.color_scaling_default
        color = (r, g, b)
        pygame.draw.circle(surface, color,
                           (x.position[0]/scaling+config.HEIGHT/2-center[0]/scaling,
                            x.position[1]/scaling+config.WIDTH/2-center[1]/scaling),
                           abs(x.mass*250/config.mass_range[1])/scaling)
    pygame.display.update()


if __name__ == "__main__":
    verse = Universe(True)
    energy_list = [0]
    counter = 0
    e1_list = []
    e2_list = []
    e1_e2_list = []
    momentum_list = []
    momentum_sum_list = []
    sim_time = 10000
    progress_bar = 0
    progress_interval = 0.05
    while verse.stepcount < sim_time:
        if verse.stepcount >= progress_bar:
            print(str(100*progress_bar/sim_time) + "% done")
            progress_bar += progress_interval*sim_time
        counter += 1
        verse.step()
        if verse.stepcount % 100 == 0:
            draw(verse)
        if counter % 10 == 0:
            e1, e2 = verse.energy()
            #  print(e1 + e2, e1, e2)
            energy_list += [e1+e2]
        #  for event in pygame.event.get():
            #  if event.type == pygame.QUIT:
                #  sys.exit()
        e1, e2 = verse.energy()
        momentum = verse.momentum()
        momentum_sum = verse.momentum().dot(verse.momentum())
        energy_list += [(e1, e2, e1 + e2)]
        e1_list += [e1]
        e2_list += [e2]
        e1_e2_list += [e1 + e2]
        momentum_list.append(momentum)
        momentum_sum_list.append(momentum_sum)
        # for event in pygame.event.get():
        # if event.type == pygame.QUIT:
        # sys.exit()
    print(e1_list[0], e2_list[0])
    while len(e1_e2_list) % 1000 != 0:
        e1_e2_list.pop(-1)
        e1_list.pop(-1)
        e2_list.pop(-1)
        momentum_list.pop(-1)
        momentum_sum_list.pop(-1)
    length = int(len(e1_e2_list)/1000)
    array_12 = np.array(e1_e2_list[::length])
    array_1 = np.array(e1_list[::length])
    array_2 = np.array(e2_list[::length])
    array_momentum = np.array(momentum_list[::length])
    array_momentum_sum = np.array(momentum_sum_list[::length])
    array_helper = []
    print(length)
    for i in range(len(array_12)):
        array_helper += [i * 10]
    array_numbering = np.array(array_helper)
    print(len(array_numbering))
    plt.plot(array_numbering, array_12, label="Total Energy")
    plt.plot(array_numbering, array_1, label="Kinetic Energy")
    plt.plot(array_numbering, array_2, label="Potential Energy")
    plt.show()
    plt.plot(array_numbering, array_momentum, label="Momentum")
    plt.show()


