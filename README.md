# Pydantic Visualizer

[![PyPI version](https://badge.fury.io/py/pydantic-visualizer.svg)](https://badge.fury.io/py/pydantic-visualizer)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Convert your Pydantic models into beautiful Mermaid class diagrams with ease! 🎨

Pydantic Visualizer automatically generates visual representations of your Pydantic data models, making it easier to understand complex data structures, document your APIs, and communicate your data architecture.

## 🚀 Turn your pydantic model in mermaid diagram

![image](./img/exemple.jpg)


## ✨ Features

- 🔄 **Automatic Conversion**: Transform Pydantic models to Mermaid diagrams instantly
- 🎯 **Relationship Detection**: Automatically identifies and visualizes model relationships
- 📊 **Enum Support**: Special handling and visualization for Enum types
- 🎨 **Customizable Colors**: Configure colors for different element types
- 📝 **Multiple Export Formats**: Save as Markdown or HTML
- 🌐 **Browser Preview**: Open diagrams directly in your browser
- 🔗 **Nested Models**: Handles complex nested model structures
- ⚡ **Type-Safe**: Fully typed with comprehensive type hints

## 📦 Installation

### Using pip

```bash
pip install pydantic-visualizer
```

### Using uv (recommended)

```bash
uv pip install pydantic-visualizer
```

```bash
uv add pydantic-visualizer
```


## Exemple :

```python

from pydantic_visualizer import PydanticVisualizer

# Define models
class Priority(str, Enum):
    """Task priority levels."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    URGENT = "urgent"


class Comment(BaseModel):
    """Comment on a task."""
    author: str = Field(description="Comment author")
    text: str = Field(description="Comment text")
    timestamp: str = Field(description="When the comment was made")


class Task(BaseModel):
    """Task model with priority and comments."""
    title: str = Field(description="Task title")
    description: str = Field(description="Detailed task description")
    priority: Priority = Field(description="Task priority level")
    completed: bool = Field(default=False, description="Whether task is completed")
    comments: List[Comment] = Field(default_factory=list, description="Task comments")


# Create a visualizer instance
visualizer = PydanticVisualizer()

# Set the data model to visualize
visualizer.set_datamodel(Task)

# Add the second model (Nothing change here as Task is already set)
visualizer.add_model(Task)

# Print the Mermaid diagram code
print(visualizer.mermaid)

# Print the markdown enum table
print(visualizer.enum_markdown_tables)

# Returns a markdown description with tables for each class and subclass.
print(visualizer.description)

# Open the diagram in your browser
visualizer.show()

# Saving complete markdown (diagram + enums + descriptions)
visualizer.save_markdown(
    output_folder="./examples/output",
    include_diagram=True,
    include_enums=True,
    include_description=True,
)

# Saving complete HTML (diagram + enums + descriptions)
visualizer.save_html(
    output_folder="./examples/output",
    include_diagram=True,
    include_enums=True,
    include_description=True,
)

```



> 📚 **More Examples**: Visit the [examples folder](https://github.com/Maxlo24/pydantic-visualizer/blob/main/examples) for 8+ complete, runnable examples covering:
> - Basic usage and nested models
> - Enum handling and custom colors
> - Complex relationships and self-referencing models
> - Saving to Markdown/HTML and browser preview
> - Adding multiple models to one diagram
>
> See the [Examples README](https://github.com/Maxlo24/pydantic-visualizer/blob/main/examples/README.md) for detailed descriptions and usage instructions.

--------

## 🎨 Diagram Features

### Relationship Types

- **Solid arrows** (`-->`) for required relationships
- **Dashed arrows** (`..>`) for optional relationships
- **Star notation** (`*`) for list/collection relationships

### Visual Indicators

- **Different colors** for objects, lists, and enums
- **Dashed borders** for optional nested models
- **Aligned field names** for better readability


### Development Setup

```bash
# Clone the repository
git clone https://github.com/Maxlo24/pydantic-visualizer.git
cd pydantic-visualizer

# Install dependencies with uv
uv pip install -e ".[dev]"

# Run tests
pytest

# Run linting
ruff check .

# Run type checking
mypy pydantic_visualizer
```

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built with [Pydantic](https://docs.pydantic.dev/) - Data validation using Python type hints
- Diagrams rendered with [Mermaid](https://mermaid.js.org/) - Generation of diagrams from text

## 📮 Contact & Support

- **Repo**: [GitHub Repo](https://github.com/Maxlo24/pydantic-visualizer)
- **Issues**: [GitHub Issues](https://github.com/Maxlo24/pydantic-visualizer/issues)
- **Discussions**: [GitHub Discussions](https://github.com/Maxlo24/pydantic-visualizer/discussions)

## 🗺️ Roadmap

- [ ] Support for Pydantic v1 models
- [ ] CLI tool for quick visualization
- [ ] Integration with FastAPI for automatic API documentation
- [ ] Export to additional formats (PNG, SVG, PDF)

---

Made with ❤️ by [Maxime Gillot](https://github.com/Maxlo24)