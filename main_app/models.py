from django.db import models
from django.contrib.auth import get_user_model

from django.forms import ValidationError
from datetime import date

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
    
    def get_leave_balance(self, leave_type):
        # Get specific leave balance for this employee
        try:
            return LeaveBalance.objects.get(employee=self, leave_type=leave_type)
        except LeaveBalance.DoesNotExist:
            return None

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
    
    type = models.CharField(max_length=20, choices=LEAVE_TYPES, unique=True, blank=False, null=False)
    description = models.TextField(blank=True)
    max_days_allowed = models.PositiveIntegerField(blank=True)
    
    def __str__(self):
        return self.get_type_display()


# -------------------------🔸 LeaveBalance model 🔸-------------------------
class LeaveBalance(models.Model):
    total_days = models.PositiveIntegerField(default=0)
    used_days = models.PositiveIntegerField(default=0)
    remaining_days = models.PositiveIntegerField()

    # Additional management fields
    warning_threshold = models.PositiveIntegerField(default=5) # if the `remaining_days` = 5, warning apear!
    is_active = models.BooleanField(default=True) # is this leave balance active or not?
    reset_date = models.DateField() 
    last_updated = models.DateTimeField(auto_now=True)

    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    leave_type = models.ForeignKey(LeaveType, on_delete=models.CASCADE)
    

    def save(self, *args, **kwargs):
        # Calculate `remaining_days` automatically
        self.remaining_days = self.total_days - self.used_days
        
        # Set `total_days` from LeaveType (if not set)
        if not self.total_days:
            self.total_days = self.leave_type.max_days_allowed
        
        # Set `reset_date` to end of current year
        if not self.reset_date:
            self.reset_date = date(date.today().year, 12, 31)
        
        # Save it to the DB
        super().save(*args, **kwargs)


    # Get warning (status) and (message) based on `remaining_days`
    def get_warning_status(self):
        if self.remaining_days <= 0:
            return "danger", "❌ No balance remaining - salary may be affected"
        elif self.remaining_days <= self.warning_threshold:
            return "warning", f"⚠️ Low balance - only {self.remaining_days} days remaining"
        else:
            return "safe", f"✅ Good balance - {self.remaining_days} days remaining"
    

    # Check if employee can request this many days of leave
    def can_request_leave(self, requested_days):
        # Special leave type has NO limit (only requires approval)
        if self.leave_type.type == 'SPECIAL':
            return True, "SPECIAL leave has NO limit - requires approval !"
        
        # Check if `requested_days` exceed `remaining_days`
        if requested_days > self.remaining_days:
            return False, f"Requested {requested_days} days but only {self.remaining_days} available"
        
        # Check if `requested_days` exceed `max_days_allowed` for this type
        if requested_days > self.leave_type.max_days_allowed:
            return False, f"Cannot request more than {self.leave_type.max_days_allowed} days for {self.leave_type.get_type_display()}"
        
        return True, "Leave request is valid"
    

    # Reduce days from balance
    def reduce_days(self, days_to_reduce):
        if days_to_reduce <= self.remaining_days:
            self.used_days += days_to_reduce
            self.save()
            return True
        return False
    

    def __str__(self):
        return f"{self.employee.user.first_name} - {self.leave_type.get_type_display()}: {self.remaining_days}"
    
    class Meta:
        # this for prevent duplicate balances for same employee and leave type!
        unique_together = ['employee', 'leave_type']


# -------------------------🔸 LeaveRequest model 🔸-------------------------
class LeaveRequest(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    )
    
    start_date = models.DateField()
    end_date = models.DateField()
    total_days = models.PositiveIntegerField(blank=True, null=True) # --> Auto-Computed field
    reason = models.TextField()
    # attachment = models.FileField(blank=True, null=True) --> optional (i will do it later)
    is_outside_country = models.BooleanField(default=False)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, null=True, blank=True, default=None)
    created_at = models.DateTimeField(auto_now_add=True)
    
    # Warning system fields that related to leave balance
    warning_message = models.TextField(blank=True, help_text="Warning message if balance is insufficient")
    is_warning_displayed = models.BooleanField(default=False, help_text="Whether warning was shown to employee")

    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    leave_type = models.ForeignKey(LeaveType, on_delete=models.CASCADE)
    
    # use clean() method to validate fields (Learn concept from `https://stackoverflow.com/questions/12278753/clean-method-in-model-and-field-validation`)
    def clean(self):
        if self.start_date and self.end_date:
            if self.end_date < self.start_date:
                raise ValidationError({ 'end_date': 'End date must be after start date!' })

    # Calculate total days between start and end date
    def calculate_total_days(self):
        if self.start_date and self.end_date:
            return (self.end_date - self.start_date).days + 1
        return 0
    
    # Check if employee has sufficient balance and set warning message
    def check_balance_and_set_warning(self):
        try:
            balance = LeaveBalance.objects.get(employee=self.employee, leave_type=self.leave_type)
            can_request, message = balance.can_request_leave(self.total_days)
            
            if not can_request:
                self.warning_message = f"Warning: {message}"
                self.is_warning_displayed = True
            else:
                self.warning_message = ""
                self.is_warning_displayed = False
                
        except LeaveBalance.DoesNotExist:
            self.warning_message = "Warning: No leave balance record found for this leave type"
            self.is_warning_displayed = True
    
    # Update leave balance when request is approved
    def update_leave_balance(self):
        try:
            balance = LeaveBalance.objects.get(employee=self.employee, leave_type=self.leave_type)
            
            # Only deduct if we haven't already done so
            if not hasattr(self, '_balance_updated'):
                success = balance.reduce_days(self.total_days)
                if success:
                    self._balance_updated = True
                    # Clear warning if balance was successfully updated
                    self.warning_message = ""
                    self.is_warning_displayed = False
                    
        except LeaveBalance.DoesNotExist:
            # Create new balance record if it doesn't exist
            balance = LeaveBalance.objects.create(
                employee=self.employee,
                leave_type=self.leave_type,
                total_days=self.leave_type.max_days_allowed,
                used_days=self.total_days
            )
            self._balance_updated = True

    # save Computed Field `total_days` automatically
    def save(self, *args, **kwargs):
        # 1. Calculate total days automatically
        self.total_days = self.calculate_total_days()
        
        # 2. Check balance and set warnings for pending or approved requests
        if self.status in ['pending', 'approved']:
            self.check_balance_and_set_warning()
        
        # Call super save first to ensure we have an ID
        super().save(*args, **kwargs)
        
        # Update balance only after saving and only if approved
        if self.status == 'approved':
            self.update_leave_balance()

    def __str__(self):
        return f"LeaveRequest: {self.employee.user.first_name} - {self.leave_type.get_type_display()} - start:{self.start_date} end:{self.end_date} ({self.total_days} days)"

    class Meta:
        # order leave requests by newest created date
        ordering = ['-created_at']

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

    
    def save(self, *args, **kwargs):
        # Automatically update leave request status when history is created
        super().save(*args, **kwargs)
        
        # Update the leave request status to match the latest history action
        self.leave_request.status = self.action_type
        self.leave_request.save()
    
    def __str__(self):
        return f"LeaveHistory: the user {self.leave_request.employee.user.username} update request {self.leave_request.id} - {self.leave_request.leave_type.get_type_display()} - {self.get_action_type_display()}, Employee: {self.leave_request.employee.user.first_name}"