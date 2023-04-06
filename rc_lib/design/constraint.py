import manim as mn
from rc_lib.design import sketch, sketch_utils


class Coincident(mn.Succession):
    """Performs an animation which constrains base to target using a coincident constraint.

    Implementation is complicated by the need to bring parent mobjects along for the ride.
    This creates a two-way dependency unless we specify so that points always drive their parents,
    which is tricky for some arcs.

    Even without updaters, implementation is challenging; we'd likely need to pass the move method or
    take the parent plus the actual child being moved.

    Also, how do we allow certain combinations but not others, like line and line point? Runtime checks
    plus common sense?
    """

    def __init__(self, base: sketch.Point | sketch.Line, target: sketch.Base):
        # base_type = sketch_utils.classify(base)
        # target_type = sketch_utils.classify(target)

        # match base_type:
        #     case sketch_utils.SketchType.POINT:
        #         pass
        #     case sketch_utils.SketchType.POINT:
        #         pass
        if isinstance(base, sketch.Point):
            # how to move to target? Need a parent method or something
            pass

        super().__init__(sketch_utils.Click(base), sketch_utils.Click(target))
