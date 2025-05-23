"""add stocks column

Revision ID: 2372f3db5050
Revises: 996495887b23
Create Date: 2025-04-24 16:05:11.398824

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2372f3db5050'
down_revision = '996495887b23'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('stocks', sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('stocks', 'created_at')
    # ### end Alembic commands ### 