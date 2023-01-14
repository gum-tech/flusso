from flusso.option import Option, Some, Nothing

def _optCube(x: int) -> Option[int]:
    return Some(x**2 * x)

def _optDouble(x: int) -> Option[int]:
    return Some(x ** 2)

def _optDivide(x: int, y: int) -> Option[int]:
    return Some(x / y) if y > 0 else Nothing


def test_option_chain():
    assert Some(2).and_then(_optCube).and_then(_optDouble).unwrap() == 64

