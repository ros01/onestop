from django.contrib import admin

from .models import Leave, Specify, Document, Training, Record, Appraisal, Schedule, Performance


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