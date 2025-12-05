import sys
from logging.config import fileConfig

    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,


        with context.begin_transaction():
            context.run_migrations()

