"""create images table

Revision ID: 90f40e3f8dc3
Revises: 
Create Date: 2023-03-08 14:46:59.363780

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '90f40e3f8dc3'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('images', sa.Column('id',sa.Integer(), nullable=False, primary_key=True))
    pass


def downgrade() -> None:
    op.drop_table('images')
    pass
