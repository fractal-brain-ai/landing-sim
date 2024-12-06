## Starship Simulator - Docs

# Setting up

Construct environment using RocketSimulator's class, use `random_coords: bool` param to specify if each `.reset()` call should reset rocket's position to random values.

> [!NOTE]
> `RocketSimulator` requires `numpy>=2.1.2` to be installed.

# Using the simulator

For each model output call `.step()` function with following params:

* `thrust` - value ranging from 0 to 1, how much thrust to apply in one sim tick (defined by `thrust * self.max_thrust`),
* `rotation` - action ranging from -1 to 1, how much to rotate the ship


#### Callbacks

Connect your callbacks using `step_hook: callable` parameter. `step_hook` takes 3 positional parameters:

* `position`: current rocket position (type: `np.array(shape=(2, 0), dtype=float32)`)
* `vel`: current rocket velocity (type: `np.array(shape=(2, 0), dtype=float32)`)
* `angle`: current rocket angle in radians (type: `float`)



> [!NOTE]
> You can add more callbacks, for this purpose create one big hook function, that'll execute all your callbacks (and pass data to them).


```python
dump = make_dumper()

def hook(*data):
    logger(*data)
    dump(*data)

sim = RocketSimulator(step_hook=hook)
```


#### Adjust rewarding

Defaults are quite relaxed. We're allowing the rocket to land with accuracy up to 5m from the base station and with speed of <=5m/s. Adjust these settings up to your liking.


#### Terminating the run

Use `.should_terminate()` function to determine if this run should be terminated. Returns true while one of the following condition is met:

* if x position is outside of pre-defined bounds (`self.bounds`),
* if z position is outside of pre-defined bounds,
* if the current tick count is more than `256 * self.time_step`


# Rendering the results

For dumping the results, use attached `make_dumper` factory, use it like this:

```python
sim = RocketSimulator(step_hook=make_dumper())
```


If you'll send us the results, we can render you a preview of your own Starship landing. Here's a preview how the final render can look like:

[https://fractalbrain.ai/rockets/r4.mp4](https://fractalbrain.ai/rockets/r4.mp4) landing-sim
