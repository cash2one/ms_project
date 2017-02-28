from django.db import models
import time

# 客户
class Company(models.Model):
    name = models.CharField('公司名称', max_length=30)
    address = models.CharField('公司地址', max_length=50, blank=True)
    phone = models.CharField('联系电话', max_length=20)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '客户'
        verbose_name_plural = verbose_name
        ordering = ['-name']


# 联系人
class Contact(models.Model):
    name = models.CharField('姓名', max_length=20)
    phone = models.CharField('电话', max_length=20)
    email = models.EmailField('邮箱', blank=True)
    company = models.ForeignKey(Company,verbose_name='公司名称', on_delete=models.CASCADE,)

    def __str__(self):
        return u'%s - %s' % (self.company.name, self.name)

    class Meta:
        verbose_name = '联系人'
        verbose_name_plural = verbose_name
        ordering = ['-company']


# 花型
class Flower(models.Model):
    name = models.CharField(verbose_name='花型名称',max_length=50)
    comment = models.CharField(verbose_name='备注',max_length=100, blank=True)
    image = models.ImageField(verbose_name='图形样例',upload_to='uploads/ms/flowers/', blank=True)  # 图片样例
    dstfile = models.FileField(verbose_name='制图文件',upload_to='uploads/ms/flowers/DST', blank=True) # 制图文件

    def __str__(self):
        return u'%s' % (self.name)

    def fileName(self):
        return self.dstfile.__str__().split('/')[-1]

    fileName.short_description = '文件名'

    class Meta:
        verbose_name = '花型'
        verbose_name_plural = verbose_name
        ordering = ['-name']


# 项目
class Project(models.Model):
    company = models.ForeignKey(Company, verbose_name='公司名称', on_delete=models.CASCADE,)
    contact = models.ManyToManyField(Contact, verbose_name='项目联系人',)
    name = models.CharField(verbose_name='项目名称', max_length=30)
    createDate = models.DateField(verbose_name='创建时间')
    finishDate = models.DateField(verbose_name='完成时间', blank=True, null= True)
    image = models.ImageField(verbose_name='原文件', upload_to='uploads/ms/projects/project/', blank=True)
    flower = models.ForeignKey(Flower, verbose_name='花型', blank=True, null= True,default='')
    isFinish = models.CharField(verbose_name='进度', max_length=1, choices=(('0', '未完成'), ('1', '完成'),), default='0')
    isClose = models.CharField(verbose_name='结算', max_length=1, choices=(('0', '未结算'), ('1', '已结算'),), default='0')
    comment = models.CharField(max_length=100,verbose_name='备注', blank=True)


    def strCreateDate(self):
        strDate = self.createDate.strftime('%Y-%m-%d')
        return strDate

    def __str__(self):
        return u'%s - %s' % (self.company.name, self.name)

    class Meta:
        verbose_name = '项目'
        verbose_name_plural = verbose_name
        ordering = ['-company']


# 布料
class Material(models.Model):
    project = models.ForeignKey(Project,verbose_name='项目名称', on_delete=models.CASCADE,)
    # 缸号
    num = models.CharField(verbose_name='缸号',max_length=10, blank=True, default='无')
    # 颜色
    color = models.CharField(verbose_name='颜色',max_length=10)
    # 米数
    length = models.FloatField(verbose_name='米数')
    # 入库时间
    inTime = models.DateField(verbose_name='入库时间', blank=True, null= True)
    image = models.ImageField(verbose_name='原文件', upload_to='uploads/ms/projects/material/', blank=True)  # 原始项目文件
    # 备注
    comment = models.CharField(verbose_name='备注',max_length=100, blank=True)


    def __str__(self):
        return u'%s - %s : 缸号[ %s ], 颜色[ %s ], 米数[ %s ]' % (self.project.company.name, self.project.name, self.num, self.color, self.length)

    class Meta:
        verbose_name = '布料'
        verbose_name_plural = verbose_name
        ordering = ['-project']


# 棉
class Cotton(models.Model):
    project = models.ForeignKey(Project, verbose_name='项目名称', on_delete=models.CASCADE,)
    # 类型
    name = models.CharField(verbose_name='类型', max_length=10)
    # 重量
    weight = models.IntegerField(verbose_name='重量')
    # 宽度
    width = models.FloatField(verbose_name='宽度', blank=True , default='1.5')
    # 米数
    length = models.FloatField(verbose_name='米数', blank=True)
    # 入库时间
    inTime = models.DateField(verbose_name='入库时间', blank=True, null= True)
    image = models.ImageField(verbose_name='原文件', upload_to='uploads/ms/projects/cotton/', blank=True)  # 原始项目文件
    # 备注
    comment = models.CharField(verbose_name='备注', max_length=100, blank=True)

    def strName(self):
        strname = self.name+' : '+str(self.weight)+' g'
        return strname

    strName.short_description = '棉名称'

    def __str__(self):
        return u'%s - %s | %s - %s ' % (self.name, self.weight, self.project.name, self.project.company.name)

    class Meta:
        verbose_name = '棉'
        verbose_name_plural = verbose_name
        ordering = ['-project']


# 机器
class Machine(models.Model):
    name = models.CharField(verbose_name='机器名称', max_length=15)
    # 前后距离 1-2
    step_1_2 = models.FloatField(verbose_name='前后间距-1')
    # 前后距离 2-3
    step_2_3 = models.FloatField(verbose_name='前后间距-2')
    # 左右两针间隔距离
    space = models.FloatField(verbose_name='左右间距')

    def __str__(self):
        return self.name + '[ ' + str(self.step_1_2) + " - " + str(self.step_2_3) + ' - ' + str(self.space) + ' ]'

    class Meta:
        verbose_name = '机器'
        verbose_name_plural = verbose_name
        ordering = ['-name']


# 员工
class Emp(models.Model):
    name = models.CharField(verbose_name='姓名', max_length=10)
    phone = models.CharField(verbose_name='电话', max_length=15, blank=True)
    address = models.CharField(verbose_name='地址', max_length=50, blank=True)
    joinDate = models.DateField(verbose_name='入职时间', blank=True, null= True)
    leaveDate = models.DateField(verbose_name='离职时间', blank=True, null= True)
    comment = models.CharField(verbose_name='备注', max_length=100, blank=True)
    onduty = models.CharField(verbose_name='状态', max_length=1, choices=(('0', '离职'), ('1', '在职'),),default='1')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '员工'
        verbose_name_plural = verbose_name
        ordering = ['-name']


class Delivery(models.Model):
    project = models.ForeignKey(Project, verbose_name='项目', on_delete=models.CASCADE,)
    # 缸号
    num = models.CharField(verbose_name='缸号',max_length=10, blank=True, default='无')
    # 颜色
    color = models.CharField(verbose_name='颜色',max_length=10, blank=True, null=True)
    length = models.FloatField(verbose_name='送出米数', blank=True, null=True)
    outDate = models.DateField(verbose_name='发货日期', blank=True, null=True)
    image = models.ImageField(verbose_name='发货单', upload_to='uploads/ms/projects/delivery/', blank=True)  # 原始项目文件
    comment = models.CharField(verbose_name='备注', max_length=100, blank=True)


    def __str__(self):
        return u'%s - %s (缸号：%s, 颜色: %s) ' %(self.project.company.name, self.project.name, self.num, self.color)

    class Meta:
        verbose_name = '出货单'
        verbose_name_plural = verbose_name
        ordering = ['-outDate']


class Record(models.Model):
    emp = models.ForeignKey(Emp, verbose_name='员工', on_delete=models.CASCADE)
    inTime = models.DateTimeField(verbose_name='上班时间', blank=True, null= True)
    outTime = models.DateTimeField(verbose_name='下班时间', blank=True, null=True)
    project = models.ForeignKey(Project, verbose_name='项目', default='')
    produce = models.FloatField(verbose_name='日产量',default=0.0)
    comment = models.CharField(verbose_name='备注', max_length=100, blank=True)

    def strInTime(self):
        strDate = self.inTime.strftime('%Y-%m-%d  %H:%m')
        return strDate

    strInTime.short_description = '上班时间'

    def strOutTime(self):
        strDate = self.outTime.strftime('%Y-%m-%d  %H:%m')
        return strDate

    strOutTime.short_description = '下班时间'

    def workDate(self):
        strDate = self.inTime.strftime('%Y-%m-%d')
        return strDate

    workDate.short_description = '工作日期'

    def workHour(self):
        hour = float((self.outTime - self.inTime).seconds / 3600)
        return hour

    workHour.short_description = '工作时长'

    def __str__(self):
        return u'%s [ %s ] 工作时长: %d 小时' % (self.emp.name, self.workDate(), self.workHour())

    class Meta:
        verbose_name = '考勤记录'
        verbose_name_plural = verbose_name
        ordering = ['-inTime']


class SampleMap(models.Model):
    flower = models.ForeignKey(Flower, verbose_name='花型', blank=True, null=True, default='')
    # 颜色
    color = models.CharField(verbose_name='颜色',max_length=10)
    # 米数
    length = models.FloatField(verbose_name='米数')
    # 类型
    cottonName = models.CharField(verbose_name='类型', max_length=10)
    # 重量
    cottonWeight = models.IntegerField(verbose_name='重量')

    machine = models.ForeignKey(Machine, verbose_name='加工机器', on_delete=models.CASCADE, blank=True, null=True, default='')

    comment = models.CharField(max_length=100, verbose_name='备注', blank=True)

    def __str__(self):
        return u'花型：%s , %s 布料 %s 米, %s %s 克 - 机器：%s' % (self.flower.name, self.color, self.length, self.cottonName, self.cottonWeight, self.machine.name)

    class Meta:
        verbose_name = '加工原料'
        verbose_name_plural = verbose_name
        ordering = ['flower']


    # 打样
class Sample(models.Model):
    company = models.ForeignKey(Company, verbose_name='公司名称', on_delete=models.CASCADE, )
    contact = models.ManyToManyField(Contact, verbose_name='项目联系人', )
    name = models.CharField(verbose_name='项目名称', max_length=30)
    createDate = models.DateField(verbose_name='创建时间')
    image = models.ImageField(verbose_name='原文件', upload_to='uploads/ms/projects/sample/', blank=True)
    sampleMap = models.ManyToManyField(SampleMap, verbose_name='加工原料',)
    comment = models.CharField(max_length=100, verbose_name='备注', blank=True)

    def __str__(self):
        return u'%s - %s' % (self.company.name, self.name)

    class Meta:
        verbose_name = '打样'
        verbose_name_plural = verbose_name
        ordering = ['-company']