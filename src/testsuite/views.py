import datetime

from django.contrib import messages
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import ListView
from django.views.generic.base import View

from account.models import User
from testsuite.models import Test, Question, Answer, TestResult, TestResultDetail


class TestSuiteListView(ListView):
    model = Test
    template_name = 'testsuite_list.html'
    paginate_by = 5


class LeaderBoardView(ListView):
    model = User
    paginate_by = 5


class TestRunView(View):
    PREFIX = 'answer_'

    def get(self, request, pk, seq_nr):
        question = Question.objects.filter(test__id=pk, number=seq_nr).first()

        answers = [
            answer.text
            for answer in question.answers.all()
        ]

        return render(
            request=request,
            template_name='testrun.html',
            context={
                'question': question,
                'answers': answers,
                'prefix': self.PREFIX
            }
        )

    def post(self, request, pk, seq_nr):
        test = Test.objects.get(pk=pk)
        question = Question.objects.filter(test__id=pk, number=seq_nr).first()

        answers = Answer.objects.filter(
            question=question
        ).all()

        choices = {
            k.replace(self.PREFIX, '') : True
            for k in request.POST if k.startswith(self.PREFIX)
        }

        if not choices:
            messages.error(self.request, extra_tags='danger', message="ERROR: You should select at least 1 answer!")
            return redirect(reverse('test:testrun_step', kwargs={'pk': pk, 'seq_nr': seq_nr}))

        current_test_result = TestResult.objects.filter(
            test=test,
            user=request.user,
            is_completed=False).last()

        for idx, answer in enumerate(answers, 1):
            value = choices.get(str(idx), False)
            TestResultDetail.objects.create(
                test_result=current_test_result,
                question=question,
                answer=answer,
                is_correct=(value == answer.is_correct)
            )

        if question.number < test.questions_count():
            return redirect(reverse('test:testrun_step', kwargs={'pk': pk, 'seq_nr': seq_nr+1}))
        else:
            current_test_result.finish()
            current_test_result.save()
            return render(
                request=request,
                template_name='testrun_end.html',
                context={
                    'test_result': current_test_result,
                    'time_spent': datetime.datetime.utcnow() - current_test_result.datetime_run.replace(tzinfo=None)
                }
            )


class StartTestView(View):

    def get(self, request, pk):
        test = Test.objects.get(pk=pk)

        test_result = TestResult.objects.create(
            user=request.user,
            test=test
        )

        return render(
            request=request,
            template_name='testrun_start.html',
            context={
                'test': test,
                'test_result': test_result
            },
        )
