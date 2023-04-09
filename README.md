## What is flusso?

`flusso` is a library for Python that aims to safely handle exceptions and missing values, similar to how Rust handles them with its `Option` and `Result` types.

In short, Flusso empowers you to craft Python code that is:
- Free from None values
- Devoid of exceptions

In python, `None` represents intentionally missing values and exceptions are used for handling errors.

Python skips using missing values and exceptions can lead to issues and bugs like:

- NoneType errors
- runtime errors
- unexpected behaviour
- unhandled exceptions
- sensitive data leakages through exceptions
- race conditions
- and so on.

Instead, Python provides two special generic `Option` and `Result` to deal with the above cases.

flusso implements the `Option` & `Result` types for python.

## Why should you use flusso?
There are already several excellent libraries that implement functional patterns in python. Why flusso?

These libraries are usually general-purpose toolkits aiming to implement all the functional programming patterns and abstractions. flusso has a more focused goal. We wanted a library specifically to ~~dominate~~ **safely** handle exceptions and missing values (None). The same way as it’s implemented in Rust.

Other distinguishing features of flusso:

- Zero dependencies: flusso has no external dependencies.
- Practical: • Rather than bore you with all the Monad / Category theory talk, we focus on the practical applications of Monads in a way you can use today. Just as you don’t need to understand group theory to do basic arithmetic, you don’t need to understand monad theory to use flusso.
- Leverages Python's pattern matching for concise and expressive code
- Provides an intuitive way to handle optional values and error handling
- Eliminates the need for writing code with None or exceptions
- Compatible with the latest Python features and best practices
- Fully typed with annotations, following PEP 484 guidelines

Convinced?

Great! Let’s get started.

## Installation
```markdown
> pip install flusso
```

If you find this package useful, please click the star button *✨*!

<div id="toc"></div>

## Table of contents
- `Option[T]`
    - [Introduction](#introduction)
    - [Basic usage](#basic-usage)
    - [Option decorator](#option-decorator)
    - [Benefits](#benefits)
- `Result<T,E>`
    - [Introduction](#introduction-1)
    - [Basic usage](#basic-usage-1)
    - [Result decorator](#result-decorator)
    - [Benefits](#benefits-1)
- `AsyncResult<T,E>`
    - [Introduction](#introduction-2)
    - [Basic usage](#basic-usage-2)
    - [AsyncResult decorator](#async_result-decorator)
    - [Benefits](#benefits-2)
- Utils
    - [Flatten](#flatten)
    - [Pattern matching](#pattern-matching)
    - [Do Notation](#do)


## `Option<T>`

### **Introduction**

“Null has led to innumerable errors, vulnerabilities, and system crashes, which have probably caused a billion dollars of pain and damage in the last forty years.” - Tony Hoare, the inventor of null

**`None`** values  can be difficult to detect and handle correctly. When a **`None`** value is encountered, it may not be immediately clear why it is there or how to handle it. This can lead to bugs that are hard to diagnose and fix.

Another problem with **`None`** values is that they can cause runtime errors if they are not properly handled. For example, if a program attempts to access a property of an object that is **`None`**, it will often raise a **`NullPointerException`** or similar error. These errors can be difficult to anticipate and debug, especially if they occur deep in the codebase or if there are many layers of abstraction involved.

To avoid these problems, we use Option as an alternative way of representing the absence of a value or the lack of an object reference.

### A brief background on Option Monad
A monad is a design pattern that allows for the creation of sequenced computations, or "actions," that can be combined in a predictable way.

The option monad is a specific type of monad that represents computations that may or may not return a value.

Option monad types allow for the explicit representation of the possibility of a missing value, and they provide methods for handling these cases in a predictable and composable way.

The option monad is usually implemented as an algebraic data type with two cases: **`Some`** and **`Nothing`**. The **`Some`** case represents a computation that has a value, and it is parameterized by the type of the value. The **`Nothing`** case represents a computation that has a missing value.


Option monad helps us safely handle missing values in a predictable and composable way without being afraid of the null pointer exception, runtime errors, and unexpected behaviour in our code.

[⬆️  Back to top](#toc)


## **Basic usage**

 **Example I**

  Let’s start with a common example you see in many codebases today.

  ```python
    class User:
        def __init__(self, id: int, fullname: str, username: str):
            self.id = id
            self.fullname = fullname
            self.username = username

        users = [
            User(1, "Leonardo Da Vinci", "leo"),
            User(2, "Galileo Galilei", "gaga")
        ]

    def get_user(id: int) -> Union[User, None]:
        return next((user for user in users if user.id == id), None)

    def get_user_name(id: int) -> Union[str, None]:
        user = get_user(id)
        if user is None:
            return None
        return user.username

    username = get_user_name(1)

    if username is not None:
        print(username)
    else:
        print("User not found")
  ```

  This code focuses on telling the computer how to perform a task, step by step. It involves specifying the sequence of actions that the computer should take and the specific operations it should perform at each step.

  The code also uses None to define missing values. Even with a simple example like this, it’s not immediately clear where the None is coming from when we check if the username is None. In large codebases, this can be a nightmare to diagnose and fix.

  However, since this code style is more familiar and follows a more traditional control flow, it can be easier to understand for most programmers.

  Let's rewrite this with a declarative style using flusso

  ```python
    from flusso.option import Option, Some, Nothing

    class User:
        def __init__(self, id: int, fullname: str, username: str):
            self.id = id
            self.fullname = fullname
            self.username = username

    users = [
        User(1, "Leonardo Da Vinci", "leo"),
        User(2, "Galileo Galilei", "gaga")
    ]

    def get_user(id: int) -> Option[User]:
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

    # Alternatively
    # if username.is_some():
    #     print(username.unwrap())
    # else:
    #     print("User not found")
  ```

  This code style focuses on describing the input (the user's ID) and the desired output (the username).
  The match function handles the case where the user is not found by providing a default value (in this case, a message saying "User not found").

  With flusso, we have  successfully handled missing values in a predictable and composable way.

   **Example II**

  Let’s look at another example of using option to handle optional values.

  if the value of an object can be empty or optional like the `middle_name`of `User` in the following example, we can set its data type as an `Option`type.

  ```python
   from flusso.option import Option, Some, Nothing

    def get_full_name(first_name: str, middle_name: Option[str], last_name: str) -> str:
        match(middle_name):
            case Some(mname):
                print(f"{first_name} {mname} {last_name}")

            # Matches `Nothing` instance
            case Nothing:
                print(f"{first_name} {last_name}")

    get_full_name("Galileo", None, "Galilei"); # Galileo Galilei
    get_full_name("Leonardo", Some("Da"), "Vinci"); # Leonardo Da Vinci
  ```
   Let’s look at another example by chaining calculations

  ```python
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
  ```
[⬆️  Back to top](#toc)

### **Benefits**

  There are several reasons why you might want to use flusso.option in your code:

  1. To avoid `NoneType` errors: As mentioned earlier, the Option is a way of representing optional values in a type-safe way. This can help you avoid NoneType errors by allowing you to explicitly handle the absence of a value in your code.
  2. To make your code more readable: Using the Option can make your code more readable, because it clearly indicates when a value may be absent. This can make it easier for other developers to understand your code and can reduce the need for comments explaining how `None` values are handled.
  3. To improve code reliability: By explicitly handling the absence of a value, you can make your code more reliable and less prone to runtime errors.
  4. To improve code maintainability: Using the Option can make your code more maintainable, because it encourages a clear and explicit handling of optional values. This can make it easier to modify and extend your code in the future.
  5. To make you write code that is more declarative and less imperative. This can make your code easier to understand and test.


 ---

  If you find this package useful, please click the star button *✨*!

  [⬆️  Back to top](#toc)


## Option decorator
When working with functions that return Optional values, it's common to encounter numerous if x is not None: checks in your code. Flusso comes to the rescue with the @option decorator, which simplifies this process by converting functions that return Optional values to return Option instances instead.

Here's how to use the @option decorator in Flusso:
  ```python
    from typing import Optional
    from flusso.option import Option, Some, option

    @option
    def find_even_number(numbers: list[int]) -> Optional[int]:
        for number in numbers:
            if number % 2 == 0:
                return number
        return None

    result: Option[int] = find_even_number([1, 3, 5, 7, 2, 4])
    assert result == Some(2)
  ```

## Result[T, E]

### **Introduction**

  Exceptions are a mechanism for handling errors and exceptional circumstances in many programming languages. When an exception is thrown, the normal flow of control in the program is interrupted, and the program tries to find an exception handler to handle the exception. If no appropriate exception handler is found, the program may crash or produce unexpected results.

  There are several problems with using exceptions for error handling:

  1. Exceptions can be difficult to anticipate: Exceptions can be thrown anywhere in the code, making it difficult to anticipate where they might occur and how to handle them. This can make it hard to write robust, reliable code.
  2. Exceptions can be hard to debug: When an exception is thrown, the normal flow of control in the program is interrupted, making it difficult to trace the cause of the exception and fix the error.
  3. Exceptions can make code harder to read: When exceptions are used extensively, the code can become cluttered with try-except blocks, making it harder to understand what is happening.
  4. Exceptions can have performance overhead: Throwing and catching exceptions can have a significant performance overhead, especially if they are used extensively.

  Result is a way to handle errors and exceptions in a more predictable and structured way. Instead of using exceptions, the result type uses a variant-based approach, with separate **`Ok`** and **`Err`** variants representing successful and unsuccessful computations, respectively. This allows for more predictable error handling and makes it easier to anticipate and handle errors in the code.

  This provides a more predictable and structured approach to error handling, which can improve the reliability, readability, performance, and composability of code.

  [⬆️  Back to top](#toc)

### **Basic usage**

  Let’s start with an example of how you might use exceptions in Python.

  ```python
    def divide(numerator: float, denominator: float) -> float:
        if denominator == 0:
            raise ZeroDivisionError("Division by zero")
        return numerator / denominator

    def add_one(x: float) -> float:
        return x + 1

    def compute(numerator: float, denominator: float) -> float:
        try:
            result = divide(numerator, denominator)
            result = add_one(result)
            return result
        except ZeroDivisionError:
            return 0

    print(compute(10, 2)) # 6.0
    print(compute(10, 0)) # 0
  ```

  In this example, the **`divide`** function throws an exception if the denominator is zero, and the **`compute`** function uses a try-except block to handle the exception and return zero if it occurs.

  Let rewrite this with a declarative style using flusso

  ```python

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

  ```

  ```python
    match(compute(10, 0)):
        case Ok(result):
            print(result)
        case Err(error):
            print(f"Error #{error}")
  ```

  In this example, the **`divide`** function returns a result type representing the result of a division operation. If the denominator is zero, it returns an **`Err`** variant with an error message. If the denominator is non-zero, it returns an **`Ok`** variant holding the result of the division.

  The **`add_one`** function takes a number and returns a result type representing the result of adding one to that number. In this case, it always returns an **`Ok`** variant.

  `and_then` is used to chain the **`divide`** and **`add_one`** functions together, passing the result of the **`divide`** function as input to the **`add_one`** function. If the **`divide`** function returns an **`Err`** variant, **`and_then`** short-circuits the chain and returns the **`Err`** variant immediately.

  You can also use **`or_else`** to handle any errors that might occur in the computation. If the result type is an **`Err`** variant, the provided fallback function is called with the error as input and its result is returned.

  ```python
    def compute(numerator: float, denominator: float) -> float:
        return(
            divide(numerator, denominator)
            .and_then(add_one)
            .or_else(lambda error: Ok(0))
            .unwrap()
        )

    print(compute(10, 2)) # 6.0
    print(compute(10, 0)) # 0.0
  ```
[⬆️  Back to top](#toc)

## Result decorator
When working with functions that might raise exceptions, it's typical to see numerous try-except blocks scattered throughout your code. Flusso swoops in to save the day with the @result decorator, which streamlines this process by converting functions that raise exceptions into functions that return Result instances instead.

Here's how to use the @result decorator in Flusso:
  ```python
    from flusso import Result, Ok, Err, result

    @result
    def divide_numbers(numerator: float, denominator: float) -> Union[float, str]:
        if denominator == 0:
            return "Division by zero is not allowed"
        return numerator / denominator

    result: Result[float, str] = divide_numbers(10, 2)
    assert result == Ok(5.0)
  ```


### **Benefits**

There are several reasons why you might choose to use the flusso.result in your code:

1. Improved error handling: Result provides a structured way to handle errors and exceptions, allowing for more predictable and easy-to-reason-about code.
2. Improved code readability: By using Result, it is clear to anyone reading the code that a computation may or may not be successful, and what to do in each case. This can make the code easier to understand and maintain.
3. Improved code reliability: By using the Result, it is easier to ensure that errors and exceptions are properly handled and do not result in unexpected behavior or crashes.
4. Improved code composability: Result allows for the chaining of operations. This can make it easier to build up complex computations from simpler ones.

[⬆️  Back to top](#toc)

## AsyncResult[T, E]

### **Introduction**

  `AsyncResult` is a utility class for working with asynchronous operations that may result in a success or an error. It is built on top of the Result class, which represents a synchronous operation's result. The AsyncResult class is useful for chaining, transforming, and handling results from asynchronous operations.

  [⬆️  Back to top](#toc)

### **Basic usage**

  Let’s start with an example of how you might use exceptions in Python.

  ```python
    from flusso.async_result import async_result, Ok, Err

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

  ```
AsyncResult provides several methods for working with and transforming the result:

- fmap(fn): Transform the successful value using an asynchronous or synchronous function.
- fmap_err(fn): Transform the error value using an asynchronous or synchronous function.
- and_then(fn): Chain an asynchronous operation that returns a new AsyncResult if the current result is a success.
- or_else(fn): Chain an asynchronous operation that returns a new AsyncResult if the current result is an error.

#### fmap
Transform the successful value using an asynchronous or synchronous function. If the AsyncResult is an error, the function won't be called, and the original error will be propagated.
```python
    async def async_multiply(value, factor):
        return value * factor

    async_result = AsyncResult(Ok(5))
    mapped_result = await async_result.fmap(async_multiply, 2)  # Ok(10)
```
#### fmap_err
Transform the error value using an asynchronous or synchronous function. If the AsyncResult is a success, the function won't be called, and the original success value will be propagated.
```python
    async def async_error_message(code):
        return f"Error {code}"

    async_result = AsyncResult(Err(404))
    mapped_error_result = await async_result.fmap_err(async_error_message)  # Err("Error 404")
```
#### and_then
Chain an asynchronous operation that returns a new AsyncResult if the current result is a success. If the AsyncResult is an error, the function won't be called, and the original error will be propagated.
```python
    async def async_double(value):
        return AsyncResult(Ok(value * 2))

    async_result = AsyncResult(Ok(5))
    chained_result = await async_result.and_then(async_double)  # Ok(10)
```

#### or_else
Chain an asynchronous operation that returns a new AsyncResult if the current result is an error. If the AsyncResult is a success, the function won't be called, and the original success value will be propagated.

```python
    async def async_handle_error(error):
        return AsyncResult(Ok(f"Recovered from {error}"))

    async_result = AsyncResult(Err("an error"))
    handled_result = await async_result.or_else(async_handle_error)  # Ok("Recovered from an error")
```

[⬆️  Back to top](#toc)

## AsyncResult decorator
When working with asynchronous functions that might raise exceptions, it's common to see many try-except blocks combined with async-await syntax, which can complicate your code. Flusso comes to the rescue with the @async_result decorator, which simplifies this process by converting asynchronous functions that raise exceptions into functions that return AsyncResult instances instead.

Here's how to use the @async_result_decorator in Flusso:
  ```python
    @async_result
    # Apply the @async_result decorator to your asynchronous functions that might raise exceptions:
    async def async_fetch_data(url: str) -> Result[str, Exception]:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status != 200:
                    raise ValueError("Failed to fetch data")
                return await response.text()

    # When calling the decorated function, it will return an AsyncResult object instead of raising an exception:
    async def main():
        url = "https://example.com/data"
        async_result = await async_fetch_data(url)

        if async_result.is_ok():
            print("Fetched data:", await async_result.unwrap())
        else:
            print("Error fetching data:", await async_result.unwrap_err())
  ```


### **Benefits**

There are several reasons why you might choose to use the flusso.async_result in your code:

1. Cleaner code: By using AsyncResult, you can minimize the need for nested try-except blocks and async-await syntax, leading to more readable and maintainable code.

2. Composable error handling: The AsyncResult class allows you to chain error handling and transformation functions, making it easy to compose complex error handling logic in a declarative manner.

3. Separation of concerns: AsyncResult helps you separate the success and error cases, ensuring that your functions are focused on their primary responsibilities and not cluttered with error handling logic.

4. Type safety: AsyncResult is a generic type that allows you to specify the success and error types, providing better type-checking and making it easier to catch potential issues during development.

5. Flexible error transformation: The AsyncResult class provides methods like fmap, fmap_err, and_then, and or_else, which allow you to transform, chain, and handle errors in a flexible way.

6. Easier testing: Since functions that return AsyncResult objects no longer raise exceptions directly, testing various scenarios and edge cases becomes simpler and more intuitive.

7. Consistent error handling: By using AsyncResult throughout your code, you can establish a consistent approach to error handling, making your codebase more robust and easier to understand.

8. Integration with Result: AsyncResult is designed to work seamlessly with Flusso's Result class, allowing you to handle both synchronous and asynchronous operations with a consistent API.


## Utils

### Flatten
To remove many levels of nesting:

```python
# With Option
print(flatten(Some(Some(Nothing))))  # Nothing
print(flatten(Some("some1")))        # Some("some1")
print(flatten(Nothing))              # Nothing

# With Result
print(flatten(Ok(Ok(Ok(Ok(Ok(Ok(Ok(10)))))))) # Ok(10)
print(flatten(Ok(Ok(Err("error1")))))         # Err("error1")
print(flatten(Ok("ok1")))                     # Ok("ok1")
print(flatten(Err("error1")))                 # Err("error1")
```

### Pattern matching
When using pattern matching with Flusso, you can match on Some, Nothing, Ok, and Err cases and extract the inner values accordingly. This approach allows you to focus on the logic of your application, making your code more maintainable and easier to understand.

  ```python

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

  ```

### Do Notation
Flusso provides a simple way to handle chained computations using the Do notation.
The do notation offers a more intuitive and readable Imperative-style syntax for working with monadic types like Result, Option, and AsyncResult, allowing you to write sequential-like code while retaining the powerful error handling and encapsulation features of monads.
With Flusso's implementation of Do notation, you can easily manage multiple steps in a computation while maintaining clean, readable code.
Here's how to use the Do notation for Option, Result, and AsyncResult types in Flusso.

Option example:
```python
    def add_numbers(a: int, b: int) -> Option[int]:
        return Some(a + b)

    def multiply_numbers(a: int, b: int) -> Option[int]:
        return Some(a * b)

    x = 2
    y = 3

    with (
        Option.do(add_numbers(x, y)) as a,
        Option.do(multiply_numbers(a, x)) as b,
        Option.do(add_numbers(b, y)) as c,
    ):
        result = Some(c)

    assert result == Some(((x + y) * x) + y)
```
Result example:
```python
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

    assert result == Ok(((x + y) * x) + y)
```
Similarly, the Do notation can also be used with Result instances. It provides a clean, functional way to handle chained computations and potential errors.

AsyncResult example:
```python
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
```

By using the Do notation in Flusso, you can write more expressive and maintainable code when working with Option, Result, and AsyncResult instances.

### Coming soon
- [x] Asynchronous support: Integrate seamless handling of asynchronous operations with Result instances, making it even more convenient to work with coroutines.
- [ ] Comprehensive documentation and examples: Expand the library's documentation and provide more practical examples to help users get the most out of Flusso.
- [ ] Enhancing the Do notation to allow more fine-grained error handling or recovery, such as customizing the behavior for specific error cases or providing default values when certain errors occur.
- [ ] Improving the error messages produced by the Do notation to provide more context and clarity when something goes wrong.
- [ ] Custom data types: Provide an easy-to-use interface for creating custom data types that adhere to Flusso's functional programming principles and type safety requirements.

[⬆️  Back to top](#toc)

If you find this package useful, please click the star button ✨!
