from django.urls import path

from testsuite.views import TestSuiteListView, TestRunView, StartTestView, LeaderBoardView

app_name = 'test'

urlpatterns = [
    path('', TestSuiteListView.as_view(), name='list'),

    path('<int:pk>/next', TestRunView.as_view(), name='next'),
    path('<int:pk>/start', StartTestView.as_view(), name='start'),
    path('leaderboard', LeaderBoardView.as_view(), name='leaderboard'),
]


