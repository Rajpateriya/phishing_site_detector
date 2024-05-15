from pydantic import BaseModel

class BankNote(BaseModel):
    features: str