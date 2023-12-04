"""Rename field

Revision ID: b40106cd10e1
Revises: 018047731c3a
Create Date: 2023-12-02 18:57:53.177759

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "b40106cd10e1"
down_revision = "018047731c3a"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.execute("ALTER TABLE user_user RENAME COLUMN id TO uuid;")
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.execute("ALTER TABLE user_user RENAME COLUMN uuid TO id;")
    # ### end Alembic commands ###