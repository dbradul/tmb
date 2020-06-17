from django.core.exceptions import ValidationError
from django.forms import inlineformset_factory, formset_factory, modelformset_factory
from django.shortcuts import render, redirect

# Create your views here.
from django.urls import reverse
from django.views.generic import ListView, UpdateView
from django.views.generic.base import View

from account.models import User
from testsuite.forms import QuestionEditForm
from testsuite.models import TestSuite, Question, Variant


class TestSuiteListView(ListView):
    model = TestSuite
    # filterset_class = StudentListFilter
    template_name = 'testsuite_list.html'
    # context_object_name = 'students_list'
    # login_url = reverse_lazy('login')
    paginate_by = 5

    # def get_queryset(self):
    #     request = self.request
    #     qs = super().get_queryset()
    #     qs = qs.select_related('group')
    #     qs = qs.order_by('-id')
    #
    #     if request.GET.get('fname'):
    #         qs = qs.filter(
    #             Q(first_name=request.GET.get('fname'))
    #         )
    #     return qs

    # def get_context_data(self, *args, **kwargs):
    #     from urllib.parse import urlencode
    #     context = super().get_context_data(*args, **kwargs)
    #
    #     query_params = copy.deepcopy(self.request.GET)
    #     if 'page' in query_params:
    #         del query_params['page']
    #     context['query_params'] = urlencode(query_params)
    #
    #     return context


class LeaderBoardView(ListView):
    model = User
    paginate_by = 5


class TestSuiteView(View):

    def get(self, request, pk):
        testsuite = TestSuite.objects.get(pk=pk)
        questions = Question.objects.filter(test_suite__id=pk)

        QuestionFormSet = modelformset_factory(
            model=Question,
            form=QuestionEditForm,
            extra=1,
            fields=('text', 'num_variant_min_limit')
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
        testsuite = TestSuite.objects.get(pk=pk)
        questions = Question.objects.filter(test_suite__id=pk)

        QuestionFormSet = modelformset_factory(
            model=Question,
            form=QuestionEditForm,
            extra=0,
            fields=('text', 'num_variant_min_limit')
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

        return redirect(reverse('testsuite:edit', kwargs={'pk':pk}))
        # formset = QuestionFormSet(instance=self.request.POST)

        # print(formset)



class QuestionView(View):

    def get(self, request, pk, q_pk):
        pass
        # testsuite = TestSuite.objects.get(pk=pk)
        # questions = Question.objects.filter(test_suite__id=pk)
        #
        # QuestionFormSet = modelformset_factory(Question,
        #                                        extra=1,
        #                                        fields=('text',))
        #
        # formset = QuestionFormSet(queryset=questions)
        #
        #
        # return render(
        #     request=request,
        #     template_name='question_list.html',
        #     context={
        #         'testsuite': testsuite,
        #         'formset': formset
        #     },
        # )

    def post(self, request):
        pass
        # QuestionFormSet = modelformset_factory(Question,
        #                                        extra=1,
        #                                        fields=('text',))
        #
        # formset = QuestionFormSet(data=request.POST)
        #
        # if formset.is_valid():
        #     formset.save()

        # formset = QuestionFormSet(instance=self.request.POST)

        # print(formset)



class StartTestView(View):

    def get(self, request, pk):
        testsuite = TestSuite.objects.get(pk=pk)
        question = testsuite.questions.first()
        # question = Question.objects.get(pk=pk)

        QuestionFormSet = inlineformset_factory(
            parent_model=Question,
            model=Variant,
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

    def post(self):
        QuestionFormSet = inlineformset_factory(Question, Variant, extra=1)

        formset = QuestionFormSet(instance=self.request.POST)

        print(formset)
