# coding: utf-8
from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Index, Integer, \
    String, Table, Text, text
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class CatalogOffering(Base):
    __tablename__ = 'catalog_offerings'

    id = Column(Integer, primary_key=True, server_default=text(
        "nextval('catalog_offerings_id_seq'::regclass)"))
    salesforce_book_name = Column(String, nullable=False, unique=True)
    content_ecosystem_id = Column(
        ForeignKey('content_ecosystems.id', ondelete='SET NULL',
                   onupdate='CASCADE'), index=True)
    is_tutor = Column(Boolean, nullable=False, server_default=text("false"))
    is_concept_coach = Column(Boolean, nullable=False,
                              server_default=text("false"))
    description = Column(String, nullable=False)
    webview_url = Column(String, nullable=False)
    pdf_url = Column(String, nullable=False)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)
    default_course_name = Column(String)
    appearance_code = Column(String)
    is_available = Column(Boolean, nullable=False)
    title = Column(String, nullable=False, index=True)
    number = Column(Integer, nullable=False, unique=True)

    content_ecosystem = relationship('ContentEcosystem')


class ContentBook(Base):
    __tablename__ = 'content_books'

    id = Column(Integer, primary_key=True, server_default=text(
        "nextval('content_books_id_seq'::regclass)"))
    url = Column(String, nullable=False, index=True)
    content = Column(Text)
    content_ecosystem_id = Column(
        ForeignKey('content_ecosystems.id', ondelete='CASCADE',
                   onupdate='CASCADE'), nullable=False, index=True)
    title = Column(String, nullable=False, index=True)
    uuid = Column(String, nullable=False)
    version = Column(String, nullable=False)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)
    short_id = Column(String)
    reading_processing_instructions = Column(Text, nullable=False,
                                             server_default=text("'[]'::text"))

    content_ecosystem = relationship('ContentEcosystem')


class ContentChapter(Base):
    __tablename__ = 'content_chapters'
    __table_args__ = (
        Index('index_content_chapters_on_content_book_id_and_number',
              'content_book_id', 'number', unique=True),
    )

    id = Column(Integer, primary_key=True, server_default=text(
        "nextval('content_chapters_id_seq'::regclass)"))
    content_book_id = Column(
        ForeignKey('content_books.id', ondelete='CASCADE', onupdate='CASCADE'),
        nullable=False)
    number = Column(Integer, nullable=False)
    title = Column(String, nullable=False, index=True)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)
    content_all_exercises_pool_id = Column(
        ForeignKey('content_pools.id', ondelete='SET NULL', onupdate='CASCADE'))
    book_location = Column(Text, nullable=False,
                           server_default=text("'[]'::text"))

    content_all_exercises_pool = relationship('ContentPool')
    content_book = relationship('ContentBook')


class ContentEcosystem(Base):
    __tablename__ = 'content_ecosystems'

    id = Column(Integer, primary_key=True, server_default=text(
        "nextval('content_ecosystems_id_seq'::regclass)"))
    title = Column(String, nullable=False, index=True)
    created_at = Column(DateTime, nullable=False, index=True)
    updated_at = Column(DateTime, nullable=False)
    comments = Column(Text)


class ContentExerciseTag(Base):
    __tablename__ = 'content_exercise_tags'
    __table_args__ = (
        Index('index_content_exercise_tags_on_c_e_id_and_c_t_id',
              'content_exercise_id', 'content_tag_id', unique=True),
    )

    id = Column(Integer, primary_key=True, server_default=text(
        "nextval('content_exercise_tags_id_seq'::regclass)"))
    content_exercise_id = Column(
        ForeignKey('content_exercises.id', ondelete='CASCADE',
                   onupdate='CASCADE'), nullable=False)
    content_tag_id = Column(
        ForeignKey('content_tags.id', ondelete='CASCADE', onupdate='CASCADE'),
        nullable=False, index=True)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)

    content_exercise = relationship('ContentExercise')
    content_tag = relationship('ContentTag')


class ContentExercise(Base):
    __tablename__ = 'content_exercises'
    __table_args__ = (
        Index('index_content_exercises_on_number_and_version', 'number',
              'version'),
    )

    id = Column(Integer, primary_key=True, server_default=text(
        "nextval('content_exercises_id_seq'::regclass)"))
    url = Column(String, nullable=False, index=True)
    content = Column(Text)
    content_page_id = Column(
        ForeignKey('content_pages.id', ondelete='CASCADE', onupdate='CASCADE'),
        nullable=False, index=True)
    number = Column(Integer, nullable=False)
    version = Column(Integer, nullable=False)
    title = Column(String, index=True)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)
    preview = Column(Text)
    context = Column(Text)
    has_interactive = Column(Boolean, nullable=False,
                             server_default=text("false"))
    has_video = Column(Boolean, nullable=False, server_default=text("false"))

    content_page = relationship('ContentPage')


class ContentLoTeksTag(Base):
    __tablename__ = 'content_lo_teks_tags'
    __table_args__ = (
        Index('content_lo_teks_tag_lo_teks_uniq', 'lo_id', 'teks_id',
              unique=True),
    )

    id = Column(Integer, primary_key=True, server_default=text(
        "nextval('content_lo_teks_tags_id_seq'::regclass)"))
    lo_id = Column(
        ForeignKey('content_tags.id', ondelete='CASCADE', onupdate='CASCADE'),
        nullable=False)
    teks_id = Column(
        ForeignKey('content_tags.id', ondelete='CASCADE', onupdate='CASCADE'),
        nullable=False)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)

    lo = relationship('ContentTag',
                      primaryjoin='ContentLoTeksTag.lo_id == ContentTag.id')
    teks = relationship('ContentTag',
                        primaryjoin='ContentLoTeksTag.teks_id == ContentTag.id')


class ContentMap(Base):
    __tablename__ = 'content_maps'
    __table_args__ = (
        Index('index_content_maps_on_from_ecosystem_id_and_to_ecosystem_id',
              'content_from_ecosystem_id', 'content_to_ecosystem_id',
              unique=True),
    )

    id = Column(Integer, primary_key=True,
                server_default=text("nextval('content_maps_id_seq'::regclass)"))
    content_from_ecosystem_id = Column(
        ForeignKey('content_ecosystems.id', ondelete='CASCADE',
                   onupdate='CASCADE'), nullable=False)
    content_to_ecosystem_id = Column(
        ForeignKey('content_ecosystems.id', ondelete='CASCADE',
                   onupdate='CASCADE'), nullable=False, index=True)
    is_valid = Column(Boolean, nullable=False)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)
    exercise_id_to_page_id_map = Column(Text, nullable=False,
                                        server_default=text("'{}'::text"))
    page_id_to_page_id_map = Column(Text, nullable=False,
                                    server_default=text("'{}'::text"))
    page_id_to_pool_type_exercise_ids_map = Column(Text, nullable=False,
                                                   server_default=text(
                                                       "'{}'::text"))
    validity_error_messages = Column(Text, nullable=False,
                                     server_default=text("'[]'::text"))

    content_from_ecosystem = relationship('ContentEcosystem',
                                          primaryjoin='ContentMap.content_from_ecosystem_id == ContentEcosystem.id')
    content_to_ecosystem = relationship('ContentEcosystem',
                                        primaryjoin='ContentMap.content_to_ecosystem_id == ContentEcosystem.id')


class ContentPageTag(Base):
    __tablename__ = 'content_page_tags'
    __table_args__ = (
        Index('index_content_page_tags_on_content_page_id_and_content_tag_id',
              'content_page_id', 'content_tag_id', unique=True),
    )

    id = Column(Integer, primary_key=True, server_default=text(
        "nextval('content_page_tags_id_seq'::regclass)"))
    content_page_id = Column(
        ForeignKey('content_pages.id', ondelete='CASCADE', onupdate='CASCADE'),
        nullable=False)
    content_tag_id = Column(
        ForeignKey('content_tags.id', ondelete='CASCADE', onupdate='CASCADE'),
        nullable=False, index=True)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)

    content_page = relationship('ContentPage')
    content_tag = relationship('ContentTag')


class ContentPage(Base):
    __tablename__ = 'content_pages'
    __table_args__ = (
        Index('index_content_pages_on_content_chapter_id_and_number',
              'content_chapter_id', 'number', unique=True),
    )

    id = Column(Integer, primary_key=True, server_default=text(
        "nextval('content_pages_id_seq'::regclass)"))
    url = Column(String, nullable=False, index=True)
    content = Column(Text)
    content_chapter_id = Column(
        ForeignKey('content_chapters.id', ondelete='CASCADE',
                   onupdate='CASCADE'), nullable=False)
    content_reading_dynamic_pool_id = Column(
        ForeignKey('content_pools.id', ondelete='SET NULL', onupdate='CASCADE'))
    content_reading_context_pool_id = Column(
        ForeignKey('content_pools.id', ondelete='SET NULL', onupdate='CASCADE'))
    content_homework_core_pool_id = Column(
        ForeignKey('content_pools.id', ondelete='SET NULL', onupdate='CASCADE'))
    content_homework_dynamic_pool_id = Column(
        ForeignKey('content_pools.id', ondelete='SET NULL', onupdate='CASCADE'))
    content_practice_widget_pool_id = Column(
        ForeignKey('content_pools.id', ondelete='SET NULL', onupdate='CASCADE'))
    number = Column(Integer, nullable=False)
    title = Column(String, nullable=False, index=True)
    uuid = Column(String, nullable=False)
    version = Column(String, nullable=False)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)
    content_all_exercises_pool_id = Column(
        ForeignKey('content_pools.id', ondelete='SET NULL', onupdate='CASCADE'))
    content_concept_coach_pool_id = Column(Integer)
    short_id = Column(String)
    book_location = Column(Text, nullable=False,
                           server_default=text("'[]'::text"))
    fragments = Column(Text, nullable=False, server_default=text("'[]'::text"))
    snap_labs = Column(Text, nullable=False, server_default=text("'[]'::text"))

    content_all_exercises_pool = relationship('ContentPool',
                                              primaryjoin='ContentPage.content_all_exercises_pool_id == ContentPool.id')
    content_chapter = relationship('ContentChapter')
    content_homework_core_pool = relationship('ContentPool',
                                              primaryjoin='ContentPage.content_homework_core_pool_id == ContentPool.id')
    content_homework_dynamic_pool = relationship('ContentPool',
                                                 primaryjoin='ContentPage.content_homework_dynamic_pool_id == ContentPool.id')
    content_practice_widget_pool = relationship('ContentPool',
                                                primaryjoin='ContentPage.content_practice_widget_pool_id == ContentPool.id')
    content_reading_context_pool = relationship('ContentPool',
                                                primaryjoin='ContentPage.content_reading_context_pool_id == ContentPool.id')
    content_reading_dynamic_pool = relationship('ContentPool',
                                                primaryjoin='ContentPage.content_reading_dynamic_pool_id == ContentPool.id')


class ContentPool(Base):
    __tablename__ = 'content_pools'

    id = Column(Integer, primary_key=True, server_default=text(
        "nextval('content_pools_id_seq'::regclass)"))
    content_ecosystem_id = Column(
        ForeignKey('content_ecosystems.id', ondelete='CASCADE',
                   onupdate='CASCADE'), nullable=False, index=True)
    uuid = Column(String, nullable=False, unique=True)
    pool_type = Column(Integer, nullable=False, index=True)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)
    content_exercise_ids = Column(Text, nullable=False,
                                  server_default=text("'[]'::text"))

    content_ecosystem = relationship('ContentEcosystem')


class ContentTag(Base):
    __tablename__ = 'content_tags'
    __table_args__ = (
        Index('index_content_tags_on_value_and_content_ecosystem_id', 'value',
              'content_ecosystem_id', unique=True),
    )

    id = Column(Integer, primary_key=True,
                server_default=text("nextval('content_tags_id_seq'::regclass)"))
    content_ecosystem_id = Column(
        ForeignKey('content_ecosystems.id', ondelete='CASCADE',
                   onupdate='CASCADE'), nullable=False, index=True)
    value = Column(String, nullable=False)
    tag_type = Column(Integer, nullable=False, index=True,
                      server_default=text("0"))
    name = Column(String)
    description = Column(Text)
    data = Column(String)
    visible = Column(Boolean)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)

    content_ecosystem = relationship('ContentEcosystem')


class CourseContentCourseEcosystem(Base):
    __tablename__ = 'course_content_course_ecosystems'
    __table_args__ = (
        Index('course_ecosystems_on_course_id_created_at',
              'course_profile_course_id', 'created_at'),
        Index('course_ecosystems_on_ecosystem_id_course_id',
              'content_ecosystem_id', 'course_profile_course_id')
    )

    id = Column(Integer, primary_key=True, server_default=text(
        "nextval('course_content_course_ecosystems_id_seq'::regclass)"))
    course_profile_course_id = Column(
        ForeignKey('course_profile_courses.id', ondelete='CASCADE',
                   onupdate='CASCADE'), nullable=False)
    content_ecosystem_id = Column(
        ForeignKey('content_ecosystems.id', ondelete='CASCADE',
                   onupdate='CASCADE'), nullable=False)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)

    content_ecosystem = relationship('ContentEcosystem')
    course_profile_course = relationship('CourseProfileCourse')


class CourseContentExcludedExercise(Base):
    __tablename__ = 'course_content_excluded_exercises'
    __table_args__ = (
        Index('index_excluded_exercises_on_number_and_course_id',
              'exercise_number', 'course_profile_course_id', unique=True),
    )

    id = Column(Integer, primary_key=True, server_default=text(
        "nextval('course_content_excluded_exercises_id_seq'::regclass)"))
    course_profile_course_id = Column(
        ForeignKey('course_profile_courses.id', ondelete='CASCADE',
                   onupdate='CASCADE'), nullable=False, index=True)
    exercise_number = Column(Integer, nullable=False)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)

    course_profile_course = relationship('CourseProfileCourse')


class CourseMembershipEnrollmentChange(Base):
    __tablename__ = 'course_membership_enrollment_changes'

    id = Column(Integer, primary_key=True, server_default=text(
        "nextval('course_membership_enrollment_changes_id_seq'::regclass)"))
    user_profile_id = Column(
        ForeignKey('user_profiles.id', ondelete='CASCADE', onupdate='CASCADE'),
        nullable=False, index=True)
    course_membership_enrollment_id = Column(
        ForeignKey('course_membership_enrollments.id', ondelete='SET NULL',
                   onupdate='CASCADE'), index=True)
    course_membership_period_id = Column(
        ForeignKey('course_membership_periods.id', ondelete='CASCADE',
                   onupdate='CASCADE'), nullable=False, index=True)
    status = Column(Integer, nullable=False, server_default=text("0"))
    requires_enrollee_approval = Column(Boolean, nullable=False,
                                        server_default=text("true"))
    enrollee_approved_at = Column(DateTime)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)
    deleted_at = Column(DateTime, index=True)
    course_membership_conflicting_enrollment_id = Column(Integer, index=True)

    course_membership_enrollment = relationship('CourseMembershipEnrollment')
    course_membership_period = relationship('CourseMembershipPeriod')
    user_profile = relationship('UserProfile')


class CourseMembershipEnrollment(Base):
    __tablename__ = 'course_membership_enrollments'
    __table_args__ = (
        Index('course_membership_enrollments_period_student',
              'course_membership_period_id', 'course_membership_student_id'),
        Index('course_membership_enrollments_student_created_at_uniq',
              'course_membership_student_id', 'created_at', unique=True)
    )

    id = Column(Integer, primary_key=True, server_default=text(
        "nextval('course_membership_enrollments_id_seq'::regclass)"))
    course_membership_period_id = Column(
        ForeignKey('course_membership_periods.id', ondelete='CASCADE',
                   onupdate='CASCADE'), nullable=False)
    course_membership_student_id = Column(
        ForeignKey('course_membership_students.id', ondelete='CASCADE',
                   onupdate='CASCADE'), nullable=False)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)
    deleted_at = Column(DateTime, index=True)

    course_membership_period = relationship('CourseMembershipPeriod')
    course_membership_student = relationship('CourseMembershipStudent')


class CourseMembershipPeriod(Base):
    __tablename__ = 'course_membership_periods'
    __table_args__ = (
        Index('index_c_m_periods_on_name_and_c_p_course_id', 'name',
              'course_profile_course_id'),
    )

    id = Column(Integer, primary_key=True, server_default=text(
        "nextval('course_membership_periods_id_seq'::regclass)"))
    course_profile_course_id = Column(
        ForeignKey('course_profile_courses.id', ondelete='CASCADE',
                   onupdate='CASCADE'), nullable=False, index=True)
    name = Column(String, nullable=False)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)
    enrollment_code = Column(String, nullable=False, unique=True)
    deleted_at = Column(DateTime, index=True)
    default_open_time = Column(String)
    default_due_time = Column(String)
    entity_teacher_student_role_id = Column(Integer, nullable=False,
                                            unique=True)

    course_profile_course = relationship('CourseProfileCourse')


class CourseMembershipStudent(Base):
    __tablename__ = 'course_membership_students'
    __table_args__ = (
        Index('index_course_membership_students_on_c_p_c_id_and_s_identifier',
              'course_profile_course_id', 'student_identifier'),
    )

    id = Column(Integer, primary_key=True, server_default=text(
        "nextval('course_membership_students_id_seq'::regclass)"))
    course_profile_course_id = Column(
        ForeignKey('course_profile_courses.id', ondelete='CASCADE',
                   onupdate='CASCADE'), nullable=False)
    entity_role_id = Column(
        ForeignKey('entity_roles.id', ondelete='CASCADE', onupdate='CASCADE'),
        nullable=False, unique=True)
    deleted_at = Column(DateTime, index=True)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)
    student_identifier = Column(String)

    course_profile_course = relationship('CourseProfileCourse')
    entity_role = relationship('EntityRole')


class CourseMembershipTeacher(Base):
    __tablename__ = 'course_membership_teachers'

    id = Column(Integer, primary_key=True, server_default=text(
        "nextval('course_membership_teachers_id_seq'::regclass)"))
    course_profile_course_id = Column(
        ForeignKey('course_profile_courses.id', ondelete='CASCADE',
                   onupdate='CASCADE'), nullable=False, index=True)
    entity_role_id = Column(
        ForeignKey('entity_roles.id', ondelete='CASCADE', onupdate='CASCADE'),
        nullable=False, unique=True)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)

    course_profile_course = relationship('CourseProfileCourse')
    entity_role = relationship('EntityRole')


class CourseProfileCourse(Base):
    __tablename__ = 'course_profile_courses'
    __table_args__ = (
        Index('index_course_profile_courses_on_year_and_term', 'year', 'term'),
    )

    id = Column(Integer, primary_key=True, server_default=text(
        "nextval('course_profile_courses_id_seq'::regclass)"))
    school_district_school_id = Column(
        ForeignKey('school_district_schools.id', ondelete='SET NULL',
                   onupdate='CASCADE'), index=True)
    name = Column(String, nullable=False, index=True)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)
    is_concept_coach = Column(Boolean, nullable=False)
    teach_token = Column(String, nullable=False, unique=True)
    catalog_offering_id = Column(
        ForeignKey('catalog_offerings.id', ondelete='SET NULL',
                   onupdate='CASCADE'), index=True)
    appearance_code = Column(String)
    biglearn_excluded_pool_uuid = Column(String)
    default_open_time = Column(String)
    default_due_time = Column(String)
    time_zone_id = Column(
        ForeignKey('time_zones.id', ondelete='SET NULL', onupdate='CASCADE'),
        nullable=False, unique=True)
    is_college = Column(Boolean, nullable=False, server_default=text("false"))
    starts_at = Column(DateTime, nullable=False)
    ends_at = Column(DateTime, nullable=False)
    term = Column(Integer, nullable=False)
    year = Column(Integer, nullable=False)
    cloned_from_id = Column(
        ForeignKey('course_profile_courses.id', ondelete='SET NULL',
                   onupdate='CASCADE'), index=True)
    is_trial = Column(Boolean, nullable=False)
    is_excluded_from_salesforce = Column(Boolean, nullable=False,
                                         server_default=text("false"))

    catalog_offering = relationship('CatalogOffering')
    cloned_from = relationship('CourseProfileCourse', remote_side=[id])
    school_district_school = relationship('SchoolDistrictSchool')
    time_zone = relationship('TimeZone')


class DelayedJob(Base):
    __tablename__ = 'delayed_jobs'
    __table_args__ = (
        Index('delayed_jobs_priority', 'priority', 'run_at'),
    )

    id = Column(Integer, primary_key=True,
                server_default=text("nextval('delayed_jobs_id_seq'::regclass)"))
    priority = Column(Integer, nullable=False, server_default=text("0"))
    attempts = Column(Integer, nullable=False, server_default=text("0"))
    handler = Column(Text, nullable=False)
    last_error = Column(Text)
    run_at = Column(DateTime)
    locked_at = Column(DateTime)
    failed_at = Column(DateTime)
    locked_by = Column(String)
    queue = Column(String)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)


class EntityRole(Base):
    __tablename__ = 'entity_roles'

    id = Column(Integer, primary_key=True,
                server_default=text("nextval('entity_roles_id_seq'::regclass)"))
    role_type = Column(Integer, nullable=False, index=True,
                       server_default=text("0"))
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)
    research_identifier = Column(String, unique=True)


class FinePrintContract(Base):
    __tablename__ = 'fine_print_contracts'
    __table_args__ = (
        Index('index_fine_print_contracts_on_name_and_version', 'name',
              'version', unique=True),
    )

    id = Column(Integer, primary_key=True, server_default=text(
        "nextval('fine_print_contracts_id_seq'::regclass)"))
    name = Column(String, nullable=False)
    version = Column(Integer)
    title = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)


class FinePrintSignature(Base):
    __tablename__ = 'fine_print_signatures'
    __table_args__ = (
        Index('index_fine_print_signatures_on_u_id_and_u_type_and_c_id',
              'user_id', 'user_type', 'contract_id', unique=True),
    )

    id = Column(Integer, primary_key=True, server_default=text(
        "nextval('fine_print_signatures_id_seq'::regclass)"))
    contract_id = Column(Integer, nullable=False, index=True)
    user_id = Column(Integer, nullable=False)
    user_type = Column(String, nullable=False)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)
    is_implicit = Column(Boolean, nullable=False, server_default=text("false"))


class LegalTargetedContractRelationship(Base):
    __tablename__ = 'legal_targeted_contract_relationships'
    __table_args__ = (
        Index('legal_targeted_contracts_rship_child_parent', 'child_gid',
              'parent_gid', unique=True),
    )

    id = Column(Integer, primary_key=True, server_default=text(
        "nextval('legal_targeted_contract_relationships_id_seq'::regclass)"))
    child_gid = Column(String, nullable=False)
    parent_gid = Column(String, nullable=False, index=True)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)


class LegalTargetedContract(Base):
    __tablename__ = 'legal_targeted_contracts'

    id = Column(Integer, primary_key=True, server_default=text(
        "nextval('legal_targeted_contracts_id_seq'::regclass)"))
    target_gid = Column(String, nullable=False, index=True)
    target_name = Column(String, nullable=False)
    contract_name = Column(String, nullable=False)
    is_proxy_signed = Column(Boolean, server_default=text("false"))
    is_end_user_visible = Column(Boolean, server_default=text("true"))
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)
    masked_contract_names = Column(Text, nullable=False,
                                   server_default=text("'[]'::text"))


class OauthAccessGrant(Base):
    __tablename__ = 'oauth_access_grants'

    id = Column(Integer, primary_key=True, server_default=text(
        "nextval('oauth_access_grants_id_seq'::regclass)"))
    resource_owner_id = Column(Integer, nullable=False)
    application_id = Column(Integer, nullable=False)
    token = Column(String, nullable=False, unique=True)
    expires_in = Column(Integer, nullable=False)
    redirect_uri = Column(Text, nullable=False)
    created_at = Column(DateTime, nullable=False)
    revoked_at = Column(DateTime)
    scopes = Column(String)


class OauthAccessToken(Base):
    __tablename__ = 'oauth_access_tokens'

    id = Column(Integer, primary_key=True, server_default=text(
        "nextval('oauth_access_tokens_id_seq'::regclass)"))
    resource_owner_id = Column(Integer, index=True)
    application_id = Column(Integer)
    token = Column(String, nullable=False, unique=True)
    refresh_token = Column(String, unique=True)
    expires_in = Column(Integer)
    revoked_at = Column(DateTime)
    created_at = Column(DateTime, nullable=False)
    scopes = Column(String)


class OauthApplication(Base):
    __tablename__ = 'oauth_applications'

    id = Column(Integer, primary_key=True, server_default=text(
        "nextval('oauth_applications_id_seq'::regclass)"))
    name = Column(String, nullable=False)
    uid = Column(String, nullable=False, unique=True)
    secret = Column(String, nullable=False)
    redirect_uri = Column(Text, nullable=False)
    scopes = Column(String, nullable=False,
                    server_default=text("''::character varying"))
    created_at = Column(DateTime)
    updated_at = Column(DateTime)


class OpenstaxAccountsAccount(Base):
    __tablename__ = 'openstax_accounts_accounts'

    id = Column(Integer, primary_key=True, server_default=text(
        "nextval('openstax_accounts_accounts_id_seq'::regclass)"))
    openstax_uid = Column(Integer, unique=True)
    username = Column(String, unique=True)
    access_token = Column(String, unique=True)
    first_name = Column(String, index=True)
    last_name = Column(String, index=True)
    full_name = Column(String, index=True)
    title = Column(String)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)
    faculty_status = Column(Integer, nullable=False, index=True,
                            server_default=text("0"))
    salesforce_contact_id = Column(String, index=True)


class OpenstaxAccountsGroupMember(Base):
    __tablename__ = 'openstax_accounts_group_members'
    __table_args__ = (
        Index('index_openstax_accounts_group_members_on_group_id_and_user_id',
              'group_id', 'user_id', unique=True),
    )

    id = Column(Integer, primary_key=True, server_default=text(
        "nextval('openstax_accounts_group_members_id_seq'::regclass)"))
    group_id = Column(Integer, nullable=False)
    user_id = Column(Integer, nullable=False, index=True)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)


class OpenstaxAccountsGroupNesting(Base):
    __tablename__ = 'openstax_accounts_group_nestings'

    id = Column(Integer, primary_key=True, server_default=text(
        "nextval('openstax_accounts_group_nestings_id_seq'::regclass)"))
    member_group_id = Column(Integer, nullable=False, unique=True)
    container_group_id = Column(Integer, nullable=False, index=True)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)


class OpenstaxAccountsGroupOwner(Base):
    __tablename__ = 'openstax_accounts_group_owners'
    __table_args__ = (
        Index('index_openstax_accounts_group_owners_on_group_id_and_user_id',
              'group_id', 'user_id', unique=True),
    )

    id = Column(Integer, primary_key=True, server_default=text(
        "nextval('openstax_accounts_group_owners_id_seq'::regclass)"))
    group_id = Column(Integer, nullable=False)
    user_id = Column(Integer, nullable=False, index=True)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)


class OpenstaxAccountsGroup(Base):
    __tablename__ = 'openstax_accounts_groups'

    id = Column(Integer, primary_key=True, server_default=text(
        "nextval('openstax_accounts_groups_id_seq'::regclass)"))
    openstax_uid = Column(Integer, nullable=False, unique=True)
    is_public = Column(Boolean, nullable=False, server_default=text("false"))
    name = Column(String)
    cached_subtree_group_ids = Column(Text)
    cached_supertree_group_ids = Column(Text)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)


class RoleRoleUser(Base):
    __tablename__ = 'role_role_users'
    __table_args__ = (
        Index('role_role_users_user_role_uniq', 'user_profile_id',
              'entity_role_id', unique=True),
    )

    id = Column(Integer, primary_key=True, server_default=text(
        "nextval('role_role_users_id_seq'::regclass)"))
    user_profile_id = Column(
        ForeignKey('user_profiles.id', ondelete='CASCADE', onupdate='CASCADE'),
        nullable=False)
    entity_role_id = Column(
        ForeignKey('entity_roles.id', ondelete='CASCADE', onupdate='CASCADE'),
        nullable=False)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)

    entity_role = relationship('EntityRole')
    user_profile = relationship('UserProfile')


class SalesforceAttachedRecord(Base):
    __tablename__ = 'salesforce_attached_records'
    __table_args__ = (
        Index('salesforce_attached_record_tutor_gid', 'salesforce_id',
              'salesforce_class_name', 'tutor_gid', unique=True),
    )

    id = Column(Integer, primary_key=True, server_default=text(
        "nextval('salesforce_attached_records_id_seq'::regclass)"))
    tutor_gid = Column(String, nullable=False, index=True)
    salesforce_class_name = Column(String, nullable=False)
    salesforce_id = Column(String, nullable=False)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)
    deleted_at = Column(DateTime, index=True)


class SalesforceUser(Base):
    __tablename__ = 'salesforce_users'

    id = Column(Integer, primary_key=True, server_default=text(
        "nextval('salesforce_users_id_seq'::regclass)"))
    name = Column(String)
    uid = Column(String, nullable=False)
    oauth_token = Column(String, nullable=False)
    refresh_token = Column(String, nullable=False)
    instance_url = Column(String, nullable=False)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)


t_schema_migrations = Table(
    'schema_migrations', metadata,
    Column('version', String, nullable=False, unique=True)
)


class SchoolDistrictDistrict(Base):
    __tablename__ = 'school_district_districts'

    id = Column(Integer, primary_key=True, server_default=text(
        "nextval('school_district_districts_id_seq'::regclass)"))
    name = Column(String, nullable=False, unique=True)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)


class SchoolDistrictSchool(Base):
    __tablename__ = 'school_district_schools'
    __table_args__ = (
        Index('index_schools_on_name_and_district_id', 'name',
              'school_district_district_id', unique=True),
    )

    id = Column(Integer, primary_key=True, server_default=text(
        "nextval('school_district_schools_id_seq'::regclass)"))
    name = Column(String, nullable=False, unique=True)
    school_district_district_id = Column(
        ForeignKey('school_district_districts.id', ondelete='SET NULL',
                   onupdate='CASCADE'), index=True)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)

    school_district_district = relationship('SchoolDistrictDistrict')


class Setting(Base):
    __tablename__ = 'settings'
    __table_args__ = (
        Index('index_settings_on_thing_type_and_thing_id_and_var', 'thing_type',
              'thing_id', 'var', unique=True),
    )

    id = Column(Integer, primary_key=True,
                server_default=text("nextval('settings_id_seq'::regclass)"))
    var = Column(String, nullable=False)
    value = Column(Text)
    thing_id = Column(Integer)
    thing_type = Column(String(30))
    created_at = Column(DateTime)
    updated_at = Column(DateTime)


class ShortCodeShortCode(Base):
    __tablename__ = 'short_code_short_codes'

    id = Column(Integer, primary_key=True, server_default=text(
        "nextval('short_code_short_codes_id_seq'::regclass)"))
    code = Column(String, nullable=False, unique=True)
    uri = Column(Text, nullable=False)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)


class TasksAssistant(Base):
    __tablename__ = 'tasks_assistants'

    id = Column(Integer, primary_key=True, server_default=text(
        "nextval('tasks_assistants_id_seq'::regclass)"))
    name = Column(String, nullable=False, unique=True)
    code_class_name = Column(String, nullable=False, unique=True)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)


class TasksConceptCoachTask(Base):
    __tablename__ = 'tasks_concept_coach_tasks'
    __table_args__ = (
        Index('index_tasks_concept_coach_tasks_on_e_r_id_and_c_p_id',
              'entity_role_id', 'content_page_id', unique=True),
    )

    id = Column(Integer, primary_key=True, server_default=text(
        "nextval('tasks_concept_coach_tasks_id_seq'::regclass)"))
    content_page_id = Column(
        ForeignKey('content_pages.id', ondelete='CASCADE', onupdate='CASCADE'),
        nullable=False, index=True)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)
    entity_role_id = Column(
        ForeignKey('entity_roles.id', ondelete='CASCADE', onupdate='CASCADE'),
        nullable=False)
    deleted_at = Column(DateTime, index=True)
    tasks_task_id = Column(ForeignKey('tasks_tasks.id'), nullable=False,
                           unique=True)

    content_page = relationship('ContentPage')
    entity_role = relationship('EntityRole')
    tasks_task = relationship('TasksTask')


class TasksCourseAssistant(Base):
    __tablename__ = 'tasks_course_assistants'
    __table_args__ = (
        Index('index_tasks_course_assistants_on_assistant_id_and_course_id',
              'tasks_assistant_id', 'course_profile_course_id'),
        Index('index_tasks_course_assistants_on_course_id_and_task_plan_type',
              'course_profile_course_id', 'tasks_task_plan_type', unique=True)
    )

    id = Column(Integer, primary_key=True, server_default=text(
        "nextval('tasks_course_assistants_id_seq'::regclass)"))
    course_profile_course_id = Column(
        ForeignKey('course_profile_courses.id', ondelete='CASCADE',
                   onupdate='CASCADE'), nullable=False)
    tasks_assistant_id = Column(
        ForeignKey('tasks_assistants.id', ondelete='CASCADE',
                   onupdate='CASCADE'), nullable=False)
    tasks_task_plan_type = Column(String, nullable=False)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)
    settings = Column(Text, nullable=False, server_default=text("'{}'::text"))
    data = Column(Text, nullable=False, server_default=text("'{}'::text"))

    course_profile_course = relationship('CourseProfileCourse')
    tasks_assistant = relationship('TasksAssistant')


class TasksPerformanceReportExport(Base):
    __tablename__ = 'tasks_performance_report_exports'
    __table_args__ = (
        Index('index_performance_report_exports_on_role_and_course',
              'entity_role_id', 'course_profile_course_id'),
    )

    id = Column(Integer, primary_key=True, server_default=text(
        "nextval('tasks_performance_report_exports_id_seq'::regclass)"))
    course_profile_course_id = Column(
        ForeignKey('course_profile_courses.id', ondelete='CASCADE',
                   onupdate='CASCADE'), nullable=False, index=True)
    entity_role_id = Column(
        ForeignKey('entity_roles.id', ondelete='CASCADE', onupdate='CASCADE'),
        nullable=False)
    export = Column(String)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)

    course_profile_course = relationship('CourseProfileCourse')
    entity_role = relationship('EntityRole')


class TasksTaskPlan(Base):
    __tablename__ = 'tasks_task_plans'
    __table_args__ = (
        Index('index_tasks_task_plans_on_owner_id_and_owner_type', 'owner_id',
              'owner_type'),
    )

    id = Column(Integer, primary_key=True, server_default=text(
        "nextval('tasks_task_plans_id_seq'::regclass)"))
    tasks_assistant_id = Column(
        ForeignKey('tasks_assistants.id', ondelete='CASCADE',
                   onupdate='CASCADE'), nullable=False, index=True)
    owner_id = Column(Integer, nullable=False)
    owner_type = Column(String, nullable=False)
    type = Column(String, nullable=False)
    title = Column(String, nullable=False)
    description = Column(Text)
    settings = Column(Text, nullable=False)
    publish_last_requested_at = Column(DateTime)
    first_published_at = Column(DateTime)
    publish_job_uuid = Column(String)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)
    content_ecosystem_id = Column(
        ForeignKey('content_ecosystems.id', ondelete='CASCADE',
                   onupdate='CASCADE'), nullable=False, index=True)
    is_feedback_immediate = Column(Boolean, nullable=False,
                                   server_default=text("true"))
    deleted_at = Column(DateTime, index=True)
    last_published_at = Column(DateTime)
    cloned_from_id = Column(
        ForeignKey('tasks_task_plans.id', ondelete='SET NULL',
                   onupdate='CASCADE'), index=True)

    cloned_from = relationship('TasksTaskPlan', remote_side=[id])
    content_ecosystem = relationship('ContentEcosystem')
    tasks_assistant = relationship('TasksAssistant')


class TasksTaskStep(Base):
    __tablename__ = 'tasks_task_steps'
    __table_args__ = (
        Index('index_tasks_task_steps_on_tasks_task_id_and_number',
              'tasks_task_id', 'number', unique=True),
        Index('index_tasks_task_steps_on_tasked_id_and_tasked_type',
              'tasked_id', 'tasked_type', unique=True)
    )

    id = Column(Integer, primary_key=True, server_default=text(
        "nextval('tasks_task_steps_id_seq'::regclass)"))
    tasks_task_id = Column(
        ForeignKey('tasks_tasks.id', ondelete='CASCADE', onupdate='CASCADE'),
        nullable=False)
    tasked_id = Column(Integer, nullable=False)
    tasked_type = Column(String, nullable=False)
    number = Column(Integer, nullable=False)
    first_completed_at = Column(DateTime)
    last_completed_at = Column(DateTime)
    group_type = Column(Integer, nullable=False, server_default=text("0"))
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)
    deleted_at = Column(DateTime, index=True)
    related_content = Column(Text, nullable=False,
                             server_default=text("'[]'::text"))
    related_exercise_ids = Column(Text, nullable=False,
                                  server_default=text("'[]'::text"))
    labels = Column(Text, nullable=False, server_default=text("'[]'::text"))

    tasks_task = relationship('TasksTask')


class TasksTaskedExercise(Base):
    __tablename__ = 'tasks_tasked_exercises'

    id = Column(Integer, primary_key=True, server_default=text(
        "nextval('tasks_tasked_exercises_id_seq'::regclass)"))
    content_exercise_id = Column(
        ForeignKey('content_exercises.id', ondelete='CASCADE',
                   onupdate='CASCADE'), nullable=False, index=True)
    url = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    title = Column(String)
    free_response = Column(Text)
    answer_id = Column(String)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)
    correct_answer_id = Column(String, nullable=False)
    is_in_multipart = Column(Boolean, nullable=False,
                             server_default=text("false"))
    question_id = Column(String, nullable=False, index=True)
    deleted_at = Column(DateTime, index=True)
    context = Column(Text)

    content_exercise = relationship('ContentExercise')


class TasksTaskedExternalUrl(Base):
    __tablename__ = 'tasks_tasked_external_urls'

    id = Column(Integer, primary_key=True, server_default=text(
        "nextval('tasks_tasked_external_urls_id_seq'::regclass)"))
    url = Column(String, nullable=False)
    title = Column(String)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)
    deleted_at = Column(DateTime, index=True)


class TasksTaskedInteractive(Base):
    __tablename__ = 'tasks_tasked_interactives'

    id = Column(Integer, primary_key=True, server_default=text(
        "nextval('tasks_tasked_interactives_id_seq'::regclass)"))
    url = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    title = Column(String)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)
    deleted_at = Column(DateTime, index=True)


class TasksTaskedPlaceholder(Base):
    __tablename__ = 'tasks_tasked_placeholders'

    id = Column(Integer, primary_key=True, server_default=text(
        "nextval('tasks_tasked_placeholders_id_seq'::regclass)"))
    placeholder_type = Column(Integer, nullable=False, server_default=text("0"))
    deleted_at = Column(DateTime, index=True)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)


class TasksTaskedReading(Base):
    __tablename__ = 'tasks_tasked_readings'

    id = Column(Integer, primary_key=True, server_default=text(
        "nextval('tasks_tasked_readings_id_seq'::regclass)"))
    url = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    title = Column(String)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)
    deleted_at = Column(DateTime, index=True)
    book_location = Column(Text, nullable=False,
                           server_default=text("'[]'::text"))


class TasksTaskedVideo(Base):
    __tablename__ = 'tasks_tasked_videos'

    id = Column(Integer, primary_key=True, server_default=text(
        "nextval('tasks_tasked_videos_id_seq'::regclass)"))
    url = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    title = Column(String)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)
    deleted_at = Column(DateTime, index=True)


class TasksTaskingPlan(Base):
    __tablename__ = 'tasks_tasking_plans'
    __table_args__ = (
        Index('index_tasking_plans_on_t_id_and_t_type_and_t_p_id', 'target_id',
              'target_type', 'tasks_task_plan_id', unique=True),
        Index('index_tasks_tasking_plans_on_due_at_ntz_and_opens_at_ntz',
              'due_at_ntz', 'opens_at_ntz')
    )

    id = Column(Integer, primary_key=True, server_default=text(
        "nextval('tasks_tasking_plans_id_seq'::regclass)"))
    target_id = Column(Integer, nullable=False)
    target_type = Column(String, nullable=False)
    tasks_task_plan_id = Column(
        ForeignKey('tasks_task_plans.id', ondelete='CASCADE',
                   onupdate='CASCADE'), nullable=False, index=True)
    opens_at_ntz = Column(DateTime, nullable=False, index=True)
    due_at_ntz = Column(DateTime, nullable=False)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)
    time_zone_id = Column(
        ForeignKey('time_zones.id', ondelete='SET NULL', onupdate='CASCADE'),
        nullable=False, index=True)
    deleted_at = Column(DateTime, index=True)

    tasks_task_plan = relationship('TasksTaskPlan')
    time_zone = relationship('TimeZone')


class TasksTasking(Base):
    __tablename__ = 'tasks_taskings'
    __table_args__ = (
        Index('index_tasks_taskings_on_tasks_task_id_and_entity_role_id',
              'tasks_task_id', 'entity_role_id', unique=True),
    )

    id = Column(Integer, primary_key=True, server_default=text(
        "nextval('tasks_taskings_id_seq'::regclass)"))
    entity_role_id = Column(
        ForeignKey('entity_roles.id', ondelete='CASCADE', onupdate='CASCADE'),
        nullable=False, index=True)
    course_membership_period_id = Column(
        ForeignKey('course_membership_periods.id', ondelete='SET NULL',
                   onupdate='CASCADE'), index=True)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)
    deleted_at = Column(DateTime, index=True)
    tasks_task_id = Column(ForeignKey('tasks_tasks.id'), nullable=False)

    course_membership_period = relationship('CourseMembershipPeriod')
    entity_role = relationship('EntityRole')
    tasks_task = relationship('TasksTask')


class TasksTask(Base):
    __tablename__ = 'tasks_tasks'
    __table_args__ = (
        Index('index_tasks_tasks_on_due_at_ntz_and_opens_at_ntz', 'due_at_ntz',
              'opens_at_ntz'),
    )

    id = Column(Integer, primary_key=True,
                server_default=text("nextval('tasks_tasks_id_seq'::regclass)"))
    tasks_task_plan_id = Column(
        ForeignKey('tasks_task_plans.id', ondelete='CASCADE',
                   onupdate='CASCADE'), index=True)
    task_type = Column(Integer, nullable=False, index=True)
    title = Column(String, nullable=False)
    description = Column(Text)
    opens_at_ntz = Column(DateTime, index=True)
    due_at_ntz = Column(DateTime)
    feedback_at_ntz = Column(DateTime)
    last_worked_at = Column(DateTime, index=True)
    tasks_taskings_count = Column(Integer, nullable=False,
                                  server_default=text("0"))
    personalized_placeholder_strategy = Column(Text)
    steps_count = Column(Integer, nullable=False, server_default=text("0"))
    completed_steps_count = Column(Integer, nullable=False,
                                   server_default=text("0"))
    core_steps_count = Column(Integer, nullable=False, server_default=text("0"))
    completed_core_steps_count = Column(Integer, nullable=False,
                                        server_default=text("0"))
    exercise_steps_count = Column(Integer, nullable=False,
                                  server_default=text("0"))
    completed_exercise_steps_count = Column(Integer, nullable=False,
                                            server_default=text("0"))
    recovered_exercise_steps_count = Column(Integer, nullable=False,
                                            server_default=text("0"))
    correct_exercise_steps_count = Column(Integer, nullable=False,
                                          server_default=text("0"))
    placeholder_steps_count = Column(Integer, nullable=False,
                                     server_default=text("0"))
    placeholder_exercise_steps_count = Column(Integer, nullable=False,
                                              server_default=text("0"))
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)
    correct_on_time_exercise_steps_count = Column(Integer, nullable=False,
                                                  server_default=text("0"))
    completed_on_time_exercise_steps_count = Column(Integer, nullable=False,
                                                    server_default=text("0"))
    completed_on_time_steps_count = Column(Integer, nullable=False,
                                           server_default=text("0"))
    accepted_late_at = Column(DateTime)
    correct_accepted_late_exercise_steps_count = Column(Integer, nullable=False,
                                                        server_default=text(
                                                            "0"))
    completed_accepted_late_exercise_steps_count = Column(Integer,
                                                          nullable=False,
                                                          server_default=text(
                                                              "0"))
    completed_accepted_late_steps_count = Column(Integer, nullable=False,
                                                 server_default=text("0"))
    time_zone_id = Column(
        ForeignKey('time_zones.id', ondelete='SET NULL', onupdate='CASCADE'),
        index=True)
    deleted_at = Column(DateTime, index=True)
    hidden_at = Column(DateTime, index=True)
    spy = Column(Text, nullable=False, server_default=text("'{}'::text"))

    tasks_task_plan = relationship('TasksTaskPlan')
    time_zone = relationship('TimeZone')


class TimeZone(Base):
    __tablename__ = 'time_zones'

    id = Column(Integer, primary_key=True,
                server_default=text("nextval('time_zones_id_seq'::regclass)"))
    name = Column(String, nullable=False, index=True)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)


class UserAdministrator(Base):
    __tablename__ = 'user_administrators'

    id = Column(Integer, primary_key=True, server_default=text(
        "nextval('user_administrators_id_seq'::regclass)"))
    user_profile_id = Column(
        ForeignKey('user_profiles.id', ondelete='CASCADE', onupdate='CASCADE'),
        nullable=False, unique=True)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)

    user_profile = relationship('UserProfile')


class UserContentAnalyst(Base):
    __tablename__ = 'user_content_analysts'

    id = Column(Integer, primary_key=True, server_default=text(
        "nextval('user_content_analysts_id_seq'::regclass)"))
    user_profile_id = Column(
        ForeignKey('user_profiles.id', ondelete='CASCADE', onupdate='CASCADE'),
        nullable=False, unique=True)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)

    user_profile = relationship('UserProfile')


class UserCustomerService(Base):
    __tablename__ = 'user_customer_services'

    id = Column(Integer, primary_key=True, server_default=text(
        "nextval('user_customer_services_id_seq'::regclass)"))
    user_profile_id = Column(
        ForeignKey('user_profiles.id', ondelete='CASCADE', onupdate='CASCADE'),
        nullable=False, unique=True)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)

    user_profile = relationship('UserProfile')


class UserProfile(Base):
    __tablename__ = 'user_profiles'

    id = Column(Integer, primary_key=True, server_default=text(
        "nextval('user_profiles_id_seq'::regclass)"))
    account_id = Column(
        ForeignKey('openstax_accounts_accounts.id', ondelete='CASCADE',
                   onupdate='CASCADE'), nullable=False, unique=True)
    exchange_read_identifier = Column(String, nullable=False, unique=True)
    exchange_write_identifier = Column(String, nullable=False, unique=True)
    deleted_at = Column(DateTime, index=True)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)
    ui_settings = Column(Text)

    account = relationship('OpenstaxAccountsAccount')


class UserTourView(Base):
    __tablename__ = 'user_tour_views'
    __table_args__ = (
        Index('index_user_tour_views_on_user_profile_id_and_user_tour_id',
              'user_profile_id', 'user_tour_id', unique=True),
    )

    id = Column(Integer, primary_key=True, server_default=text(
        "nextval('user_tour_views_id_seq'::regclass)"))
    view_count = Column(Integer, nullable=False, server_default=text("0"))
    user_profile_id = Column(ForeignKey('user_profiles.id'), nullable=False)
    user_tour_id = Column(ForeignKey('user_tours.id'), nullable=False,
                          index=True)

    user_profile = relationship('UserProfile')
    user_tour = relationship('UserTour')


class UserTour(Base):
    __tablename__ = 'user_tours'

    id = Column(Integer, primary_key=True,
                server_default=text("nextval('user_tours_id_seq'::regclass)"))
    identifier = Column(Text, nullable=False, unique=True)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)
