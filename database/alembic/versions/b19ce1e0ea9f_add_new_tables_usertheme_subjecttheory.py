"""add new tables: UserTheme SubjectTheory

Revision ID: b19ce1e0ea9f
Revises: 14acc6eeb00b
Create Date: 2024-03-23 14:23:08.832578

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b19ce1e0ea9f'
down_revision: Union[str, None] = '14acc6eeb00b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('enrollments_user_id_fkey', 'enrollments', type_='foreignkey')
    op.create_foreign_key(None, 'enrollments', 'users', ['user_id'], ['user_id'], ondelete='CASCADE')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'enrollments', type_='foreignkey')
    op.create_foreign_key('enrollments_user_id_fkey', 'enrollments', 'users', ['user_id'], ['user_id'])
    # ### end Alembic commands ###
