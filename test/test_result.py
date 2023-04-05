from flusso.result import Ok, Err, result, Result
from flusso.primitives.exceptions import UnwrapFailedError

def fail_on_even(x: int) -> Result[int, str]:
    if x % 2 == 0:
        return Err("Even number")
    return Ok(x)

def triple(x: int) -> Result[int, str]:
    return Ok(x * 3)

def add_one_result(x: int) -> Result[int, str]:
    return Ok(x + 1)


def test_ok():
    res = Ok(42)
    assert res.is_ok() == True
    assert res.is_err() == False
    assert res.ok().unwrap() == 42
    assert res.err().is_none()

def test_err():
    res = Err("Error")
    assert res.is_ok() == False
    assert res.is_err() == True
    assert res.ok().is_none()
    assert res.err().unwrap() == "Error"

def test_ok_unwrap_err():
    ok_value = Ok(42)

    try:
        ok_value.unwrap_err()
        assert False, "Expected UnwrapFailedError when calling unwrap_err on Ok value"
    except UnwrapFailedError:
        pass  # Expected exception

def test_err_unwrap():
    e = Err("error message")

    try:
        e.unwrap()
        assert False, "Expected UnwrapFailedError when calling unwrap on Err value"
    except UnwrapFailedError as ex:
        assert ex.halted_container == e, "Expected halted_container to be the same Err instance"

def test_unwrap_or():
    res_ok = Ok(42)
    res_err = Err("Error")
    assert res_ok.unwrap_or(0) == 42
    assert res_err.unwrap_or(0) == 0

def test_unwrap_or_else():
    res_ok = Ok(42)
    res_err = Err("Error")
    assert res_ok.unwrap_or_else(lambda x: 0) == 42
    assert res_err.unwrap_or_else(lambda x: 0) == 0

def test_err_expect():
    e = Err("error message")

    try:
        e.expect("Custom error message")
        assert False, "Expected ValueError when calling expect on Err value"
    except ValueError as ex:
        assert str(ex) == "Custom error message", "Expected custom error message to be raised"

def test_fmap():
    res_ok = Ok(42)
    res_err = Err("Error")
    assert res_ok.fmap(lambda x: x * 2) == Ok(84)
    assert res_err.fmap(lambda x: x * 2) == res_err

def test_fmap_err():
    res_ok = Ok(42)
    res_err = Err("Error")
    assert res_ok.fmap_err(lambda x: "New error") == res_ok
    assert res_err.fmap_err(lambda x: "New error") == Err("New error")

def test_and_then():
    res_ok = Ok(42)
    res_err = Err("Error")
    assert res_ok.and_then(lambda x: Ok(x * 2)) == Ok(84)
    assert res_err.and_then(lambda x: Ok(x * 2)) == res_err

def test_value_or():
    res_ok = Ok(42)
    res_err = Err("Error")
    assert res_ok.value_or(Err("New error")) == res_ok
    assert res_err.value_or(Ok(42)) == Ok(42)

def test_or_else():
    res_ok = Ok(42)
    res_err = Err("Error")
    assert res_ok.or_else(lambda x: Ok(0)) == res_ok
    assert res_err.or_else(lambda x: Ok(0)) == Ok(0)

def test_value_and():
    res_ok = Ok(42)
    res_err = Err("Error")
    assert res_ok.value_and(Ok(84)) == Ok(84)
    assert res_err.value_and(Ok(84)) == res_err

def test_result_decorator():

    @result
    def foo(val):
        if val == 0:
            return None
        return val

    res1 = foo(1)
    res2 = foo(0)

    if not res1.is_ok() or res1.unwrap() != 1:
        assert False, "Expected Ok(1) for foo(1)"

    if not res2.is_err() or res2.unwrap_err() is not None:
        assert False, "Expected Err(None) for foo(0)"

def test_eq():
    res_ok1 = Ok(42)
    res_ok2 = Ok(42)
    res_ok3 = Ok(84)
    res_err1 = Err("Error")
    res_err2 = Err("Error")
    res_err3 = Err("Different error")

    assert res_ok1 == res_ok2
    assert res_ok1 != res_ok3
    assert res_err1 == res_err2
    assert res_err1 != res_err3
    assert res_ok1 != res_err1

def test_result_do_notation():
    x = 3
    result = Err("Not executed")

    with (
        Result.do(fail_on_even(x)) as a,
        Result.do(triple(a)) as b,
        Result.do(add_one_result(b)) as c,
    ):
        print(f"a: {a}, b: {b}, c: {c}")
        result = Ok(c)

    assert result == Ok((x * 3 + 1))

def test_result_pattern_matching():
    res = Ok(42)

    match res:
        case Ok(x):
            assert x == 42
        case Err(_):
            assert False, "Unexpected match with Err"

    res = Err("error")

    match res:
        case Ok(_):
            assert False, "Unexpected match with Ok"
        case Err(e):
            assert e == "error"
