from django.db import models

class User(models.Model):
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

  name = models.CharField(max_length=128)
  email = models.EmailField()
  password = models.CharField(max_length=128)

  def __unicode__(self):
    return self.name

  def __str__(self):
    return self.name
