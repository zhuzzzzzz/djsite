from django.shortcuts import render, redirect
from django.views.generic.edit import FormView
from django.views.generic.base import TemplateView
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import LoginForm, RegisterForm, ProfileForm, ProfileChangeForm, PasswordChangeForm
from .models import Profile


def index(request):
    print(f'"view.index": request user authenticated: {request.user.is_authenticated}')
    print(f'"view.index": request user: {request.user.username}')
    context = {
        'log_state': request.user.is_authenticated,
        'log_user': request.user.username,
    }
    return render(request, "account/index_template.html", context)


class LoginView(FormView):
    template_name = "account/login_template.html"
    form_class = LoginForm
    success_url = "/account"
    extra_context = {}

    def get(self, request, *args, **kwargs):
        self.extra_context['log_state'] = self.request.user.is_authenticated
        self.extra_context['log_user'] = self.request.user.username
        return self.render_to_response(self.get_context_data())

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        username = form.cleaned_data["username"]
        password = form.cleaned_data["password"]
        user = authenticate(self.request, username=username, password=password)
        print(user)
        print(self.request.user)
        self.extra_context['logging_user'] = username
        if user is not None:
            login(self.request, user)
            return super().form_valid(form)
        else:
            return self.render_to_response(
                self.get_context_data(form=LoginForm(initial={"username": form.cleaned_data["username"]}),
                                      prompt='密码错误！'))
            # form=LoginForm() 重新初始化一个表单对象以返回一个空表单，并传入当前用户名的initial参数


def Logout(request):
    logout(request)
    return redirect('account:index')


# 使用普通表单对应的注册视图
# class RegisterView(FormView):
#     template_name = "login_template.html"
#     form_class = RegisterForm
#     success_url = "/account"
#
#     def form_valid(self, form):
#         # This method is called when valid form data has been POSTed.
#         # It should return an HttpResponse.
#         print(form.cleaned_data)
#         username = form.cleaned_data["username"]
#         password = form.cleaned_data["password"]
#         email = form.cleaned_data["email"]
#         first_name = form.cleaned_data["first_name"]
#         last_name = form.cleaned_data["last_name"]
#         user = User.objects.create_user(username, email, password)
#         user.first_name = first_name
#         user.last_name = last_name
#         user.save()
#
#         return super().form_valid(form)


class RegisterView(FormView):
    template_name = "account/register_template.html"
    form_class = RegisterForm
    success_url = "/account/login"
    extra_context = {}

    def get(self, request, *args, **kwargs):
        self.extra_context['log_state'] = self.request.user.is_authenticated
        self.extra_context['log_user'] = self.request.user.username
        return self.render_to_response(self.get_context_data())

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        print(form.cleaned_data)
        # 注销的部分是因为刚开始写完密码存进去不是哈希的
        # 后加了两行对instance的强赋值得到解决，目前的解决方法是在表单的clean()上对密码进行哈希转换
        # form.cleaned_data['password'] = make_password(form.cleaned_data['password'])
        # print(form.cleaned_data)
        # print(form.instance)
        form.save()
        # form.instance.password = form.cleaned_data['password']
        # form.save()
        return super().form_valid(form)


class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = "account/profile_template.html"
    extra_context = {}

    def get_context_data(self, **kwargs):
        self.extra_context['log_state'] = self.request.user.is_authenticated
        self.extra_context['log_user'] = self.request.user.username
        context = super().get_context_data(**kwargs)
        user = self.request.user
        u_d = {
            'username': user.username,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email,
        }
        if hasattr(user, 'profile'):
            p_d = {
                'sex': user.profile.sex,
                'birth_date': user.profile.birth_date,
                'introduce_text': user.profile.introduce_text,
            }
        else:
            p_d = {
                'sex': None,
                'birth_date': None,
                'introduce_text': None,
            }
        u_d.update(p_d)
        context['info_dict'] = u_d
        return context


class ProfileChangeView(LoginRequiredMixin, FormView):
    template_name = "account/setProfile_template.html"
    form_class = ProfileChangeForm
    success_url = "/account/profile"
    extra_context = {}

    def get(self, request, *args, **kwargs):
        """Handle GET requests: instantiate a blank version of the form."""
        self.extra_context['log_state'] = self.request.user.is_authenticated
        self.extra_context['log_user'] = self.request.user.username
        user = request.user
        u_d = {
            'username': user.username,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email,
        }
        if hasattr(user, 'profile'):
            p_d = {
                'sex': user.profile.sex,
                'birth_date': user.profile.birth_date,
                'introduce_text': user.profile.introduce_text,
            }
            u_d.update(p_d)
        return self.render_to_response(self.get_context_data(form=self.form_class(initial=u_d)))

    def post(self, request, *args, **kwargs):
        """
        Handle POST requests: instantiate a form instance with the passed
        POST variables and then check if it's valid.
        """
        self.initial = {'username': request.user.username}  # 每次都更新当前要创建表单的用户名初始值，因为Form中的字段设置了disable选项后将不会被post
        form = self.get_form()
        form.instance = self.request.user  # 指定form对应的实例对象，否则django默认要新建一个数据库对象
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        print(form.cleaned_data)

        # 必须要有这个if，否则会引发 Exception Value: User has no profile.
        if not hasattr(form.instance, 'profile'):
            temp_p = Profile(user=self.request.user)

        form.instance.profile.sex = form.cleaned_data['sex']
        form.instance.profile.birth_date = form.cleaned_data['birth_date']
        form.instance.profile.introduce_text = form.cleaned_data['introduce_text']
        form.save()
        form.instance.profile.save()
        return super().form_valid(form)


class PasswordChangeView(LoginRequiredMixin, FormView):
    template_name = "account/register_template.html"
    form_class = PasswordChangeForm
    success_url = "/account/profile"

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        password = form.cleaned_data['password']
        user = authenticate(username=self.request.user, password=password)
        if user is not None:
            new_password = form.cleaned_data['new_password']
            user = self.request.user
            user.set_password(new_password)
            user.save()
            return super().form_valid(form)
        else:
            return super().form_invalid(form)
