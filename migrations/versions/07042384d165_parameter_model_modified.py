"""Parameter model modified

Revision ID: 07042384d165
Revises: d24e1e56f563
Create Date: 2020-03-31 11:31:13.602080

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '07042384d165'
down_revision = 'd24e1e56f563'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('parameters', sa.Column('original', sa.String(length=100), nullable=True))
    op.add_column('parameters', sa.Column('value', sa.String(length=100), nullable=True))
    op.drop_column('parameters', 'text')
    op.drop_column('parameters', 'entry')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('parameters', sa.Column('entry', sa.VARCHAR(length=100), autoincrement=False, nullable=True))
    op.add_column('parameters', sa.Column('text', sa.VARCHAR(length=100), autoincrement=False, nullable=True))
    op.drop_column('parameters', 'value')
    op.drop_column('parameters', 'original')
    # ### end Alembic commands ###
