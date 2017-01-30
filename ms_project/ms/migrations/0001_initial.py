# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('name', models.CharField(verbose_name='公司名称', max_length=30)),
                ('address', models.CharField(verbose_name='公司地址', max_length=50, blank=True)),
                ('phone', models.CharField(verbose_name='联系电话', max_length=20)),
            ],
            options={
                'verbose_name_plural': '客户',
                'verbose_name': '客户',
                'ordering': ['-name'],
            },
        ),
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('name', models.CharField(verbose_name='姓名', max_length=20)),
                ('phone', models.CharField(verbose_name='电话', max_length=20)),
                ('email', models.EmailField(verbose_name='邮箱', max_length=254, blank=True)),
                ('company', models.ForeignKey(verbose_name='公司名称', to='ms.Company')),
            ],
            options={
                'verbose_name_plural': '联系人',
                'verbose_name': '联系人',
                'ordering': ['-company'],
            },
        ),
        migrations.CreateModel(
            name='Cotton',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('name', models.CharField(verbose_name='类型', max_length=10)),
                ('weight', models.IntegerField(verbose_name='重量')),
                ('width', models.FloatField(verbose_name='宽度', blank=True, default='1.5')),
                ('length', models.FloatField(verbose_name='米数', blank=True)),
                ('inTime', models.DateField(verbose_name='入库时间', blank=True, null=True)),
                ('image', models.ImageField(upload_to='uploads/ms/projects/cotton/', verbose_name='原文件', blank=True)),
                ('comment', models.CharField(verbose_name='备注', max_length=100, blank=True)),
            ],
            options={
                'verbose_name_plural': '棉',
                'verbose_name': '棉',
                'ordering': ['-project'],
            },
        ),
        migrations.CreateModel(
            name='Delivery',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('num', models.CharField(default='无', verbose_name='缸号', max_length=10, blank=True)),
                ('color', models.CharField(verbose_name='颜色', max_length=10, null=True, blank=True)),
                ('length', models.FloatField(verbose_name='送出米数', blank=True, null=True)),
                ('outDate', models.DateField(verbose_name='发货日期', blank=True, null=True)),
                ('image', models.ImageField(upload_to='uploads/ms/projects/delivery/', verbose_name='发货单', blank=True)),
                ('comment', models.CharField(verbose_name='备注', max_length=100, blank=True)),
            ],
            options={
                'verbose_name_plural': '出货单',
                'verbose_name': '出货单',
                'ordering': ['-outDate'],
            },
        ),
        migrations.CreateModel(
            name='Emp',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('name', models.CharField(verbose_name='姓名', max_length=10)),
                ('phone', models.CharField(verbose_name='电话', max_length=15, blank=True)),
                ('address', models.CharField(verbose_name='地址', max_length=50, blank=True)),
                ('joinDate', models.DateField(verbose_name='入职时间', blank=True, null=True)),
                ('leaveDate', models.DateField(verbose_name='离职时间', blank=True, null=True)),
                ('comment', models.CharField(verbose_name='备注', max_length=100, blank=True)),
                ('onduty', models.CharField(choices=[('0', '离职'), ('1', '在职')], verbose_name='状态', max_length=1, default='1')),
            ],
            options={
                'verbose_name_plural': '员工',
                'verbose_name': '员工',
                'ordering': ['-name'],
            },
        ),
        migrations.CreateModel(
            name='Flower',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('name', models.CharField(verbose_name='花型名称', max_length=10)),
                ('comment', models.CharField(verbose_name='备注', max_length=100, blank=True)),
                ('image', models.ImageField(upload_to='uploads/ms/flowers/', verbose_name='图形样例', blank=True)),
                ('dstfile', models.FileField(upload_to='uploads/ms/flowers/DST', verbose_name='制图文件', blank=True)),
            ],
            options={
                'verbose_name_plural': '花型',
                'verbose_name': '花型',
                'ordering': ['-name'],
            },
        ),
        migrations.CreateModel(
            name='Machine',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('name', models.CharField(verbose_name='机器名称', max_length=15)),
                ('step_1_2', models.FloatField(verbose_name='前后间距-1')),
                ('step_2_3', models.FloatField(verbose_name='前后间距-2')),
                ('space', models.FloatField(verbose_name='左右间距')),
            ],
            options={
                'verbose_name_plural': '机器',
                'verbose_name': '机器',
                'ordering': ['-name'],
            },
        ),
        migrations.CreateModel(
            name='Material',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('num', models.CharField(default='无', verbose_name='缸号', max_length=10, blank=True)),
                ('color', models.CharField(verbose_name='颜色', max_length=10)),
                ('length', models.FloatField(verbose_name='米数')),
                ('inTime', models.DateField(verbose_name='入库时间', blank=True, null=True)),
                ('image', models.ImageField(upload_to='uploads/ms/projects/material/', verbose_name='原文件', blank=True)),
                ('comment', models.CharField(verbose_name='备注', max_length=100, blank=True)),
            ],
            options={
                'verbose_name_plural': '布料',
                'verbose_name': '布料',
                'ordering': ['-project'],
            },
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('name', models.CharField(verbose_name='项目名称', max_length=30)),
                ('createDate', models.DateField(verbose_name='创建时间')),
                ('finishDate', models.DateField(verbose_name='完成时间', blank=True, null=True)),
                ('image', models.ImageField(upload_to='uploads/ms/projects/project/', verbose_name='原文件', blank=True)),
                ('isFinish', models.CharField(choices=[('0', '未完成'), ('1', '完成')], verbose_name='进度', max_length=1, default='0')),
                ('isClose', models.CharField(choices=[('0', '未结算'), ('1', '已结算')], verbose_name='结算', max_length=1, default='0')),
                ('comment', models.CharField(verbose_name='备注', max_length=100, blank=True)),
                ('company', models.ForeignKey(verbose_name='公司名称', to='ms.Company')),
                ('contact', models.ManyToManyField(verbose_name='项目联系人', to='ms.Contact')),
                ('flower', models.ForeignKey(verbose_name='花型', default='', blank=True, null=True, to='ms.Flower')),
            ],
            options={
                'verbose_name_plural': '项目',
                'verbose_name': '项目',
                'ordering': ['-company'],
            },
        ),
        migrations.CreateModel(
            name='Record',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('inTime', models.DateTimeField(verbose_name='上班时间', blank=True, null=True)),
                ('outTime', models.DateTimeField(verbose_name='下班时间', blank=True, null=True)),
                ('produce', models.FloatField(verbose_name='日产量', default=0.0)),
                ('comment', models.CharField(verbose_name='备注', max_length=100, blank=True)),
                ('emp', models.ForeignKey(verbose_name='员工', to='ms.Emp')),
                ('project', models.ForeignKey(verbose_name='项目', default='', to='ms.Project')),
            ],
            options={
                'verbose_name_plural': '考勤记录',
                'verbose_name': '考勤记录',
                'ordering': ['-inTime'],
            },
        ),
        migrations.CreateModel(
            name='Sample',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('name', models.CharField(verbose_name='项目名称', max_length=30)),
                ('createDate', models.DateField(verbose_name='创建时间')),
                ('image', models.ImageField(upload_to='uploads/ms/projects/sample/', verbose_name='原文件', blank=True)),
                ('comment', models.CharField(verbose_name='备注', max_length=100, blank=True)),
                ('company', models.ForeignKey(verbose_name='公司名称', to='ms.Company')),
                ('contact', models.ManyToManyField(verbose_name='项目联系人', to='ms.Contact')),
            ],
            options={
                'verbose_name_plural': '打样',
                'verbose_name': '打样',
                'ordering': ['-company'],
            },
        ),
        migrations.CreateModel(
            name='SampleMap',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('color', models.CharField(verbose_name='颜色', max_length=10)),
                ('length', models.FloatField(verbose_name='米数')),
                ('cottonName', models.CharField(verbose_name='类型', max_length=10)),
                ('cottonWeight', models.IntegerField(verbose_name='重量')),
                ('comment', models.CharField(verbose_name='备注', max_length=100, blank=True)),
                ('flower', models.ForeignKey(verbose_name='花型', default='', blank=True, null=True, to='ms.Flower')),
                ('machine', models.ForeignKey(verbose_name='加工机器', default='', blank=True, null=True, to='ms.Machine')),
            ],
            options={
                'verbose_name_plural': '加工原料',
                'verbose_name': '加工原料',
                'ordering': ['flower'],
            },
        ),
        migrations.AddField(
            model_name='sample',
            name='sampleMap',
            field=models.ManyToManyField(verbose_name='加工原料', to='ms.SampleMap'),
        ),
        migrations.AddField(
            model_name='material',
            name='project',
            field=models.ForeignKey(verbose_name='项目名称', to='ms.Project'),
        ),
        migrations.AddField(
            model_name='delivery',
            name='project',
            field=models.ForeignKey(verbose_name='项目', to='ms.Project'),
        ),
        migrations.AddField(
            model_name='cotton',
            name='project',
            field=models.ForeignKey(verbose_name='项目名称', to='ms.Project'),
        ),
    ]
