"""added biglearn knowledge models

Revision ID: cbac16278e4f
Revises: b9287092c49f
Create Date: 2017-04-17 15:31:43.103265

"""
from alembic import op
import sqlalchemy as sa

from sqlalchemy.schema import Sequence, CreateSequence, DropSequence

# revision identifiers, used by Alembic.
revision = 'cbac16278e4f'
down_revision = 'b9287092c49f'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('cmatrix',
    sa.Column('id', sa.Integer(), primary_key=True, nullable=False),
    sa.Column('learner_id', sa.String(length=255), nullable=False),
    sa.Column('topic_id', sa.String(length=255), nullable=False),
    sa.Column('mastery', sa.Float(precision=53), nullable=False),
    sa.Column('created', sa.DateTime(), primary_key=True, nullable=False),
    )
    op.create_index(op.f('ix_cmatrix_learner_id'), 'cmatrix', ['learner_id'], unique=False)
    op.create_index(op.f('ix_cmatrix_topic_id'), 'cmatrix', ['topic_id'], unique=False)
    op.create_table('cpercent',
    sa.Column('id', sa.Integer(), primary_key=True, nullable=False),
    sa.Column('percentile', sa.Integer(), nullable=False),
    sa.Column('mastery', sa.Float(precision=53), nullable=False),
    sa.Column('created', sa.DateTime(), primary_key=True, nullable=False),
    sa.UniqueConstraint('percentile')
    )
    op.create_index(op.f('ix_cpercent_mastery'), 'cpercent', ['mastery'], unique=False)
    op.create_table('mu',
    sa.Column('id', sa.Integer(), primary_key=True, nullable=False),
    sa.Column('question_id', sa.String(length=255), nullable=False),
    sa.Column('difficulty', sa.Float(precision=53), nullable=False),
    sa.Column('created', sa.DateTime(), primary_key=True, nullable=False),
    sa.UniqueConstraint('question_id')
    )
    op.create_table('wmatrix',
    sa.Column('id', sa.Integer(), primary_key=True, nullable=False),
    sa.Column('question_id', sa.String(length=255), nullable=False),
    sa.Column('topic_id', sa.String(length=255), nullable=False),
    sa.Column('assoc_score', sa.Float(precision=53), nullable=False),
    sa.Column('created', sa.DateTime(), primary_key=True, nullable=False),
    )


def downgrade():
    op.drop_table('wmatrix')
    op.drop_table('mu')
    op.drop_index(op.f('ix_cpercent_mastery'), table_name='cpercent')
    op.drop_table('cpercent')
    op.drop_index(op.f('ix_cmatrix_topic_id'), table_name='cmatrix')
    op.drop_index(op.f('ix_cmatrix_learner_id'), table_name='cmatrix')
    op.drop_table('cmatrix')
