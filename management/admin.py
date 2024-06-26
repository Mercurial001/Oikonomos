from django.contrib import admin
from .models import Expense
from .models import FundReceived
from .models import Fund
from .models import FundExpenditure
from .models import NetWorth


class ExpenseAdmin(admin.ModelAdmin):
    list_display = ('personnel', 'amount', 'name')


class FundReceivedAdmin(admin.ModelAdmin):
    list_display = ('name', 'amount')


class FundAdmin(admin.ModelAdmin):
    list_display = ('name', 'amount', 'depleted')


class FundExpenditureAdmin(admin.ModelAdmin):
    list_display = ('name', 'amount', 'expense')


class NetWorthAdmin(admin.ModelAdmin):
    list_display = ('amount',)


admin.site.register(Expense, ExpenseAdmin)
admin.site.register(FundReceived, FundReceivedAdmin)
admin.site.register(Fund, FundAdmin)
admin.site.register(FundExpenditure, FundExpenditureAdmin)
admin.site.register(NetWorth, NetWorthAdmin)
