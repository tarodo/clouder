"""add pack model

Revision ID: 4cb3629c3567
Revises: 84c519ad3d53
Create Date: 2022-10-23 11:11:36.612792

"""
from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision = '4cb3629c3567'
down_revision = '84c519ad3d53'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('pack',
    sa.Column('style_id', sa.Integer(), nullable=False),
    sa.Column('period_id', sa.Integer(), nullable=False),
    sa.Column('sheets_count', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['period_id'], ['period.id'], ),
    sa.ForeignKeyConstraint(['style_id'], ['style.id'], ),
    sa.PrimaryKeyConstraint('style_id', 'period_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('pack')
    # ### end Alembic commands ###
