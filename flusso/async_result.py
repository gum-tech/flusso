import asyncio
from functools import wraps
from typing import Callable, Any, Awaitable, Generic, Union, Coroutine
from .result import Result, Ok, Err
from .types import T, E, A

class AsyncResult(Generic[T, E]):
    def __init__(self, result: Result[T, E]):
        """
        Initialize an AsyncResult instance.

        :param result: A Result instance containing either a value or an error.
        """
        self._result = result

    @staticmethod
    async def _call_and_await_if_needed(fn: Callable[..., Awaitable[A]], value: Union[T, E]) -> A:
        """
        Helper method to call a function with a value, and await the result if it's a coroutine.

        :param fn: The function to call with the value.
        :param value: The value to pass to the function.
        :return: The result of the function call, awaited if it's a coroutine.
        """
        result = fn(value)
        return await result if asyncio.iscoroutine(result) else result

    async def fmap(self, fn: Callable[[T], Awaitable[A]]) -> 'AsyncResult[A, E]':
        """
        Transform the value within the AsyncResult if it's an Ok instance, otherwise, keep the error.

        :param fn: A function to apply to the value if it's an Ok instance.
        :return: A new AsyncResult with the transformed value or the original error.
        """
        if not self._result.is_ok():
            return self
        new_result = await self._call_and_await_if_needed(fn, self._result.unwrap())
        return AsyncResult(Ok(new_result))

    async def fmap_err(self, fn: Callable[[E], Awaitable[A]]) -> 'AsyncResult[T, A]':
        """
        Transform the error within the AsyncResult if it's an Err instance, otherwise, keep the value.

        :param fn: A function to apply to the error if it's an Err instance.
        :return: A new AsyncResult with the transformed error or the original value.
        """
        if not self._result.is_err():
            return self
        new_result = await self._call_and_await_if_needed(fn, self._result.unwrap_err())
        return AsyncResult(Err(new_result))

    async def and_then(self, fn: Callable[[T], Awaitable['AsyncResult[A, E]']]) -> 'AsyncResult[A, E]':
        """
        Chain a function that returns an AsyncResult, only called if the current AsyncResult is an Ok instance.

        :param fn: A function to call with the value if it's an Ok instance.
        :return: A new AsyncResult with the result of the function call, or the original error.
        """
        if self._result.is_ok():
            return await self._call_and_await_if_needed(fn, self._result.unwrap())
        else:
            return self

    async def or_else(self, fn: Callable[[E], Awaitable['AsyncResult[A, E]']]) -> 'AsyncResult[T, A]':
        """
        Chain a function that returns an AsyncResult, only called if the current AsyncResult is an Err instance.

        :param fn: A function to call with the error if it's an Err instance.
        :return: A new AsyncResult with the result of the function call, or the original value.
        """
        if self._result.is_err():
            return await self._call_and_await_if_needed(fn, self._result.unwrap_err())
        else:
            return self

    async def unwrap(self) -> T:
        """
        Unwrap the value within the AsyncResult if it's an Ok instance, raising an exception if it's an Err instance.

        :return: The value within the AsyncResult.
        :raises: An exception if the AsyncResult contains an error.
        """
        return self._result.unwrap()

    async def unwrap_err(self) -> E:
        """
        Unwrap the error within the AsyncResult if it's an Err instance, raising an exception if it's an Ok instance.

        :return: The error within the AsyncResult.
        :raises: An exception if the AsyncResult contains a value.
        """
        return self._result.unwrap_err()

    def is_ok(self) -> bool:
        """
        Check if the AsyncResult contains an Ok instance.

        :return: True if the AsyncResult contains an Ok instance, False otherwise.
        """
        return self._result.is_ok()

    def is_err(self) -> bool:
        """
        Check if the AsyncResult contains an Err instance.

        :return: True if the AsyncResult contains an Err instance, False otherwise.
        """
        return self._result.is_err()

    def __eq__(self, other: object) -> bool:
        """
        Check if two AsyncResult instances are equal.

        :param other: The other AsyncResult instance to compare.
        :return: True if the two AsyncResult instances are equal, False otherwise.
        """
        return (
            self._result == other._result
            if isinstance(other, AsyncResult)
            else False
        )

def async_result(fn: Callable[..., Awaitable[T]]) -> Callable[..., Coroutine[T, Any, AsyncResult[T, E]]]:
    """
    A decorator that wraps an async function to catch any exceptions and return an AsyncResult.

    :param fn: The async function to wrap.
    :return: The wrapped async function.
    """
    @wraps(fn)
    async def wrapper(*args: Any, **kwargs: Any) -> AsyncResult[T, E]:
        try:
            result = await fn(*args, **kwargs)
            return AsyncResult(Ok(result))
        except Exception as e:
            return AsyncResult(Err(e))
    return wrapper
