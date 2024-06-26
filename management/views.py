from django.shortcuts import render, redirect
from .models import *
from django.utils import timezone
from django.http import HttpResponseRedirect


def index(request):
    funds = Fund.objects.all()
    expenses = Expense.objects.all()
    received_funds = FundReceived.objects.all()
    fund_expenditures = FundExpenditure.objects.all()
    net_balance, net_balance_created = NetWorth.objects.get_or_create(id=1)
    net_balance.save()

    if request.method == 'POST':
        if 'add-fund-btn' in request.POST:
            fund_name = request.POST.get('fund-name')
            fund_amount = request.POST.get('fund-amount')
            fund_document = request.FILES.get('fund-document')

            balance, balance_created = NetWorth.objects.get_or_create(id=1)
            balance.amount += float(fund_amount)
            balance.save()

            fund, created = Fund.objects.get_or_create(
                name=fund_name,
                amount=float(fund_amount),
                date=timezone.now().date(),
                date_time=timezone.now(),
            )
            fund.save()

            fund_received, fund_received_created = FundReceived.objects.get_or_create(
                name=fund_name,
                amount=float(fund_amount),
                date=timezone.now().date(),
                date_time=timezone.now(),
                document=fund_document,
            )

            fund_received.save()

            http_referrer = request.META.get('HTTP_REFERER')

            if http_referrer:
                return HttpResponseRedirect(http_referrer)
            else:
                return redirect('homepage')

        elif 'add-expense-btn' in request.POST:
            expense_fund_id = request.POST.get('expense-fund')
            expense_name = request.POST.get('expense-name')
            expense_amount = request.POST.get('expense-amount')
            expense_document = request.FILES.get('expense-document')

            balance, balance_created = NetWorth.objects.get_or_create(id=1)
            balance.amount -= float(expense_amount)
            balance.save()

            expense_fund = Fund.objects.get(id=expense_fund_id)
            expense_fund.amount -= float(expense_amount)
            expense_fund.save()

            expense, created_expense = Expense.objects.get_or_create(
                personnel=request.user,
                name=expense_name,
                amount=float(expense_amount),
                date=timezone.now().date(),
                date_time=timezone.now(),
                document=expense_document,
                fund=expense_fund,
            )

            expense.save()

            fund_expenditure, fund_expenditure_created = FundExpenditure.objects.get_or_create(
                name=expense_name,
                amount=expense_fund.amount,
                expense=expense,
                date=timezone.now().date(),
                date_time=timezone.now(),
            )

            fund_expenditure.save()

            http_referrer = request.META.get('HTTP_REFERER')
            if http_referrer:
                return HttpResponseRedirect(http_referrer)
            else:
                return redirect('homepage')

    return render(request, 'base.html', {
        'funds': funds,
        'expenses': expenses,
        'received_funds': received_funds,
        'fund_expenditures': fund_expenditures,
        'net_balance': net_balance,
    })
