from typing import TypeVar, Callable, Union, Tuple
# from flusso.utils import UnwrapFailedError

T = TypeVar('T')

Option = Union[Callable[[T], 'Some'], Callable[[], 'Nothing']]

class Option:
    def __init__(self, /, **kwargs):
        self.__dict__.update(kwargs)

    def __repr__(self):
        items = (f"{k}={v!r}" for k, v in self.__dict__.items())
        return f'{type(self).__name__}({", ".join(items)})'

    def __eq__(self: 'Option[T]', other: 'Option[T]') -> bool:
        if isinstance(self, Option) and isinstance(other, Option):
            return self.unwrap_or('Nothing') == other.unwrap_or('Nothing')
        return False
    
    # @classmethod
    # def do(cls, expr: Generator[T, None, None]) -> 'Option[T]':
    #     try:
    #         return cls.from_value(next(expr))
    #     except UnwrapFailedError as exc:
    #         return exc.halted_container
    

def _some(value: T) -> 'Option[T]':
    def map_(fn: Callable[[T], T]) -> 'Option[T]':
        return _some(fn(value))

    def and_then(fn: Callable[[T], 'Option[T]']) -> 'Option[T]':
        return fn(value)

    def filter_(fn: Callable[[T], bool]) -> 'Option[T]':
        return _some(value) if fn(value) else _none()

    def unwrap() -> T:
        return value

    def expect(_: str) -> T:
        return value

    def unwrap_or(_: T) -> T:
        return value

    def unwrap_or_else(_: Callable[[], T]) -> T:
        return value

    def or_(_: 'Option[T]') -> 'Option[T]':
        return _some(value)

    def or_else(_: Callable[[], 'Option[T]']) -> 'Option[T]':
        return _some(value)

    def and_(_: 'Option[T]') -> 'Option[T]':
        return _

    def ok_or(_: T) -> Tuple[bool, Union[T, T]]:
        return (True, value)
    
    def is_some() -> bool:
        return True
    
    def is_none() -> bool: 
        return False

    return Option(**{
        'map': map_,
        'and_then': and_then,
        'filter': filter_,
        'unwrap': unwrap,
        'expect': expect,
        'unwrap_or': unwrap_or,
        'unwrap_or_else': unwrap_or_else,
        'or_': or_,
        'or_else': or_else,
        'and_': and_,
        'ok_or': ok_or,
        'is_some': is_some, 
        'is_none': is_none,
        'value': value
    })

def _none() -> 'Option[T]':  # sourcery skip: raise-specific-error
    def map(_: Callable[[T], T]) -> 'Option[T]':
        return _none()

    def and_then(_: Callable[[T], 'Option[T]']) -> 'Option[T]':
        return _none()
    def filter(_: Callable[[T], bool]) -> 'Option[T]':
      return _none()

    def unwrap() -> T:
        raise ReferenceError('`Option.unwrap()` on a `None` value')

    def expect(a: str) -> T:
        raise Exception(f"{a}")

    def unwrap_or(a: T) -> T:
        return a

    def unwrap_or_else(fn: Callable[[], T]) -> T:
        return fn()

    def or_(a: 'Option[T]') -> 'Option[T]':
        return a

    def or_else(fn: Callable[[], 'Option[T]']) -> 'Option[T]':
        return fn()

    def and_(a: 'Option[T]') -> 'Option[T]':
        return a

    def ok_or(e: T) -> Tuple[bool, Union[T, T]]:
        return (False, e)

    def is_some() -> bool:
        return False
    
    def is_none() -> bool: 
        return True

    return Option(**{
         'map': map,
        'and_then': and_then,
        'filter': filter,
        'unwrap': unwrap,
        'expect': expect,
        'unwrap_or': unwrap_or,
        'unwrap_or_else': unwrap_or_else,
        'or_': or_,
        'or_else': or_else,
        'and_': and_,
        'ok_or': ok_or,
        'is_some': is_some, 
        'is_none': is_none
    })



# Alias for none() to avoid consfusion with None
Nothing: 'Option[T]' = _none()
def Some(value: T) -> 'Option[T]': 
    return _none() if value is None else _some(value)



# Option decorator 
def option(fn: Callable) -> Callable:
    def wrapper(*args, **kwargs):
        return Nothing if fn(*args, **kwargs) is None else Some(fn(*args, **kwargs))
    return wrapper

# print(_some(2))
# print(_some(2) == _some(2))
# result = Option.do((x * 2 + y -1 for x in Option(_some(3)) for y in Option(_some(2))))
# print(result.unwrap()) # 5