---
name: token-counting
description: "Use this when implementing token counting, cost estimation, or budget management for LLM API calls"
---

# Token Counting and Cost Estimation

Count tokens and estimate costs before making API calls to manage budgets.

## Example

```python
import tiktoken

def count_tokens(text, model="gpt-3.5-turbo"):
  encoding = tiktoken.encoding_for_model(model)
  return len(encoding.encode(text))

def estimate_cost(prompt, max_response_tokens=1000):
  prompt_tokens = count_tokens(prompt)
  res_tokens = int(max_response_tokens * 0.7) # rough estimate

  # pricing info
  cost_per_1k_prompt = 0.00005
  cost_per_1k_completion = 0.0015

  prompt_cost = (prompt_tokens / 1000) * cost_per_1k_prompt
  res_cost = (res_tokens / 1000) * cost_per_1k_completion

  return prompt_cost + res_cost


# If you want a hard cost limit, you could dynamically adjust the max response tokens based on the prompt cost - or truncate prompt
```

## Key Points

- Use `tiktoken` for accurate OpenAI token counts
- Estimate response tokens at ~70% of max_tokens for budgeting
- Pricing varies by model - keep rates updated
- Consider truncating prompts or adjusting max_tokens to stay within budget
