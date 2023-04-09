from typing import Any, Dict
import aiohttp
import pytest
from aiohttp import ClientError
from flusso.async_result import AsyncResult, Ok, Err, async_result
from flusso.primitives.exceptions import UnwrapFailedError


# Helper functions for async tests
async def async_identity(value):
    return value

async def async_multiply(value, factor):
    return value * factor

async def async_error(value):
    raise ValueError("An error occurred")

@async_result
async def async_fetch_data(url: str) -> Dict[str, Any]:
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status != 200:
                raise ValueError("Failed to fetch data")
            return await response.json()
 # Tests for AsyncResult
@pytest.mark.asyncio
async def test_async_result_fmap():
    ok_result = Ok(2)
    async_result = AsyncResult(ok_result)

    mapped_result = await async_result.fmap(lambda x: async_multiply(x, 3))
    assert mapped_result == AsyncResult(Ok(6))

    err_result = Err("Error")
    async_err_result = AsyncResult(err_result)

    mapped_err_result = await async_err_result.fmap(lambda x: async_multiply(x, 3))
    assert mapped_err_result == AsyncResult(err_result)

@pytest.mark.asyncio
async def test_async_result_fmap_err():
    err_result = Err(2)
    async_result = AsyncResult(err_result)

    mapped_result = await async_result.fmap_err(lambda x: async_multiply(x, 3))
    assert mapped_result == AsyncResult(Err(6))

    ok_result = Ok("Success")
    async_result = AsyncResult(ok_result)

    mapped_result = await async_result.fmap_err(lambda x: async_multiply(x, 3))
    assert mapped_result == AsyncResult(ok_result)

@pytest.mark.asyncio
async def test_async_result_and_then():
    ok_result = Ok(2)
    async_result = AsyncResult(ok_result)

    new_result = await async_result.and_then(lambda x: AsyncResult(Ok(x * 3)))
    assert new_result == AsyncResult(Ok(6))

    err_result = Err("Error")
    async_err_result = AsyncResult(err_result)
    new_err_result = await async_err_result.and_then(lambda x: AsyncResult(Ok(x * 3)))
    assert new_err_result == AsyncResult(err_result)


@pytest.mark.asyncio
async def test_async_result_or_else():
    err_result = Err(2)
    async_result = AsyncResult(err_result)

    new_result = await async_result.or_else(lambda x: AsyncResult(Ok(x * 3)))
    assert new_result == AsyncResult(Ok(6))

    ok_result = Ok("Success")
    async_result = AsyncResult(ok_result)

    new_result = await async_result.or_else(lambda x: AsyncResult(Ok(x * 3)))
    assert new_result == AsyncResult(ok_result)

# Test unwrapping AsyncResult instances
@pytest.mark.asyncio
async def test_async_result_unwrap():
    ok_result = Ok("Success")
    async_result = AsyncResult(ok_result)

    assert await async_result.unwrap() == "Success"

    err_result = Err("Error")
    async_result = AsyncResult(err_result)

    with pytest.raises(UnwrapFailedError):
        await async_result.unwrap()

@pytest.mark.asyncio
async def test_async_result_unwrap_err():
    err_result = Err("Error")
    async_result = AsyncResult(err_result)

    assert await async_result.unwrap_err() == "Error"

    ok_result = Ok("Success")
    async_result = AsyncResult(ok_result)

    with pytest.raises(UnwrapFailedError):
        await async_result.unwrap_err()

@async_result
async def async_decorated_identity(value):
    return await async_identity(value)

@async_result
async def async_decorated_multiply(value, factor):
    return await async_multiply(value, factor)

@async_result
async def async_decorated_error(value):
    return await async_error(value)

@pytest.mark.asyncio
async def test_async_result_decorator_success():
    result = await async_decorated_identity(42)
    assert result == AsyncResult(Ok(42))

    result = await async_decorated_multiply(6, 7)
    assert result == AsyncResult(Ok(42))

@pytest.mark.asyncio
async def test_async_result_decorator_failure():
    result = await async_decorated_error(42)
    assert isinstance(result._result, Err)

    err_value = result._result.unwrap_err()
    assert isinstance(err_value, ValueError)
    assert str(err_value) == "An error occurred"

@pytest.mark.asyncio
async def test_async_result_do_success():
    url = "https://jsonplaceholder.typicode.com/todos/1"

    async with (
        AsyncResult.do(fetch_data=async_fetch_data(url)) as fetch_result
    ):

        match fetch_result._result:
            case AsyncResult(Ok(data)):
                assert data["id"] == 1
            case AsyncResult(Err(error)):
                assert False, f"Error fetching data: {error}"

@pytest.mark.asyncio
async def test_async_result_do_failure():
    url = "https://nonexistent.example.com"

    async with (
        AsyncResult.do(fetch_data=async_fetch_data(url)) as fetch_result
    ):

        match fetch_result._result:
            case AsyncResult(Ok(data)):
                assert False, f"Expected error but received data: {data}"
            case AsyncResult(Err(error)):
                assert isinstance(error, ClientError)
