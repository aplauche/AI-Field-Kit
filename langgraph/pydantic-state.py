# When creating custom state objects Pydantic provides runtime validation

from pydantic import BaseModel, field_validator, ValidationError

class CustomState(BaseModel):
    name: str
    mood: str # "happy" or "sad" 

    @field_validator('mood')
    def validate_mood(cls, value):
        # Ensure the mood is either "happy" or "sad"
        if value not in ["happy", "sad"]:
            raise ValueError("Each mood must be either 'happy' or 'sad'")
        return value

try:
    state = CustomState(name="John Doe", mood="mad")
except ValidationError as e:
    print("Validation Error:", e)