from .form import FeedbackForm
from django.views.generic.edit import CreateView
from .models import Feedback  # Import your Feedback model
from django.shortcuts import render, redirect
from django.urls import reverse_lazy


class feedback_form(CreateView):
    model = Feedback
    form_class = FeedbackForm
    template_name = "feedback.html"
    # success_url = "success"
    # success_url = reverse_lazy('feedback')
    success_url = '/home/feedback'  

    # def form_valid(self, form):
    #     # This method is called when valid form data has been POSTed.
    #     # It should return an HttpResponse.
    #     return super().form_valid(form)
    def form_valid(self, form):
        self.object = form.save()
        return self.render_to_response(self.get_context_data(form=self.form_class(), submitted=True))  # Provide a new form instance

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form, submitted=False))