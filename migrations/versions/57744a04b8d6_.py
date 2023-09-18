"""empty message

Revision ID: 57744a04b8d6
Revises: ae1fb18a7629
Create Date: 2023-09-17 17:03:23.030710

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '57744a04b8d6'
down_revision = 'ae1fb18a7629'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('animals', schema=None) as batch_op:
        batch_op.add_column(sa.Column('phone', sa.String(length=64), nullable=True))
        batch_op.drop_column('owner_phone')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('animals', schema=None) as batch_op:
        batch_op.add_column(sa.Column('owner_phone', sa.INTEGER(), autoincrement=False, nullable=True))
        batch_op.drop_column('phone')

    # ### end Alembic commands ###
