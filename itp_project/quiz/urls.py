from django.urls import path
from .views import QuizListView,QuizShowQuiz,QuizSubmitView,get_solution

app_name = 'quiz'


urlpatterns = [
    path('submit/', QuizSubmitView.as_view(), name='submit'),

    path('<str:level>/', QuizListView.as_view(), name='choose'),
    # path('<str:level>/<str:exam_date>', QuizDetailView.as_view(), name='quiz'),
    # path('<int:pk>', QuizDetailView.as_view(), name='quiz'),
    path('<slug:slug>', QuizShowQuiz.as_view(), name='start'),
    # path('submitform', QuizSubmitView.as_view(), name='submitform'),
    path("solution/<str:level>/<str:folder>/<str:questionId>/", get_solution, name="get_solution"),
]
