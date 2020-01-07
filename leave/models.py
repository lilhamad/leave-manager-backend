from django.db import models
from datetime import date, timedelta
from employee.models import Employee

class Leave(models.Model):
    PENDING, APPROVED, RUNNING, RETURNED, CANCELLED, REJECTED = range(6)
    STATUS = (
        (PENDING, 'Pending'),
        (APPROVED, 'Approved'),
        (RUNNING, 'Running'),
        (RETURNED, 'Returned'),
        (CANCELLED, 'Cancelled'),
        (REJECTED, 'Rejected'),
    )

    
    start_date = models.DateField()
    end_date = models.DateField()
    employee = models.ForeignKey(Employee, related_name='employee_leaves', on_delete=models.CASCADE)
    status = models.PositiveIntegerField(choices=STATUS, default=PENDING)
    application_date = models.DateField(default=date.today, editable=False)

    class Meta:
        verbose_name  = 'Leave'
        verbose_name_plural = 'Leaves'
        ordering = ('-start_date',)