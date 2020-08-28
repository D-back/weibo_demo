"""empty message

Revision ID: 6d8bf60dc33c
Revises: 7c87e96a5c97
Create Date: 2020-08-27 22:40:14.682857

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6d8bf60dc33c'
down_revision = '7c87e96a5c97'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('thumb',
    sa.Column('uid', sa.Integer(), nullable=False),
    sa.Column('wid', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('uid', 'wid')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('thumb')
    # ### end Alembic commands ###