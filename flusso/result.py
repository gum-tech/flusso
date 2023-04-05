from typing import Callable, Any, NoReturn
from dataclasses import dataclass
from .types import T, E, A
from flusso.primitives.base import Option, Result
from flusso.primitives.exceptions import UnwrapFailedError
from flusso.option import Some, Nothing

@dataclass
class Ok(Result[T, E]):
    value: T

    def ok(self) -> Option[T]:
        """
        Returns the wrapped value as a `Some` instance.
        """
        return Some(self.value)

    def err(self) -> Option[E]:
        """
        Returns a `Nothing` instance for `Err` variant.
        """
        return Nothing

    def unwrap(self) -> T:
        """
        Returns the wrapped value.
        """
        return self.value

    def unwrap_or(self, _default: T) -> T:
        """
        Returns the wrapped value ignoring the default value.
        """
        return self.value

    def unwrap_or_else(self, _fn: Callable[[E], T]) -> T:
        """
        Returns the wrapped value ignoring the provided function.
        """
        return self.value

    def unwrap_err(self) -> NoReturn:
        """
        Raises a `UnwrapFailedError` as unwrapping error is not allowed on `Ok` value.
        """
        # raise ValueError("Cannot call `unwrap_err` on `Ok` value")
        raise UnwrapFailedError(self)

    def expect(self, _: str) -> T:
        """
        Returns the wrapped value ignoring the error message.
        """
        return self.value

    def expect_err(self, msg: str) -> NoReturn:
        """
        Raises a `ValueError` with the provided error message.
        """
        raise ValueError(msg)

    def fmap(self, fn: Callable[[T], A]) -> Result[A, E]:
        """
        Applies the given function to the wrapped value and returns a new `Ok` instance with the result.
        """
        return Ok(fn(self.value))

    def fmap_err(self, _fn: Callable[[E], A]) -> Result[T, A]:
        """
        Ignores the given function and returns the current `Ok` instance unchanged.
        """
        return self

    def and_then(self, fn: Callable[[T], Result[A, E]]) -> Result[A, E]:
        """
        Applies the given function to the wrapped value and returns the resulting `Result` instance.
        """
        return fn(self.value)

    def value_or(self, other: Result[A, E]) -> Result[A, E]:
        """
        Returns the current `Ok` instance ignoring the other `Result` instance.
        """
        return self

    def or_else(self, _fn: Callable[[E], Result[A, E]]) -> Result[T | A, E]:
        """
        Ignores the given function and returns the current `Ok` instance unchanged.
        """
        return self

    def value_and(self, other: Result[A, E]) -> Result[A, E]:
        """
        Returns the other `Result` instance.
        """
        return other

    def is_ok(self) -> bool:
        """
        Returns `True` as the current instance is `Ok`.
        """
        return True

    def is_err(self) -> bool:
        """
        Returns `False` as the current instance is not `Err`.
        """
        return False


@dataclass
class Err(Result[T, E]):
    value: E

    def ok(self) -> Option[T]:
        """
        Returns a `Nothing` instance for `Ok` variant.
        """
        return Nothing

    def err(self) -> Option[E]:
        """
        Returns the wrapped error as a `Some` instance.
        """
        return Some(self.value)

    def unwrap(self) -> NoReturn:
        """
        Raises a `UnwrapFailedError` as unwrapping is not allowed on `Err` value.
        """
        # raise ValueError("Cannot call `unwrap` on `Err` value")
        raise UnwrapFailedError(self)


    def unwrap_or(self, default: T) -> T:
        """
        Returns the provided default value.
        """
        return default

    def unwrap_or_else(self, fn: Callable[[E], T]) -> T:
        """
        Applies the given function to the wrapped error and returns the result.
        """
        return fn(self.value)

    def unwrap_err(self) -> E:
        """
        Returns the wrapped error value.
        """
        return self.value

    def expect(self, msg: str) -> NoReturn:
        """
        Raises a `ValueError` with the provided error message.
        """
        raise ValueError(msg)

    def expect_err(self, _: str) -> E:
        """
        Returns the wrapped error value ignoring the error message.
        """
        return self.value

    def fmap(self, _fn: Callable[[T], A]) -> Result[A, E]:
        """
        Ignores the given function and returns the current `Err` instance unchanged.
        """
        return self

    def fmap_err(self, fn: Callable[[E], A]) -> Result[T, A]:
        """
        Applies the given function to the wrapped error and returns a new `Err` instance with the result.
        """
        return Err(fn(self.value))

    def and_then(self, _fn: Callable[[T], Result[A, E]]) -> Result[A, E]:
        """
        Ignores the given function and returns the current `Err` instance unchanged.
        """
        return self

    def value_or(self, other: Result[A, E]) -> Result[A, E]:
        """
        Returns the other `Result` instance.
        """
        return other

    def or_else(self, fn: Callable[[E], Result[A, E]]) -> Result[T | A, E]:
        """
        Applies the given function to the wrapped error and returns the resulting `Result` instance.
        """
        return fn(self.value)

    def value_and(self, other: Result[A, E]) -> Result[T | A, E]:
        """
        Returns the current `Err` instance ignoring the other `Result` instance.
        """
        return self

    def is_ok(self) -> bool:
        """
        Returns `False` as the current instance is not `Ok`.
        """
        return False

    def is_err(self) -> bool:
        """
        Returns `True` as the current instance is `Err`.
        """
        return True


# Result decorator
def result(fn: Callable[..., Any]) -> Callable[..., Result[Any, Any]]:
    """
    A decorator that takes a function and returns a new function that returns an `Result` instance.

    If the original function returns `None`, the returned function will return an instance of the `Err` variant.
    Otherwise, the returned function will return a new instance of the `Ok` variant, wrapping the result of the original function.

    Args:
        fn: The function to decorate.

    Returns:
        A new function that returns an `Result` instance.
    """
    def wrapper(*args, **kwargs) -> Result[Any, Any]:
        result = fn(*args, **kwargs)
        return Err(result) if result is None else Ok(result)
    return wrapper
