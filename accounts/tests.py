from django.test import TestCase , Client
from accounts.models import Employee
from django.contrib.auth.models import User
from django.urls import reverse

# Create your tests here.
#コマンドラインから「python3.5 manage.py test accounts」と入力して実行すること

#社員レコードを作成、検証するためのクラス
class EmployeeAssertion(TestCase):
    def creating_and_saving_employee(self,id=1,name=None,password=None,bicycles=None):
        employee = Employee()
        if id is not None:
            employee.employee_id=id
        if name is not None:
            employee.username=name
        if password is not None:
            employee.password=password
        if bicycles is not None:
            employee.borrowed_bicycles=bicycles
        employee.save()
    
    def assertEmployeeModel(self,actual_employee,id,name,password,bicycles):
        self.assertEqual(actual_employee.employee_id,id)
        self.assertEqual(actual_employee.username,name)
        self.assertEqual(actual_employee.password,password)
        self.assertEqual(actual_employee.borrowed_bicycles,bicycles)
        

class EmployeeModelTest(EmployeeAssertion):
    
    #何も登録しなければレコードの数は0個
    def test_is_empty(self):
        saved_employees = Employee.objects.all()
        self.assertEqual(saved_employees.count(),0)
    
    #レコードの追加ができるかどうか
    def test_is_not_empty(self):
        self.creating_and_saving_employee()
        saved_employees = Employee.objects.all()
        self.assertEqual(saved_employees.count(), 1)
        
    #保存したレコードと取り出したレコードが一致するかどうか
    def test_saving_and_retrieving_employee(self):
        _id=10
        _username='test'
        _password='itsys2018'
        _num = 2
        self.creating_and_saving_employee(_id,_username,_password,_num)
        
        saved_employees = Employee.objects.all()
        actual_employee = saved_employees[0]
        
        self.assertEmployeeModel(actual_employee,_id,_username,_password,_num)

