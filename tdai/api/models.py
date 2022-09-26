# from django.db import models


# # Create your models here.
# class Bot(models.Model):
#     name = models.CharField(max_length=200)
#     description = models.CharField(max_length=200)
#     created_time = models.DateTimeField(auto_now=True)
#     updated_time = models.DateTimeField(auto_now=True)

#     def __str__(self):
#         return self.name

#     class Meta:
#         ordering = ['created_time']


# class Intent(models.Model):
#     bot = models.ForeignKey(Bot, on_delete=models.CASCADE)
#     intent = models.CharField(max_length=200)
#     description = models.CharField(max_length=200)
#     created_time = models.DateTimeField(auto_now=True)
#     updated_time = models.DateTimeField(auto_now=True)

#     def __str__(self):
#         return self.intent

#     class Meta:
#         ordering = ['created_time']


# class Sentence(models.Model):
#     bot = models.ForeignKey(Bot, on_delete=models.CASCADE)
#     intent = models.ForeignKey(Intent, on_delete=models.SET_NULL, null=True)
#     sentence = models.CharField(max_length=200)
#     created_time = models.DateTimeField(auto_now=True)
#     updated_time = models.DateTimeField(auto_now=True)

#     def __str__(self):
#         return self.sentence

#     class Meta:
#         ordering = ['created_time']


# class Entity(models.Model):
#     bot = models.ForeignKey(Bot, on_delete=models.CASCADE)
#     entity = models.CharField(max_length=200)
#     description = models.CharField(max_length=200)
#     created_time = models.DateTimeField(auto_now=True)
#     updated_time = models.DateTimeField(auto_now=True)

#     def __str__(self):
#         return self.entity

#     class Meta:
#         ordering = ['created_time']


# class KeyWord(models.Model):
#     bot = models.ForeignKey(Bot, on_delete=models.CASCADE)
#     entity = models.ForeignKey(Entity, on_delete=models.CASCADE, null=True)
#     keyword = models.CharField(max_length=200)
#     synonym = models.CharField(max_length=200)
#     created_time = models.DateTimeField(auto_now=True)
#     updated_time = models.DateTimeField(auto_now=True)

#     def __str__(self):
#         return self.keyword

#     class Meta:
#         ordering = ['created_time']


# class Dictionary(models.Model):
#     bot = models.ForeignKey(Bot, on_delete=models.CASCADE)
#     word = models.CharField(max_length=200)
#     synonym = models.CharField(max_length=200)
#     created_time = models.DateTimeField(auto_now=True)
#     updated_time = models.DateTimeField(auto_now=True)

#     class Meta:
#         ordering = ['created_time']


# class IntentModel(models.Model):
#     bot = models.ForeignKey(Bot, on_delete=models.CASCADE)
#     data = models.BinaryField()
#     created_time = models.DateTimeField(auto_now=True)
#     updated_time = models.DateTimeField(auto_now=True)


# class EntityModel(models.Model):
#     bot = models.ForeignKey(Bot, on_delete=models.CASCADE)
#     data = models.BinaryField()
#     created_time = models.DateTimeField(auto_now=True)
#     updated_time = models.DateTimeField(auto_now=True)


# class Scenario(models.Model):
#     bot = models.ForeignKey(Bot, on_delete=models.CASCADE, default=1)
#     name = models.CharField(max_length=200, null=True)
#     position = models.IntegerField(null=True)
#     created_time = models.DateTimeField(auto_now=True)
#     updated_time = models.DateTimeField(auto_now=True)


# class Step(models.Model):
#     scenario = models.ForeignKey(Scenario, on_delete=models.CASCADE, default=1)
#     name = models.CharField(max_length=200, null=True)
#     position = models.IntegerField(null=True)
#     created_time = models.DateTimeField(auto_now=True)
#     updated_time = models.DateTimeField(auto_now=True)


# class Card(models.Model):
#     step = models.ForeignKey(Step, on_delete=models.CASCADE, default=1)
#     name = models.CharField(max_length=200, null=True)
#     card_type = models.CharField(max_length=200, null=True)
#     config = models.CharField(max_length=2000, null=True)
#     position = models.IntegerField(null=True)
#     created_time = models.DateTimeField(auto_now=True)
#     updated_time = models.DateTimeField(auto_now=True)


# class Variable(models.Model):
#     name = models.CharField(max_length=200, null=True)
#     variable_type = models.CharField(max_length=200, null=True)
#     created_time = models.DateTimeField(auto_now=True)
#     updated_time = models.DateTimeField(auto_now=True)


# class HistoryUsedIntent(models.Model):
#     step = models.ForeignKey(Step, on_delete=models.CASCADE)
#     intent = models.ForeignKey(Intent, on_delete=models.CASCADE)


# class RequireVariables(models.Model):
#     step = models.ForeignKey(Step, on_delete=models.CASCADE, null=True)
#     variable = models.ForeignKey(Variable, on_delete=models.CASCADE, null=True)


# class HistoryChat(models.Model):
#     step = models.ForeignKey(Step, on_delete=models.CASCADE, null=True)
#     variable = models.ForeignKey(Variable, on_delete=models.CASCADE, null=True)
#     user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
#     value = models.CharField(max_length=1000, null=True)
