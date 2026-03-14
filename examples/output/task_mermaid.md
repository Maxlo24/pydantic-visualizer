# Task Diagram
```mermaid
classDiagram
class Comment {
    author   : str
    text     : str
    timestamp: str
}
style Comment fill: #FFEFDD, stroke: #000, stroke-width: 1px, color: #000
class Task {
    title      : str
    description: str
    priority   : Enum.Priority
    completed  : bool
    comments   : List[Comment]
}
style Task fill: #DDEDFF, stroke: #000, stroke-width: 1px, color: #000
Task --* Comment : Has_list_of_Comment
```
--------
# Enums Values

#### Priority
| ENUM     | Value   |
|:---------|:--------|
| `LOW`    | low     |
| `MEDIUM` | medium  |
| `HIGH`   | high    |
| `URGENT` | urgent  |
--------
# Task - Model Descriptions

## Task

Task model with priority and comments.

| Field         | Type          | Description               | Default     |
|:--------------|:--------------|:--------------------------|:------------|
| `title`       | str           | Task title                |             |
| `description` | str           | Detailed task description |             |
| `priority`    | Enum.Priority | Task priority level       |             |
| `completed`   | bool          | Whether task is completed | `False`     |
| `comments`    | List[Comment] | Task comments             | `<factory>` |

## Comment

Comment on a task.

| Field       | Type   | Description               |
|:------------|:-------|:--------------------------|
| `author`    | str    | Comment author            |
| `text`      | str    | Comment text              |
| `timestamp` | str    | When the comment was made |
