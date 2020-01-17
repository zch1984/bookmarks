from django.db import models
from django.conf import settings
from django.utils.text import slugify


# Create your models here.
class Image(models.Model):
    # 设定图像数千的user对象,并定义为一个外键字段————此处定义了一个一对多的关系。
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='images_created', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, blank=True)  # 表示一个简短标题，仅包含字母、数字、下划线或者连字符，用于构建SEO友好链接
    url = models.URLField()   # 表示图像原始的URL
    image = models.ImageField(upload_to='images/%Y/%m/%d/')   # 表示图像文件
    description = models.TextField(blank=True)    # 可选的图像描述
    created = models.DateField(auto_now_add=True, db_index=True)   # auto_now_add是记录创建时间，db_index=True则是在数据库中创建该字段索引
    # 其中related_name字段是创建出来关联两个模型，Image和User都有的字段。
    # ManyToManyField（）提供了一个多对多的管理器，从而可检索相关的对象，如image.users_like.all()或者user.images_like.all()中检索
    user_like = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='images_liked', blank=True)   # 多对多字段

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):   # 覆写save方法
        if not self.slug:      # 如果slug不存在
            self.slug = slugify(self.title)   # 使用slugify方法，根据self.title标题自动生成图像的slug
        super(Image, self).save(*args, **kwargs)