from __future__ import unicode_literals

# {{ api_domains }}
ALLOWED_HOSTS = []

DEBUG = True

# Make these unique, and don't share it with anybody.
SECRET_KEY = "57b96088-4153-4075-8c27-bd248bd20cf38fe63350-a4c8-4e3f-a060-de2c0c07e047097a6d95-cc70-4978-a1dd-b5b885905194"
NEVERCACHE_KEY = "e7246b78-2e40-4c4f-a755-9da14d273824f307536e-72b8-41cb-8be1-327aa01bf2ca9d95f790-d658-433b-bfc5-0311af046dbb"

DATABASES = {
    "default": {
        # Ends with "postgresql_psycopg2", "mysql", "sqlite3" or "oracle".
        "ENGINE": "django.db.backends.sqlite3",
        # DB name or path to database file if using sqlite3.
        "NAME": "dev.db",
        # Not used with sqlite3.
        "USER": "",
        # Not used with sqlite3.
        "PASSWORD": "",
        # Set to empty string for localhost. Not used with sqlite3.
        "HOST": "",
        # Set to empty string for default. Not used with sqlite3.
        "PORT": "",
    }
}

SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTOCOL", "https")

CACHE_MIDDLEWARE_SECONDS = 60

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.memcached.MemcachedCache",
        "LOCATION": "127.0.0.1:11211",
    }
}

SESSION_ENGINE = "django.contrib.sessions.backends.cache"
