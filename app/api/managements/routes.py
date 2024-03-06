from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.orm import Session
from .schema import DepartmentCreate, EmployeeCreate, Department, Employee
from .services import DepartmentServices, EmployeeServices
from app.core.db.engine import get_db

router = APIRouter()


@router.get("/departments", summary="Get all the departments")
async def get_department(db: Session = Depends(get_db)):
    dp = DepartmentServices(db)
    return dp.get_all_departments()


@router.post("/create_department", summary="Create the department")
async def create_department(data: DepartmentCreate, db: Session = Depends(get_db)):
    data = data.dict()
    dp = DepartmentServices(db)
    dp.create(**data)
    return {"Status": "Created"}


@router.get("/employee", summary="Get all the employees")
async def get_employee(db: Session = Depends(get_db)):
    dp = EmployeeServices(db)
    return dp.get_all_employee()


@router.post("/on_board_employee", summary="Onboard employee", response_model=Employee)
async def onboard_employee(data: EmployeeCreate, db: Session = Depends(get_db)):
    emp = EmployeeServices(db)
    return emp.create_record(data.dict())


@router.delete("/off_board_employee", summary="Offboard employee")
async def off_board_employee(data: EmployeeCreate, db: Session = Depends(get_db)):
    data = data.dict()
    emp = EmployeeServices(db)
    return emp.delete_record(**data)


@router.post("/update_employee", summary="Update the employee details")
async def update_employee(data: EmployeeCreate, db: Session = Depends(get_db)):
    data = data.dict()
    emp = EmployeeServices(db)
    return emp.update(**data)
