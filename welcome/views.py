from django.views.generic import TemplateView


class WelcomeHomeView(TemplateView):
    template_name = "welcome/index.html"
