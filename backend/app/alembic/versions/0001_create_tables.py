"""initial tables"""
from alembic import op
import sqlalchemy as sa

revision = '0001'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'users',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('username', sa.String, unique=True, nullable=False),
        sa.Column('password_hash', sa.String, nullable=False),
        sa.Column('full_name', sa.String, nullable=False),
        sa.Column('role', sa.String, nullable=False, default='user'),
        sa.Column('is_active', sa.Boolean, default=True),
        sa.Column('created_at', sa.DateTime, server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime, server_default=sa.func.now(), onupdate=sa.func.now()),
    )
    op.create_table(
        'patients',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('patient_code', sa.String, unique=True, nullable=False),
        sa.Column('first_name', sa.String, nullable=False),
        sa.Column('last_name', sa.String, nullable=False),
        sa.Column('date_of_birth', sa.Date),
        sa.Column('gender', sa.String),
        sa.Column('phone', sa.String),
        sa.Column('email', sa.String),
        sa.Column('address', sa.String),
        sa.Column('medical_history', sa.Text),
        sa.Column('allergies', sa.Text),
        sa.Column('is_active', sa.Boolean, default=True),
        sa.Column('created_at', sa.DateTime, server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime, server_default=sa.func.now(), onupdate=sa.func.now()),
    )
    op.create_table(
        'visits',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('patient_id', sa.Integer, sa.ForeignKey('patients.id')),\
        sa.Column('visit_date', sa.DateTime, server_default=sa.func.now()),
        sa.Column('referring_doctor', sa.String),
        sa.Column('reason_for_visit', sa.String),
        sa.Column('status', sa.String),
        sa.Column('created_by_user_id', sa.Integer, sa.ForeignKey('users.id')),
        sa.Column('created_at', sa.DateTime, server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime, server_default=sa.func.now(), onupdate=sa.func.now()),
    )
    op.create_table(
        'test_catalog',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('code', sa.String, unique=True, nullable=False),
        sa.Column('name', sa.String, nullable=False),
        sa.Column('sample_type', sa.String),
        sa.Column('reference_range', sa.Text),
        sa.Column('turnaround_time_hours', sa.Integer),
        sa.Column('price', sa.Numeric),
        sa.Column('is_active', sa.Boolean, default=True),
        sa.Column('created_at', sa.DateTime, server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime, server_default=sa.func.now(), onupdate=sa.func.now()),
    )
    op.create_table(
        'test_orders',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('visit_id', sa.Integer, sa.ForeignKey('visits.id')),
        sa.Column('test_catalog_id', sa.Integer, sa.ForeignKey('test_catalog.id')),
        sa.Column('status', sa.String),
        sa.Column('sample_collected_at', sa.DateTime),
        sa.Column('created_at', sa.DateTime, server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime, server_default=sa.func.now(), onupdate=sa.func.now()),
    )
    op.create_table(
        'test_results',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('test_order_id', sa.Integer, sa.ForeignKey('test_orders.id'), unique=True),
        sa.Column('result_value', sa.Text),
        sa.Column('units', sa.String),
        sa.Column('reference_range', sa.Text),
        sa.Column('comment', sa.Text),
        sa.Column('status', sa.String),
        sa.Column('finalized_by_user_id', sa.Integer, sa.ForeignKey('users.id')),
        sa.Column('finalized_at', sa.DateTime),
        sa.Column('created_at', sa.DateTime, server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime, server_default=sa.func.now(), onupdate=sa.func.now()),
    )
    op.create_table(
        'billing_records',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('visit_id', sa.Integer, sa.ForeignKey('visits.id'), unique=True),
        sa.Column('subtotal_amount', sa.Numeric),
        sa.Column('discount_amount', sa.Numeric),
        sa.Column('total_amount', sa.Numeric),
        sa.Column('amount_paid', sa.Numeric),
        sa.Column('balance_amount', sa.Numeric),
        sa.Column('payment_mode', sa.String),
        sa.Column('status', sa.String),
        sa.Column('created_at', sa.DateTime, server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime, server_default=sa.func.now(), onupdate=sa.func.now()),
    )
    op.create_table(
        'imaging_studies',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('patient_id', sa.Integer, sa.ForeignKey('patients.id')),
        sa.Column('study_uid', sa.String, unique=True),
        sa.Column('modality', sa.String),
        sa.Column('study_date', sa.Date),
        sa.Column('description', sa.Text),
        sa.Column('dicom_file_path', sa.Text),
        sa.Column('source_device', sa.Text),
        sa.Column('created_at', sa.DateTime, server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime, server_default=sa.func.now(), onupdate=sa.func.now()),
    )
    op.create_table(
        'audit_logs',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('user_id', sa.Integer, sa.ForeignKey('users.id')),
        sa.Column('action', sa.String, nullable=False),
        sa.Column('entity_type', sa.String),
        sa.Column('entity_id', sa.Integer),
        sa.Column('details', sa.Text),
        sa.Column('created_at', sa.DateTime, server_default=sa.func.now()),
    )


def downgrade():
    op.drop_table('audit_logs')
    op.drop_table('imaging_studies')
    op.drop_table('billing_records')
    op.drop_table('test_results')
    op.drop_table('test_orders')
    op.drop_table('test_catalog')
    op.drop_table('visits')
    op.drop_table('patients')
    op.drop_table('users')
