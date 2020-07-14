from django.shortcuts import render
from django.http import HttpResponse
from .models import Borrow_history
from django.shortcuts import redirect
from .models import Bicycle
from .models import Office
import datetime
from django.contrib.auth.decorators import login_required
import time
from .models import Employee
from django.urls import reverse
from django.contrib import messages

@login_required
def top(request):
    all_my_bike = Borrow_history.objects.all().filter(employee_id=request.user.employee_id).count()
    params = {
        'title':'トップ画面',
        'all_my_bike':all_my_bike
        }
    return render(request, 'bicycle_borrow_sub_sys/top.html', params)

@login_required
def borrow_bicycle(request):
    office2 = Office.objects.get(office_id=2)
    office1 = Office.objects.get(office_id=1)
    office3 = Office.objects.get(office_id=3)
    data = Borrow_history.objects.all().order_by('bicycle_id')
    nums1 = Bicycle.objects.all().filter(office_id=1).count()
    nums2 = Bicycle.objects.all().filter(office_id=2).count()
    nums3 = Bicycle.objects.all().filter(office_id=3).count()
    list = []
    already_borrow_bicycle = Borrow_history.objects.all().filter(employee_id=request.user.employee_id)
    for bike in already_borrow_bicycle:
        list.append(bike.bicycle_id)#Jibun ga karite iru jitensya no borrow_id no ichiran(list)
    params = {
        'title':'借りる画面',
        #'msg':'借りる自転車を選択してください',
        #'form':borrow_bicycleForm(),
        'data':data,
        'list':list,
        'nums1':nums1,
        'nums2':nums2,
        'nums3':nums3,
        'office1': office1,
        'office2': office2,
        'office3': office3,
        }
    return render(request, 'bicycle_borrow_sub_sys/borrow_bicycle.html', params)


def borrow_warning(request, num):
    bicycle_borrowed_history = Borrow_history.objects.all().filter(bicycle_id=num)
    #my_bicycles = request.user.borrowed_bicycles
    my_bicycles = Borrow_history.objects.all().filter(employee_id = request.user.employee_id).count()
    my_limit = 3 - my_bicycles
    bicycle = Bicycle.objects.get(bicycle_id=num)
    params = {
        'title':'貸し出し確認画面',
        'data':bicycle_borrowed_history,
        'obj':bicycle,
        'my_limit':my_limit,
        }

    if(request.method == 'POST'):
        #もし自転車を3台以上借りている場合
        if(my_bicycles>=3):
            messages.success(request, '自転車を3台借りています。これ以上借りることはできません。')
            #return redirect(request, 'bicycle_borrow_sub_sys/borrow_warning.html')
        #もし自転車を3台以上借りていない場合
        if(my_bicycles<3):
            #その自転車の履歴が何個あるか
            if(bicycle_borrowed_history.count() ==1):
                for bike in bicycle_borrowed_history:
                        #もしその自転車が誰にも借りられていない場合
                    if(bike.employee_id is None):
                        bicycle_borrowed_history.delete()
                        date = datetime.date.today()
                        b_history  = Borrow_history(bicycle_id_id = num ,  employee_id_id = request.user.employee_id, start_day = date)
                        b_history.save()
                        my_limit = my_limit - 1
                        Bicycle.objects.filter(bicycle_id = num).update(status=True)
                        my_bicycles = my_bicycles+1
                        Employee.objects.all().filter(employee_id = request.user.employee_id).update(borrowed_bicycles = my_bicycles)
                        return redirect(to='/bicycle_borrow_sub_sys/borrowed/' + str(num))
                    else:
                        #その自転車が誰かに（1人）借りられたいた場合
                        date = datetime.date.today()
                        b_history  = Borrow_history(bicycle_id_id = num ,  employee_id_id = request.user.employee_id, start_day = date)
                        b_history.save()
                        my_bicycles = my_bicycles+1
                        Employee.objects.all().filter(employee_id = request.user.employee_id).update(borrowed_bicycles = my_bicycles)
                        my_limit = my_limit - 1
                        return redirect(to='/bicycle_borrow_sub_sys/borrowed/' + str(num))
            else:
                #もしその自転車が誰かに（1人以上）借りられていた場合
                date = datetime.date.today()
                b_history  = Borrow_history(bicycle_id_id = num ,  employee_id_id = request.user.employee_id, start_day = date)
                b_history.save()
                my_bicycles = my_bicycles+1
                Employee.objects.all().filter(employee_id = request.user.employee_id).update(borrowed_bicycles = my_bicycles)
                my_limit = my_limit - 1
                return redirect(to='/bicycle_borrow_sub_sys/borrowed/' + str(num))
    
    return render(request, 'bicycle_borrow_sub_sys/borrow_warning.html', params)

@login_required
def borrowed(request, num):
    bicycle = Bicycle.objects.get(bicycle_id=num)
    all_my_bike = Borrow_history.objects.all().filter(employee_id=request.user.employee_id)
    rest_num_can_borrow = 3 - all_my_bike.count()
    params = {
        'title':'貸し出し完了画面',
        'obj':bicycle,
        'rest_num_can_borrow':rest_num_can_borrow
        }
    
    return render(request, 'bicycle_borrow_sub_sys/borrowed.html', params)

    

@login_required
def return_bicycle(request):
    data = Borrow_history.objects.all().filter(employee_id=request.user.employee_id)
    num = Borrow_history.objects.all().filter(employee_id=request.user.employee_id).count()
    data2=Office.objects.all()
    params = {
        'title':'返す画面',
        'msg':'返す自転車を選択してください',
        #'form':borrow_bicycleForm(),
        'data':data,
        'data2':data2,
        }
    if(num==0):
        params['title']="あなたは一台も借りていません"
        params['msg']="ログアウトまたはトップページへ戻ってください"
        
        return render(request, 'bicycle_borrow_sub_sys/return_bicycle_nobike.html', params)
    else:
        return render(request, 'bicycle_borrow_sub_sys/return_bicycle.html', params)


@login_required
def return_warning(request):
    params = {
        'title':'返却確認',
        'msg':'返却内容はこれでよいですか？',
        #'form':borrow_bicycleForm(),
        'data':[],
        'data2':[],
        }
    if(request.method=='POST'):
        oid=request.POST['office']
        bid=request.POST['bicycle']
        item2=Office.objects.get(office_id=oid)
        item=Bicycle.objects.get(bicycle_id=bid)
        params['data']=item
        params['data2']=item2
        return render(request, 'bicycle_borrow_sub_sys/return_warning.html', params)
    else:
        return HttpResponse("入力に不備がありました")

@login_required
def returned(request, num):
    data = Bicycle.objects.get(bicycle_id=num)
    all_my_bike = Borrow_history.objects.all().filter(employee_id=request.user.employee_id)
    rest_num_can_borrow =all_my_bike.count()
    my_limit=3 - rest_num_can_borrow
    rest_num_can_borrow = rest_num_can_borrow-1
    Employee.objects.all().filter(employee_id = request.user.employee_id).update(borrowed_bicycles = rest_num_can_borrow)
    my_limit = my_limit + 1
    params = {
        'title':'返却完了しました',
        'data':data,
        'my_limit':my_limit
        }
    if(request.method=='POST'):
        oid=request.POST['office']#返却先事務所
        bid=request.POST['bicycle']
        borrow_bike_num=Borrow_history.objects.all().filter(bicycle_id=bid).count()
        bike=Bicycle.objects.get(bicycle_id=bid)
        office_a=Office.objects.get(office_id=oid)
        office_b=Office.objects.get(office_id=bike.office_id.office_id)
        item=Borrow_history.objects.all().filter(employee_id=request.user.employee_id,bicycle_id=bid)
        item.delete()
        bike.office_id=office_a
        bike.save()
        if(office_a.office_id!=office_b.office_id):
        
            office_a.bicycle_nums_office+=1
            office_a.save()
            office_b.bicycle_nums_office-=1
            office_b.save()
        
        if(borrow_bike_num==1):
            bike.status = False
            bike.save()
            date = datetime.datetime.today()
            b_history = Borrow_history(bicycle_id_id = bid , start_day = date)
            b_history.save()
            
        return render(request, 'bicycle_borrow_sub_sys/returned.html', params)
        
    else:
        return HttpResponse("Hello NO Return Warning!")

