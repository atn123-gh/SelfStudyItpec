from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field,Submit
from django import forms
from django.urls import reverse

from django.forms.widgets import TextInput

class OutputTextWidget(TextInput):
    def render(self, name, value, attrs=None, renderer=None):
        output_html = f'{value}'
        return output_html


class QuizForm(forms.Form):
    options = (
            ('a', "a"), 
            ('b', "b"),
            ('c', "c"), 
            ('d', "d"),
        )

    def __init__(self, *args, **kwargs):
        show_ans = kwargs.pop('show_ans', False)  # get the condition value from kwargs
        q_cnt = kwargs.pop('q_cnt')  # get the condition value from kwargs

        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout()
        q_cnt=q_cnt +1
        for i in range(1,q_cnt):
            question = 'Q%d' % i
            self.fields[question] = forms.ChoiceField(choices = QuizForm.options, widget = forms.RadioSelect, required=False)
            self.helper.layout.append(question)        

        self.fields['slug_hidden'] = forms.CharField(widget=forms.HiddenInput(),max_length=80)
        self.fields['stud_answers_hidden'] = forms.CharField(widget=forms.HiddenInput(),max_length=100)

        self.helper.form_action = reverse('quiz:submit')

