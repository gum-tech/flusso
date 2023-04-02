from typing import Callable
from .types import T, E
from flusso.primitives.base import Option, Result


def _some(value: T) -> Option:
    """
    Create a new `Some` instance of the OptionMonad pattern with the specified value.

    Args:
        value: The value to wrap in the `Some` instance.

    Returns:
        An `Option` instance representing the `Some` variant, wrapping the specified value.
    """
    def fmap(fn: Callable[[T], T]) -> Option:
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
        return value

    def unwrap_or_else(default: T) -> T:
       return value if value is not Nothing else default

    def or_(other: Option) -> Option:
        return _some(value)

    def or_else(fn: Callable[[], Option]) -> Option:
        return _some(value) if value is not Nothing else fn()

    def and_(other: Option) -> Option:
        return other if value is not Nothing else _none()

    def ok_or(_error: E) -> 'Result[T, E]':
        from flusso import Ok
        return Ok(value)

    def is_some() -> bool:
        return True

    def is_none() -> bool:
        return False

    return Option(
        fmap, and_then, filter_, unwrap, expect, unwrap_or,
        unwrap_or_else, or_, or_else, and_, ok_or, is_some,
        is_none
    )

def _none() -> Option:
    """
    Create a new `None` instance of the OptionMonad pattern.

    Returns:
        An `Option` instance representing the `None` variant.
    """
    def fmap(_: Callable[[T], T]) -> Option:
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

    def unwrap_or_else(fn: Callable[[], T]) -> T:
        return fn()

    def or_(other: Option) -> Option:
        return other

    def or_else(fn: Callable[[], Option]) -> Option:
        return fn()

    def and_(other: Option) -> Option:
        return _none()

    def ok_or(error: E) -> 'Result[T, E]':
        from flusso import Err
        return Err(error)

    def is_some() -> bool:
        return False

    def is_none() -> bool:
        return True

    return Option(
        fmap, and_then, filter_, unwrap, expect, unwrap_or,
        unwrap_or_else, or_, or_else, and_, ok_or, is_some,
        is_none
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
