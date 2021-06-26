from django.shortcuts import render
from django.http import HttpResponse
from administrator.models import Administrator
from administrator.models import Commodity
from administrator.models import Vindor
from administrator.models import Orders
from django.db import connection
from administrator.models import Users
import datetime
import socket


# Create your views here.


def hello_word(request):
    return HttpResponse("Hello_ World")


# 商品信息
def show_commodity(request, account):
    commodities = Commodity.objects.all()
    print('right')
    print(account)
    return render(request, 'commotities.html', {
        'account': account,
        'commodities': commodities,
    })


# 添加商品
def add_commodity(request, account):
    print(account)
    commodities_1 = Commodity.objects.filter(number__lt=10)
    commodities_2 = Commodity.objects.filter(number__lt=30, number__gt=10)
    res = Orders.objects.all()
    m = []
    for i in res:
        m.append(i.commodity_id)
    res_1 = []
    for i in m:
        if m.count(i) > 2:
            res_1.append(i)
    m = []
    res_1 = set(res_1)
    for i in res_1:
        m.append(Commodity.objects.get(id=i))
    return render(request, 'add_commodity.html', {
        'account': account,
        'commodities_1': commodities_1,
        'commodities_2': commodities_2,
        'commodities_3': m,
    })


# 删除商品
def delete_commodity(request):
    try:
        commodity_name = request.POST.get('commodity_name')
        Commodity.objects.get(commodity_name=commodity_name).delete()
        return render(request, 'correct.html')
    except:
        return render(request, 'worning.html')


# 注册管理员
def register(request):
    account = request.POST.get('account')
    password = request.POST.get('password')
    phone_number = request.POST.get('phone_number')
    administrator = Administrator()
    accounts = Administrator.objects.all()
    for ars in accounts:
        if ars.account == account:
            return render(request, 'worning.html')
    try:
        administrator.account = account
        administrator.password = password
        administrator.phone_number = phone_number
        administrator.save()
        return render(request, 'administrator/login.html', {
            'account': account,
            'password': password,
        })
    except:
        print('Error')


def get_detail_page(request, commodity_id, account):
    try:
        print(commodity_id)
        print(account)
        curr_commodity = Commodity.objects.filter(id=commodity_id)
        curr_vindor = Vindor.objects.filter(commodity_name=curr_commodity[0].commodity_name)
        orders = Orders.objects.filter(commodity_id=commodity_id)
        print(curr_vindor[0].commodity_name)
        print(curr_vindor[0].vind_name)
        return render(request, 'detail_2.html', {
            'curr_commodity': curr_commodity[0],
            'curr_vinder': curr_vindor[0],
            'orders': orders,
            'account': account,
        })
    except:
        return render(request, 'worning.html')


def get_modify_page(request, commodity_id, account):
    try:
        curr_commodity = Commodity.objects.filter(id=commodity_id)
        curr_vindor = Vindor.objects.filter(commodity_name=curr_commodity[0].commodity_name)
        print(curr_vindor[0].commodity_name)
        print(curr_vindor[0].vind_name)
        return render(request, 'modify.html', {
            'curr_commodity': curr_commodity[0],
            'curr_vinder': curr_vindor[0],
            "account": account,
        })
    except:
        return render(request, 'worning.html')


def submit(request):
    account = request.POST.get('account')
    commodity_name = request.POST.get('commodity_name')
    commodity_price = request.POST.get('commodity_price')
    comment = request.POST.get('comment')
    photo = request.POST.get('photo')
    vind_name = request.POST.get('vind_name')
    vind_location = request.POST.get('vind_location')
    phone_number = request.POST.get('phone_number')
    curr_commodity = Commodity.objects.get(commodity_name=commodity_name)
    curr_commodity.commodity_price = commodity_price
    curr_commodity.comment = comment
    curr_commodity.photo = photo
    curr_commodity.save()
    vindor = Vindor.objects.get(commodity_name=commodity_name)
    print(vind_location)
    vindor.vind_name = vind_name
    vindor.vind_location = vind_location
    vindor.phone_number = phone_number
    vindor.save()
    commodities = Commodity.objects.all()
    return render(request, 'commotities.html', {
        'account': account,
        'commodity_list': commodities
    })


def get_my_information_page(request, account):
    res = Administrator.objects.get(account=account)
    return render(request, 'my_information.html', {'res': res})


def iter_administrator(request):
    return render(request, 'correct.html')


def sale_commodity(request, account):
    commodities = Commodity.objects.all()
    res = []
    dt = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    for i in commodities:
        if dt < str(i.expiration_date) < '2021-06-28':
            res.append(i)
    for i in res:
        print(i.commodity_name)
        print("ok")
    return render(request, 'sales.html', {
        "account": account,
        "commodities": res,
        "dt": dt,
    })


def confirm_sale_commodity(request, account):
    discount = request.POST.get("discount")
    id = request.POST.get("id")
    curr_commodity = Commodity.objects.get(id=id)
    curr_commodity.commodity_price = curr_commodity.commodity_price * discount / 100
    curr_commodity.save()
    return_index()


def show_orders(request, account):
    all_orders = Orders.objects.order_by("time")
    turnover = 0  # 所有订单收入
    for i in all_orders:
        curr_commodity_id = i.commodity_id
        curr_commodity = Commodity.objects.get(id=curr_commodity_id)
        turnover = turnover + i.number*curr_commodity.commodity_price
    print(turnover)
    return render(request, 'orders.html', {
        'account': account,
        'all_orders': all_orders,
        'turnover': turnover,
    })


def return_index():
    return render('index.html')


# 风险管控
def show_warnings(request,account):
    commodities = Commodity.objects.all()
    dt = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    warning_commodity = []
    for i in commodities:
        if str(i.expiration_date) < str(dt):
            warning_commodity.append(i)
    return render(request, 'worning.html', {
        'warning_commodity': warning_commodity,
        'account': account,
    })
