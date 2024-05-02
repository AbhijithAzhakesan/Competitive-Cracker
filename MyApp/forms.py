from django import forms
from django.contrib.auth.forms import UserCreationForm

from MyApp.models import Courses, Customers, OnlineClass, StudyMaterials,User,TeachersLogin
from django_countries.fields import CountryField
from django_countries.widgets import CountrySelectWidget

class DateInput(forms.DateInput):
    input_type='date'

class User_register (UserCreationForm):
    username=forms.CharField()
    password1=forms.CharField(label='password',widget=forms.PasswordInput)
    password2=forms.CharField(label='password',widget=forms.PasswordInput)
    class Meta:
        model=User
        fields=('username','password1','password2')

class signup (forms.ModelForm):
    class Meta:
        model=Customers
        exclude=('user',)

class TeachersReg(forms.ModelForm):
    class Meta:
        model=TeachersLogin
        exclude=('user',)
        
class CourseReg(forms.ModelForm):
    start_date = forms.DateField(widget=DateInput)
    end_date = forms.DateField(widget=DateInput)
    class Meta:
        model=Courses
        fields=('course_name','course_price','start_date','end_date','image',)
        
class Video(forms.ModelForm):
    date_time= forms.DateField(widget=DateInput)
    class Meta:
        model=OnlineClass
        fields=('title','description','date_time','class_hours','instructor','video',)
        
class Materials(forms.ModelForm):
    date=forms.DateField(widget=DateInput)
    class Meta:
        model=StudyMaterials
        fields=('title','topic','date','pdf_notes',)

        