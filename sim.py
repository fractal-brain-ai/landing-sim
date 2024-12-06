import math
import numpy as np
import random
from config import RocketConfig

G = 9.80665


def deg_to_rad(angle: int) -> float:
    return angle * (math.pi / 180)


def clamp(mi: float, x: float, mx: float) -> float:
    return min(mx, max(x, mi))


def noop(pos, vel, angle): ...


class RocketSimulator:
    def __init__(
        self,
        step_hook: callable = noop,
        config: RocketConfig = RocketConfig(disable_random_coords=False),
    ):
        """
        :param callable step_hook: hook that gets executed after each step invocation
        """
        # bounds of sim (rocket shouldn't exceed these coords)
        self.bounds = np.array(
            [
                [-40, 40],  # x axis
                [0, 150],  # z axis
            ]
        )
        self.config = config
        self.step_hook = step_hook
        self.reset()

    def reset(self):
        """
        Resets simulation to random starting positions.
        """

        if self.config.disable_random_coords:
            self.starting_position = np.array([0, 100], dtype=np.float32)
            self.position = np.copy(self.starting_position)

            self.target_position = np.array([0, 0], dtype=np.float32)
            self.velocity = np.array([0, 0], dtype=np.float32)  # x, y

            self.angle = 0
            self.fuel = self.config.fuel

        else:
            self.starting_position = np.array(
                [
                    random.randint(*self.config.starting_position_x),
                    random.randint(*self.config.starting_position_y),
                ],
                dtype=np.float32,
            )
            self.position = np.copy(self.starting_position)

            self.target_position = np.array([0, 0], dtype=np.float32)
            self.velocity = np.array(
                [0, -(random.randint(*self.config.starting_velocity_range))],
                dtype=np.float32,
            )  # x, y

            self.angle = (
                0  # deg_to_rad(random.randint(*self.config.starting_angle_range))
            )
            self.fuel = self.config.fuel

        self.angular_velocity = 0
        self.time_elapsed = 0
        self.time_step = 0.1

    def step(self, thrust: float, rotation: float):
        """
        Steps through the simulation with given thrust and rotation angle.

        :param float thrust: Thrust value (bound between 0 and 1)
        :param float rotation: Rotation angle value (bound between -1 and 1)
        """

        thrust = clamp(0, thrust, 1)
        rotation = clamp(-1, rotation, 1)

        self.angular_velocity += rotation * self.time_step
        self.angle += self.angular_velocity * self.time_step

        self.velocity[1] -= G * self.time_step
        if self.fuel > 0:
            accel = (thrust * self.config.max_thrust) / (self.config.mass + self.fuel)

            self.velocity[0] += np.sin(self.angle) * accel * self.time_step
            self.velocity[1] += np.cos(self.angle) * accel * self.time_step

            self.fuel -= min(
                self.config.burn_rate * self.time_step * max(0.0, thrust), self.fuel
            )

        self.position += self.velocity * self.time_step
        self.time_elapsed += self.time_step

        self.step_hook(self.position, self.velocity, self.angle)

    def should_terminate(self):
        """
        :return bool: whether this run should be terminated
        """

        return (
            self.position[1] < 0
            or not (self.bounds[0][0] <= self.position[0] <= self.bounds[0][1])
            or not (self.bounds[1][0] <= self.position[1] <= self.bounds[1][1])
            or self.time_elapsed > 256
        )

    def reward(self) -> int:
        """
        :return int: returns reward (1 - if landed properly, 0 - if not)
        """
        if (
            self.position[1]
            < 0.1  # and abs(self.position[0] - self.target_position[0]) <= 5
            and abs(self.velocity[1]) <= 40
        ):
            return 1

        return 0


def make_dumper(path: str = "results.csv"):
    import csv

    # inb4, this file descriptor should be closed in the future
    f = open(path, "w")
    w = csv.writer(f, delimiter=";", quoting=csv.QUOTE_MINIMAL)
    w.writerow(["tick", "pos_x", "pos_y", "vel_x", "vel_y", "angle"])

    # we need pointer here
    r = [0]

    def dump_results(pos, vel, angle):
        result = [r[0]] + list(pos) + list(vel) + [angle]

        w.writerow([round(x, 4) for x in result])
        r[0] += 1

    return dump_results


def logger(pos, vel, angle):
    from datetime import datetime

    with np.printoptions(precision=4, formatter={"float_kind": "{:.4f}".format}):
        print(
            "[%s] current state: pos=%s, vel=%s, angle=%s"
            % (datetime.now().isoformat(), pos, vel, angle)
        )


if __name__ == "__main__":
    dump = make_dumper()

    def hook(*data):
        logger(*data)
        dump(*data)

    sim = RocketSimulator(random_coords=False, step_hook=hook)
    sim.reset()
    sim.step(1, 0)
    sim.step(1, 0)
