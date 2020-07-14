import logging

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.views import View

from django.shortcuts import render,redirect
from django.http import HttpResponse

from .forms import EmployeeLoginForm,ManagerLoginForm

# Create your views here.

logger = logging.getLogger(__name__)

class EmployeeLoginView(View):
    
    def get(self, request, *args, **kwargs):
        """GETリクエスト用のメソッド"""
        # すでにログインしている場合はショップ画面へリダイレクト
        if request.user.is_authenticated:
            return redirect(reverse('bicycle_borrow_sub_sys:top'))

        context = {
            'form': EmployeeLoginForm(),
        }
        # ログイン画面用のテンプレートに値が空のフォームをレンダリング
        return render(request, 'accounts/login.html', context)

    def post(self, request, *args, **kwargs):
        """POSTリクエスト用のメソッド"""
        # リクエストからフォームを作成
        form = EmployeeLoginForm(request.POST)
        # バリデーション（ユーザーの認証も合わせて実施）
        if not form.is_valid():
            # バリデーションNGの場合はログイン画面のテンプレートを再表示
            return render(request, 'accounts/login.html', {'form': form})

        # ユーザーオブジェクトをフォームから取得
        user = form.get_user()

        # ログイン処理（取得したユーザーオブジェクトをセッションに保存 & ユーザーデータを更新）
        auth_login(request, user)

        # ロギング
        logger.info("User(employee_id={}) has logged in.".format(user.employee_id))

        # ショップ画面にリダイレクト
        return redirect(reverse('bicycle_borrow_sub_sys:top'))

employee_login = EmployeeLoginView.as_view()



class EmployeeLogoutView(View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            # ロギング
            logger.info("User(employee_id={}) has logged out.".format(request.user.employee_id))
            # ログアウト処理
            auth_logout(request)

        return redirect(reverse('accounts:login'))

employee_logout = EmployeeLogoutView.as_view()



class ManagerLoginView(View):
    
    def get(self, request, *args, **kwargs):
        """GETリクエスト用のメソッド"""
        # すでにログインしている場合はショップ画面へリダイレクト
        if request.user.is_authenticated:
            return redirect(reverse('admin_func:top'))

        context = {
            'form': ManagerLoginForm(),
        }
        # ログイン画面用のテンプレートに値が空のフォームをレンダリング
        return render(request, 'accounts/manager_login.html', context)

    def post(self, request, *args, **kwargs):
        """POSTリクエスト用のメソッド"""
        # リクエストからフォームを作成
        form = ManagerLoginForm(request.POST)
        # バリデーション（ユーザーの認証も合わせて実施）
        if not form.is_valid():
            # バリデーションNGの場合はログイン画面のテンプレートを再表示
            return render(request, 'accounts/manager_login.html', {'form': form})

        # ユーザーオブジェクトをフォームから取得
        user = form.get_user()

        # ログイン処理（取得したユーザーオブジェクトをセッションに保存 & ユーザーデータを更新）
        auth_login(request, user)

        # ロギング
        logger.info("User(employee_id={}) has logged in.".format(user.employee_id))

        # ショップ画面にリダイレクト
        return redirect(reverse('admin_func:top'))

manager_login = ManagerLoginView.as_view()



class ManagerLogoutView(View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            # ロギング
            logger.info("User(employee_id={}) has logged out.".format(request.user.employee_id))
            # ログアウト処理
            auth_logout(request)

        return redirect(reverse('accounts:manager_login'))

manager_logout = ManagerLogoutView.as_view()



@login_required
def top_test(request):
    return render(request, 'accounts/top_test.html')

@login_required
def manager_top_test(request):
    return render(request, 'accounts/manager_top_test.html')