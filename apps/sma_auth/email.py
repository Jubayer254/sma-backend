from djoser import email

class ActivationEmail(email.ActivationEmail):
    template_name = "email/activation.html"

    def get_context_data(self):
        context = super().get_context_data()
        context["domain"] = "localhost:8000"
        context["site_name"] = "Spark Medical Academy"
        return context

class PasswordResetEmail(email.PasswordResetEmail):
    template_name = "email/password_reset.html"

    def get_context_data(self):
        context = super().get_context_data()
        context["domain"] = "localhost:8000"
        context["site_name"] = "Spark Medical Academy"
        return context
