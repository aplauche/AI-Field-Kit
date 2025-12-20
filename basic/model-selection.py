# A simple dictionary can help with managing multiple configs for different tasks

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
