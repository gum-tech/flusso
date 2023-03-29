from typing import Dict, Optional

from flusso.option import Nothing, Some, option


@option
def _func(dict: Dict[str, str], key: str) -> Optional[str]:
    return dict.get(key, None)


def test_option_some():
    """Ensures that option decorator works correctly for Some case."""
    assert _func({'a': 'b'}, 'a') == Some('b')


def test_option_nothing():
    """Ensures that option decorator works correctly for Nothing case."""
    assert _func({'a': 'b'}, 'c') == Nothing
