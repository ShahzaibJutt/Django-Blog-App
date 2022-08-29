from argparse import ONE_OR_MORE
from time import time
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from blog_website import settings

# Create your models here.

class Post(models.Model):
	title = models.CharField(max_length=100)
	content = models.TextField()
	date_posted = models.DateTimeField(default=timezone.now)
	author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	
	def __str__(self):
		return self.title

	def get_absolute_url(self):
		return reverse('post-detail',kwargs={'pk': self.pk})