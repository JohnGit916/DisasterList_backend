"""Clean up: timestamp and status already exist on ResponderIncident

Revision ID: 39213e89a985
Revises: 636692e2df43
Create Date: 2025-06-28 21:58:01.210089
"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '39213e89a985'
down_revision = '636692e2df43'
branch_labels = None
depends_on = None


def upgrade():
    # Ensure values are set for existing records
    op.execute("""
        UPDATE responder_incidents
        SET timestamp = NOW()
        WHERE timestamp IS NULL;
    """)

    op.execute("""
        UPDATE responder_incidents
        SET status = 'Pending'
        WHERE status IS NULL;
    """)


def downgrade():
    # No rollback needed for data update
    pass
