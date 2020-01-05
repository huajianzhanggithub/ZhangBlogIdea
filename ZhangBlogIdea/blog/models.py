import mistune
from django.contrib.auth.admin import User
from django.core.cache import cache
from django.db import models

# Create your models here.
from django.utils.functional import cached_property


class Category(models.Model):
    STATUS_NORMAL = 1
    STATUS_DELETE = 0
    STATUS_ITEMS = (
        (STATUS_NORMAL, '正常'),
        (STATUS_DELETE, '删除'),
    )

    name = models.CharField(max_length=50, verbose_name='名称')
    status = models.PositiveIntegerField(
        default=STATUS_NORMAL, choices=STATUS_ITEMS, verbose_name='状态')
    is_nav = models.BooleanField(default=False, verbose_name='是否为导航')
    owner = models.ForeignKey(User, verbose_name='作者',
                              on_delete=models.CASCADE)
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = verbose_name_plural = '分类'

    @classmethod
    def get_navs(cls):
        categories = cls.objects.filter(status=cls.STATUS_NORMAL)
        nav_categories = []
        normal_categoryies = []
        for cate in categories:
            if cate.is_nav:
                nav_categories.append(cate)
            else:
                normal_categoryies.append(cate)

        return {
            'navs': nav_categories,
            'categories': normal_categoryies,
        }


class Tag(models.Model):
    STATUS_NORMAL = 1
    STATUS_DELETE = 0
    STATUS_ITEMS = (
        (STATUS_NORMAL, '正常'),
        (STATUS_DELETE, '删除'),
    )

    name = models.CharField(max_length=10, verbose_name='名称')
    status = models.PositiveIntegerField(
        default=STATUS_NORMAL, choices=STATUS_ITEMS, verbose_name='状态')
    owner = models.ForeignKey(User, verbose_name='作者',
                              on_delete=models.CASCADE)
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = verbose_name_plural = '标签'


class Post(models.Model):
    STATUS_NORMAL = 1
    STATUS_DELETE = 0
    STATUS_DRAFT = 2
    STATUS_ITEMS = (
        (STATUS_NORMAL, '正常'),
        (STATUS_DELETE, '删除'),
        (STATUS_DRAFT, '草稿')
    )

    title = models.CharField(max_length=255, verbose_name='标题')
    desc = models.CharField(max_length=1024, blank=True, verbose_name='摘要')
    content = models.TextField(verbose_name='正文', help_text='正文必须为MarkDown格式')
    is_md = models.BooleanField(default=False, verbose_name="Markdown语法")  # 是否使用Markdown语法
    content_html = models.TextField(verbose_name="正文HTML代码", blank=True, editable=False)
    status = models.PositiveIntegerField(default=STATUS_NORMAL,
                                         choices=STATUS_ITEMS,
                                         verbose_name='状态')
    category = models.ForeignKey(
        Category, verbose_name='分类', on_delete=models.CASCADE)
    tag = models.ManyToManyField(Tag, verbose_name='标签')
    owner = models.ForeignKey(User, verbose_name='作者',
                              on_delete=models.CASCADE)
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    pv = models.PositiveIntegerField(default=1)
    uv = models.PositiveIntegerField(default=1)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = verbose_name_plural = '文章'
        ordering = ['-id']  # 根据id进行降序排列

    @staticmethod
    def get_by_tag(tag_id):
        try:
            tag = Tag.objects.get(id=tag_id)
        except Tag.DoesNotExist:
            tag = None
        else:
            post_list = tag.post_set.filter(status=Post.STATUS_NORMAL)
        return post_list, tag

    @staticmethod
    def get_by_category(category_id):
        try:
            category = Category.objects.get(id=category_id)
        except Category.DoesNotExist:
            category = None
        else:
            post_list = category.post_set.filter(status=Post.STATUS_NORMAL) \
                .select_related('owner', 'category', 'tag', 'created_time')
        return post_list, category

    @classmethod
    def latest_posts(cls, with_related=True):
        queryset = cls.objects.filter(status=cls.STATUS_NORMAL)
        if with_related:
            queryset = queryset.select_related('owner', 'category')
        return queryset

    @classmethod
    def hot_posts(cls):
        result = cache.get('hot_posts')
        if not result:
            result = cls.objects.filter(status=cls.STATUS_NORMAL).order_by('-pv').only('title')
            cache.set('hot_posts', result, 10 * 60)
        return result

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        if self.is_md:
            self.content_html = mistune.markdown(self.content)
        else:
            self.content_html = self.content
        super().save(force_insert=False, force_update=False, using=None,
                     update_fields=None)

    @cached_property
    def tags(self):
        return ','.join(self.tag.values_list('name', flat=True))
