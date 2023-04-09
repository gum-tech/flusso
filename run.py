import math
import asyncio
from typing import Dict, Any
import aiohttp
from flusso.option import Option, Some, Nothing
from flusso.result import Result, Ok, Err
from flusso.async_result import async_result, AsyncResult

# Examples from documentation
# python run.py

# Example I
print("----Example I----")
class User:
    def __init__(self, id: int, fullname: str, username: str):
        self.id = id
        self.fullname = fullname
        self.username = username

users = [
    User(1, "Leonardo Da Vinci", "leo"),
    User(2, "Galileo Galilei", "gaga")
]

def get_user(id: int) -> 'Option[User]':
    user = next((user for user in users if user.id == id), Nothing)
    return Some(user)

def get_username(id: int) -> Option[str]:
    return get_user(id).fmap(lambda user: user.username)


match get_username(1):
    # Matches any `Some` instance and binds its value to the `username` variable
    case Some(username):
        print('User found: {0}'.format(username))

    # Matches `Nothing` instance
    case Nothing:
        print('User not found!')


# Example II
print("----Example II----")
def get_full_name(first_name: str, middle_name: Option[str], last_name: str) -> str:
    match(middle_name):
        case Some(mname):
            print(f"{first_name} {mname} {last_name}")

        # Matches `Nothing` instance
        case Nothing:
            print(f"{first_name} {last_name}")

get_full_name("Galileo", None, "Galilei"); # Galileo Galilei
get_full_name("Leonardo", Some("Da"), "Vinci"); # Leonardo Da Vinci

# Example III
print("----Example III----")
def sine(x: float) -> Option[float]:
        return math.sin(x)

def cube(x: float) -> Option[float]:
    return x * x * x

def inc(x: float) -> Option[float]:
    return x + 1

def double(x: float) -> Option[float]:
    return x ** 2

def divide(x: float, y: float) -> Option[float]:
    return x / y if y > 0 else Nothing

def sineCubedIncDoubleDivideBy10(x: float):
    return (
        Some(x)
        .fmap(sine)
        .fmap(cube)
        .fmap(inc)
        .fmap(double)
        .fmap(lambda x: divide(x, 10))
    )

match(sineCubedIncDoubleDivideBy10(30)):
    case Some(result):
        print(f"`Result is {result}")

    # Matches `Nothing` instance
    case Nothing:
        print("Please check your inputs")


# Example IV
print("----Example IV----")
def divide(numerator: float, denominator: float) -> Result[float,str]:
    if denominator == 0:
        return Err("Division by zero")
    return Ok(numerator / denominator)

def add_one(x: float) -> Result[float,str]:
    return Ok(x + 1)

def compute(numerator: float, denominator: float) -> Result[float,str]:
    return divide(numerator, denominator).and_then(add_one)

match(compute(10, 2)):
    case Ok(result):
        print(result)
    case Err(error):
        print(f"Error #{error}")


match(compute(10, 0)):
    case Ok(result):
        print(result)
    case Err(error):
        print(f"Error #{error}")


# Example V
print("----Example V----")

def compute(numerator: float, denominator: float) -> float:
    return(
        divide(numerator, denominator)
        .and_then(add_one)
        .or_else(lambda error: Ok(0))
        .unwrap()
    )

print(compute(10, 2)) # 6.0
print(compute(10, 0)) # 0.0


# Example VI
print("----Example VI----")
def process_data(data: dict) -> Option[int]:
    return Some(data["value"]) if "value" in data else Nothing

def calculate_percentage(value: int, total: int) -> Result[float, str]:
    return Err("Total cannot be zero") if total == 0 else Ok((value / total) * 100)

# Example data
data = {"value": 10, "total": 50}

# Using pattern matching with Flusso's Option and Result
opt_value = process_data(data)
total = data["total"]

match opt_value:
    case Some(value):
        result = calculate_percentage(value, total)
        match result:
            case Ok(percentage):
                print(f"The percentage is {percentage}%")
            case Err(err_msg):
                print(f"Error: {err_msg}")
    case Nothing:
        print("Value not found in the data")


# Example VII
print("----Example VII----")
@async_result
async def async_fetch_data(url: str) -> Dict[str, Any]:
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status != 200:
                raise ValueError("Failed to fetch data")
            return await response.json()

async def fetch():
    url = "https://jsonplaceholder.typicode.com/todos/1"
    async_result = await async_fetch_data(url)

    match async_result._result:
        case Ok(value):
            print("Fetched data:", value)
        case Err(error):
            print("Error fetching data:", error)

    # Alternatively
    # if async_result.is_ok():
    #     print("Fetched data:", await async_result.unwrap())
    # else:
    #     print("Error fetching data:", await async_result.unwrap_err())

asyncio.run(fetch())


# Example VIII
print("----Example VIII----")
@async_result
async def async_fetch_data(url: str) -> Dict[str, Any]:
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status != 200:
                raise ValueError("Failed to fetch data")
            return await response.json()

async def fetch_do():
    url = "https://jsonplaceholder.typicode.com/todos/1"

    async with (
        AsyncResult.do(fetch_data=async_fetch_data(url)) as fetch_result
    ):

        match fetch_result._result:
            case Ok(data):
                print("Fetched data:", data)
            case Err(error):
                print("Error fetching data:", error)

asyncio.run(fetch_do())

# Example IX
print("----Example IX----")
def add_numbers_result(a: int, b: int) -> Result[int, str]:
    return Ok(a + b)

def multiply_numbers_result(a: int, b: int) -> Result[int, str]:
    return Ok(a * b)

x = 2
y = 3

with (
    Result.do(add_numbers_result(x, y)) as a,
    Result.do(multiply_numbers_result(a, x)) as b,
    Result.do(add_numbers_result(b, y)) as c,
):
    result = Ok(c)

    print(result)

# Example X
print("----Example X----")
def add_numbers_result(a: int, b: int) -> Result[int, str]:
    return Ok(a + b)

def multiply_numbers_result(a: int, b: int) -> Result[int, str]:
    return Ok(a * b)

x = 2
y = 3

with (
    Result.do(add_numbers_result(x, y)) as a,
    Result.do(multiply_numbers_result(a, x)) as b,
    Result.do(add_numbers_result(b, y)) as c,
):
    result = Ok(c)

    print(result)
