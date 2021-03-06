"""Add Plant model

Revision ID: dc290b4e9dea
Revises: d4867f3a4c0a
Create Date: 2021-05-14 13:53:21.437080

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'dc290b4e9dea'
down_revision = 'd4867f3a4c0a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('plant',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('description', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_plant_description'), 'plant', ['description'], unique=False)
    op.create_index(op.f('ix_plant_id'), 'plant', ['id'], unique=False)
    op.create_index(op.f('ix_plant_name'), 'plant', ['name'], unique=False)
    op.alter_column('user', 'email',
               existing_type=sa.VARCHAR(),
               nullable=False)
    op.alter_column('user', 'hashed_password',
               existing_type=sa.VARCHAR(),
               nullable=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('user', 'hashed_password',
               existing_type=sa.VARCHAR(),
               nullable=True)
    op.alter_column('user', 'email',
               existing_type=sa.VARCHAR(),
               nullable=True)
    op.drop_index(op.f('ix_plant_name'), table_name='plant')
    op.drop_index(op.f('ix_plant_id'), table_name='plant')
    op.drop_index(op.f('ix_plant_description'), table_name='plant')
    op.drop_table('plant')
    # ### end Alembic commands ###
