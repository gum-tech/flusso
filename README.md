Dominate exceptions and missing values in Python.   

## What is flusso?

`flusso` is a library for Python that aims to safely handle exceptions and missing values, similar to how Rust handles them with its `Option` and `Result` types.

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

Convinced? 

Great! Let’s get started.

## Installation
```markdown
> pip install flusso 
```

If you find this package useful, please click the star button *✨*!

<div id="toc"></div>

## Table of contents
- `Option<T>`
    - [Introduction](#introduction)
    - [Basic usage](#basic-usage)
    - [Benefits](#benefits)
    - [API](#api)
    - [API documentation](#api-documentation)
- `Result<T,E>`
    - [Introduction](#introduction-1)
    - [Basic usage](#basic-usage-1)
    - [Benefits](#benefits-1)
    - [API](#api-1)
    - [API documentation](#api-documentation-1)
- Utils
    - [Flatten](#flatten)
    - [Pattern matching](#pattern-matching)
    

## `Option<T>`

### **Introduction**

“Null has led to innumerable errors, vulnerabilities, and system crashes, which have probably caused a billion dollars of pain and damage in the last forty years.” - Tony Hoare, the inventor of null

**`None`** values  can be difficult to detect and handle correctly. When a **`None`** value is encountered, it may not be immediately clear why it is there or how to handle it. This can lead to bugs that are hard to diagnose and fix.

Another problem with **`None`** values is that they can cause runtime errors if they are not properly handled. For example, if a program attempts to access a property of an object that is **`None`**, it will often raise a **`NullPointerException`** or similar error. These errors can be difficult to anticipate and debug, especially if they occur deep in the codebase or if there are many layers of abstraction involved.

To avoid these problems, we use Option monad as an alternative way of representing the absence of a value or the lack of an object reference. 

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
  
  Let's rewrite this with a declarative style using flusso option monad 
  
  ```python
    from flusso import Option, Some, Nothing

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
        return get_user(id).map(lambda user: user.username)


    match get_username(1):
        # Matches any `Some` instance and binds its value to the `username` variable
        case Some(username):
            print('User found: {0}'.format(username))

        # Matches `Nothing` instance
        case Nothing
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
   from flusso import Option, Some, Nothing
  
    def get_full_name(first_name: str, middle_name: 'Option[str]', last_name: str) -> str:
        match(middle_name):
            case Some(mname):
                print(f"{first_name} {mname} {last_name}")

            # Matches `Nothing` instance
            case Nothing
                print(f"{first_name} {last_name}")
    
    getFullName({firstName: "Galileo", middleName: None, lastName: "Galilei"}); // Galileo Galilei	
    getFullName({firstName: "Leonardo", middleName: Some("Da"), lastName: "Vinci"}); // Leonardo Da Vinci
  ```
   Let’s look at another example by chaining calculations 
  
  ```python
   from flusso import Option, Some, Nothing

    def sine(x: float) -> 'Option[float]':
        return math.sin(x)

    def cube(x: float) -> 'Option[float]':
        return x * x * x

    def inc(x: float) -> 'Option[float]':
        return x + 1

    def double(x: float) -> 'Option[float]':
        return x * x

    def divide(x: float, y: float) -> 'Option[float]':
        if y > 0:
            return x / y
        else:
            return Nothing
    
    def sineCubedIncDoubleDivideBy10(x: float):
        return Some(x)
                    .map(sine)
                    .map(cube)
                    .map(inc)
                    .map(double)
                    .map(lambda x: divide(x, 10)))

    match(sineCubedIncDoubleDivideBy10(30)):
            case Some(result):
                print(f"`Result is {result}")

            # Matches `Nothing` instance
            case Nothing
                print(f"Please check your inputs")
  ```