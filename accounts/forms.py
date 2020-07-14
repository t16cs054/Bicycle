from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, UsernameField
from django.core.exceptions import ObjectDoesNotExist

from .models import Employee

class EmployeeLoginForm(forms.Form):
    """一般社員ログイン画面用のフォーム"""
    
    employee_id = forms.IntegerField(
        label='社員番号',
        widget=forms.NumberInput(attrs={'placeholder': '社員番号'}),
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user_cache = None
    
    def clean_employee_id(self):
        value = self.cleaned_data['employee_id']
        return value

    def clean(self):
        employee_id = self.cleaned_data.get('employee_id')
        
        try:
            user = get_user_model().objects.get(employee_id=employee_id)
        except ObjectDoesNotExist:
            raise forms.ValidationError("正しい社員番号を入力してください")
        # 取得したユーザーオブジェクトを使い回せるように内部に保持しておく
        self.user_cache = user

    def get_user(self):
        return self.user_cache
    


class ManagerLoginForm(forms.Form):
    """管理者ログイン画面用のフォーム"""
    
    employee_id = forms.IntegerField(
        label='社員番号',
        widget=forms.NumberInput(attrs={'placeholder': '社員番号'}),
        )
    
    password = forms.CharField(
        label='パスワード',
        strip=False,
        widget=forms.PasswordInput(attrs={'placeholder': 'パスワード'}, render_value=True),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user_cache = None
    
    def clean_employee_id(self):
        value = self.cleaned_data['employee_id']
        return value
    
    def clean_password(self):
        value = self.cleaned_data['password']
        return value

    def clean(self):
        employee_id = self.cleaned_data.get('employee_id')
        password = self.cleaned_data.get('password')
        
        try:
            user = get_user_model().objects.get(employee_id=employee_id)
        except ObjectDoesNotExist:
            raise forms.ValidationError("正しい社員番号を入力してください")
        # パスワードはハッシュ化されて保存されているので平文での検索はできない
        if not user.check_password(password):
            raise forms.ValidationError("正しい社員番号とパスワードを入力してください")
        if user.is_staff == False or user.is_superuser == False:
            raise forms.ValidationError("入力した社員は存在しますが管理者ではありません")
        # 取得したユーザーオブジェクトを使い回せるように内部に保持しておく
        self.user_cache = user

    def get_user(self):
        return self.user_cache

