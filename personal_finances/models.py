from django.db import models
from django.contrib.auth.models import User


class PersonalFund(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    name = models.CharField(max_length=255)
    amount = models.FloatField()
    date = models.DateField()
    date_time = models.DateTimeField()
    depleted_date = models.DateField(null=True, blank=True)
    depleted_date_time = models.DateTimeField(null=True, blank=True)
    depleted = models.BooleanField(default=False)
    removed = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.name}'


class PersonalReceivedFund(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    name = models.CharField(max_length=255)
    amount = models.FloatField()
    date = models.DateField()
    fund = models.ForeignKey(PersonalFund, on_delete=models.PROTECT)
    date_time = models.DateTimeField()
    document = models.ImageField(null=True, blank=True, upload_to='funds/')
    removed = models.BooleanField(default=False)


class PersonalExpense(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name='personal_expense')
    name = models.CharField(max_length=255)
    amount = models.FloatField()
    date = models.DateField()
    date_time = models.DateTimeField()
    fund = models.ForeignKey(PersonalFund, on_delete=models.PROTECT)
    document = models.ImageField(null=True, blank=True, upload_to='expenses/')
    removed = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.name}'

    class Meta:
        ordering = ['-date_time']


class PersonalFundExpenditure(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    name = models.CharField(max_length=255)
    amount = models.FloatField()
    net_worth_amount = models.FloatField(default=0)
    expense = models.ForeignKey(PersonalExpense, on_delete=models.PROTECT)
    date = models.DateField()
    date_time = models.DateTimeField()
    removed = models.BooleanField(default=False)

    class Meta:
        ordering = ['-date_time']


class PersonalNetWorth(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    amount = models.FloatField(default=0)
    removed = models.BooleanField(default=False)


class PersonalFundAdded(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    fund = models.ForeignKey(PersonalFund, on_delete=models.PROTECT)
    net_worth_amount = models.FloatField(default=0)
    amount = models.FloatField()
    date = models.DateField()
    date_time = models.DateTimeField()
    removed = models.BooleanField(default=False)


class PersonalNetWorthFlow(models.Model):
    fund = models.ForeignKey(PersonalFund, on_delete=models.PROTECT, null=True, blank=True)
    expense = models.ForeignKey(PersonalExpense, on_delete=models.PROTECT, blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    amount = models.FloatField(default=0)
    amount_added = models.FloatField(default=0)
    date = models.DateField()
    date_time = models.DateTimeField()
    removed = models.BooleanField(default=False)


class RemovedPersonalFinanceData(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    name = models.CharField(max_length=255, null=True, blank=True)
    object_id = models.IntegerField()
    amount = models.FloatField(null=True, blank=True)
    date = models.DateField()
    date_time = models.DateTimeField()


class PersonalDebts(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    name = models.CharField(max_length=255)
    amount = models.FloatField()
    date = models.DateField()
    date_time = models.DateTimeField()
    paid = models.BooleanField(default=False)
    paid_amount = models.FloatField(null=True, blank=True)
    fund = models.ForeignKey(PersonalFund, null=True, blank=True, on_delete=models.PROTECT)
    date_paid = models.DateField(blank=True, null=True)
    date_time_paid = models.DateTimeField(blank=True, null=True)


class PersonalTransferMode(models.Model):
    name = models.CharField(max_length=100)
    removed = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class PersonalFundTransferred(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    receiver = models.ForeignKey(PersonalFund, related_name='fund_receiver', on_delete=models.PROTECT)
    sender = models.ForeignKey(PersonalFund, related_name='fund_sender', on_delete=models.PROTECT)
    amount = models.FloatField(default=0)
    date = models.DateField()
    date_time = models.DateTimeField()
    mode = models.ForeignKey(PersonalTransferMode, on_delete=models.PROTECT)
    removed = models.BooleanField(default=False)
