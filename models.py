from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
import re
from datetime import datetime
from django.db import models
import uuid
import random
# Create your models here.

class AuthGroup(models.Model):
	name = models.CharField(unique=True, max_length=80)

	class Meta:
		managed = False
		db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
	group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
	permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

	class Meta:
		managed = False
		db_table = 'auth_group_permissions'
		unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
	name = models.CharField(max_length=255)
	content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
	codename = models.CharField(max_length=100)

	class Meta:
		managed = False
		db_table = 'auth_permission'
		unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
	password = models.CharField(max_length=128)
	last_login = models.DateTimeField(blank=True, null=True)
	is_superuser = models.IntegerField()
	username = models.CharField(unique=True, max_length=150)
	first_name = models.CharField(max_length=30)
	last_name = models.CharField(max_length=150)
	email = models.CharField(max_length=254)
	is_staff = models.IntegerField()
	is_active = models.IntegerField()
	date_joined = models.DateTimeField()

	class Meta:
		managed = False
		db_table = 'auth_user'


class AuthUserGroups(models.Model):
	user = models.ForeignKey(AuthUser, models.DO_NOTHING)
	group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

	class Meta:
		managed = False
		db_table = 'auth_user_groups'
		unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
	user = models.ForeignKey(AuthUser, models.DO_NOTHING)
	permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

	class Meta:
		managed = False
		db_table = 'auth_user_user_permissions'
		unique_together = (('user', 'permission'),)

class DjangoContentType(models.Model):
	app_label = models.CharField(max_length=100)
	model = models.CharField(max_length=100)

	class Meta:
		managed = False
		db_table = 'django_content_type'
		unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
	app = models.CharField(max_length=255)
	name = models.CharField(max_length=255)
	applied = models.DateTimeField()

	class Meta:
		managed = False
		db_table = 'django_migrations'


class DjangoSession(models.Model):
	session_key = models.CharField(primary_key=True, max_length=40)
	session_data = models.TextField()
	expire_date = models.DateTimeField()

	class Meta:
		managed = False
		db_table = 'django_session'

class Address(models.Model):
	AddressID = models.AutoField(primary_key=True)
	city = models.CharField(max_length = 256)
	sub_city = models.CharField(max_length=256)
	state = models.CharField(max_length=256)
	country = models.CharField(max_length=50)
	
	class Meta:
		managed = True
		db_table = 'Address'


	def __str__(self):
		return self.city + ',' + self.state


class Doctor(models.Model):
	user = models.OneToOneField(User,on_delete=models.DO_NOTHING,default=None)
	Title = models.CharField(max_length=10,null=True,default='Dr.')
	first_name = models.CharField(max_length=100,null=True)
	last_name = models.CharField(max_length=100,null=True)
	gender = models.CharField(max_length=10,null=True)
	DOB = models.CharField(max_length=100,null=True)#store DOB as a string and convert when reading it.
	state = models.CharField(max_length=256,null=True)
	city = models.CharField(max_length=20,null=True)
	subcity = models.CharField(max_length=20,null=True)
	state = models.CharField(max_length=20,null=True)
	country = models.CharField(max_length=20,null=True)


	class Meta:
		managed = True
		db_table = 'Doctor'

	def __str__(self):
		return 'Dr ' + self.first_name + ' ' + self.last_name

class Receptionist(models.Model):
	ReceptionistID = models.AutoField(primary_key=True)
	user = models.OneToOneField(User,on_delete=models.DO_NOTHING,default=None)
	first_name = models.CharField(max_length=20)
	last_name = models.CharField(max_length=20)
	
	class Meta:
		managed = True
		db_table = 'Receptionist'

# will add additional fields based on spec
class Bill(models.Model):
	BillID = models.AutoField(primary_key=True)
	Patient_id = models.ForeignKey('Patient',models.CASCADE,default=None,db_column='patientID',null=True)
	payment_date = models.DateField(null=True,blank=True)
	amount = models.FloatField()
	entered_by = models.CharField(max_length=20)
	enteredDate = models.DateField(auto_now=True,null=True)
	entered_by = models.ForeignKey(User, models.DO_NOTHING,null=True,blank=True)
	insuranceName = models.CharField(max_length=30,null=True)
	paymentOptions = (
		('CRD','CARD',),
        ('IP','LAB',),
        ('CO','MEDICATION',),
    )
	paymentType = models.CharField(max_length = 30, choices = paymentOptions,null=True,default='UNASSIGNED')

	class Meta:
		managed = True
		db_table = 'Bill'



class Patient(models.Model):
	ID = models.AutoField(primary_key=True)
	#user = models.OneToOneField(User,on_delete=models.DO_NOTHING,default=None)#Patient is not a user now. Keep code for future.
	first_name = models.CharField(max_length=100)
	last_name = models.CharField(max_length=100)
	age = models.CharField(max_length=100)
	gender = models.CharField(max_length=20)
	DocID = models.ForeignKey('Doctor',models.CASCADE,blank=True,default=None,null=True)
	address_id = models.ForeignKey('Address',models.CASCADE,default=None,db_column='AddressID')
	receptionist = models.ForeignKey(User, models.DO_NOTHING,null=True,blank=True)
	card_number = models.CharField(max_length=6, unique=True,default=str(random.randint(000000, 999999)))
	phone_number = models.CharField(max_length=10,default="unknown",unique=True,null=True)
	activeStatus = models.BooleanField(default=True,null=True)
	patientCreatedDate = models.DateField(auto_now=True,null=True)
	payment = models.ManyToManyField(Bill)

	class Meta:
		managed = True
		db_table = 'Patient'

	def __str__(self):
		return self.first_name + ' ' + self.last_name + '-' + self.card_number

class LabTech(models.Model):
	user = models.OneToOneField(User,on_delete=models.DO_NOTHING,default=None)
	labtechID = models.AutoField(primary_key=True)
	first_name = models.CharField(max_length=15)
	last_name = models.CharField(max_length=15)

	class Meta:
		managed = True
		db_table = 'LabTech'

	def __str__(self):
		return self.first_name + ' ' + self.last_name

class Laboratory(models.Model):
	labID = models.AutoField(primary_key=True)
	patient_id = models.ForeignKey('Patient',models.CASCADE,default=None,db_column='PatientID')
	doctor_id = models.ForeignKey(User, models.DO_NOTHING,null=True,blank=True)
	doctor_note = models.TextField(null=True)
	labtech_note = models.TextField(null=True)
	request_date = models.DateField()
	complete_date = models.DateField(null=True)
	lab_tech = models.ForeignKey('LabTech',models.CASCADE,default=None,related_name='labtech',null=True)
	status = (
		('UA','UNASSIGNED',),
        ('IP','IN PROGRESS',),
        ('CO','COMPLETED',),
        ('CA','CANCELED',),
    )
	labstatus = models.CharField(max_length = 30, choices = status,null=True,default='UNASSIGNED')

	class Meta:
		managed = True
		db_table = 'Laboratory'

	def __str__(self):
		return str(self.patient_id)

class proxyLaboratory(Laboratory):
	class Meta:
		proxy=True
		verbose_name = 'Lab Result'


class Room(models.Model):
	RoomID = models.AutoField(primary_key=True)
	room_type = models.CharField(max_length=100)
	status = models.CharField(max_length=20)
	
	class Meta:
		managed = True
		db_table = 'Room'


class InPatient(models.Model):
	IPID = models.AutoField(primary_key=True)
	patient_id = models.ForeignKey('Patient',models.CASCADE,default=None,db_column='patientID')
	room_no = models.ForeignKey('Room',models.CASCADE,default=None,db_column='RoomID')
	date_admitted = models.DateField(null=True,blank=True)
	date_discharged = models.DateField(null=True,blank=True)
	lab_no = models.ForeignKey('Laboratory',models.CASCADE,default=None,db_column='LabID')
	DocID = models.ForeignKey('Doctor',models.CASCADE,blank=True,default=None)

	class Meta:
		managed = True
		db_table = 'InPatient'

	def __str__(self):
		return self.patient_id.first_name + ' ' + self.patient_id.last_name

class Outpatient(models.Model):
	IPID = models.AutoField(primary_key=True)
	patient_id = models.ForeignKey('Patient',models.CASCADE,default=None,db_column='patientID')
	date = models.DateField()
	lab_no = models.ForeignKey('Laboratory',models.CASCADE,default=None,db_column='LabID')
	DocID = models.ForeignKey('Doctor',models.CASCADE,blank=True,default=None,db_column='DocID')

	class Meta:
		managed = True
		db_table = 'Outpatient'

class Nurse(models.Model):
	NurseID = models.AutoField(primary_key=True)
	user = models.OneToOneField(User,on_delete=models.DO_NOTHING,default=None)
	first_name = models.CharField(max_length=20)
	last_name = models.CharField(max_length=20)
	start_date = models.DateField(null=True,blank=True)
	gender = models.CharField(max_length=50,blank=True,null=True)
	dob = models.DateField(max_length=50,null=True)

	class Meta:
		managed = True
		db_table = 'Nurse'


class Prescripton(models.Model):
	prescriptionID = models.AutoField(primary_key=True)
	presName = models.CharField(max_length=100)
	#prodID = models.ForeignKey('Product',models.CASCADE,default=None,db_column='Product_ID')
	presCreatedDate = models.DateField(null=True)
	presCreatedBy = models.ForeignKey(User, models.DO_NOTHING,null=True,blank=True)
	presDescription = models.TextField(null=True)

	class Meta:
		managed = True
		db_table = 'Prescripton'

	def __str__(self):
		return self.presName



class Chart(models.Model):
	ChartID = models.AutoField(primary_key=True)#This is ok as an autofield.
	Patient_id = models.ForeignKey('Patient',models.CASCADE,default=None,db_column='patientID')
	temprature = models.CharField(max_length=50)
	weight = models.CharField(max_length=50)
	height = models.CharField(max_length=50)
	pulse = models.CharField(max_length=50)
	BMI = models.CharField(max_length=50)
	allergy = models.TextField(max_length=256)
	current_medications = models.TextField(max_length=50)
	family_history = models.TextField(max_length=50)
	previous_diagnosis = models.TextField(max_length=1000)
	general_symptom_note = models.TextField(max_length = 2000)
	entered_by = models.ForeignKey(User, models.DO_NOTHING,null=True,blank=True) #current user entering this.
	enteredDate = models.DateField(auto_now=True,null=True)
	activeStatus = models.BooleanField(default=True,null=True)
	RequestLab = models.ForeignKey('Laboratory',models.CASCADE,default=None,db_column='LabID')
	CreatePresciption = models.ManyToManyField(Prescripton)#models.CASCADE,default=None,db_column='presID',null=True)
	

	class Meta:
		managed = True
		db_table = 'Chart'




class Employee(models.Model):
	EmployeeID = models.AutoField(primary_key=True)
	first_name = models.CharField(max_length=20)
	last_name = models.CharField(max_length=20)
	address = models.ForeignKey('Address',models.CASCADE,default=None,db_column='AddressID')
	title = models.CharField(max_length=20)
	hire_date = models.DateField()
	end_date = models.DateField()

	class Meta:
		managed = True
		db_table = 'Employee'

## inventory management ## design
class Product(models.Model):
	ProductId = models.AutoField(primary_key=True)
	stock = models.CharField(max_length=50)
	name = models.CharField(max_length=50)
	price = models.DecimalField(max_digits=10,decimal_places=4)
	expire_date = models.DateField(null=True)

	class Meta:
		managed = True
		db_table = 'Product'

class Stock(models.Model):
	stockID = models.AutoField(primary_key=True)
	startingQuantity = models.DecimalField(max_digits=10,decimal_places=4)
	currentQuantity = models.DecimalField(max_digits=10,decimal_places=4)
	ProductId = models.ForeignKey('Product',models.CASCADE,default=None,related_name='productStock')

	class Meta:
		managed = True
		db_table = 'stock'

class Customer(models.Model):
	customerID = models.AutoField(primary_key=True)
	first_name = models.CharField(max_length=30)
	last_name = models.CharField(max_length=30)
	orgName = models.CharField(max_length=40)
	note = models.CharField(max_length=20)

	class Meta:
		managed = True
		db_table = 'Customer'

class Order(models.Model):
	OrderID = models.AutoField(primary_key=True)
	customerID = models.ForeignKey('Customer',models.CASCADE,default=None,db_column='customerID')
	orderdate = models.DateField()
	note = models.CharField(max_length=100)

	class Meta:
		managed = True
		db_table = 'Order'

