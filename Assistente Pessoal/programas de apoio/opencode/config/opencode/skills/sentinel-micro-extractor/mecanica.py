from pydantic import BaseModel, Field
import filelock
class Codigo(BaseModel):
    codigo: str = Field(pattern=r"^[0-9]{5}$")
    def validate(self): return self.model_validate(self.model_dump())
