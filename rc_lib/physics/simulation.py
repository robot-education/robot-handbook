import numpy as np

from typing import Callable, Any
import abc
from rc_lib.math_utils.vector import Vector

PhysicalSystem = Any
ForceFunction = Callable[[PhysicalSystem], Vector]


class PositionSystem(abc.ABC):
    @abc.abstractmethod
    def get_position(self) -> Vector:
        return np.array([])

    @classmethod
    def __subclasshook__(cls, subclass):
        if callable(getattr(subclass, "get_position", None)):
            return True
        return NotImplemented


class VelocitySystem(abc.ABC):
    @abc.abstractmethod
    def get_velocity(self) -> Vector:
        return np.array([])

    @classmethod
    def __subclasshook__(cls, subclass):
        if callable(getattr(subclass, "get_velocity", None)):
            return True
        return NotImplemented


class TimeSystem(abc.ABC):
    @abc.abstractmethod
    def get_time(self) -> float:
        return 0

    @classmethod
    def __subclasshook__(cls, subclass):
        if callable(getattr(subclass, "get_time", None)):
            return True
        return NotImplemented


class EvolvedSystem(abc.ABC):
    @abc.abstractmethod
    def step(self, dt: float):
        pass

    @classmethod
    def __subclasshook__(cls, subclass):
        if callable(getattr(subclass, "step", None)):
            return True
        return NotImplemented


class SingleBodyForces:
    """
    Simulates a point mass experiencing forces in any number of dimensions.

    Simulation is driven by regestering forces (as functions) and keeping
    track of the point state as position and momentum, and then updating the
    simulation by calling `step(dt)`.

    Update equations are a first-order approximation: they assume that
    dt**2 is small and can be approximated to zero. Thus, the state update
    becomes:
        x' = x + v * dt
        momentum' = momentum + (sum of forces) * dt

    Force functions take

    Initial/reset conditions are specified as a position and velocity of the
    point mass.
    """

    def __init__(
        self,
        *forces,
        mass=1.0,
        position: Vector = np.array([0, 0, 0]),
        velocity: Vector = np.array([0, 0, 0]),
        start_time=0.0
    ):
        self.time = start_time
        self.mass = mass

        self.position = position
        self.momentum = velocity * mass

        self.forces = []
        self.add_forces(*forces)

    def reset_state(
        self, position: Vector | None = None, velocity: Vector | None = None
    ):
        if position is not None:
            self.position = position
        if velocity is not None:
            self.momentum = velocity * self.mass

    def add_forces(self, *forces: ForceFunction):
        self.forces.extend(forces)

    def step(self, dt: float):
        force = [f(self) for f in self.forces]
        net_force = sum(force, np.zeros_like(self.momentum))

        self.position += dt * self.get_velocity()
        self.momentum += dt * net_force

        self.time += dt

    def get_velocity(self) -> Vector:
        return self.momentum / self.mass

    def get_position(self) -> Vector:
        # Implemented to meet the PositionSystem contract
        return self.position

    def get_time(self) -> float:
        return self.time


class PIDForces:
    """
    A PID system where effort is analogous to a force- it effects the second
    derivative of error, such as effort representing motor output and error
    representing position.

    Primarily intended for use along a single dimension, this simulation
    can also extend arbitrarily to any number of homogenous dimensions by
    setting the initial conditions and setpoint to vectors. PIDForces uses
    an underlying SingleBodyForces instance to track the system; force functions
    are given that SingleBodyForces instance instead of PIDForces. kP, kI,
    and kD may be specified as vectors as well, in which case element-wise
    multiplication happens, but this is not the intended usage scenario.

    Call `step(dt)` on this object not the underlying SingleBodyForces
    """

    def __init__(
        self,
        kP: float | Vector,
        kI: float | Vector,
        kD: float | Vector,
        system: SingleBodyForces,
        setpoint: float | Vector = 0,
        force_factor: float = 1,  # translation of effort into force
    ):
        self.kP, self.kI, self.kD = kP, kI, kD
        self.force_factor = force_factor
        self.system = system

        if isinstance(setpoint, float):
            self.use_scalar = True
            # need to use a vector to mesh smoothly with SingleBodyForces
            self.setpoint = np.array([self.setpoint])
        else:
            self.use_scalar = False
            self.setpoint = setpoint

        self.error = None
        self.error_buildup = self._zero_vector()
        self.error_derivative = self._zero_vector()

        system.add_forces(lambda system: self._force())

    def _zero_vector(self):
        """Takes dimension cues from the setpoint"""
        return np.zeros_like(self.setpoint)

    def reset(self):
        """Resets the PID calculations, not the underlying system."""
        self.last_error = None
        self.error_buildup = self._zero_vector()

    def step(self, dt: float):
        err = self.setpoint - self.system.position

        if self.error is not None:
            self.error_derivative = (err - self.error) / dt
        else:
            self.error_derivative = self._zero_vector()

        self.error_buildup += err * dt
        self.error = err

        self.system.step(dt)

    def _effort_proportional(self) -> Vector:
        """
        Always returns effort as a vector
        """
        assert self.error is not None, "Please call `step` before sampling system"
        return self.kP * self.error

    def _effort_integral(self) -> Vector:
        return self.kI * self.error_buildup

    def _effort_derivative(self) -> Vector:
        return self.kD * self.error_derivative

    def _effort(self) -> Vector:
        """Total effort"""
        return (
            self._effort_proportional()
            + self._effort_integral()
            + self._effort_derivative()
        )

    def _force(self) -> Vector:
        return self.force_factor * self._effort()

    def effort_proportional(self) -> float | Vector:
        """
        Returns the proportional effort of the system from the last timestep.

        Will return the same type as the given setpoint: a scalar if given
        a scalar setpoint, a vector if given a vector setpoint (even if dim 1)
        """
        e = self._effort_proportional()
        return e.item() if self.use_scalar else e

    def effort_integral(self) -> float | Vector:
        """
        Returns the integral effort of the system from the last timestep.

        Will return the same type as the given setpoint: a scalar if given
        a scalar setpoint, a vector if given a vector setpoint (even if dim 1)
        """
        e = self._effort_integral()
        return e.item() if self.use_scalar else e

    def effort_derivative(self) -> float | Vector:
        """
        Returns the derivative effort of the system from the last timestep.

        Will return the same type as the given setpoint: a scalar if given
        a scalar setpoint, a vector if given a vector setpoint (even if dim 1)
        """
        e = self._effort_derivative()
        return e.item() if self.use_scalar else e

    def effort(self) -> float | Vector:
        """
        Returns the total effort of the system from the last timestep,
        matching types with the provided setpoint.
        """
        e = self._effort()
        return e.item() if self.use_scalar else e
