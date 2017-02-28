"""ms_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from ms import views
from django.contrib import admin


urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^home$', views.home, name='home'),
    url(r'^login$', views.login, name='login'),
    url(r'^logout$', views.logout, name='logout'),
    url(r'^emp$', views.emp, name='emp'),
    url(r'^empDetial/(?P<eid>[0-9]+)$', views.empDetial, name='empDetial'),
    url(r'^company$', views.company, name='company'),
    url(r'^companyDetial/(?P<cid>[0-9]+)$',views.companyDetial, name='companyDetial'),
    url(r'^projectDetial/(?P<pid>[0-9]+)$',views.projectDetial, name='projectDetial'),
    url(r'^project$', views.project, name='project'),
    url(r'^contactList/(?P<cid>[0-9]+)$',views.contactList, name='contactList'),
    url(r'^chart$', views.chart, name='chart'),
    url(r'^chartSearch$', views.chartSearch, name='chartSearch'),
    url(r'^chartDetial/(?P<cid>[0-9]+)$',views.chartDetial,name='chartDetial'),
    url(r'^sample$', views.sample, name='sample'),
    url(r'^sampleSearch$', views.sampleSearch, name='sampleSearch'),
    url(r'^sampleOfCompany/(?P<cid>[0-9]+)$', views.sampleOfCompany, name='sampleOfCompany'),
    url(r'sampleDetial/(?P<sid>[0-9]+)$', views.sampleDetial, name='sampleDetial'),
    url(r'createCompany$', views.createCompany, name='createCompany'),
    url(r'createContact$', views.createContact, name='createContact'),
    url(r'createFlower$', views.createFlower, name='createFlower'),
    url(r'createSample$', views.createSample, name='createSample'),
    url(r'createProject$', views.createProject, name='createProject'),
    url(r'createDelivery$', views.createDelivery, name='createDelivery'),
    url(r'createCotton$', views.createCotton, name='createCotton'),
    url(r'createMaterial$', views.createMaterial, name='createMaterial'),
    url(r'createEmpRecord$', views.createEmpRecord, name='createEmpRecord'),
    url(r'deliveryList$', views.deliveryList ,name='deliveryList'),
    url(r'searchDelivery$', views.searchDelivery, name='searchDelivery'),
    url(r'materialList$', views.materialList, name='materialList'),
    url(r'cottonList$', views.cottonList, name='cottonList'),
    url(r'searchMaterial$', views.searchMaterial, name='searchMaterial'),
    url(r'searchCotton$', views.searchCotton, name='searchCotton'),
    url(r'addDelivery$', views.addDelivery, name='addDelivery'),
    url(r'addMaterial$', views.addMaterial, name='addMaterial'),
    url(r'addCotton$', views.addCotton, name='addCotton'),
    url(r'outputCSV/(?P<pid>[0-9]+)$', views.outputCSV, name='outputCSV'),
    url(r'reportOfrecord$', views.recordReport, name='recordReport'),
    url(r'newrecord$',views.newrecord, name='newrecord'),
    url(r'sendmail',views.sendmail, name='sendmail')

]