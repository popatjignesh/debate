from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class Discussion(models.Model):
	types = (
		('article','Article'),
		('question','Question'),
		('post','Post'),
		('blog','Blog'),
		)

	title = models.CharField(max_length = 50)
	text = models.TextField(null=True, blank=True)
	title_type = models.CharField(choices=types, max_length = 10)
	added_by = models.ForeignKey(User)
	is_published = models.BooleanField(default=True)
	created_date = models.DateTimeField(auto_now_add=True)
	modified_date = models.DateTimeField(auto_now=True)
	image = models.ImageField(upload_to = 'discussion/', null=True, blank=True)

	class Meta:
		verbose_name = "Discussion"
		verbose_name_plural = "Discussion"

	def __str__(self):
		return self.title

class Comment(models.Model):
	discussion = models.ForeignKey(Discussion, related_name='comments')
	text = models.TextField(null=True, blank=True)
	added_by = models.ForeignKey(User)
	created_date = models.DateTimeField(auto_now_add=True)
	modified_date = models.DateTimeField(auto_now=True)

	class Meta:
		verbose_name = "Comment"
		verbose_name_plural = "Comment"

	def __str__(self):
		return self.text
