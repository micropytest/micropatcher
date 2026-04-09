TYPE_CHECKING = False
if TYPE_CHECKING:
  from typing import Any


# Value to use when item or key doesn't exist.
_non_existing_value = type("NonExistingValue", (), {})()


class Patcher:
  """An adaptable object for representing an object in a test.

  Attributes:
    _attrs: Patched attributes.
    _items: Patched dictionary items.
  """

  def __init__(self, **kwargs):
    self._attrs = {"set": []}
    self._items = {"set": [], "del": []}

  def setattr(self, tgt: Any, name: str, value: Any) -> Any:
    """Patches an attribute of a given object.

    Args:
      tgt: Target object where to work.
      name: Attribute name to patch.
      value: Attribute value to use during the test.

    Raises:
      AttributeError: If the attribute doesn't exist.
      TypeError: If the attribute not defined in the instance such as, for example, a property.
    """

    # (1) pre
    if not hasattr(tgt, name):
      raise AttributeError(f"Target expected to have the attribute '{name}'.")

    if name not in tgt.__dict__:
      raise TypeError(
        f"Attribute '{name}' can't be patched, for example, properties can't be patched at instance-level."
      )

    # (2) patch
    old_value = getattr(tgt, name)
    setattr(tgt, name, value)
    self._attrs["set"].append((tgt, name, old_value))

    # (3) return
    return tgt

  def setitem(self, tgt: dict, key: str, value: Any) -> dict:
    """Patches a key from a dictionary. If this doesn't exist, this is created
    for the test.

    Args:
      tgt: Target dictionary where to work.
      key: Key to patch.
      value: Value to set.
    """

    # (1) patch
    old_value = _non_existing_value if key not in tgt else tgt[key]
    tgt[key] = value
    self._items["set"].append((tgt, key, old_value))

    # (2) return
    return tgt

  def delitem(self, tgt: dict, key: str) -> dict:
    """Deletes a key from a dictionary during a test.

    Args:
      tgt: Target dictionary where to work.
      key: Key to delete.
    """

    # (1) patch
    if key in tgt:
      value = tgt[key]
      del tgt[key]
    else:
      value = _non_existing_value

    # (2) remember patch to undo
    self._items["del"].append((tgt, key, value))

    # (3) return
    return tgt

  def undo(self) -> None:
    """Undoes the patching performed."""

    self._undo_patched_attrs()
    self._undo_patched_items()

  def _undo_patched_attrs(self) -> None:
    for tgt, name, value in self._attrs["set"]:
      setattr(tgt, name, value)

  def _undo_patched_items(self) -> None:
    # (1) set
    for tgt, key, value in self._items["set"]:
      tgt[key] = value

    # (2) del
    for tgt, key, value in self._items["del"]:
      if value is _non_existing_value:
        tgt.pop(key, None)
      else:
        tgt[key] = value
