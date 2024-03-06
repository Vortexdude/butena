from datetime import datetime

from pydantic import BaseModel


class DepartmentBase(BaseModel):
    name: str


class DepartmentCreate(DepartmentBase):
    pass


class Department(DepartmentBase):
    id: int

    class Config:
        orm_mode: True


class EmployeeBase(BaseModel):
    name: str
    email: str
    department_id: int


class EmployeeCreate(EmployeeBase):
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "name": "Nitin",
                    "email": "nnamdev@company.com",
                    'department_id': 1,
                }
            ]
        }
    }


class Employee(EmployeeBase):
    id: int
    department: Department
    hire_date: datetime

    class Config:
        orm_mode = True
