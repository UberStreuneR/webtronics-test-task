"""unique_username

Revision ID: 3643fd8a91e6
Revises: 988ad9c660a8
Create Date: 2023-01-08 12:04:39.881613

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3643fd8a91e6'
down_revision = '988ad9c660a8'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint(None, 'users', ['username'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'users', type_='unique')
    # ### end Alembic commands ###
