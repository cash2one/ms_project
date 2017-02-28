from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib import auth
from django.http import HttpResponseRedirect
from ms import models
from ms.forms import SearchProjectForm
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
from django.core import serializers
from django.db.models import Q
from django.http import HttpResponse
from ms.forms import CreateCompanyForm
from ms.forms import CreateContactForm
from ms.forms import CreateFlowerForm
from ms.forms import CreateSampleForm
from ms.forms import CreateProjectForm
from ms.forms import CreateDeliveryForm
from ms.forms import CreateCottonForm
from ms.forms import CreateMaterialForm
from ms.forms import EmpRecordForm


# Create your views here.
def index(request):
    if request.user.is_active:
        project_list = models.Project.objects.filter(isClose=0).filter(isFinish=0).order_by('-createDate')
        company_list = models.Company.objects.all()
        contact_list = models.Contact.objects.all()
        flower_list = models.Flower.objects.all()
        machine_list = models.Machine.objects.all()
        emp_list = models.Emp.objects.filter(onduty='1')
        return render(request,'home.html',{'project_list':project_list,
                                        'company_list':company_list,
                                        'contact_list':contact_list,
                                        'flower_list': flower_list,
                                        'machine_list': machine_list,
                                        'emp_list':emp_list})
    return render(request,'index.html')


def home(request):
    project_list = models.Project.objects.filter(isClose=0).filter(isFinish=0).order_by('-createDate')
    company_list = models.Company.objects.all()
    contact_list = models.Contact.objects.all()
    flower_list = models.Flower.objects.all()
    machine_list = models.Machine.objects.all()
    emp_list = models.Emp.objects.filter(onduty='1')
    return render(request,'home.html', {'project_list':project_list,
                                        'company_list':company_list,
                                        'contact_list':contact_list,
                                        'flower_list': flower_list,
                                        'machine_list': machine_list,
                                        'emp_list':emp_list})


def login(request):
    request.encoding = 'utf-8'
    name = request.POST.get("name")
    password = request.POST.get("password")
    # 验证一个用户的证书
    user = auth.authenticate(username=name, password=password)
    if user is not None and user.is_active:
        # Correct password, and the user is marked "active"
        auth.login(request, user)
        # Redirect to a success page.
        return home(request)
    else:
        # Show an error page
        return index(request)


def logout(request):
    auth.logout(request)
    # Redirect to a success page.
    return index(request)


def emp(request):
    emps = models.Emp.objects.all()
    records = models.Record.objects.all()
    company_list = models.Company.objects.all()
    project_list = models.Project.objects.filter(isClose=0).filter(isFinish=0)
    return render(request,'emp.html', {'emp_list': emps, 'record_list': records, 'company_list':company_list, 'project_list':project_list})


@require_http_methods(["GET"])
def empDetial(request, eid='1'):
    emps = models.Emp.objects.all()
    records = models.Record.objects.filter(emp__id=eid)
    company_list = models.Company.objects.all()
    project_list = models.Project.objects.filter(isClose=0).filter(isFinish=0)
    return render(request, 'emp_detial.html', {'emp_list': emps, 'record_list': records, 'company_list':company_list, 'project_list':project_list})


@require_http_methods(["GET", "POST"])
def company(request):
    if request.method == 'POST':
        # post method
        project = ''
        searchProjectForm = SearchProjectForm(request.POST)
        if searchProjectForm.is_valid():
            company_name = searchProjectForm.cleaned_data['company_name']
            projectName = searchProjectForm.cleaned_data['project_name']
            project_is_finish = searchProjectForm.cleaned_data['project_is_finish']
            project_is_close = searchProjectForm.cleaned_data['project_is_close']
            if company_name:# 公司名称存在
                if projectName:# 项目名称存在， 公司名称存在
                    # company name and project name
                    project = models.Project.objects.filter(Q(company__name__icontains=company_name), Q(name__icontains=projectName)
                                                            ,Q(isFinish=project_is_finish) , Q(isClose=project_is_close)).order_by('-createDate')

                else:# 项目名称不存在，公司名称存在
                    # company name, no project name
                    project = models.Project.objects.filter(Q(company__name__icontains=company_name)
                                                            , Q(isFinish=project_is_finish) , Q(isClose=project_is_close)).order_by('-createDate')
            else:# 公司名称不存在
                if projectName:# 公司名称不存在，项目名称存在
                    # project name, no company name
                    project = models.Project.objects.filter(Q(name__icontains=projectName)
                                                            , Q(isFinish=project_is_finish) , Q(isClose=project_is_close)).order_by('-createDate')
                else:
                    # none of both
                    project = models.Project.objects\
                        .filter(isFinish=project_is_finish)\
                        .filter(isClose=project_is_close).order_by('-createDate')
    else:
        # get method
        project = models.Project.objects.all().order_by('-createDate')
    companys = models.Company.objects.all()
    companyLengthMap = {}
    sumlengthOfCompany = 0.0
    for c in companys:
        material_list = models.Material.objects.filter(project__company_id=c.id)
        for m in material_list:
            p = models.Project.objects.get(id = m.project.id)
            if p.isFinish == '0':
                sumlengthOfCompany = sumlengthOfCompany + m.length
        companyLengthMap[c.id] = sumlengthOfCompany
        sumlengthOfCompany = 0.0
    return render(request, 'company.html', {'company_list': companys, 'project_list': project, 'companyLengthMap':companyLengthMap})


def companyDetial(request, cid='0'):
    company = models.Company.objects.get(id=cid)
    notFinishedProjects = models.Project.objects.filter(company__name=company.name).filter(isFinish=0).order_by('-createDate')  # 未完成 未结算
    notClosedProjects = models.Project.objects.filter(company__name=company.name).filter(isFinish=1).filter(isClose=0).order_by('-createDate') #已完成 未结算
    closedProjects = models.Project.objects.filter(company__name=company.name).filter(isFinish=1).filter(isClose=1).order_by('-createDate')  # 已完成 已结算
    sample_list = models.Sample.objects.filter(company_id=cid).order_by('-createDate')
    return render(request, 'companyDetial.html', {'company':company,
                                                  'notFinishedProjects':notFinishedProjects,
                                                  'notClosedProjects':notClosedProjects,
                                                  'closedProjects':closedProjects,
                                                  'sample_list':sample_list})


def projectDetial(request, pid='1'):
    project = models.Project.objects.get(id=pid)
    materials = project.material_set.all()
    cottons = project.cotton_set.all()
    records = project.record_set.all()
    delivery = project.delivery_set.all()
    material_map = {}
    sumLength = 0.0
    for m in materials:
        key = str(m.num)+' - '+str(m.color)
        value = m.length
        sumLength = sumLength + value
        if key in material_map.keys():
            a = material_map.get(key)
            material_map[key] = a + value
        if key not in material_map.keys():
            material_map[key] = value

    delivery_map = {}
    for m in delivery:
        key = str(m.num)+' - '+str(m.color)
        value = m.length
        if key in delivery_map.keys():
            a = delivery_map.get(key)
            delivery_map[key] = a + value
        if key not in delivery_map.keys():
            delivery_map[key] = value

    cottons_map = {}
    for m in cottons:
        key = str(m.name)+' - '+str(m.weight)+' g'
        value = m.length
        if key in cottons_map.keys():
            a = cottons_map.get(key)
            cottons_map[key] = a + value
        if key not in cottons_map.keys():
            cottons_map[key] = value

    info_map = {}
    key = 1
    for k, v in material_map.items():
        d_v = delivery_map.get(k)
        if not d_v:
            d_v = 0
        elif d_v is None:
            d_v = 0

        last_v = v - d_v
        nc = k.split(' - ')
        info_map[key] = {'num':nc[0],
                         'color': nc[1],
                         'total':v,
                         'delivery': d_v,
                         'last': last_v}
        key = key + 1

    return render(request,'projectDetial.html',{'project': project,
                                                'materials': materials,
                                                'cottons': cottons,
                                                'records': records,
                                                'delivery': delivery,
                                                'material_map':material_map,
                                                'delivery_map': delivery_map,
                                                'cottons_map': cottons_map,
                                                'info_map':info_map,
                                                'sumLength':sumLength})


def project(request):
    project_list = models.Project.objects.all().order_by('-createDate')
    notFinishedProjects = models.Project.objects.filter(isFinish=0).order_by('-createDate')  # 未完成 未结算
    notClosedProjects = models.Project.objects.filter(isFinish=1).filter(isClose=0).order_by('-createDate') #已完成 未结算
    closedProjects = models.Project.objects.filter(isFinish=1).filter(isClose=1).order_by('-createDate')  # 已完成 已结算
    sumLength = 0.0
    for p in notFinishedProjects:
        materiallist = models.Material.objects.filter(project_id=p.id)
        for m in materiallist:
            sumLength = sumLength + m.length

    return render(request,'project.html',{'project_list':project_list,
                                          'notFinishedProjects':notFinishedProjects,
                                          'notClosedProjects': notClosedProjects,
                                          'closedProjects': closedProjects,
                                          'sumLength':sumLength})


def contactList(request, cid=''):
    contact_list = models.Contact.objects.filter(company__id=cid)
    return JsonResponse(serializers.serialize('json', contact_list),safe=False)


def chart(request):
    chartList = models.Flower.objects.all()[:10]
    return render(request,'chart.html',{'chartList':chartList})


def chartSearch(request):
    key = request.POST.get('keywords')
    chartList = models.Flower.objects.filter(Q(name__contains=key) | Q(comment__contains=key))
    return render(request, 'chart.html',{'chartList':chartList})


def chartDetial(request, cid):
    chart = models.Flower.objects.get(id=cid)
    projectList = models.Project.objects.filter(flower_id=cid).order_by('-createDate')
    sample_list = models.Sample.objects.filter(sampleMap__flower_id=cid).order_by('-createDate')
    return render(request, 'chartDetial.html', {'projectList': projectList, 'chart':chart, 'sample_list':sample_list})


def sample(request):
    company_list = models.Company.objects.all()
    sample_list = models.Sample.objects.all().order_by('-createDate')[:10]
    return render(request, 'sample.html', {'company_list':company_list, 'sample_list':sample_list})


def sampleOfCompany(request, cid):
    company = models.Company.objects.get(id=cid)
    sample_list = models.Sample.objects.filter(company_id=cid).order_by('-createDate')
    return render(request, 'sampleOfCompany.html', { 'sample_list': sample_list, 'company':company})


def sampleSearch(request):
    key = request.POST.get('key')
    company_list = models.Company.objects.all()
    sample_list = models.Sample.objects.filter(Q(company__name__contains=key) | Q(name__contains=key)
                                 | Q(contact__name__contains=key) | Q(sampleMap__flower__name__contains=key)).order_by('-createDate')
    return render(request, 'sample.html', {'sample_list': sample_list, 'company_list': company_list})


def sampleDetial(request, sid):
    sample = models.Sample.objects.get(id=sid)
    return render(request, 'sampleDetial.html', {'sample': sample})


def createCompany(request):
    project_list = models.Project.objects.filter(isClose=0).filter(isFinish=0).order_by('-createDate')
    company_list = models.Company.objects.all()
    contact_list = models.Contact.objects.all()
    flower_list = models.Flower.objects.all()
    machine_list = models.Machine.objects.all()
    emp_list = models.Emp.objects.filter(onduty='1')
    message_company = {}
    createCompanyForm = CreateCompanyForm(request.POST)
    if createCompanyForm.is_valid():
        companyName = createCompanyForm.cleaned_data['name']
        address = createCompanyForm.cleaned_data['address']
        phone = createCompanyForm.cleaned_data['phone']
        # save new company
        oldCompany = models.Company.objects.filter(name=companyName)
        if oldCompany:
            message_company['error'] = '公司 [ '+ companyName + ' ] 已经存在'
        else:
            models.Company.objects.create(name=companyName,
                                                    address = address,
                                                    phone = phone)
            message_company['success'] = '公司 [ ' + companyName + ' ] 添加成功'
    return render(request, 'home.html', {'message_company':message_company,
                                         'project_list':project_list,
                                         'company_list': company_list,
                                         'contact_list': contact_list,
                                         'flower_list': flower_list,
                                         'machine_list': machine_list,
                                         'emp_list':emp_list
                                         })

def createContact(request):
    project_list = models.Project.objects.filter(isClose=0).filter(isFinish=0).order_by('-createDate')
    company_list = models.Company.objects.all()
    contact_list = models.Contact.objects.all()
    flower_list = models.Flower.objects.all()
    machine_list = models.Machine.objects.all()
    createContactForm = CreateContactForm(request.POST)
    emp_list = models.Emp.objects.filter(onduty='1')
    message_contact = {}
    if createContactForm.is_valid():
        companyObj = models.Company.objects.get(id=createContactForm.cleaned_data['contact_company'])
        models.Contact.objects.create(name=createContactForm.cleaned_data['contact_name'],
                                      phone=createContactForm.cleaned_data['contact_phone'],
                                      email=createContactForm.cleaned_data['contact_email'],
                                      company=companyObj)
        message_contact['success'] = '创建项目联系人成功, 公司：'+companyObj.name+' 联系人：'+createContactForm.cleaned_data['contact_name']
    else:
        message_contact['error'] = '创建项目联系人失败'
    return render(request, 'home.html', {'message_contact':message_contact, 'tag':'contact',
                                         'project_list': project_list,
                                         'company_list': company_list,
                                         'contact_list': contact_list,
                                         'flower_list': flower_list,
                                         'machine_list': machine_list,
                                         'emp_list':emp_list
                                         })


def createFlower(request):
    project_list = models.Project.objects.filter(isClose=0).filter(isFinish=0).order_by('-createDate')
    company_list = models.Company.objects.all()
    contact_list = models.Contact.objects.all()
    flower_list = models.Flower.objects.all()
    machine_list = models.Machine.objects.all()
    emp_list = models.Emp.objects.filter(onduty='1')
    createFlowerForm = CreateFlowerForm(request.POST,request.FILES)
    message_flower = {}
    if createFlowerForm.is_valid():
        models.Flower.objects.create(
            name=createFlowerForm.cleaned_data['flower_name'],
            comment=createFlowerForm.cleaned_data['flower_comment'],
            image=createFlowerForm.cleaned_data['flower_image'],
            dstfile=createFlowerForm.cleaned_data['flower_file']
        )
        message_flower['success'] = '创建新花型成功，花型名称：'+ createFlowerForm.cleaned_data['flower_name']
    else:
        message_flower['error'] = '创建花型失败'
    return render(request,'home.html',{'message_flower':message_flower,'tag': 'flower',
                                       'project_list': project_list,
                                       'company_list': company_list,
                                       'contact_list': contact_list,
                                       'flower_list': flower_list,
                                       'machine_list': machine_list,
                                       'emp_list':emp_list
                                       })


def createSample(request):
    project_list = models.Project.objects.filter(isClose=0).filter(isFinish=0).order_by('-createDate')
    company_list = models.Company.objects.all()
    contact_list = models.Contact.objects.all()
    flower_list = models.Flower.objects.all()
    machine_list = models.Machine.objects.all()
    emp_list = models.Emp.objects.filter(onduty='1')
    createSampleForm = CreateSampleForm(request.POST, request.FILES)
    message_sample = {}
    if createSampleForm.is_valid():
        companyObj = models.Company.objects.get(id=createSampleForm.cleaned_data['sample_company'])
        s = models.Sample(company=companyObj,
                      name=createSampleForm.cleaned_data['sample_name'],
                      createDate=createSampleForm.cleaned_data['sample_createDate'],
                      image=createSampleForm.cleaned_data['sample_image'],
                      comment = createSampleForm.cleaned_data['sample_comment'])
        s.save()
        contact = models.Contact.objects.get(id=createSampleForm.cleaned_data['sample_contact'])
        s.contact.add(contact)
        if createSampleForm.cleaned_data['color_1']:
            sm = models.SampleMap()
            sm.color = createSampleForm.cleaned_data['color_1']
            sm.length = createSampleForm.cleaned_data['length_1']
            sm.cottonName = createSampleForm.cleaned_data['cottonName_1']
            sm.cottonWeight = createSampleForm.cleaned_data['cottonWeight_1']
            sm.machine = models.Machine.objects.get(id=createSampleForm.cleaned_data['machine_1'])
            sm.flower = models.Flower.objects.get(id=createSampleForm.cleaned_data['flower_1'])
            sm.comment = createSampleForm.cleaned_data['comment_1']
            sm.save()
            s.sampleMap.add(sm)
        if createSampleForm.cleaned_data['color_2']:
            sm = models.SampleMap()
            sm.color = createSampleForm.cleaned_data['color_2']
            sm.length = createSampleForm.cleaned_data['length_2']
            sm.cottonName = createSampleForm.cleaned_data['cottonName_2']
            sm.cottonWeight = createSampleForm.cleaned_data['cottonWeight_2']
            sm.machine = models.Machine.objects.get(id=createSampleForm.cleaned_data['machine_2'])
            sm.flower = models.Flower.objects.get(id=createSampleForm.cleaned_data['flower_2'])
            sm.comment = createSampleForm.cleaned_data['comment_2']
            sm.save()
            s.sampleMap.add(sm)
        if createSampleForm.cleaned_data['color_3']:
            sm = models.SampleMap()
            sm.color = createSampleForm.cleaned_data['color_3']
            sm.length = createSampleForm.cleaned_data['length_3']
            sm.cottonName = createSampleForm.cleaned_data['cottonName_3']
            sm.cottonWeight = createSampleForm.cleaned_data['cottonWeight_3']
            sm.machine = models.Machine.objects.get(id=createSampleForm.cleaned_data['machine_3'])
            sm.flower = models.Flower.objects.get(id=createSampleForm.cleaned_data['flower_3'])
            sm.comment = createSampleForm.cleaned_data['comment_3']
            sm.save()
            s.sampleMap.add(sm)

        message_sample['success'] = '创建新打样成功, 公司名称：'+companyObj.name\
                                    +', 打样项目：'+createSampleForm.cleaned_data['sample_name']

    else:
        message_sample['error'] = '创建新打样失败'

    return render(request,'home.html',{'message_sample':message_sample,'tag':'sample',
                                       'project_list': project_list,
                                       'company_list': company_list,
                                       'contact_list': contact_list,
                                       'flower_list': flower_list,
                                       'machine_list': machine_list,
                                       'emp_list':emp_list
                                       })


def createProject(request):
    project_list = models.Project.objects.filter(isClose=0).filter(isFinish=0).order_by('-createDate')
    company_list = models.Company.objects.all()
    contact_list = models.Contact.objects.all()
    flower_list = models.Flower.objects.all()
    machine_list = models.Machine.objects.all()
    emp_list = models.Emp.objects.filter(onduty='1')
    createProjectForm = CreateProjectForm(request.POST, request.FILES)
    message_project = {}
    if createProjectForm.is_valid():
        companyObj = models.Company.objects.get(id=createProjectForm.cleaned_data['project_company'])
        s = models.Project(company=companyObj,
                           name=createProjectForm.cleaned_data['project_name'],
                           createDate=createProjectForm.cleaned_data['project_createDate'],
                           image=createProjectForm.cleaned_data['project_image'],
                           comment=createProjectForm.cleaned_data['project_comment'],
                           flower=models.Flower.objects.get(id=createProjectForm.cleaned_data['project_flower']))
        s.save()
        contact = models.Contact.objects.get(id=createProjectForm.cleaned_data['project_contact'])
        s.contact.add(contact)
        message_project['success'] = '创建新项目成功，公司名称：'+companyObj.name+', 项目名称：'+createProjectForm.cleaned_data['project_name']
    else:
        message_project['error'] = '创建新项目失败'

    return render(request,'home.html',{'message_project':message_project,'tag':'project',
                                       'project_list': project_list,
                                       'company_list': company_list,
                                       'contact_list': contact_list,
                                       'flower_list': flower_list,
                                       'machine_list': machine_list,
                                       'emp_list':emp_list
                                       })


def createDelivery(request):
    project_list = models.Project.objects.filter(isClose=0).filter(isFinish=0).order_by('-createDate')
    company_list = models.Company.objects.all()
    contact_list = models.Contact.objects.all()
    flower_list = models.Flower.objects.all()
    machine_list = models.Machine.objects.all()
    emp_list = models.Emp.objects.filter(onduty='1')
    createDeliveryForm = CreateDeliveryForm(request.POST, request.FILES)
    message_delivery = {}
    if createDeliveryForm.is_valid():
        companyObj = models.Company.objects.get(id=createDeliveryForm.cleaned_data['delivery_company'])
        projectObj = models.Project.objects.get(id=createDeliveryForm.cleaned_data['delivery_project'])
        outdate = createDeliveryForm.cleaned_data['delivery_outdate']
        delivery_image =createDeliveryForm.cleaned_data['delivery_image']
        if createDeliveryForm.cleaned_data['delivery_num_1']:
            num = createDeliveryForm.cleaned_data['delivery_num_1']
            color = createDeliveryForm.cleaned_data['delivery_color_1']
            length = createDeliveryForm.cleaned_data['delivery_length_1']
            comment = createDeliveryForm.cleaned_data['delivery_comment_1']
            models.Delivery.objects.create(project = projectObj,
                                           image = delivery_image,
                                           outDate = outdate,
                                           num = num,
                                           color = color,
                                           length = length,
                                           comment = comment)
        if createDeliveryForm.cleaned_data['delivery_num_2']:
            num = createDeliveryForm.cleaned_data['delivery_num_2']
            color = createDeliveryForm.cleaned_data['delivery_color_2']
            length = createDeliveryForm.cleaned_data['delivery_length_2']
            comment = createDeliveryForm.cleaned_data['delivery_comment_2']
            models.Delivery.objects.create(project=projectObj,
                                           image=delivery_image,
                                           outDate=outdate,
                                           num=num,
                                           color=color,
                                           length=length,
                                           comment=comment)
        if createDeliveryForm.cleaned_data['delivery_num_3']:
            num = createDeliveryForm.cleaned_data['delivery_num_3']
            color = createDeliveryForm.cleaned_data['delivery_color_3']
            length = createDeliveryForm.cleaned_data['delivery_length_3']
            comment = createDeliveryForm.cleaned_data['delivery_comment_3']
            models.Delivery.objects.create(project=projectObj,
                                           image=delivery_image,
                                           outDate=outdate,
                                           num=num,
                                           color=color,
                                           length=length,
                                           comment=comment)
        if createDeliveryForm.cleaned_data['delivery_num_4']:
            num = createDeliveryForm.cleaned_data['delivery_num_4']
            color = createDeliveryForm.cleaned_data['delivery_color_4']
            length = createDeliveryForm.cleaned_data['delivery_length_4']
            comment = createDeliveryForm.cleaned_data['delivery_comment_4']
            models.Delivery.objects.create(project=projectObj,
                                           image=delivery_image,
                                           outDate=outdate,
                                           num=num,
                                           color=color,
                                           length=length,
                                           comment=comment)
        if createDeliveryForm.cleaned_data['delivery_num_5']:
            num = createDeliveryForm.cleaned_data['delivery_num_5']
            color = createDeliveryForm.cleaned_data['delivery_color_5']
            length = createDeliveryForm.cleaned_data['delivery_length_5']
            comment = createDeliveryForm.cleaned_data['delivery_comment_5']
            models.Delivery.objects.create(project=projectObj,
                                           image=delivery_image,
                                           outDate=outdate,
                                           num=num,
                                           color=color,
                                           length=length,
                                           comment=comment)

        message_delivery['success'] = '创建新发货单成功，公司名称：'+companyObj.name+' 项目名称：'+projectObj.name
        checkProjectState(createDeliveryForm.cleaned_data['delivery_project'])

    else:
        message_delivery['error'] = '创建新发货单失败'

    return render(request, 'home.html', {'message_delivery': message_delivery, 'tag': 'delivery',
                                         'project_list': project_list,
                                         'company_list': company_list,
                                         'contact_list': contact_list,
                                         'flower_list': flower_list,
                                         'machine_list': machine_list,
                                         'emp_list':emp_list
                                         })


def createCotton(request):
    project_list = models.Project.objects.filter(isClose=0).filter(isFinish=0).order_by('-createDate')
    company_list = models.Company.objects.all()
    contact_list = models.Contact.objects.all()
    flower_list = models.Flower.objects.all()
    machine_list = models.Machine.objects.all()
    emp_list = models.Emp.objects.filter(onduty='1')
    createCottonForm = CreateCottonForm(request.POST, request.FILES)
    message_cotton = {}
    if createCottonForm.is_valid():
        companyObj = models.Company.objects.get(id=createCottonForm.cleaned_data['cotton_company'])
        projectObj = models.Project.objects.get(id=createCottonForm.cleaned_data['cotton_project'])
        cotton_inTime = createCottonForm.cleaned_data['cotton_inTime']
        cotton_image = createCottonForm.cleaned_data['cotton_image']
        if createCottonForm.cleaned_data['cotton_name_1']:
            cotton_name = createCottonForm.cleaned_data['cotton_name_1']
            cotton_weight = createCottonForm.cleaned_data['cotton_weight_1']
            cotton_width = createCottonForm.cleaned_data['cotton_width_1']
            cotton_length = createCottonForm.cleaned_data['cotton_length_1']
            cotton_comment = createCottonForm.cleaned_data['cotton_comment_1']
            models.Cotton.objects.create(project=projectObj,
                                         name = cotton_name,
                                         weight = cotton_weight,
                                         width = cotton_width,
                                         length = cotton_length,
                                         inTime = cotton_inTime,
                                         image = cotton_image,
                                         comment = cotton_comment)
        if createCottonForm.cleaned_data['cotton_name_2']:
            cotton_name = createCottonForm.cleaned_data['cotton_name_2']
            cotton_weight = createCottonForm.cleaned_data['cotton_weight_2']
            cotton_width = createCottonForm.cleaned_data['cotton_width_2']
            cotton_length = createCottonForm.cleaned_data['cotton_length_2']
            cotton_comment = createCottonForm.cleaned_data['cotton_comment_2']
            models.Cotton.objects.create(project=projectObj,
                                         name = cotton_name,
                                         weight = cotton_weight,
                                         width = cotton_width,
                                         length = cotton_length,
                                         inTime = cotton_inTime,
                                         image = cotton_image,
                                         comment = cotton_comment)
        if createCottonForm.cleaned_data['cotton_name_3']:
            cotton_name = createCottonForm.cleaned_data['cotton_name_3']
            cotton_weight = createCottonForm.cleaned_data['cotton_weight_3']
            cotton_width = createCottonForm.cleaned_data['cotton_width_3']
            cotton_length = createCottonForm.cleaned_data['cotton_length_3']
            cotton_comment = createCottonForm.cleaned_data['cotton_comment_3']
            models.Cotton.objects.create(project=projectObj,
                                         name = cotton_name,
                                         weight = cotton_weight,
                                         width = cotton_width,
                                         length = cotton_length,
                                         inTime = cotton_inTime,
                                         image = cotton_image,
                                         comment = cotton_comment)

        message_cotton['success'] = '创建棉收货单成功, 公司名称：'+companyObj.name+', 项目名称：'+projectObj.name

    else:
        message_cotton['error'] = '创建棉收货单失败'

    return render(request, 'home.html', {'message_cotton': message_cotton, 'tag': 'cotton',
                                         'project_list': project_list,
                                         'company_list': company_list,
                                         'contact_list': contact_list,
                                         'flower_list': flower_list,
                                         'machine_list': machine_list,
                                         'emp_list':emp_list
                                         })

def createMaterial(request):
    project_list = models.Project.objects.filter(isClose=0).filter(isFinish=0).order_by('-createDate')
    company_list = models.Company.objects.all()
    contact_list = models.Contact.objects.all()
    flower_list = models.Flower.objects.all()
    machine_list = models.Machine.objects.all()
    emp_list = models.Emp.objects.filter(onduty='1')
    createMaterialForm = CreateMaterialForm(request.POST, request.FILES)
    message_material = {}
    if createMaterialForm.is_valid():
        companyObj = models.Company.objects.get(id=createMaterialForm.cleaned_data['material_company'])
        projectObj = models.Project.objects.get(id=createMaterialForm.cleaned_data['material_project'])
        material_inTime = createMaterialForm.cleaned_data['material_inTime']
        material_image = createMaterialForm.cleaned_data['material_image']
        if createMaterialForm.cleaned_data['material_num_1']:
            num = createMaterialForm.cleaned_data['material_num_1']
            color = createMaterialForm.cleaned_data['material_color_1']
            length = createMaterialForm.cleaned_data['material_length_1']
            comment = createMaterialForm.cleaned_data['material_comment_1']
            models.Material.objects.create(project = projectObj,
                                         inTime = material_inTime,
                                         image = material_image,
                                         num = num,
                                         color = color,
                                         length = length,
                                         comment = comment)
        if createMaterialForm.cleaned_data['material_num_2']:
            num = createMaterialForm.cleaned_data['material_num_2']
            color = createMaterialForm.cleaned_data['material_color_2']
            length = createMaterialForm.cleaned_data['material_length_2']
            comment = createMaterialForm.cleaned_data['material_comment_2']
            models.Material.objects.create(project = projectObj,
                                         inTime = material_inTime,
                                         image = material_image,
                                         num = num,
                                         color = color,
                                         length = length,
                                         comment = comment)
        if createMaterialForm.cleaned_data['material_num_3']:
            num = createMaterialForm.cleaned_data['material_num_3']
            color = createMaterialForm.cleaned_data['material_color_3']
            length = createMaterialForm.cleaned_data['material_length_3']
            comment = createMaterialForm.cleaned_data['material_comment_3']
            models.Material.objects.create(project = projectObj,
                                         inTime = material_inTime,
                                         image = material_image,
                                         num = num,
                                         color = color,
                                         length = length,
                                         comment = comment)
        if createMaterialForm.cleaned_data['material_num_4']:
            num = createMaterialForm.cleaned_data['material_num_4']
            color = createMaterialForm.cleaned_data['material_color_4']
            length = createMaterialForm.cleaned_data['material_length_4']
            comment = createMaterialForm.cleaned_data['material_comment_4']
            models.Material.objects.create(project = projectObj,
                                         inTime = material_inTime,
                                         image = material_image,
                                         num = num,
                                         color = color,
                                         length = length,
                                         comment = comment)
        if createMaterialForm.cleaned_data['material_num_5']:
            num = createMaterialForm.cleaned_data['material_num_5']
            color = createMaterialForm.cleaned_data['material_color_5']
            length = createMaterialForm.cleaned_data['material_length_5']
            comment = createMaterialForm.cleaned_data['material_comment_5']
            models.Material.objects.create(project = projectObj,
                                         inTime = material_inTime,
                                         image = material_image,
                                         num = num,
                                         color = color,
                                         length = length,
                                         comment = comment)
        message_material['success'] = '创建布料收货单成功, 公司名称：'+companyObj.name+', 项目名称：'+projectObj.name

    else:
        message_material['error'] = '创建布料收货单失败'
    return render(request, 'home.html', {'message_material': message_material, 'tag': 'material',
                                         'project_list': project_list,
                                         'company_list': company_list,
                                         'contact_list': contact_list,
                                         'flower_list': flower_list,
                                         'machine_list': machine_list,
                                         'emp_list':emp_list
                                         })


def createEmpRecord(request):
    project_list = models.Project.objects.filter(isClose=0).filter(isFinish=0).order_by('-createDate')
    company_list = models.Company.objects.all()
    contact_list = models.Contact.objects.all()
    flower_list = models.Flower.objects.all()
    machine_list = models.Machine.objects.all()
    emp_list = models.Emp.objects.filter(onduty='1')
    empRecordForm = EmpRecordForm(request.POST, request.FILES)
    message_emp = {}
    if empRecordForm.is_valid():
        emp_id = empRecordForm.cleaned_data['emp_name']
        emp_project_id = empRecordForm.cleaned_data['emp_project']
        emp = models.Emp.objects.get(id=emp_id)
        projectObj = models.Project.objects.get(id=emp_project_id)
        emp_produce = empRecordForm.cleaned_data['emp_produce']
        emp_inTime = empRecordForm.cleaned_data['emp_inTime']
        emp_outTime = empRecordForm.cleaned_data['emp_outTime']
        emp_comment = empRecordForm.cleaned_data['emp_comment']
        models.Record.objects.create(emp=emp,
                                     project = projectObj,
                                     produce = emp_produce,
                                     inTime = emp_inTime,
                                     outTime = emp_outTime,
                                     comment = emp_comment)

        message_emp['success'] = '创建员工工作记录成功，员工：'+emp.name
    else:
        message_emp['error'] = '创建员工工作记录失败'
    return render(request, 'home.html', {'message_emp': message_emp, 'tag': 'emp',
                                         'project_list': project_list,
                                         'company_list': company_list,
                                         'contact_list': contact_list,
                                         'flower_list': flower_list,
                                         'machine_list': machine_list,
                                         'emp_list':emp_list
                                         })

def deliveryList(request):
    deliveryList = models.Delivery.objects.all().order_by('-outDate')[:10]
    return render(request,'deliveryList.html',{'deliveryList':deliveryList})


def searchDelivery(request):
    delivery_search = request.POST.get('delivery_search')
    if delivery_search:
        delivery_lsit = models.Delivery.objects.filter(Q(project__company__name__icontains=delivery_search)|
                                                       Q( project__name__icontains=delivery_search)).order_by('-outDate')

        return render(request, 'deliveryList.html', {'deliveryList':delivery_lsit,
                                                     'delivery_search':delivery_search})
    else:
        return deliveryList(request)


def materialList(request):
    materialList = models.Material.objects.all().order_by('-inTime')[:10]
    return render(request, 'materialList.html', {'materialList': materialList})


def cottonList(request):
    cottonList = models.Cotton.objects.all().order_by('-inTime')[:10]
    return render(request, 'cottonList.html', {'cottonList': cottonList})


def searchCotton(request):
    cotton_search = request.POST.get('cotton_search')
    if cotton_search:
        cotton_List = models.Cotton.objects.filter(Q(project__company__name__icontains=cotton_search) |
                                                       Q(project__name__icontains=cotton_search)).order_by('-inTime')

        return render(request, 'cottonList.html', {'cottonList': cotton_List,
                                                     'cotton_search': cotton_search})
    else:
        return cottonList(request)


def searchMaterial(request):
    material_search = request.POST.get('material_search')
    if material_search:
        material_list = models.Material.objects.filter(Q(project__company__name__icontains=material_search) |
                                                       Q(project__name__icontains=material_search)).order_by('-inTime')

        return render(request, 'materialList.html', {'materialList': material_list,
                                                     'material_search': material_search})
    else:
        return materialList(request)


def addDelivery(request):
    projectId = request.POST.get('projectId')
    createDate = request.POST.get('createDate')
    deliveryFile = request.FILES.get('deliveryFile')
    project_Detial = models.Project.objects.get(id=projectId)
    materials = project_Detial.material_set.all()
    material_map = {}
    for m in materials:
        key = str(m.num) + '-' + str(m.color)
        value = m.length
        if key in material_map.keys():
            a = material_map.get(key)
            material_map[key] = a + value
        if key not in material_map.keys():
            material_map[key] = value

    for k, v in material_map.items():
        delivery_num_color_length = request.POST.get(k+'-length')
        delivery_num_color_comment = request.POST.get(k + '-comment')
        if delivery_num_color_length:
            num = k.split('-')[0]
            color = k.split('-')[1]
            print('num=' + num + ',color=' + color + ',length=' + delivery_num_color_length)
            models.Delivery.objects.create(project=project_Detial, num=num, color=color,
                                           length=delivery_num_color_length,
                                           outDate=createDate,
                                           comment=delivery_num_color_comment,
                                           image=deliveryFile)

    checkProjectState(projectId)
    return projectDetial(request, pid=projectId)

def checkProjectState(pid):
    materialList = models.Material.objects.filter(project_id=pid)
    deliveryList = models.Delivery.objects.filter(project_id=pid)
    m_total = 0.0
    for m in materialList:
        m_total = m_total + m.length
    d_total = 0.0
    for d in deliveryList:
        d_total = d_total + d.length
    if m_total==d_total:
        project = models.Project.objects.get(id=pid)
        project.isFinish = 1
        project.save()
    else:
        project = models.Project.objects.get(id=pid)
        project.isFinish = 0
        project.save()


def addMaterial(request):
    projectId = request.POST.get('projectId')
    createDate = request.POST.get('createDate')
    materialFile = request.FILES.get('materialFile')
    project_Detial = models.Project.objects.get(id=projectId)
    num_1 = request.POST.get('num_1')
    color_1 = request.POST.get('color_1')
    length_1 = request.POST.get('length_1')
    comment_1 = request.POST.get('comment_1')

    num_2 = request.POST.get('num_2')
    color_2 = request.POST.get('color_2')
    length_2 = request.POST.get('length_2')
    comment_2 = request.POST.get('comment_2')

    num_3 = request.POST.get('num_3')
    color_3 = request.POST.get('color_3')
    length_3 = request.POST.get('length_3')
    comment_3 = request.POST.get('comment_3')

    if num_1 :
        models.Material.objects.create(project=project_Detial, num=num_1,
                                       color=color_1, length=length_1, comment=comment_1,
                                       inTime=createDate, image=materialFile)
    if num_2 :
        models.Material.objects.create(project=project_Detial, num=num_2,
                                       color=color_2, length=length_2, comment=comment_2,
                                       inTime=createDate, image=materialFile)
    if num_3 :
        models.Material.objects.create(project=project_Detial, num=num_3,
                                       color=color_3, length=length_3, comment=comment_3,
                                       inTime=createDate, image=materialFile)
    checkProjectState(projectId)
    return projectDetial(request, pid=projectId)

def addCotton(request):
    projectId = request.POST.get('projectId')
    createDate = request.POST.get('createDate')
    cottonFile = request.FILES.get('cottonFile')
    project_Detial = models.Project.objects.get(id=projectId)

    cottonType_1 = request.POST.get('cottonType_1')
    cottonWeight_1 = request.POST.get('cottonWeight_1')
    cottonLength_1 = request.POST.get('cottonLength_1')
    cottonComment_1 = request.POST.get('cottonComment_1')

    cottonType_2 = request.POST.get('cottonType_2')
    cottonWeight_2 = request.POST.get('cottonWeight_2')
    cottonLength_2 = request.POST.get('cottonLength_2')
    cottonComment_2 = request.POST.get('cottonComment_2')

    cottonType_3 = request.POST.get('cottonType_3')
    cottonWeight_3 = request.POST.get('cottonWeight_3')
    cottonLength_3 = request.POST.get('cottonLength_3')
    cottonComment_3 = request.POST.get('cottonComment_3')

    if cottonType_1:
        models.Cotton.objects.create(project=project_Detial, name=cottonType_1,
                                     weight=cottonWeight_1, length=cottonLength_1,
                                     comment=cottonComment_1, inTime=createDate,
                                     image=cottonFile)
    if cottonType_2:
        models.Cotton.objects.create(project=project_Detial, name=cottonType_2,
                                     weight=cottonWeight_2, length=cottonLength_2,
                                     comment=cottonComment_2, inTime=createDate,
                                     image=cottonFile)
    if cottonType_3:
        models.Cotton.objects.create(project=project_Detial, name=cottonType_3,
                                     weight=cottonWeight_3, length=cottonLength_3,
                                     comment=cottonComment_3, inTime=createDate,
                                     image=cottonFile)

    return projectDetial(request, pid=projectId)


import csv
import codecs


def outputCSV(request, pid):
    # Create the HttpResponse object with the appropriate CSV header.
    request.encoding = 'utf-8'
    project = models.Project.objects.get(id=pid)
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment;filename="project.csv"'
    response.write(codecs.BOM_UTF8)
    writer = csv.writer(response)
    materialList = models.Material.objects.filter(project_id=pid)
    deliveryList = models.Delivery.objects.filter(project_id=pid)
    writer.writerow(['公司名称', '项目名称', '花型', '创建日期'])
    writer.writerow([project.company.name, project.name, project.flower.name, project.createDate])
    writer.writerow(['布料进货单'])
    writer.writerow(['日期', '缸号', '颜色', '米数'])
    for m in materialList:
        writer.writerow([m.inTime, m.num, m.color, m.length])
    writer.writerow([])
    writer.writerow([])
    writer.writerow([])
    writer.writerow(['发货记录'])
    writer.writerow(['日期', '缸号', '颜色', '米数'])
    for d in deliveryList:
        writer.writerow([d.outDate, d.num, d.color, d.length])

    response.close()
    return response


def recordReport(request):
    request.encoding = 'utf-8'
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment;filename="record_report.csv"'
    response.write(codecs.BOM_UTF8)
    writer = csv.writer(response)
    empid = request.POST.get('emp')
    startDate = request.POST.get('startdate')
    endDate = request.POST.get('enddate')

    if empid == '0':
        writer.writerow(['统计报告', '全部员工', '开始日期', startDate, '结束日期', endDate])
        records = models.Record.objects.filter(inTime__gte=startDate).filter(outTime__lte=endDate).order_by('inTime')
    else:
        records = models.Record.objects.filter(emp_id=empid).filter(inTime__gte=startDate).filter(outTime__lte=endDate).order_by('inTime')
        writer.writerow(['统计报告', models.Emp.objects.get(id=empid).name, '开始日期', startDate, '结束日期', endDate])


    writer.writerow(['员工ID', '员工姓名', '日期', '上班时间', '下班时间', '工作时长', '备注'])
    for record in records:
        writer.writerow([record.emp_id, record.emp.name, record.workDate(), record.inTime, record.outTime, record.workHour(), record.comment])

    response.close()
    return response


def newrecord(request):
    empRecordForm = EmpRecordForm(request.POST, request.FILES)
    if empRecordForm.is_valid():
        emp_id = empRecordForm.cleaned_data['emp_name']
        emp_project_id = empRecordForm.cleaned_data['emp_project']
        emp = models.Emp.objects.get(id=emp_id)
        projectObj = models.Project.objects.get(id=emp_project_id)
        emp_produce = empRecordForm.cleaned_data['emp_produce']
        emp_inTime = empRecordForm.cleaned_data['emp_inTime']
        emp_outTime = empRecordForm.cleaned_data['emp_outTime']
        emp_comment = empRecordForm.cleaned_data['emp_comment']
        models.Record.objects.create(emp=emp,
                                     project=projectObj,
                                     produce=emp_produce,
                                     inTime=emp_inTime,
                                     outTime=emp_outTime,
                                     comment=emp_comment)
    emps = models.Emp.objects.all()
    records = models.Record.objects.all()
    company_list = models.Company.objects.all()
    project_list = models.Project.objects.filter(isClose=0).filter(isFinish=0)
    return render(request, 'emp.html', {'emp_list': emps, 'record_list': records, 'company_list': company_list,
                                        'project_list': project_list})


import smtplib
from email.mime.text import MIMEText
import time
def sendmail(request):

<<<<<<< HEAD
    _user = "aaa"
    _pwd = "ccc"
    _to = "ddd"

    str_sample = '<tr>' \
                 '<td rowspan="{rowspan}">{project_date}</td>' \
                 '<td rowspan="{rowspan}">{company_name}</td>' \
                 '<td rowspan="{rowspan}">{project_name}</td>' \
                 '<td rowspan="{rowspan}">{project_comment}</td>' \
                 '</tr>'

    str_material = """
    <tr>
    <td>{material_num_and_color}</td>
    <td>{material_length}</td>
    <td>{material_sendout_length}</td>
    <td>{material_remain_length}</td>
    </tr>
    """

    project_list = models.Project.objects.filter(isClose=0).order_by('company_id','-createDate')
=======
    _user = "*"
    _pwd = "*"
    _to = "642294626@qq.com"

    str_sample = '<tr><td rowspan="{rowspan}">{company_name}</td><td rowspan="{rowspan}">{project_name}</td>' \
                 '<td rowspan="{rowspan}">{project_comment}</td></tr>'

    str_material = """
    <tr><td>{material_num_and_color}</td><td>{material_length}</td><td>{material_sendout_length}</td><td>{material_remain_length}</td></tr>
    """

    project_list = models.Project.objects.filter(isClose=0).order_by('company_id').order_by('-createDate')
>>>>>>> origin/master
    sumLine = ''
    for project in project_list:

        material_list = models.Material.objects.filter(project_id=project.id)
        delivery_list = models.Delivery.objects.filter(project_id=project.id)

        material_map = {}
        sumLength = 0.0
        for m in material_list:
            key = str(m.num) + ' - ' + str(m.color)
            value = m.length
            sumLength = sumLength + value
            if key in material_map.keys():
                a = material_map.get(key)
                material_map[key] = a + value
            if key not in material_map.keys():
                material_map[key] = value

        delivery_map = {}
        for m in delivery_list:
            key = str(m.num) + ' - ' + str(m.color)
            value = m.length
            if key in delivery_map.keys():
                a = delivery_map.get(key)
                delivery_map[key] = a + value
            if key not in delivery_map.keys():
                delivery_map[key] = value



        rowspan = 1
        for k, v in material_map.items():
            rowspan = rowspan +1

<<<<<<< HEAD
        line = str_sample.format(rowspan=rowspan,project_date=project.strCreateDate(), company_name=project.company.name, project_name=project.name
=======
        line = str_sample.format(rowspan=rowspan, company_name=project.company.name, project_name=project.name
>>>>>>> origin/master
                                     , project_comment=project.comment)

        for k, v in material_map.items():
            if delivery_map.get(k):
                material_remain_length = v - delivery_map.get(k)
            else:
                material_remain_length = v
            item = str_material.format(material_num_and_color=k, material_length=v, material_sendout_length=delivery_map.get(k), material_remain_length=material_remain_length)
            line = line + item

        sumLine = sumLine + line

    now = time.localtime(time.time())
    strnow = time.strftime('%Y-%m-%d',now)
<<<<<<< HEAD
    mail_text = """
=======
    msg = MIMEText("""
>>>>>>> origin/master
    <div>
    <h4 align=center><a href="http://www.quiltinggroup.com">莫氏绗缝绣饰中心</a> - 项目汇报 - {date}</h4>
    </div>
    <div>

    </div>
    <div>
        <table border="1.5px;" style="word-break:break-all; word-wrap:break-all;" align=center>
<<<<<<< HEAD
            <th>日期</th><th>公司名称</th><th>项目名称</th><th>加工备注</th><th>缸号 - 颜色</th><th>总米数</th><th>已发货米数</th><th>剩余米数</th>
=======
            <th>公司名称</th><th>项目名称</th><th>加工备注</th><th>缸号 - 颜色</th><th>总米数</th><th>已发货米数</th><th>剩余米数</th>
>>>>>>> origin/master
            <tbody>
                {table}
            </tbody>
        </table>
    </div>

    """.format(table=sumLine,date=strnow)
<<<<<<< HEAD
    msg = MIMEText(mail_text,'html','utf-8')
    msg["Subject"] = "莫氏绗缝绣饰中心 "+strnow
=======
                   ,'html','utf-8')
    msg["Subject"] = "项目汇报 "+strnow
>>>>>>> origin/master
    msg["From"] = _user
    msg["To"] = _to
    message = ''
    try:
        s = smtplib.SMTP_SSL('smtp.163.com',465)
        s.login(_user, _pwd)
        s.sendmail(_user, _to, msg.as_string())
        s.quit()
        message = '发送邮件成功'
    except smtplib.SMTPException as  e:
<<<<<<< HEAD
        print(e)
=======
>>>>>>> origin/master
        message = '发送邮件失败'
    return HttpResponse(message)
