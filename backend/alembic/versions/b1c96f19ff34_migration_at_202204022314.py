"""migration at 202204022314

Revision ID: b1c96f19ff34
Revises: 7d079344d5b6
Create Date: 2022-04-02 16:14:59.223011

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "b1c96f19ff34"
down_revision = "7d079344d5b6"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column("placelists", sa.Column("name", sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("placelists", "name")
    # ### end Alembic commands ###
