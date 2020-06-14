from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static

from testsuite.views import TestSuiteListView

app_name = 'testsuite'

urlpatterns = [
    path('', TestSuiteListView.as_view(), name='list'),
]

