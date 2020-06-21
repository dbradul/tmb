from django.urls import path

from testsuite.views import TestSuiteListView, TestRunView, StartTestView

app_name = 'test'

urlpatterns = [
    path('', TestSuiteListView.as_view(), name='list'),
    path('<int:pk>/question/<int:seq_nr>', TestRunView.as_view(), name='testrun_step'),
    path('<int:pk>/start', StartTestView.as_view(), name='start'),
]


