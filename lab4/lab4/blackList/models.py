from django.db import models


class ContactModel(models.Model):
	id = models.AutoField(primary_key=True)
	name = models.CharField(max_length=30)
	surname = models.CharField(max_length=30)
	date = models.DateTimeField(auto_created=True)
	telephone = models.CharField(max_length=30)
