from flusso.option import Nothing, Some, option, Option
from flusso.primitives.exceptions import UnwrapFailedError

def double(x: int) -> Option[int]:
    return Some(x * 2)

def add_one(x: int) -> Option[int]:
    return Some(x + 1)

def test_some():
    s = Some(42)
    assert s.is_some()
    assert not s.is_none()
    assert s.unwrap() == 42
    assert s.unwrap_or(0) == 42
    assert s.unwrap_or_else(lambda: 0) == 42
    assert s.fmap(lambda x: x * 2) == Some(84)
    assert s.and_then(lambda x: Some(x * 2)) == Some(84)
    assert s.filter_by_predicate(lambda x: x > 50) == Nothing
    assert s.value_or(Some(100)) == Some(42)
    assert s.or_else(lambda: Some(100)) == Some(42)
    assert s.value_and(Some(100)) == Some(100)
    assert Some(None) == Nothing
    assert Some(Nothing) == Nothing


def test_nothing():
    n = Nothing
    assert not n.is_some()
    assert n.is_none()
    assert n.unwrap_or(0) == 0
    assert n.unwrap_or_else(lambda: 0) == 0
    assert n.fmap(lambda x: x * 2) == Nothing
    assert n.and_then(lambda x: Some(x * 2)) == Nothing
    assert n.filter_by_predicate(lambda x: x > 50) == Nothing
    assert n.value_or(Some(100)) == Some(100)
    assert n.or_else(lambda: Some(100)) == Some(100)
    assert n.value_and(Some(100)) == Nothing

def test_nothing_unwrap():
    n = Nothing
    try:
        n.unwrap()
        assert False, "Expected UnwrapFailedError when calling unwrap on Nothing"
    except UnwrapFailedError:
        pass  # Expected exception

def test_nothing_expect():
    n = Nothing
    expected_message = "Expected exception message"

    try:
        n.expect(expected_message)
        assert False, "Expected a ValueError with a message when calling expect on Nothing"
    except ValueError as e:
        assert str(e) == expected_message, f"Expected exception message '{expected_message}', got '{str(e)}'"

def test_option_decorator():
    @option
    def maybe_square(x):
        return x ** 2 if x % 2 == 0 else None

    assert maybe_square(2) == Some(4)
    assert maybe_square(3) == Nothing

def test_option_eq():
    assert Some(42) == Some(42)
    assert Some(42) != Some(43)
    assert Nothing == Nothing
    assert Some(42) != Nothing

def test_ok_or():
    s = Some(12)
    error = "An error occurred"

    result = s.ok_or(error)
    assert result.is_ok()
    assert not result.is_err()
    assert result.unwrap() == 12
    assert result.unwrap_or(0) == 12
    assert result.unwrap_or_else(lambda: 0) == 12

    n = Nothing
    res_err = n.ok_or(error)
    assert not res_err.is_ok()
    assert res_err.is_err()
    assert res_err.unwrap_or(0) == 0
    print(result)
    assert res_err.unwrap_or_else(lambda x: 0) == 0

def test_option_do_notation() -> None:
    x = 3

    with (
        Option.do(double(x)) as a,
        Option.do(add_one(a)) as b,
        Option.do(double(b)) as c,
    ):
        result = Some(c)

    assert result == Some((x * 2 + 1) * 2)


def test_option_pattern_matching():
    opt = Some(42)
    opt_nothing = Some(None)

    match opt:
        case Some(x):
            assert x == 42
        case Nothing:
            assert False, "Unexpected match with Nothing"

    match opt_nothing:
        case Some(_):
            assert False, "Unexpected match with Some"
        case Nothing:
            pass
