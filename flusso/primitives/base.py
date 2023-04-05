from typing import Generic, Callable, Generator, NoReturn
from contextlib import contextmanager
from flusso.types import T, E, A
import logging


class Option(Generic[T]):
    """
    An Interface implementation of the Option Monad pattern, which represents an optional value that may or may not be present.
    """
    def fmap(self, fn: Callable[[T], A]) -> 'Option[A]':
        raise NotImplementedError

    def and_then(self, fn: Callable[[T], 'Option[A]']) -> 'Option[A]':
        raise NotImplementedError

    def filter_by_predicate(self, fn: Callable[[T], bool]) -> 'Option[T]':
        raise NotImplementedError

    def unwrap(self) -> T | NoReturn:
        raise NotImplementedError

    def expect(self, msg: str) -> T | NoReturn:
        raise NotImplementedError

    def unwrap_or(self, _val: A) -> T:
        raise NotImplementedError

    def unwrap_or_else(self, fn: Callable[[], T]) -> T:
        raise NotImplementedError

    def value_or(self, other: 'Option[T | A]') -> 'Option[T | A]':
        raise NotImplementedError

    def or_else(self, fn: Callable[[], 'Option[A]']) -> 'Option[T | A]':
        raise NotImplementedError

    def value_and(self, other: 'Option[A]') -> 'Option[T | A]':
        raise NotImplementedError

    def ok_or(self, _error: 'E') -> 'Result[T, E]':
        raise NotImplementedError

    def is_some(self) -> bool:
        raise NotImplementedError

    def is_none(self) -> bool:
        raise NotImplementedError

    def __eq__(self, other: object) -> bool:
        """
        Compare this Option instance with another instance.

        Returns:
            True if both instances are None or both have the same value, False otherwise.
        """
        if not isinstance(other, Option):
            return False

        if self.is_none() and other.is_none():
            return True
        elif self.is_some() and other.is_some():
            return self.unwrap() == other.unwrap()
        else:
            return False

    @classmethod
    @contextmanager
    def do(cls, option: 'Option[T]') -> Generator[T, None, None]:
        if option.is_some():
            try:
                yield option.unwrap()
            except Exception as e:
                logging.error(f"An error occurred while unwrapping the Option value: {e}")

        else:
            return


class Result(Generic[T, E]):
    def ok(self) -> Option[T]:
        raise NotImplementedError

    def err(self) -> Option[E]:
        raise NotImplementedError

    def unwrap(self) -> T | NoReturn:
        raise NotImplementedError

    def unwrap_or(self, default: T) -> T:
        raise NotImplementedError

    def unwrap_or_else(self, fn: Callable[[E], T]) -> T:
        raise NotImplementedError

    def unwrap_err(self) -> E | NoReturn:
        raise NotImplementedError

    def expect(self, msg: str) -> T | NoReturn:
        raise NotImplementedError

    def expect_err(self, msg: str) -> E | NoReturn:
        raise NotImplementedError

    def fmap(self, fn: Callable[[T], A]) -> 'Result[A, E]':
        raise NotImplementedError

    def fmap_err(self, fn: Callable[[E], A]) -> 'Result[T, A]':
        raise NotImplementedError

    def and_then(self, fn: Callable[[T], 'Result[A, E]']) -> 'Result[A, E]':
        raise NotImplementedError

    def value_or(self, other: 'Result[A, E]') -> 'Result[T | A, E]':
        raise NotImplementedError

    def or_else(self, fn: Callable[[E], 'Result[A, E]']) -> 'Result[T, A | E]':
        raise NotImplementedError

    def value_and(self, other: 'Result[A, E]') -> 'Result[T | A, E]':
        raise NotImplementedError

    def is_ok(self) -> bool:
        raise NotImplementedError

    def is_err(self) -> bool:
        raise NotImplementedError

    def __eq__(self, other: object) -> bool:
        """
        Compare this Result instance with another instance.

        Returns:
            True if both instances are of the same variant (Ok or Err) and have the same value, False otherwise.
        """
        if not isinstance(other, Result):
            return False

        if self.is_ok() and other.is_ok():
            return self.ok().unwrap() == other.ok().unwrap()
        elif self.is_err() and other.is_err():
            return self.err().unwrap() == other.err().unwrap()
        else:
            return False

    @classmethod
    @contextmanager
    def do(cls, result: 'Result[T, E]') -> Generator[T, None, None]:
        if result.is_ok():
            try:
                yield result.unwrap()
            except Exception as e:
                logging.error(f"An error occurred while unwrapping the Result value: {e}")
        else:
            return
