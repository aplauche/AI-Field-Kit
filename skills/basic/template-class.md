---
name: template-class
description: "Use this when implementing prompt templates, reusable prompt patterns, or parameterized prompts"
---

# Prompt Template Class

Simple pattern for creating reusable, parameterized prompts.

## Example

```python
class PromptTemplate:
  def __init__(self, template):
    self.template = template

  def format(self, **kwargs):
    return self.template.format(**kwargs)


bug_fix_template = PromptTemplate("""
  Debug this {language} code:
  {code}
  Error: {error}
  Provide: Explanation, fixed code, and future prevention tips
  """)

# Usage
prompt = bug_fix_template.format(language="python", code=code, error=error)
```

## Key Points

- Templates use Python's `str.format()` with named placeholders
- Create templates for common tasks (debugging, explaining, generating)
- Templates ensure consistent prompt structure across calls
- Easy to version control and iterate on prompts
