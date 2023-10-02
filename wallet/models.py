from django.db import models


class Transaction(models.Model):
    category = models.CharField(max_length=50)
    amount = models.IntegerField()
    detail = models.CharField(max_length=200)
    date_created = models.DateField()

    def __str__(self):
        return self.category
