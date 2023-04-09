import asyncio
from contextlib import asynccontextmanager
from functools import wraps
from typing import Callable, Any, AsyncIterable, Awaitable, Generic, Union, Coroutine, Dict
from .result import Result, Ok, Err
from .types import T, E, A

class AsyncResult(Generic[T, E]):
    def __init__(self, result: Result[T, E]):
        """
        Initialize an AsyncResult instance.

        :param result: A Result instance containing either a value or an error.
        """
        self._result = result

    @classmethod
    @asynccontextmanager
    async def do(cls, **kwargs: Awaitable['AsyncResult[T, E]']) -> AsyncIterable['AsyncResult[Dict[str, T], E]']:
        """
        An asynchronous context manager for chaining async computations using do notation for AsyncResult.

        This method allows you to pass multiple async functions that return AsyncResult objects as keyword
        arguments. It will execute them sequentially, stopping at the first error encountered, if any.
        The context manager will yield an AsyncResult containing either a dictionary of the successful results
        or an error, depending on the outcome.

        Usage example:

        async with AsyncResult.do(
            data=async_fetch_data(url)
        ) as fetch_result:

            match fetch_result._result:
                case Ok(data):
                    print("Fetched data:", data)
                case Err(error):
                    print("Error fetching data:", error)

        :param kwargs: Asynchronous functions returning AsyncResult objects as keyword arguments.
        :return: An asynchronous iterable yielding an AsyncResult containing either a dictionary
                of the successful results or an error.
        """
        results = {}
        try:
            for name, coro in kwargs.items():
                async_result = await coro
                if async_result.is_err():
                    yield cls(Err(await async_result.unwrap_err()))
                    return
                else:
                    results[name] = await async_result.unwrap()
            yield cls(Ok(results))
        except Exception as e:
            yield cls(Err(e))


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
