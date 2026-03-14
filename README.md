# Pydantic Visualizer

[![PyPI version](https://badge.fury.io/py/pydantic-visualizer.svg)](https://badge.fury.io/py/pydantic-visualizer)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Convert your Pydantic models into beautiful Mermaid class diagrams with ease! 🎨

Pydantic Visualizer automatically generates visual representations of your Pydantic data models, making it easier to understand complex data structures, document your APIs, and communicate your data architecture.

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

### For Development

```bash
# Clone the repository
git clone https://github.com/maxime-gillot/pydantic-visualizer.git
cd pydantic-visualizer

# Install with development dependencies using uv
uv pip install -e ".[dev]"
```

## 🚀 Quick Start

```python

from enum import Enum
from typing import List
from pydantic import BaseModel, Field
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


# Create the visualizer
visualizer = PydanticVisualizer()

# Add your models
visualizer.set_datamodel(Task)

# Get the Mermaid diagram code
mermaid_code = visualizer.mermaid
print(mermaid_code)

# Save as Markdown
generator.save_markdown("./output")

# Or open in browser as HTML
generator.show_html("./output")
```

### Result TODO



## 📖 Usage Examples

### Basic Model Visualization

```python
from pydantic import BaseModel
from pydantic_visualizer import PydanticToMermaidGenerator

class Product(BaseModel):
    name: str
    price: float
    in_stock: bool

generator = PydanticToMermaidGenerator(title="Product Model")
generator.add_pydantic_model(Product)
print(generator.get_mermaid())
```

### Custom Colors

```python
generator = PydanticToMermaidGenerator(
    title="My Models",
    object_color="#E8F4F8",      # Light blue for objects
    list_color="#FFF4E6",         # Light orange for lists
    enum_color="#E8F8F5"          # Light green for enums
)
```

### Multiple Models

```python
generator = PydanticToMermaidGenerator(title="Complete System")
generator.add_pydantic_model(User)
generator.add_pydantic_model(Product)
generator.add_pydantic_model(Order)

# All models and their relationships will be in one diagram
generator.save_markdown("complete_system.md")
```

### Working with Enums

The generator automatically detects and visualizes Enum types with special formatting:

```python
from enum import Enum

class Status(str, Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"

class Request(BaseModel):
    title: str
    status: Status

generator = PydanticToMermaidGenerator()
generator.add_pydantic_model(Request)

# Enums are shown in the diagram and detailed in tables
print(generator.enum_tables_string)
```

## 🎨 Diagram Features

### Relationship Types

- **Solid arrows** (`-->`) for required relationships
- **Dashed arrows** (`..>`) for optional relationships
- **Star notation** (`*`) for list/collection relationships

### Visual Indicators

- **Different colors** for objects, lists, and enums
- **Dashed borders** for optional nested models
- **Aligned field names** for better readability

## 🤝 Contributing

Contributions are welcome! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for details.

### Development Setup

```bash
# Clone the repository
git clone https://github.com/maxime-gillot/pydantic-visualizer.git
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

- **Issues**: [GitHub Issues](https://github.com/maxime-gillot/pydantic-visualizer/issues)
- **Discussions**: [GitHub Discussions](https://github.com/maxime-gillot/pydantic-visualizer/discussions)

## 🗺️ Roadmap

- [ ] Support for Pydantic v1 models
- [ ] Additional diagram types (ER diagrams, sequence diagrams)
- [ ] CLI tool for quick visualization
- [ ] Integration with FastAPI for automatic API documentation
- [ ] Export to additional formats (PNG, SVG, PDF)
- [ ] Interactive web-based diagram editor

---

Made with ❤️ by [Maxime Gillot](https://github.com/maxime-gillot)