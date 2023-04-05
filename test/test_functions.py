from flusso.option import Some, Nothing
from flusso.result import Ok, Err
from flusso.functions import flatten

# Test cases for Option
def test_flatten_option():
    assert flatten(Some(Some(42))) == Some(42)
    assert flatten(Some(Some(Some(42)))) == Some(42)
    assert flatten(Some(42)) == Some(42)
    assert flatten(Some(Some(Nothing))) == Some(Nothing)
    assert flatten(Some(Nothing)) == Some(Nothing)
    assert flatten(Nothing) == Nothing


# Test cases for Result
def test_flatten_result():
    assert flatten(Ok(Ok(42))) == Ok(42)
    assert flatten(Ok(Ok(Ok(42)))) == Ok(42)
    assert flatten(Ok(42)) == Ok(42)
    assert flatten(Ok(Ok(Err("error")))) == Ok(Err("error"))
    assert flatten(Ok(Err("error"))) == Ok(Err("error"))
    assert flatten(Err("error")) == Err("error")
