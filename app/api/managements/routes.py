from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.orm import Session
from .schema import DepartmentCreate, EmployeeCreate, Department, Employee
from .services import DepartmentServices, EmployeeServices
from app.core.db.engine import get_db

router = APIRouter()


@router.get("/departments", response_model=Department)
async def get_department(db: Session = Depends(get_db)):
    dp = DepartmentServices(db)
    return dp.get_all()


@router.post("/create_department")
async def create_department(data: DepartmentCreate, db: Session = Depends(get_db)):
    data = data.dict()
    dp = DepartmentServices(db)
    dp.create(**data)
    return {"Status": "Created"}


@router.get("/")
async def get_employee():
    return {"Employees": []}


@router.post("/on_board_employee", response_model=Employee)
async def onboard_employee(data: EmployeeCreate, db: Session = Depends(get_db)):
    emp = EmployeeServices(db)
    return emp.create(data.dict())


@router.delete("/off_board_employee")
async def off_board_employee(data: EmployeeCreate, db: Session = Depends(get_db)):
    data = data.dict()
    emp = EmployeeServices(db)
    return emp.delete(**data)


@router.post("/update_employee")
async def update_employee(data: EmployeeCreate, db: Session = Depends(get_db)):
    data = data.dict()
    emp = EmployeeServices(db)
    return emp.update(**data)
