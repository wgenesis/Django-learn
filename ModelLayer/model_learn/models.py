from django.db import models
import datetime
# Create your models here.
class Person(models.Model):
    '''
    每个属性表示表的某一列
    '''
    first_name=models.CharField(max_length=30)
    last_name=models.CharField(max_length=30)
    birth_date=models.DateField()
    
    def bady_boomer_status(self):
        '''
        判断是否是婴儿潮时期出生
        '''
        if self.birth_date<datetime.date(1945,8,1):
            return "早于婴儿潮时期"
        elif self.birth_date<datetime.date(1965,1,1):
            return "出生于婴儿潮时期"
        else:
            return "晚于婴儿潮时期"
        
    @property
    def full_name(self):
        '''
        返回全名
        '''
        return '{} {}'.format(first_name,last_name)
    
    def __str__(self):
        return "{} {}".format(self.first_name,self.last_name)
    
class Musician(models.Model):
    first_name=models.CharField(max_length=50)
    last_name=models.CharField(max_length=50)
    instrument=models.CharField(max_length=100)
    
    def __str__(self):
        return '{} {}'.format(self.first_name,self.last_name)
    
class Album(models.Model):
    #定义多对一的关系：一个专辑可以有多名艺术家
    #on_delete=models.CASCAD定义级联删除，即删除主表时，从表数据也会一并删除
    #外键要定义在‘多’的一方
    artist=models.ForeignKey(Musician,on_delete=models.CASCADE)
    name=models.CharField(max_length=100)
    release_date=models.DateField()
    num_stars=models.IntegerField()
    
    def __str__(self):
        return self.name
    
class Comment(models.Model):
    title=models.CharField(max_length=128)
    text=models.TextField()
    #一个递归外键
    parent_comment=models.ForeignKey('self',on_delete=models.CASCADE)
    
class FileModel(models.Model):
    #文件被保存至‘MEDIS_ROOT/upload/{年}/{月}/{日}’目录中
    upload=models.FileField(upload_to='uploads/%Y/%m/%d/')
    
'''
回调函数形式：
def user_directory_path(instance, filename):
    #必须接受两个参数
    #文件上传到MEDIA_ROOT/user_<id>/<filename>目录中
    #user_directory_path这种回调函数，必须接收两个参数，然后返回一个Unix风格的路径字符串。
    #参数instace代表一个定义了FileField的模型的实例，说白了就是当前数据记录。
    #filename是原本的文件名。
    return 'user_{0}/{1}'.format(instance.user.id, filename)

class MyModel(models.Model):
    upload = models.FileField(upload_to=user_directory_path)
'''

# class Person(models.Model):
#     name = models.CharField(max_length=50)

class Group(models.Model):
    name = models.CharField(max_length=128)
    members = models.ManyToManyField(
        Person,
        through='Membership',       ## 自定义中间表
        through_fields=('group', 'person'),
    )

class Membership(models.Model):  # 这就是具体的中间表模型
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    inviter = models.ForeignKey(
        Person,
        on_delete=models.CASCADE,
        related_name="membership_invites",
    )
    invite_reason = models.CharField(max_length=64)