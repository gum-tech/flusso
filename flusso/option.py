from typing import Generic, TypeVar, Callable, Union, Tuple
from dataclasses import dataclass

T = TypeVar('T')

@dataclass
class Option(Generic[T]):
    """
    An implementation of the Option Monad pattern, which represents an optional value that may or may not be present.
    """
    bind: Callable[[T], 'Option']
    and_then: Callable[[Callable[[T], 'Option']], 'Option']
    filter_: Callable[[Callable[[T], bool]], 'Option']
    unwrap: Callable[[], T]
    expect: Callable[[str], T]
    unwrap_or: Callable[[], T]
    unwrap_or_else: Callable[[T], T]
    or_: Callable[['Option'], 'Option']
    or_else: Callable[[Callable[[], 'Option']], 'Option']
    and_: Callable[['Option'], 'Option']
    ok_or: Callable[[T], Tuple[bool, T]]
    is_some: Callable[[], bool]
    is_none: Callable[[], bool]
    value: Union[T, None]

    def __eq__(self, other: 'Option') -> bool:
        """
        Compare this Option instance with another instance.

        Returns:
            True if both instances are None or both have the same value, False otherwise.
        """
        if self.is_none() and other.is_none():
            return True
        elif self.is_some() and other.is_some():
            return self.unwrap() == other.unwrap()
        else:
            return False

def _some(value: T) -> Option:
    """
    Create a new `Some` instance of the OptionMonad pattern with the specified value.

    Args:
        value: The value to wrap in the `Some` instance.

    Returns:
        An `Option` instance representing the `Some` variant, wrapping the specified value.
    """
    def bind(fn: Callable[[T], T]) -> Option:
        return _some(fn(value))

    def and_then(fn: Callable[[T], Option]) -> Option:
        return fn(value)

    def filter_(fn: Callable[[T], bool]) -> Option:
        return _some(value) if fn(value) else _none()

    def unwrap() -> T:
        return value

    def expect(msg: str) -> T:
        if value is None:
            raise Exception(msg)
        return value

    def unwrap_or(_val: T) -> T:
        if value is None:
            raise ValueError("Cannot call `unwrap_or` on `None` value")
        return value

    def unwrap_or_else(default: T) -> T:
        return value if value is not None else default

    def or_(other: Option) -> Option:
        return _some(value)

    def or_else(fn: Callable[[], Option]) -> Option:
        return _some(value) if value is not None else fn()

    def and_(other: Option) -> Option:
        return other if value is not None else _none()

    def ok_or(error: T) -> Tuple[bool, T]:
        return (True, value)

    def is_some() -> bool:
        return True

    def is_none() -> bool:
        return False

    return Option(
        bind, and_then, filter_, unwrap, expect, unwrap_or,
        unwrap_or_else, or_, or_else, and_, ok_or, is_some,
        is_none, value
    )

def _none() -> Option:
    """
    Create a new `None` instance of the OptionMonad pattern.

    Returns:
        An `Option` instance representing the `None` variant.
    """
    def bind(_: Callable[[T], T]) -> Option:
        return _none()

    def and_then(_: Callable[[T], Option]) -> Option:
        return _none()

    def filter_(_: Callable[[T], bool]) -> Option:
        return _none()

    def unwrap() -> T:
        raise ValueError("Cannot call `unwrap` on `Nothing` value")

    def expect(msg: str) -> T:
        raise Exception(msg)

    def unwrap_or(other: T) -> T:
        return other

    def unwrap_or_else(other: T) -> T:
        return other

    def or_(other: Option) -> Option:
        return other

    def or_else(fn: Callable[[], Option]) -> Option:
        return fn()

    def and_(other: Option) -> Option:
        return _none()

    def ok_or(error: T) -> Tuple[bool, T]:
        return (False, error)

    def is_some() -> bool:
        return False

    def is_none() -> bool:
        return True

    return Option(
        bind, and_then, filter_, unwrap, expect, unwrap_or,
        unwrap_or_else, or_, or_else, and_, ok_or, is_some,
        is_none, None
    )

# Alias for none() to avoid confusion with None
Nothing: Option = _none()

def Some(value: T) -> Option:
    """
    Create a new `Some` instance of the OptionMonad pattern with the specified value, or `None` if the value is `None`.

    Args:
        value: The value to wrap in the `Some` instance.

    Returns:
        An `Option` instance representing the `Some` variant, wrapping the specified value, or an instance of the `None` variant if the specified value is `None`.
    """
    return _none() if value is Nothing else _some(value)

# Option decorator
def option(fn: Callable) -> Callable:
    """
    A decorator that takes a function and returns a new function that returns an `Option` instance.

    If the original function returns `None`, the returned function will return an instance of the `None` variant.
    Otherwise, the returned function will return a new instance of the `Some` variant, wrapping the result of the original function.

    Args:
        fn: The function to decorate.

    Returns:
        A new function that returns an `Option` instance.
    """
    def wrapper(*args, **kwargs) -> Option:
        return Nothing if fn(*args, **kwargs) is None else Some(fn(*args, **kwargs))
    return wrapper
