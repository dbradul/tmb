import datetime

from django.contrib import messages
from django.conf import settings
from django.http import HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView
from django.views.generic.base import View

from account.models import User
from testsuite.models import Test, Question, Answer, TestResult, TestResultDetail
from testsuite.tasks import run_slow

class TestSuiteListView(ListView):
    model = Test
    template_name = 'testsuite_list.html'
    queryset = Test.objects.order_by('id').all()
    paginate_by = 5


class LeaderBoardView(LoginRequiredMixin, ListView):
    model = User
    queryset = User.objects.order_by('-avr_score').all()
    paginate_by = 5
    template_name = 'leaderboard.html'
    login_url = reverse_lazy('login')


class TestRunView(LoginRequiredMixin, View):
    PREFIX = 'answer_'

    def get(self, request, pk):
        if 'testresult' not in request.session:
            return HttpResponse('ERROR!')

        testresult_step = request.session.get('testresult_step', 1)
        request.session['testresult_step'] = testresult_step

        question = Question.objects.get(test__id=pk, number=testresult_step)

        answers = question.answers.values_list('text', flat=True)

        return render(
            request=request,
            template_name='testrun_next.html',
            context={
                'question': question,
                'answers': answers,
                'prefix': self.PREFIX
            }
        )

    def post(self, request, pk):
        if 'testresult_step' not in request.session:
            return HttpResponse('ERROR!')

        testresult_step = request.session['testresult_step']

        test = Test.objects.get(pk=pk)
        question = Question.objects.get(test__id=pk, number=testresult_step)

        answers = Answer.objects.filter(
            question=question
        ).all()

        choices = {
            k.replace(self.PREFIX, '') : True
            for k in request.POST if k.startswith(self.PREFIX)
        }

        if not choices:
            messages.error(self.request, extra_tags='danger', message="ERROR: You should select at least 1 answer!")
            return redirect(reverse('test:next', kwargs={'pk': pk}))

        if len(choices) == len(answers):
            messages.error(self.request, extra_tags='danger', message="ERROR: You can't select ALL answer!")
            return redirect(reverse('test:next', kwargs={'pk': pk}))

        current_test_result = TestResult.objects.get(
            id=request.session['testresult']
        )

        for idx, answer in enumerate(answers, 1):
            value = choices.get(str(idx), False)
            TestResultDetail.objects.create(
                test_result=current_test_result,
                question=question,
                answer=answer,
                is_correct=(value == answer.is_correct)
            )

        if question.number < test.questions_count():
            current_test_result.is_new = False
            current_test_result.save()
            request.session['testresult_step'] = testresult_step + 1
            return redirect(reverse('test:next', kwargs={'pk': pk}))
        else:
            del request.session['testresult']
            del request.session['testresult_step']
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


class StartTestView(LoginRequiredMixin, View):

    def get(self, request, pk):
        test = Test.objects.get(id=pk)

        test_result_id = request.session.get('testresult')

        if test_result_id:
            test_result = TestResult.objects.get(id=test_result_id)
        else:
            test_result = TestResult.objects.create(
                user=request.user,
                test=test
            )

        request.session['testresult'] = test_result.id

        return render(
            request=request,
            template_name='testrun_start.html',
            context={
                'test': test,
                'test_result': test_result
            },
        )

def slow_func(request):
    run_slow.delay(2)
    return HttpResponse('DONE!')

