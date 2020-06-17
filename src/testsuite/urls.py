from django.urls import path

from testsuite.views import TestSuiteListView, QuestionView, StartTestView, TestSuiteView

app_name = 'testsuite'

urlpatterns = [
    path('', TestSuiteListView.as_view(), name='list'),
    path('<int:pk>/', TestSuiteView.as_view(), name='edit'),
    path('<int:pk>/question/<int:q_pk>', QuestionView.as_view(), name='question'),
        path('<int:pk>/start', StartTestView.as_view(), name='start'),
]


