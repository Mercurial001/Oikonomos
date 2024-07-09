from django.shortcuts import render, redirect
from .models import *
from django.utils import timezone
from django.http import HttpResponseRedirect, JsonResponse
import re
from datetime import datetime
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from sklearn.feature_extraction.text import CountVectorizer
from django.contrib.auth.decorators import login_required


@login_required(login_url='login')
def index(request, username):
    # Prerequisites
    user = User.objects.get(
        username=username
    )
    personal_funds = PersonalFund.objects.filter(user=user, removed=False)
    personal_received_funds = PersonalReceivedFund.objects.filter(user=user, removed=False)
    personal_expenses = PersonalExpense.objects.filter(user=user, removed=False)
    personal_expense_funds = PersonalFundExpenditure.objects.filter(user=user, removed=False)
    fund_transfer_modes = PersonalTransferMode.objects.all()
    personal_net_worth_main, personal_net_worth_created = PersonalNetWorth.objects.get_or_create(
        user=user,
    )
    personal_net_worth_main.save()
    # End Prerequisites

    # Funds Data Manipulation
    fund_list_indexing = []
    fund_net_flow_objects = PersonalNetWorthFlow.objects.filter(removed=False, user=user)
    for fund_object in fund_net_flow_objects:
        fund_list_indexing.append(fund_object)

    funds_flow = PersonalNetWorthFlow.objects.filter(removed=False, user=user).order_by('date_time')[len(fund_net_flow_objects) - 10:]

    fund_flow_label = []
    for fund_obj in funds_flow:
        fund_date_format = fund_obj.date
        fund_date = datetime.strptime(str(fund_date_format), '%Y-%m-%d').strftime('%B %d, %Y')
        fund_flow_label.append(fund_date)

    fund_flow_net_worth = []
    for fund in funds_flow:
        net_worth = fund.amount
        fund_flow_net_worth.append(net_worth)

    fund_increase = PersonalFund.objects.filter(removed=False, user=user)

    fund_increase_amount_list = []
    for fund in fund_increase:
        fund_increase_amount_list.append(fund.amount)

    fund_increase_dict = {}
    for fund in fund_increase:
        fund_name_obj = fund.name
        if fund_name_obj not in fund_increase_dict:
            fund_increase_dict[fund_name_obj] = [fund.amount]
        else:
            fund_increase_dict[fund_name_obj].append(fund.amount)

    fund_increase_label = [fund_name for fund_name, amount in fund_increase_dict.items()]
    fund_increase_amount = [round((sum(amount) / sum(fund_increase_amount_list)) * 100) for fund_name, amount in fund_increase_dict.items()]

    # End Funds Data Manipulation

    # Expenses Data Manipulation
    expenses = PersonalExpense.objects.filter(removed=False, user=user).order_by('date_time')
    expenses_dict = {}
    for expense in expenses:
        expense_name = expense.name
        if expense_name not in expenses_dict:
            expenses_dict[expense_name] = [expense]
        else:
            expenses_dict[expense_name].append(expense)

    expenses_name = []
    for expense in expenses:
        name = expense.name
        expenses_name.append(name)

    expenses_amount_list = []
    for expense in expenses:
        amount = expense.amount
        expenses_amount_list.append(amount)

    clean_expense_name_list = []
    for name, expense in expenses_dict.items():
        clean_expense_name_list.append(clean_expense_name(name))

    expenses_dict = {}
    for expense in expenses:
        date = expense.date
        if date not in expenses_dict:
            expenses_dict[date] = [expense.amount]
        else:
            expenses_dict[date].append(expense.amount)

    expenses_date = [datetime.strptime(str(date), '%Y-%m-%d').strftime('%B %d, %Y') for date, amounts in expenses_dict.items()]
    expenses_amount = [sum(amounts) for date, amounts in expenses_dict.items()]

    expense_category_dictionary = {
        'housing': [
            'rent', 'mortgagepayment', 'mortgage payment' 'homeownersinsurance',
            'homeownersassociationfees', 'homeowners association fees'
            'homemaintenance' 'home maintenance', 'propertytax', 'property tax'
            'homeimprovement', 'home improvement' 'mortgage', 'home', 'renovation', 'renovate'
        ],
        'pets': [
            'dog', 'cat', 'bird', 'fish', 'snake', 'alligator', 'animals', 'dogfood', 'catfood',
            'birdfood', 'fishfood', 'vet', 'veterinary', 'veterinarian', 'petvaccine', 'pet', 'grooming',
            'pettoys', 'petaccessories', 'dog food', 'cat food', 'bird food', 'fish food',

        ],
        'food': [
            'piatoss', 'nova', 'chips', 'patatas', 'cheezie', 'junkfood', 'snack', 'meal',
            'lunch', 'breakfast', 'dinner', 'dining', 'grocery', 'food', 'alcohol',
            'drive-thru', 'jolibee', 'manginasal', 'chowking', 'milktea', 'pizza', 'burger',
            'takeout', 'takeaway', 'restaurant', 'cafeteria', 'cafe'
        ],
        'transportation': [
            'transpo', 'transportationfee', 'gasoline', 'gas', 'carleasepayment', 'autorepairs',
            'carmaintenance', 'carinsurance', 'car insurance' 'parking', 'parkingfees', 'ridesharefees',
            'ridesharecost', 'ridesharetips', 'carregistrationfee', 'driverslicense', 'drivers license'
            'publictransport', 'busfare', 'bus fare' 'trainfare', 'train fare', 'taxi', 'uber',
            'fuel',
        ],
        'savings': [
            'emergencyfund', 'deposit', 'investments', 'savings', 'fund', 'withdraw', 'atmcard', 'atm'
        ],
        'medical': [
            'health', 'medicine', 'hospital', 'dental', 'vision', 'doctor', 'dr', 'optics',
            'eyeglasses', 'contactlens', 'contact lens' 'lens', 'contacts',
            'prescriptionmedications', 'prescription medications',
            'medications', 'medicaldevice', 'medical device', 'wheelchairs',
            'canes', 'clinic', 'checkup', 'medical'
        ],
        'utilities': [
            'electricity', 'waterbill', 'water bill', 'subscription', 'rent', 'internet', 'water', 'utility',
            'mobilephones', 'phones', 'load', 'cable', 'wifi', 'mobile phones'
        ],
        'insurance': [
            'lifeinsurance', 'disabilityinsurance', 'accidentaldeathinsurance', 'rentersinsurance',
            'insurance', 'autoinsurance', 'healthinsurance', 'homeinsurance'
        ],
        'taxes': [
            'yearlytax', 'monthlytax', 'incometax', 'tax', 'propertytax', 'salestax'
        ],
        'education': [
            'tuition', 'books', 'daycare', 'school', 'schoolcare', 'tutor', 'tutoring',
            'schoolcamp', 'schoolsupplies', 'training', 'course', 'onlineclass', 'onlinecourse',
            'seminar', 'workshop'
        ],
        'debts': [
            'debts', 'debt', 'utang', 'loan', 'credit', 'creditcard', 'mortgage'
        ],
        'household items': [
            'cleaningsupplies', 'papergoods', 'toiletpaper', 'dishwashingliquid', 'detergent', 'soap',
            'dishwashing', 'powdersoap', 'appliances', 'refrigerator', 'dish', 'spoon', 'fork', 'plates',
            'cup', 'glass', 'towel', 'table', 'chair', 'chairs', 'guitar', 'instruments', 'amplifiers',
            'speakers', 'television', 'wardrobe', 'cabinet', 'bedding', 'blanket', 'pillow', 'curtain',
            'kitchenware', 'utensils'
        ],
        'personal care': [
            'salon', 'nail', 'rebond', 'haircut', 'spa', 'massage', 'beauty', 'deodorant',
            'shampoo', 'hairfix', 'hair', 'makeup', 'eyelash', 'nosejob', 'skincare', 'cosmetics',
            'facial', 'pedicure', 'manicure'
        ],
        'clothing': [
            'clothes', 'clothing', 'shirt', 'shorts', 'accessories',
            'apparel', 'accessory', 'watches', 'bag', 'backpacks', 'shoes', 'flipflops', 'tsianelas',
            'chanelas', 'footwear', 'jacket', 'bodywear', 'torso', 'legs', 'leggings',
            'jeans', 'watch', 'pendants', 'necklace', 'earrings', 'hat', 'cap', 'headwear', 'wristband',
            'neckwear', 'bracelet', 'short', 'cuff', 'gloves', 'belt'
        ],
        'entertainment': [
            'gym', 'cable', 'signal', 'cignal', 'movie', 'movieoutings', 'bars', 'hobbies', 'craft',
            'youtube', 'netflix', 'subscriptions', 'concert', 'games', 'sport', 'theater'
        ],
        'travel': [
            'airplane', 'airfare', 'ticket', 'carrental', 'hotel', 'souvenirs', 'bus', 'bustickets',
            'traintickets', 'flight', 'tour', 'vacation', 'trip', 'cruise'
        ],
        'gifts': [
            'gift', 'gave', 'handed', 'donation', 'charity', 'holidaygift', 'christmasgift',
            'hostessgift', 'weddinggift', 'babygift', 'birthdaygift'
        ],
        'miscellaneous': [
            'repairment fee', 'services', 'service', 'bankfees', 'personal spending', 'beyond',
            'unnecessary', 'pictures', 'misc', 'miscellaneous', 'other', 'fee', 'repairment',
            'shopping'
        ]
    }

    categorized_expenses = {expen: categorize_expense(expen.name, expense_category_dictionary) for expen in expenses}
    categorized_expense = {}
    for expense, category in categorized_expenses.items():
        if category not in categorized_expense:
            categorized_expense[category] = [expense]
        else:
            categorized_expense[category].append(expense)

    categorized_expense_amount = {}
    for expense, category in categorized_expenses.items():
        if category not in categorized_expense_amount:
            categorized_expense_amount[category] = [expense.amount]
        else:
            categorized_expense_amount[category].append(expense.amount)
        # print(f"Expense: {expense} -> Category: {category}")

    expense_donut_label = [category for category, objects in categorized_expense_amount.items()]
    expense_donut_percentage = [round(sum(objects) / sum(expenses_amount_list) * 100) for category, objects in categorized_expense_amount.items()]

    # End Expenses Data Manipulation

    if request.method == 'POST':
        if 'add-personal-fund-btn' in request.POST:
            personal_fund_name = request.POST.get('personal-fund-name')
            personal_fund_amount = request.POST.get('personal-fund-amount')
            personal_fund_document = request.FILES.get('personal-fund-document')

            net_worth, created_net_worth = PersonalNetWorth.objects.get_or_create(
                user=user
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

            PersonalNetWorthFlow.objects.create(
                fund=personal_fund,
                user=user,
                amount=net_worth.amount + float(personal_fund_amount),
                amount_added=float(personal_fund_amount),
                date=timezone.now().date(),
                date_time=timezone.now(),
            )

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

            personal_expense_fund = PersonalFund.objects.get(id=int(personal_expense_fund_id))

            personal_net_worth = PersonalNetWorth.objects.get(user=user)
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
                net_worth_amount=personal_net_worth.amount,
                expense=personal_expense,
                date=timezone.now().date(),
                date_time=timezone.now(),
            )
            personal_fund_expenditure.save()

            personal_expense_fund.amount -= float(personal_expense_amount)
            personal_expense_fund.save()

            PersonalNetWorthFlow.objects.create(
                expense=personal_expense,
                user=user,
                amount=personal_net_worth.amount - float(personal_expense_amount),
                amount_added=float(personal_expense_amount),
                date=timezone.now().date(),
                date_time=timezone.now(),
            )

            referring_url = request.META.get('HTTP_REFERER')
            if referring_url:
                return HttpResponseRedirect(referring_url)
            else:
                return redirect('personal-homepage')
        elif 'add-fund-amount-btn' in request.POST:
            fund_id = request.POST.get('fund-id')
            fund_amount_added = request.POST.get('fund-amount-added')

            personal_net_worth = PersonalNetWorth.objects.get(
                user=user,
            )

            fund = PersonalFund.objects.get(user=user, id=int(fund_id))
            personal_net_balance = PersonalNetWorth.objects.get(user=user)
            personal_net_balance.amount += float(fund_amount_added)
            personal_net_balance.save()

            fund.amount += float(fund_amount_added)
            fund.save()

            fund_added_object, fund_added_object_created = PersonalFundAdded.objects.get_or_create(
                user=user,
                fund=fund,
                amount=fund_amount_added,
                net_worth_amount=personal_net_worth.amount + float(fund_amount_added),
                date=timezone.now().date(),
                date_time=timezone.now(),
            )
            fund_added_object.save()

            PersonalNetWorthFlow.objects.create(
                fund=fund,
                user=user,
                amount=personal_net_worth.amount + float(fund_amount_added),
                amount_added=float(fund_amount_added),
                date=timezone.now().date(),
                date_time=timezone.now(),
            )

            referring_url = request.META.get('HTTP_REFERER')
            if referring_url:
                return HttpResponseRedirect(referring_url)
            else:
                return redirect('personal-homepage')

        elif 'transfer-fund-btn' in request.POST:
            fund_transferred = request.POST.get('fund-transferred')
            fund_receiver_id = request.POST.get('fund-receiver-id')
            fund_sender_id = request.POST.get('fund-sender-id')
            fund_tranfer_mode_id = request.POST.get('fund-transfer-mode')

            fund_transfer_mode = PersonalTransferMode.objects.get(id=int(fund_tranfer_mode_id))
            fund_receiver = PersonalFund.objects.get(id=int(fund_receiver_id), user=user)
            fund_sender = PersonalFund.objects.get(id=int(fund_sender_id), user=user)
            fund_transfer_obj, created = PersonalFundTransferred.objects.get_or_create(
                user=user,
                receiver=fund_receiver,
                sender=fund_sender,
                amount=float(fund_transferred),
                date=timezone.now().date(),
                date_time=timezone.now(),
                mode=fund_transfer_mode,
            )

            fund_receiver.amount += float(fund_transferred)
            fund_sender.amount -= float(fund_transferred)

            fund_receiver.save()
            fund_sender.save()
            fund_transfer_obj.save()

            http_referrer = request.META.get('HTTP_REFERER')
            if http_referrer:
                return HttpResponseRedirect(http_referrer)
            else:
                return redirect('personal-homepage', username=user.username)

    return render(request, 'personal_base.html', {
        'personal_funds': personal_funds,
        'personal_received_funds': personal_received_funds,
        'personal_expenses': personal_expenses,
        'personal_expense_funds': personal_expense_funds,
        'personal_net_worth': personal_net_worth_main,
        'user': user,
        # 'expenses_dict': expenses_dict,
        'categorized_expense': categorized_expense,
        'categorized_expenses': categorized_expenses,
        'expenses_amount': expenses_amount,
        'expenses_date': expenses_date,
        'expense_donut_label': expense_donut_label,
        'expense_donut_percentage': expense_donut_percentage,
        'fund_flow_label': fund_flow_label,
        'fund_flow_net_worth': fund_flow_net_worth,
        'fund_increase_label': fund_increase_label,
        'fund_increase_amount': fund_increase_amount,
        'fund_transfer_modes': fund_transfer_modes,
    })


def clean_expense_name(name):
    cleaned_expense_name = name.lower()

    cleaned_expense_name = re.sub(r'[^a-zA-Z\s]', '', cleaned_expense_name)
    cleaned_expense_name = re.sub(r'\s+', '', cleaned_expense_name)

    return cleaned_expense_name


def categorize_expense(expense, category_dict):
    """
    Categorizes an expense based on keywords in the category dictionary.

    Parameters:
    - expense (str): The cleaned and standardized expense name.
    - category_dict (dict): A dictionary where keys are category names and values are lists of keywords.

    Returns:
    - str: The category name if a match is found, otherwise 'uncategorized'.
    """
    expense = expense.lower()  # Ensure the expense name is in lowercase
    for category, keywords in category_dict.items():
        for keyword in keywords:
            if keyword in expense:
                return category
    return 'uncategorized'


@login_required(login_url='login')
def remove_personal_expenses(request, id, username):
    if request.method == 'POST':
        user = User.objects.get(username=username)
        expense = PersonalExpense.objects.get(id=id, user=user)
        personal_net_flow = PersonalNetWorthFlow.objects.get(expense__id=id, user=user)
        personal_net_worth = PersonalNetWorth.objects.get(user=user)
        personal_expenditure = PersonalFundExpenditure.objects.get(
            expense=expense
        )

        removed_finance_data, created = RemovedPersonalFinanceData.objects.get_or_create(
            user=user,
            name=expense.name,
            object_id=expense.id,
            amount=expense.amount,
            date=timezone.now().date(),
            date_time=timezone.now(),
        )
        removed_finance_data.save()

        expense.removed = True
        personal_expenditure.removed = True
        personal_net_flow.removed = True

        fund_id = expense.fund.id
        fund = PersonalFund.objects.get(id=fund_id)

        fund.amount += expense.amount
        personal_net_worth.amount += expense.amount

        expense.save()
        fund.save()
        personal_net_worth.save()
        personal_expenditure.save()
        personal_net_flow.save()

        url_referrer = request.META.get('HTTP_REFERER')
        if url_referrer:
            return HttpResponseRedirect(url_referrer)
        else:
            return redirect('personal-homepage', username=username)


def remove_fund(request, id, username):
    user = User.objects.get(
        username=username
    )
    personal_balance = PersonalNetWorth.objects.get(
        user=user
    )

    fund = PersonalFund.objects.get(
        id=id,
        user=user
    )
    received_fund = PersonalReceivedFund.objects.get(
        fund=fund
    )

    personal_balance.amount += received_fund.amount
    fund.removed = True
    received_fund.removed = True

    fund.save()
    received_fund.save()
    personal_balance.save()

    referring_url = request.META.get('HTTP_REFERER')
    if referring_url:
        return HttpResponseRedirect(referring_url)
    else:
        return redirect('personal-homepage', username=user.username)


@login_required(login_url='login')
def create_net_worth_flow(request, username):
    user = User.objects.get(username=username)
    personal_expenditures = PersonalFundExpenditure.objects.filter(removed=False).order_by('date_time')

    for expense in personal_expenditures:

        PersonalNetWorthFlow.objects.create(
            expense=expense.expense,
            user=user,
            amount=expense.net_worth_amount,
            amount_added=expense.amount,
            date=expense.date,
            date_time=expense.date_time
        )

    referring_url = request.META.get('HTTP_REFERER')
    if referring_url:
        return HttpResponseRedirect(referring_url)
    else:
        return redirect('homepage', username=username)


@login_required(login_url='login')
def filter_personal_fund(request):
    selected_fund_id = request.GET.get('fundSenderId')
    if selected_fund_id:
        try:
            selected_fund = PersonalFund.objects.get(id=selected_fund_id, user=request.user, removed=False)
            receiver_funds = PersonalFund.objects.filter(user=request.user, removed=False).exclude(id=selected_fund.id)

            serialized_funds = [{'id': fund.id, 'name': fund.name} for fund in receiver_funds]
            return JsonResponse(serialized_funds, safe=False)
        except PersonalFund.DoesNotExist:
            return JsonResponse({'error': 'Selected fund does not exist.'}, status=404)
    else:
        return JsonResponse([], safe=False)


# def logout_user(request):
#     logout(request)
#     return redirect('login')
