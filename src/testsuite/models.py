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
    image = models.ImageField(default='default.jpg', upload_to='covers')

    def __str__(self):
        return f'{self.title}'

class Question(models.Model):
    test_suite = models.ForeignKey(to=TestSuite, related_name='questions', on_delete=models.CASCADE)
    text = models.CharField(max_length=64)
    description = models.TextField(max_length=512, null=True, blank=True)
    num_variant_min_limit = models.PositiveSmallIntegerField(
        name='Minimal number of variants',
        default=3,
        validators=[MinValueValidator(3),
                    MaxValueValidator(6)]
    )
    def __str__(self):
        return f'{self.text}'


class Variant(models.Model):
    text = models.CharField(max_length=64)
    question = models.ForeignKey(to=Question, related_name='variants', on_delete=models.CASCADE)
    correct = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.text}'


class TestSuiteRun(models.Model):
    STATE = (
        (1, 'New'),
        (2, 'Started'),
    )
    user = models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='test_suite_runs', on_delete=models.CASCADE)
    test_suite = models.ForeignKey(to=TestSuite, related_name='test_suite_runs', on_delete=models.CASCADE)
    datetime_run = models.DateTimeField(auto_now_add=True)#, default=datetime.now)
    is_completed = models.BooleanField(default=False)
    score = models.PositiveSmallIntegerField(default=0,
                                             validators=[MinValueValidator(0),
                                                         MaxValueValidator(100)])
    state = models.PositiveSmallIntegerField(choices=STATE, default=1)

    def __str__(self):
        return f'{self.test_suite.title}, {self.user.full_name()}, {self.datetime_run}'