# Pydantic Visualizer Examples

This directory contains example scripts demonstrating the various features and capabilities of the Pydantic Visualizer package.


## 📖 Usage Examples

### Basic Model Visualization

```python
from pydantic import BaseModel
from pydantic_visualizer import PydanticVisualizer

class Product(BaseModel):
    name: str
    price: float
    in_stock: bool

visualizer = PydanticVisualizer()
visualizer.set_datamodel(Product)
print(visualizer.mermaid)
```

### Custom Colors

```python
visualizer = PydanticVisualizer(
    object_color="#E8F4F8",      # Light blue for objects
    list_color="#FFF4E6",         # Light orange for lists
    enum_color="#E8F8F5",         # Light green for enums
    html_color="#006699"          # Color for HTML styling
)
```

### Multiple Models

```python
visualizer = PydanticVisualizer()
visualizer.set_datamodel(User)      # Set the first model
visualizer.add_model(Product)       # Add additional models
visualizer.add_model(Order)

# All models and their relationships will be in one diagram
visualizer.save_markdown("./output")
```

### Working with Enums

The visualizer automatically detects and visualizes Enum types with special formatting:

```python
from enum import Enum

class Status(str, Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"

class Request(BaseModel):
    title: str
    status: Status

visualizer = PydanticVisualizer()
visualizer.set_datamodel(Request)

# Enums are shown in the diagram and detailed in tables
print(visualizer.enum_markdown_tables)
```

### Output Options

```python
# Get raw Mermaid code
mermaid_code = visualizer.mermaid

# Get markdown with optional sections
markdown = visualizer.markdown(
    include_diagram=True,
    include_enums=True,
    include_description=True
)

# Get HTML with optional sections
html = visualizer.html(
    include_diagram=True,
    include_enums=True,
    include_description=True
)

# Save to files
visualizer.save_markdown("./output")
visualizer.save_html("./output")

# Open directly in browser (temporary file)
visualizer.show()
```

### Access Model Information

```python
# Get enum tables as pandas DataFrames
enum_tables = visualizer.enum_tables  # dict[str, pd.DataFrame]

# Get description tables as pandas DataFrames
description_tables = visualizer.description_tables  # dict[str, pd.DataFrame]

# Get formatted markdown descriptions
descriptions = visualizer.description  # str
```


## 📚 Examples Overview

### 01. Basic Usage (`01_basic_usage.py`)
**What it demonstrates:**
- Creating a simple Pydantic model
- Initializing the PydanticVisualizer
- Setting a data model
- Printing Mermaid diagrams and markdown output

**Run it:**
```bash
python examples/01_basic_usage.py
```

### 02. Nested Models (`02_nested_models.py`)
**What it demonstrates:**
- Models containing other models as fields
- Optional nested models
- Automatic relationship detection
- How relationships are visualized with arrows

**Run it:**
```bash
python examples/02_nested_models.py
```

### 03. Enum Handling (`03_enum_handling.py`)
**What it demonstrates:**
- Using Python Enums in Pydantic models
- Special visualization for Enum types
- Enum value tables in the output
- Multiple enums in one diagram

**Run it:**
```bash
python examples/03_enum_handling.py
```

### 04. Custom Colors (`04_custom_colors.py`)
**What it demonstrates:**
- Customizing colors for objects, lists, and enums, html
- Creating different color themes (monochrome)
- Using hex color codes
- Visual distinction between element types

**Run it:**
```bash
python examples/04_custom_colors.py
```
### 05. Complex Relationships (`05_complex_relationships.py`)
**What it demonstrates:**
- Self-referencing models (recursive relationships)
- Multiple levels of nesting (4+ levels deep)
- Lists of nested models
- Optional relationships
- Mixed relationship types
- Real-world project management scenario

**Run it:**
```bash
python examples/05_complex_relationships.py
```

### 06. Save Markdown (`06_save_markdown.py`)
**What it demonstrates:**
- Saving diagrams as Markdown files
- Controlling output content (diagram, enums, descriptions)
- Specifying output folders
- Automatic filename generation

**Run it:**
```bash
python examples/06_save_markdown.py
```

### 07. Save HTML (`07_save_html.py`)
**What it demonstrates:**
- Saving diagrams as HTML files
- Embedded Mermaid.js rendering
- Browser-ready output
- Interactive diagrams

**Run it:**
```bash
python examples/07_save_html.py
```

### 08. Add Multiple Models (`08_add_multiple_models.py`)
**What it demonstrates:**
- Adding multiple independent models to the same diagram using `add_model()`
- Handling overlapping submodels (shared models between different main models)
- Automatic title generation with all model names
- Preventing duplicate classes in the diagram
- Real-world scenario with User, Company, and Store models sharing Address and ContactInfo

**Run it:**
```bash
python examples/08_add_multiple_models.py
```


## 🚀 Running the Examples

### Prerequisites
Make sure you have the package installed:

```bash
# Using pip
pip install pydantic-visualizer

# Or using uv (recommended)
uv pip install pydantic-visualizer

# Or for development
uv pip install -e ".[dev]"
```


## 📁 Output Files

Some examples create output files:
- `06_save_markdown.py` creates `./output/employee_mermaid.md`
- `07_save_html.py` creates `./output/task_mermaid.html`

The `output/` directory will be created automatically if it doesn't exist.

## 🎨 Viewing the Results

### Markdown Files
- Open in any markdown viewer (VS Code, GitHub, etc.)
- Mermaid diagrams will render automatically in supported viewers

### HTML Files
- Open directly in any web browser
- No additional setup required
- Interactive diagrams with hover effects

## 💡 Tips

1. **Start Simple**: Begin with `01_basic_usage.py` to understand the basics
2. **Experiment**: Modify the examples to test with your own models
3. **Combine Features**: Mix and match features from different examples
4. **Check Output**: Look at the generated files to see the final results

## 🔗 Related Documentation

- [Main README](../README.md) - Package overview and installation
- [Contributing Guide](../CONTRIBUTING.md) - How to contribute

---

Happy visualizing! 🎨