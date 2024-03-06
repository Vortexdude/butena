from app.core.db.models import Department, Employee
from sqlalchemy.orm import Session


class BaseService:
    def __init__(self, db: Session):
        self.db = db

    def save_to_db(self, data):
        self.db.add(data)
        self.db.commit()
        self.db.refresh(data)
        return data

    def get_all(self, Model):
        return self.db.query(Model).all()

    def get_by_id(self, Model, _id: str):
        return self.db.query(Model).filter_by(id=_id).first()

    def get_by_email(self, Model, email: str):
        return self.db.query(Model).filter_by(email=email).first()

    def get_by_name(self, Model, name: str):
        return self.db.query(Model).filter_by(name=name).first()


class DepartmentServices(BaseService):
    def __init__(self, db: Session):
        super().__init__(db)

    def create(self, name: str = None):
        _dep = self.get_by_name(Model=Department, name=name)
        if _dep:
            return {"Status": "Department is already exists"}

        dp_in = Department(name=name)
        self.db.add(dp_in)
        self.db.commit()
        self.db.refresh(dp_in)
        return dp_in

    def get_all_departments(self):
        return self.get_all(Model=Department)


class EmployeeServices(BaseService):
    def __init__(self, db: Session):
        super().__init__(db)

    def create_record(self, data: dict):
        email = data['email']
        emp = self.get_by_email(Model=Employee, email=email)
        if emp:
            return {"Status": "Employee already exist"}

        dp_in = Employee(**data)
        return self.save_to_db(dp_in)

    def delete_record(self, **data):
        email = data['email']
        emp = self.get_by_email(Model=Employee, email=email)
        if emp:
            return {"Status": "Record is already exist so deleting the record"}

    def update(self, **data):
        pass

    def get_all_employee(self):
        return self.get_all(Model=Employee)
