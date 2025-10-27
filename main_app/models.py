from django.db import models
from django.contrib.auth import get_user_model
# Create your models here.

# -------------------------🔸 User model 🔸-------------------------
User = get_user_model()


# -------------------------🔸 Profile model 🔸-------------------------
class Profile(models.Model):
    
    ROLE_TYPES = (
        ('admin', 'Admin'),
        ('employee', 'Employee'),
    )
    
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    role = models.CharField(max_length=20, choices=ROLE_TYPES, default=ROLE_TYPES[0][0])
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"Profile: {self.first_name} {self.last_name} - Role: {self.role}"


# -------------------------🔸 Department model 🔸-------------------------
class Department(models.Model):
    name = models.CharField(max_length=100)
    manager_name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name


# -------------------------🔸 Employee model 🔸-------------------------
class Employee(models.Model):
    job_title = models.CharField(max_length=100)
    hire_date = models.DateField('Hire date')

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"Employee name: {self.user.username} - {self.job_title}"


# -------------------------🔸 LeaveType model 🔸-------------------------
class LeaveType(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    max_days_allowed = models.PositiveIntegerField()
    
    def __str__(self):
        return self.name


# -------------------------🔸 LeaveRequest model 🔸-------------------------
class LeaveRequest(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]
    
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
        return f"{self.employee.user.username} - {self.leave_type.name}"


# -------------------------🔸 LeaveHistory model 🔸-------------------------
class LeaveHistory(models.Model):
    ACTION_CHOICES = [
        ('submitted', 'Submitted'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]
    
    action_type = models.CharField(max_length=20, choices=ACTION_CHOICES)
    action_date = models.DateTimeField(auto_now_add=True)
    note = models.TextField(blank=True)
    
    leave_request = models.ForeignKey(LeaveRequest, on_delete=models.CASCADE)
    action_by_user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.leave_request} - {self.action_type}"


# -------------------------🔸 LeaveBalance model 🔸-------------------------
class LeaveBalance(models.Model):
    total_days = models.PositiveIntegerField()
    used_days = models.PositiveIntegerField(default=0)
    remaining_days = models.PositiveIntegerField()
    last_updated = models.DateTimeField(auto_now=True)
    
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    leave_type = models.ForeignKey(LeaveType, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.employee} - {self.leave_type}: {self.remaining_days}"
    
    class Meta:
        unique_together = ['employee', 'leave_type']