from django import forms

from .models import Feedback
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit,Field
from .models import Feedback  # Import your Feedback model
class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        exclude = []
        widgets = {
            'category': forms.RadioSelect()
        }
    

    def __init__(self, *args, **kwargs):
        super(FeedbackForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_method='post'
        self.helper.layout = Layout(
            Field('feedback_type'),
            Field('email'),  # Apply inline style
            Field('details'),  # Add mb-3 for margin-bottom
        )
        self.helper.add_input(Submit('submit','Submit'))

    # feedback_type = forms.ChoiceField(widget=forms.RadioSelect,  # Use RadioSelect widget
    #     choices=Feedback.FEEDBACK_TYPE,  # Use the same choices as in the model
    #     )