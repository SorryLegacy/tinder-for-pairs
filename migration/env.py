from logging.config import fileConfig

from alembic import context

from services.database import POSTGRES_URL, engine

from services.alembic_models import Base

config = context.config
fileConfig(config.config_file_name)


target_metadata = Base.metadata


def run_migrations_offline():
    context.configure(
        url=POSTGRES_URL,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():

    connectable = engine
    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
