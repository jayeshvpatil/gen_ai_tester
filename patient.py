from pydantic import BaseModel, Field

class Patient(BaseModel):
    firstName: str = Field(..., example="John")
    lastName: str = Field(..., example="Doe")
    email: str = Field(..., example="john.doe@gmail.com")

class PatientList(BaseModel):
    patients : list[Patient] = Field(description="Marketing List of Patients")

