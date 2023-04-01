from functools import partial

import manim as mn
import numpy as np
import pid_mobjects

from rc_lib.style import animation, text
from rc_lib.common_mobjects import layouts
from rc_lib.physics import simulation
from rc_lib.math_utils import vector, mobject_geometry


def friction_force(mu, system: simulation.SingleBodyForces):
    vel = system.get_velocity()
    if vector.norm(vel) < 0.01:
        return np.zeros_like(vel)
    dir = -vector.normalize(vel)
    return dir * mu * system.mass


class RobotScene(mn.Scene):
    def setup(self):
        # display stuff
        self.robot = pid_mobjects.Robot()
        self.line = pid_mobjects.RobotLine(self.robot)
        self.robot_pos = self.line.robot_position

        self.add(self.line)  # robot comes along with
        self.add(self.robot_pos)  # in case of any updaters

        self.line.align_on_border(mn.DOWN)


class PhysicalRobotScene(RobotScene):
    def setup(self):
        super().setup()

        # physics stuff
        self.phys_sim = simulation.SingleBodyForces(
            position=np.array([0.0]), velocity=np.array([0.0])
        )

        # for physical robots, interact via the simulation
        self.robot_pos.add_updater(
            lambda vt: vt.set_value(self.phys_sim.get_position().item())
        )

        self.force_legend_layout = layouts.LinearLayout(
            direction=mn.DOWN, root=3.0 * mn.UP
        )
        self.add(self.force_legend_layout)

        self.force_diagram_layout = layouts.LinearLayout()
        self.force_diagram_layout.add_updater(
            lambda fd: fd.move_to(self.robot.get_center()),  # type: ignore
        )

        self.add(self.force_diagram_layout)

    def show_vector(self, label: str, length_func, color=mn.WHITE):
        lab = mn.Text(label, color=color, font_size=text.FontSize.LARGE)
        self.force_legend_layout.add(lab)

        for layout in (self.force_diagram_layout, self.force_legend_layout):
            root = mn.Dot(color=color)
            layout.add(root)

            vec = mn.Line(color=color, buff=0.5, stroke_width=10)  # type: ignore
            vec.add_updater(
                partial(
                    lambda root, vec: vec.put_start_and_end_on(
                        *mobject_geometry.no_loop(
                            root.get_center(),
                            root.get_center() + length_func() * mn.RIGHT,
                        )
                    ),
                    root,
                )  # type: ignore doesn't like the implicit return
            )
            self.add(vec)
            layout.arrange()


class IntroduceRobotScene(RobotScene):
    def construct(self):
        super().construct()

        self.robot_pos.set_value(-1)
        self.play(
            self.robot_pos.animate.set_value(1),
            run_time=animation.LONG,
            rate_func=mn.smooth,
        )

        self.wait(animation.END_DELAY)


class DriveRightScene(PhysicalRobotScene):
    def setup(self):
        super().setup()

        self.show_vector(
            "Robot Velocity", self.phys_sim.get_velocity, pid_mobjects.col_speed
        )

        def fixed_force(system):
            return np.array([0.5])

        self.phys_sim.add_forces(fixed_force)
        self.show_vector(
            "Robot Force", partial(fixed_force, self.phys_sim), pid_mobjects.col_accel
        )

    def construct(self):
        self.phys_sim.reset_state(position=np.array([-1.0]))
        self.play(simulation.EvolveSystem(self.phys_sim, 5))  # type: ignore


class DemonstrateFrictionScene(PhysicalRobotScene):
    def setup(self):
        super().setup()

        self.show_vector(
            "Robot Velocity", self.phys_sim.get_velocity, pid_mobjects.col_speed
        )

        do_drive = True

        def drive_up_to_center(system):
            nonlocal do_drive
            if do_drive and system.get_position().item() < 0.0:
                return np.array([1])
            do_drive = False
            return np.array([0.0])

        self.phys_sim.add_forces(drive_up_to_center)
        self.show_vector(
            "Robot Force",
            partial(drive_up_to_center, self.phys_sim),
            pid_mobjects.col_accel,
        )

        friction = partial(friction_force, 0.75)
        self.phys_sim.add_forces(friction)
        self.show_vector(
            "Friction",
            partial(friction, self.phys_sim),
            pid_mobjects.col_friction,
        )

    def construct(self):
        self.phys_sim.reset_state(position=np.array([-1.0]))
        self.play(simulation.EvolveSystem(self.phys_sim, 4))  # type: ignore
        self.wait(animation.END_DELAY)
