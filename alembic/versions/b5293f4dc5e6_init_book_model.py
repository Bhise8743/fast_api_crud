"""init book model

Revision ID: b5293f4dc5e6
Revises: 3f75052c743c
Create Date: 2023-12-28 16:09:19.416524

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b5293f4dc5e6'
down_revision: Union[str, None] = '3f75052c743c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('contact',
    sa.Column('id', sa.BigInteger(), nullable=False),
    sa.Column('f_name', sa.String(length=50), nullable=False),
    sa.Column('l_name', sa.String(length=50), nullable=True),
    sa.Column('email', sa.String(length=50), nullable=False),
    sa.Column('phone', sa.BigInteger(), nullable=True),
    sa.Column('location', sa.String(length=100), nullable=True),
    sa.Column('book_id', sa.BigInteger(), nullable=False),
    sa.ForeignKeyConstraint(['book_id'], ['book.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('f_name')
    )
    op.create_index(op.f('ix_contact_id'), 'contact', ['id'], unique=False)
    op.add_column('book', sa.Column('b_name', sa.String(length=50), nullable=False))
    op.drop_constraint('book_name_key', 'book', type_='unique')
    op.create_unique_constraint(None, 'book', ['b_name'])
    op.drop_column('book', 'name')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('book', sa.Column('name', sa.VARCHAR(length=50), autoincrement=False, nullable=False))
    op.drop_constraint(None, 'book', type_='unique')
    op.create_unique_constraint('book_name_key', 'book', ['name'])
    op.drop_column('book', 'b_name')
    op.drop_index(op.f('ix_contact_id'), table_name='contact')
    op.drop_table('contact')
    # ### end Alembic commands ###