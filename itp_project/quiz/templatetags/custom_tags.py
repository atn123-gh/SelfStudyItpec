from django import template

from ..models import QuizModel


register = template.Library()


@register.simple_tag
def iscorrect(answers , related_field_name):
    number= int(related_field_name[1:])

    ans= QuizModel.get_answers(answers,number)
    return ans == '1'

@register.simple_tag
def get_ans(answers , related_field_name):
    number= int(related_field_name[1:])
    ans= QuizModel.get_answers(answers ,number)
    return ans

# eg IP/2017A_IP_Question__2017_Oct/Q2.png ->  IP_2017A_IP_Question__2017_Oct_Q2png  
# id for solution
@register.filter
def replace_slash(value):
    return value.replace("/", "_").replace(".","")
      