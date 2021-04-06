import os
import logging


HOST = os.environ.get("HOST", "0.0.0.0")
PORT = os.environ.get("PORT", 8080)

DB_HOST = os.environ.get("DB_HOST", "localhost")
DB_PORT = os.environ.get("DB_PORT", 5432)
DB_USER = os.environ.get("DB_USER", "postgres")
DB_PASSWORD = os.environ.get("DB_PASSWORD", "password")

MEMCACHED_HOST = os.environ.get("MEMCACHED_HOST", "localhost")
MEMCACHED_PORT = os.environ.get("MEMCACHED_PORT", 11211)

SESSION_MAX_AGE = 1800

LOGGER_LEVEL = logging.DEBUG

