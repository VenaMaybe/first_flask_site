"""create a bunch of planned tables 

Revision ID: cfb7f0dce7c4
Revises: 584d793996a6
Create Date: 2025-05-07 04:24:56.882062

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'cfb7f0dce7c4'
down_revision = '584d793996a6'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('node_types',
    sa.Column('id', sa.BigInteger(), nullable=False),
    sa.Column('type_of_node', sa.String(length=50), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('type_of_node')
    )
    op.create_table('nodes',
    sa.Column('id', sa.BigInteger(), nullable=False),
    sa.Column('node_type_id', sa.BigInteger(), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), nullable=True),
    sa.Column('created_by', sa.BigInteger(), nullable=True),
    sa.ForeignKeyConstraint(['created_by'], ['nodes.id'], ),
    sa.ForeignKeyConstraint(['node_type_id'], ['node_types.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('connections',
    sa.Column('id', sa.BigInteger(), nullable=False),
    sa.Column('from_node_id', sa.BigInteger(), nullable=False),
    sa.Column('to_node_id', sa.BigInteger(), nullable=False),
    sa.Column('type', sa.String(length=50), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), nullable=True),
    sa.ForeignKeyConstraint(['from_node_id'], ['nodes.id'], ),
    sa.ForeignKeyConstraint(['to_node_id'], ['nodes.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('persons',
    sa.Column('id', sa.BigInteger(), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.Column('email', sa.String(length=255), nullable=False),
    sa.Column('birthday', sa.Date(), nullable=False),
    sa.Column('owner_user_id', sa.BigInteger(), nullable=True),
    sa.ForeignKeyConstraint(['id'], ['nodes.id'], ),
    sa.ForeignKeyConstraint(['owner_user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
    )
    op.create_table('social_accounts',
    sa.Column('id', sa.BigInteger(), nullable=False),
    sa.Column('platform', sa.String(length=50), nullable=False),
    sa.Column('handle', sa.String(length=100), nullable=False),
    sa.ForeignKeyConstraint(['id'], ['nodes.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('claim_requests',
    sa.Column('id', sa.BigInteger(), nullable=False),
    sa.Column('person_id', sa.BigInteger(), nullable=False),
    sa.Column('requester_user_id', sa.BigInteger(), nullable=False),
    sa.Column('target_user_id', sa.BigInteger(), nullable=False),
    sa.Column('status', sa.Enum('pending', 'approved', 'denied', name='claim_status'), nullable=False),
    sa.Column('message', sa.Text(), nullable=True),
    sa.Column('created_at', sa.DateTime(timezone=True), nullable=True),
    sa.Column('decided_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['person_id'], ['persons.id'], ),
    sa.ForeignKeyConstraint(['requester_user_id'], ['users.id'], ),
    sa.ForeignKeyConstraint(['target_user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('claim_requests')
    op.drop_table('social_accounts')
    op.drop_table('persons')
    op.drop_table('connections')
    op.drop_table('nodes')
    op.drop_table('node_types')
    # ### end Alembic commands ###
