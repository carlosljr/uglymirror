# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.core.urlresolvers import reverse
from django.conf import settings
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from fernet_fields import EncryptedTextField, EncryptedCharField, EncryptedIntegerField, EncryptedDateTimeField

# Create your models here.

class Profile(models.Model):
  user = models.OneToOneField(User, on_delete=models.CASCADE)
  email_confirmed = models.BooleanField(default=False)

@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
  if created:
    Profile.objects.create(user=instance)
  instance.profile.save()

class UglyMirror(models.Model):
  user = models.ForeignKey(User)
  # age = models.IntegerField(help_text='Age of my ugliness')
  age = EncryptedIntegerField(help_text='Age of my ugliness')
  # ugly_rate = models.IntegerField(help_text='How ugly am I? (1 - Not so ugly / 99999999 - Monster level)')
  ugly_rate = EncryptedIntegerField(help_text='How ugly am I? (1 - Not so ugly / 99999999 - Monster level)')
  # feeling = models.TextField(help_text='How am I feeling today?')
  feeling = EncryptedTextField(help_text='How am I feeling today?')
  # interface_compare = models.CharField(max_length=200, help_text='Am I more ugly than this interface?')
  interface_compare = EncryptedCharField(max_length=200, help_text='Am I uglier than this interface? (Yes/No/A little/A lot)')
  # date = models.DateTimeField(auto_now_add=True)
  date = EncryptedDateTimeField(auto_now_add=True)

  def __unicode__(self):
    return self.date

  def get_absolute_url(self):
    return reverse('ugly_edit', kwargs={'pk': self.pk})


