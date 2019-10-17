from django.db import models

# Create your models here.

class UserInfo(models.Model):
    """
    用户信息表
    """
    nid = models.BigAutoField(primary_key=True)
    username = models.CharField(max_length=32,verbose_name="用户名",unique=True)
    password = models.CharField(max_length=64,verbose_name="密码")
    nickname = models.CharField(max_length=32,verbose_name="昵称")
    email = models.EmailField(verbose_name="邮箱",unique=True)
    avatar = models.ImageField(verbose_name="头像",upload_to='static/user_avatar')
    createtime = models.DateTimeField(verbose_name="创建时间",auto_now_add=True)

    fans = models.ManyToManyField(verbose_name="粉丝",
                                  to="UserInfo",
                                  through="UserFans",   #自定义第三张表时，使用字段用于指定关系表
                                  related_name="f",
                                  through_fields= ("user","follower"),
                                  )

    class Meta:
        verbose_name_plural="用户列表"

    def __str__(self):
        return self.username

class UserFans(models.Model):
    """
    互粉表关系
    user :博主
    follow:粉丝
    """
    #related_name是反向操作时，使用的字段名，用于代替 【表名_set】
    user = models.ForeignKey(verbose_name="博主",on_delete=models.CASCADE,to="UserInfo",to_field="nid",related_name="users")
    follower = models.ForeignKey(verbose_name="粉丝",on_delete=models.CASCADE,to="UserInfo",to_field="nid",related_name="followers")
    class Meta:
        #联合唯一
        unique_together = [
            ("user","follower"),
        ]

class Blog(models.Model):
    """
    个人博客信息
    """
    bid = models.AutoField(primary_key=True)
    title = models.CharField(max_length=60,verbose_name="个人博客标题")
    site  = models.CharField(max_length=32,verbose_name="个人博客前缀",unique=True)
    theme = models.CharField(max_length=32,verbose_name="博客主题")
    user = models.OneToOneField(to="UserInfo",to_field="nid",on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural="个人博客"

    def __str__(self):
        return self.title

class IssueInfo(models.Model):
    """
    故障单信息
    """

    uuid = models.UUIDField()
    title = models.CharField(max_length=60,verbose_name="故障标题")
    detail = models.TextField(verbose_name="故障详情")
    user = models.ForeignKey(verbose_name="提单人",to="UserInfo",to_field="nid",on_delete=models.CASCADE,related_name="user")
    processor = models.ForeignKey(verbose_name="责任人",to="UserInfo",to_field="nid",on_delete=models.CASCADE,related_name="processor",null=True,blank=True)
    status_type = [
        (1,"待处理"),
        (2,"处理中"),
        (3,"已处理"),
    ]
    status = models.IntegerField(choices=status_type)
    create_time = models.DateTimeField(verbose_name="创建时间",auto_now_add=True)
    endtime = models.DateTimeField(verbose_name="处理时间",null=True,blank=True)

    class Meta:
        verbose_name_plural="故障单信息"

    def __str__(self):
        return self.title

class Category(models.Model):
    """
    个人文章分类
    """
    nid = models.AutoField(primary_key=True)
    title = models.CharField(verbose_name="分类名称",max_length=32)
    blog = models.ForeignKey(verbose_name="所属博客",to="Blog",to_field="bid",on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural="个人文章分类"

class Tag(models.Model):
    """
    标签表
    """
    nid = models.AutoField(primary_key=True)
    title = models.CharField(verbose_name="标签名称",max_length=32)
    blog = models.ForeignKey(verbose_name="所属博客",to="Blog",to_field="bid",on_delete=models.CASCADE)

class Article(models.Model):
    """
    文章表
    """
    nid = models.BigAutoField(primary_key=True)
    title = models.CharField(verbose_name="文章标题",max_length=128)
    summary = models.CharField(verbose_name="文章简介",max_length=512)
    read_count = models.IntegerField(default=0)
    comment_count = models.IntegerField(default=0)
    up_count = models.IntegerField(default=0)
    down_count = models.IntegerField(default=0)
    create_time = models.DateTimeField(auto_now_add=True)
    blog = models.ForeignKey(verbose_name="所属博客",to="Blog",to_field="bid",on_delete=models.CASCADE)
    category = models.ForeignKey(verbose_name="文章类型",to="Category",to_field="nid",on_delete=models.CASCADE)
    article_type_choices = [
        (1,"Python"),
        (2,"Linux"),
        (3,"Java"),
        (4,"Golang"),
    ]
    article_type_id = models.IntegerField(verbose_name="主站分类id",choices=article_type_choices,default=None)
    tag = models.ManyToManyField(
        verbose_name="文章标签",
        to="Tag",
        through="Tag2Article",

    )
    class Meta:
        verbose_name_plural="文章信息"

class Tag2Article(models.Model):
    """
    文章与标签关系表
    """

    tag = models.ForeignKey(verbose_name="标签",to="Tag",to_field="nid",on_delete=models.CASCADE)
    article = models.ForeignKey(verbose_name="文章",to="Article",to_field="nid",on_delete=models.CASCADE)

    class Meta:
        unique_together = [
            ("tag","article"),
        ]

class ArticleDetail(models.Model):
    """
    文章内容表
    """
    content = models.TextField(verbose_name="文章内容")
    article= models.ForeignKey(verbose_name="所属文章",to="Article",to_field="nid",on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural="文章内容"

class UpDown(models.Model):
    """
    文章点赞关系
    """
    article = models.ForeignKey(verbose_name="所属文章",to="Article",to_field="nid",on_delete=models.CASCADE)
    user = models.ForeignKey(verbose_name="踩或赞用户",to="UserInfo",to_field="nid",on_delete=models.CASCADE)
    up = models.BooleanField(verbose_name="是否赞")

    class Meta:
        verbose_name_plural = "文章点赞关系"
        unique_together = [
            ("article","user"),
        ]


class Comment(models.Model):
    nid = models.BigIntegerField(primary_key=True)
    content = models.CharField(verbose_name="评论内容",max_length=256)
    create_time = models.DateTimeField(auto_now_add=True)
    reply = models.ForeignKey(verbose_name="回复评论",to="self",null=True,blank=True,on_delete=models.CASCADE)
    article = models.ForeignKey(verbose_name="评论文章", to="Article", to_field="nid", on_delete=models.CASCADE)
    user = models.ForeignKey(verbose_name="评论用户", to="UserInfo", to_field="nid", on_delete=models.CASCADE)
    class Meta:
        verbose_name_plural="评论信息"