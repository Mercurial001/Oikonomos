from django.contrib import admin
from .models import models
from .models import Expense
from .models import FundReceived
from .models import Fund
from .models import FundExpenditure
from .models import NetWorth
from .models import PrivacyPolicy
from .models import TermsOfService
from .models import About
from ckeditor.widgets import CKEditorWidget


class AboutAdmin(admin.ModelAdmin):
    list_display = ('name', 'date')
    formfield_overrides = {
        models.TextField: {'widget': CKEditorWidget}
    }


class TermsOfServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'date_updated')
    formfield_overrides = {
        models.TextField: {'widget': CKEditorWidget}
    }


class PrivacyPolicyAdmin(admin.ModelAdmin):
    list_display = ('name',)
    formfield_overrides = {
        models.TextField: {'widget': CKEditorWidget}
    }


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


admin.site.register(About, AboutAdmin)
admin.site.register(TermsOfService, TermsOfServiceAdmin)
admin.site.register(PrivacyPolicy, PrivacyPolicyAdmin)
admin.site.register(Expense, ExpenseAdmin)
admin.site.register(FundReceived, FundReceivedAdmin)
admin.site.register(Fund, FundAdmin)
admin.site.register(FundExpenditure, FundExpenditureAdmin)
admin.site.register(NetWorth, NetWorthAdmin)
