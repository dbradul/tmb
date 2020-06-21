from django.core.exceptions import ValidationError
from django.forms import inlineformset_factory, formset_factory, modelformset_factory
from django.shortcuts import render, redirect

# Create your views here.
from django.urls import reverse
from django.views.generic import ListView, UpdateView
from django.views.generic.base import View

from account.models import User
from testsuite.forms import QuestionForm, TestRunForm
from testsuite.models import Test, Question, Answer, TestRun, TestRunDetail


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
        testsuite = Test.objects.get(pk=pk)
        question = Question.objects.filter(test__id=pk, number=seq_nr).first()

        answers = Answer.objects.filter(
            question=question
        ).all()

        data = request.POST
        # logic...

        return redirect(reverse('test:testrun_step', kwargs={'pk':pk, 'seq_nr': seq_nr+1}))


class TestView(View):

    def get(self, request, pk):
        testsuite = Test.objects.get(pk=pk)
        questions = Question.objects.filter(test_suite__id=pk)

        QuestionFormSet = modelformset_factory(
            model=Question,
            form=QuestionForm,
            #extra=0,
            # fields=('text', )
        )

        formset = QuestionFormSet(queryset=questions)

        return render(
            request=request,
            template_name='question_list.html',
            context={
                'testsuite': testsuite,
                'formset': formset
            },
        )

    def post(self, request, pk):
        testsuite = Test.objects.get(pk=pk)
        questions = Question.objects.filter(test_suite__id=pk)

        QuestionFormSet = modelformset_factory(
            model=Question,
            form=QuestionForm,
            extra=0,
            fields=('text', )
        )

        formset = QuestionFormSet(
            data=request.POST,
            queryset=questions
        )

        if formset.is_valid():
            instances = formset.save(commit=False)
            for instance in instances:
                instance.test_suite = testsuite
                instance.save()
        else:
            raise formset.forms.ValidationError(formset.errors)

        return redirect(reverse('test:edit', kwargs={'pk':pk}))
        # formset = QuestionFormSet(instance=self.request.POST)

        # print(formset)



# class QuestionView(View):
#
#     def get(self, request, pk, q_pk):
#         pass
#         # testsuite = TestSuite.objects.get(pk=pk)
#         # questions = Question.objects.filter(test_suite__id=pk)
#         #
#         # QuestionFormSet = modelformset_factory(Question,
#         #                                        extra=1,
#         #                                        fields=('text',))
#         #
#         # formset = QuestionFormSet(queryset=questions)
#         #
#         #
#         # return render(
#         #     request=request,
#         #     template_name='question_list.html',
#         #     context={
#         #         'testsuite': testsuite,
#         #         'formset': formset
#         #     },
#         # )
#
#     def post(self, request):
#         pass
#         # QuestionFormSet = modelformset_factory(Question,
#         #                                        extra=1,
#         #                                        fields=('text',))
#         #
#         # formset = QuestionFormSet(data=request.POST)
#         #
#         # if formset.is_valid():
#         #     formset.save()
#
#         # formset = QuestionFormSet(instance=self.request.POST)
#
#         # print(formset)



class StartTestView(View):

    def get(self, request, pk):
        testsuite = Test.objects.get(pk=pk)
        question = testsuite.questions.first()
        # question = Question.objects.get(pk=pk)

        QuestionFormSet = inlineformset_factory(
            parent_model=Question,
            model=Answer,
            extra=0,
            can_delete=False,
            fields=('text',)
        )

        formset = QuestionFormSet(instance=question)

        return render(
            request=request,
            template_name='question_edit.html',
            context={
                'question': question,
                'formset': formset
            },
        )

    def post(self, request, pk):
        QuestionFormSet = inlineformset_factory(Question, Answer, extra=1)

        formset = QuestionFormSet(instance=self.request.POST)

        print(formset)
