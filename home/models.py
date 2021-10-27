from django.db import models
from django.utils.timezone import now
from users.models import User


class Post(models.Model):
	sno = models.AutoField(primary_key=True)
	username = models.CharField(max_length=50) 
	likes = models.CharField(max_length=999999999999999999999999, default=0)
	comments = models.TextField(default="")
	replies = models.TextField(default="")
	image = models.ImageField(upload_to="home/images", default="")
	caption = models.CharField(max_length=200)
	pub_date = models.DateTimeField(default=now)

	def __str__(self):
		return self.username