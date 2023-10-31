G = (6.6743*10**-11)/(10**-4)  # Gravitational constant of the universe
body_count = 10  # initial amount of bodies for the randomizer
mass_range = (10**10, 10**11)  # mass range for mass randomizer
k = 10**3
position_range = ((-k, k), (-k, k), (-k, k))
c = 10**1
velocity_range = ((-c, c), (-c, c), (-c, c))
# gives range for randomized positions and velocities
# ((min_x, max_x), (min_y, max_y), (min_z, max_z))
WIDTH = 900
HEIGHT = 900
# determines the size of the display
white = (255,255,255)
black = (0, 0, 0)
red = (255, 0, 0)
blue = (0, 0, 255)
# defines some colors
width = 10  # width of ... something?
scaling_default = 5  # default scaling value
scaling_border = 0.9  # default distance kept from border (only if do_scaling = True)
do_scaling = False  # scale to keep everything inside view?
do_centering = True  # move to keep everything more central?
timescale = 1
color_scaling_default = 1
do_color_scaling = False
do_color_centering = True
distance_threshold = k  # threshold for how close two bodies have to be to slow down time
timescale_exponent = 2  # how much should time be slowed down for encounters
