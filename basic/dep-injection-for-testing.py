# Using dependency injection is useful when you want mocked AI functionality

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

if is_prod: # this would be a real condition
  prod_email_builder.build_email("Let's get coffee soon", "friendly")
else:
  mock_email_builder.build_email("Let's get coffee soon", "friendly")