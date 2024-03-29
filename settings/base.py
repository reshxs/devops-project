import os
import logging

BASE_URL = 'http://84.201.153.135'

HOST = os.environ.get("HOST", "0.0.0.0")
PORT = os.environ.get("PORT", 8080)

DB_HOST = os.environ.get("DB_HOST", "0.0.0.0")
DB_PORT = os.environ.get("DB_PORT", 5432)
DB_USER = os.environ.get("DB_USER", "postgres")
DB_PASSWORD = os.environ.get("DB_PASSWORD", "password")

MEMCACHED_HOST = os.environ.get("MEMCACHED_HOST", "localhost")
MEMCACHED_PORT = os.environ.get("MEMCACHED_PORT", 11211)

RABBIT_HOST = os.environ.get("RABBIT_HOST", "localhost")
RABBIT_PORT = os.environ.get("RABBIT_PORT", 5672)
RABBIT_LOGIN = os.environ.get("RABBIT_USER", "guest")
RABBIT_PASSWORD = os.environ.get("RABBIT_PASS", "guest")

ESB_EMAIL_EXCHANGE = 'email'
ESB_EMAIL_ROUTING_KEY = 'email'

SESSION_MAX_AGE = 1800

LOGGER_LEVEL = logging.DEBUG

