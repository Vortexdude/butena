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

    def get_all(self):
        return self.db.query(Department).all()


class DepartmentServices(BaseService):
    def __init__(self, db: Session):
        super().__init__(db)

    def create(self, name: str = None):
        dp_in = Department(name=name)
        self.db.add(dp_in)
        self.db.commit()
        self.db.refresh(dp_in)

    def get_by_id(self, dp_id):
        return self.db.query(Department).filter_by(id=dp_id).first()


class EmployeeServices(BaseService):
    def __init__(self, db: Session):
        super().__init__(db)

    def create(self, data: dict):
        dp_in = Employee(**data)
        return self.save_to_db(dp_in)

    def get_by_id(self, dp_id):
        return self.db.query(Employee).filter_by(id=dp_id).first()

    def delete(self, **data):
        pass

    def update(self, **data):
        pass
