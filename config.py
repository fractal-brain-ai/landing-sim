from dataclasses import dataclass


@dataclass
class RocketConfig:
    mass = 2  # kg
    fuel = 20  # kgs
    max_thrust = 1000  # kN
    burn_rate = 5  # kgs/s

    starting_velocity_range = (10, 20)  # values are automatically converted to negative
    starting_angle_range = (-30, 30)
    starting_position_x = (0, 0)
    starting_position_y = (80, 100)
    disable_random_coords: bool = False
