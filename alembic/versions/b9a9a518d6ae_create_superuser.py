"""create superuser

Revision ID: b9a9a518d6ae
Revises: 29d55cea1d9e
Create Date: 2024-03-05 15:20:24.509380

"""
from typing import Sequence, Union

from alembic import op
from app.core.utils import JWT
from sqlalchemy.orm import Session
from app.core.db.models import User

SUPER_USERS = [
    dict(
        first_name='Nitin',
        last_name='Namdev',
        email='nnamdev@butena.com',
        user_name='nnamdev',
        password='Nothingspecial',
        super_user=True
    ),
]


def populate_db(session):
    for data in SUPER_USERS:
        email = data['email']
        _user = session.query(User).filter_by(email=email).one_or_none()
        if _user:
            print(f"Skipping {email} sponsor because it already exists.")
            continue
        params = data.copy()
        params['user_id'] = int(100)
        params['hashed_password'] = JWT.get_password_hash(params['password'])
        params.pop('password')

        user = User(**params)
        try:
            session.add(user)
            session.commit()
            print(f"User {data['user_name']}created")
        except Exception as e:
            session.rollback()
            print(f"Error while creating {data['user_name']} user:")
            print(f"\t{e}")


# revision identifiers, used by Alembic.
revision: str = 'b9a9a518d6ae'
down_revision: Union[str, None] = '29d55cea1d9e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    session = Session(op.get_bind())
    populate_db(session)


def downgrade():
    session = Session(op.get_bind())
    session.query(User).delete()
