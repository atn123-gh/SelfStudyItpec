from django.test import TestCase
from quiz.models.rdbms_models import QuizModel


class QuizModelTest(TestCase):
    
    @classmethod
    def setUpTestData(cls):
        QuizModel.objects.create(level='i', exam_date_str='Bob',answer="dbabcdabcdbbacdabcdaabdcdbdacdbacdabcdacbdcabdbacddabcdbcabacbccdba")

    def testcheckFileExist(self):
        quiz=QuizModel.objects.get(1)

