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


class TestAttr(TestCase):
  def test_setattr(self) -> None:
    """Check that setattr() works ok and it patches."""

    # (1) arrange
    out = Point(12, 34)
    patcher = Patcher()

    # (2) act
    patcher.setattr(out, "x", 21)
    patcher.setattr(out, "y", 43)

    # (3) assessment
    should(out.x).be_eq(21)
    should(out.y).be_eq(43)

  def test_setattr_raises_if_non_existing(self) -> None:
    """Check that setattr() raises an error if attribute doesn't exist."""

    # (1) arrange
    p = Point(12, 34)
    patcher = Patcher()

    # (2) act and assessment
    should(lambda: patcher.setattr(p, "z", 1234)).throw(
      AttributeError,
      match="Target expected to have the attribute 'z'",
    )

  def test_setattr_raises_if_property(self) -> None:
    """Check that setattr() raises error if @property."""

    # (1) arrange
    p = Point(12, 34)
    patcher = Patcher()

    # (2) act and assessment
    should(lambda: patcher.setattr(p, "xy", 1234)).throw(
      TypeError,
      match="Attribute 'xy' can't be patched",
    )
