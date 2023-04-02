from typing import Generic, Callable, Generator
from dataclasses import dataclass
from contextlib import contextmanager
from flusso.types import T, E, A
import logging


@dataclass
class Option(Generic[T]):
    """
    An implementation of the Option Monad pattern, which represents an optional value that may or may not be present.
    """
    fmap: Callable[[T], 'Option']
    and_then: Callable[[Callable[[T], 'Option']], 'Option']
    filter_: Callable[[Callable[[T], bool]], 'Option']
    unwrap: Callable[[], T]
    expect: Callable[[str], T]
    unwrap_or: Callable[[], T]
    unwrap_or_else: Callable[[T], T]
    or_: Callable[['Option'], 'Option']
    or_else: Callable[[Callable[[], 'Option']], 'Option']
    and_: Callable[['Option'], 'Option']
    ok_or: Callable[[E], 'Result[T, E]']
    is_some: Callable[[], bool]
    is_none: Callable[[], bool]

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




@dataclass
class Result(Generic[T, E]):
    ok: Callable[[], Option[T]]
    err: Callable[[], Option[E]]
    unwrap: Callable[[], T]
    unwrap_or: Callable[[T], T]
    unwrap_or_else: Callable[[Callable[[E], T]], T]
    unwrap_err: Callable[[], E]
    expect: Callable[[A], T]
    expect_err: Callable[[str], E]
    fmap: Callable[[Callable[[T], 'Result[T, E]']], 'Result[T, E]']
    fmap_err: Callable[[Callable[[E], 'Result[T, E]']], 'Result[T, E]']
    and_then: Callable[[Callable[[T], 'Result[T,E]']], 'Result[T, E]']
    or_: Callable[['Result[T, E]'], 'Result[T, E]']
    or_else: Callable[[Callable[[E], 'Result[T, E]']], 'Result[T, E]']
    and_: Callable[['Result[T, E]'], 'Result[T, E]']
    is_ok: Callable[[], bool]
    is_err: Callable[[], bool]

    def __eq__(self, other: 'Result[T, E]') -> bool:
        """
        Compare this Result instance with another instance.

        Returns:
            True if both instances are of the same variant (Ok or Err) and have the same value, False otherwise.
        """
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
