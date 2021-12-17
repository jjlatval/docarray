import copy as cp
from typing import TYPE_CHECKING, Optional, Tuple
from .helper import typename

if TYPE_CHECKING:
    from .types import T


class BaseDCType:
    _data_class = None

    @property
    def non_empty_fields(self) -> Tuple[str]:
        """Get all non-emtpy fields of this :class:`Document`.

        Non-empty fields are the fields with not-`None` and not-default values.

        :return: field names in a tuple.
        """
        return self._data._non_empty_fields

    def __init__(self: 'T', _obj: Optional['T'] = None, copy: bool = False, **kwargs):
        self._data = None
        if isinstance(_obj, type(self)):
            if copy:
                self.copy_from(_obj)
            else:
                self._data = _obj._data
        elif isinstance(_obj, dict):
            kwargs.update(_obj)
        if kwargs:
            self._data = self._data_class(self, **kwargs)
        if _obj is None and not kwargs:
            self._data = self._data_class(self)

        if self._data is None:
            raise ValueError(
                f'Failed to initialize {typename(self)} from obj={_obj}, kwargs={kwargs}'
            )

    def copy_from(self: 'T', other: 'T') -> None:
        """Overwrite self by copying from another :class:`Document`.

        :param other: the other Document to copy from
        """
        self._data = cp.deepcopy(other._data)

    def clear(self) -> None:
        """Clear all fields from this :class:`Document` to their default values."""
        for f in self.non_empty_fields:
            setattr(self._data, f, None)

    def pop(self, *fields) -> None:
        """Clear some fields from this :class:`Document` to their default values.

        :param fields: field names to clear.
        """
        for f in fields:
            if hasattr(self, f):
                setattr(self._data, f, None)

    @property
    def nbytes(self) -> int:
        """Return total bytes consumed by protobuf.

        :return: number of bytes
        """
        return len(bytes(self))

    def __hash__(self):
        return hash(self._data)

    def __repr__(self):
        content = str(self.non_empty_fields)
        content += f' at {id(self)}'
        return f'<{typename(self)} {content.strip()}>'

    def __bytes__(self):
        return self.to_bytes()

    def __eq__(self, other):
        return self._data == other._data