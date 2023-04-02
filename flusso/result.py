from typing import Callable, Any, NoReturn
from .types import T, E, A
from flusso.primitives.base import Option, Result
from flusso import Some, Nothing


def Ok(value: T) -> Result[T, E]:
    def ok() -> Option[T]:
        return Some(value)

    def err() -> Option[T]:
        return Nothing

    def unwrap() -> T:
        return value

    def unwrap_or(_default: T) -> T:
        return value

    def unwrap_or_else(_fn: Callable[[E], T]) -> T:
        return value

    def unwrap_err():
        raise ValueError("Cannot call `unwrap_err` on `Ok` value")

    def expect(_: A) -> T:
        return value

    def expect_err(message: str):
        raise ValueError(message)

    def fmap(fn: Callable[[T], Result[T, E]]) -> Result[T, E]:
        return Ok(fn(value))

    def fmap_err(_fn: Callable[[E], Result[T, E]]) -> Result[T, E]:
        return Ok(value)

    def and_then(fn: Callable[[T], Result[T, E]]) -> Result[T, E]:
        return fn(value)

    def or_(other: Result[T, E]) -> Result[T, E]:
        return Ok(value)

    def or_else(_fn: Callable[[E], Result[T, E]]) -> Result[T, E]:
        return Ok(value)

    def and_(other: Result[T, E]) -> Result[T, E]:
        return other

    def is_ok() -> bool:
        return True

    def is_err() -> bool:
        return False

    return Result(ok, err, unwrap, unwrap_or, unwrap_or_else, unwrap_err, expect, expect_err, fmap, fmap_err, and_then, or_, or_else, and_, is_ok, is_err)

def Err(value: E) -> Result[T, E]:
    def ok() -> Option[T]:
        return Nothing

    def err() -> Option[E]:
        return Some(value)

    def unwrap() -> T:
        raise ValueError("Cannot call `unwrap` on `Err` value")

    def unwrap_or(default: T) -> T:
        return default

    def unwrap_or_else(fn: Callable[[E], T]) -> T:
        return fn(value)

    def unwrap_err() -> E:
        return value

    def expect(message: str) -> NoReturn:
        raise ValueError(message)

    def expect_err(message: A) -> E:
        return value

    def fmap(fn: Callable[[T], Result[T, E]]) -> Result[T, E]:
        return Err(value)

    def fmap_err(fn: Callable[[E], Result[T, E]]) -> Result[T, E]:
        return Err(fn(value))

    def and_then(fn: Callable[[T], Result[T, E]]) -> Result[T, E]:
        return Err(value)

    def or_(other: Result[T, E]) -> Result[T, E]:
        return other

    def or_else(fn: Callable[[E], Result[T, E]]) -> Result[T, E]:
        return fn(value)

    def and_(other: Result[T, E]) -> Result[T, E]:
        return Err(value)

    def is_ok() -> bool:
        return False

    def is_err() -> bool:
        return True

    return Result(ok, err, unwrap, unwrap_or, unwrap_or_else, unwrap_err, expect, expect_err, fmap, fmap_err, and_then, or_, or_else, and_, is_ok, is_err)


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
