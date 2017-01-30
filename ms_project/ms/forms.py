from django import forms


# in company page, search project
class SearchProjectForm(forms.Form):
    company_name = forms.CharField(required=False)
    project_name = forms.CharField(required=False)
    project_is_finish = forms.CharField()
    project_is_close = forms.CharField()


# create new company
class CreateCompanyForm(forms.Form):
    name = forms.CharField(required=True)
    address = forms.CharField(required=False)
    phone = forms.CharField(required=False)


class CreateContactForm(forms.Form):
    contact_name = forms.CharField(required=True)
    contact_phone = forms.CharField(required=False)
    contact_email =forms.EmailField(required=False)
    contact_company = forms.CharField(required=False)


class CreateFlowerForm(forms.Form):
    flower_name = forms.CharField(required=True)
    flower_comment = forms.CharField(required=False)
    flower_image = forms.ImageField(required=False)
    flower_file = forms.FileField(required=False)


class CreateSampleForm(forms.Form):
    sample_company = forms.CharField(required=True)
    sample_contact = forms.CharField(required=False)
    sample_name = forms.CharField(required=True)
    sample_createDate = forms.DateField(required=True)
    sample_image = forms.ImageField(required=False)
    sample_comment = forms.CharField(required=False)
    color_1 = forms.CharField(required=False)
    length_1 = forms.CharField(required=False)
    cottonName_1 = forms.CharField(required=False)
    cottonWeight_1 = forms.CharField(required=False)
    machine_1 = forms.CharField(required=False)
    flower_1 = forms.CharField(required=False)
    comment_1 = forms.CharField(required=False)
    color_2 = forms.CharField(required=False)
    length_2 = forms.CharField(required=False)
    cottonName_2 = forms.CharField(required=False)
    cottonWeight_2 = forms.CharField(required=False)
    machine_2 = forms.CharField(required=False)
    flower_2 = forms.CharField(required=False)
    comment_2 = forms.CharField(required=False)
    color_3 = forms.CharField(required=False)
    length_3 = forms.CharField(required=False)
    cottonName_3 = forms.CharField(required=False)
    cottonWeight_3 = forms.CharField(required=False)
    machine_3 = forms.CharField(required=False)
    flower_3 = forms.CharField(required=False)
    comment_3 = forms.CharField(required=False)


class CreateProjectForm(forms.Form):
    project_company = forms.CharField(required=True)
    project_name =  forms.CharField(required=True)
    project_contact = forms.CharField(required=False)
    project_createDate = forms.DateField(required=True)
    project_image = forms.ImageField(required=False)
    project_flower = forms.CharField(required=False)
    project_comment = forms.CharField(required=False)


class CreateDeliveryForm(forms.Form):
    delivery_company = forms.CharField(required=True)
    delivery_project = forms.CharField(required=True)
    delivery_image = forms.ImageField(required=False)
    delivery_outdate = forms.DateField(required=False)

    delivery_num_1 = forms.CharField(required=False)
    delivery_color_1 = forms.CharField(required=False)
    delivery_length_1 = forms.CharField(required=False)
    delivery_comment_1 = forms.CharField(required=False)

    delivery_num_2 = forms.CharField(required=False)
    delivery_color_2 = forms.CharField(required=False)
    delivery_length_2 = forms.CharField(required=False)
    delivery_comment_2 = forms.CharField(required=False)

    delivery_num_3 = forms.CharField(required=False)
    delivery_color_3 = forms.CharField(required=False)
    delivery_length_3 = forms.CharField(required=False)
    delivery_comment_3 = forms.CharField(required=False)

    delivery_num_4 = forms.CharField(required=False)
    delivery_color_4 = forms.CharField(required=False)
    delivery_length_4 = forms.CharField(required=False)
    delivery_comment_4 = forms.CharField(required=False)

    delivery_num_5 = forms.CharField(required=False)
    delivery_color_5 = forms.CharField(required=False)
    delivery_length_5 = forms.CharField(required=False)
    delivery_comment_5 = forms.CharField(required=False)


class CreateCottonForm(forms.Form):
    cotton_company = forms.CharField(required=True)
    cotton_project = forms.CharField(required=True)
    cotton_image = forms.ImageField(required=False)
    cotton_inTime = forms.DateField(required=True)

    cotton_name_1 = forms.CharField(required=False)
    cotton_weight_1 = forms.IntegerField(required=False)
    cotton_width_1 = forms.FloatField(required=False)
    cotton_length_1 = forms.FloatField(required=False)
    cotton_comment_1 = forms.CharField(required=False)

    cotton_name_2 = forms.CharField(required=False)
    cotton_weight_2 = forms.IntegerField(required=False)
    cotton_width_2 = forms.FloatField(required=False)
    cotton_length_2 = forms.FloatField(required=False)
    cotton_comment_2 = forms.CharField(required=False)

    cotton_name_3 = forms.CharField(required=False)
    cotton_weight_3 = forms.IntegerField(required=False)
    cotton_width_3 = forms.FloatField(required=False)
    cotton_length_3 = forms.FloatField(required=False)
    cotton_comment_3 = forms.CharField(required=False)


class CreateMaterialForm(forms.Form):
    material_company = forms.CharField(required=True)
    material_project = forms.CharField(required=True)
    material_image = forms.ImageField(required=False)
    material_inTime = forms.DateField(required=True)

    material_num_1 = forms.CharField(required=False)
    material_color_1 = forms.CharField(required=False)
    material_length_1 =forms.FloatField(required=False)
    material_comment_1 = forms.CharField(required=False)

    material_num_2 = forms.CharField(required=False)
    material_color_2 = forms.CharField(required=False)
    material_length_2 =forms.FloatField(required=False)
    material_comment_2 = forms.CharField(required=False)

    material_num_3 = forms.CharField(required=False)
    material_color_3 = forms.CharField(required=False)
    material_length_3 =forms.FloatField(required=False)
    material_comment_3 = forms.CharField(required=False)

    material_num_4 = forms.CharField(required=False)
    material_color_4 = forms.CharField(required=False)
    material_length_4 =forms.FloatField(required=False)
    material_comment_4 = forms.CharField(required=False)

    material_num_5 = forms.CharField(required=False)
    material_color_5 = forms.CharField(required=False)
    material_length_5 =forms.FloatField(required=False)
    material_comment_5 = forms.CharField(required=False)


class EmpRecordForm(forms.Form):
    emp_name = forms.CharField(required=True)
    emp_company = forms.CharField(required=True)
    emp_project = forms.CharField(required=True)
    emp_produce = forms.FloatField(required=True)
    emp_inTime = forms.DateTimeField(required=True)
    emp_outTime = forms.DateTimeField(required=True)
    emp_comment = forms.CharField(required=False)

