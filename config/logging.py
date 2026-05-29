import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
ON_RENDER = os.environ.get("RENDER", "").lower() in ("1", "true", "yes")

_handlers = {
    "console": {
        "level": "DEBUG",
        "class": "logging.StreamHandler",
        "formatter": "simple",
    },
}

if not ON_RENDER:
    _handlers["file"] = {
        "level": "DEBUG",
        "class": "logging.FileHandler",
        "formatter": "verbose",
        "filename": BASE_DIR / "django.log",
    }

_default_handlers = ["console"] if ON_RENDER else ["console", "file"]
_server_handlers = ["console"] if ON_RENDER else ["console", "file"]
_request_handlers = ["console"] if ON_RENDER else ["file"]

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse',
        },
    },
    'formatters': {
        'simple': {
            'format': '{levelname} {asctime:s} {name} {message}',
            'style': '{' #форматирование в виде строк
        },
        'verbose': {
            'format': '{levelname} {asctime:s} {name} {module}.py (line {lineno:d}) {funcName} {message}',
            'style': '{',
        },
    },
    'handlers': _handlers,
    'loggers': {
        '': {
            'level': 'WARNING',
            'handlers': _default_handlers,
        },
        'django.request': {
            'level': 'WARNING',
            'handlers': _request_handlers,
            'propagate': False,
        },
        'django.server': {
            'level': 'INFO',
            'handlers': _server_handlers,
            'propagate': False,
        },
        'django': {
            'level': 'INFO',
            'handlers': ['console'],
            'propagate': False,
        },
        'django.template': {
            'level': 'DEBUG',
            'handlers': _request_handlers,
            'propagate': False,
        },
    },
}