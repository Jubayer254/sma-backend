LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,

    'filters': {
        'ignore_broken_pipe': {
            '()': 'sma_backend.logging_filters.IgnoreBrokenPipeFilter',
        },
    },

    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'filters': ['ignore_broken_pipe'],
        },
    },

    'loggers': {
        'django.server': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False,
        },
    },
}
