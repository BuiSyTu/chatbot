# pylint: disable=missing-module-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=missing-function-docstring
from django.db import models


# Create your models here.
class User(models.Model):
    username = models.CharField(max_length=200)
    password = models.CharField(max_length=200)
    email = models.CharField(max_length=200)
    created_time = models.DateTimeField(auto_now=True)
    updated_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.username)

    class Meta:
        ordering = ['created_time']


class Bot(models.Model):
    user = models.ForeignKey(User, null=True, blank=True, on_delete=None)
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=200)
    created_time = models.DateTimeField(auto_now=True)
    updated_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.name)

    class Meta:
        ordering = ['created_time']


class Intent(models.Model):
    bot = models.ForeignKey(Bot, null=True, blank=True, on_delete=None)
    intent = models.CharField(max_length=200)
    description = models.CharField(max_length=200)
    created_time = models.DateTimeField(auto_now=True)
    updated_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.intent)

    class Meta:
        ordering = ['created_time']


class Sentence(models.Model):
    bot = models.ForeignKey(Bot, null=True, blank=True, on_delete=None)
    intent = models.ForeignKey(Intent, on_delete=models.SET_NULL, null=True, blank=True)
    sentence = models.CharField(max_length=200)
    created_time = models.DateTimeField(auto_now=True)
    updated_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.sentence)

    class Meta:
        ordering = ['created_time']


class Entity(models.Model):
    bot = models.ForeignKey(Bot, null=True, blank=True, on_delete=None)
    entity = models.CharField(max_length=200)
    description = models.CharField(max_length=200)
    created_time = models.DateTimeField(auto_now=True)
    updated_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.entity)

    class Meta:
        ordering = ['created_time']


class KeyWord(models.Model):
    bot = models.ForeignKey(Bot, null=True, blank=True, on_delete=None)
    entity = models.ForeignKey(Entity, null=True, blank=True, on_delete=None)
    keyword = models.CharField(max_length=200)
    synonym = models.CharField(max_length=200)
    created_time = models.DateTimeField(auto_now=True)
    updated_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.keyword)

    class Meta:
        ordering = ['created_time']


class Dictionary(models.Model):
    bot = models.ForeignKey(Bot, null=True, blank=True, on_delete=None)
    word = models.CharField(max_length=200)
    synonym = models.CharField(max_length=200)
    created_time = models.DateTimeField(auto_now=True)
    updated_time = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['created_time']


class IntentModel(models.Model):
    bot = models.ForeignKey(Bot, null=True, blank=True, on_delete=None)
    data = models.BinaryField()
    created_time = models.DateTimeField(auto_now=True)
    updated_time = models.DateTimeField(auto_now=True)


class EntityModel(models.Model):
    bot = models.ForeignKey(Bot, null=True, blank=True, on_delete=None)
    data = models.BinaryField()
    created_time = models.DateTimeField(auto_now=True)
    updated_time = models.DateTimeField(auto_now=True)


class Scenario(models.Model):
    bot = models.ForeignKey(Bot, null=True, blank=True, on_delete=None)
    name = models.CharField(max_length=200, null=True, blank=True)
    position = models.IntegerField(null=True, blank=True)
    created_time = models.DateTimeField(auto_now=True)
    updated_time = models.DateTimeField(auto_now=True)


class Step(models.Model):
    scenario = models.ForeignKey(Scenario, null=True, blank=True, on_delete=None)
    name = models.CharField(max_length=200, null=True, blank=True)
    position = models.IntegerField(null=True, blank=True)
    created_time = models.DateTimeField(auto_now=True)
    updated_time = models.DateTimeField(auto_now=True)


class Card(models.Model):
    step = models.ForeignKey(Step, null=True, blank=True, on_delete=None)
    name = models.CharField(max_length=200, null=True, blank=True)
    card_type = models.CharField(max_length=200, null=True, blank=True)
    config = models.CharField(max_length=2000, null=True, blank=True)
    position = models.IntegerField(null=True, blank=True)
    created_time = models.DateTimeField(auto_now=True)
    updated_time = models.DateTimeField(auto_now=True)


class Variable(models.Model):
    name = models.CharField(max_length=200, null=True, blank=True)
    variable_type = models.CharField(max_length=200, null=True, blank=True)
    created_time = models.DateTimeField(auto_now=True)
    updated_time = models.DateTimeField(auto_now=True)


class HistoryUsedIntent(models.Model):
    step = models.ForeignKey(Step, on_delete=None)
    intent = models.ForeignKey(Intent, on_delete=None)


class RequireVariables(models.Model):
    step = models.ForeignKey(Step, null=True, blank=True, on_delete=None)
    variable = models.ForeignKey(Variable, null=True, blank=True, on_delete=None)


class HistoryChat(models.Model):
    step = models.ForeignKey(Step, null=True, blank=True, on_delete=None)
    variable = models.ForeignKey(Variable, null=True, blank=True, on_delete=None)
    # user = models.ForeignKey(User, null=True, blank=True, on_delete=None)
    user_name = models.CharField(max_length=1000, null=True, blank=True)
    value = models.CharField(max_length=1000, null=True, blank=True)
