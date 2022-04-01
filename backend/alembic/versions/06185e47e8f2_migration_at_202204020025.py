"""migration at 202204020025

Revision ID: 06185e47e8f2
Revises: 866bf57c65f0
Create Date: 2022-04-01 17:25:39.750979

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '06185e47e8f2'
down_revision = '866bf57c65f0'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('savedplaces')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('savedplaces',
    sa.Column('created_date', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
    sa.Column('updated_date', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('user_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('place_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['place_id'], ['places.id'], name='savedplaces_place_id_fkey'),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], name='savedplaces_user_id_fkey'),
    sa.PrimaryKeyConstraint('id', name='savedplaces_pkey')
    )
    # ### end Alembic commands ###
