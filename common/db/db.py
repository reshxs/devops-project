import peewee_async

import settings

database = peewee_async.PostgresqlDatabase("postgres",
                                           host=settings.DB_HOST,
                                           port=settings.DB_PORT,
                                           user=settings.DB_USER,
                                           password=settings.DB_PASSWORD)
