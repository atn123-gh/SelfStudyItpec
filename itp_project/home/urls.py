from django.urls import path
from .views import feedback_form
from django.views.generic import TemplateView

app_name = 'home'


urlpatterns = [
    path("", TemplateView.as_view(template_name="itpechome.html"), name="itpec"),
    path("itpec", TemplateView.as_view(template_name="itpechome.html"), name="itpec"),
    path("feedback", feedback_form.as_view() , name="feedback"),
    # path("success", TemplateView.as_view(template_name="feedbackSuccess.html"), name="success"),

]

