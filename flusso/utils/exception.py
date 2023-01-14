class UnwrapFailedError(Exception):
    """Raised when a container can not be unwrapped into a meaningful value."""

    __slots__ = ('halted_container',)

    def __init__(self, container: 'Option[T]') -> None:
        """
        Saves halted container in the inner state.
        So, this container can later be unpacked from this exception
        and used as a regular value.
        """
        super().__init__()
        self.halted_container = container