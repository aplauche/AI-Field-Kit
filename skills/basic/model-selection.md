---
name: model-selection
description: "Use this when implementing dynamic model selection, model switching based on task type, or routing to different models based on complexity"
---

# Dynamic Model Selection

Use dictionary-based configuration to switch between models based on task type or complexity.

## Example

```python
models = {
  "quick": {
    "name": "gpt-3.5-turbo",
    "max_tokens": 500,
    "temperature": 0.7
  },
  "code": {
    "name": "gpt-4",
    "max_tokens": 1000,
    "temperature": 0.3
  },
  "complex": {
    "name": "gpt-4",
    "max_tokens": 2000,
    "temperature": 0.5
  }
}

def use_model(task_type:str):
  # you can include more complex logic here as well if desired
  return models[task_type]

def model_by_complexity(complexity:int):
  if(complexity > 6):
    return models["quick"]
  else:
    return models["complex"]
```

## Key Points

- Store model configs in dictionaries for easy switching
- Use task-based selection (quick, code, complex) for explicit control
- Implement complexity scoring to auto-route requests
- Keep temperature low (0.3) for code, higher (0.7) for creative tasks
