from django.db import models


class TestModel(models.Model):
	field_1 = models.CharField(max_length=100)
	field_2 = models.CharField(max_length=100)
	field_3 = models.CharField(max_length=100)
	field_4 = models.CharField(max_length=100)
	field_5 = models.CharField(max_length=100)
