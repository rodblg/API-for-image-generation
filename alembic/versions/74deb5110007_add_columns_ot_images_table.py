"""add columns ot images table

Revision ID: 74deb5110007
Revises: 90f40e3f8dc3
Create Date: 2023-03-08 15:08:36.592165

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '74deb5110007'
down_revision = '90f40e3f8dc3'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('images', sa.Column('path_image', sa.String(), nullable=False))
    op.add_column('images', sa.Column('prompt', sa.String(), nullable=False))
    op.add_column('images', sa.Column('created_at', sa.TIMESTAMP(timezone=True),
                                      server_default=sa.text('now()'), nullable=False))

    pass


def downgrade() -> None:
    op.drop_column('images','path_image')
    op.drop_column('images','prompt')
    op.drop_column('images','created_at')
    pass
