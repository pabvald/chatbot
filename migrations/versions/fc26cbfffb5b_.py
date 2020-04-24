"""empty message

Revision ID: fc26cbfffb5b
Revises: 10ba57d3fa61
Create Date: 2020-04-18 12:08:15.155831

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'fc26cbfffb5b'
down_revision = '10ba57d3fa61'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('users', 'first_name',
               existing_type=sa.VARCHAR(length=40),
               nullable=False)
    op.drop_column('users', 'username')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('username', sa.VARCHAR(length=40), autoincrement=False, nullable=True))
    op.alter_column('users', 'first_name',
               existing_type=sa.VARCHAR(length=40),
               nullable=True)
    # ### end Alembic commands ###
