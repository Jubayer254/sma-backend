from djoser import email

class ActivationEmail(email.ActivationEmail):
    template_name = "email/activation_mail.html"

class PasswordResetEmail(email.PasswordResetEmail):
    template_name = "email/password_reset.html"

class CustomConfirmationEmail(email.ConfirmationEmail):
    template_name = "email/activation_success.html"

class CustomPasswordChangedConfirmationEmail(email.PasswordChangedConfirmationEmail):
    template_name = "email/password_change_success.html"
