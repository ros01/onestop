from django.contrib import admin

from .models import Department, Employee, Course, Leave, Specify, Document, Training, Record, Appraisal, Schedule, Performance, Discipline, Compliance, Title, Grade


class DepartmentAdmin(admin.ModelAdmin):
  list_display = ('id', 'name')
  list_display_links = ('id', 'name')
  list_filter = ('id', 'name')
  search_fields = ('id', 'name')
  list_per_page = 25


admin.site.register(Department, DepartmentAdmin)




class TitleAdmin(admin.ModelAdmin):
  list_display = ('id', 'job_title')
  list_display_links = ('id', 'job_title')
  list_filter = ('id', 'job_title')
  search_fields = ('id', 'job_title')
  list_per_page = 25


admin.site.register(Title, TitleAdmin)


class GradeAdmin(admin.ModelAdmin):
  list_display = ('id', 'pay_grade_code', 'pay_grade_name')
  list_display_links = ('id', 'pay_grade_code', 'pay_grade_name')
  list_filter = ('id', 'pay_grade_code', 'pay_grade_name')
  search_fields = ('id', 'pay_grade_code', 'pay_grade_name')
  list_per_page = 25


admin.site.register(Grade, GradeAdmin)

class EmployeeAdmin(admin.ModelAdmin):
  list_display = ('id','employee', 'dob', 'gender', 'department', 'designation')
  list_display_links = ('id','employee', 'dob', 'department', 'designation')
  list_filter = ('id','employee', 'department', 'designation')
  search_fields = ('id','employee', 'dob', 'gender', 'entered_by', 'department', 'designation')
  list_per_page = 25


admin.site.register(Employee, EmployeeAdmin)


class LeaveAdmin(admin.ModelAdmin):
  list_display = ('staff_name', 'leave_type', 'leave_status', 'leave_application_date')
  list_display_links = ('staff_name', 'leave_type', 'leave_application_date')
  list_filter = ('staff_name', 'leave_application_date')
  search_fields = ('staff_name', 'leave_type', 'leave_status', 'entered_by', 'leave_application_date')
  list_per_page = 25


admin.site.register(Leave, LeaveAdmin)


class SpecifyAdmin(admin.ModelAdmin):
  list_display = ('staff_name', 'leave_type', 'leave_status', 'leave_application_date')
  list_display_links = ('staff_name', 'leave_type', 'leave_application_date')
  list_filter = ('staff_name', 'leave_application_date')
  search_fields = ('staff_name', 'leave_type', 'leave_status', 'assigned_by', 'leave_application_date')
  list_per_page = 25


admin.site.register(Specify, SpecifyAdmin)

class DocumentAdmin(admin.ModelAdmin):
  list_display = ('staff_name', 'request_no', 'leave_type', 'leave_application_date', 'actual_start_date', 'actual_end_date')
  list_display_links = ('staff_name', 'request_no', 'leave_application_date', 'actual_start_date', 'actual_end_date')
  list_filter = ('staff_name', 'leave_application_date', 'actual_start_date', 'actual_end_date')
  search_fields = ('staff_name', 'request_no', 'leave_type', 'assigned_by', 'leave_application_date', 'actual_start_date', 'actual_end_date')
  list_per_page = 25


admin.site.register(Document, DocumentAdmin)


class CourseAdmin(admin.ModelAdmin):
  list_display = ('training_name', 'category', 'vendor', 'training_description', 'date_added')
  list_display_links = ('training_name', 'vendor', 'training_description', 'date_added')
  list_filter = ('vendor', 'training_description', 'date_added')
  search_fields = ('training_name', 'category', 'training_description', 'vendor', 'date_added')
  list_per_page = 25


admin.site.register(Course, CourseAdmin)


class TrainingAdmin(admin.ModelAdmin):
  list_display = ('training_name', 'category', 'vendor', 'projected_start_date', 'projected_end_date')
  list_display_links = ('training_name', 'vendor', 'projected_start_date', 'projected_end_date')
  list_filter = ('vendor', 'projected_start_date', 'projected_end_date')
  search_fields = ('training_name', 'category', 'projected_start_date', 'vendor', 'projected_end_date')
  list_per_page = 25


admin.site.register(Training, TrainingAdmin)



class RecordAdmin(admin.ModelAdmin):
  list_display = ('training_name', 'category', 'vendor', 'training_start_date', 'training_end_date')
  list_display_links = ('training_name', 'vendor', 'training_start_date', 'training_end_date')
  list_filter = ('vendor', 'training_start_date', 'training_end_date')
  search_fields = ('training_name', 'category', 'vendor', 'training_start_date', 'training_end_date')
  list_per_page = 25


admin.site.register(Record, RecordAdmin)



class AppraisalAdmin(admin.ModelAdmin):
  list_display = ('appraisal_name', 'description', 'added_on', 'added_by')
  list_display_links = ('appraisal_name', 'description', 'added_by')
  list_filter = ('appraisal_name', 'added_by')
  search_fields = ('appraisal_name', 'description', 'added_on', 'added_by')
  list_per_page = 25


admin.site.register(Appraisal, AppraisalAdmin)


class ScheduleAdmin(admin.ModelAdmin):
  list_display = ('staff_name', 'schedule_no', 'appraisal', 'appraisal_status', 'projected_start_date', 'projected_end_date')
  list_display_links = ('staff_name', 'schedule_no', 'appraisal_status', 'projected_start_date', 'projected_end_date')
  list_filter = ('staff_name', 'appraisal_status', 'projected_start_date', 'projected_end_date')
  search_fields = ('staff_name', 'schedule_no', 'appraisal_type', 'appraisal_status', 'projected_start_date', 'projected_end_date')
  list_per_page = 25


admin.site.register(Schedule, ScheduleAdmin)


class PerformanceAdmin(admin.ModelAdmin):
  list_display = ('staff_name', 'schedule_no', 'appraisal', 'appraisal_start_date', 'appraisal_end_date', 'comments')
  list_display_links = ('staff_name', 'schedule_no', 'appraisal_start_date', 'appraisal_end_date', 'comments')
  list_filter = ('staff_name', 'appraisal_start_date', 'appraisal_end_date', 'comments')
  search_fields = ('staff_name', 'schedule_no', 'appraisal_type', 'appraisal_start_date', 'appraisal_end_date', 'comments')
  list_per_page = 25


admin.site.register(Performance, PerformanceAdmin)



class DisciplineAdmin(admin.ModelAdmin):
  list_display = ('staff_name', 'case_no', 'case_name', 'case_description', 'case_status', 'due_date')
  list_display_links = ('staff_name', 'case_no', 'case_description', 'case_status', 'due_date')
  list_filter = ('staff_name', 'case_description', 'case_status', 'due_date')
  search_fields = ('staff_name', 'case_no', 'case_description', 'case_status', 'due_date')
  list_per_page = 25


admin.site.register(Discipline, DisciplineAdmin)

class ComplianceAdmin(admin.ModelAdmin):
  list_display = ('staff_name', 'case_no', 'case_name', 'case_description', 'case_status', 'due_date', 'completed_on')
  list_display_links = ('staff_name', 'case_no', 'case_description', 'case_status', 'due_date', 'completed_on')
  list_filter = ('staff_name', 'case_description', 'case_status', 'due_date', 'completed_on')
  search_fields = ('staff_name', 'case_no', 'case_description', 'case_status', 'due_date', 'completed_on')
  list_per_page = 25

admin.site.register(Compliance, ComplianceAdmin)




