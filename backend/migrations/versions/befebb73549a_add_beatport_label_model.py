"""add beatport label model

Revision ID: befebb73549a
Revises: 015f5faee482
Create Date: 2022-10-26 06:22:00.712126

"""
from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision = 'befebb73549a'
down_revision = '015f5faee482'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('label',
    sa.Column('name', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('url', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('bp_id', sa.Integer(), nullable=False),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_label_bp_id'), 'label', ['bp_id'], unique=False)
    op.create_index(op.f('ix_label_name'), 'label', ['name'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_label_name'), table_name='label')
    op.drop_index(op.f('ix_label_bp_id'), table_name='label')
    op.drop_table('label')
    # ### end Alembic commands ###
