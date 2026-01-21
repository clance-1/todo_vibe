from __future__ import with_statement

"""alembic environment 설정 파일

이 모듈은 `alembic` 명령(예: `alembic upgrade head`)이 실행될 때 로드됩니다.
주요 역할:
- 애플리케이션의 SQLAlchemy 메타데이터(`db.metadata`)를 가져와 Alembic의
    타깃 메타데이터로 사용합니다.
- 환경변수 `SQLALCHEMY_DATABASE_URI`를 읽어 DB 연결 문자열로 사용하고,
    지정되지 않으면 로컬 SQLite(`sqlite:///todo.db`)로 폴백합니다.
- 오프라인(`run_migrations_offline`) 및 온라인(`run_migrations_online`) 모드를
    지원해 CLI 환경 및 접속 가능한 DB 환경 모두에서 마이그레이션을 수행합니다.

참고:
- 이 파일은 애플리케이션 코드에서 Alembic API를 직접 호출하지 않으며,
    CI나 수동 실행하는 Alembic CLI가 로드하여 실행합니다.
"""

import sys
import os
from logging.config import fileConfig

from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context

# allow imports from project root
sys.path.append(os.getcwd())

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Import target metadata from the application
# Prevent the application from creating tables when alembic imports the app
# (see app.py which respects SKIP_DB_CREATE). Set the env var here so
# the top-level import of `app` does not call `db.create_all()`.
os.environ['SKIP_DB_CREATE'] = '1'
from app import db
target_metadata = db.metadata


def get_url():
    """데이터베이스 연결 URL을 반환합니다.

    우선 환경변수 `SQLALCHEMY_DATABASE_URI`를 확인하고, 존재하지 않으면
    로컬 SQLite (`sqlite:///todo.db`) URL을 반환합니다. Alembic이 실행될 때
    사용되는 연결 문자열을 중앙에서 관리합니다.

    Returns:
        str: SQLAlchemy 연결 문자열.
    """
    return os.environ.get('SQLALCHEMY_DATABASE_URI', 'sqlite:///todo.db')


def run_migrations_offline():
    """오프라인 모드에서 마이그레이션을 실행합니다.

    이 모드는 데이터베이스에 직접 연결하지 않고, 연결 URL을 사용해 SQL
    스크립트를 생성하거나 오프라인 환경에서 마이그레이션을 적용할 때
    사용됩니다.
    """
    url = get_url()
    context.configure(url=url, target_metadata=target_metadata, literal_binds=True)
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    """온라인 모드에서 마이그레이션을 실행합니다.

    데이터베이스에 직접 연결하여 Alembic의 마이그레이션을 적용합니다.
    일반적으로 CI나 실제 실행 환경에서 사용됩니다. 이 함수는 alembic
    설정에서 읽은 값을 기반으로 연결을 구성하고 마이그레이션을 실행합니다.
    """
    configuration = config.get_section(config.config_ini_section) or {}
    configuration['sqlalchemy.url'] = get_url()
    connectable = engine_from_config(
        configuration,
        prefix='sqlalchemy.',
        poolclass=pool.NullPool,
    )
    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)
        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
