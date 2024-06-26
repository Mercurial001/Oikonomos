from django.contrib import admin
from .models import PersonalReceivedFund
from .models import PersonalFund
from .models import PersonalExpense
from .models import PersonalFundExpenditure
from .models import PersonalNetWorth


class PersonalReceivedFundAdmin(admin.ModelAdmin):
    list_display = ('user', 'name', 'amount')


class PersonalFundAdmin(admin.ModelAdmin):
    list_display = ('user', 'amount', 'name', 'date')


class PersonalExpenseAdmin(admin.ModelAdmin):
    list_display = ('user', 'amount', 'name', 'date')


class PersonalFundExpenditureAdmin(admin.ModelAdmin):
    list_display = ('user', 'amount', 'name', 'date')


class PersonalNetWorthAdmin(admin.ModelAdmin):
    list_display = ('user', 'amount')


admin.site.register(PersonalReceivedFund, PersonalReceivedFundAdmin)
admin.site.register(PersonalFund, PersonalFundAdmin)
admin.site.register(PersonalExpense, PersonalExpenseAdmin)
admin.site.register(PersonalFundExpenditure, PersonalFundExpenditureAdmin)
admin.site.register(PersonalNetWorth, PersonalNetWorthAdmin)
