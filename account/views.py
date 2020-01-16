from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth import authenticate, login
from .forms import LoginForm, UserRegistrationForm, UserEditForm, ProfileEditForm
from django.contrib.auth.decorators import login_required
from .models import Profile
from django.contrib import messages


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)  # 实例化包含表提交数据的表单
        if form.is_valid():  # 检验表单是否有效
            cd = form.cleaned_data
            # authenticate()方法根据数据库对用户予以验证。该方法接收request、username、password参数，并返回User或None。
            user = authenticate(request, username=cd['username'], password=cd['password'])
            if user is not None:
                if user.is_active:  # is_active是访问用户的active属性，检查用户是否处于活动状态
                    login(request, user)  # login()方法，会将数据库中的对象于提交的进行匹配验证，并在当前会话中设置用户
                    return HttpResponse('Authenticated successfully')
                else:
                    return HttpResponse('Disabled account')  # 如果active属性为False，则告知其为不可用账户
            else:
                return HttpResponse('Invalid login')  # 当user为None时返回无效的登录
    else:
        form = LoginForm()
    return render(request, 'account/login.html', {'form': form})


@login_required    # 验证框架中的login_required装饰器，检测当前用户是否已被验证。若是，则执行装饰器后的视图；若否，则利用最初请求的URL作为参数（名为next）将用户重定向至登录URL
def dashboard(request):
    return render(request, 'account/dashboard.html', {'section': 'dashboard'})


def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            # 如果传进来的表单验证通过，则建立新的表单对象但是不提交数据库
            new_user = user_form.save(commit=False)
            # 设置该用户的密码为传递过来的password,set_password()方法会对密码进行加密
            new_user.set_password(user_form.cleaned_data['password'])
            # 将该用户保存至数据库
            new_user.save()
            # 创建profile用户
            Profile.objects.create(user=new_user)
            return render(request, 'account/register_done.html', {'new_user': new_user})
    else:
        user_form = UserRegistrationForm()
    return render(request, 'account/register.html', {'user_form': user_form})


@login_required
def edit(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user, data=request.POST)
        profile_form = ProfileEditForm(instance=request.user.profile, data=request.POST, files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Profile updated successfully')
        else:
            messages.error(request, 'Error updating your profile')
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)
    return render(request, 'account/edit.html', {'user_form': user_form, 'profile_form': profile_form})
# Create your views here.
