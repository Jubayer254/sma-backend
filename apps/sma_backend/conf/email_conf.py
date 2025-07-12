# Email settings (for production, use environment variables or secure storage)
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True

EMAIL_HOST_USER = 'bitnova.net@gmail.com'         # sender email
EMAIL_HOST_PASSWORD = 'dzmv vjmj zell smlj'   # NOT your Gmail password!
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER