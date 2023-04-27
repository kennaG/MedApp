from django.contrib import admin
from .models import (Address,
Doctor,Receptionist,Patient,LabTech,Laboratory,Room,InPatient,Outpatient,Nurse,Bill,Chart,Employee,Product,
Stock,Customer,Order,proxyLaboratory,Prescripton)
from django.contrib.admin import AdminSite

# Register your models here.

class EventAdminSite(admin.AdminSite):
    site_header = "Daandi School Site"
    site_title = "Department Heads"
    index_title = "Welcome to Department Head Portal"

@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
	list_display = ('city','sub_city','state','country')
	#raw_id_fields = ('card_number',)
	fields = (
        ('city','country'),
        ('sub_city', 'state')
    )


@admin.register(Receptionist)
class ReceptionistAdmin(admin.ModelAdmin):
	raw_id_fields = ('user',)
	list_display = ('user','first_name','last_name')
	fields = ('user','first_name','last_name')

@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
	list_display = ('first_name','last_name','gender','DOB','state','city','subcity','state','country')
	fields = ('user','first_name','last_name','gender','DOB','state','city','subcity','country')

@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
	exclude = ('receptionist',)
	raw_id_fields = ('address_id','payment')
	list_filter = ['activeStatus','patientCreatedDate']
	search_fields = ['card_number','phone_number','first_name','last_name']
	list_display = ('card_number','phone_number','first_name','last_name','age','gender','address_id')
	#list_display_links = ['paymentType']
	fields = ('activeStatus','first_name','last_name','age','gender','address_id','phone_number','payment')
	


@admin.register(LabTech)
class LabTechAdmin(admin.ModelAdmin):
	list_display = ('user','first_name','last_name')
	fields = ('user','first_name','last_name')

@admin.register(Laboratory)
class Laboratory(admin.ModelAdmin):
	exclude = ('doctor_id',)
	list_filter = ['labstatus']
	readonly_fields = ('labtech_note','complete_date','lab_tech')
	list_display = ('patient_id','doctor_note','request_date','complete_date','lab_tech')
	fields = ('patient_id','request_date','complete_date','lab_tech','doctor_note','labtech_note')

@admin.register(proxyLaboratory)
class proxyLaboratory(admin.ModelAdmin):
	exclude = ('doctor_id',)
	list_editable = ['labstatus']
	list_filter = ['labstatus']
	readonly_fields = ('patient_id','doctor_note','request_date')
	list_display = ('patient_id','request_date','complete_date','lab_tech','labstatus','labtech_note')
	fields = ('patient_id','request_date','complete_date','lab_tech','doctor_note','labstatus','labtech_note')



@admin.register(Room)
class Laboratory(admin.ModelAdmin):
	list_display = ('room_type','status')
	fields = ('room_type','status')

@admin.register(InPatient)
class InPatientAdmin(admin.ModelAdmin):
	raw_id_fields = ('patient_id',)
	list_display = ('patient_id','room_no','date_admitted','date_discharged','lab_no','DocID')
	fields = ('patient_id','room_no','date_admitted','date_discharged','lab_no','DocID')

@admin.register(Outpatient)
class OutpatientAdmin(admin.ModelAdmin):
	list_display = ('patient_id','date','lab_no','DocID')
	fields = ('patient_id','date','lab_no','DocID')

@admin.register(Nurse)
class NurseAdmin(admin.ModelAdmin):
	list_display = ('user','first_name','last_name','start_date','gender','dob')
	fields = ('user','first_name','last_name','start_date','gender','dob')

@admin.register(Bill)
class BillAdmin(admin.ModelAdmin):
	exclude = ('entered_by',)
	raw_id_fields = ('Patient_id',)
	list_filter = ['paymentType','payment_date']
	list_display = ('Patient_id','insuranceName','paymentType','payment_date','amount')
	#list_display_links = ('paymentType',)
	fields = ('Patient_id','insuranceName','paymentType','payment_date','amount')


#testing textinput fields size.
from django.forms import TextInput, Textarea
from django.db import models
@admin.register(Chart)
class ChartAdmin(admin.ModelAdmin):
	exclude	= ('entered_by',)
	search_fields = ['Patient_id__first_name','Patient_id__last_name','Patient_id__card_number','Patient_id__DocID__first_name']
	list_filter = ['Patient_id__DocID','activeStatus','enteredDate']
	raw_id_fields = ('RequestLab','CreatePresciption')
	list_display = ('Patient_id','temprature','weight','height','pulse','BMI','allergy','current_medications','family_history','previous_diagnosis','general_symptom_note','RequestLab')
	fields = ('activeStatus','Patient_id',('temprature','weight','height'),('pulse','BMI'),('allergy','current_medications'),('family_history','previous_diagnosis'),'general_symptom_note','RequestLab','CreatePresciption')
	formfield_overrides = {
	models.CharField: {'widget': TextInput(attrs={'size':'10'})},
	models.TextField: {'widget': Textarea(attrs={'rows':3, 'cols':30})},
	}


@admin.register(Prescripton)
class PrescriptionAdmin(admin.ModelAdmin):
	exclude = ('presCreatedBy',)
	list_display = ('presName','presCreatedDate','presDescription')
	fields = ('presName','presCreatedDate','presDescription')