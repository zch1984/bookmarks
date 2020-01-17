from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import ImageCreateForm
# Create your views here.


@login_required  # 防止未验证用户的访问行为
def image_create(request):
    if request.method == 'POST':
        # form is sent
        form = ImageCreateForm(data=request.POST)
        if form.is_valid():
            # from data is valid
            cd = form.cleaned_data  # 清洗数据
            new_item = form.save(commit=False)  # 将form数据保存至new_item变量中，但是不提交到数据库False

            # assign current user to the item
            new_item.user = request.user  # 将request中关于user的对象信息数组形式，保存到new_item表单对象中，完善image中对象信息
            new_item.save()  # 将得到的数据保存并提交到数据库
            messages.success(request, 'Image added successfully')  # 消息系统提示用户成功保存Image

            # redirect to new created item detail view
            return redirect(new_item.get_absolute_url())  # 重定向至get_absolute_url()方法指定的页面
    else:
        # build form with data provided by the bookmarklet via GET
        form = ImageCreateForm(data=request.GET)  # 如果是以GET方式传递过来，就创建一个form接收数据

    return render(request, 'images/image/create.html', {'section': 'images', 'form': form})

