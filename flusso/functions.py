from typing import TypeVar, Union
from flusso.option import Option, Some
from flusso.result import Result, Ok, Err
from flusso.types import T, E


def flatten(f: Union[Option[T], Result[T, E]]) -> Union[Option[T], Result[T, E]]:
    """
    Recursively flattens nested Option and Result containers into a single container.

    Args:
        f (Union[Option[T], Result[T, E]]): A nested Option or Result container.

    Returns:
        Union[Option[T], Result[T, E]]: A flattened Option or Result container.

    Examples:
        >>> flatten(Some(Some(42)))
        Some(42)
        >>> flatten(Ok(Ok(42)))
        Ok(42)
        >>> flatten(Ok(Err("error")))
        Ok(Err("error"))
    """
    match f:
        case Some(inner) if isinstance(inner, Option):
            return flatten(inner)
        case Ok(inner) if isinstance(inner, Result) and not isinstance(inner, Err):
            return flatten(inner)
        case _:
            return f
