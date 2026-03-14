"""Tests for PydanticVisualizer class."""

import tempfile
from enum import Enum, StrEnum
from pathlib import Path
from typing import List, Optional

import pandas as pd
import pytest
from pydantic import BaseModel, Field

from pydantic_visualizer import PydanticVisualizer


# Test Models
class Priority(StrEnum):
    """Priority levels."""

    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class Status(Enum):
    """Task status."""

    TODO = "todo"
    IN_PROGRESS = "in_progress"
    DONE = "done"


class Address(BaseModel):
    """Address model."""

    street: str = Field(description="Street name")
    city: str = Field(description="City name")
    zipcode: str = Field(default="00000", description="Zip code")


class User(BaseModel):
    """User model with documentation."""

    name: str = Field(description="User's full name", examples=["John Doe"])
    age: int = Field(description="User's age", examples=[25, 30])
    email: Optional[str] = Field(default=None, description="Email address")
    address: Optional[Address] = None


class Task(BaseModel):
    """Task model."""

    title: str
    description: str
    priority: Priority
    status: Status = Status.TODO
    assignee: Optional[User] = None
    tags: List[str] = Field(default_factory=list)


class Project(BaseModel):
    """Project with tasks."""

    name: str
    tasks: List[Task]
    owner: User


class SimpleModel(BaseModel):
    """Simple model for basic tests."""

    field1: str
    field2: int


class TestPydanticVisualizerInit:
    """Tests for PydanticVisualizer initialization."""

    def test_default_initialization(self):
        """Test default initialization."""
        visualizer = PydanticVisualizer()
        assert visualizer.object_color == "#DDEDFF"
        assert visualizer.list_color == "#FFEFDD"
        assert visualizer.enum_color == "#DDFFEA"
        assert visualizer.html_color == "#006699"
        assert visualizer.title == "Diagram"
        assert visualizer.model_cls is None
        assert visualizer.enum_dict == {}
        assert visualizer.seen_classes == set()
        assert visualizer.all_classes == []
        assert visualizer.lines == ["classDiagram"]
        assert visualizer.relationships == []

    def test_custom_colors(self):
        """Test initialization with custom colors."""
        visualizer = PydanticVisualizer(
            object_color="#FF0000",
            list_color="#00FF00",
            enum_color="#0000FF",
            html_color="#FFFF00",
        )
        assert visualizer.object_color == "#FF0000"
        assert visualizer.list_color == "#00FF00"
        assert visualizer.enum_color == "#0000FF"
        assert visualizer.html_color == "#FFFF00"


class TestSetDatamodel:
    """Tests for set_datamodel method."""

    def test_set_simple_model(self):
        """Test setting a simple model."""
        visualizer = PydanticVisualizer()
        visualizer.set_datamodel(SimpleModel)
        
        assert visualizer.model_cls == SimpleModel
        assert visualizer.title == "SimpleModel"
        assert "SimpleModel" in visualizer.seen_classes
        assert SimpleModel in visualizer.all_classes
        assert len(visualizer.lines) > 1  # More than just "classDiagram"

    def test_set_model_with_enum(self):
        """Test setting a model with enum."""
        visualizer = PydanticVisualizer()
        visualizer.set_datamodel(Task)
        
        assert "Priority" in visualizer.enum_dict
        assert "Status" in visualizer.enum_dict
        assert isinstance(visualizer.enum_dict["Priority"], pd.DataFrame)
        assert isinstance(visualizer.enum_dict["Status"], pd.DataFrame)

    def test_reset_on_new_model(self):
        """Test that state is reset when setting a new model."""
        visualizer = PydanticVisualizer()
        visualizer.set_datamodel(SimpleModel)
        
        initial_classes = len(visualizer.all_classes)
        
        visualizer.set_datamodel(User)
        
        assert visualizer.model_cls == User
        assert visualizer.title == "User"
        assert "SimpleModel" not in visualizer.seen_classes
        assert SimpleModel not in visualizer.all_classes

    def test_nested_models(self):
        """Test setting a model with nested models."""
        visualizer = PydanticVisualizer()
        visualizer.set_datamodel(Project)
        
        assert "Project" in visualizer.seen_classes
        assert "Task" in visualizer.seen_classes
        assert "User" in visualizer.seen_classes
        assert "Address" in visualizer.seen_classes
        assert len(visualizer.relationships) > 0


class TestMermaidProperty:
    """Tests for mermaid property."""

    def test_mermaid_output(self):
        """Test mermaid property returns valid string."""
        visualizer = PydanticVisualizer()
        visualizer.set_datamodel(SimpleModel)
        
        mermaid = visualizer.mermaid
        assert isinstance(mermaid, str)
        assert "classDiagram" in mermaid
        assert "SimpleModel" in mermaid

    def test_mermaid_with_relationships(self):
        """Test mermaid includes relationships."""
        visualizer = PydanticVisualizer()
        visualizer.set_datamodel(User)
        
        mermaid = visualizer.mermaid
        assert "User" in mermaid
        assert "Address" in mermaid
        # Check for relationship syntax
        assert "-->" in mermaid or "..*" in mermaid or "..>" in mermaid


class TestMarkdownMethod:
    """Tests for markdown method."""

    def test_markdown_all_sections(self):
        """Test markdown with all sections included."""
        visualizer = PydanticVisualizer()
        visualizer.set_datamodel(Task)
        
        markdown = visualizer.markdown()
        assert "# Task Diagram" in markdown
        assert "```mermaid" in markdown
        assert "# Enums Values" in markdown
        assert "# Task - Model Descriptions" in markdown

    def test_markdown_diagram_only(self):
        """Test markdown with only diagram."""
        visualizer = PydanticVisualizer()
        visualizer.set_datamodel(Task)
        
        markdown = visualizer.markdown(
            include_diagram=True,
            include_enums=False,
            include_description=False,
        )
        assert "# Task Diagram" in markdown
        assert "```mermaid" in markdown
        assert "# Enums Values" not in markdown
        assert "# Task - Model Descriptions" not in markdown

    def test_markdown_no_diagram(self):
        """Test markdown without diagram."""
        visualizer = PydanticVisualizer()
        visualizer.set_datamodel(Task)
        
        markdown = visualizer.markdown(include_diagram=False)
        assert "# Task Diagram" not in markdown
        assert "```mermaid" not in markdown


class TestHtmlMethod:
    """Tests for html method."""

    def test_html_structure(self):
        """Test HTML has proper structure."""
        visualizer = PydanticVisualizer()
        visualizer.set_datamodel(SimpleModel)
        
        html = visualizer.html()
        assert "<!DOCTYPE html>" in html
        assert "<html>" in html
        assert "</html>" in html
        assert "<head>" in html
        assert "<body>" in html
        assert "mermaid" in html

    def test_html_all_sections(self):
        """Test HTML with all sections."""
        visualizer = PydanticVisualizer()
        visualizer.set_datamodel(Task)
        
        html = visualizer.html()
        assert "<h1>Task Diagram</h1>" in html
        assert '<div class="mermaid">' in html
        assert "<h1>Enums Values</h1>" in html
        assert "<h1>Task - Model Descriptions</h1>" in html

    def test_html_custom_color(self):
        """Test HTML uses custom colors."""
        visualizer = PydanticVisualizer(html_color="#FF0000")
        visualizer.set_datamodel(SimpleModel)
        
        html = visualizer.html()
        assert "#FF0000" in html


class TestDescriptionProperty:
    """Tests for description property."""

    def test_description_output(self):
        """Test description property."""
        visualizer = PydanticVisualizer()
        visualizer.set_datamodel(User)
        
        description = visualizer.description
        assert isinstance(description, str)
        assert "User" in description
        assert "Address" in description

    def test_description_includes_field_info(self):
        """Test description includes field information."""
        visualizer = PydanticVisualizer()
        visualizer.set_datamodel(User)
        
        description = visualizer.description
        assert "name" in description
        assert "age" in description
        assert "email" in description


class TestEnumProperties:
    """Tests for enum-related properties."""

    def test_enum_tables(self):
        """Test enum_tables property."""
        visualizer = PydanticVisualizer()
        visualizer.set_datamodel(Task)
        
        enum_tables = visualizer.enum_tables
        assert isinstance(enum_tables, dict)
        assert "Priority" in enum_tables
        assert "Status" in enum_tables
        assert isinstance(enum_tables["Priority"], pd.DataFrame)

    def test_enum_markdown_tables(self):
        """Test enum_markdown_tables property."""
        visualizer = PydanticVisualizer()
        visualizer.set_datamodel(Task)
        
        markdown = visualizer.enum_markdown_tables
        assert "# Enums Values" in markdown
        assert "Priority" in markdown
        assert "Status" in markdown

    def test_enum_html_tables(self):
        """Test enum_html_tables property."""
        visualizer = PydanticVisualizer()
        visualizer.set_datamodel(Task)
        
        html = visualizer.enum_html_tables
        assert "<h1>Enums Values</h1>" in html
        assert "<h4>Priority</h4>" in html
        assert "<h4>Status</h4>" in html
        assert "<table" in html

    def test_no_enums(self):
        """Test enum properties with no enums."""
        visualizer = PydanticVisualizer()
        visualizer.set_datamodel(SimpleModel)
        
        assert visualizer.enum_tables == {}
        assert visualizer.enum_markdown_tables == ""
        assert visualizer.enum_html_tables == ""


class TestDescriptionTables:
    """Tests for description_tables property."""

    def test_description_tables_structure(self):
        """Test description_tables returns proper structure."""
        visualizer = PydanticVisualizer()
        visualizer.set_datamodel(User)
        
        tables = visualizer.description_tables
        assert isinstance(tables, dict)
        assert "User" in tables
        assert "Address" in tables
        assert isinstance(tables["User"], pd.DataFrame)

    def test_description_tables_columns(self):
        """Test description tables have expected columns."""
        visualizer = PydanticVisualizer()
        visualizer.set_datamodel(User)
        
        user_df = visualizer.description_tables["User"]
        assert "Field" in user_df.columns
        assert "Type" in user_df.columns

    def test_description_markdown_tables(self):
        """Test description_markdown_tables property."""
        visualizer = PydanticVisualizer()
        visualizer.set_datamodel(User)
        
        markdown = visualizer.description_markdown_tables
        assert "## User" in markdown
        assert "## Address" in markdown

    def test_description_html_tables(self):
        """Test description_html_tables property."""
        visualizer = PydanticVisualizer()
        visualizer.set_datamodel(User)
        
        html = visualizer.description_html_tables
        assert "<h2>User</h2>" in html
        assert "<h2>Address</h2>" in html
        assert "<table" in html


class TestSaveMarkdown:
    """Tests for save_markdown method."""

    def test_save_markdown_default_location(self):
        """Test saving markdown to default location."""
        visualizer = PydanticVisualizer()
        visualizer.set_datamodel(SimpleModel)
        
        with tempfile.TemporaryDirectory() as tmpdir:
            visualizer.save_markdown(output_folder=tmpdir)
            
            expected_file = Path(tmpdir) / "simplemodel_mermaid.md"
            assert expected_file.exists()
            
            content = expected_file.read_text()
            assert "SimpleModel" in content
            assert "```mermaid" in content

    def test_save_markdown_custom_location(self):
        """Test saving markdown to custom location."""
        visualizer = PydanticVisualizer()
        visualizer.set_datamodel(User)
        
        with tempfile.TemporaryDirectory() as tmpdir:
            custom_path = Path(tmpdir) / "custom" / "folder"
            visualizer.save_markdown(output_folder=custom_path)
            
            expected_file = custom_path / "user_mermaid.md"
            assert expected_file.exists()

    def test_save_markdown_selective_content(self):
        """Test saving markdown with selective content."""
        visualizer = PydanticVisualizer()
        visualizer.set_datamodel(Task)
        
        with tempfile.TemporaryDirectory() as tmpdir:
            visualizer.save_markdown(
                output_folder=tmpdir,
                include_diagram=True,
                include_enums=False,
                include_description=False,
            )
            
            expected_file = Path(tmpdir) / "task_mermaid.md"
            content = expected_file.read_text()
            assert "```mermaid" in content
            assert "# Enums Values" not in content


class TestSaveHtml:
    """Tests for save_html method."""

    def test_save_html_default_location(self):
        """Test saving HTML to default location."""
        visualizer = PydanticVisualizer()
        visualizer.set_datamodel(SimpleModel)
        
        with tempfile.TemporaryDirectory() as tmpdir:
            visualizer.save_html(output_folder=tmpdir)
            
            expected_file = Path(tmpdir) / "simplemodel_mermaid.html"
            assert expected_file.exists()
            
            content = expected_file.read_text()
            assert "<!DOCTYPE html>" in content
            assert "SimpleModel" in content

    def test_save_html_custom_location(self):
        """Test saving HTML to custom location."""
        visualizer = PydanticVisualizer()
        visualizer.set_datamodel(User)
        
        with tempfile.TemporaryDirectory() as tmpdir:
            custom_path = Path(tmpdir) / "output"
            visualizer.save_html(output_folder=custom_path)
            
            expected_file = custom_path / "user_mermaid.html"
            assert expected_file.exists()

    def test_save_html_selective_content(self):
        """Test saving HTML with selective content."""
        visualizer = PydanticVisualizer()
        visualizer.set_datamodel(Task)
        
        with tempfile.TemporaryDirectory() as tmpdir:
            visualizer.save_html(
                output_folder=tmpdir,
                include_diagram=False,
                include_enums=True,
                include_description=True,
            )
            
            expected_file = Path(tmpdir) / "task_mermaid.html"
            content = expected_file.read_text()
            assert '<div class="mermaid">' not in content
            assert "<h1>Enums Values</h1>" in content


class TestPrivateMethods:
    """Tests for private helper methods."""

    def test_type_name_with_enum(self):
        """Test _type_name with enum type."""
        visualizer = PydanticVisualizer()
        visualizer.set_datamodel(Task)
        
        type_name = visualizer._type_name(Priority)
        assert type_name == "Enum.Priority"
        assert "Priority" in visualizer.enum_dict

    def test_type_name_with_basemodel(self):
        """Test _type_name with BaseModel type."""
        visualizer = PydanticVisualizer()
        
        type_name = visualizer._type_name(User)
        assert type_name == "User"

    def test_type_name_with_builtin(self):
        """Test _type_name with builtin type."""
        visualizer = PydanticVisualizer()
        
        type_name = visualizer._type_name(str)
        assert type_name == "str"

    def test_format_annotation_optional(self):
        """Test _format_annotation with Optional type."""
        visualizer = PydanticVisualizer()
        
        formatted = visualizer._format_annotation(Optional[str])
        assert "Optional" in formatted
        assert "str" in formatted

    def test_format_annotation_list(self):
        """Test _format_annotation with List type."""
        visualizer = PydanticVisualizer()
        
        formatted = visualizer._format_annotation(List[str])
        assert "List" in formatted
        assert "str" in formatted

    def test_add_relationship(self):
        """Test _add_relationship method."""
        visualizer = PydanticVisualizer()
        visualizer.set_datamodel(SimpleModel)
        
        visualizer._add_relationship("Parent", "Child")
        assert len(visualizer.relationships) > 0
        assert "Parent" in visualizer.relationships[-1]
        assert "Child" in visualizer.relationships[-1]

    def test_add_relationship_optional(self):
        """Test _add_relationship with optional flag."""
        visualizer = PydanticVisualizer()
        visualizer.set_datamodel(SimpleModel)
        
        visualizer._add_relationship("Parent", "Child", is_optional=True)
        relationship = visualizer.relationships[-1]
        assert ".." in relationship
        assert "optional" in relationship

    def test_add_relationship_list(self):
        """Test _add_relationship with list flag."""
        visualizer = PydanticVisualizer()
        visualizer.set_datamodel(SimpleModel)
        
        visualizer._add_relationship("Parent", "Child", is_list=True)
        relationship = visualizer.relationships[-1]
        assert "*" in relationship
        assert "list_of" in relationship


class TestEdgeCases:
    """Tests for edge cases and special scenarios."""

    def test_model_with_no_fields(self):
        """Test with a model that has no fields."""
        
        class EmptyModel(BaseModel):
            pass
        
        visualizer = PydanticVisualizer()
        visualizer.set_datamodel(EmptyModel)
        
        assert visualizer.model_cls == EmptyModel
        assert "EmptyModel" in visualizer.mermaid

    def test_deeply_nested_models(self):
        """Test with deeply nested models."""
        
        class Level3(BaseModel):
            value: str
        
        class Level2(BaseModel):
            level3: Level3
        
        class Level1(BaseModel):
            level2: Level2
        
        visualizer = PydanticVisualizer()
        visualizer.set_datamodel(Level1)
        
        assert "Level1" in visualizer.seen_classes
        assert "Level2" in visualizer.seen_classes
        assert "Level3" in visualizer.seen_classes

    def test_circular_reference_prevention(self):
        """Test that circular references don't cause infinite loops."""
        
        class Node(BaseModel):
            value: str
            children: Optional[List["Node"]] = None
        
        visualizer = PydanticVisualizer()
        visualizer.set_datamodel(Node)
        
        # Should complete without error
        assert "Node" in visualizer.seen_classes
        # Node should only appear once in seen_classes
        assert len([c for c in visualizer.all_classes if c.__name__ == "Node"]) == 1

    def test_model_with_default_factory(self):
        """Test model with default_factory."""
        
        class ModelWithFactory(BaseModel):
            items: List[str] = Field(default_factory=list)
        
        visualizer = PydanticVisualizer()
        visualizer.set_datamodel(ModelWithFactory)
        
        tables = visualizer.description_tables
        df = tables["ModelWithFactory"]
        # Check that default factory is represented
        assert any("<factory>" in str(val) for val in df["Default"].values)


class TestIntegration:
    """Integration tests combining multiple features."""

    def test_full_workflow(self):
        """Test complete workflow from model to output."""
        visualizer = PydanticVisualizer()
        visualizer.set_datamodel(Project)
        
        # Check all components are generated
        assert visualizer.mermaid
        assert visualizer.markdown()
        assert visualizer.html()
        assert visualizer.description
        assert visualizer.enum_tables
        
        # Check relationships are created
        assert len(visualizer.relationships) > 0
        
        # Check all models are tracked
        assert len(visualizer.all_classes) > 0

    def test_multiple_model_switches(self):
        """Test switching between different models."""
        visualizer = PydanticVisualizer()
        
        # First model
        visualizer.set_datamodel(SimpleModel)
        simple_mermaid = visualizer.mermaid
        
        # Second model
        visualizer.set_datamodel(User)
        user_mermaid = visualizer.mermaid
        
        # Third model
        visualizer.set_datamodel(Project)
        project_mermaid = visualizer.mermaid
        
        # Each should be different
        assert simple_mermaid != user_mermaid
        assert user_mermaid != project_mermaid
        
        # Final state should only reflect Project
        assert visualizer.title == "Project"
        assert visualizer.model_cls == Project

# Made with Bob
