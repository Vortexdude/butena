from app.core.db.models import Department, Employee
from sqlalchemy.orm import Session
from app.exceptions import UserException, DatabaseException, StatusCode


class BaseService:
    def __init__(self, db: Session):
        self.db = db

    def save_to_db(self, data):
        try:
            self.db.add(data)
            self.db.commit()
            self.db.refresh(data)
        except Exception as e:
            self.db.rollback()
            raise e
        return data

    def get_all(self, Model):
        try:
            return self.db.query(Model).all()
        except Exception as e:
            raise e

    def get_by_id(self, Model, _id: str):
        try:
            return self.db.query(Model).filter_by(id=_id).first()
        except Exception as e:
            raise e

    def get_by_email(self, Model, email: str):
        try:
            return self.db.query(Model).filter_by(email=email).first()
        except Exception as e:
            raise e

    def get_by_name(self, Model, name: str):
        try:
            return self.db.query(Model).filter_by(name=name).first()
        except Exception as e:
            raise e


class DepartmentServices(BaseService):
    def __init__(self, db: Session):
        super().__init__(db)

    def create(self, name: str = None):
        _dep = self.get_by_name(Model=Department, name=name)
        if _dep:
            raise DatabaseException(status_code=StatusCode.ALREADY_202)

        dp_in = Department(name=name)
        self.db.add(dp_in)
        self.db.commit()
        self.db.refresh(dp_in)
        return dp_in

    def get_all_departments(self):
        departments = self.get_all(Model=Department)
        if not departments:
            raise DatabaseException(status_code=StatusCode.NOT_FOUND_204)

        return departments


class EmployeeServices(BaseService):
    def __init__(self, db: Session):
        super().__init__(db)

    def create_record(self, data: dict):
        email = data['email']
        emp = self.get_by_email(Model=Employee, email=email)
        if emp:
            raise UserException(status_code=StatusCode.CONFLICT_409)

        dp_in = Employee(**data)
        return self.save_to_db(dp_in)

    def delete_record(self, **data):
        email = data['email']
        emp = self.get_by_email(Model=Employee, email=email)
        if not emp:
            raise UserException(status_code=StatusCode.BAD_REQUEST_400)

    def update(self, **data):
        pass

    def get_all_employee(self):
        employees = self.get_all(Model=Employee)
        if not employees:
            raise DatabaseException(status_code=StatusCode.NOT_FOUND_204)

        return employees
