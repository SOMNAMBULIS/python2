from pydantic import BaseModel, ConfigDict



class UserAdd(BaseModel):
    name: str
    age: int
    
class User(UserAdd):    
    id: int
    
    model_config = ConfigDict(from_attributes=True)    
       
class UserId(BaseModel):
    id: int

class QuestionAdd(BaseModel):
    name: str
    anwer: str
    opt1: str
    opt2: str
    opt3: str | None

class Question(QuestionAdd):
    id: int

    model_config = ConfigDict(from_attributes=True)

class QuestrionId(BaseModel):
    id: int