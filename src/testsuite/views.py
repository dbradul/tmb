from django.core.exceptions import ValidationError
from django.forms import inlineformset_factory, formset_factory, modelformset_factory
from django.shortcuts import render, redirect

# Create your views here.
from django.urls import reverse
from django.views.generic import ListView, UpdateView
from django.views.generic.base import View

from account.models import User
from testsuite.models import Test, Question, Answer


class TestSuiteListView(ListView):
    model = Test
    template_name = 'testsuite_list.html'
    paginate_by = 5


class LeaderBoardView(ListView):
    model = User
    paginate_by = 5


class TestRunView(View):

    def get(self, request, pk, seq_nr):
        testsuite = Test.objects.get(pk=pk)
        question = Question.objects.filter(test__id=pk, number=seq_nr).first()

        answers = Answer.objects.filter(
            question=question
        ).all()

        data = [
            answer.text
            for answer in answers
        ]

        return render(
            request=request,
            template_name='testrundetail_edit.html',
            context={
                'question': question,
                'data': data,
            },
        )

    def post(self, request, pk, seq_nr):
        question = Question.objects.filter(test__id=pk, number=seq_nr).first()

        answers = Answer.objects.filter(
            question=question
        ).all()

        data = request.POST
        # logic...

        return redirect(reverse('test:testrun_step', kwargs={'pk':pk, 'seq_nr': seq_nr+1}))


class StartTestView(View):

    def get(self, request, pk):
        test = Test.objects.get(pk=pk)

        return render(
            request=request,
            template_name='testrun_start.html',
            context={
                'test': test,
            },
        )
