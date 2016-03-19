from __future__ import unicode_literals

from django.db import models

# Create your models here.
class Word(models.Model):
    word_content = models.CharField(max_length=20)
    word_type = models.CharField(max_length=10)
    def __unicode__(self):
        return self.word