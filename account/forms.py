from django import forms
from django.contrib.auth.models import User
from .models import Profile


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)  # PasswordInput是一个微件，用来显示其HTML input元素，
    # 同时包含type=“password”属性，以使浏览器可以将其视为密码输入。


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label="Repeat password", widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'email')  # 模型所包含的三个字段

    def clean_password2(self):  # 对两次输入的密码进行比较
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:  # 两次密码不同，则抛出异常，终止表单填写
            raise forms.ValidationError('Passwords don\'t match.')
        return cd['password2']


class UserEditForm(forms.ModelForm):   # 允许用户编辑其名字、姓氏以及电子邮件，这一类内容均为内置Django用户模型中的属性。
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')


class ProfileEditForm(forms.ModelForm):  # 使得用户可以编辑保存在自定义Profile模型中的配置数据。用户可编辑其出生日期并上传其配置照片
    class Meta:
        model = Profile
        fields = ('date_of_birth', 'photo')
