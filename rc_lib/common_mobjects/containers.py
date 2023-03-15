"""
    Different mobject-specific containing structures. 

    Semantic extension of Group / VGroup, which behave like sets, to structures
    like lists. 
"""

from manim import *

# The VGroup source checks if a mobject is either a VMobject or an OpenGLVMobject;
# we will do the same here.
from manim.mobject.opengl.opengl_vectorized_mobject import OpenGLVMobject

from typing import List, Self

__all__ = [
    "OrderedVGroup",
]


def is_valid_vmobject(item) -> bool:
    """Returns True if the given item is a valid mobject, as accepted by
    VGroup."""
    return isinstance(item, (VMobject, OpenGLVMobject))


def all_are_valid_vmobjects(item_list: list) -> bool:
    """Returns True if all items in the given list are valid mobjects, as
    accepted by VGroup."""
    return all(is_valid_vmobject(item) for item in item_list)


class OrderedVGroup(VGroup):
    """A VGroup that allows for ordered manipulation of its elements.

    VGroups are already equipped with +, -, +=, -=, which are understood to
    add to the end of the group, and [] for elements retrieval/assignment.

    This class adds:
     * insert(index, mobject) for inserting at a particular index. Returns `self`
        so that calls may be chained.
     * remove(index) and remove(mobject) for removing elements. Returns `self`
        so that calls may be chained.
     * pop(index) for removing and returning an element at a particular index.
     * __len__() and __iter__() over the elements of the group.


    Members of a VGroup must be unique, so adding in duplicate elements will
    be ignored silently; use mobject.copy() if you want to add a duplicate.

    remove(mobject) is a redundant method with - and -=, and due to uniqueness
    remove(index) is too.

    Note: I'm not sure how much of the methods called are part of the public
    interface, so this may break in future versions of manim.
    """

    def _validate_mobjects(self, *mobjects: VMobject):
        """Checks the validity of all provided mobjects and raises a value
        error if any are invalid."""
        if not all_are_valid_vmobjects(mobjects):
            raise ValueError("Member mobjects must be of type VMobject")

    # Constructor is the same as VGroup
    def __init__(self, *submobjects: VMobject, **kwargs):
        super().__init__(*submobjects, **kwargs)

    # a few aliases for methods called on members:
    def contains(self, mobject: VMobject) -> bool:
        """Returns True if the given object is in the group."""
        # count method not needed since we are enforcing uniqueness
        return self.submobjects.count(mobject) > 0

    def index(self, mobject: VMobject) -> int:
        """Returns the index of the given mobject in the group.

        Raises a ValueError if the mobject is not in the group: use
        `contains(mobject)` to check if it is in the group first.
        """
        return self.submobjects.index(mobject)

    def __len__(self) -> int:
        """Returns the number of elements in the group."""
        return len(self.submobjects)

    def __iter__(self):
        """Returns an iterator over the elements of the group."""
        return iter(self.submobjects)

    # Insertion
    def insert(self, index: int, mobject: VMobject) -> Self:
        """Inserts the given mobject at the given index.

        Raises a ValueError if not given a valid mobject. Inserting a duplicate
        does nothing.
        """
        self._validate_mobjects(mobject)
        if not self.contains(mobject):
            self.submobjects.insert(index, mobject)

        return self

    # Removal
    def remove(self, mobject_or_index: VMobject) -> Self:
        """
        Removes the given mobject or index from the group.

        Raises a ValueError if not given a valid mobject or index.
        """
        if isinstance(mobject_or_index, int):
            self.pop(mobject_or_index)
        else:
            self._validate_mobjects(mobject_or_index)
            self -= mobject_or_index
        return self

    def pop(self, index: int) -> VMobject:
        """Removes and returns the mobject at the given index."""
        return self.submobjects.pop(index)
