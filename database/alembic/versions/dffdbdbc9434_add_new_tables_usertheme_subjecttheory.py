"""add new tables: UserTheme SubjectTheory

Revision ID: dffdbdbc9434
Revises: b19ce1e0ea9f
Create Date: 2024-03-23 14:26:18.268015

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'dffdbdbc9434'
down_revision: Union[str, None] = 'b19ce1e0ea9f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user_theme',
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('theme', sa.String(), server_default='light', nullable=False),
    sa.Column('seed_color', sa.String(), server_default='green', nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['users.user_id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('user_id')
    )
    op.create_table('subject_theory',
    sa.Column('topic_id', sa.Integer(), nullable=False),
    sa.Column('topic_title', sa.String(), nullable=False),
    sa.Column('topic_data', sa.String(), nullable=False),
    sa.ForeignKeyConstraint(['topic_id'], ['subjects.subject_id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('topic_id'),
    sa.UniqueConstraint('topic_title')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('subject_theory')
    op.drop_table('user_theme')
    # ### end Alembic commands ###