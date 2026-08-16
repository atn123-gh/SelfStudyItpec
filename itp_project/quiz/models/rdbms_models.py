from django.db import models
from django.urls import reverse

from itp_project import constant


TEST_LEVEL = (
        ('ip', 'IP'),
        ('fe', 'FE'),
    )

AVAILABILITY = (
        ('a', 'available'),  # ok to use
        ('c', 'checking'),   # need to check 
        ('e', 'error'),  # error (e.g missing or wrong format)
    )

class QuizModel(models.Model):

    level = models.CharField(max_length=2, choices=TEST_LEVEL ,help_text='IP/FE',default="default")
    exam_date_str=  models.CharField(max_length=8 ,help_text='Year_Month',default="default")
    answer=models.CharField(max_length=100 ,help_text='abcd',default='default')
    qfolder_name= models.CharField(max_length=50,default="default")
    quesImg_cnt= models.IntegerField(default=-1)
    availability = models.CharField(max_length=10, choices=AVAILABILITY,default="default")
    slug = models.SlugField(unique=True,max_length=100,default="default")
   

    @staticmethod
    def questCnt(level):
        q_count=0
        if level == constant.IP:
            q_count=100
        elif level== constant.FE:
            q_count=80
        return q_count

    # @staticmethod
    # def form_student_answers2(cnt):
    #     return '0'*cnt

    
    @staticmethod
    def generateFilePath(level,qfolder_name):
        """ Return constructed file path base on level and folder name

        Args:
            level (_type_): level
            qfolder_name (_type_): questoin folder name(name of pdf file)

        Returns:
            _type_: file path
        """
        questionPath=f"{level}/{qfolder_name}/"
        return questionPath

    @staticmethod
    def initial_form_answers(cnt):
        return '0'*cnt
    
    @staticmethod
    def set_answers(answers,no,value):
        answers[no-1]=value

    @staticmethod
    def get_answers(answers,no):
        return answers[no-1]
    

    @staticmethod
    def get_check_answers(stud_answer,correct_answer):
        return ''.join(['1' if a == c else '0' for a, c in zip(stud_answer, correct_answer)]) 
    

    def get_absolute_url(self):
        return reverse('quiz:start', args=[str(self.slug)])
    

    def __str__(self):
        return '{0} ({1})'.format(self.level, self.exam_date_str)
    