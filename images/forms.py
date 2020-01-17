from django import forms
from .models import Image
from urllib import request
from django.core.files.base import ContentFile
from django.utils.text import slugify


class ImageCreateForm(forms.ModelForm):
    def clean_url(self):   # 自定义了该方法并清空url字段。工作方式：（1）通过访问表单实例的目录，可获得url字段。（2）解析URL并获得文件扩展名，并检测是否为有效扩展名。若无效抛出异常，表单实例不会被验证
        url = self.cleaned_data['url']
        valid_extensions = ['jpg', 'jpeg']
        extension = url.rsplit('.', 1)[1].lower()
        if extension not in valid_extensions:
            raise forms.ValidationError('The given URL does not match valid image extensions.')
        return url

    def save(self, force_insert=False, force_update=False, commit=True):   # 覆写save方法，同时保留了ModelForm所需要的参数。
        image = super(ImageCreateForm, self).save(commit=False)   # 通过调用表单的save()方法（commit=False），创建新的image实例
        image_url = self.cleaned_data['url']   # 从表单的cleaned_data目录中获取URL
        # 将image标题的slug与原始文件口占名进行整合，生成图像名称
        image_name = '{}.{}'.format(slugify(image.title), image_url.rsplit('.', 1)[1].lower())

        # download image from the given URL
        response = request.urlopen(image_url)  # 通过图像链接获取图像对象response
        # ContentFile()利用下载图像内容实例化对象，response.read()以字节的形式读取该对象，save=False为暂时不保存。
        # save()方法是图像字段的方法，将其保存在media目录中
        image.image.save(image_name, ContentFile(response.read()), save=False)

        if commit:  # 为了保持与覆写的save()方法相一致的行为，仅当commit参数为True时，方可将表单保存至数据库
            image.save()
        return image

    class Meta:
        model = Image    # 构建于Image模型
        fields = ('title', 'url', 'description')    # 包含的字段
        widgets = {
            'url': forms.HiddenInput,    # 覆写url字段的微件，以使用HiddenInput微件。该微件基于type="hidden"属性显示为HTML input元素。
        }