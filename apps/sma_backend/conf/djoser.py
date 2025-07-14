# Djoser settings
DJOSER = {
    'SERIALIZERS': {
        'user_create': 'sma_auth.serializers.UserCreateSerializer',
        'user': 'sma_auth.serializers.UserSerializer',
    },
    'PASSWORD_RESET_CONFIRM_URL': 'password/reset/confirm/{uid}/{token}/',
    'ACTIVATION_URL': 'activate/{uid}/{token}/',
    'SEND_CONFIRMATION_EMAIL': True,
    'SEND_ACTIVATION_EMAIL': True,
    'EMAIL': {
        'password_reset': 'djoser.email.PasswordResetEmail',
        'activation': 'djoser.email.ActivationEmail',
    },
}