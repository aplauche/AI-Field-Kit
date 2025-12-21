# Class-based inheritance for specialized AI services

class BaseAI:
  def __init__(self, api_key):
    self.api_key = api_key
    self.usage_stats = {
      'total_tokens': 0,
      'total_cost': 0.0
    }
  
  def _call_api(self, prompt):
    """Implement in subclasses"""
    raise NotImplementedError("You must implement _call_api within subclass.")
  
  def track_usage(self, tokens, cost):
    self.usage_stats["total_tokens"] += tokens
    self.usage_stats["total_cost"] += cost

  def get_stats(self):
    return self.usage_stats
  
# Example 1: Coding focused AI service
class CoderAI(BaseAI):
  def __init__(self, api_key, language="python"):
    super().__init__(api_key)
    self.language = language

  def _call_api(self, prompt):
    # Here you would implement the actual call based on your provider...
    return f"API response: "
  
  def explain_code(self, code):
    # Specialized prompt engineering - this could be much more advanced to suit needs
    prompt = f"Explain this {self.language} code: \n {code}"
    response = self._call_api(prompt)

    # Real world we would get usage stats from response
    self.track_usage(tokens=1000, cost=0.03)

    return response
  
  def fix_error(self, code, error):
    prompt = f"Examine this {self.language} code and fix the error. Code: \n {code} \n Error: \n {error}"
    response = self._call_api(prompt)

    # Real world we would get usage stats from response
    self.track_usage(tokens=1000, cost=0.03)

    return response


# Example 2: WordPress specific AI service
class WordPressAI(BaseAI):
  def __init__(self, api_key):
    super().__init__(api_key)

  def _call_api(self, prompt):
    # Here you would implement the actual call based on your provider...
    # you could also include system prompts here...
    return f"API response: " 
  
  def create_block(self, block_description):
    prompt = f"Generate the PHP and javascript files for the following custom block spec: {block_description}"
    response = self._call_api(prompt)

    # Real world we would get usage stats from response
    self.track_usage(tokens=1000, cost=0.03)

    return response
  
  def propose_plugin(self, functionality):
    prompt = f"I want to accomplish the following on a wordpress site: {functionality} \n\n Reccommend a plugin that would meet my needs."
    response = self._call_api(prompt)

    # Real world we would get usage stats from response
    self.track_usage(tokens=1000, cost=0.03)

    return response
