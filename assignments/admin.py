from django.contrib import admin
from assignments.models import *
# Register your models here.

admin.site.register(Assignment)
admin.site.register(AssignmentTopView)


admin.site.register(LabAssignment)
admin.site.register(LabAssignmentTopView)

