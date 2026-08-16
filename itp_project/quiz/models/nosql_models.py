from djongo import models


class QuestionSet(models.Model):
    folder = models.CharField(max_length=255, unique=True)  # Unique folder name

    # Storing data as JSON fields since MongoDB supports flexible schemas
    questions = models.JSONField()  # Dictionary: { "Q1": "Q1.png", "Q2": "Q2.png" }
    solutions = models.JSONField()  # Dictionary: { "Q1": "Solution text", "Q2": "Solution text" }
    correct_options = models.JSONField()  # Dictionary: { "Q1": 0, "Q2": 1 }
    ratings = models.JSONField()  # Dictionary: { "Q1": 5, "Q2": 3 }

    class Meta:
        abstract = True  # Prevents this from being created directly as a collection


# Collection for IP questions
class IPQuestion(QuestionSet):
    class Meta:
        db_table = "ip_questions"


# Collection for FE questions
class FEQuestion(QuestionSet):
    class Meta:
        db_table = "fe_questions"
