from typing import Callable, NoReturn
from dataclasses import dataclass
from .types import T, E, A
from flusso.primitives.base import Option, Result
from flusso.primitives.exceptions import UnwrapFailedError


@dataclass
class Some(Option[T]):
    value: T

    def __new__(cls, value: T) -> Option[T]:
        """
        Create a new `Some` instance, or return `Nothing` if the provided value is `None` or `Nothing`.
        """
        return Nothing if value is None or value is Nothing else super().__new__(cls)

    def fmap(self, fn: Callable[[T], A]) -> Option[A]:
        """
        Apply the given function to the value and return a new `Some` instance with the result, or `Nothing` if the value is `None` or `Nothing`.
        """
        return Some(fn(self.value))

    def and_then(self, fn: Callable[[T], Option[A]]) -> Option[A]:
        """
        Apply the given function to the value and return the resulting `Option` instance.
        """
        return fn(self.value)

    def filter_by_predicate(self, predicate: Callable[[T], bool]) -> Option[T]:
        """
        Apply the given predicate to the value and return `Some(value)` if the predicate returns `True`, or `Nothing` otherwise.
        """
        return Some(self.value) if predicate(self.value) else Nothing

    def unwrap(self) -> T:
        """
        Return the contained value if it is `Some`, otherwise raise a `ValueError`.
        """
        return self.value

    def expect(self, msg: str) -> T:
        """
        Return the contained value if it is `Some`, otherwise raise an `Exception` with the provided message.
        """
        return self.value

    def unwrap_or(self, _val: A) -> T:
        """
        Return the contained value if it is `Some`, otherwise return the provided default value.
        """
        return self.value

    def unwrap_or_else(self, fn: Callable[[], T]) -> T:
        """
        Return the contained value if it is `Some`, otherwise call the provided function and return its result.
        """
        return self.value

    def value_or(self, other: Option[A]) -> Option[T]:
        """
        Return the `Some` instance if it has a value, otherwise return the provided `Option` instance.
        """
        return self

    def or_else(self, fn: Callable[[], Option[A]]) -> Option[T]:
        """
        Return the `Some` instance if it has a value, otherwise call the provided function and return its result.
        """
        return self

    def value_and(self, other: Option[A]) -> Option[A]:
        """
        Return the provided `Option` instance if the current instance has a value, otherwise return `Nothing`.
        """
        return other

    def ok_or(self, _error: 'E') -> Result[T, E]:
        """
        Return an `Ok` instance containing the value if it is `Some`, otherwise return an `Err` instance containing the provided error.
        """
        from flusso.result import Ok
        return Ok(self.value)

    def is_some(self) -> bool:
        """
        Return `True` if the instance is a `Some` variant, otherwise return `False`.
        """
        return True

    def is_none(self) -> bool:
        """
        Return `True` if the instance is a `Nothing` variant, otherwise return `False`.
        """
        return False


@dataclass
class Nothing(Option[T]):

    def fmap(self, _: Callable[[T], A]) -> Option[A]:
        """
        Do not apply the given function and return `Nothing`.
        """
        return self


    def and_then(self, _: Callable[[T], Option[A]]) -> Option[A]:
        """
        Do not apply the given function and return `Nothing`.
        """
        return self

    def filter_by_predicate(self, _: Callable[[T], bool]) -> Option[T]:
        """
        Do not apply the given predicate and return `Nothing`.
        """
        return self

    def unwrap(self) -> NoReturn:
        """
        Raise a `UnwrapFailedError` since `Nothing` has no value to unwrap.
        """
        # raise ValueError("Cannot call `unwrap` on `Nothing` value")
        raise UnwrapFailedError(self)

    def expect(self, msg: str) -> NoReturn:
        """
        Raise a `ValueError` with the provided message since `Nothing` has no value.
        """
        raise ValueError(msg)

    def unwrap_or(self, other: A) -> T:
        """
        Return the provided default value since `Nothing` has no value.
        """
        return other

    def unwrap_or_else(self, fn: Callable[[], T]) -> T:
        """
        Call the provided function and return its result since `Nothing` has no value.
        """
        return fn()

    def value_or(self, other: Option[A]) -> Option[A]:
        """
        Return the provided `Option` instance since `Nothing` has no value.
        """
        return other

    def or_else(self, fn: Callable[[], Option[A]]) -> Option[A]:
        """
        Call the provided function and return its result since `Nothing` has no value.
        """
        return fn()

    def value_and(self, other: Option[A]) -> Option[T]:
        """
        Return `Nothing` since the current instance has no value.
        """
        return self

    def ok_or(self, error: 'E') -> Result[T, E]:
        """
        Return an `Err` instance containing the provided error since `Nothing` has no value.
        """
        from flusso.result import Err
        return Err(error)

    def is_some(self) -> bool:
        """
        Return `False` since the instance is not a `Some` variant.
        """
        return False

    def is_none(self) -> bool:
        """
        Return `True` since the instance is a `Nothing` variant.
        """
        return True

# Singleton pattern for Nothing
Nothing = Nothing()

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
