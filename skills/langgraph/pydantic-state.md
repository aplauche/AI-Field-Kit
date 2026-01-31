---
name: pydantic-state
description: "Use this when implementing state validation with Pydantic in LangGraph, adding runtime type checking, or validating agent state fields"
---

# Pydantic State Validation

Use Pydantic BaseModel for state with runtime validation and custom validators.

## Example

```python
from pydantic import BaseModel, field_validator, ValidationError


class CustomState(BaseModel):
    name: str
    mood: str  # "happy" or "sad"

    @field_validator('mood')
    def validate_mood(cls, value):
        # Ensure the mood is either "happy" or "sad"
        if value not in ["happy", "sad"]:
            raise ValueError("Each mood must be either 'happy' or 'sad'")
        return value


# Valid state
state = CustomState(name="John Doe", mood="happy")

# Invalid state - raises ValidationError
try:
    state = CustomState(name="John Doe", mood="mad")
except ValidationError as e:
    print("Validation Error:", e)
```

## Key Points

- Inherit from `BaseModel` for Pydantic validation
- `@field_validator('field_name')`: Custom validation logic
- Validation runs automatically on instantiation
- `ValidationError` raised for invalid values
- Type hints are enforced at runtime
- Useful for ensuring agent state stays consistent
