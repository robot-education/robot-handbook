from manim import *
from rc_lib import types as T
from rc_lib import style
from rc_lib.design_utils import plate
from rc_lib.view_utils import title_sequence

# from common.view import style, sequential_title
quality = "ql"


class IntakePlateScene(Scene):
    def construct(self):
        small_base = plate.PlateCircle.make(0.15, 0.2)
        medium_base = plate.PlateCircle.make(0.4, 0.2)

        front_hole = T.point_2d(-4, -3)
        middle_hole = T.point_2d(-1.5, 0.25)
        back_hole = T.point_2d(2.5, 1.5)

        back_offset = T.point_2d(0.8, 0.75)

        points = [
            medium_base.copy(front_hole),
            medium_base.copy(middle_hole),
            medium_base.copy(back_hole),
            small_base.copy(back_hole + back_offset),
            small_base.copy(back_hole + T.point_2d(1, -0.2)),
            small_base.copy((middle_hole + back_hole) / 2),
            small_base.copy((front_hole + middle_hole) / 2),
        ]

        boundary_order = [1, 3, 4, 0]
        plate_group = plate.PlateGroup(points, boundary_order)
        title = title_sequence.TitleSequence(
            ["Draw plate holes", "Add larger circles", "Connect boundary"])

        self.play(title.next(), run_time=0.5)
        self.play(plate_group.draw_inner_circles())
        self.wait(1)

        self.play(title.next(), run_time=0.5)
        self.play(plate_group.draw_outer_circles())
        self.wait(1)

        self.play(title.next(), run_time=0.5)
        self.play(plate_group.draw_boundary(), run_time=2)
        self.wait(3)
