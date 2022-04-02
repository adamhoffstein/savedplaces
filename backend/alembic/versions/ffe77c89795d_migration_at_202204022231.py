"""migration at 202204022231

Revision ID: ffe77c89795d
Revises: cb697b121368
Create Date: 2022-04-02 15:31:23.192432

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "ffe77c89795d"
down_revision = "cb697b121368"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "savedplaces", sa.Column("placelist_id", sa.Integer(), nullable=True)
    )
    op.create_foreign_key(
        None, "savedplaces", "placelists", ["placelist_id"], ["id"]
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, "savedplaces", type_="foreignkey")
    op.drop_column("savedplaces", "placelist_id")
    # ### end Alembic commands ###