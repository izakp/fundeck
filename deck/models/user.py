from django.db import models

class User(models.Model):
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

  name = models.CharField(max_length=128)
  email = models.EmailField()

  def __unicode__(self):
    return self.email

  def __str__(self):
    return self.email
