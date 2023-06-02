from django import forms
from django.contrib.auth.hashers import make_password
from django.core.exceptions import ValidationError
from django.forms import PasswordInput
from django.contrib.auth.models import User


class LoginForm(forms.Form):
    username = forms.CharField(max_length=20)
    password = forms.CharField(max_length=20, widget=PasswordInput)


# 使用普通表单定义注册字段
# class RegisterForm(forms.Form):
#     username = forms.CharField(max_length=20)
#     password = forms.CharField(max_length=20, widget=PasswordInput)
#     re_password = forms.CharField(max_length=20, widget=PasswordInput)
#     first_name = forms.CharField(max_length=20)
#     last_name = forms.CharField(max_length=20)
#     email = forms.EmailField(max_length=100)
#
#     def clean(self):
#         cleaned_data = super().clean()
#         p = cleaned_data.get("password")
#         rp = cleaned_data.get("re_password")
#
#         if p and rp:
#             # Only do something if both fields are valid so far.
#             if p != rp:
#                 raise ValidationError("Inputs for password doesn't equal.")
#                 # 引发验证错误表单的密码输入项会清空，其他项会保留


class RegisterForm(forms.ModelForm):
    password = forms.CharField(max_length=20, widget=PasswordInput)
    re_password = forms.CharField(max_length=20, widget=PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password']

    def clean(self):
        cleaned_data = super().clean()
        p = cleaned_data.get("password")
        rp = cleaned_data.get("re_password")

        if p and rp:
            # Only do something if both fields are valid so far.
            if p != rp:
                raise ValidationError("Inputs for password doesn't equal.")
                # 引发验证错误表单的密码输入项会清空，其他项会保留
            self.cleaned_data['password'] = make_password(p)


class ProfileForm(forms.ModelForm):
    username = forms.CharField(disabled=True)
    sex = forms.CharField(disabled=True)
    birth_date = forms.CharField(disabled=True)
    introduce_text = forms.CharField(disabled=True)

    first_name = forms.CharField(disabled=True)
    last_name = forms.CharField(disabled=True)
    email = forms.CharField(disabled=True)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']


class ProfileChangeForm(forms.ModelForm):
    username = forms.CharField(disabled=True)
    sex = forms.ChoiceField(required=False, choices=[('男', '男'), ('女', '女')])
    birth_date = forms.DateField(required=False, help_text='示例：xxxx-xx-xx')
    introduce_text = forms.CharField(required=False, max_length=50, widget=forms.Textarea)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']


class PasswordChangeForm(forms.Form):
    password = forms.CharField(max_length=20, widget=PasswordInput)
    new_password = forms.CharField(max_length=20, widget=PasswordInput)
    renew_password = forms.CharField(max_length=20, widget=PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        p = cleaned_data.get("new_password")
        rp = cleaned_data.get("renew_password")

        if p and rp:
            # Only do something if both fields are valid so far.
            if p != rp:
                raise ValidationError("Inputs for password doesn't equal.")
                # 引发验证错误表单的密码输入项会清空，其他项会保留
