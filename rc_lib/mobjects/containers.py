"""
    Different mobject-specific containing structures. 

    Semantic extension of Group / VGroup, which behave like sets, to structures
    like lists. 
"""
import manim as mn

# The VGroup source checks if a mobject is either a VMobject or an OpenGLVMobject;
# we will do the same here.

from typing import Any, Iterable, List, Self, TypeGuard, cast


def is_valid_vmobject(item) -> TypeGuard[mn.VMobject]:
    """Returns True if the given item is a valid mobject, as accepted by
    VGroup."""
    return isinstance(item, mn.VMobject)


def all_valid_vmobjects(item_list: Iterable[Any]) -> TypeGuard[List[mn.VMobject]]:
    """Returns True if all items in the given list are valid mobjects, as
    accepted by VGroup."""
    return all(is_valid_vmobject(item) for item in item_list)


class OrderedVGroup(mn.VGroup):
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

    def _validate_mobjects(self, *mobjects: mn.VMobject):
        """Checks the validity of all provided mobjects and raises a value
        error if any are invalid."""
        if not all_valid_vmobjects(mobjects):
            raise ValueError("Member mobjects must be of type VMobject")

    # Constructor is the same as VGroup
    def __init__(self, *submobjects: mn.VMobject, **kwargs):
        super().__init__(*submobjects, **kwargs)

    # a few aliases for methods called on members:
    def contains(self, mobject: mn.VMobject) -> bool:
        """Returns True if the given object is in the group."""
        # count method not needed since we are enforcing uniqueness
        return self.submobjects.count(mobject) > 0

    def index(self, mobject: mn.VMobject) -> int:
        """
        Returns the index of the given mobject in the group.

        Raises a ValueError if the mobject is not in the group: use
        `contains(mobject)` to check if it is in the group first.
        """
        return self.submobjects.index(mobject)

    def __getitem__(self, value: int) -> mn.VMobject:
        return cast(mn.VMobject, super().__getitem__(value))

    def __len__(self) -> int:
        """Returns the number of elements in the group."""
        return len(self.submobjects)

    def __iter__(self):
        """Returns an iterator over the elements of the group."""
        return iter(self.submobjects)

    # Insertion
    def insert(self, index: int, mobject: mn.VMobject) -> Self:
        """
        Inserts the given mobject at the given index.

        Raises a ValueError if not given a valid mobject. Inserting a duplicate
        does nothing.
        """
        self._validate_mobjects(mobject)
        if not self.contains(mobject):
            self.submobjects.insert(index, mobject)
        return self

    # Removal
    def remove(self, mobject_or_index: mn.VMobject) -> Self:
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

    def pop(self, index: int) -> mn.VMobject:
        """Removes and returns the mobject at the given index."""
        return cast(mn.VMobject, self.submobjects.pop(index))