"""empty message

Revision ID: c0f1185fdf7a
Revises: 7e52163609ff
Create Date: 2024-07-04 18:36:41.813649

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c0f1185fdf7a'
down_revision = '7e52163609ff'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('personaje', schema=None) as batch_op:
        batch_op.alter_column('nacimiento',
               existing_type=sa.VARCHAR(length=120),
               nullable=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('personaje', schema=None) as batch_op:
        batch_op.alter_column('nacimiento',
               existing_type=sa.VARCHAR(length=120),
               nullable=True)

    # ### end Alembic commands ###
