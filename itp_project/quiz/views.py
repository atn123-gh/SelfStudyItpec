from django.utils import timezone
from django.views.generic import ListView,DetailView
from django.views.generic.edit import FormView
from django.views import View
from django.views.generic.detail import SingleObjectMixin
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.shortcuts import render
from itp_project import constant
from django.views.decorators.http import require_http_methods

from quiz.form import QuizForm
from .models import QuizModel,IPQuestion, FEQuestion 
import os
import re
import logging
logger=logging.getLogger("quiz_view_logger")

# from django.contrib.sitemaps import GenericSitemap
# quiz_dict={
#     'queryset': QuizModel.objects.all(),
# }
# quiz_sitemap=GenericSitemap(quiz_dict)


class QuizListView(ListView):
    template_name="quiz/quiz_list.html"
    model = QuizModel
    context_object_name = "quizzes"

    def get_queryset(self):
        queryset = super().get_queryset()
        level = self.kwargs.get('level')
        if level:
            queryset = queryset.filter(level=level).order_by('id')
        queryset=queryset.reverse()   # recent first
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['level'] = self.kwargs.get('level') ##  displaying title
        return context

class QuizShowQuiz(DetailView):
    model = QuizModel
    template_name = 'quiz/quiz.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        quiz_instance = self.object
        q_cnt=QuizModel.questCnt(quiz_instance.level)

        context['QImgPath'] = QuizModel.generateFilePath(quiz_instance.level,quiz_instance.qfolder_name)
        context['level'] = quiz_instance.level
        context['qfolder_name'] = quiz_instance.qfolder_name

        if 'submitted_form' in self.request.session:
            submitted_data= self.request.session['submitted_form']
            context['qform'] = QuizForm(initial=submitted_data,show_ans=True,q_cnt=q_cnt)
            checkedAns=QuizModel.get_check_answers(submitted_data['stud_answers_hidden'],quiz_instance.answer)
            del self.request.session['submitted_form']
            qPattern = r'Q\d+'  
            for field_name in context['qform'].fields.keys():
                if re.match(qPattern, field_name):
                    context['qform'].fields[field_name].widget.attrs['disabled'] = True
            context['correct_answers'] =quiz_instance.answer
            context['check_results'] = checkedAns
        else:
            stud_answers_hidden=QuizModel.initial_form_answers(q_cnt)
            context['qform'] = QuizForm(initial={'slug_hidden':quiz_instance.slug,'stud_answers_hidden':stud_answers_hidden},q_cnt=q_cnt)

        return context


# just checking validation (no checking answer) and redirect to detail
class QuizSubmitView(FormView):
    template_name = 'quiz/quiz.html'    
    form_class = QuizForm
    slug_hidden=''

    def get_form_kwargs(self):
        kwargs = super(QuizSubmitView, self).get_form_kwargs()
        slug=self.request.POST['slug_hidden']
        level=slug[:2]
        kwargs['q_cnt'] = QuizModel.questCnt(level)
        logger.info('Submit Quiz Name : %s', slug)
        return kwargs

    def form_valid(self, form):
        if form.is_valid():
            self.slug_hidden = form.cleaned_data['slug_hidden']
            self.request.session['submitted_form']=form.cleaned_data
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("quiz:start", args={self.slug_hidden})


from django.http import JsonResponse
from itp_project.settings.mongodb_service import MongoDBService

def get_solution(request, level, folder, questionId):

    try:
        # Determine collection based on level
        if level.upper() == "IP":
            collection_name = "ip_questions"
        elif level.upper() == "FE":
            collection_name = "fe_questions"
        else:
            return JsonResponse({"error": "Invalid level. Use 'IP' or 'FE'."}, status=400)

        # Get the collection
        collection = MongoDBService.get_collection(collection_name)

        # Retrieve the document from the selected collection
        document = collection.find_one({"folder": folder})

        if not document:
            return JsonResponse({"error": f"Folder '{folder}' not found"}, status=404)

        print("Document retrieved successfully.")

        # Ensure solutions is a dictionary and get the solution
        if "solutions" in document and isinstance(document["solutions"], dict) and questionId in document["solutions"]:
            solution = document["solutions"][questionId]
            correct_option = document["correct_options"][questionId]
            print("Solution retrieved:", solution)
            return JsonResponse({
                "level": level.upper(),
                "folder": folder,
                "question": questionId,
                "solution": solution,
                "correct_option": correct_option
            })
        else:
            return JsonResponse({"error": f"Solution for question '{questionId}' not found"}, status=404)

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
