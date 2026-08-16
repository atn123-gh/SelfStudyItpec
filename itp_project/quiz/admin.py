from django.contrib import admin

from quiz.models.rdbms_models import QuizModel

# Register your models here.

@admin.register(QuizModel)
class QuizModelAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('level', 'exam_date_str')}
