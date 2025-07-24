DJOSER = {
    'SERIALIZERS': {
        'user_create': 'sma_auth.serializers.UserCreateSerializer',
        'user': 'sma_auth.serializers.UserSerializer',
    },
    'PASSWORD_RESET_CONFIRM_URL': 'password/reset/confirm/?uid={uid}&token={token}',
    'ACTIVATION_URL': 'activate/?uid={uid}&token={token}',
    'SEND_CONFIRMATION_EMAIL': True,
    'SEND_ACTIVATION_EMAIL': True,
    'EMAIL': {
        'activation': 'sma_auth.custom_email.ActivationEmail',
        'confirmation': 'sma_auth.custom_email.CustomConfirmationEmail',
        'password_reset': 'sma_auth.custom_email.PasswordResetEmail',
        'password_changed_confirmation': 'sma_auth.custom_email.CustomPasswordChangedConfirmationEmail',
    },
}
