from django.db import models
from django.contrib.auth import get_user_model
# Create your models here.

# -------------------------🔸 User model 🔸-------------------------
User = get_user_model()


# -------------------------🔸 Employee model 🔸-------------------------
class Employee(models.Model):
    
    DEPARTMENT_CHOICES = (
        ('HR', 'Human Resources'),
        ('MKT', 'Marketing'),
        ('R&D', 'Research & Development'),
        ('SALES', 'Sales'),
        ('FIN', 'Finance'),
        ('IT', 'Information Technology'),
        ('ADMIN', 'Administration'),
        ('CS', 'Customer Service'),
        ('ACC', 'Accounting'),
        ('QA', 'Quality Assurance'),
        ('MNT', 'Maintenance'),
        ('BIZ', 'Business'),
        ('DES', 'Designing'),
        ('LEAD', 'Leadership'),
        ('LEGAL', 'Legal'),
        ('OTHER', 'Other')
    )
    
    ROLE_TYPES = (
        ('admin', 'Admin'),
        ('employee', 'Employee'),
    )

    job_title = models.CharField(max_length=100)
    department = models.CharField(max_length=20, choices=DEPARTMENT_CHOICES, default='OTHER', null=False, blank=False)
    role = models.CharField(max_length=20, choices=ROLE_TYPES, default='employee')
    hire_date = models.DateField('Hire date')

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"Employee name: {self.user.first_name} {self.user.last_name} - {self.job_title} ({self.get_role_display()})"


# -------------------------🔸 LeaveType model 🔸-------------------------
class LeaveType(models.Model):
    
    LEAVE_TYPES = (
        ('ANNUAL', 'Annual Leave'),
        # ('STUDY', 'Study Leave'),
        ('EMERGENCY', 'Emergency Leave'),
        ('SICK', 'Sick Leave'),
        ('PATIENT_CARE', 'Patient Care Leave'),
        ('SPECIAL', 'Special Leave'),
        ('BEREAVEMENT', 'Bereavement Leave'),
        # ('NATIONAL', 'National Participation Leave'),
    )
    
    type = models.CharField(max_length=20, choices=LEAVE_TYPES, unique=True, default='SPECIAL')
    description = models.TextField(blank=True)
    max_days_allowed = models.PositiveIntegerField()
    
    def save(self, *args, **kwargs):
        # set `description` and `max_days_allowed` for the Leave Type
        if not self.description: self.description = self.get_description()
        if not self.max_days_allowed: self.max_days_allowed = self.get_max_days_allowed()
        # save it to the db
        super().save(*args, **kwargs)
    
    # 
    def get_description(self):
        descriptions = {
            'ANNUAL': 'Regular annual vacation for employees',
            # 'STUDY': 'Leave for educational exams and study purposes',
            'EMERGENCY': 'Urgent leave for unforeseen circumstances',
            'SICK': 'Medical leave for health-related issues',
            'PATIENT_CARE': 'Leave to accompany and care for sick family members',
            'SPECIAL': 'Exceptional leave for special circumstances',
            'BEREAVEMENT': 'Leave in case of family member death',
            # 'NATIONAL': 'Leave for national events and participation',
        }
        return descriptions.get(self.type, '')
    
    def get_max_days_allowed(self):
        max_days = {
            'ANNUAL': 30,
            # 'STUDY': , # --------> Depends on number of study days
            'EMERGENCY': 3,
            'SICK': 30,
            'PATIENT_CARE': 5,
            'SPECIAL': 10000, # -------> # of days is not specified (indefinitely), it Just required the `Approved`!
            'BEREAVEMENT': 5,
            # 'NATIONAL': , # --------> Depends on number of national events days
        }
        return max_days.get(self.type, 0)
    
    def __str__(self):
        return self.get_type_display()

# -------------------------🔸 LeaveRequest model 🔸-------------------------
class LeaveRequest(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    )
    
    start_date = models.DateField()
    end_date = models.DateField()
    reason = models.TextField()
    # attachment = models.FileField(blank=True, null=True) --> optional (i will do it later)
    is_outside_country = models.BooleanField(default=False)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    leave_type = models.ForeignKey(LeaveType, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.employee.user.first_name} - {self.leave_type.get_type_display()}"


# -------------------------🔸 LeaveHistory model 🔸-------------------------
class LeaveHistory(models.Model):
    ACTION_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]
    
    action_type = models.CharField(max_length=20, choices=ACTION_CHOICES)
    action_date = models.DateTimeField(auto_now_add=True)
    note = models.TextField(blank=True)
    
    leave_request = models.ForeignKey(LeaveRequest, on_delete=models.CASCADE)
    action_by_user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"LeaveHistory: {self.leave_request.leave_type.get_type_display()} - {self.action_type}, Employee: {self.leave_request.employee.user.first_name}"


# -------------------------🔸 LeaveBalance model 🔸-------------------------
class LeaveBalance(models.Model):
    total_days = models.PositiveIntegerField(default=30)
    used_days = models.PositiveIntegerField(default=0)
    remaining_days = models.PositiveIntegerField()
    last_updated = models.DateTimeField(auto_now=True)
    
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    leave_type = models.ForeignKey(LeaveType, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.employee.user.first_name} - {self.leave_type.get_type_display()}: {self.remaining_days}"
    
    class Meta:
        unique_together = ['employee', 'leave_type']