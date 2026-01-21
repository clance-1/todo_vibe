"""initial

Revision ID: 0001_initial
Revises: 
Create Date: 2026-01-20
"""
from alembic import op
import sqlalchemy as sa

revision = '0001_initial'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'user',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('username', sa.String(80), nullable=False, unique=True),
        sa.Column('password_hash', sa.String(200), nullable=False),
    )

    op.create_table(
        'todo',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('user_id', sa.Integer, sa.ForeignKey('user.id'), nullable=False),
        sa.Column('title', sa.String(200), nullable=False),
        sa.Column('category', sa.String(20), nullable=False),
        sa.Column('date', sa.String(10), nullable=False),
        sa.Column('completed', sa.Boolean, nullable=False, server_default=sa.text('false')),
        sa.Column('created_at', sa.DateTime, nullable=False, server_default=sa.text('now()')),
    )


def downgrade():
    op.drop_table('todo')
    op.drop_table('user')
