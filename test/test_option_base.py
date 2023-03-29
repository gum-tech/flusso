from flusso.option import Nothing, Some, Option

def test_option_creation():
    # Test creating Some and Nothing instances
    assert Some(5).value == 5

def test_option_map():
    # Test mapping a function over a Some instance
    assert Some(5).bind(lambda x: x + 1).value == 6

    # Test mapping a function over a Nothing instance
    assert Nothing.bind(lambda x: x + 1) == Nothing

def test_option_and_then():
    # Test chaining two Some instances
    assert (Some(5)
            .and_then(lambda x: Some(x * 2))
            .value) == 10

    # Test chaining a Some and Nothing instance
    assert (Some(5)
            .and_then(lambda x: Nothing)) == Nothing

    # Test chaining a Nothing and Some instance
    assert (Nothing
            .and_then(lambda x: Some(x * 2))) == Nothing

def test_option_filter():
    # Test filtering a Some instance
    assert (Some(5)
            .filter_(lambda x: x > 3)
            .value) == 5

    # Test filtering a Some instance that doesn't pass the filter
    assert Nothing.filter_(lambda x: x > 3) == Nothing

    # Test filtering a Nothing instance
    assert Nothing.filter_(lambda x: x > 3) == Nothing



def _optCube(x: int) -> Option[int]:
    return Some(x**2 * x)

def _optDouble(x: int) -> int:
    return x ** 2

def _optDivide(x: int, y: int) -> Option[int]:
    return Some(x / y) if y > 0 else Nothing


def test_option_chain():
    assert Some(2).and_then(_optCube).bind(_optDouble).unwrap() == 64


def test_some_case():
    # Test some case
    option_value = Some(5)
    assert option_value.unwrap() == 5
    assert option_value.is_some() == True
    assert option_value.is_none() == False
    assert option_value.bind(lambda x: x*2).unwrap() == 10
    assert option_value.filter_(lambda x: x > 4).unwrap() == 5
    assert option_value.and_then(lambda x: Some(x*3)).unwrap() == 15
    assert option_value.or_(Nothing).unwrap() == 5
    assert option_value.or_else(lambda: Nothing).unwrap() == 5
    assert option_value.and_(Nothing).is_none() == True
    assert option_value.ok_or("Error") == (True, 5)
    assert option_value.unwrap_or(10) == 5
    assert option_value.unwrap_or_else(lambda: 10) == 5

def test_nothing_case():
    # Test none case
    option_value = Nothing
    try:
        option_value.unwrap()
        assert False, "Should raise ReferenceError"
    except ValueError:
        assert True
    assert option_value.is_some() == False
    assert option_value.is_none() == True
    assert option_value.bind(lambda x: x*2).is_none() == True
    assert option_value.filter_(lambda x: x > 4).is_none() == True
    assert option_value.and_then(lambda x: Some(x*3)).is_none() == True
    assert option_value.or_(Some(5)).unwrap() == 5
    assert option_value.or_else(lambda: Some(5)).unwrap() == 5
    assert option_value.and_(Some(5)) == Nothing
    assert option_value.ok_or("Error") == (False, "Error")
    assert option_value.unwrap_or(10) == 10
    assert option_value.unwrap_or_else(10) == 10
