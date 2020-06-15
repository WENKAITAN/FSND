"""empty message

Revision ID: 6374113eb5b2
Revises: 50265a11321d
Create Date: 2020-06-15 12:57:22.503265

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6374113eb5b2'
down_revision = '50265a11321d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('shows', sa.Column('artist_image_link', sa.String(), nullable=True))
    op.add_column('shows', sa.Column('artist_name', sa.String(), nullable=True))
    op.add_column('shows', sa.Column('venue_name', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('shows', 'venue_name')
    op.drop_column('shows', 'artist_name')
    op.drop_column('shows', 'artist_image_link')
    # ### end Alembic commands ###
