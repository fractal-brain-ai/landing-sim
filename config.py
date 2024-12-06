from dataclasses import dataclass


@dataclass
class RocketConfig:
    mass = 2  # kg
    fuel = 20  # kgs
    max_thrust = 1000  # kN
    burn_rate = 5  # kgs/s
