from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver
from datetime import datetime,timedelta

from ckeditor.fields import RichTextField
# Create your models here.


class CustomUser(AbstractUser):
    user_type_data=((1,"Admin"),(2,"Employs"))
    user_type=models.CharField(default=1,choices=user_type_data,max_length=10)

from django.db import models
from django.contrib.auth.models import User

class Companys(models.Model):
    usernumber = models.OneToOneField(CustomUser, on_delete=models.CASCADE,default="1")
    organizationname = models.CharField(max_length=100)
    registration_number = models.CharField(max_length=5, unique=True, editable=False)
    address = models.TextField()
    contact_person = models.CharField(max_length=50)
    email = models.EmailField()
    phone_number = models.CharField(max_length=10)
    password = models.CharField(max_length=100, default="")
    Numberofemployees = models.CharField(max_length=100, default="")
    your_title = models.CharField(max_length=100, default="")
    otp = models.CharField(max_length=4, default="")
    agreement_status = models.IntegerField(default="3")
    profilepic=models.ImageField(upload_to="media/",default="")

    def save_company(self):
        self.save()

    def save(self, *args, **kwargs):
        # If registration number is not provided, generate a new one
        if not self.registration_number:
            last_company = Companys.objects.order_by('-id').first()
            if last_company:
                last_registration_number = int(last_company.registration_number)
                new_registration_number = str(last_registration_number + 1).zfill(5)
            else:
                new_registration_number = "20231"

            self.registration_number = new_registration_number

        super(Companys, self).save(*args, **kwargs)


    def __str__(self):
        return self.name





class AdminHod(models.Model):
    id=models.AutoField(primary_key=True)
    admin=models.OneToOneField(CustomUser,on_delete=models.CASCADE)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now_add=True)
    firstname=models.CharField(max_length=100,default="")
    lastname=models.CharField(max_length=100,default="")
    username=models.CharField(max_length=100,default="")
    password=models.CharField(max_length=100,default="")
    email=models.CharField(max_length=100,default="")
    empid=models.CharField(max_length=100,default="")
    phnos = models.CharField(max_length=20, default="")  
    address=models.CharField(max_length=50,default="")
    dateofbirth = models.DateField(default=None)
    dateofjoining = models.DateField(default=None)
    Department=models.CharField(max_length=100,default="")
    manager=models.CharField(max_length=100,default="")
    gender=models.CharField(max_length=100,default="")
    location=models.CharField(max_length=100,default="")
    package=models.IntegerField(default=0)
    pincode=models.IntegerField(default=0)
    designation=models.CharField(max_length=100,default="")
    status=models.CharField(max_length=100,default="")
    bloodgroup=models.CharField(max_length=100,default="")
    adminprofilepic=models.ImageField(upload_to="media/",default="")
    options=models.CharField(max_length=100,default="")
    objects=models.Manager()
    

class list(models.Model):
    name=models.CharField(max_length=100)
class meta:
    db_table="list"

class working_shifts(models.Model):

    starting_time = models.TimeField()
    ending_time = models.TimeField(max_length=100)
    cutoff_time = models.PositiveIntegerField(default="10")
    shift_name = models.CharField(max_length=100)
    befor_time=models.PositiveIntegerField(default="2")

class Meta:
    db_table="working_shifts" 
    def get_shift_name(self):
        if self.working:
            return self.working.shift_name
        else:
            return "N/A" 


class documents_setup1(models.Model):
    document_type = models.CharField(max_length=100, null=True, blank=True)
    compulsory=models.CharField(max_length=100)
    Enabled=models.CharField(max_length=100)

class Meta:
    db_table="documents_setup1"  


class Employs(models.Model):
    id=models.AutoField(primary_key=True)
    admin=models.OneToOneField(CustomUser,on_delete=models.CASCADE)
      # shift_name = models.CharField(max_length=100,default="")
    working= models.ForeignKey(working_shifts, on_delete=models.CASCADE , related_name='workshifts', null=True)
    working12=models.CharField(max_length=100,default="a")
    first_name=models.CharField(max_length=100)
    last_name=models.CharField(max_length=100)
    email=models.CharField(max_length=100)
    web_mail=models.CharField(max_length=100,default="")
    username=models.CharField(max_length=100,default="")
    password=models.CharField(max_length=100,default="")
    gender=models.CharField(max_length=255)
    profile_pic=models.FileField(upload_to='media/')
    address=models.TextField()
    empid=models.CharField(max_length=100)
    companyid= models.ForeignKey(Companys, on_delete=models.CASCADE,default="1")
    dateofjoining=models.DateField()
    designation=models.CharField(max_length=100)
    location=models.CharField(max_length=100)
    package=models.CharField(max_length=100)
    pincode=models.CharField(max_length=100)
    contactno=models.CharField(max_length=100)
    status=models.CharField(max_length=100,default="")
    bloodgroup=models.CharField(max_length=100,default="")
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now_add=True)
    insert=models.CharField(max_length=500,default="")
    is_team_lead = models.BooleanField(default=False)
    role=models.CharField(max_length=100,default="")
    hroptions=models.IntegerField(default=0)
    projectmanagerop=models.IntegerField(default=0)
    b_name = models.CharField(max_length=100,default="")
    insert = models.CharField(max_length=500,default="")
    is_team_lead = models.BooleanField(default=False)

    fcm_token=models.TextField()
    objects = models.Manager()
    def missing_info(self):
        required_info=['profile_pic']
        missing_info = {}
        for field in required_info:
            if not getattr(self, field):
                missing_info[field] = 'Missing'
        return missing_info
    # def get_shift_name(self):
    #     if self.working:
    #         return self.working.shift_name
    #     else:
    #         return "N/A"  # Provide a default value if no working shift is assigned


    def __str__(self):
        return self.last_name
    
    def calculate_overall_performance(self):
        completed_tasks = self.employeeids.filter(t_status='completed')
        total_tasks = self.employeeids.all()
        high_priority_tasks = completed_tasks.filter(t_priority='High').count()
        medium_priority_tasks = completed_tasks.filter(t_priority='Medium').count()
        low_priority_tasks = completed_tasks.filter(t_priority='Low').count()

        performance_score = (high_priority_tasks * 10 + medium_priority_tasks * 5 + low_priority_tasks * 2)

        return {
            'total_tasks_taken': total_tasks.count(),
            'total_tasks_completed': completed_tasks.count(),
            'high_priority_tasks_completed': high_priority_tasks,
            'medium_priority_tasks_completed': medium_priority_tasks,
            'low_priority_tasks_completed': low_priority_tasks,
            'performance_score': performance_score,
        }

    def __str__(self):
        return self.last_name


    
    def __str__(self):
        return self.profile_pic

from django.utils import timezone

class Project(models.Model):
    p_name = models.CharField(max_length=100)
    p_desc = models.CharField(max_length=200)
    o_id = models.ForeignKey(Employs, on_delete=models.CASCADE)
    status=models.CharField(max_length=100,default="")
    project_deadline = models.DateTimeField(default=timezone.now)
    project_manager = models.CharField(max_length=100,default="")
    
    def calculate_project_performance(self):
        completed_tasks = self.projectids.filter(t_status='completed')
        total_tasks_count = self.projectids.count()
        completed_tasks_count = completed_tasks.count()
        pending_tasks = self.projectids.filter(t_status='todo')
        if total_tasks_count == 0:
            return 0  # Avoid division by zero error

        completion_rate = (completed_tasks_count / total_tasks_count) * 100

        return {
            'completion_rate': completion_rate,
            'total_tasks': total_tasks_count,
            'pending_tasks': pending_tasks.count(),
            'completed_tasks':completed_tasks_count
        }

    class Meta:
        db_table = "project"

    def __str__(self):
        return self.p_name
    
    # def get_team_leader(self):
    #     try:
    #         # Get the team member who is the team leader for this project
    #         team_leader = self.teammember_set.get(is_team_lead=True)
    #         team_first_name = team_leader.employee.first_name
    #         team_last_name = team_leader.employee.last_name
    #         team_role = team_leader.employee.role
    #         team_empid = team_leader.employee.empid
    #         team_id = team_leader.employee.id
    #         return {
    #            'team_first_name': team_first_name,
    #            'team_last_name':team_last_name,
    #            'team_role':team_role,
    #            'team_empid':team_empid,
    #            'team_id':team_id
    #         }
    #     except TeamMember.DoesNotExist:
    #         return "No team leader assigned"


    def get_team_leader(self):
        try:
            # Get the team member who is the team leader for this project
            team_leader = self.teammember_set.get(is_team_lead=True)
            team_first_name = team_leader.employee.first_name
            team_last_name = team_leader.employee.last_name
            team_role = team_leader.employee.role
            team_empid = team_leader.employee.empid
            team_id = team_leader.employee.id
            return {
            'team_first_name': team_first_name,
            'team_last_name': team_last_name,
            'team_role': team_role,
            'team_empid': team_empid,
            'team_id': team_id,
            }
        except TeamMember.DoesNotExist:
            return {
                'team_first_name': None,
                'team_last_name': None,
                'team_role': None,
                'team_empid': None,
                'team_id': None,
            }

        

class TeamMember(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    employee = models.ForeignKey(Employs, on_delete=models.CASCADE)
    is_team_lead = models.BooleanField(default=False) 

    class Meta:
        unique_together = ('project', 'employee')
        db_table = "team_member"

    def calculate_total_score_in_project(self):
        # Calculate the total score for tasks in the current project
        tasks = Task.objects.filter(e_id=self.employee, p_id=self.project, t_status='completed')
        total_score = sum(task.calculate_task_score() for task in tasks)
        return total_score

    def calculate_total_score_across_all_projects(self):
        total_score = 0

        # Get all projects associated with the employee
        projects = Project.objects.filter(teammember__employee=self.employee)

        for project in projects:
            # Get completed tasks for the current project
            tasks = Task.objects.filter(e_id=self.employee, p_id=project, t_status='completed')

            # Calculate the score for tasks in the current project
            project_score = sum(task.calculate_task_score() for task in tasks)

            # Add the project score to the total score
            total_score += project_score

        return total_score
    def __str__(self):
        return f"{self.employee.first_name} {self.employee.last_name} on {self.project.p_name}"

class HR(models.Model):
    b_name = models.CharField(max_length=100,default="")
    o_id = models.ForeignKey(AdminHod, on_delete=models.CASCADE)
    id=models.AutoField(primary_key=True)
    admin=models.OneToOneField(CustomUser,on_delete=models.CASCADE)
    first_name=models.CharField(max_length=100)
    last_name=models.CharField(max_length=100)
    email=models.CharField(max_length=100)
    web_mail=models.CharField(max_length=100)
    username=models.CharField(max_length=100)
    password=models.CharField(max_length=100)
    gender=models.CharField(max_length=255)
    address=models.TextField()
    empid=models.CharField(max_length=100)
    Manager=models.CharField(max_length=100)
    dateofbirth = models.DateField(default=None)
    dateofjoining=models.DateField(default=None)
    role=models.CharField(max_length=100)
    location=models.CharField(max_length=100)
    package=models.CharField(max_length=100)
    pincode=models.CharField(max_length=100)
    contactno=models.CharField(max_length=100)
    status=models.CharField(max_length=100)
    bloodgroup=models.CharField(max_length=100)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now_add=True)
    insert=models.CharField(max_length=500)
    is_team_lead = models.BooleanField(default=False)
    hroptions=models.IntegerField(default=1)
    fcm_token=models.TextField()
    objects = models.Manager()

class project_drop(models.Model):
    name = models.CharField(max_length=200, db_index=True)
    url=models.CharField(max_length=100)
    parent_category = models.ForeignKey('self', related_name='subdrop', blank=True, null=True, on_delete=models.CASCADE)
    class Meta:
        ordering = ('name',)
        verbose_name = 'category'
        verbose_name_plural = 'categories'
    
    def __str__(self):
        return self.name
from datetime import date
class admin_project_create (models.Model):
    companyid= models.ForeignKey(Companys, on_delete=models.CASCADE,default="1")
    project_name=models.CharField(max_length=100)
    project_dec=models.CharField(max_length=100)
    admin_id =models.CharField(max_length=100)

    date=models.DateField(default=date.today) 
    status=models.CharField(max_length=100,default="")
    class Meta:
        db_table = "admin_project_create"

class Task(models.Model):
    t_name = models.CharField(max_length=55)
    t_desc = models.CharField(max_length=200)
    t_status = models.CharField(max_length=55)
    t_priority = models.CharField(max_length=30)
    t_assign_date = models.DateTimeField(auto_now_add=True )
    t_deadline_date = models.DateTimeField()
    t_update_date = models.DateTimeField(default=timezone.now)
    is_expired = models.BooleanField(default=False)
    b_id = models.ForeignKey(HR, on_delete=models.CASCADE, related_name='HRids')
    p_id = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='projectids')
    o_id = models.ForeignKey(Employs, on_delete=models.CASCADE,null=True, blank=True)
    e_id = models.ForeignKey(Employs, on_delete=models.CASCADE, related_name='employeeids')
    
    def calculate_task_score(self):
        score = 0

        if self.t_status == "completed":
            time_difference = self.t_deadline_date - self.t_update_date

            if self.t_priority == "High":
                if time_difference > timedelta(days=0):
                    # Task completed before the deadline
                    score = 15 + int(time_difference.total_seconds() / 3600)  # Add score based on hours before the deadline
                else:
                    # Task completed after the deadline
                    score = 5 - int(abs(time_difference.total_seconds()) / 3600)  # Subtract score based on hours after the deadline

            elif self.t_priority == "Medium":
                if time_difference > timedelta(days=0):
                    score = 10 + int(time_difference.total_seconds() / 3600)
                else:
                    score = 3 - int(abs(time_difference.total_seconds()) / 3600)

            elif self.t_priority == "Low":
                if time_difference > timedelta(days=0):
                    score = 5 + int(time_difference.total_seconds() / 3600)
                else:
                    score = 1 - int(abs(time_difference.total_seconds()) / 3600)

        return score

    def calculate_remaining_time(self):
        if self.t_status == "completed":
            return None  # Task is already completed, no remaining time

        current_time = timezone.now()
        remaining_time = self.t_deadline_date - current_time

        # Ensure remaining time is positive (no negative remaining time)
        if remaining_time.total_seconds() < 0:
            return None

        return remaining_time
    class Meta:
        db_table = "task"

class Project_Employee_Linker(models.Model):
    p_id = models.ForeignKey(Project, on_delete=models.CASCADE)
    e_id = models.ForeignKey(Employs, on_delete=models.CASCADE)
    o_id = models.ForeignKey(AdminHod, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('p_id', 'e_id','o_id')
        db_table = "project_emp_assign"



class types(models.Model):
    name=models.CharField(max_length=100)
   
class meta:
    db_table="types"

class Reimbursement(models.Model):
    id=models.AutoField(primary_key=True)
    employ_id=models.ForeignKey(Employs,on_delete=models.CASCADE)
    typea=models.CharField(max_length=100,default='')
    date=models.DateField(default=None)
    detail=models.CharField(max_length=5000)
    amount=models.IntegerField()
    image=models.ImageField(upload_to="media/")
    reimbursement_status=models.IntegerField(default=0)
    objects=models.Manager()



class Monitoring(models.Model):
    m_title = models.CharField(max_length=200, null=True)
    m_log_ts = models.CharField(max_length=200)
    employee = models.ForeignKey(Employs, on_delete=models.CASCADE )
    

    class Meta:
        db_table = "monitoring"

class MonitoringDetails(models.Model):
    md_title = models.CharField(max_length=200)
    md_total_time_seconds = models.CharField(max_length=200)
    md_date = models.CharField(max_length=200)
    employee = models.ForeignKey(Employs, on_delete=models.CASCADE )
    

    class Meta:
        db_table = "MonitoringDetails"

class SystemStatus(models.Model):
    STATUS_CHOICES = [
        ('battery', 'Battery'),
        ('online', 'Online'),
         
    ]

    status_type = models.CharField(max_length=20, choices=STATUS_CHOICES)
    status_message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    employee = models.ForeignKey(Employs, on_delete=models.CASCADE )

    def __str__(self):
        return f"{self.status_type}: {self.status_message}"
    
class Screenshots(models.Model):
    image = models.ImageField(upload_to='media/')
    timestamp =models.DateField(default=None)
    employee = models.ForeignKey(Employs, on_delete=models.CASCADE )
    
    class Meta:
        db_table = "Screenshots"



class Admin_Reimbursement(models.Model):
    id=models.AutoField(primary_key=True)
    admin_id=models.ForeignKey(AdminHod,on_delete=models.CASCADE)
    typea=models.CharField(max_length=100,default='')
    date=models.DateField(default=None)
    detail=models.CharField(max_length=5000)
    amount=models.IntegerField()
    image=models.ImageField(upload_to="media/")
    reimbursement_status=models.IntegerField(default=0)
    objects=models.Manager()

class adminnav(models.Model):
    name=models.CharField(max_length=100)
    icon=models.CharField(max_length=100)
    url=models.CharField(max_length=100)
    is_name_exist = models.BooleanField(default=True)
    is_projectmanager= models.BooleanField(default=True)
    is_admin=models.BooleanField(default=True)

class employnav(models.Model):
    name=models.CharField(max_length=100)
    icon=models.CharField(max_length=100)
    url=models.CharField(max_length=100)
    is_name_exist = models.BooleanField(default=True)
    is_tl_option=models.BooleanField(default="0")
    hr_options=models.BooleanField(default="0")
    employ_options=models.BooleanField(default="1")
    projectmanager_options=models.BooleanField(default="1")


class admin_drop(models.Model):
    name = models.CharField(max_length=200, db_index=True)
    url=models.CharField(max_length=100)
    show=models.BooleanField(default=0)
    parentshow=models.BooleanField(default=0)
    parent_category = models.ForeignKey('self', related_name='subdrop', blank=True, null=True, on_delete=models.CASCADE)
    class Meta:
        ordering = ('name',)
        verbose_name = 'category'
        verbose_name_plural = 'categories'
    
    def __str__(self):
        return self.name


class employ_drop(models.Model):
    name = models.CharField(max_length=200, db_index=True)
    url=models.CharField(max_length=100)
    parent_category = models.ForeignKey('self', related_name='subdrop', blank=True, null=True, on_delete=models.CASCADE)
    class Meta:
        ordering = ('name',)
        verbose_name = 'category'
        verbose_name_plural = 'categories'
    
    def __str__(self):
        return self.name


class admin_home_drop(models.Model):
    dashname = models.CharField(max_length=200, db_index=True)
    url=models.CharField(max_length=100)
    parent_category = models.ForeignKey('self', related_name='subhomedrop', blank=True, null=True, on_delete=models.CASCADE)
    progress_value=models.IntegerField(default="0")
    check_value=models.IntegerField(default="0")
    edit_url=models.CharField(max_length=100,default="")
    class Meta:
        ordering = ('dashname',)
        verbose_name = 'category'
        verbose_name_plural = 'categories'
    
    def __str__(self):
        return self.dashname



class loc_role_dropdown(models.Model):
    location=models.CharField(max_length=100)
    role=models.CharField(max_length=100)


class duration_year(models.Model):
    years=models.CharField(max_length=100)
    objects=models.Manager()

class duration_months(models.Model):
    months=models.CharField(max_length=100)
    objects=models.Manager()
    
class empdocs(models.Model):
    id=models.AutoField(primary_key=True)
    employ_id=models.ForeignKey(Employs,on_delete=models.CASCADE)
    empid=models.CharField(max_length=100)
    documenttype1=models.CharField(max_length=100)
    imagefile=models.ImageField(upload_to='images/')
    description=RichTextField()
    date=models.DateTimeField(default=datetime.now)
    email=models.CharField(max_length=100,default="")
    objects=models.Manager()
    def missing_info(self):
        required_info=['documenttype1','imagefile','description']
        missing_info = {}
        for field in required_info:
            if not getattr(self, field):
                missing_info[field] = 'Missing'
        return missing_info

    def __str__(self):
        return self.documenttype

class documents_setup(models.Model):
    document_type=models.CharField(max_length=100)
    compulsory=models.CharField(max_length=100, choices=(('Yes','Yes'),('No','No')))
    Enabled=models.CharField(max_length=100, choices=(('Yes','Yes'),('No','No')))

class Meta:
    db_table="documents_setup"    
   

class admin_doc(models.Model):
    id=models.AutoField(primary_key=True)
    admin=models.ForeignKey(AdminHod,on_delete=models.CASCADE)
    emp_id=models.CharField(max_length=100)
    documenttype1=models.CharField(max_length=100)
    imagefile1=models.ImageField(upload_to='media/')
    description=models.TextField()
    date=models.DateTimeField(default=datetime.now)
    objects=models.Manager()
    class Meta:
         db_table="admin_doc"




class typeofd(models.Model):    
    certificates=models.CharField(max_length=100)


class depart(models.Model):
    department=models.CharField(max_length=100)

    def __str__(self):
        return self.department
class Meta:
    db_table="depart"

class loca(models.Model):
    location=models.CharField(max_length=100)
    def __str__(self):
        return self.location
class Meta:
    db_table="loca"

class Employee_runpay(models.Model):
    employee_id = models.IntegerField(unique=True)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    department= models.ForeignKey(depart,on_delete=models.CASCADE)
    location = models.ForeignKey(loca,on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    monthly_ctc = models.DecimalField(max_digits=10, decimal_places=2)
    addition = models.DecimalField(max_digits=10, decimal_places=2)
    deduction = models.DecimalField(max_digits=10, decimal_places=2)
    reimbursement = models.DecimalField(max_digits=10, decimal_places=2)
    remarks = models.TextField(blank=True)
    gross_pay = models.DecimalField(max_digits=10, decimal_places=2, blank=True)

    def save(self, *args, **kwargs):
        self.gross_pay = float(self.monthly_ctc) + float(self.addition) - float(self.deduction) + float(self.reimbursement)
        super(Employee_runpay, self).save(*args, **kwargs)
class Meta:
    db_table="Employee_runpay"


class year(models.Model):
    id=models.AutoField(primary_key=True)
    employ_id=models.ForeignKey(Employs,on_delete=models.CASCADE)
    fin_year=models.CharField(max_length=100)
    duration=models.CharField(max_length=100)
    objects=models.Manager()


class LeaveReportEmploy(models.Model):
    id=models.AutoField(primary_key=True)
    leave_type=models.CharField(max_length=100,default="")
    employ_id=models.ForeignKey(Employs,on_delete=models.CASCADE)
    leave_date=models.DateField()
    email_leave=models.CharField(max_length=100,default="")
    to_date=models.DateField()
    leave_message=models.TextField()
    leave_status=models.IntegerField(default=0)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now_add=True)
    objects=models.Manager()
    def get_leave_duration(self):
        """
        Calculate and return the number of days for this leave request.
        """
        if self.leave_date and self.to_date:
            duration = (self.to_date - self.leave_date).days + 1  # Include both start and end days
            if duration == 2 and self.leave_date == self.to_date:
                return 1  # Consider a one-day leave with same start and end dates as one day
            return duration
        return 0

class LeaveReportAdmin(models.Model):
    id=models.AutoField(primary_key=True)
    leave_type=models.CharField(max_length=100)
    admin=models.ForeignKey(AdminHod,on_delete=models.CASCADE)
    leave_date=models.CharField(max_length=255)
    to_date=models.CharField(max_length=255,default="")
    leave_message=models.TextField()    
    leave_status=models.IntegerField(default=0)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now_add=True)
    objects=models.Manager()


class employ_add_form(models.Model):
    id=models.AutoField(primary_key=True)
    student_id=models.ForeignKey(Employs,on_delete=models.CASCADE,default="")
    firstname1=models.CharField(max_length=100,default="" )
    lastname1=models.CharField(max_length=100,default="")
    email2=models.CharField(max_length=100,default="")
    pan=models.CharField(max_length=100)
    ifsecode=models.CharField(max_length=100)
    acno = models.BigIntegerField(null=True, blank=True)
    beneficiaryname=models.CharField(max_length=100)
    phno=models.BigIntegerField()
    gender1=models.CharField(max_length=100)
    dob = models.DateField(null=True, blank=True)
    address1=models.CharField(max_length=500)
    heq=models.CharField(max_length=100)
    aadharno=models.BigIntegerField()
    fathername=models.CharField(max_length=100,default="")
    fathersdob=models.DateField(blank=True,null=True)
    mothername=models.CharField(max_length=100,default="")
    mothersdob=models.DateField(blank=True,null=True)
    Childdetails1=models.CharField(max_length=100,default="")
    Childdetails2=models.CharField(max_length=100,default="")
    maritalstatus=models.CharField(max_length=100,default="")
    workexperiance=models.CharField(max_length=100,default="")
    previousemploye=models.CharField(max_length=100,default="")
    previousdesignation=models.CharField(max_length=100,default="")
    Marriageannivarsary=models.CharField(max_length=100,default="")
    emergencycontactname=models.CharField(max_length=100,default="")
    emergencycontactnumber=models.CharField(max_length=100,default="")
    emergencycontactrelation=models.CharField(max_length=100,default="")
    nationality=models.CharField(max_length=100,default="")
    qualification=models.CharField(max_length=100,default="")

    bloodgroup=models.CharField(max_length=100)
    profile_pic=models.FileField(upload_to='media/')

    objects=models.Manager()
    def missing_info(self):
        required_info=['pan','ifsecode','acno','beneficiaryname','phno','gender1','dob','address1','heq','aadharno','bloodgroup','profile_pic']
        missing_info = {}
        for field in required_info:
            if not getattr(self, field):
                missing_info[field] = 'Missing'
        return missing_info

    def __str__(self):
        return self.pan
        

class task1(models.Model):
    Personalphonenumber1=models.CharField(max_length=100)
    PersonalEmailAddress1=models.CharField(max_length=100)
    FathersName1=models.CharField(max_length=100)
    FathersDOB1=models.CharField(max_length=100)
    MothersName1=models.CharField(max_length=100)
    MothersDOB1=models.CharField(max_length=100)
    SpousesName1=models.CharField(max_length=100)
    SpousesDOB1=models.CharField(max_length=100)
    Childdetails1=models.CharField(max_length=100)
    Childdetails2=models.CharField(max_length=100)
    TemporaryAddress1=models.CharField(max_length=100)
    HighestEducatonalQualification1=models.CharField(max_length=100)
    Addharnumber1=models.CharField(max_length=100)
    maritalstatus1=models.CharField(max_length=100)
    workexperiance1=models.CharField(max_length=100)
    previousemploye1=models.CharField(max_length=100)
    previousdesignation1=models.CharField(max_length=100)
    Marriageannivarsary1=models.CharField(max_length=100)
    emergencycontactname1=models.CharField(max_length=100)
    emergencycontactnumber1=models.CharField(max_length=100)
    emergencycontactrelation1=models.CharField(max_length=100)
    bloodgroup1=models.CharField(max_length=100)
    nationality=models.CharField(max_length=100)


        
class admin_add_form1(models.Model):
    id=models.AutoField(primary_key=True)
    admin=models.ForeignKey(AdminHod,on_delete=models.CASCADE,default="")
    firstname1=models.CharField(max_length=100,default="" )
    lastname1=models.CharField(max_length=100,default="")
    email2=models.CharField(max_length=100,default="")
    pan=models.CharField(max_length=100)
    ifsecode=models.CharField(max_length=100)
    acno=models.BigIntegerField()
    beneficiaryname=models.CharField(max_length=100)
    phno=models.BigIntegerField()
    gender1=models.CharField(max_length=100)
    dob=models.DateField()
    address1=models.CharField(max_length=500)
    heq=models.CharField(max_length=100)
    aadharno=models.BigIntegerField()
    bloodgroup=models.CharField(max_length=100)
    objects=models.Manager() 
    
    def missing_info(self):
        required_info=['pan','ifsecode','acno','beneficiaryname','phno','gender1','dob','address1','heq','aadharno','bloodgroup']
        missing_info = {}
        for field in required_info:
            if not getattr(self, field):
                missing_info[field] = 'Missing'
        return missing_info

    def __str__(self):
        return self.pan   


class  employ_payslip(models.Model):
    organization=models.CharField(max_length=100)
    address=models.CharField(max_length=500)
    employId=models.CharField(max_length=100)
    dateofbirth=models.DateField(max_length=100)
    panno=models.CharField(max_length=100)
    Hiringdate=models.DateField(max_length=100)
    role=models.CharField(max_length=100)
    annual_salary=models.CharField(max_length=100,default="")
    email=models.CharField(max_length=100,default="")
    current_year=models.CharField(max_length=100,default="")

class NotificationEmploy(models.Model):
    id = models.AutoField(primary_key=True)
    employ_id = models.ForeignKey(Employs, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()

class payslip_request(models.Model):
    student_id=models.ForeignKey(Employs,on_delete=models.CASCADE)
    duration=models.CharField(max_length=50)
    reason=models.CharField(max_length=120)
    status=models.CharField(max_length=50)
    date=models.DateField(default=None)
    remarks=models.CharField(max_length=100)
class Meta:
    db_table="payslip_request"


class employ_tax_form(models.Model):
    email=models.CharField(max_length=100)
    Current_Monthly_Rent=models.IntegerField()
    Name_of_landlord=models.CharField(max_length=100)
    PAN_of_landlord=models.CharField(max_length=100)
    Address_of_landlord=models.CharField(max_length=400)
    Section_80C=models.IntegerField()
    Section_80CCD=models.IntegerField()
    Section_80D=models.IntegerField()
    Section_80DD=models.IntegerField()
    Section_80E=models.IntegerField()
    Section_80EEB=models.IntegerField()
    Section_80G=models.IntegerField()
    Section_80U=models.IntegerField()
    Section_80DDB=models.CharField(max_length=100,default="")
    Section_80TTA=models.CharField(max_length=100,default="")
    Section_80TTB=models.CharField(max_length=100,default="")
    Annual_interest_payable=models.IntegerField()
    Additional_benefit_under_Section=models.IntegerField()
    Name_of_lender=models.CharField(max_length=100)
    PAN_of_lender=models.CharField(max_length=100)	
    Address_of_lender=models.CharField(max_length=400)	
    Section_80EEA=models.IntegerField()
    Amount=models.IntegerField()
    Origin=models.CharField(max_length=100)
    Destination=models.CharField(max_length=100)	
    home_rent_proof=models.ImageField(upload_to="images/",default="")
    employ = models.ForeignKey(Employs, on_delete=models.CASCADE)
    TravelStartDate=models.DateField(default=None)	
    House_Property_proof=models.ImageField(upload_to="images/",default="")
    Section_80EE_proof=models.ImageField(upload_to="images/",default="")
    Section_80EEA_proof=models.ImageField(upload_to="images/",default="")
    Section_80C_proof=models.ImageField(upload_to="images/",default="")
    Section_80D_proof=models.ImageField(upload_to="images/",default="")
    Section_80CCD1BS_proof=models.ImageField(upload_to="images/",default="")
    Section_80DD_proof=models.ImageField(upload_to="images/",default="")
    Section_80E_proof=models.ImageField(upload_to="images/",default="")
    Section_80G_proof=models.ImageField(upload_to="images/",default="")
    Section_80U_proof=models.ImageField(upload_to="images/",default="")
    Section_80EEB_proof=models.ImageField(upload_to="images/",default="")
    Section_80DDB_proof=models.ImageField(upload_to="images/",default="")
    Section_80TTA_proof=models.ImageField(upload_to="images/",default="")
    Section_80TTB_proof=models.ImageField(upload_to="images/",default="")
    from_date=models.DateField(default=None)	
    to_date=models.DateField(default=None)

class admin_tax_details(models.Model):
    email=models.CharField(max_length=100)
    Current_Monthly_Rent=models.IntegerField()
    Name_of_landlord=models.CharField(max_length=100)
    PAN_of_landlord=models.CharField(max_length=100)
    Address_of_landlord=models.CharField(max_length=400)
    Section_80C=models.IntegerField()
    Section_80CCD=models.IntegerField()
    Section_80D=models.IntegerField()
    Section_80DD=models.IntegerField()
    Section_80E=models.IntegerField()
    Section_80EEB=models.IntegerField()
    Section_80G=models.IntegerField()
    Section_80U=models.IntegerField()
    Section_80DDB=models.CharField(max_length=100,default="")
    Section_80TTA=models.CharField(max_length=100,default="")
    Section_80TTB=models.CharField(max_length=100,default="")
    Annual_interest_payable=models.IntegerField()
    Additional_benefit_under_Section=models.IntegerField()
    Name_of_lender=models.CharField(max_length=100)
    PAN_of_lender=models.CharField(max_length=100)	
    Address_of_lender=models.CharField(max_length=400)	
    Section_80EEA=models.IntegerField()
    Amount=models.IntegerField()
    Origin=models.CharField(max_length=100)
    Destination=models.CharField(max_length=100)	
    admin_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    home_rent_proof=models.ImageField(upload_to="images/",default="")
    TravelStartDate=models.DateField(default=None)	
    House_Property_proof=models.ImageField(upload_to="images/",default="")
    Section_80EE_proof=models.ImageField(upload_to="images/",default="")
    Section_80EEA_proof=models.ImageField(upload_to="images/",default="")
    Section_80C_proof=models.ImageField(upload_to="images/",default="")
    Section_80D_proof=models.ImageField(upload_to="images/",default="")
    Section_80CCD1BS_proof=models.ImageField(upload_to="images/",default="")
    Section_80DD_proof=models.ImageField(upload_to="images/",default="")
    Section_80E_proof=models.ImageField(upload_to="images/",default="")
    Section_80G_proof=models.ImageField(upload_to="images/",default="")
    Section_80U_proof=models.ImageField(upload_to="images/",default="")
    Section_80EEB_proof=models.ImageField(upload_to="images/",default="")
    Section_80DDB_proof=models.ImageField(upload_to="images/",default="")
    Section_80TTA_proof=models.ImageField(upload_to="images/",default="")
    Section_80TTB_proof=models.ImageField(upload_to="images/",default="")
    from_date=models.DateField(default=None)	
    to_date=models.DateField(default=None)	



@receiver(post_save,sender=CustomUser)
def create_user_profile(sender,instance,created,**kwargs):
    if created:
        if instance.user_type==1:
            AdminHod.objects.create(admin=instance)
        
        if instance.user_type==2:
            Employs.objects.create(admin=instance)
       

@receiver(post_save,sender=CustomUser)
def save_user_profile(sender,instance,**kwargs):
    if instance.user_type==1:
        instance.adminhod.save()
    if instance.user_type==2:
        instance.employs.save()
   

class otp(models.Model):
    amount=models.IntegerField()
    paymenttype=models.CharField(max_length=100)
class Meta:
    db_table="otp"

class checkin(models.Model):
    empid=models.CharField(max_length=100)
    status=models.CharField(max_length=100)
    date=models.DateField(default=None)
    time=models.TimeField(default=datetime.now)
    shift_name = models.CharField(max_length=100,default="")
    companyid=models.ForeignKey(Companys,on_delete=models.CASCADE,null=True,blank=True)
    is_employee=models.CharField(max_length=100,default="0")
class Meta:
    db_table="checkin"
    
class checkout(models.Model):
    date_value=models.IntegerField()
    empid=models.CharField(max_length=100)
    date=models.DateField(default=None)
    time=models.TimeField(default=datetime.now)
    created_at=models.DateTimeField(auto_now_add=True)
    shift_name = models.CharField(max_length=100,default="")
    companyid=models.ForeignKey(Companys,on_delete=models.CASCADE,null=True,blank=True)
    is_employee=models.CharField(max_length=100,default="0")

    def __str__(self):
        return f"checkout {self.id}: {self.data_value}"



class TDS(models.Model):
    id = models.AutoField(primary_key=True)
    tds_payment=models.CharField(max_length=100)
    verify_tan=models.CharField(max_length=100,default="")
    tds_filling_setup=models.CharField(max_length=10)
    filling_form=models.CharField(max_length=100)
    userid=models.CharField(max_length=100)
    password=models.CharField(max_length=100)
    username=models.CharField(max_length=100)
    password1=models.CharField(max_length=100)
    tds_payment1=models.CharField(max_length=100,default='')
    tds_filling_setup1=models.CharField(max_length=10,default='')
    tds_filling_setup2=models.CharField(max_length=10,default='')
    companyid=models.ForeignKey(Companys,on_delete=models.CASCADE,null=True,blank=True)
  
class P_tax(models.Model):
    id = models.AutoField(primary_key=True)
    professional_tax=models.CharField(max_length=100)
    pt_payment=models.CharField(max_length=100,default='')
    username3=models.CharField(max_length=100,default='')
    password4=models.CharField(max_length=100,default='')
    
    
class PF(models.Model):
    id = models.AutoField(primary_key=True)
    pf_status=models.CharField(max_length=100)
    pf_payment=models.CharField(max_length=100)
    username1=models.CharField(max_length=100)
    password2=models.CharField(max_length=100)
    pf_setup=models.CharField(max_length=100)
    pf_setup1=models.CharField(max_length=100,default='')
    pf_setup2=models.CharField(max_length=100,default='')
    pf_setup3=models.CharField(max_length=100,default='')
    pf_setup4=models.CharField(max_length=100,default='')

class ESIC(models.Model):
    id = models.AutoField(primary_key=True)
    esi_status=models.CharField(max_length=100)
    esi_payment=models.CharField(max_length=100)
    username2=models.CharField(max_length=100)
    password3=models.CharField(max_length=100)
    esi_settings=models.CharField(max_length=100)
    esi_settings1=models.CharField(max_length=100,default='')


class ad_salary(models.Model):
    employ = models.ForeignKey(Employs, on_delete=models.CASCADE)
    amount=models.IntegerField()
    request_status=models.IntegerField(default=0)
    emi=models.IntegerField()
    reason=models.CharField(max_length=100)

class admin_ad_salary(models.Model):
    admin_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    amount=models.IntegerField()
    request_status=models.IntegerField(default=0)
    emi=models.IntegerField()
    reason=models.CharField(max_length=100)


class Company(models.Model):
    company_Name=models.CharField(max_length=100)
    Address=models.CharField(max_length=200)
    PAN=models.CharField(max_length=100)
    TAN=models.CharField(max_length=100)
    GSTIN=models.CharField(max_length=100)
    KYCSTATUS=models.CharField(max_length=100)
    PFSTATUS=models.CharField(max_length=100)
    ESICSTATUS=models.CharField(max_length=100)
    PTSTATUS=models.CharField(max_length=100)
    LWFSTATUS=models.CharField(max_length=100)
    INCOMETAXPORTAL= models.CharField(max_length=200)
    TRACES=models.CharField(max_length=100)
    PF=models.CharField(max_length=100)
    ESIC=models.CharField(max_length=100)
    PT=models.CharField(max_length=100)
    
    def missing_info(self):
        required_info=['company_Name ','Address','PAN','TAN','GSTIN','KYCSTATUS','PFSTATUS','ESICSTATUS','PTSTATUS','LWFSTATUS','INCOMETAXPORTAL','TRACES','PF','ESIC','PT']
        missing_info = {}
        for field in required_info:
            if not getattr(self, field):
                missing_info[field] = 'Missing'
        return missing_info

    def __str__(self):
        return self.Name



STATE_CHOICES=((
    ('Andaman and Nicobar Islands','Andaman and Nicobar Islands'),
    ('Andhra pradesh','Andhra pradesh'),
    ('Arrunachal prodesh','Arrunachal prodesh'),
    ('Assam','Assam'),
    ('Bihar','Bihar'),
    ('chandigarh','chandigarh'),
    ('Chhattisgarh','Chhattisgarh'),
    ('Dadra and Nagar haveli','Dadra and Nagar haveli'),
    ('Daman and Diu','Daman and Diu'),
    ('Delhi','Delhi'),
    ('Goa','Goa'),
    ('Gujarat','Gujarat'),
    ('Haryana','Haryana'),
    ('Himachal Pradesh','Himachal Pradesh'),
    ('Jammu and kashmir','Jammu and kashmir'),
    ('Uttar Pradesh','Jharkhand'),
    ('Karnataka','Karnataka'),
    ('Kerala','Kerala'),
    ('Ladakh','Ladakh'),
    ('Lakshadweep','Lakshadweep'),
    ('Madhya pradesh','Madhya pradesh'),
    (' Maharashtra',' Maharashtra'),
    ('Manipur','Manipur'),
    ('Meghalaya','Meghalaya'),
    ('Mizoram','Mizoram'),
    ('Nagaland','Nagaland'),
    ('Odisha','Odisha'),
    ('Puducherry','Puducherry'),
    ('Punjab','Punjab'),
    ('Rajasthan','Rajasthan'),
    ('Sikkim','Sikkim'),
    ('Tamil Nadu','Tamil Nadu'),
    ('Telangana','Telangana'),
    ('Tripura','Tripura'),
    ('Uttar Pradesh','Uttar Pradesh'),
    ('Uttarakhand','Uttarakhand'),
    ('West Bengal','West Bengal'),
))

   


# Create your models here.
class company_details(models.Model):
    Organisationtype=models.CharField(max_length=100)
    companypan=models.CharField(max_length=100,default="")
    companyname=models.CharField(max_length=100,default="")
    companyGSTIN=models.CharField(max_length=100)
    brandname=models.CharField(max_length=100)
    registeraddress=models.CharField(max_length=100)
    address=models.CharField(max_length=100)
    State=models.CharField(choices=STATE_CHOICES,max_length=100,default="Andhra pradesh")
    pincode=models.IntegerField(default="0")
    logo=models.ImageField(upload_to="images/",default="")
    companyid=models.ForeignKey(Companys,on_delete=models.CASCADE,null=True,blank=True)
class Meta:
    db_table="company_details" 

class details(models.Model):
    id = models.AutoField(primary_key=True)
    form1=models.CharField(max_length=100)
    form2=models.CharField(max_length=100)
    form3=models.CharField(max_length=100)

class company_logo(models.Model):
    logo=models.ImageField(upload_to="media/")
class meta:
    db_table="company_logo"



class masterctc(models.Model):
    id=models.AutoField(primary_key=True)
    employ_id=models.ForeignKey(Employs,on_delete=models.CASCADE)
    objects=models.Manager()

class Department(models.Model):
    attribute = models.CharField(max_length=100)


class Employee(models.Model):
    empname=models.CharField(max_length=100)
    department_id = models.ForeignKey(Department, on_delete=models.CASCADE)
    salary = models.DecimalField(max_digits=10, decimal_places=2)
    final_year = models.DateField(default=None)

class pay_contractors(models.Model):
    paymentdate=models.DateField(default=None)
    invoicedate=models.DateField(default=None)
    searchcontractors=models.CharField(max_length=100,default="")
    image=models.ImageField(upload_to="images/",default="")
    repeatpayment=models.CharField(max_length=100)
    amount=models.IntegerField()
    tax=models.IntegerField()
    anyremarks=models.CharField(max_length=100)
    purpose=models.CharField(max_length=100)
    tds=models.CharField(max_length=100)
    taxcode=models.CharField(max_length=100)
    
class Meta:
    db_table="pay_contractors" 

class companylogo(models.Model):
    id=models.AutoField(primary_key=True)
    logo1=models.ImageField(upload_to="media/")
    # description=models.CharField(max_length=1000,default="")
    objects = models.Manager()
class Meta:
    db_table="companylogo" 

class company_details_first(models.Model):
    admin_id=models.ForeignKey(AdminHod,on_delete=models.CASCADE)
    Organisation_Name=models.CharField(max_length=500)
    companypan=models.CharField(max_length=700)
    companyname=models.CharField(max_length=600)
    companyGSTIN=models.CharField(max_length=800)
    brandname=models.CharField(max_length=100)
    registeraddress=models.CharField(max_length=1000)
    address=models.CharField(max_length=100)
    State=models.CharField(max_length=100)
    pincode=models.IntegerField(default="0")
    objects = models.Manager()



class set_payroll_date(models.Model):
    id=models.AutoField(primary_key=True)
    payrolldate=models.CharField(max_length=100,default="")
    auto_run_payroll=models.CharField(max_length=100)
    advance_salary_request=models.CharField(max_length=100)
    payroll=models.CharField(max_length=100,default="")
    objects = models.Manager()

class set_salary_structure(models.Model):
    id=models.AutoField(primary_key=True)
    default_salary=models.CharField(max_length=100)
    FBP_allowances=models.CharField(max_length=100)
    objects = models.Manager()


class salary_struc(models.Model):
    salarycomponent=models.CharField(max_length=100)
    percentageofCTC=models.CharField(max_length=100)
    percentageorfixed=models.CharField(max_length=100)
    Taxable=models.CharField(max_length=100)

class Meta:
    db_table="salary_struc"

class salary_struct(models.Model):
    salarycomponent=models.CharField(max_length=100)
    percentageofCTC=models.CharField(max_length=100)
    percentageorfixed=models.CharField(max_length=100)
    Taxable=models.CharField(max_length=100)
class Meta:
    db_table="salary_struct"

class Progress(models.Model):
    value = models.IntegerField(default=0)
    value1 = models.IntegerField(default=0)
    value2 = models.IntegerField(default=0)
    value3 = models.IntegerField(default=0)
    value4 = models.IntegerField(default=0)
    value5 = models.IntegerField(default=0)
    
    progress_form1=models.CharField(max_length=100,default=0)
    progress_form2=models.CharField(max_length=100,default=0)
    progress_form3=models.CharField(max_length=100,default=0)
    progress_form4=models.CharField(max_length=100,default=0)
    progress_form5=models.CharField(max_length=100,default=0)
    progress_form6=models.CharField(max_length=100,default=0)

class admin_chart_ac(models.Model):
    chart_ac_name=models.CharField(max_length=100)
    chart_ac_email=models.EmailField(max_length=100)
    chart_ac_no=models.IntegerField()
class Meta:
    db_table="admin_chart_ac"


class employlev(models.Model):
    type=models.CharField(max_length=1000,default="name")
    defaultleave=models.IntegerField(default="4")
    leave_id=models.IntegerField(default="1")
class Meta:
    db_table="employlev"


class pvt_pub(models.Model):
    id=models.AutoField(primary_key=True)
    certificate=models.FileField(upload_to="media/")
    cmpny_pancard=models.FileField(upload_to="media/")
    cheque=models.FileField(upload_to="media/")
    owner_pancard=models.FileField(upload_to="media/")
    id_proof=models.FileField(upload_to="media/")
    gst=models.FileField(upload_to="media/")
    admin_id = models.ForeignKey(AdminHod,on_delete=models.CASCADE,default="")

class Meta:
    db_table="pvt_pub"

class sole_proprietorship(models.Model): 
    id=models.AutoField(primary_key=True)   
    gst_certificate=models.FileField(upload_to="media/")
    cancelled_cheque=models.FileField(upload_to="media/")
    owner_pancard1=models.FileField(upload_to="media/")
    idproof=models.FileField(upload_to="media/")
    GST=models.FileField(upload_to="media/")  
    admin_id = models.ForeignKey(AdminHod,on_delete=models.CASCADE,default="")

class Meta:
    db_table="sole_proprietorship"

class partnership(models.Model):    
    id=models.AutoField(primary_key=True)
    shop_license=models.FileField(upload_to="media/")
    cmpny_pan=models.FileField(upload_to="media/")
    cheque1=models.FileField(upload_to="media/")
    owner_pan=models.FileField(upload_to="media/")
    id_proof1=models.FileField(upload_to="media/")
    gst1=models.FileField(upload_to="media/")
    admin_id = models.ForeignKey(AdminHod,on_delete=models.CASCADE,default="")

class Meta:
    db_table="partnership"

class trust_ngo(models.Model): 
    id=models.AutoField(primary_key=True)  
    shop_license1=models.FileField(upload_to="media/")
    cmpny_pan1=models.FileField(upload_to="media/")
    cheque2=models.FileField(upload_to="media/")
    owner_pan1=models.FileField(upload_to="media/")
    id_proof2=models.FileField(upload_to="media/")
    gst2=models.FileField(upload_to="media/")
    admin_id = models.ForeignKey(AdminHod,on_delete=models.CASCADE,default="")

class Meta:
    db_table="trust_ngo"

class reimbursementsetup(models.Model):
    Reimbursements_Enabled=models.CharField(max_length=100)
    Make_attachments_compulsory=models.CharField(max_length=100)
    Include_reimbursements_with_payroll=models.CharField(max_length=100)
    # selected_reimbursements = models.CharField(max_length=500, null=True, blank=True)

class Meta:
    db_table="reimbursementsetup"

class reimbursementsetup1(models.Model):
    reimbursement_type = models.CharField(max_length=100, null=True, blank=True)
    select_reimbursement=models.CharField(max_length=100, choices=(('Yes','Yes'),('No','No')),default="")

class Meta:
    db_table="reimbursementsetup1"


class employ_help(models.Model):
    image1=models.ImageField(upload_to="media/")
    image2=models.ImageField(upload_to="media/")
    image3=models.ImageField(upload_to="media/")
    image4=models.ImageField(upload_to="media/")
    image5=models.ImageField(upload_to="media/")
class Meta:
    db_table="employ_help"

class integrations(models.Model):
    name=models.CharField(max_length=100)
    img=models.ImageField(upload_to='media/')
    purpose=models.CharField(max_length=100)
    description=models.CharField(max_length=100)
    btn=models.CharField(max_length=100,default='')
    footer=models.CharField(max_length=100,default='')
    url=models.CharField(max_length=100,default='')
class Meta:
    db_table="icon"

class app(models.Model):
    response=models.CharField(max_length=100)
class Meta:
    db_table="app" 

class MonthlyTotal(models.Model):
    id=models.AutoField(primary_key=True)
    student_id=models.ForeignKey(Employs,on_delete=models.CASCADE)
    year = models.IntegerField()
    month = models.IntegerField()
    total = models.IntegerField()
    month_and_year = models.CharField(max_length=20,default="")
    def __str__(self):
        return f"{self.get_month_display()} {self.year}: {self.total}"


class adminMonthlyTotal(models.Model):
    id=models.AutoField(primary_key=True)
    student_id=models.ForeignKey(AdminHod,on_delete=models.CASCADE)
    year = models.IntegerField()
    month = models.IntegerField()
    total = models.IntegerField()
    month_and_year = models.CharField(max_length=20,default="")
    def __str__(self):
        return f"{self.get_month_display()} {self.year}: {self.total}"


class employhelp(models.Model):
    image1=models.ImageField(upload_to="media/")
    image2=models.ImageField(upload_to="media/")
    image3=models.ImageField(upload_to="media/")
    image4=models.ImageField(upload_to="media/")
    image5=models.ImageField(upload_to="media/")
class Meta:
    db_table="employhelp"



#settings models:


from django.db import models

# Create your models here.
class check(models.Model):
    EnabledAttendance=models.CharField(max_length=50,choices=(('Yes','Yes'),('No','No'))) 
    
    AllowEmployees=models.CharField(max_length=50,choices=(('Yes','Yes'),('No','No'))) 
    AllowHalfdayleave=models.CharField(max_length=50,choices=(('Yes','Yes'),('No','No'))) 
    Employeemustenter=models.CharField(max_length=50,choices=(('Yes','Yes'),('No','No'))) 
    Showattendence=models.CharField(max_length=50,choices=(('Yes','Yes'),('No','No'))) 
    automaticallyadd=models.CharField(max_length=50,choices=(('Yes','Yes'),('No','No'))) 
    lossofpay=models.CharField(max_length=64,choices=(('Yes','Yes'),('No','No'))) 
    usefinancal=models.CharField(max_length=50,choices=(('Yes','Yes'),('No','No'))) 
    track=models.CharField(max_length=50,choices=(('Yes','Yes'),('No','No'))) 
    type=models.CharField(max_length=100)
    defaultleave=models.CharField(max_length=100)
    monthlyincrement=models.CharField(max_length=100)
    maxleave=models.CharField(max_length=100)
    carryforward=models.CharField(max_length=100)
    Defaultshift=models.CharField(max_length=100)
    graceperiod=models.CharField(max_length=100)
    fulltime=models.CharField(max_length=100)
    halftime=models.CharField(max_length=100)
    date=models.DateField()
    description=models.CharField(max_length=100)
    attendanceenabled=models.CharField(max_length=50,choices=(('Yes','Yes'),('No','No')))
    all = models.CharField(max_length=50, choices=(('Yes', 'Yes'), ('No', 'No')), default='No')    
    andhrapradesh = models.CharField(max_length=50, choices=(('Yes', 'Yes'), ('No', 'No')), default='No')
    telangana = models.CharField(max_length=50, choices=(('Yes', 'Yes'), ('No', 'No')), default='No')
    date2 = models.CharField(max_length=100,default="")
    description2 = models.CharField(max_length=100,default="")
    day = models.CharField(max_length=50, default='Monday')  
    holidays=models.CharField(max_length=100,default="")
    weekend=models.CharField(max_length=100,default="N0") 

from django.db import models

class YourModel(models.Model):
    all = models.CharField(max_length=3, choices=(('Yes', 'Yes'), ('No', 'No')), default='No')


class default_salary_structure(models.Model):
    default_salary=models.CharField(max_length=100,choices=(('Yes','Yes'),('No','No')))
    salarycomponent=models.CharField(max_length=100)
    percentageofCTC=models.CharField(max_length=100)
    percentageorfixed=models.CharField(max_length=100)
    Taxable=models.CharField(max_length=100)
class Meta:
    db_table="default_salary_structure"   

class default_salary(models.Model):
    default_sal=models.CharField(max_length=100,choices=(('Yes','Yes'),('No','No')))
    
class Meta:
    db_table="default_salary"   


class reimbursement_setup_settings(models.Model):
    document_type=models.CharField(max_length=100,default="")
    Enabled=models.CharField(max_length=100, choices=(('Yes','Yes'),('No','No')))
    Reimbursements_Enabled=models.CharField(max_length=100,choices=(('Yes','Yes'),('No','No')))
    Make_attachments_compulsory=models.CharField(max_length=100,choices=(('Yes','Yes'),('No','No')))
    Include_reimbursements_with_payroll=models.CharField(max_length=100,choices=(('Yes','Yes'),('No','No')))
class Meta:
    db_table="reimbursement_setup_settings"


class emp_reg_setup(models.Model):
    resignations=models.CharField(max_length=50)
class Meta:
    db_table="emp_reg_setup"


class tdsfillingsetup(models.Model):
    Automated_filling24=models.CharField(max_length=100,choices=(('Yes','Yes'),('No','No')))
    Automated_filling26=models.CharField(max_length=100,choices=(('Yes','Yes'),('No','No')))
class Meta:
    db_table="tdsfillingsetup"

class employedata(models.Model):
    employe_id_prefix=models.CharField(max_length=100)
    employe_directory=models.CharField(max_length=100,choices=(('Yes','Yes'),('No','No')))
    additionalinfo=models.CharField(max_length=100,choices=(('Yes','Yes'),('No','No')))

class Meta:
    db_table="employedata"

class tax_deduction(models.Model):
     approval=models.CharField(max_length=300)
     verify=models.CharField(max_length=300)
     taxable=models.CharField(max_length=300)
class Meta:
    db_table="tax_deduction"

class empnotificationupdate(models.Model):
    id = models.AutoField(primary_key=True)
    send_email_notify=models.CharField(max_length=500)
    email_notify=models.CharField(max_length=500)

class documents_setup(models.Model):
    document_type=models.CharField(max_length=100)
    compulsory=models.CharField(max_length=100, choices=(('Yes','Yes'),('No','No')))
    Enabled=models.CharField(max_length=100, choices=(('Yes','Yes'),('No','No')))

class Meta:
    db_table="documents_setup"  


  
class editholiday12(models.Model):
    companyid= models.ForeignKey(Companys, on_delete=models.CASCADE,default="1")
    sun=models.BooleanField(null=True,blank=True)
    sat1=models.BooleanField(null=True,blank=True)
    sat2=models.BooleanField(null=True,blank=True)
    sat3=models.BooleanField(null=True,blank=True)
    sat4=models.BooleanField(null=True,blank=True)
    sat5=models.BooleanField(null=True,blank=True)
    alsat=models.BooleanField(null=True,blank=True)
    mon=models.BooleanField(null=True,blank=True)
    tue=models.BooleanField(null=True,blank=True)
    web=models.BooleanField(null=True,blank=True)
    thu=models.BooleanField(null=True,blank=True)
    fri=models.BooleanField(null=True,blank=True)
    
class Meta:
    db_table="editholiday"


class customholidays(models.Model):
    date=models.DateField(null=True,blank=True)
    reason=models.CharField(max_length=100)
    companyid=models.ForeignKey(Companys,on_delete=models.CASCADE)
class Meta:
    db_table="customholidays"


class halfldayvreason(models.Model):
    halfdaylev=models.BooleanField(default="0",null=True,blank=True)
    reason1=models.BooleanField(default="0",null=True,blank=True)
class Meta:
    db_table="halfdayreason"

class publicholidays(models.Model):
    publicholiday_date=models.DateField()
    festival_name=models.CharField(max_length=100)
    finding=models.BooleanField(default='0', null=True,blank=True)
    companyid=models.ForeignKey(Companys,on_delete=models.CASCADE)

class Meta:
    db_table="publicholidays"



class employlevsheet(models.Model):
    causalleave=models.IntegerField()
    medicalleave=models.IntegerField()
    earnedleave=models.IntegerField()
class Meta:
    db_table="employlevsheet"



class taskdata(models.Model):
    p_name = models.CharField(max_length=100)
    p_url = models.CharField(max_length=200)
    team_lead = models.IntegerField()
    date = models.DateTimeField(auto_now_add=True )
class Meta:
    db_table="taskdata"
from datetime import date


# class projecttask(models.Model):
#     p_name = models.ForeignKey(Project, on_delete=models.CASCADE)
#     tasks = models.CharField(max_length=100)
#     l_name = models.CharField(max_length=100)
#     task_date = models.DateField(default=None
#     def get_status(self):
#         today = date.today()

#         if self.task_date < today:
#             return "Completed"
#         elif self.task_date == today:
#             return "Ongoing"
#         else:
#             return "Upcoming"
from datetime import date
from datetime import time

class projecttask(models.Model):
    p_name = models.ForeignKey(Project, on_delete=models.CASCADE)
    tasks = models.CharField(max_length=100)
    l_name = models.CharField(max_length=100)
    task_date = models.DateField(default=date.today())
    task_time = models.TimeField(default='00:00')

    def get_status(self):
        current_datetime = datetime.combine(self.task_date, self.task_time)
        current_datetime_now = datetime.now()

        end_of_day = datetime.combine(current_datetime_now.date(), time(23, 59, 59))

        if current_datetime.date() < current_datetime_now.date():
            return "Completed"
        elif current_datetime <= end_of_day:
            return "Pending"
        else:
            return "Upcoming"




class tlassigntask(models.Model):
    task=models.CharField(max_length=100)
    employid=models.IntegerField()
    project_id=models.IntegerField(default="0")
    task_date=models.DateField(default=date.today())
    companyid=models.ForeignKey(Companys,on_delete=models.CASCADE,default="1")
class Meta:
     db_table="tlassigntask"



class employperformance(models.Model):
    project_name = models.ForeignKey(Project, on_delete=models.CASCADE)
    employ_name = models.ForeignKey(Employs, on_delete=models.CASCADE)
    project_task1 = models.ForeignKey(projecttask, on_delete=models.CASCADE, null=True, default=None)
    performance = models.BigIntegerField()
    date = models.DateField(default=None)

    @property
    def task_name(self):
        if self.project_task1:
            return self.project_task1.tasks
        return None

    @property
    def task_date(self):
        if self.project_task1:
            return self.project_task1.task_date
        return None

    @property
    def task_time(self):
        if self.project_task1:
            return self.project_task1.task_time
        return None

    class Meta:
        db_table = "employperformance"



class Meeting(models.Model):
    meeting_url = models.CharField(max_length=500)
    team_member = models.CharField(max_length=100)
    date = models.DateTimeField(default=datetime.now)


    def __str__(self):
        return f"Meeting for {self.team_member.first_name} {self.team_member.last_name}"
    
from django.db import models

class employ_nav(models.Model):
    is_name_exist = models.BooleanField(default=False)
    is_tl_option = models.BooleanField(default=False)

    def __str__(self):
        return f"employ_nav: {self.id} - Name Exists: {self.is_name_exist}, TL Option: {self.is_tl_option}"

class projectmanager(models.Model):
    b_name = models.CharField(max_length=100)
    o_id = models.ForeignKey(AdminHod, on_delete=models.CASCADE)
    id=models.AutoField(primary_key=True)
    admin=models.OneToOneField(CustomUser,on_delete=models.CASCADE)
    first_name=models.CharField(max_length=100)
    last_name=models.CharField(max_length=100)
    email=models.CharField(max_length=100)
    web_mail=models.CharField(max_length=100)
    username=models.CharField(max_length=100)
    password=models.CharField(max_length=100)
    gender=models.CharField(max_length=255)
    address=models.TextField()
    empid=models.CharField(max_length=100)
    Manager=models.CharField(max_length=100)
    dateofbirth = models.DateField(default=None)
    dateofjoining=models.DateField(default=None)
    role=models.CharField(max_length=100)
    location=models.CharField(max_length=100)
    package=models.CharField(max_length=100)
    pincode=models.CharField(max_length=100)
    contactno=models.CharField(max_length=100)
    status=models.CharField(max_length=100)
    bloodgroup=models.CharField(max_length=100)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now_add=True)
    insert=models.CharField(max_length=500)
    is_team_lead = models.BooleanField(default=False)
    hroptions=models.IntegerField(default=1)
    projectmanagerop=models.IntegerField(default=2)
    fcm_token=models.TextField()
    objects = models.Manager()
    class Meta:
        db_table="projectmanager"