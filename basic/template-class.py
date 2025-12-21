# Useful simple pattern for templatizing your prompts

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

bug_fix_template.format(language="python", code=code, error=error) # these would be defined in real-world use