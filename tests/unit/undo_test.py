from unittest import TestCase

from should import should  # type: ignore

from micropatcher import Patcher


class Point:
  def __init__(self, x: int, y: int):
    self.x = x
    self.y = y

  @property
  def xy(self) -> int:
    return self.x + self.y


class TestUndo(TestCase):
  def test_undo(self) -> None:
    """Check that undo() undoes the patching."""

    # (1) arrange
    p = Point(12, 34)
    d = dict(x=21, y=43)

    patcher = Patcher()

    patcher.setattr(p, "x", 1234)
    should(p.x).be_eq(1234)

    patcher.setitem(d, "y", 1234)
    should(d).have("y").eq(1234)
    patcher.delitem(d, "x")
    should(d).not_have("x")
    patcher.delitem(d, "z")
    should(d).not_have("z")

    # (2) act
    patcher.undo()

    # (3) assessment
    should(p.x).be_eq(12)
    should(p.y).be_eq(34)
    should(d).have("x").eq(21)
    should(d).have("y").eq(43)
    should(d).not_have("z")
