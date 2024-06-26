from django.shortcuts import render, redirect
from .models import *
from django.utils import timezone
from django.http import HttpResponseRedirect


def index(request, username):
    user = User.objects.get(
        username=username
    )
    personal_funds = PersonalFund.objects.filter(user=user)
    personal_received_funds = PersonalReceivedFund.objects.filter(user=user)
    personal_expenses = PersonalExpense.objects.filter(user=user)
    personal_expense_funds = PersonalFundExpenditure.objects.filter(user=user)
    personal_net_worth, personal_net_worth_created = PersonalNetWorth.objects.get_or_create(
        id=1,
        user=user,
    )
    personal_net_worth.save()

    if request.method == 'POST':
        if 'add-personal-fund-btn' in request.POST:
            personal_fund_name = request.POST.get('personal-fund-name')
            personal_fund_amount = request.POST.get('personal-fund-amount')
            personal_fund_document = request.FILES.get('personal-fund-document')

            net_worth, created_net_worth = PersonalNetWorth.objects.get_or_create(
                id=1
            )
            net_worth.amount += float(personal_fund_amount)
            net_worth.save()

            personal_fund, personal_fund_created = PersonalFund.objects.get_or_create(
                user=request.user,
                name=personal_fund_name,
                amount=float(personal_fund_amount),
                date=timezone.now().date(),
                date_time=timezone.now(),
            )
            personal_fund.save()

            personal_received_fund, personal_received_fund_created = PersonalReceivedFund.objects.get_or_create(
                user=request.user,
                name=personal_fund_name,
                amount=float(personal_fund_amount),
                date=timezone.now().date(),
                date_time=timezone.now(),
                document=personal_fund_document,
            )
            personal_received_fund.save()

            referring_url = request.META.get('HTTP_REFERER')
            if referring_url:
                return HttpResponseRedirect(referring_url)
            else:
                return redirect('personal-homepage')

        elif 'add-personal-expense-btn' in request.POST:
            personal_expense_fund_id = request.POST.get('personal-expense-fund')
            personal_expense_name = request.POST.get('personal-expense-name')
            personal_expense_amount = request.POST.get('personal-expense-amount')
            personal_expense_document = request.FILES.get('personal-expense-document')

            personal_expense_fund = PersonalFund.objects.get(id=float(personal_expense_fund_id))

            personal_net_worth = PersonalNetWorth.objects.get(id=1)
            personal_net_worth.amount -= float(personal_expense_amount)
            personal_net_worth.save()

            personal_expense, personal_expense_created = PersonalExpense.objects.get_or_create(
                user=request.user,
                name=personal_expense_name,
                amount=float(personal_expense_amount),
                date=timezone.now().date(),
                date_time=timezone.now(),
                fund=personal_expense_fund,
                document=personal_expense_document,
            )
            personal_expense.save()

            personal_fund_expenditure, personal_expenditure_created = PersonalFundExpenditure.objects.get_or_create(
                user=request.user,
                name=personal_expense_name,
                amount=personal_expense_fund.amount - personal_expense.amount,
                expense=personal_expense,
                date=timezone.now().date(),
                date_time=timezone.now(),
            )
            personal_fund_expenditure.save()

            personal_expense_fund.amount -= float(personal_expense_amount)
            personal_expense_fund.save()

            referring_url = request.META.get('HTTP_REFERER')
            if referring_url:
                return HttpResponseRedirect(referring_url)
            else:
                return redirect('personal-homepage')

    return render(request, 'personal_base.html', {
        'personal_funds': personal_funds,
        'personal_received_funds': personal_received_funds,
        'personal_expenses': personal_expenses,
        'personal_expense_funds': personal_expense_funds,
        'personal_net_worth': personal_net_worth,
        'user': user,
    })
