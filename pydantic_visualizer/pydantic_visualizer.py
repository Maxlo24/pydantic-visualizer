"""
Pydantic to Mermaid Diagram Generator

This module provides functionality to convert Pydantic models into Mermaid class diagrams.
"""

import webbrowser
from pathlib import Path
from typing import Any, Union, get_args, get_origin

import pandas as pd
from pydantic import BaseModel
from pydantic_core import PydanticUndefined

from .type_checkers import (
    is_basemodel_type,
    is_enum_type,
    unwrap_optional,
)


class PydanticVisualizer:
    """
    A visualizer that converts Pydantic models to Mermaid class diagrams.
    
    This class analyzes Pydantic models and their relationships, generating
    Mermaid diagram syntax that can be rendered as class diagrams. It supports
    nested models, enums, optional fields, and lists.
    
    Args:
        object_color: Hex color for regular object classes
        list_color: Hex color for list-type classes
        enum_color: Hex color for enum classes
        
    Example:
        >>> from pydantic import BaseModel
        >>> from pydantic_visualizer import PydanticVisualizer
        >>>
        >>> class User(BaseModel):
        ...     name: str
        ...     age: int
        >>>
        >>> visualizer = PydanticVisualizer()
        >>> visualizer.set_datamodel(User)
        >>> print(visualizer.mermaid)
    """

    def __init__(
        self,
        object_color: str = "#DDEDFF",
        list_color: str = "#FFEFDD",
        enum_color: str = "#DDFFEA",
        html_color: str = "#006699",
    ):
        # Configuration settings
        self.object_color = object_color
        self.list_color = list_color
        self.enum_color = enum_color
        self.html_color = html_color

        # State containers - initialized but empty
        self.title: str = "Diagram"
        self.model_cls: type[BaseModel] | None = None
        self.enum_dict: dict = {}
        self.seen_classes: set = set()
        self.all_classes: list[type[BaseModel]] = []
        self.lines: list[str] = ["classDiagram"]
        self.relationships: list[str] = []

    def set_datamodel(self, model_cls: type[BaseModel]) -> None:
        """
        Set or reset the data model to visualize.
        
        This method resets all internal state and processes the new model.
        The title is automatically set to the class name.
        
        Args:
            model_cls: A Pydantic BaseModel class to visualize
            
        Example:
            >>> visualizer = PydanticVisualizer()
            >>> visualizer.set_datamodel(User)
            >>> # Later, visualize a different model
            >>> visualizer.set_datamodel(Product)
        """
        # Reset state containers
        self.model_cls = model_cls
        self.title = model_cls.__name__  # Set title to class name
        self.enum_dict = {}
        self.seen_classes = set()
        self.all_classes = []
        self.lines = ["classDiagram"]
        self.relationships = []

        # Process the new model
        self._add_class(model_cls)

    @property
    def mermaid(self) -> str:
        """
        Returns the complete Mermaid diagram string for the model.
        
        Returns:
            A string containing the Mermaid diagram syntax
        """
        return "\n".join(self.lines + self.relationships)

    def markdown(
        self,
        include_diagram: bool = True,
        include_enums: bool = True,
        include_description: bool = True
    ) -> str:
        """
        Returns the complete Markdown document with embedded Mermaid diagram.
        
        Args:
            include_diagram: Whether to include the Mermaid diagram. Default: True
            include_enums: Whether to include enum tables. Default: True
            include_description: Whether to include model description tables. Default: True
        
        Returns:
            A string containing the Markdown document with Mermaid syntax
        """
        content_parts = []

        if include_diagram:
            content_parts.append(f"# {self.title} Diagram\n```mermaid\n{self.mermaid}\n```")

        if include_enums and len(self.enum_dict) > 0:
            content_parts.append(self.enum_markdown_tables)

        if include_description:
            content_parts.append(self.description)

        return "\n".join(content_parts)

    def html(
        self,
        include_diagram: bool = True,
        include_enums: bool = True,
        include_description: bool = True
    ) -> str:
        """
        Returns the complete HTML document with embedded Mermaid diagram.
        
        Args:
            include_diagram: Whether to include the Mermaid diagram. Default: True
            include_enums: Whether to include enum tables. Default: True
            include_description: Whether to include model description tables. Default: True
        
        Returns:
            A string containing the complete HTML document with Mermaid syntax
        """
        html_parts = [
            '<!DOCTYPE html>',
            '<html>',
            '<head>',
            '<meta charset="UTF-8">',
            f'<title>{self.title} Diagram</title>',
            '<script src="https://cdn.jsdelivr.net/npm/mermaid/dist/mermaid.min.js"></script>',
            '<script>mermaid.initialize({startOnLoad:true});</script>',
            '<style>',
            'body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif; margin: 20px; background-color: #f5f5f5; }',
            f'h1 {{ color: #333; border-bottom: 3px solid {self.html_color}; padding-bottom: 10px; }}',
            'h2 { color: #555; margin-top: 30px; }',
            'h2 + p { color: #666; font-style: italic; margin: 10px 0; }',
            'h4 { color: #666; margin-top: 20px; }',
            'table.dataframe { border-collapse: collapse; width: 100%; margin: 20px 0; background-color: white; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }',
            f'table.dataframe thead {{ background-color: {self.html_color}; color: white; }}',
            'table.dataframe th { padding: 12px; text-align: left; font-weight: 600; border: none; }',
            'table.dataframe td { padding: 10px 12px; border-bottom: 1px solid #ddd; }',
            'table.dataframe tbody tr:hover { background-color: #f5f5f5; }',
            f'table.dataframe tbody tr:last-child td {{ border-bottom: 2px solid {self.html_color}; }}',
            'code { background-color: #f4f4f4; padding: 2px 6px; border-radius: 3px; font-family: "Courier New", monospace; color: #000; font-weight: bold; }',
            '.mermaid { background-color: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.1); margin: 20px 0; }',
            '</style>',
            '</head>',
            '<body>'
        ]

        if include_diagram:
            html_parts.append(f'<center><h1>{self.title} Diagram</h1></center>')
            html_parts.append(f'<center><div class="mermaid">\n{self.mermaid}\n</div></center>')

        if include_enums and len(self.enum_dict) > 0:
            html_parts.append(self.enum_html_tables)

        if include_description:
            html_parts.append(self.description_html_tables)

        html_parts.extend(['</body>', '</html>'])

        return "\n".join(html_parts)

    @property
    def description(self) -> str:
        """
        Returns a markdown description with tables for each class and subclass.
        
        Each table includes field name, type, description, default value, and examples.
        
        Returns:
            A string containing markdown tables describing all models
        """
        return self.description_markdown_tables

    @property
    def enum_mermaid_string(self) -> str:
        """Generates the mermaid string for enums based on current state."""
        return self._get_enums_mermaid()

    @property
    def enum_tables(self) -> dict[str, pd.DataFrame]:
        """
        Returns a dictionary of pandas DataFrames for each enum.
        
        Returns:
            A dictionary where keys are enum names and values are DataFrames
        """
        return self.enum_dict

    @property
    def enum_markdown_tables(self) -> str:
        """
        Generates markdown tables for enums using pandas to_markdown().
        
        Returns:
            A string containing markdown tables for all enums
        """
        if not self.enum_dict:
            return ""

        lines = ["--------", "# Enums Values\n"]
        for enum_name, df in self.enum_dict.items():
            lines.append(f"#### {enum_name}")
            lines.append(df.to_markdown(index=False))
            lines.append("--------")
        return "\n".join(lines)

    @property
    def enum_html_tables(self) -> str:
        """
        Generates HTML tables for enums using pandas to_html().
        
        Returns:
            A string containing HTML tables for all enums
        """
        import re

        if not self.enum_dict:
            return ""

        lines = ["<h1>Enums Values</h1>"]
        for enum_name, df in self.enum_dict.items():
            lines.append(f"<h4>{enum_name}</h4>")
            html_table = df.to_html(index=False, escape=False)
            # Convert backtick-wrapped text to <code> tags
            html_table = re.sub(r'`([^`]+)`', r'<code>\1</code>', html_table)
            lines.append(html_table)
        return "\n".join(lines)

    @property
    def description_tables(self) -> dict[str, pd.DataFrame]:
        """
        Returns a dictionary of pandas DataFrames for each model's description.
        
        Returns:
            A dictionary where keys are model names and values are DataFrames
        """
        description_dfs = {}

        for cls in self.all_classes:
            data = {
                'Field': [],
                'Type': [],
                'Description': [],
                'Default': [],
                'Examples': []
            }

            for field_name, field in cls.__pydantic_fields__.items():
                # Field name
                data['Field'].append(f"`{field_name}`")

                # Type
                data['Type'].append(self._format_annotation(field.annotation))

                # Description
                data['Description'].append(field.description or "")

                # Default value
                default_str = ""
                if field.default is not PydanticUndefined and field.default is not None:
                    default_str = f"`{field.default}`"
                elif field.default_factory is not None:
                    default_str = "`<factory>`"
                data['Default'].append(default_str)

                # Examples
                examples_str = ""
                if hasattr(field, 'examples') and field.examples:
                    examples_str = ", ".join(f"`{ex}`" for ex in field.examples)
                elif hasattr(field, 'json_schema_extra') and field.json_schema_extra:
                    if isinstance(field.json_schema_extra, dict) and 'examples' in field.json_schema_extra:
                        examples = field.json_schema_extra['examples']
                        if isinstance(examples, list):
                            examples_str = ", ".join(f"`{ex}`" for ex in examples)
                data['Examples'].append(examples_str)

            df = pd.DataFrame(data)
            # Remove columns where all values are empty strings
            df = df.loc[:, (df != "").any(axis=0)]
            description_dfs[cls.__name__] = df

        return description_dfs

    @property
    def description_markdown_tables(self) -> str:
        """
        Generates markdown tables for model descriptions using pandas to_markdown().
        
        Returns:
            A string containing markdown tables for all models
        """
        lines = [f"# {self.title} - Model Descriptions\n"]

        for cls in self.all_classes:
            lines.append(f"## {cls.__name__}\n")

            if cls.__doc__:
                lines.append(f"{cls.__doc__.strip()}\n")

            df = self.description_tables[cls.__name__]
            lines.append(df.to_markdown(index=False))
            lines.append("")  # Empty line between tables

        return "\n".join(lines)

    @property
    def description_html_tables(self) -> str:
        """
        Generates HTML tables for model descriptions using pandas to_html().
        
        Returns:
            A string containing HTML tables for all models
        """
        import re

        lines = [f"<h1>{self.title} - Model Descriptions</h1>"]

        for cls in self.all_classes:
            lines.append(f"<h2>{cls.__name__}</h2>")

            if cls.__doc__:
                lines.append(f"<p>{cls.__doc__.strip()}</p>")

            df = self.description_tables[cls.__name__]
            html_table = df.to_html(index=False, escape=False)
            # Convert backtick-wrapped text to <code> tags
            html_table = re.sub(r'`([^`]+)`', r'<code>\1</code>', html_table)
            lines.append(html_table)

        return "\n".join(lines)

    def _add_relationship(
        self,
        parent: str,
        child: str,
        label_prefix: str = "Has",
        is_list: bool = False,
        is_optional: bool = False,
    ) -> None:
        arrow_line = "--"
        arrow_shape = ">"
        optional_str = ""
        list_str = ""
        if is_optional:
            arrow_line = ".."
            optional_str = "optional_"
        if is_list:
            arrow_shape = "*"
            list_str = "list_of_"

        self.relationships.append(
            f"{parent} {arrow_line}{arrow_shape} {child} : {label_prefix}_{optional_str}{list_str}{child}"
        )

    def _type_name(self, typ: Any) -> str:
        if is_enum_type(typ):
            # Create DataFrame directly from enum members
            data = {
                'ENUM': [f"`{key}`" for key in typ.__members__.keys()],
                'Value': [member.value for member in typ.__members__.values()]
            }
            self.enum_dict[typ.__name__] = pd.DataFrame(data)
            return f"Enum.{typ.__name__}"
        if is_basemodel_type(typ):
            return typ.__name__
        if isinstance(typ, type):
            return typ.__name__

        # Fallback to string form
        s = str(typ)
        s = s.replace("typing.", "")
        s = s.replace("<class '", "").replace("'>", "")
        s = s.replace("<enum '", "Enum.").replace("'>", "")
        parts = s.split(".")
        return parts[-1] if parts else s

    def _format_annotation(self, annotation: Any) -> str:
        origin = get_origin(annotation)
        args = get_args(annotation)

        if origin is Union and args:
            non_none = [a for a in args if a is not type(None)]
            if len(non_none) == 1:
                inner_display = self._format_annotation(non_none[0])
                return f"Optional[{inner_display}]"
            else:
                inner = ", ".join(self._format_annotation(a) for a in non_none)
                return f"Union[{inner}]"

        if origin in (list, list) and args:
            item = args[0]
            item_str = (
                self._format_annotation(item)
                if get_origin(item)
                else self._type_name(item)
            )
            return f"List[{item_str}]"

        if origin is not None and args:
            inner = ", ".join(self._format_annotation(a) for a in args)
            return f"{origin.__name__}[{inner}]"

        return self._type_name(annotation)

    def _add_class(
        self, cls: type[BaseModel], is_list: bool = False, is_optional: bool = False
    ) -> None:
        cls_name = cls.__name__

        # Prevent infinite recursion or duplication
        if cls_name in self.seen_classes:
            return
        self.seen_classes.add(cls_name)
        self.all_classes.append(cls)  # Track for description tables (only added once due to seen_classes check)

        class_def = [f"class {cls_name} {{"]

        # Handle max length safely
        keys = cls.__pydantic_fields__.keys()
        max_field_str_length = max(len(k) for k in keys) if keys else 0

        for field_name, field in cls.__pydantic_fields__.items():
            ann = field.annotation
            display_type = self._format_annotation(ann)
            str_field_name = field_name.ljust(max_field_str_length, " ")
            class_def.append(f"    {str_field_name}: {display_type}")

            # Recursion for nested models
            ann_unwrapped, field_is_optional = unwrap_optional(ann)
            origin = get_origin(ann_unwrapped)
            args = get_args(ann_unwrapped)

            if origin in (list, list) and args:
                item = args[0]
                if is_basemodel_type(item):
                    self._add_class(item, is_list=True, is_optional=field_is_optional)
                    self._add_relationship(
                        cls_name,
                        item.__name__,
                        is_list=True,
                        is_optional=field_is_optional,
                    )
            elif is_basemodel_type(ann_unwrapped):
                self._add_class(
                    ann_unwrapped, is_list=False, is_optional=field_is_optional
                )
                self._add_relationship(
                    cls_name, ann_unwrapped.__name__, is_optional=field_is_optional
                )

        class_def.append("}")

        color = self.object_color
        if is_list:
            color = self.list_color

        stroke = ""
        if is_optional:
            stroke = ",stroke-dasharray: 10 10"

        class_def.append(
            f"style {cls_name} fill: {color}, stroke: #000, stroke-width: 1px, color: #000{stroke}"
        )
        self.lines.extend(class_def)

    def _get_enums_mermaid(self) -> str:
        """Generate mermaid diagrams for enums."""
        lines = ["# Enums Values\n"]
        for enum_name, df in self.enum_dict.items():
            class_def = [f"#### {enum_name}"]
            class_def.extend(["```mermaid", "classDiagram", f"class {enum_name} {{"])
            for _, row in df.iterrows():
                class_def.append(f"    {row['ENUM']} : {row['Value']}")
            class_def.append("}")
            class_def.append(
                f"style {enum_name} fill: {self.enum_color}, stroke: #000, stroke-width: 1px, color: #000"
            )
            class_def.append("```")
            lines.extend(class_def)
        return "\n".join(lines)

    def save_markdown(
        self,
        output_folder: str | Path | None = None,
        include_diagram: bool = True,
        include_enums: bool = True,
        include_description: bool = True
    ) -> None:
        """
        Save the diagram as a Markdown file with embedded Mermaid syntax.
        
        Args:
            output_folder: Folder path where to save the file. If None, uses current directory "./".
            (The filename is automatically set to {title}_mermaid.md)
            include_diagram: Whether to include the Mermaid diagram. Default: True
            include_enums: Whether to include enum tables. Default: True
            include_description: Whether to include model description tables. Default: True
        """
        if output_folder is None:
            output_folder = Path("./")
        else:
            output_folder = Path(output_folder)

        # Ensure the folder exists
        output_folder.mkdir(parents=True, exist_ok=True)

        # Enforce the filename format
        filename = f"{self.title.lower()}_mermaid.md"
        output_path = output_folder / filename

        # Build the content based on parameters
        content = self.markdown(
            include_diagram,
            include_enums,
            include_description
        )

        with open(output_path, "w") as file:
            file.write(content)

    def save_html(
        self,
        output_folder: str | Path | None = None,
        include_diagram: bool = True,
        include_enums: bool = True,
        include_description: bool = True
    ) -> None:
        """
        Save the diagram as an HTML file.
        
        Args:
            output_folder: Folder path where to save the file. If None, uses current directory "./".
            (The filename is automatically set to {title}_mermaid.html)
            include_diagram: Whether to include the Mermaid diagram. Default: True
            include_enums: Whether to include enum tables. Default: True
            include_description: Whether to include model description tables. Default: True
        """
        if output_folder is None:
            output_folder = Path("./")
        else:
            output_folder = Path(output_folder)

        # Ensure the folder exists
        output_folder.mkdir(parents=True, exist_ok=True)

        # Enforce the filename format
        filename = f"{self.title.lower()}_mermaid.html"
        output_path = output_folder / filename

        # Build the content based on parameters
        content = self.html(
            include_diagram,
            include_enums,
            include_description
        )

        with open(output_path, "w") as file:
            file.write(content)

    def show(
        self,
        include_diagram: bool = True,
        include_enums: bool = True,
        include_description: bool = True
    ) -> None:
        """
        Open the diagram directly in the default web browser without saving a file.
        
        Creates a temporary HTML file with the diagram and opens it in the browser.
        The temporary file is automatically cleaned up after opening.
        
        Args:
            include_diagram: Whether to include the Mermaid diagram. Default: True
            include_enums: Whether to include enum tables. Default: True
            include_description: Whether to include model description tables. Default: True
        """
        import os
        import tempfile

        # Build the HTML content based on parameters
        content = self.html(
            include_diagram,
            include_enums,
            include_description
        )

        # Create a temporary HTML file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.html', delete=False) as f:
            f.write(content)
            temp_path = f.name

        # Open in browser
        webbrowser.open('file://' + os.path.abspath(temp_path))
