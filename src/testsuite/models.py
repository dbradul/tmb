from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

class Topic(models.Model):

    name = models.CharField(max_length=64)

    def __str__(self):
        return f'{self.name}'


class Test(models.Model):
    LEVEL_CHOICES = (
        (1, 'Basic'),
        (2, 'Middle'),
        (3, 'Advanced'),
    )

    topic = models.ForeignKey(to=Topic, related_name='tests', null=True, on_delete=models.SET_NULL)
    title = models.CharField(max_length=64)
    description = models.TextField(max_length=1024, null=True, blank=True)
    level = models.PositiveSmallIntegerField(choices=LEVEL_CHOICES, default=2)
    image = models.ImageField(default='default.png', upload_to='covers')

    def __str__(self):
        return f'{self.title}'


class Question(models.Model):
    MIN_LIMIT = 3
    MAX_LIMIT = 6

    test = models.ForeignKey(to=Test, related_name='questions', on_delete=models.CASCADE)
    number = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(MAX_LIMIT)])
    text = models.CharField(max_length=64)
    description = models.TextField(max_length=512, null=True, blank=True)

    def __str__(self):
        return f'{self.text}'



class Answer(models.Model):
    text = models.CharField(max_length=64)
    question = models.ForeignKey(to=Question, related_name='answers', on_delete=models.CASCADE)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.text}'


class TestRun(models.Model):
    STATE = (
        (1, 'New'),
        (2, 'Started'),
    )
    user = models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='test_suite_runs', on_delete=models.CASCADE)
    test_suite = models.ForeignKey(to=Test, related_name='test_suite_runs', on_delete=models.CASCADE)
    datetime_run = models.DateTimeField(auto_now_add=True)
    is_completed = models.BooleanField(default=False)
    score = models.PositiveSmallIntegerField(default=0,
                                             validators=[MinValueValidator(0),
                                                         MaxValueValidator(100)])
    state = models.PositiveSmallIntegerField(choices=STATE, default=1)

    def __str__(self):
        return f'{self.test_suite.title}, {self.user.full_name()}, {self.datetime_run}'


class TestRunDetail(models.Model):
    test_suite_run = models.ForeignKey(to=TestRun, related_name='details', on_delete=models.CASCADE)
    question = models.ForeignKey(to=Question, null=True, blank=True, on_delete=models.CASCADE)
    answer = models.ForeignKey(to=Answer, related_name='results', on_delete=models.CASCADE)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return f'Test Run: {self.test_suite_run.id}, Question: {self.question.text}, Success: {self.success}'