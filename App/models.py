from django.db import models

# Import Character Grader Module
import App.grader as grader

# Create your models here.
# class User(models.Model):
	
# 	username = models.CharField(max_length=30, unique=True)
# 	first_name = models.CharField(max_length=30, default='')
# 	last_name = models.CharField(max_length=30, default='')


class Character(models.Model):

	unicode_value = models.PositiveIntegerField(primary_key=True)
	unicode_block = models.CharField(max_length=50)
	unicode_display = models.CharField(max_length=1)
	unicode_description = models.CharField(max_length=50)
	points = models.TextField(default="[]")

	def __unicode__(self):
		return "UNICODE " + str(self.unicode_value) + " - " + self.unicode_block + " - " + self.unicode_description + " - '" + self.unicode_display + "'"


# class Exercise(models.Model):
	
# 	def key(self, filename):
# 		url = "user-submissions/%s-%s/%s" % (self.user.id, self.character.id, "character.png")
# 		return url

# 	def grade_submission(self):
# 		self.grade = grader.grade_character(self.user_submission)

# 	def submit(self, image):
# 		# TODO: Validate image input
# 		self.user_submission = image
# 		self.save()
	
# 	user_submission = models.ImageField(upload_to=key)
# 	timestamp = models.DateTimeField(auto_now=True)
# 	character = models.ForeignKey('Character')
# 	user = models.ForeignKey('User')
# 	grade = models.FloatField(default=0.0)