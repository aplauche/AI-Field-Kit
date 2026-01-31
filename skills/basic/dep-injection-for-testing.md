---
name: dep-injection-for-testing
description: "Use this when making AI services testable, mocking LLM calls for tests, or implementing dependency injection for AI components"
---

# Dependency Injection for Testable AI

Inject AI services to enable easy mocking during tests without real API calls.

## Example

```python
class EmailBuilder():

  def __init__(self, ai):
    self.ai = ai

  def build_email(self, contents, tone):
    prompt = f"""
    Write an email using a {tone} tone of voice with the following contents {contents}
    """
    return self.ai.generate(prompt)

class ProdAIService:
  def generate(prompt):
    # Insert your real AI call logic here
    return "this would be the real generated content..."

class MockAIService:
  def generate(prompt):
    return f"""
    *** MOCKED CONTENT ***
    Subject: Example Email
    Content: This email would be generated using the following prompt:
    {prompt}
    """

# Usage
prod_ai = ProdAIService()
mock_ai = MockAIService()

prod_email_builder = EmailBuilder(prod_ai)
mock_email_builder = EmailBuilder(mock_ai)

if is_prod:
  prod_email_builder.build_email("Let's get coffee soon", "friendly")
else:
  mock_email_builder.build_email("Let's get coffee soon", "friendly")
```

## Key Points

- Pass AI service as constructor parameter (dependency injection)
- Create mock services that return predictable responses
- Mock services can include the prompt in output for debugging
- Enables fast tests without API costs or rate limits
