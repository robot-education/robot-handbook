import manim as mn
from rc_lib.style import color

col_p, col_accel, col_friction, col_i, col_speed, col_d = color.color_categories(6)


class Robot(mn.VGroup):
    def __init__(self):
        self.body = mn.Square()
        self.body_center = mn.Line(0.6 * mn.DOWN, 0.6 * mn.UP)
        super().__init__(self.body, self.body_center)


class RobotLine(mn.VGroup):
    def __init__(self, robot: mn.Mobject, length=11.0):
        self.robot = robot
        self.line = mn.NumberLine([-1, 1], length=length)

        self.robot_position = mn.ValueTracker()
        self.robot.add_updater(self._move_robot)
        super().__init__(self.robot, self.line)

    def _move_robot(self, robot: mn.Mobject):
        robot.next_to(self.get_robot_screen_pos(), mn.UP)

    def get_robot_screen_pos(self):
        return self.line.n2p(self.robot_position.get_value())
