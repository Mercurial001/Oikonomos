from django.db import models
from django.contrib.auth.models import User


class PersonalReceivedFund(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    name = models.CharField(max_length=255)
    amount = models.IntegerField()
    date = models.DateField()
    date_time = models.DateTimeField()
    document = models.ImageField(null=True, blank=True, upload_to='funds/')


class PersonalFund(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    name = models.CharField(max_length=255)
    amount = models.IntegerField()
    date = models.DateField()
    date_time = models.DateTimeField()
    depleted_date = models.DateField(null=True, blank=True)
    depleted_date_time = models.DateTimeField(null=True, blank=True)
    depleted = models.BooleanField(default=False)


class PersonalExpense(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name='personal_expense')
    name = models.CharField(max_length=255)
    amount = models.IntegerField()
    date = models.DateField()
    date_time = models.DateTimeField()
    fund = models.ForeignKey(PersonalFund, on_delete=models.PROTECT)
    document = models.ImageField(null=True, blank=True, upload_to='expenses/')


class PersonalFundExpenditure(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    name = models.CharField(max_length=255)
    amount = models.IntegerField()
    expense = models.ForeignKey(PersonalExpense, on_delete=models.PROTECT)
    date = models.DateField()
    date_time = models.DateTimeField()


class PersonalNetWorth(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    amount = models.IntegerField(default=0)
