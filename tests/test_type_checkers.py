"""Tests for type checking utilities."""

from enum import StrEnum
from typing import Optional, Union

from pydantic import BaseModel

from pydantic_visualizer.type_checkers import (
    first_arg,
    is_basemodel_type,
    is_enum_type,
    is_optional_type,
    is_type,
    safe_is_subclass,
    unwrap_optional,
)


class TestModel(BaseModel):
    """Test Pydantic model."""

    field: str


class TestEnum(StrEnum):
    """Test enum."""

    VALUE1 = "value1"
    VALUE2 = "value2"


class TestIsType:
    """Tests for is_type function."""

    def test_with_class(self):
        """Test is_type with a class."""
        assert is_type(str) is True
        assert is_type(int) is True
        assert is_type(TestModel) is True

    def test_with_instance(self):
        """Test is_type with an instance."""
        assert is_type("string") is False
        assert is_type(123) is False
        assert is_type(TestModel(field="test")) is False

    def test_with_none(self):
        """Test is_type with None."""
        assert is_type(None) is False


class TestIsBaseModelType:
    """Tests for is_basemodel_type function."""

    def test_with_basemodel_class(self):
        """Test with a BaseModel subclass."""
        assert is_basemodel_type(TestModel) is True

    def test_with_basemodel_instance(self):
        """Test with a BaseModel instance."""
        assert is_basemodel_type(TestModel(field="test")) is False

    def test_with_regular_class(self):
        """Test with a regular class."""
        assert is_basemodel_type(str) is False
        assert is_basemodel_type(int) is False

    def test_with_none(self):
        """Test with None."""
        assert is_basemodel_type(None) is False


class TestIsEnumType:
    """Tests for is_enum_type function."""

    def test_with_enum_class(self):
        """Test with an Enum class."""
        assert is_enum_type(TestEnum) is True

    def test_with_enum_member(self):
        """Test with an Enum member."""
        assert is_enum_type(TestEnum.VALUE1) is False

    def test_with_regular_class(self):
        """Test with a regular class."""
        assert is_enum_type(str) is False
        assert is_enum_type(TestModel) is False

    def test_with_none(self):
        """Test with None."""
        assert is_enum_type(None) is False


class TestSafeIsSubclass:
    """Tests for safe_is_subclass function."""

    def test_with_valid_subclass(self):
        """Test with a valid subclass."""
        assert safe_is_subclass(TestModel, BaseModel) is True

    def test_with_non_subclass(self):
        """Test with a non-subclass."""
        assert safe_is_subclass(str, BaseModel) is False

    def test_with_non_type(self):
        """Test with a non-type argument."""
        assert safe_is_subclass("string", BaseModel) is False
        assert safe_is_subclass(123, BaseModel) is False

    def test_with_none(self):
        """Test with None."""
        assert safe_is_subclass(None, BaseModel) is False


class TestFirstArg:
    """Tests for first_arg function."""

    def test_with_list_type(self):
        """Test with List type."""
        result = first_arg(list[str])
        assert result is str

    def test_with_optional_type(self):
        """Test with Optional type."""
        result = first_arg(Optional[str])
        assert result is str

    def test_with_no_args(self):
        """Test with type that has no args."""
        result = first_arg(str)
        assert result is None

    def test_with_union_type(self):
        """Test with Union type."""
        result = first_arg(Union[str, int])
        assert result is str


class TestIsOptionalType:
    """Tests for is_optional_type function."""

    def test_with_optional_type(self):
        """Test with Optional type."""
        assert is_optional_type(Optional[str]) is True
        assert is_optional_type(Optional[int]) is True

    def test_with_union_with_none(self):
        """Test with Union that includes None."""
        assert is_optional_type(Union[str, None]) is True

    def test_with_regular_type(self):
        """Test with regular type."""
        assert is_optional_type(str) is False
        assert is_optional_type(int) is False

    def test_with_union_without_none(self):
        """Test with Union that doesn't include None."""
        assert is_optional_type(Union[str, int]) is False


class TestUnwrapOptional:
    """Tests for unwrap_optional function."""

    def test_with_optional_type(self):
        """Test unwrapping Optional type."""
        inner_type, is_optional = unwrap_optional(Optional[str])
        assert inner_type is str
        assert is_optional is True

    def test_with_union_with_none(self):
        """Test unwrapping Union with None."""
        inner_type, is_optional = unwrap_optional(Union[str, None])
        assert inner_type is str
        assert is_optional is True

    def test_with_regular_type(self):
        """Test with regular type (not optional)."""
        inner_type, is_optional = unwrap_optional(str)
        assert inner_type is str
        assert is_optional is False

    def test_with_union_without_none(self):
        """Test with Union that doesn't include None."""
        union_type = Union[str, int]
        inner_type, is_optional = unwrap_optional(union_type)
        assert inner_type == union_type
        assert is_optional is False

    def test_with_complex_optional(self):
        """Test with complex Optional type."""
        inner_type, is_optional = unwrap_optional(Optional[list[str]])
        assert inner_type == list[str]
        assert is_optional is True

    def test_with_nested_model_optional(self):
        """Test with Optional nested model."""
        inner_type, is_optional = unwrap_optional(Optional[TestModel])
        assert inner_type == TestModel
        assert is_optional is True
