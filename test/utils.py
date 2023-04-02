def double(x: int) -> Option[int]:
    return Option.Some(x * 2)

def add_one(x: int) -> Option[int]:
    return Option.Some(x + 1)

def fail_on_even(x: int) -> Result[int, str]:
    if x % 2 == 0:
        return Result.Err("Even number")
    return Result.Ok(x)

def triple(x: int) -> Result[int, str]:
    return Result.Ok(x * 3)
