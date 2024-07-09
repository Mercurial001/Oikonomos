from django.contrib import admin
from .models import PersonalReceivedFund
from .models import PersonalFund
from .models import PersonalExpense
from .models import PersonalFundExpenditure
from .models import PersonalNetWorth
from .models import PersonalFundAdded
from .models import RemovedPersonalFinanceData
from .models import PersonalDebts
from .models import PersonalNetWorthFlow
from .models import PersonalTransferMode
from .models import PersonalFundTransferred


class PersonalTransferModeAdmin(admin.ModelAdmin):
    list_display = ('name', 'removed')


class PersonalFundTransferredAdmin(admin.ModelAdmin):
    list_display = ('user', 'receiver', 'sender', 'amount', 'date')


class PersonalNetWorthFlowAdmin(admin.ModelAdmin):
    list_display = ('user', 'amount', 'date', 'date_time', 'removed')


class PersonalFundAddedAdmin(admin.ModelAdmin):
    list_display = ('user',)


class RemovedPersonalFinanceDataAdmin(admin.ModelAdmin):
    list_display = ('user',)


class PersonalDebtsAdmin(admin.ModelAdmin):
    list_display = ('user',)


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


admin.site.register(PersonalTransferMode, PersonalTransferModeAdmin)
admin.site.register(PersonalFundTransferred, PersonalFundTransferredAdmin)
admin.site.register(PersonalNetWorthFlow, PersonalNetWorthFlowAdmin)
admin.site.register(PersonalFundAdded, PersonalFundAddedAdmin)
admin.site.register(RemovedPersonalFinanceData, RemovedPersonalFinanceDataAdmin)
admin.site.register(PersonalDebts, PersonalDebtsAdmin)
admin.site.register(PersonalReceivedFund, PersonalReceivedFundAdmin)
admin.site.register(PersonalFund, PersonalFundAdmin)
admin.site.register(PersonalExpense, PersonalExpenseAdmin)
admin.site.register(PersonalFundExpenditure, PersonalFundExpenditureAdmin)
admin.site.register(PersonalNetWorth, PersonalNetWorthAdmin)
