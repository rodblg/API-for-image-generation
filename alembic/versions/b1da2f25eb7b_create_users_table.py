"""Create users table

Revision ID: b1da2f25eb7b
Revises: 74deb5110007
Create Date: 2023-03-08 16:10:49.073390

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b1da2f25eb7b'
down_revision = '74deb5110007'
branch_labels = None
depends_on = None


def upgrade() -> None:

    op.create_table('users',
                    sa.Column('id', sa.Integer(), primary_key=True, nullable=False),
                    sa.Column('name', sa.String(), nullable=False),
                    sa.Column('email', sa.String(), nullable=False),
                    sa.Column('password', sa.String(), nullable=False),
                    sa.Column('created_at', sa.TIMESTAMP(timezone=True),
                                      server_default=sa.text('now()'), nullable=False)
                    )
    pass


def downgrade() -> None:
    op.drop_table('users')
    pass
