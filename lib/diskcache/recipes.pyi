from .core import ENOVAL as ENOVAL, args_to_key as args_to_key, full_name as full_name
from typing import Any, Optional

class Averager:
    _cache: Any = ...
    _key: Any = ...
    _expire: Any = ...
    _tag: Any = ...
    def __init__(self, cache: Any, key: Any, expire: Optional[Any] = ..., tag: Optional[Any] = ...) -> None: ...
    def add(self, value: Any) -> None: ...
    def get(self): ...
    def pop(self): ...

class Lock:
    _cache: Any = ...
    _key: Any = ...
    _expire: Any = ...
    _tag: Any = ...
    def __init__(self, cache: Any, key: Any, expire: Optional[Any] = ..., tag: Optional[Any] = ...) -> None: ...
    def acquire(self) -> None: ...
    def release(self) -> None: ...
    def locked(self): ...
    def __enter__(self) -> None: ...
    def __exit__(self, *exc_info: Any) -> None: ...

class RLock:
    _cache: Any = ...
    _key: Any = ...
    _expire: Any = ...
    _tag: Any = ...
    def __init__(self, cache: Any, key: Any, expire: Optional[Any] = ..., tag: Optional[Any] = ...) -> None: ...
    def acquire(self) -> None: ...
    def release(self) -> None: ...
    def __enter__(self) -> None: ...
    def __exit__(self, *exc_info: Any) -> None: ...

class BoundedSemaphore:
    _cache: Any = ...
    _key: Any = ...
    _value: Any = ...
    _expire: Any = ...
    _tag: Any = ...
    def __init__(self, cache: Any, key: Any, value: int = ..., expire: Optional[Any] = ..., tag: Optional[Any] = ...) -> None: ...
    def acquire(self) -> None: ...
    def release(self) -> None: ...
    def __enter__(self) -> None: ...
    def __exit__(self, *exc_info: Any) -> None: ...

def throttle(cache: Any, count: Any, seconds: Any, name: Optional[Any] = ..., expire: Optional[Any] = ..., tag: Optional[Any] = ..., time_func: Any = ..., sleep_func: Any = ...): ...
def barrier(cache: Any, lock_factory: Any, name: Optional[Any] = ..., expire: Optional[Any] = ..., tag: Optional[Any] = ...): ...
def memoize_stampede(cache: Any, expire: Any, name: Optional[Any] = ..., typed: bool = ..., tag: Optional[Any] = ..., beta: int = ...): ...
