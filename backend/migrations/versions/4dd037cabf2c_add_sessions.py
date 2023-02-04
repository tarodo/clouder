"""add sessions

Revision ID: 4dd037cabf2c
Revises: 83942bd985ee
Create Date: 2022-12-24 20:00:31.731896

"""
from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision = '4dd037cabf2c'
down_revision = '83942bd985ee'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('session',
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('pack_id', sa.Integer(), nullable=False),
    sa.Column('sheet_number', sa.Integer(), nullable=False),
    sa.Column('start_time', sa.Date(), nullable=False),
    sa.Column('is_finished', sa.Boolean(), nullable=True),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['pack_id'], ['pack.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('session')
    # ### end Alembic commands ###