from unittest import TestCase

from should import should

from micropatcher import Patcher


class TestItem(TestCase):
  def test_setitem(self) -> None:
    """Check that setitem() works ok and it patches."""

    # (1) arrange
    out = dict(x=12, y=34)
    patcher = Patcher()

    # (2) act
    patcher.setitem(out, "x", 21)
    patcher.setitem(out, "xy", 21)

    # (3) assessment
    should(out).have("x").eq(21)
    should(out).have("y").eq(34)
    should(out).have("xy").eq(21)

  def test_delitem(self) -> None:
    """Check that delitem() works ok and it patches."""

    # (1) arrange
    out = dict(x=12, y=34)
    patcher = Patcher()

    # (2) act
    patcher.delitem(out, "x")
    patcher.delitem(out, "z")

    # (3) assessment
    should(out).not_have("x")
    should(out).have("y").eq(34)
    should(out).not_have("z")
