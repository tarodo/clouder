"""add user to styleg

Revision ID: 49229117b843
Revises: 9351566155e5
Create Date: 2022-10-15 14:00:26.347826

"""
from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision = '49229117b843'
down_revision = '9351566155e5'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('style', sa.Column('user_id', sa.Integer(), nullable=False))
    op.create_foreign_key(None, 'style', 'user', ['user_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'style', type_='foreignkey')
    op.drop_column('style', 'user_id')
    # ### end Alembic commands ###