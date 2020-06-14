from django.shortcuts import render

# Create your views here.
from django.views.generic import ListView

from account.models import User
from testsuite.models import TestSuite


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
