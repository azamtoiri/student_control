"""add user_image and short_description

Revision ID: 2999ce04298b
Revises: 082ead5113d7
Create Date: 2024-03-16 10:30:01.212220

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2999ce04298b'
down_revision: Union[str, None] = '082ead5113d7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('subjects', sa.Column('short_description', sa.String(), nullable=False))
    op.alter_column('subjects', 'description',
               existing_type=sa.VARCHAR(),
               nullable=False)
    op.add_column('users', sa.Column('user_image', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'user_image')
    op.alter_column('subjects', 'description',
               existing_type=sa.VARCHAR(),
               nullable=True)
    op.drop_column('subjects', 'short_description')
    # ### end Alembic commands ###
