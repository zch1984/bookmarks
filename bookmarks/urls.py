"""bookmarks URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static    # static()帮助函数适用于开发环境，而非产品应用环境。不要在产品环境中为Django提供静态文件

urlpatterns = [
    path('admin/', admin.site.urls),
    path('account/', include('account.urls')),      # 添加account路由
    path('social-auth/', include('social_django.urls', namespace='social')),   # 第三方登录路由
    path('images/', include('images.urls', namespace='images')),        # 添加images路由
]

if settings.DEBUG:   # 通过这一方式，Django开发服务器将负责在开发期间为媒体文件提供服务（也就是说DEBUG设置为True）
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)