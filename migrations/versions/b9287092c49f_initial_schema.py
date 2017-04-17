"""initial schema

Revision ID: b9287092c49f
Revises:
Create Date: 2017-04-14 13:28:17.740909

"""

from alembic import op
import sqlalchemy as sa

from sqlalchemy.schema import Sequence, CreateSequence

# revision identifiers, used by Alembic.
revision = 'b9287092c49f'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('content_ecosystems',
    sa.Column('id', sa.Integer(), primary_key=True, nullable=False),
    sa.Column('title', sa.String(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.Column('comments', sa.Text(), nullable=True),
    )
    op.create_index(op.f('ix_content_ecosystems_created_at'), 'content_ecosystems', ['created_at'], unique=False)
    op.create_index(op.f('ix_content_ecosystems_title'), 'content_ecosystems', ['title'], unique=False)

    
    op.create_table('delayed_jobs',
    sa.Column('id', sa.Integer(), primary_key=True, nullable=False),
    sa.Column('priority', sa.Integer(), server_default=sa.text('0'), nullable=False),
    sa.Column('attempts', sa.Integer(), server_default=sa.text('0'), nullable=False),
    sa.Column('handler', sa.Text(), nullable=False),
    sa.Column('last_error', sa.Text(), nullable=True),
    sa.Column('run_at', sa.DateTime(), nullable=True),
    sa.Column('locked_at', sa.DateTime(), nullable=True),
    sa.Column('failed_at', sa.DateTime(), nullable=True),
    sa.Column('locked_by', sa.String(), nullable=True),
    sa.Column('queue', sa.String(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    )
    op.create_index('delayed_jobs_priority', 'delayed_jobs', ['priority', 'run_at'], unique=False)
    
    op.create_table('entity_roles',
    sa.Column('id', sa.Integer(), primary_key=True, nullable=False),
    sa.Column('role_type', sa.Integer(), server_default=sa.text('0'), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.Column('research_identifier', sa.String(), nullable=True),
    sa.UniqueConstraint('research_identifier')
    )
    op.create_index(op.f('ix_entity_roles_role_type'), 'entity_roles', ['role_type'], unique=False)
    
    op.create_table('fine_print_contracts',
    sa.Column('id', sa.Integer(), primary_key=True, nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('version', sa.Integer(), nullable=True),
    sa.Column('title', sa.String(), nullable=False),
    sa.Column('content', sa.Text(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    )
    op.create_index('index_fine_print_contracts_on_name_and_version', 'fine_print_contracts', ['name', 'version'], unique=True)
    
    op.create_table('fine_print_signatures',
    sa.Column('id', sa.Integer(), primary_key=True, nullable=False),
    sa.Column('contract_id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('user_type', sa.String(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.Column('is_implicit', sa.Boolean(), server_default=sa.text('false'), nullable=False),
    )
    op.create_index('index_fine_print_signatures_on_u_id_and_u_type_and_c_id', 'fine_print_signatures', ['user_id', 'user_type', 'contract_id'], unique=True)
    op.create_index(op.f('ix_fine_print_signatures_contract_id'), 'fine_print_signatures', ['contract_id'], unique=False)
    
    op.create_table('legal_targeted_contract_relationships',
    sa.Column('id', sa.Integer(), primary_key=True, nullable=False),
    sa.Column('child_gid', sa.String(), nullable=False),
    sa.Column('parent_gid', sa.String(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    )
    op.create_index(op.f('ix_legal_targeted_contract_relationships_parent_gid'), 'legal_targeted_contract_relationships', ['parent_gid'], unique=False)
    op.create_index('legal_targeted_contracts_rship_child_parent', 'legal_targeted_contract_relationships', ['child_gid', 'parent_gid'], unique=True)
    
    op.create_table('legal_targeted_contracts',
    sa.Column('id', sa.Integer(), primary_key=True, nullable=False),
    sa.Column('target_gid', sa.String(), nullable=False),
    sa.Column('target_name', sa.String(), nullable=False),
    sa.Column('contract_name', sa.String(), nullable=False),
    sa.Column('is_proxy_signed', sa.Boolean(), server_default=sa.text('false'), nullable=True),
    sa.Column('is_end_user_visible', sa.Boolean(), server_default=sa.text('true'), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.Column('masked_contract_names', sa.Text(), server_default=sa.text("'[]'::text"), nullable=False),
    )
    op.create_index(op.f('ix_legal_targeted_contracts_target_gid'), 'legal_targeted_contracts', ['target_gid'], unique=False)
    
    op.create_table('oauth_access_grants',
    sa.Column('id', sa.Integer(), primary_key=True, nullable=False),
    sa.Column('resource_owner_id', sa.Integer(), nullable=False),
    sa.Column('application_id', sa.Integer(), nullable=False),
    sa.Column('token', sa.String(), nullable=False),
    sa.Column('expires_in', sa.Integer(), nullable=False),
    sa.Column('redirect_uri', sa.Text(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('revoked_at', sa.DateTime(), nullable=True),
    sa.Column('scopes', sa.String(), nullable=True),
    sa.UniqueConstraint('token')
    )
    
    op.create_table('oauth_access_tokens',
    sa.Column('id', sa.Integer(), primary_key=True, nullable=False),
    sa.Column('resource_owner_id', sa.Integer(), nullable=True),
    sa.Column('application_id', sa.Integer(), nullable=True),
    sa.Column('token', sa.String(), nullable=False),
    sa.Column('refresh_token', sa.String(), nullable=True),
    sa.Column('expires_in', sa.Integer(), nullable=True),
    sa.Column('revoked_at', sa.DateTime(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('scopes', sa.String(), nullable=True),
    sa.UniqueConstraint('refresh_token'),
    sa.UniqueConstraint('token')
    )
    op.create_index(op.f('ix_oauth_access_tokens_resource_owner_id'), 'oauth_access_tokens', ['resource_owner_id'], unique=False)
    
    op.create_table('oauth_applications',
    sa.Column('id', sa.Integer(), primary_key=True, nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('uid', sa.String(), nullable=False),
    sa.Column('secret', sa.String(), nullable=False),
    sa.Column('redirect_uri', sa.Text(), nullable=False),
    sa.Column('scopes', sa.String(), server_default=sa.text("''::character varying"), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.UniqueConstraint('uid')
    )
    
    op.create_table('openstax_accounts_accounts',
    sa.Column('id', sa.Integer(), primary_key=True, nullable=False),
    sa.Column('openstax_uid', sa.Integer(), nullable=True),
    sa.Column('username', sa.String(), nullable=True),
    sa.Column('access_token', sa.String(), nullable=True),
    sa.Column('first_name', sa.String(), nullable=True),
    sa.Column('last_name', sa.String(), nullable=True),
    sa.Column('full_name', sa.String(), nullable=True),
    sa.Column('title', sa.String(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.Column('faculty_status', sa.Integer(), server_default=sa.text('0'), nullable=False),
    sa.Column('salesforce_contact_id', sa.String(), nullable=True),
    sa.UniqueConstraint('access_token'),
    sa.UniqueConstraint('openstax_uid'),
    sa.UniqueConstraint('username')
    )
    op.create_index(op.f('ix_openstax_accounts_accounts_faculty_status'), 'openstax_accounts_accounts', ['faculty_status'], unique=False)
    op.create_index(op.f('ix_openstax_accounts_accounts_first_name'), 'openstax_accounts_accounts', ['first_name'], unique=False)
    op.create_index(op.f('ix_openstax_accounts_accounts_full_name'), 'openstax_accounts_accounts', ['full_name'], unique=False)
    op.create_index(op.f('ix_openstax_accounts_accounts_last_name'), 'openstax_accounts_accounts', ['last_name'], unique=False)
    op.create_index(op.f('ix_openstax_accounts_accounts_salesforce_contact_id'), 'openstax_accounts_accounts', ['salesforce_contact_id'], unique=False)
    
    op.create_table('openstax_accounts_group_members',
    sa.Column('id', sa.Integer(), primary_key=True, nullable=False),
    sa.Column('group_id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    )
    op.create_index('index_openstax_accounts_group_members_on_group_id_and_user_id', 'openstax_accounts_group_members', ['group_id', 'user_id'], unique=True)
    op.create_index(op.f('ix_openstax_accounts_group_members_user_id'), 'openstax_accounts_group_members', ['user_id'], unique=False)
    
    op.create_table('openstax_accounts_group_nestings',
    sa.Column('id', sa.Integer(), primary_key=True, nullable=False),
    sa.Column('member_group_id', sa.Integer(), nullable=False),
    sa.Column('container_group_id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.UniqueConstraint('member_group_id')
    )
    op.create_index(op.f('ix_openstax_accounts_group_nestings_container_group_id'), 'openstax_accounts_group_nestings', ['container_group_id'], unique=False)
    
    op.create_table('openstax_accounts_group_owners',
    sa.Column('id', sa.Integer(), primary_key=True, nullable=False),
    sa.Column('group_id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    )
    op.create_index('index_openstax_accounts_group_owners_on_group_id_and_user_id', 'openstax_accounts_group_owners', ['group_id', 'user_id'], unique=True)
    op.create_index(op.f('ix_openstax_accounts_group_owners_user_id'), 'openstax_accounts_group_owners', ['user_id'], unique=False)
    
    op.create_table('openstax_accounts_groups',
    sa.Column('id', sa.Integer(), primary_key=True, nullable=False),
    sa.Column('openstax_uid', sa.Integer(), nullable=False),
    sa.Column('is_public', sa.Boolean(), server_default=sa.text('false'), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('cached_subtree_group_ids', sa.Text(), nullable=True),
    sa.Column('cached_supertree_group_ids', sa.Text(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.UniqueConstraint('openstax_uid')
    )
    
    op.create_table('salesforce_attached_records',
    sa.Column('id', sa.Integer(), primary_key=True, nullable=False),
    sa.Column('tutor_gid', sa.String(), nullable=False),
    sa.Column('salesforce_class_name', sa.String(), nullable=False),
    sa.Column('salesforce_id', sa.String(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.Column('deleted_at', sa.DateTime(), nullable=True),
    )
    op.create_index(op.f('ix_salesforce_attached_records_deleted_at'), 'salesforce_attached_records', ['deleted_at'], unique=False)
    op.create_index(op.f('ix_salesforce_attached_records_tutor_gid'), 'salesforce_attached_records', ['tutor_gid'], unique=False)
    op.create_index('salesforce_attached_record_tutor_gid', 'salesforce_attached_records', ['salesforce_id', 'salesforce_class_name', 'tutor_gid'], unique=True)
    
    op.create_table('salesforce_users',
    sa.Column('id', sa.Integer(), primary_key=True, nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('uid', sa.String(), nullable=False),
    sa.Column('oauth_token', sa.String(), nullable=False),
    sa.Column('refresh_token', sa.String(), nullable=False),
    sa.Column('instance_url', sa.String(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    )
    op.create_table('schema_migrations',
    sa.Column('version', sa.String(), nullable=False),
    sa.UniqueConstraint('version')
    )
    
    op.create_table('school_district_districts',
    sa.Column('id', sa.Integer(), primary_key=True, nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.UniqueConstraint('name')
    )
    
    op.create_table('settings',
    sa.Column('id', sa.Integer(), primary_key=True, nullable=False),
    sa.Column('var', sa.String(), nullable=False),
    sa.Column('value', sa.Text(), nullable=True),
    sa.Column('thing_id', sa.Integer(), nullable=True),
    sa.Column('thing_type', sa.String(length=30), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    )
    op.create_index('index_settings_on_thing_type_and_thing_id_and_var', 'settings', ['thing_type', 'thing_id', 'var'], unique=True)
    
    op.create_table('short_code_short_codes',
    sa.Column('id', sa.Integer(), primary_key=True, nullable=False),
    sa.Column('code', sa.String(), nullable=False),
    sa.Column('uri', sa.Text(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.UniqueConstraint('code')
    )
    
    op.create_table('tasks_assistants',
    sa.Column('id', sa.Integer(), primary_key=True, nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('code_class_name', sa.String(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.UniqueConstraint('code_class_name'),
    sa.UniqueConstraint('name')
    )
    
    op.create_table('tasks_tasked_external_urls',
    sa.Column('id', sa.Integer(), primary_key=True, nullable=False),
    sa.Column('url', sa.String(), nullable=False),
    sa.Column('title', sa.String(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.Column('deleted_at', sa.DateTime(), nullable=True),
    )
    op.create_index(op.f('ix_tasks_tasked_external_urls_deleted_at'), 'tasks_tasked_external_urls', ['deleted_at'], unique=False)
    
    op.create_table('tasks_tasked_interactives',
    sa.Column('id', sa.Integer(), primary_key=True, nullable=False),
    sa.Column('url', sa.String(), nullable=False),
    sa.Column('content', sa.Text(), nullable=False),
    sa.Column('title', sa.String(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.Column('deleted_at', sa.DateTime(), nullable=True),
    )
    op.create_index(op.f('ix_tasks_tasked_interactives_deleted_at'), 'tasks_tasked_interactives', ['deleted_at'], unique=False)
    
    op.create_table('tasks_tasked_placeholders',
    sa.Column('id', sa.Integer(), primary_key=True, nullable=False),
    sa.Column('placeholder_type', sa.Integer(), server_default=sa.text('0'), nullable=False),
    sa.Column('deleted_at', sa.DateTime(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    )
    op.create_index(op.f('ix_tasks_tasked_placeholders_deleted_at'), 'tasks_tasked_placeholders', ['deleted_at'], unique=False)
    
    op.create_table('tasks_tasked_readings',
    sa.Column('id', sa.Integer(), primary_key=True, nullable=False),
    sa.Column('url', sa.String(), nullable=False),
    sa.Column('content', sa.Text(), nullable=False),
    sa.Column('title', sa.String(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.Column('deleted_at', sa.DateTime(), nullable=True),
    sa.Column('book_location', sa.Text(), server_default=sa.text("'[]'::text"), nullable=False),
    )
    op.create_index(op.f('ix_tasks_tasked_readings_deleted_at'), 'tasks_tasked_readings', ['deleted_at'], unique=False)
    
    op.create_table('tasks_tasked_videos',
    sa.Column('id', sa.Integer(), primary_key=True, nullable=False),
    sa.Column('url', sa.String(), nullable=False),
    sa.Column('content', sa.Text(), nullable=False),
    sa.Column('title', sa.String(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.Column('deleted_at', sa.DateTime(), nullable=True),
    )
    op.create_index(op.f('ix_tasks_tasked_videos_deleted_at'), 'tasks_tasked_videos', ['deleted_at'], unique=False)
    
    op.create_table('time_zones',
    sa.Column('id', sa.Integer(), primary_key=True, nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    )
    op.create_index(op.f('ix_time_zones_name'), 'time_zones', ['name'], unique=False)
    
    op.create_table('user_tours',
    sa.Column('id', sa.Integer(), primary_key=True, nullable=False),
    sa.Column('identifier', sa.Text(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.UniqueConstraint('identifier')
    )
    
    op.create_table('catalog_offerings',
    sa.Column('id', sa.Integer(), primary_key=True, nullable=False),
    sa.Column('salesforce_book_name', sa.String(), nullable=False),
    sa.Column('content_ecosystem_id', sa.Integer(), nullable=True),
    sa.Column('is_tutor', sa.Boolean(), server_default=sa.text('false'), nullable=False),
    sa.Column('is_concept_coach', sa.Boolean(), server_default=sa.text('false'), nullable=False),
    sa.Column('description', sa.String(), nullable=False),
    sa.Column('webview_url', sa.String(), nullable=False),
    sa.Column('pdf_url', sa.String(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.Column('default_course_name', sa.String(), nullable=True),
    sa.Column('appearance_code', sa.String(), nullable=True),
    sa.Column('is_available', sa.Boolean(), nullable=False),
    sa.Column('title', sa.String(), nullable=False),
    sa.Column('number', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['content_ecosystem_id'], ['content_ecosystems.id'], onupdate='CASCADE', ondelete='SET NULL'),
    sa.UniqueConstraint('number'),
    sa.UniqueConstraint('salesforce_book_name')
    )
    op.create_index(op.f('ix_catalog_offerings_content_ecosystem_id'), 'catalog_offerings', ['content_ecosystem_id'], unique=False)
    op.create_index(op.f('ix_catalog_offerings_title'), 'catalog_offerings', ['title'], unique=False)
    
    op.create_table('content_books',
    sa.Column('id', sa.Integer(), primary_key=True, nullable=False),
    sa.Column('url', sa.String(), nullable=False),
    sa.Column('content', sa.Text(), nullable=True),
    sa.Column('content_ecosystem_id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(), nullable=False),
    sa.Column('uuid', sa.String(), nullable=False),
    sa.Column('version', sa.String(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.Column('short_id', sa.String(), nullable=True),
    sa.Column('reading_processing_instructions', sa.Text(), server_default=sa.text("'[]'::text"), nullable=False),
    sa.ForeignKeyConstraint(['content_ecosystem_id'], ['content_ecosystems.id'], onupdate='CASCADE', ondelete='CASCADE'),
    )
    op.create_index(op.f('ix_content_books_content_ecosystem_id'), 'content_books', ['content_ecosystem_id'], unique=False)
    op.create_index(op.f('ix_content_books_title'), 'content_books', ['title'], unique=False)
    op.create_index(op.f('ix_content_books_url'), 'content_books', ['url'], unique=False)
    
    op.create_table('content_maps',
    sa.Column('id', sa.Integer(), primary_key=True, nullable=False),
    sa.Column('content_from_ecosystem_id', sa.Integer(), nullable=False),
    sa.Column('content_to_ecosystem_id', sa.Integer(), nullable=False),
    sa.Column('is_valid', sa.Boolean(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.Column('exercise_id_to_page_id_map', sa.Text(), server_default=sa.text("'{}'::text"), nullable=False),
    sa.Column('page_id_to_page_id_map', sa.Text(), server_default=sa.text("'{}'::text"), nullable=False),
    sa.Column('page_id_to_pool_type_exercise_ids_map', sa.Text(), server_default=sa.text("'{}'::text"), nullable=False),
    sa.Column('validity_error_messages', sa.Text(), server_default=sa.text("'[]'::text"), nullable=False),
    sa.ForeignKeyConstraint(['content_from_ecosystem_id'], ['content_ecosystems.id'], onupdate='CASCADE', ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['content_to_ecosystem_id'], ['content_ecosystems.id'], onupdate='CASCADE', ondelete='CASCADE'),
    )
    op.create_index('index_content_maps_on_from_ecosystem_id_and_to_ecosystem_id', 'content_maps', ['content_from_ecosystem_id', 'content_to_ecosystem_id'], unique=True)
    op.create_index(op.f('ix_content_maps_content_to_ecosystem_id'), 'content_maps', ['content_to_ecosystem_id'], unique=False)
    
    op.create_table('content_pools',
    sa.Column('id', sa.Integer(), primary_key=True, nullable=False),
    sa.Column('content_ecosystem_id', sa.Integer(), nullable=False),
    sa.Column('uuid', sa.String(), nullable=False),
    sa.Column('pool_type', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.Column('content_exercise_ids', sa.Text(), server_default=sa.text("'[]'::text"), nullable=False),
    sa.ForeignKeyConstraint(['content_ecosystem_id'], ['content_ecosystems.id'], onupdate='CASCADE', ondelete='CASCADE'),
    sa.UniqueConstraint('uuid')
    )
    op.create_index(op.f('ix_content_pools_content_ecosystem_id'), 'content_pools', ['content_ecosystem_id'], unique=False)
    op.create_index(op.f('ix_content_pools_pool_type'), 'content_pools', ['pool_type'], unique=False)
    
    op.create_table('content_tags',
    sa.Column('id', sa.Integer(), primary_key=True, nullable=False),
    sa.Column('content_ecosystem_id', sa.Integer(), nullable=False),
    sa.Column('value', sa.String(), nullable=False),
    sa.Column('tag_type', sa.Integer(), server_default=sa.text('0'), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('data', sa.String(), nullable=True),
    sa.Column('visible', sa.Boolean(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['content_ecosystem_id'], ['content_ecosystems.id'], onupdate='CASCADE', ondelete='CASCADE'),
    )
    op.create_index('index_content_tags_on_value_and_content_ecosystem_id', 'content_tags', ['value', 'content_ecosystem_id'], unique=True)
    op.create_index(op.f('ix_content_tags_content_ecosystem_id'), 'content_tags', ['content_ecosystem_id'], unique=False)
    op.create_index(op.f('ix_content_tags_tag_type'), 'content_tags', ['tag_type'], unique=False)
    
    op.create_table('school_district_schools',
    sa.Column('id', sa.Integer(), primary_key=True, nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('school_district_district_id', sa.Integer(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['school_district_district_id'], ['school_district_districts.id'], onupdate='CASCADE', ondelete='SET NULL'),
    sa.UniqueConstraint('name')
    )
    op.create_index('index_schools_on_name_and_district_id', 'school_district_schools', ['name', 'school_district_district_id'], unique=True)
    op.create_index(op.f('ix_school_district_schools_school_district_district_id'), 'school_district_schools', ['school_district_district_id'], unique=False)
    
    op.create_table('tasks_task_plans',
    sa.Column('id', sa.Integer(), primary_key=True, nullable=False),
    sa.Column('tasks_assistant_id', sa.Integer(), nullable=False),
    sa.Column('owner_id', sa.Integer(), nullable=False),
    sa.Column('owner_type', sa.String(), nullable=False),
    sa.Column('type', sa.String(), nullable=False),
    sa.Column('title', sa.String(), nullable=False),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('settings', sa.Text(), nullable=False),
    sa.Column('publish_last_requested_at', sa.DateTime(), nullable=True),
    sa.Column('first_published_at', sa.DateTime(), nullable=True),
    sa.Column('publish_job_uuid', sa.String(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.Column('content_ecosystem_id', sa.Integer(), nullable=False),
    sa.Column('is_feedback_immediate', sa.Boolean(), server_default=sa.text('true'), nullable=False),
    sa.Column('deleted_at', sa.DateTime(), nullable=True),
    sa.Column('last_published_at', sa.DateTime(), nullable=True),
    sa.Column('cloned_from_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['cloned_from_id'], ['tasks_task_plans.id'], onupdate='CASCADE', ondelete='SET NULL'),
    sa.ForeignKeyConstraint(['content_ecosystem_id'], ['content_ecosystems.id'], onupdate='CASCADE', ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['tasks_assistant_id'], ['tasks_assistants.id'], onupdate='CASCADE', ondelete='CASCADE'),
    )
    op.create_index('index_tasks_task_plans_on_owner_id_and_owner_type', 'tasks_task_plans', ['owner_id', 'owner_type'], unique=False)
    op.create_index(op.f('ix_tasks_task_plans_cloned_from_id'), 'tasks_task_plans', ['cloned_from_id'], unique=False)
    op.create_index(op.f('ix_tasks_task_plans_content_ecosystem_id'), 'tasks_task_plans', ['content_ecosystem_id'], unique=False)
    op.create_index(op.f('ix_tasks_task_plans_deleted_at'), 'tasks_task_plans', ['deleted_at'], unique=False)
    op.create_index(op.f('ix_tasks_task_plans_tasks_assistant_id'), 'tasks_task_plans', ['tasks_assistant_id'], unique=False)
    
    op.create_table('user_profiles',
    sa.Column('id', sa.Integer(), primary_key=True, nullable=False),
    sa.Column('account_id', sa.Integer(), nullable=False),
    sa.Column('exchange_read_identifier', sa.String(), nullable=False),
    sa.Column('exchange_write_identifier', sa.String(), nullable=False),
    sa.Column('deleted_at', sa.DateTime(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.Column('ui_settings', sa.Text(), nullable=True),
    sa.ForeignKeyConstraint(['account_id'], ['openstax_accounts_accounts.id'], onupdate='CASCADE', ondelete='CASCADE'),
    sa.UniqueConstraint('account_id'),
    sa.UniqueConstraint('exchange_read_identifier'),
    sa.UniqueConstraint('exchange_write_identifier')
    )
    op.create_index(op.f('ix_user_profiles_deleted_at'), 'user_profiles', ['deleted_at'], unique=False)
    
    op.create_table('content_chapters',
    sa.Column('id', sa.Integer(), primary_key=True, nullable=False),
    sa.Column('content_book_id', sa.Integer(), nullable=False),
    sa.Column('number', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.Column('content_all_exercises_pool_id', sa.Integer(), nullable=True),
    sa.Column('book_location', sa.Text(), server_default=sa.text("'[]'::text"), nullable=False),
    sa.ForeignKeyConstraint(['content_all_exercises_pool_id'], ['content_pools.id'], onupdate='CASCADE', ondelete='SET NULL'),
    sa.ForeignKeyConstraint(['content_book_id'], ['content_books.id'], onupdate='CASCADE', ondelete='CASCADE'),
    
    )
    op.create_index('index_content_chapters_on_content_book_id_and_number', 'content_chapters', ['content_book_id', 'number'], unique=True)
    op.create_index(op.f('ix_content_chapters_title'), 'content_chapters', ['title'], unique=False)
    
    op.create_table('content_lo_teks_tags',
    sa.Column('id', sa.Integer(), primary_key=True, nullable=False),
    sa.Column('lo_id', sa.Integer(), nullable=False),
    sa.Column('teks_id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['lo_id'], ['content_tags.id'], onupdate='CASCADE', ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['teks_id'], ['content_tags.id'], onupdate='CASCADE', ondelete='CASCADE'),
    )
    op.create_index('content_lo_teks_tag_lo_teks_uniq', 'content_lo_teks_tags', ['lo_id', 'teks_id'], unique=True)
    
    op.create_table('course_profile_courses',
    sa.Column('id', sa.Integer(), primary_key=True, nullable=False),
    sa.Column('school_district_school_id', sa.Integer(), nullable=True),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.Column('is_concept_coach', sa.Boolean(), nullable=False),
    sa.Column('teach_token', sa.String(), nullable=False),
    sa.Column('catalog_offering_id', sa.Integer(), nullable=True),
    sa.Column('appearance_code', sa.String(), nullable=True),
    sa.Column('biglearn_excluded_pool_uuid', sa.String(), nullable=True),
    sa.Column('default_open_time', sa.String(), nullable=True),
    sa.Column('default_due_time', sa.String(), nullable=True),
    sa.Column('time_zone_id', sa.Integer(), nullable=False),
    sa.Column('is_college', sa.Boolean(), server_default=sa.text('false'), nullable=False),
    sa.Column('starts_at', sa.DateTime(), nullable=False),
    sa.Column('ends_at', sa.DateTime(), nullable=False),
    sa.Column('term', sa.Integer(), nullable=False),
    sa.Column('year', sa.Integer(), nullable=False),
    sa.Column('cloned_from_id', sa.Integer(), nullable=True),
    sa.Column('is_trial', sa.Boolean(), nullable=False),
    sa.Column('is_excluded_from_salesforce', sa.Boolean(), server_default=sa.text('false'), nullable=False),
    sa.ForeignKeyConstraint(['catalog_offering_id'], ['catalog_offerings.id'], onupdate='CASCADE', ondelete='SET NULL'),
    sa.ForeignKeyConstraint(['cloned_from_id'], ['course_profile_courses.id'], onupdate='CASCADE', ondelete='SET NULL'),
    sa.ForeignKeyConstraint(['school_district_school_id'], ['school_district_schools.id'], onupdate='CASCADE', ondelete='SET NULL'),
    sa.ForeignKeyConstraint(['time_zone_id'], ['time_zones.id'], onupdate='CASCADE', ondelete='SET NULL'),
    sa.UniqueConstraint('teach_token'),
    sa.UniqueConstraint('time_zone_id')
    )
    op.create_index('index_course_profile_courses_on_year_and_term', 'course_profile_courses', ['year', 'term'], unique=False)
    op.create_index(op.f('ix_course_profile_courses_catalog_offering_id'), 'course_profile_courses', ['catalog_offering_id'], unique=False)
    op.create_index(op.f('ix_course_profile_courses_cloned_from_id'), 'course_profile_courses', ['cloned_from_id'], unique=False)
    op.create_index(op.f('ix_course_profile_courses_name'), 'course_profile_courses', ['name'], unique=False)
    op.create_index(op.f('ix_course_profile_courses_school_district_school_id'), 'course_profile_courses', ['school_district_school_id'], unique=False)
    
    op.create_table('role_role_users',
    sa.Column('id', sa.Integer(), primary_key=True, nullable=False),
    sa.Column('user_profile_id', sa.Integer(), nullable=False),
    sa.Column('entity_role_id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['entity_role_id'], ['entity_roles.id'], onupdate='CASCADE', ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user_profile_id'], ['user_profiles.id'], onupdate='CASCADE', ondelete='CASCADE'),
    )
    op.create_index('role_role_users_user_role_uniq', 'role_role_users', ['user_profile_id', 'entity_role_id'], unique=True)
    
    op.create_table('tasks_tasking_plans',
    sa.Column('id', sa.Integer(), primary_key=True, nullable=False),
    sa.Column('target_id', sa.Integer(), nullable=False),
    sa.Column('target_type', sa.String(), nullable=False),
    sa.Column('tasks_task_plan_id', sa.Integer(), nullable=False),
    sa.Column('opens_at_ntz', sa.DateTime(), nullable=False),
    sa.Column('due_at_ntz', sa.DateTime(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.Column('time_zone_id', sa.Integer(), nullable=False),
    sa.Column('deleted_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['tasks_task_plan_id'], ['tasks_task_plans.id'], onupdate='CASCADE', ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['time_zone_id'], ['time_zones.id'], onupdate='CASCADE', ondelete='SET NULL'),
    )
    op.create_index('index_tasking_plans_on_t_id_and_t_type_and_t_p_id', 'tasks_tasking_plans', ['target_id', 'target_type', 'tasks_task_plan_id'], unique=True)
    op.create_index('index_tasks_tasking_plans_on_due_at_ntz_and_opens_at_ntz', 'tasks_tasking_plans', ['due_at_ntz', 'opens_at_ntz'], unique=False)
    op.create_index(op.f('ix_tasks_tasking_plans_deleted_at'), 'tasks_tasking_plans', ['deleted_at'], unique=False)
    op.create_index(op.f('ix_tasks_tasking_plans_opens_at_ntz'), 'tasks_tasking_plans', ['opens_at_ntz'], unique=False)
    op.create_index(op.f('ix_tasks_tasking_plans_tasks_task_plan_id'), 'tasks_tasking_plans', ['tasks_task_plan_id'], unique=False)
    op.create_index(op.f('ix_tasks_tasking_plans_time_zone_id'), 'tasks_tasking_plans', ['time_zone_id'], unique=False)
    
    op.create_table('tasks_tasks',
    sa.Column('id', sa.Integer(), primary_key=True, nullable=False),
    sa.Column('tasks_task_plan_id', sa.Integer(), nullable=True),
    sa.Column('task_type', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(), nullable=False),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('opens_at_ntz', sa.DateTime(), nullable=True),
    sa.Column('due_at_ntz', sa.DateTime(), nullable=True),
    sa.Column('feedback_at_ntz', sa.DateTime(), nullable=True),
    sa.Column('last_worked_at', sa.DateTime(), nullable=True),
    sa.Column('tasks_taskings_count', sa.Integer(), server_default=sa.text('0'), nullable=False),
    sa.Column('personalized_placeholder_strategy', sa.Text(), nullable=True),
    sa.Column('steps_count', sa.Integer(), server_default=sa.text('0'), nullable=False),
    sa.Column('completed_steps_count', sa.Integer(), server_default=sa.text('0'), nullable=False),
    sa.Column('core_steps_count', sa.Integer(), server_default=sa.text('0'), nullable=False),
    sa.Column('completed_core_steps_count', sa.Integer(), server_default=sa.text('0'), nullable=False),
    sa.Column('exercise_steps_count', sa.Integer(), server_default=sa.text('0'), nullable=False),
    sa.Column('completed_exercise_steps_count', sa.Integer(), server_default=sa.text('0'), nullable=False),
    sa.Column('recovered_exercise_steps_count', sa.Integer(), server_default=sa.text('0'), nullable=False),
    sa.Column('correct_exercise_steps_count', sa.Integer(), server_default=sa.text('0'), nullable=False),
    sa.Column('placeholder_steps_count', sa.Integer(), server_default=sa.text('0'), nullable=False),
    sa.Column('placeholder_exercise_steps_count', sa.Integer(), server_default=sa.text('0'), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.Column('correct_on_time_exercise_steps_count', sa.Integer(), server_default=sa.text('0'), nullable=False),
    sa.Column('completed_on_time_exercise_steps_count', sa.Integer(), server_default=sa.text('0'), nullable=False),
    sa.Column('completed_on_time_steps_count', sa.Integer(), server_default=sa.text('0'), nullable=False),
    sa.Column('accepted_late_at', sa.DateTime(), nullable=True),
    sa.Column('correct_accepted_late_exercise_steps_count', sa.Integer(), server_default=sa.text('0'), nullable=False),
    sa.Column('completed_accepted_late_exercise_steps_count', sa.Integer(), server_default=sa.text('0'), nullable=False),
    sa.Column('completed_accepted_late_steps_count', sa.Integer(), server_default=sa.text('0'), nullable=False),
    sa.Column('time_zone_id', sa.Integer(), nullable=True),
    sa.Column('deleted_at', sa.DateTime(), nullable=True),
    sa.Column('hidden_at', sa.DateTime(), nullable=True),
    sa.Column('spy', sa.Text(), server_default=sa.text("'{}'::text"), nullable=False),
    sa.ForeignKeyConstraint(['tasks_task_plan_id'], ['tasks_task_plans.id'], onupdate='CASCADE', ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['time_zone_id'], ['time_zones.id'], onupdate='CASCADE', ondelete='SET NULL'),
    )
    op.create_index('index_tasks_tasks_on_due_at_ntz_and_opens_at_ntz', 'tasks_tasks', ['due_at_ntz', 'opens_at_ntz'], unique=False)
    op.create_index(op.f('ix_tasks_tasks_deleted_at'), 'tasks_tasks', ['deleted_at'], unique=False)
    op.create_index(op.f('ix_tasks_tasks_hidden_at'), 'tasks_tasks', ['hidden_at'], unique=False)
    op.create_index(op.f('ix_tasks_tasks_last_worked_at'), 'tasks_tasks', ['last_worked_at'], unique=False)
    op.create_index(op.f('ix_tasks_tasks_opens_at_ntz'), 'tasks_tasks', ['opens_at_ntz'], unique=False)
    op.create_index(op.f('ix_tasks_tasks_task_type'), 'tasks_tasks', ['task_type'], unique=False)
    op.create_index(op.f('ix_tasks_tasks_tasks_task_plan_id'), 'tasks_tasks', ['tasks_task_plan_id'], unique=False)
    op.create_index(op.f('ix_tasks_tasks_time_zone_id'), 'tasks_tasks', ['time_zone_id'], unique=False)
    
    op.create_table('user_administrators',
    sa.Column('id', sa.Integer(), primary_key=True, nullable=False),
    sa.Column('user_profile_id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['user_profile_id'], ['user_profiles.id'], onupdate='CASCADE', ondelete='CASCADE'),
    sa.UniqueConstraint('user_profile_id')
    )
    
    op.create_table('user_content_analysts',
    sa.Column('id', sa.Integer(), primary_key=True, nullable=False),
    sa.Column('user_profile_id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['user_profile_id'], ['user_profiles.id'], onupdate='CASCADE', ondelete='CASCADE'),
    sa.UniqueConstraint('user_profile_id')
    )
    
    op.create_table('user_customer_services',
    sa.Column('id', sa.Integer(), primary_key=True, nullable=False),
    sa.Column('user_profile_id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['user_profile_id'], ['user_profiles.id'], onupdate='CASCADE', ondelete='CASCADE'),
    sa.UniqueConstraint('user_profile_id')
    )
    
    op.create_table('user_tour_views',
    sa.Column('id', sa.Integer(), primary_key=True, nullable=False),
    sa.Column('view_count', sa.Integer(), server_default=sa.text('0'), nullable=False),
    sa.Column('user_profile_id', sa.Integer(), nullable=False),
    sa.Column('user_tour_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['user_profile_id'], ['user_profiles.id'], ),
    sa.ForeignKeyConstraint(['user_tour_id'], ['user_tours.id'], ),
    )
    op.create_index('index_user_tour_views_on_user_profile_id_and_user_tour_id', 'user_tour_views', ['user_profile_id', 'user_tour_id'], unique=True)
    op.create_index(op.f('ix_user_tour_views_user_tour_id'), 'user_tour_views', ['user_tour_id'], unique=False)
    
    op.create_table('content_pages',
    sa.Column('id', sa.Integer(), primary_key=True, nullable=False),
    sa.Column('url', sa.String(), nullable=False),
    sa.Column('content', sa.Text(), nullable=True),
    sa.Column('content_chapter_id', sa.Integer(), nullable=False),
    sa.Column('content_reading_dynamic_pool_id', sa.Integer(), nullable=True),
    sa.Column('content_reading_context_pool_id', sa.Integer(), nullable=True),
    sa.Column('content_homework_core_pool_id', sa.Integer(), nullable=True),
    sa.Column('content_homework_dynamic_pool_id', sa.Integer(), nullable=True),
    sa.Column('content_practice_widget_pool_id', sa.Integer(), nullable=True),
    sa.Column('number', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(), nullable=False),
    sa.Column('uuid', sa.String(), nullable=False),
    sa.Column('version', sa.String(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.Column('content_all_exercises_pool_id', sa.Integer(), nullable=True),
    sa.Column('content_concept_coach_pool_id', sa.Integer(), nullable=True),
    sa.Column('short_id', sa.String(), nullable=True),
    sa.Column('book_location', sa.Text(), server_default=sa.text("'[]'::text"), nullable=False),
    sa.Column('fragments', sa.Text(), server_default=sa.text("'[]'::text"), nullable=False),
    sa.Column('snap_labs', sa.Text(), server_default=sa.text("'[]'::text"), nullable=False),
    sa.ForeignKeyConstraint(['content_all_exercises_pool_id'], ['content_pools.id'], onupdate='CASCADE', ondelete='SET NULL'),
    sa.ForeignKeyConstraint(['content_chapter_id'], ['content_chapters.id'], onupdate='CASCADE', ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['content_homework_core_pool_id'], ['content_pools.id'], onupdate='CASCADE', ondelete='SET NULL'),
    sa.ForeignKeyConstraint(['content_homework_dynamic_pool_id'], ['content_pools.id'], onupdate='CASCADE', ondelete='SET NULL'),
    sa.ForeignKeyConstraint(['content_practice_widget_pool_id'], ['content_pools.id'], onupdate='CASCADE', ondelete='SET NULL'),
    sa.ForeignKeyConstraint(['content_reading_context_pool_id'], ['content_pools.id'], onupdate='CASCADE', ondelete='SET NULL'),
    sa.ForeignKeyConstraint(['content_reading_dynamic_pool_id'], ['content_pools.id'], onupdate='CASCADE', ondelete='SET NULL'),
    )
    op.create_index('index_content_pages_on_content_chapter_id_and_number', 'content_pages', ['content_chapter_id', 'number'], unique=True)
    op.create_index(op.f('ix_content_pages_title'), 'content_pages', ['title'], unique=False)
    op.create_index(op.f('ix_content_pages_url'), 'content_pages', ['url'], unique=False)
    
    op.create_table('course_content_course_ecosystems',
    sa.Column('id', sa.Integer(), primary_key=True, nullable=False),
    sa.Column('course_profile_course_id', sa.Integer(), nullable=False),
    sa.Column('content_ecosystem_id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['content_ecosystem_id'], ['content_ecosystems.id'], onupdate='CASCADE', ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['course_profile_course_id'], ['course_profile_courses.id'], onupdate='CASCADE', ondelete='CASCADE'),
    )
    op.create_index('course_ecosystems_on_course_id_created_at', 'course_content_course_ecosystems', ['course_profile_course_id', 'created_at'], unique=False)
    op.create_index('course_ecosystems_on_ecosystem_id_course_id', 'course_content_course_ecosystems', ['content_ecosystem_id', 'course_profile_course_id'], unique=False)
    
    op.create_table('course_content_excluded_exercises',
    sa.Column('id', sa.Integer(), primary_key=True, nullable=False),
    sa.Column('course_profile_course_id', sa.Integer(), nullable=False),
    sa.Column('exercise_number', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['course_profile_course_id'], ['course_profile_courses.id'], onupdate='CASCADE', ondelete='CASCADE'),
    )
    op.create_index('index_excluded_exercises_on_number_and_course_id', 'course_content_excluded_exercises', ['exercise_number', 'course_profile_course_id'], unique=True)
    op.create_index(op.f('ix_course_content_excluded_exercises_course_profile_course_id'), 'course_content_excluded_exercises', ['course_profile_course_id'], unique=False)
    
    op.create_table('course_membership_periods',
    sa.Column('id', sa.Integer(), primary_key=True, nullable=False),
    sa.Column('course_profile_course_id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.Column('enrollment_code', sa.String(), nullable=False),
    sa.Column('deleted_at', sa.DateTime(), nullable=True),
    sa.Column('default_open_time', sa.String(), nullable=True),
    sa.Column('default_due_time', sa.String(), nullable=True),
    sa.Column('entity_teacher_student_role_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['course_profile_course_id'], ['course_profile_courses.id'], onupdate='CASCADE', ondelete='CASCADE'),
    sa.UniqueConstraint('enrollment_code'),
    sa.UniqueConstraint('entity_teacher_student_role_id')
    )
    op.create_index('index_c_m_periods_on_name_and_c_p_course_id', 'course_membership_periods', ['name', 'course_profile_course_id'], unique=False)
    op.create_index(op.f('ix_course_membership_periods_course_profile_course_id'), 'course_membership_periods', ['course_profile_course_id'], unique=False)
    op.create_index(op.f('ix_course_membership_periods_deleted_at'), 'course_membership_periods', ['deleted_at'], unique=False)
    
    op.create_table('course_membership_students',
    sa.Column('id', sa.Integer(), primary_key=True, nullable=False),
    sa.Column('course_profile_course_id', sa.Integer(), nullable=False),
    sa.Column('entity_role_id', sa.Integer(), nullable=False),
    sa.Column('deleted_at', sa.DateTime(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.Column('student_identifier', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['course_profile_course_id'], ['course_profile_courses.id'], onupdate='CASCADE', ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['entity_role_id'], ['entity_roles.id'], onupdate='CASCADE', ondelete='CASCADE'),
    sa.UniqueConstraint('entity_role_id')
    )
    op.create_index('index_course_membership_students_on_c_p_c_id_and_s_identifier', 'course_membership_students', ['course_profile_course_id', 'student_identifier'], unique=False)
    op.create_index(op.f('ix_course_membership_students_deleted_at'), 'course_membership_students', ['deleted_at'], unique=False)
    
    op.create_table('course_membership_teachers',
    sa.Column('id', sa.Integer(), primary_key=True, nullable=False),
    sa.Column('course_profile_course_id', sa.Integer(), nullable=False),
    sa.Column('entity_role_id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['course_profile_course_id'], ['course_profile_courses.id'], onupdate='CASCADE', ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['entity_role_id'], ['entity_roles.id'], onupdate='CASCADE', ondelete='CASCADE'),
    sa.UniqueConstraint('entity_role_id')
    )
    op.create_index(op.f('ix_course_membership_teachers_course_profile_course_id'), 'course_membership_teachers', ['course_profile_course_id'], unique=False)
    
    op.create_table('tasks_course_assistants',
    sa.Column('id', sa.Integer(), primary_key=True, nullable=False),
    sa.Column('course_profile_course_id', sa.Integer(), nullable=False),
    sa.Column('tasks_assistant_id', sa.Integer(), nullable=False),
    sa.Column('tasks_task_plan_type', sa.String(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.Column('settings', sa.Text(), server_default=sa.text("'{}'::text"), nullable=False),
    sa.Column('data', sa.Text(), server_default=sa.text("'{}'::text"), nullable=False),
    sa.ForeignKeyConstraint(['course_profile_course_id'], ['course_profile_courses.id'], onupdate='CASCADE', ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['tasks_assistant_id'], ['tasks_assistants.id'], onupdate='CASCADE', ondelete='CASCADE'),
    )
    op.create_index('index_tasks_course_assistants_on_assistant_id_and_course_id', 'tasks_course_assistants', ['tasks_assistant_id', 'course_profile_course_id'], unique=False)
    op.create_index('index_tasks_course_assistants_on_course_id_and_task_plan_type', 'tasks_course_assistants', ['course_profile_course_id', 'tasks_task_plan_type'], unique=True)
    
    op.create_table('tasks_performance_report_exports',
    sa.Column('id', sa.Integer(), primary_key=True, nullable=False),
    sa.Column('course_profile_course_id', sa.Integer(), nullable=False),
    sa.Column('entity_role_id', sa.Integer(), nullable=False),
    sa.Column('export', sa.String(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['course_profile_course_id'], ['course_profile_courses.id'], onupdate='CASCADE', ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['entity_role_id'], ['entity_roles.id'], onupdate='CASCADE', ondelete='CASCADE'),
    )
    op.create_index('index_performance_report_exports_on_role_and_course', 'tasks_performance_report_exports', ['entity_role_id', 'course_profile_course_id'], unique=False)
    op.create_index(op.f('ix_tasks_performance_report_exports_course_profile_course_id'), 'tasks_performance_report_exports', ['course_profile_course_id'], unique=False)
    
    op.create_table('tasks_task_steps',
    sa.Column('id', sa.Integer(), primary_key=True, nullable=False),
    sa.Column('tasks_task_id', sa.Integer(), nullable=False),
    sa.Column('tasked_id', sa.Integer(), nullable=False),
    sa.Column('tasked_type', sa.String(), nullable=False),
    sa.Column('number', sa.Integer(), nullable=False),
    sa.Column('first_completed_at', sa.DateTime(), nullable=True),
    sa.Column('last_completed_at', sa.DateTime(), nullable=True),
    sa.Column('group_type', sa.Integer(), server_default=sa.text('0'), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.Column('deleted_at', sa.DateTime(), nullable=True),
    sa.Column('related_content', sa.Text(), server_default=sa.text("'[]'::text"), nullable=False),
    sa.Column('related_exercise_ids', sa.Text(), server_default=sa.text("'[]'::text"), nullable=False),
    sa.Column('labels', sa.Text(), server_default=sa.text("'[]'::text"), nullable=False),
    sa.ForeignKeyConstraint(['tasks_task_id'], ['tasks_tasks.id'], onupdate='CASCADE', ondelete='CASCADE'),
    )
    op.create_index('index_tasks_task_steps_on_tasked_id_and_tasked_type', 'tasks_task_steps', ['tasked_id', 'tasked_type'], unique=True)
    op.create_index('index_tasks_task_steps_on_tasks_task_id_and_number', 'tasks_task_steps', ['tasks_task_id', 'number'], unique=True)
    op.create_index(op.f('ix_tasks_task_steps_deleted_at'), 'tasks_task_steps', ['deleted_at'], unique=False)
    
    op.create_table('content_exercises',
    sa.Column('id', sa.Integer(), primary_key=True, nullable=False),
    sa.Column('url', sa.String(), nullable=False),
    sa.Column('content', sa.Text(), nullable=True),
    sa.Column('content_page_id', sa.Integer(), nullable=False),
    sa.Column('number', sa.Integer(), nullable=False),
    sa.Column('version', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.Column('preview', sa.Text(), nullable=True),
    sa.Column('context', sa.Text(), nullable=True),
    sa.Column('has_interactive', sa.Boolean(), server_default=sa.text('false'), nullable=False),
    sa.Column('has_video', sa.Boolean(), server_default=sa.text('false'), nullable=False),
    sa.ForeignKeyConstraint(['content_page_id'], ['content_pages.id'], onupdate='CASCADE', ondelete='CASCADE'),
    )
    op.create_index('index_content_exercises_on_number_and_version', 'content_exercises', ['number', 'version'], unique=False)
    op.create_index(op.f('ix_content_exercises_content_page_id'), 'content_exercises', ['content_page_id'], unique=False)
    op.create_index(op.f('ix_content_exercises_title'), 'content_exercises', ['title'], unique=False)
    op.create_index(op.f('ix_content_exercises_url'), 'content_exercises', ['url'], unique=False)
    
    op.create_table('content_page_tags',
    sa.Column('id', sa.Integer(), primary_key=True, nullable=False),
    sa.Column('content_page_id', sa.Integer(), nullable=False),
    sa.Column('content_tag_id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['content_page_id'], ['content_pages.id'], onupdate='CASCADE', ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['content_tag_id'], ['content_tags.id'], onupdate='CASCADE', ondelete='CASCADE'),
    )
    op.create_index('index_content_page_tags_on_content_page_id_and_content_tag_id', 'content_page_tags', ['content_page_id', 'content_tag_id'], unique=True)
    op.create_index(op.f('ix_content_page_tags_content_tag_id'), 'content_page_tags', ['content_tag_id'], unique=False)
    
    op.create_table('course_membership_enrollments',
    sa.Column('id', sa.Integer(), primary_key=True, nullable=False),
    sa.Column('course_membership_period_id', sa.Integer(), nullable=False),
    sa.Column('course_membership_student_id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.Column('deleted_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['course_membership_period_id'], ['course_membership_periods.id'], onupdate='CASCADE', ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['course_membership_student_id'], ['course_membership_students.id'], onupdate='CASCADE', ondelete='CASCADE'),
    )
    op.create_index('course_membership_enrollments_period_student', 'course_membership_enrollments', ['course_membership_period_id', 'course_membership_student_id'], unique=False)
    op.create_index('course_membership_enrollments_student_created_at_uniq', 'course_membership_enrollments', ['course_membership_student_id', 'created_at'], unique=True)
    op.create_index(op.f('ix_course_membership_enrollments_deleted_at'), 'course_membership_enrollments', ['deleted_at'], unique=False)
    
    op.create_table('tasks_concept_coach_tasks',
    sa.Column('id', sa.Integer(), primary_key=True, nullable=False),
    sa.Column('content_page_id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.Column('entity_role_id', sa.Integer(), nullable=False),
    sa.Column('deleted_at', sa.DateTime(), nullable=True),
    sa.Column('tasks_task_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['content_page_id'], ['content_pages.id'], onupdate='CASCADE', ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['entity_role_id'], ['entity_roles.id'], onupdate='CASCADE', ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['tasks_task_id'], ['tasks_tasks.id'], ),
    sa.UniqueConstraint('tasks_task_id')
    )
    op.create_index('index_tasks_concept_coach_tasks_on_e_r_id_and_c_p_id', 'tasks_concept_coach_tasks', ['entity_role_id', 'content_page_id'], unique=True)
    op.create_index(op.f('ix_tasks_concept_coach_tasks_content_page_id'), 'tasks_concept_coach_tasks', ['content_page_id'], unique=False)
    op.create_index(op.f('ix_tasks_concept_coach_tasks_deleted_at'), 'tasks_concept_coach_tasks', ['deleted_at'], unique=False)
    
    op.create_table('tasks_taskings',
    sa.Column('id', sa.Integer(), primary_key=True, nullable=False),
    sa.Column('entity_role_id', sa.Integer(), nullable=False),
    sa.Column('course_membership_period_id', sa.Integer(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.Column('deleted_at', sa.DateTime(), nullable=True),
    sa.Column('tasks_task_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['course_membership_period_id'], ['course_membership_periods.id'], onupdate='CASCADE', ondelete='SET NULL'),
    sa.ForeignKeyConstraint(['entity_role_id'], ['entity_roles.id'], onupdate='CASCADE', ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['tasks_task_id'], ['tasks_tasks.id'], ),
    )
    op.create_index('index_tasks_taskings_on_tasks_task_id_and_entity_role_id', 'tasks_taskings', ['tasks_task_id', 'entity_role_id'], unique=True)
    op.create_index(op.f('ix_tasks_taskings_course_membership_period_id'), 'tasks_taskings', ['course_membership_period_id'], unique=False)
    op.create_index(op.f('ix_tasks_taskings_deleted_at'), 'tasks_taskings', ['deleted_at'], unique=False)
    op.create_index(op.f('ix_tasks_taskings_entity_role_id'), 'tasks_taskings', ['entity_role_id'], unique=False)
    
    op.create_table('content_exercise_tags',
    sa.Column('id', sa.Integer(), primary_key=True, nullable=False),
    sa.Column('content_exercise_id', sa.Integer(), nullable=False),
    sa.Column('content_tag_id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['content_exercise_id'], ['content_exercises.id'], onupdate='CASCADE', ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['content_tag_id'], ['content_tags.id'], onupdate='CASCADE', ondelete='CASCADE'),
    )
    op.create_index('index_content_exercise_tags_on_c_e_id_and_c_t_id', 'content_exercise_tags', ['content_exercise_id', 'content_tag_id'], unique=True)
    op.create_index(op.f('ix_content_exercise_tags_content_tag_id'), 'content_exercise_tags', ['content_tag_id'], unique=False)
    
    op.create_table('course_membership_enrollment_changes',
    sa.Column('id', sa.Integer(), primary_key=True, nullable=False),
    sa.Column('user_profile_id', sa.Integer(), nullable=False),
    sa.Column('course_membership_enrollment_id', sa.Integer(), nullable=True),
    sa.Column('course_membership_period_id', sa.Integer(), nullable=False),
    sa.Column('status', sa.Integer(), server_default=sa.text('0'), nullable=False),
    sa.Column('requires_enrollee_approval', sa.Boolean(), server_default=sa.text('true'), nullable=False),
    sa.Column('enrollee_approved_at', sa.DateTime(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.Column('deleted_at', sa.DateTime(), nullable=True),
    sa.Column('course_membership_conflicting_enrollment_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['course_membership_enrollment_id'], ['course_membership_enrollments.id'], onupdate='CASCADE', ondelete='SET NULL'),
    sa.ForeignKeyConstraint(['course_membership_period_id'], ['course_membership_periods.id'], onupdate='CASCADE', ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user_profile_id'], ['user_profiles.id'], onupdate='CASCADE', ondelete='CASCADE'),
    )
    op.create_index(op.f('ix_course_membership_enrollment_changes_course_membership_conflicting_enrollment_id'), 'course_membership_enrollment_changes', ['course_membership_conflicting_enrollment_id'], unique=False)
    op.create_index(op.f('ix_course_membership_enrollment_changes_course_membership_enrollment_id'), 'course_membership_enrollment_changes', ['course_membership_enrollment_id'], unique=False)
    op.create_index(op.f('ix_course_membership_enrollment_changes_course_membership_period_id'), 'course_membership_enrollment_changes', ['course_membership_period_id'], unique=False)
    op.create_index(op.f('ix_course_membership_enrollment_changes_deleted_at'), 'course_membership_enrollment_changes', ['deleted_at'], unique=False)
    op.create_index(op.f('ix_course_membership_enrollment_changes_user_profile_id'), 'course_membership_enrollment_changes', ['user_profile_id'], unique=False)
    
    op.create_table('tasks_tasked_exercises',
    sa.Column('id', sa.Integer(), primary_key=True, nullable=False),
    sa.Column('content_exercise_id', sa.Integer(), nullable=False),
    sa.Column('url', sa.String(), nullable=False),
    sa.Column('content', sa.Text(), nullable=False),
    sa.Column('title', sa.String(), nullable=True),
    sa.Column('free_response', sa.Text(), nullable=True),
    sa.Column('answer_id', sa.String(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.Column('correct_answer_id', sa.String(), nullable=False),
    sa.Column('is_in_multipart', sa.Boolean(), server_default=sa.text('false'), nullable=False),
    sa.Column('question_id', sa.String(), nullable=False),
    sa.Column('deleted_at', sa.DateTime(), nullable=True),
    sa.Column('context', sa.Text(), nullable=True),
    sa.ForeignKeyConstraint(['content_exercise_id'], ['content_exercises.id'], onupdate='CASCADE', ondelete='CASCADE'),
    )
    op.create_index(op.f('ix_tasks_tasked_exercises_content_exercise_id'), 'tasks_tasked_exercises', ['content_exercise_id'], unique=False)
    op.create_index(op.f('ix_tasks_tasked_exercises_deleted_at'), 'tasks_tasked_exercises', ['deleted_at'], unique=False)
    op.create_index(op.f('ix_tasks_tasked_exercises_question_id'), 'tasks_tasked_exercises', ['question_id'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_tasks_tasked_exercises_question_id'), table_name='tasks_tasked_exercises')
    op.drop_index(op.f('ix_tasks_tasked_exercises_deleted_at'), table_name='tasks_tasked_exercises')
    op.drop_index(op.f('ix_tasks_tasked_exercises_content_exercise_id'), table_name='tasks_tasked_exercises')
    op.drop_table('tasks_tasked_exercises')
    op.drop_index(op.f('ix_course_membership_enrollment_changes_user_profile_id'), table_name='course_membership_enrollment_changes')
    op.drop_index(op.f('ix_course_membership_enrollment_changes_deleted_at'), table_name='course_membership_enrollment_changes')
    op.drop_index(op.f('ix_course_membership_enrollment_changes_course_membership_period_id'), table_name='course_membership_enrollment_changes')
    op.drop_index(op.f('ix_course_membership_enrollment_changes_course_membership_enrollment_id'), table_name='course_membership_enrollment_changes')
    op.drop_index(op.f('ix_course_membership_enrollment_changes_course_membership_conflicting_enrollment_id'), table_name='course_membership_enrollment_changes')
    op.drop_table('course_membership_enrollment_changes')
    op.drop_index(op.f('ix_content_exercise_tags_content_tag_id'), table_name='content_exercise_tags')
    op.drop_index('index_content_exercise_tags_on_c_e_id_and_c_t_id', table_name='content_exercise_tags')
    op.drop_table('content_exercise_tags')
    op.drop_index(op.f('ix_tasks_taskings_entity_role_id'), table_name='tasks_taskings')
    op.drop_index(op.f('ix_tasks_taskings_deleted_at'), table_name='tasks_taskings')
    op.drop_index(op.f('ix_tasks_taskings_course_membership_period_id'), table_name='tasks_taskings')
    op.drop_index('index_tasks_taskings_on_tasks_task_id_and_entity_role_id', table_name='tasks_taskings')
    op.drop_table('tasks_taskings')
    op.drop_index(op.f('ix_tasks_concept_coach_tasks_deleted_at'), table_name='tasks_concept_coach_tasks')
    op.drop_index(op.f('ix_tasks_concept_coach_tasks_content_page_id'), table_name='tasks_concept_coach_tasks')
    op.drop_index('index_tasks_concept_coach_tasks_on_e_r_id_and_c_p_id', table_name='tasks_concept_coach_tasks')
    op.drop_table('tasks_concept_coach_tasks')
    op.drop_index(op.f('ix_course_membership_enrollments_deleted_at'), table_name='course_membership_enrollments')
    op.drop_index('course_membership_enrollments_student_created_at_uniq', table_name='course_membership_enrollments')
    op.drop_index('course_membership_enrollments_period_student', table_name='course_membership_enrollments')
    op.drop_table('course_membership_enrollments')
    op.drop_index(op.f('ix_content_page_tags_content_tag_id'), table_name='content_page_tags')
    op.drop_index('index_content_page_tags_on_content_page_id_and_content_tag_id', table_name='content_page_tags')
    op.drop_table('content_page_tags')
    op.drop_index(op.f('ix_content_exercises_url'), table_name='content_exercises')
    op.drop_index(op.f('ix_content_exercises_title'), table_name='content_exercises')
    op.drop_index(op.f('ix_content_exercises_content_page_id'), table_name='content_exercises')
    op.drop_index('index_content_exercises_on_number_and_version', table_name='content_exercises')
    op.drop_table('content_exercises')
    op.drop_index(op.f('ix_tasks_task_steps_deleted_at'), table_name='tasks_task_steps')
    op.drop_index('index_tasks_task_steps_on_tasks_task_id_and_number', table_name='tasks_task_steps')
    op.drop_index('index_tasks_task_steps_on_tasked_id_and_tasked_type', table_name='tasks_task_steps')
    op.drop_table('tasks_task_steps')
    op.drop_index(op.f('ix_tasks_performance_report_exports_course_profile_course_id'), table_name='tasks_performance_report_exports')
    op.drop_index('index_performance_report_exports_on_role_and_course', table_name='tasks_performance_report_exports')
    op.drop_table('tasks_performance_report_exports')
    op.drop_index('index_tasks_course_assistants_on_course_id_and_task_plan_type', table_name='tasks_course_assistants')
    op.drop_index('index_tasks_course_assistants_on_assistant_id_and_course_id', table_name='tasks_course_assistants')
    op.drop_table('tasks_course_assistants')
    op.drop_index(op.f('ix_course_membership_teachers_course_profile_course_id'), table_name='course_membership_teachers')
    op.drop_table('course_membership_teachers')
    op.drop_index(op.f('ix_course_membership_students_deleted_at'), table_name='course_membership_students')
    op.drop_index('index_course_membership_students_on_c_p_c_id_and_s_identifier', table_name='course_membership_students')
    op.drop_table('course_membership_students')
    op.drop_index(op.f('ix_course_membership_periods_deleted_at'), table_name='course_membership_periods')
    op.drop_index(op.f('ix_course_membership_periods_course_profile_course_id'), table_name='course_membership_periods')
    op.drop_index('index_c_m_periods_on_name_and_c_p_course_id', table_name='course_membership_periods')
    op.drop_table('course_membership_periods')
    op.drop_index(op.f('ix_course_content_excluded_exercises_course_profile_course_id'), table_name='course_content_excluded_exercises')
    op.drop_index('index_excluded_exercises_on_number_and_course_id', table_name='course_content_excluded_exercises')
    op.drop_table('course_content_excluded_exercises')
    op.drop_index('course_ecosystems_on_ecosystem_id_course_id', table_name='course_content_course_ecosystems')
    op.drop_index('course_ecosystems_on_course_id_created_at', table_name='course_content_course_ecosystems')
    op.drop_table('course_content_course_ecosystems')
    op.drop_index(op.f('ix_content_pages_url'), table_name='content_pages')
    op.drop_index(op.f('ix_content_pages_title'), table_name='content_pages')
    op.drop_index('index_content_pages_on_content_chapter_id_and_number', table_name='content_pages')
    op.drop_table('content_pages')
    op.drop_index(op.f('ix_user_tour_views_user_tour_id'), table_name='user_tour_views')
    op.drop_index('index_user_tour_views_on_user_profile_id_and_user_tour_id', table_name='user_tour_views')
    op.drop_table('user_tour_views')
    op.drop_table('user_customer_services')
    op.drop_table('user_content_analysts')
    op.drop_table('user_administrators')
    op.drop_index(op.f('ix_tasks_tasks_time_zone_id'), table_name='tasks_tasks')
    op.drop_index(op.f('ix_tasks_tasks_tasks_task_plan_id'), table_name='tasks_tasks')
    op.drop_index(op.f('ix_tasks_tasks_task_type'), table_name='tasks_tasks')
    op.drop_index(op.f('ix_tasks_tasks_opens_at_ntz'), table_name='tasks_tasks')
    op.drop_index(op.f('ix_tasks_tasks_last_worked_at'), table_name='tasks_tasks')
    op.drop_index(op.f('ix_tasks_tasks_hidden_at'), table_name='tasks_tasks')
    op.drop_index(op.f('ix_tasks_tasks_deleted_at'), table_name='tasks_tasks')
    op.drop_index('index_tasks_tasks_on_due_at_ntz_and_opens_at_ntz', table_name='tasks_tasks')
    op.drop_table('tasks_tasks')
    op.drop_index(op.f('ix_tasks_tasking_plans_time_zone_id'), table_name='tasks_tasking_plans')
    op.drop_index(op.f('ix_tasks_tasking_plans_tasks_task_plan_id'), table_name='tasks_tasking_plans')
    op.drop_index(op.f('ix_tasks_tasking_plans_opens_at_ntz'), table_name='tasks_tasking_plans')
    op.drop_index(op.f('ix_tasks_tasking_plans_deleted_at'), table_name='tasks_tasking_plans')
    op.drop_index('index_tasks_tasking_plans_on_due_at_ntz_and_opens_at_ntz', table_name='tasks_tasking_plans')
    op.drop_index('index_tasking_plans_on_t_id_and_t_type_and_t_p_id', table_name='tasks_tasking_plans')
    op.drop_table('tasks_tasking_plans')
    op.drop_index('role_role_users_user_role_uniq', table_name='role_role_users')
    op.drop_table('role_role_users')
    op.drop_index(op.f('ix_course_profile_courses_school_district_school_id'), table_name='course_profile_courses')
    op.drop_index(op.f('ix_course_profile_courses_name'), table_name='course_profile_courses')
    op.drop_index(op.f('ix_course_profile_courses_cloned_from_id'), table_name='course_profile_courses')
    op.drop_index(op.f('ix_course_profile_courses_catalog_offering_id'), table_name='course_profile_courses')
    op.drop_index('index_course_profile_courses_on_year_and_term', table_name='course_profile_courses')
    op.drop_table('course_profile_courses')
    op.drop_index('content_lo_teks_tag_lo_teks_uniq', table_name='content_lo_teks_tags')
    op.drop_table('content_lo_teks_tags')
    op.drop_index(op.f('ix_content_chapters_title'), table_name='content_chapters')
    op.drop_index('index_content_chapters_on_content_book_id_and_number', table_name='content_chapters')
    op.drop_table('content_chapters')
    op.drop_index(op.f('ix_user_profiles_deleted_at'), table_name='user_profiles')
    op.drop_table('user_profiles')
    op.drop_index(op.f('ix_tasks_task_plans_tasks_assistant_id'), table_name='tasks_task_plans')
    op.drop_index(op.f('ix_tasks_task_plans_deleted_at'), table_name='tasks_task_plans')
    op.drop_index(op.f('ix_tasks_task_plans_content_ecosystem_id'), table_name='tasks_task_plans')
    op.drop_index(op.f('ix_tasks_task_plans_cloned_from_id'), table_name='tasks_task_plans')
    op.drop_index('index_tasks_task_plans_on_owner_id_and_owner_type', table_name='tasks_task_plans')
    op.drop_table('tasks_task_plans')
    op.drop_index(op.f('ix_school_district_schools_school_district_district_id'), table_name='school_district_schools')
    op.drop_index('index_schools_on_name_and_district_id', table_name='school_district_schools')
    op.drop_table('school_district_schools')
    op.drop_index(op.f('ix_content_tags_tag_type'), table_name='content_tags')
    op.drop_index(op.f('ix_content_tags_content_ecosystem_id'), table_name='content_tags')
    op.drop_index('index_content_tags_on_value_and_content_ecosystem_id', table_name='content_tags')
    op.drop_table('content_tags')
    op.drop_index(op.f('ix_content_pools_pool_type'), table_name='content_pools')
    op.drop_index(op.f('ix_content_pools_content_ecosystem_id'), table_name='content_pools')
    op.drop_table('content_pools')
    op.drop_index(op.f('ix_content_maps_content_to_ecosystem_id'), table_name='content_maps')
    op.drop_index('index_content_maps_on_from_ecosystem_id_and_to_ecosystem_id', table_name='content_maps')
    op.drop_table('content_maps')
    op.drop_index(op.f('ix_content_books_url'), table_name='content_books')
    op.drop_index(op.f('ix_content_books_title'), table_name='content_books')
    op.drop_index(op.f('ix_content_books_content_ecosystem_id'), table_name='content_books')
    op.drop_table('content_books')
    op.drop_index(op.f('ix_catalog_offerings_title'), table_name='catalog_offerings')
    op.drop_index(op.f('ix_catalog_offerings_content_ecosystem_id'), table_name='catalog_offerings')
    op.drop_table('catalog_offerings')
    op.drop_table('user_tours')
    op.drop_index(op.f('ix_time_zones_name'), table_name='time_zones')
    op.drop_table('time_zones')
    op.drop_index(op.f('ix_tasks_tasked_videos_deleted_at'), table_name='tasks_tasked_videos')
    op.drop_table('tasks_tasked_videos')
    op.drop_index(op.f('ix_tasks_tasked_readings_deleted_at'), table_name='tasks_tasked_readings')
    op.drop_table('tasks_tasked_readings')
    op.drop_index(op.f('ix_tasks_tasked_placeholders_deleted_at'), table_name='tasks_tasked_placeholders')
    op.drop_table('tasks_tasked_placeholders')
    op.drop_index(op.f('ix_tasks_tasked_interactives_deleted_at'), table_name='tasks_tasked_interactives')
    op.drop_table('tasks_tasked_interactives')
    op.drop_index(op.f('ix_tasks_tasked_external_urls_deleted_at'), table_name='tasks_tasked_external_urls')
    op.drop_table('tasks_tasked_external_urls')
    op.drop_table('tasks_assistants')
    op.drop_table('short_code_short_codes')
    op.drop_index('index_settings_on_thing_type_and_thing_id_and_var', table_name='settings')
    op.drop_table('settings')
    op.drop_table('school_district_districts')
    op.drop_table('schema_migrations')
    op.drop_table('salesforce_users')
    op.drop_index('salesforce_attached_record_tutor_gid', table_name='salesforce_attached_records')
    op.drop_index(op.f('ix_salesforce_attached_records_tutor_gid'), table_name='salesforce_attached_records')
    op.drop_index(op.f('ix_salesforce_attached_records_deleted_at'), table_name='salesforce_attached_records')
    op.drop_table('salesforce_attached_records')
    op.drop_table('openstax_accounts_groups')
    op.drop_index(op.f('ix_openstax_accounts_group_owners_user_id'), table_name='openstax_accounts_group_owners')
    op.drop_index('index_openstax_accounts_group_owners_on_group_id_and_user_id', table_name='openstax_accounts_group_owners')
    op.drop_table('openstax_accounts_group_owners')
    op.drop_index(op.f('ix_openstax_accounts_group_nestings_container_group_id'), table_name='openstax_accounts_group_nestings')
    op.drop_table('openstax_accounts_group_nestings')
    op.drop_index(op.f('ix_openstax_accounts_group_members_user_id'), table_name='openstax_accounts_group_members')
    op.drop_index('index_openstax_accounts_group_members_on_group_id_and_user_id', table_name='openstax_accounts_group_members')
    op.drop_table('openstax_accounts_group_members')
    op.drop_index(op.f('ix_openstax_accounts_accounts_salesforce_contact_id'), table_name='openstax_accounts_accounts')
    op.drop_index(op.f('ix_openstax_accounts_accounts_last_name'), table_name='openstax_accounts_accounts')
    op.drop_index(op.f('ix_openstax_accounts_accounts_full_name'), table_name='openstax_accounts_accounts')
    op.drop_index(op.f('ix_openstax_accounts_accounts_first_name'), table_name='openstax_accounts_accounts')
    op.drop_index(op.f('ix_openstax_accounts_accounts_faculty_status'), table_name='openstax_accounts_accounts')
    op.drop_table('openstax_accounts_accounts')
    op.drop_table('oauth_applications')
    op.drop_index(op.f('ix_oauth_access_tokens_resource_owner_id'), table_name='oauth_access_tokens')
    op.drop_table('oauth_access_tokens')
    op.drop_table('oauth_access_grants')
    op.drop_index(op.f('ix_legal_targeted_contracts_target_gid'), table_name='legal_targeted_contracts')
    op.drop_table('legal_targeted_contracts')
    op.drop_index('legal_targeted_contracts_rship_child_parent', table_name='legal_targeted_contract_relationships')
    op.drop_index(op.f('ix_legal_targeted_contract_relationships_parent_gid'), table_name='legal_targeted_contract_relationships')
    op.drop_table('legal_targeted_contract_relationships')
    op.drop_index(op.f('ix_fine_print_signatures_contract_id'), table_name='fine_print_signatures')
    op.drop_index('index_fine_print_signatures_on_u_id_and_u_type_and_c_id', table_name='fine_print_signatures')
    op.drop_table('fine_print_signatures')
    op.drop_index('index_fine_print_contracts_on_name_and_version', table_name='fine_print_contracts')
    op.drop_table('fine_print_contracts')
    op.drop_index(op.f('ix_entity_roles_role_type'), table_name='entity_roles')
    op.drop_table('entity_roles')
    op.drop_index('delayed_jobs_priority', table_name='delayed_jobs')
    op.drop_table('delayed_jobs')
    op.drop_index(op.f('ix_content_ecosystems_title'), table_name='content_ecosystems')
    op.drop_index(op.f('ix_content_ecosystems_created_at'), table_name='content_ecosystems')
    op.drop_table('content_ecosystems')
