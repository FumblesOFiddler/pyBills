"""empty message

Revision ID: 507062a13078
Revises: 4b58e44fb73c
Create Date: 2017-09-24 14:39:46.692817

"""

# revision identifiers, used by Alembic.
revision = '507062a13078'
down_revision = '4b58e44fb73c'

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('author', 'is_auth',
               existing_type=mysql.TINYINT(display_width=1),
               type_=sa.Boolean(),
               existing_nullable=True)
    op.add_column('bill', sa.Column('pdf', sa.String(length=255), nullable=True))
    op.alter_column('bill', 'paid',
               existing_type=mysql.TINYINT(display_width=1),
               type_=sa.Boolean(),
               existing_nullable=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('bill', 'paid',
               existing_type=sa.Boolean(),
               type_=mysql.TINYINT(display_width=1),
               existing_nullable=True)
    op.drop_column('bill', 'pdf')
    op.alter_column('author', 'is_auth',
               existing_type=sa.Boolean(),
               type_=mysql.TINYINT(display_width=1),
               existing_nullable=True)
    # ### end Alembic commands ###
