from enum import Enum
from typing import (
    Any,
    TypeGuard,
    Union,
    get_args,
    get_origin,
)

from pydantic import BaseModel


def is_type(x: Any) -> TypeGuard[type]:
    return isinstance(x, type)


def is_basemodel_type(x: Any) -> TypeGuard[type[BaseModel]]:
    return isinstance(x, type) and issubclass(x, BaseModel)


def is_enum_type(tp: Any) -> bool:
    """Check if a type is an Enum or subclass of Enum."""
    try:
        return isinstance(tp, type) and issubclass(tp, Enum)
    except TypeError:
        return False


def safe_is_subclass(tp: Any, parent: Any) -> bool:
    """issubclass with guard against non-type inputs."""
    return isinstance(tp, type) and issubclass(tp, parent)


def first_arg(tp: Any) -> Any | None:
    """Return the first type argument if present, else None."""
    args = get_args(tp)
    return args[0] if args else None


def is_optional_type(annotation: Any) -> bool:
    origin = get_origin(annotation)
    args = get_args(annotation)
    return origin is Union and any(a is type(None) for a in args)


def unwrap_optional(tp: Any) -> tuple[Any, bool]:
    """
    If the type is Optional[T] or T | None, return (T, True).
    Otherwise return (tp, False).
    """
    origin = get_origin(tp)
    if origin is Union:
        args = tuple(a for a in get_args(tp) if a is not type(None))
        if len(args) == 1:
            return args[0], True
    # For Python 3.10+ UnionType (T | None), get_origin returns types.UnionType
    # but get_args still works, and the above covers it.
    return tp, False
