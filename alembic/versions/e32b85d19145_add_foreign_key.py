"""add foreign key

Revision ID: e32b85d19145
Revises: b1da2f25eb7b
Create Date: 2023-03-08 16:16:11.833588

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e32b85d19145'
down_revision = 'b1da2f25eb7b'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('images', sa.Column('owner_id', sa.Integer(), nullable=False))
    op.create_foreign_key('images_user_fk',source_table='images',referent_table='users',
                          local_cols=['owner_id'],remote_cols=['id'],ondelete='CASCADE')
    pass


def downgrade() -> None:
    op.drop_constraint('images_user_fk',table_name='images')
    op.drop_column('images','owner_id')
    pass
