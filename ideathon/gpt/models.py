from django.db import models

class GptAnswer(models.Model):
    content = models.TextField()  

    def __str__(self):
        return self.content  

class Character(models.Model):
    character_name = models.CharField(max_length=100)
    tone = models.CharField(max_length=100)
    text_length = models.IntegerField()
    situation = models.CharField()
    language = models.CharField(max_length=100)

    def __str__(self):
        return self.character_name