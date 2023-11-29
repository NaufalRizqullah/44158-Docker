from pydantic import BaseModel

class OutputBase(BaseModel):
    message: str
    class_predicted: str
    prob: float
    inference_time: str