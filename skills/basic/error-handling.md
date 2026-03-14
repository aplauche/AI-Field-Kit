---
name: error-handling
description: "Use this when implementing error handling, retry logic, or error translation for LLM/AI API calls across different providers"
---

# Error Handling for AI APIs

Translates provider-specific errors into unified error types and implements retry logic with exponential backoff.

## Example

```python
import time
from openai import RateLimitError as OAIRateLimitError
from anthropic import RateLimitError as AnthropicRateLimitError

class AIError(Exception):
  """Base class"""
  pass

class RateLimitError(AIError):
  """Too many requests"""
  pass

class TokenLimitError(AIError):
  """Request exceeds token limit"""
  pass

class ContentFilterError(AIError):
  """Content blocked"""
  pass

def call_ai(prompt, provider="openai"):
  """Wrapper with error translation"""
  try:
    if provider == "openai":
      response = openai_client.chat.completions.create(
        model = "gpt-3.5-turbo",
        messages = [
          {"role": "user", "content": prompt}
        ]
      )
      return response.choices[0].message.content
  except OAIRateLimitError:
    raise RateLimitError("Rate limit exceeded")
  except Exception as e:
    if "maximum content length" in str(e):
      raise TokenLimitError("Token limit")
    elif "content_filter" in str(e):
      raise ContentFilterError("Blocked content")
    raise # for unkown errors just use blank raise

def call_with_retry(prompt, retry_limit=3):
  """Call the llm with retry logic and error handling"""
  for attempt in range(retry_limit):
    try:
      response = call_ai(prompt)
      return response

    except RateLimitError:
      # retry
      if attempt < retry_limit - 1:
        wait_time = 2 ** attempt
        print(f"Rate limited. Waiting {wait_time} seconds...")
      else:
        print("Max retries reached. Try again later.")

    except TokenLimitError:
      # shorten the prompt
      print(f"Truncating prompt...")
      prompt = prompt[:1000] + "..." # In prod this would be a summarization or other technique
      attempt -= 1 # this does not count towards retries

    except ContentFilterError:
      print("Content was blocked! Try again with a different prompt.")
      return "Not available - content blocked."

    except Exception as e:
      print(f"Unexpected error: {e}")
      print("Trying again in 3 seconds...")
      if attempt < retry_limit:
        time.sleep(3)
      else:
        raise # catch all
```

## Key Points

- Create unified error classes that abstract away provider differences
- Use exponential backoff for rate limit errors (2^attempt seconds)
- Handle token limits by truncating/summarizing prompts
- Content filter errors should not retry - return gracefully
