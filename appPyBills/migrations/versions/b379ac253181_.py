"""empty message

Revision ID: b379ac253181
Revises: fbdd8d0baf7d
Create Date: 2017-09-23 13:28:42.084993

"""

# revision identifiers, used by Alembic.
revision = 'b379ac253181'
down_revision = 'fbdd8d0baf7d'

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('author', 'is_auth',
               existing_type=mysql.TINYINT(display_width=1),
               type_=sa.Boolean(),
               existing_nullable=True)
    op.add_column('bill', sa.Column('amount', sa.Float(), nullable=True))
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
    op.drop_column('bill', 'amount')
    op.alter_column('author', 'is_auth',
               existing_type=sa.Boolean(),
               type_=mysql.TINYINT(display_width=1),
               existing_nullable=True)
    # ### end Alembic commands ###
