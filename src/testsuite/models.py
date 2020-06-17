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
    image = models.ImageField(default='default.png', upload_to='covers')

    def __str__(self):
        return f'{self.title}'


class Question(models.Model):
    MIN_LIMIT = 3
    MAX_LIMIT = 6

    test_suite = models.ForeignKey(to=TestSuite, related_name='questions', on_delete=models.CASCADE)
    text = models.CharField(max_length=64)
    description = models.TextField(max_length=512, null=True, blank=True)

    def __str__(self):
        return f'{self.text}'

    def next(self):
        return 'next'

    def prev(self):
        return 'prev'


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
    datetime_run = models.DateTimeField(auto_now_add=True)
    is_completed = models.BooleanField(default=False)
    score = models.PositiveSmallIntegerField(default=0,
                                             validators=[MinValueValidator(0),
                                                         MaxValueValidator(100)])
    state = models.PositiveSmallIntegerField(choices=STATE, default=1)

    def __str__(self):
        return f'{self.test_suite.title}, {self.user.full_name()}, {self.datetime_run}'


class TestSuiteRunDetails(models.Model):
    test_suite_run = models.ForeignKey(to=TestSuiteRun, related_name='details', on_delete=models.CASCADE)
    question = models.ForeignKey(to=Question, on_delete=models.CASCADE)
    variant = models.ForeignKey(to=Variant, related_name='results', on_delete=models.CASCADE)
    success = models.BooleanField(default=False)

    def __str__(self):
        return f'Test Run: {self.test_suite_run.id}, Question: {self.question.text}, Success: {self.success}'