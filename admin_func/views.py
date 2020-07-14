from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import Borrow_history
from django.shortcuts import redirect
from .models import Bicycle
import datetime
import time
from .models import Office
from django.urls import reverse
from django.contrib import messages
from django.shortcuts import render
from django.http import HttpResponse
from .models import Borrow_history
from django.shortcuts import redirect
from .models import Bicycle
import datetime
from django.contrib.auth.decorators import login_required
import time
from django.urls import reverse
from django.contrib import messages
from datetime import datetime,timedelta
from .models import Employee

@login_required
def top(request):
    office2 = Office.objects.get(office_id=2)
    office1 = Office.objects.get(office_id=1)
    office3 = Office.objects.get(office_id=3)
    data = Borrow_history.objects.all().order_by('bicycle_id')
    alloffice = Office.objects.all().order_by('office_id')
    nums1 = Bicycle.objects.all().filter(office_id=1).count()
    nums2 = Bicycle.objects.all().filter(office_id=2).count()
    nums3 = Bicycle.objects.all().filter(office_id=3).count()
    params = {
        'title':'管理者用トップ画面',
        'msg':'移動する自転車を選択してください',
        #'form':borrow_bicycleForm(),
        'data':data,
        'nums1':nums1,
        'nums2':nums2,
        'nums3':nums3,
        'alloffice':alloffice,
        'office1':office1,
        'office2':office2,
        'office3':office3,
        }
    return render(request, 'admin_func/top.html', params)

@login_required
def transfer_warning(request,num):
    #num => 自転車番号
    target_histories = Borrow_history.objects.all().filter(bicycle_id = num)
    exceptionflag = False
    list = []
    my_nums = []
    if(Bicycle.objects.get(bicycle_id = num).status == False):
        exceptionflag = True
    if(exceptionflag == False):
        for item in target_histories:
            list.append(item.employee_id.employee_id)#その自転車を借りているユーザのIDのリスト
    target_bicycle = Bicycle.objects.get(bicycle_id=num)
    offices = Office.objects.all()
    if(request.method=='POST'):
        #異動元の事務所の自転車台数を1減らす
        from_office = Office.objects.get(office_id = target_bicycle.office_id.office_id)
        new_nums1 = from_office.bicycle_nums_office - 1
        Office.objects.filter(office_id = target_bicycle.office_id.office_id).update(bicycle_nums_office = new_nums1)
        #その自転車の貸し出し履歴を初期化する
        target_office_id=request.POST['office']
        target_histories.delete()
        Bicycle.objects.filter(bicycle_id = num).update(status=False)
        #異動先の事務所の自転車台数を1増やす
        dst_office = Office.objects.get(office_id = target_office_id)
        new_nums2 = dst_office.bicycle_nums_office + 1
        Office.objects.filter(office_id = dst_office.office_id).update(bicycle_nums_office = new_nums2)
        #新しい初期化された履歴を作る
        Bicycle.objects.filter(bicycle_id = num).update(office_id=target_office_id)
        new_borrow_history = Borrow_history(bicycle_id_id = num)
        new_borrow_history.save()
        if(exceptionflag == False):
            for target_id in list:
                Employee.objects.all().filter(employee_id = target_id).update(borrowed_bicycles = Employee.objects.get(employee_id = target_id).return_my_nums() - 1)
        return redirect(to='/admin_func/transfer_comp/' + str(num))
    params = {
        #'form':borrow_bicycleForm(),
        'data':target_histories,
        'target_bicycle':target_bicycle,
        'offices':offices,
        'num':num,
        }
    return render(request, 'admin_func/transfer_warning', params)

@login_required
def transfer_comp(request,num):
    #num 自転車番号
    bicycle = Bicycle.objects.get(bicycle_id=num)
    params = {
        'obj':bicycle,
        }
    return render(request, 'admin_func/transfer_comp', params)

