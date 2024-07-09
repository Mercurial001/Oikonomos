from django.db import models
from django.contrib.auth.models import User


class FundReceived(models.Model):
    name = models.CharField(max_length=255)
    amount = models.IntegerField()
    date = models.DateField()
    date_time = models.DateTimeField()
    document = models.ImageField(null=True, blank=True, upload_to='funds/')
    removed = models.BooleanField(default=False)


class Fund(models.Model):
    name = models.CharField(max_length=255)
    amount = models.IntegerField()
    date = models.DateField()
    date_time = models.DateTimeField()
    depleted_date = models.DateField(null=True, blank=True)
    depleted_date_time = models.DateTimeField(null=True, blank=True)
    depleted = models.BooleanField(default=False)


class Expense(models.Model):
    personnel = models.ForeignKey(User, on_delete=models.PROTECT)
    name = models.CharField(max_length=255)
    amount = models.IntegerField()
    date = models.DateField()
    date_time = models.DateTimeField()
    fund = models.ForeignKey(Fund, on_delete=models.PROTECT)
    document = models.ImageField(null=True, blank=True, upload_to='expenses/')
    removed = models.BooleanField(default=False)


class FundExpenditure(models.Model):
    name = models.CharField(max_length=255)
    amount = models.IntegerField()
    expense = models.ForeignKey(Expense, on_delete=models.PROTECT)
    date = models.DateField()
    date_time = models.DateTimeField()
    removed = models.BooleanField(default=False)


class NetWorth(models.Model):
    amount = models.IntegerField(default=0)


class PrivacyPolicy(models.Model):
    name = models.CharField(max_length=100)
    statement = models.TextField()
    date = models.DateField()
    date_time = models.DateTimeField()
    date_updated = models.DateField()
    date_time_updated = models.DateTimeField()


class TermsOfService(models.Model):
    name = models.CharField(max_length=100)
    statement = models.TextField()
    date_updated = models.DateField()
    date_time_updated = models.DateTimeField()


class About(models.Model):
    name = models.CharField(max_length=100)
    statement = models.TextField()
    date = models.DateField()
    date_time = models.DateTimeField()
