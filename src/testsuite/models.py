from datetime import datetime
from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class TestSuite(models.Model):
    LEVEL_CHOICES = (
        (1, 'Basic'),
        (2, 'Middle'),
        (3, 'Advanced'),
    )
    title = models.CharField(max_length=64)
    description = models.TextField(max_length=1024, null=True, blank=True)
    level = models.PositiveSmallIntegerField(choices=LEVEL_CHOICES, default=2)


class Question(models.Model):
    test_suite = models.ForeignKey(to=TestSuite, related_name='questions', on_delete=models.CASCADE)
    text = models.CharField(max_length=64)
    description = models.TextField(max_length=512, null=True, blank=True)
    num_variant_limit = models.PositiveSmallIntegerField(validators=[MinValueValidator(3),
                                                                     MaxValueValidator(6)])


class Variant(models.Model):
    text = models.CharField(max_length=64)
    question = models.ForeignKey(to=Question, related_name='variants', on_delete=models.CASCADE)


class TestSuiteRun(models.Model):
    user = models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='test_suite_runs', on_delete=models.CASCADE)
    test_suite = models.ForeignKey(to=TestSuite, related_name='test_suite_runs', on_delete=models.CASCADE)
    datetime_run = models.DateTimeField(auto_now_add=True)#, default=datetime.now)
    is_completed = models.BooleanField(default=False)
    score = models.PositiveSmallIntegerField(validators=[MinValueValidator(0),
                                                         MaxValueValidator(100)])
