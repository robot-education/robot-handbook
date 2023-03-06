from manim import *
from common.design import plate
from common.view import sequential_title
from common.calc import util

# from common.view import style, sequential_title
quality = "ql"


class IntakePlateScene(Scene):
    def construct(self):
        small_base = plate.PlateCircle.make(0.15, 0.2)
        medium_base = plate.PlateCircle.make(0.4, 0.2)

        front_hole = util.point(-4, -3)
        middle_hole = util.point(-1.5, 0.25)
        back_hole = util.point(2.5, 1.5)

        back_offset = util.point(0.8, 0.75)

        points = [
            medium_base.copy(front_hole),
            medium_base.copy(middle_hole),
            medium_base.copy(back_hole),
            small_base.copy(back_hole + back_offset),
            small_base.copy(back_hole + util.point(1, -0.2)),
            small_base.copy((middle_hole + back_hole) / 2),
            small_base.copy((front_hole + middle_hole) / 2),
        ]

        boundary_order = [1, 3, 4, 0]
        pl = plate.Plate(points, boundary_order)
        # titles = sequential_title.SequentialTitle(
        #     ["Draw plate holes", "Add larger circles", "Connect boundary"])

        # self.play(titles.next(), run_time=0.5)
        self.play(pl.draw_inner_circles())
        self.wait(1)

        # self.play(titles.next(), run_time=0.5)
        self.play(pl.draw_outer_circles())
        self.wait(1)

        # self.play(titles.next(), run_time=0.5)
        self.play(pl.draw_boundary(), run_time=2)
        self.wait(3)
