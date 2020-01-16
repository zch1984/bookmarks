from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views


"""
LoginView：处理登录表单并实现用户登录操作
LogoutView：注销某个用户
PasswordChangeView：处理某个表单并修改用户密码
PasswordChangeDoneView：密码被成功修改后，用户将被重定向至成功试图页面
PasswordResetView：允许用户重定向密码，并生成包含令牌的一次性使用链接，同时将其发送至用户的电子邮箱账户中。
PasswordResetDoneView：通知用户，一封电子邮件（包含重置密码的来链接）已被发送
PasswordResetConfirmView：允许用户设置新的密码
PasswordResetCompleteView：密码重置成功后，用户被重定向至成功视图页面。
"""
urlpatterns = [
    # previous login views
    # path('login/', views.user_login, name='login'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('', views.dashboard, name='dashboard'),
    # change password urls
    path('password_change/', auth_views.PasswordChangeView.as_view(), name="password_change"),
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(), name="password_change_done"),
    # reset password urls
    path('password_reset/', auth_views.PasswordResetView.as_view(), name="password_reset"),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name="password_reset_done"),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name="password_reset_confirm"),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name="password_reset_complete"),
    # 包含身份验证视图的替代方法
    # path('', include('django.contrib.auth.urls')),
    path('register/', views.register, name='register'),
    path('edit/', views.edit, name='edit'),
]
