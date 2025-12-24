# This demonstrates the principles behind a naive React agent architecture
# IMPORTANT: not for production use

class ReactAgent:
  def __init__(self, llm, tools):
    self.llm = llm
    self.tools = tools
    self.history = []

  def run(self, task):
    self.history.append(f"task: {task}")
    while not self.is_complete(task):
      # Reason
      thought = self.think()
      self.history.append(f"Thought: {thought}")

      # Decide on action
      action = self.decide_action(thought)
      self.history.append(f"Action: {action}")

      # Execute and Observe
      observation = self.act(action)
      self.history.append(f"Observation: {observation}")

    return self.final_answer(task)
  
  def think(self):
    prompt = f"""
    {chr(10).join(self.history)} 
    What should I do next? Think step-by-step.   
    """
    return self.llm.generate(prompt)
  
  def decide_action(self, thought):
    prompt = f"""
    Based on this thought: {thought}
    With these available tools: {self.tools}
    What action should I take next?
    Format: TOOLNAME[ARGS]
    """
    return self.llm.generate(prompt)
  
  def act(self, action):
    """Implement logic for custom tool running"""
    return "Result of the tool"
  
  def final_answer(self, task):
    prompt = f"""
    This is our goal: {task}
    Our final observation: {self.history[-1]}
    Provide a summary of our findings
    """
    return self.llm.generate(prompt)
  
  def is_complete(self, task):
    prompt = f"""
    This is our goal: {task}
    Work so far: {chr(10).join(self.history)}
    Have we reached our goal yet?
    Format: true / false
    """
    return self.llm.generate(prompt)
    