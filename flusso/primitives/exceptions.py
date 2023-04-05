from typing import Union
from flusso.primitives.base import Option, Result
from flusso.types import T, E

class UnwrapFailedError(Exception):
    """
    Raised when attempting to unwrap a container that doesn't have a valid value.
    """

    __slots__ = ('halted_container',)

    def __init__(self, container: Union['Option[T]', 'Result[T, E]']) -> None:
        """
        Stores the container that caused the unwrap operation to fail in the exception's state.
        This allows the container to be later retrieved from the exception and used as a regular value.
        """
        super().__init__()
        self.halted_container = container
