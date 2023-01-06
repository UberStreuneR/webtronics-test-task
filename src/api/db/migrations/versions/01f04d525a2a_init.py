"""init

Revision ID: 01f04d525a2a
Revises: 
Create Date: 2023-01-06 11:59:57.410049

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '01f04d525a2a'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('user_id', sa.Integer(), autoincrement=True, nullable=False),
    sa.PrimaryKeyConstraint('user_id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('users')
    # ### end Alembic commands ###
