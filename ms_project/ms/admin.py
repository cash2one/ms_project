from django.contrib import admin
from django.contrib.admin import AdminSite
# Register your models here.
from ms import models

admin.site.site_header = '莫氏绗缝绣饰中心 信息管理系统'
admin.site.site_title = '莫氏绗缝绣饰中心'
admin.site.index_title = ''



class ProjectAdmin(admin.ModelAdmin):
    list_display = ('company', 'name', 'createDate', 'flower', 'comment')
    search_fields = ('company__name', 'name', 'flower__name',)
    list_filter = ('company',)
    ordering = ('-createDate',)
    filter_horizontal = ('contact',)


class MaterialAdmin(admin.ModelAdmin):
    list_display = ('project', 'num', 'color', 'length', 'inTime', 'comment')
    search_fields = ('project__name', 'num', )
    list_filter = ('project__company__name', 'project__name',)


class CottonAdmin(admin.ModelAdmin):
    list_display = ('project', 'name', 'weight', 'width', 'length',  'inTime', 'comment')
    search_fields = ('project__name', 'name', 'weight',)
    list_filter = ('project__company__name', 'project__name', 'name')
    ordering = ('-inTime',)


class EmpAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone')
    search_fields = ('name',)


class ContactAdmin(admin.ModelAdmin):
    list_display = ('company', 'name', 'phone')
    search_fields = ('company__name', 'name',)
    list_filter = ('company__name',)


class DeliveryAdmin(admin.ModelAdmin):
    list_display = ('project', 'num', 'color', 'length', 'outDate','comment')
    #list_display_links = ('companyName', 'projectName', )
    #search_fields = ('material__project__name', )
    #list_filter = ('material__project__company__name',)
    date_hierarchy = 'outDate'


class RecordAdmin(admin.ModelAdmin):
    list_display = ('emp', 'strInTime', 'strOutTime', 'project', 'produce','comment')
    search_fields = ('emp__name', 'project__name', 'project__company__name',)
    list_filter = ('emp__name',)


class SampleAdmin(admin.ModelAdmin):
    list_display = ('company', 'name', 'createDate', 'comment')
    search_fields = ('company__name', 'name', 'contact__name', 'sampleMap__flower__name',)
    list_filter = ('company__name',)


class SampleMapAdmin(admin.ModelAdmin):
    list_display = ('flower', 'color', 'length', 'cottonName', 'cottonWeight', 'comment')
    search_fields = ('flower__name', 'comment')
    list_filter = ('flower__name',)

admin.site.register(models.Company)
admin.site.register(models.Contact, ContactAdmin)
admin.site.register(models.Cotton, CottonAdmin)
admin.site.register(models.Machine)
admin.site.register(models.Material, MaterialAdmin)
admin.site.register(models.Emp, EmpAdmin)
admin.site.register(models.Flower)
admin.site.register(models.Project, ProjectAdmin)
admin.site.register(models.Delivery, DeliveryAdmin)
admin.site.register(models.Record, RecordAdmin)
admin.site.register(models.Sample, SampleAdmin)
admin.site.register(models.SampleMap, SampleMapAdmin)


