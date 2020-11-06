from django.contrib import admin

from .models import Category, Assign


class CategoryAdmin(admin.ModelAdmin):
  list_display = ('category_name', 'description', 'active', 'entered_by', 'date_created')
  list_display_links = ('category_name', 'description', 'date_created')
  list_filter = ('category_name', 'date_created')
  search_fields = ('category_name', 'description', 'active', 'entered_by', 'date_created')
  list_per_page = 25


admin.site.register(Category, CategoryAdmin)



class AssignAdmin(admin.ModelAdmin):
  list_display = ('request_no', 'vehicle', 'requesting_staff', 'department', 'start_date', 'end_date', 'assigned_by', 'approved_date')
  list_display_links = ('request_no', 'vehicle', 'start_date', 'end_date', 'assigned_by', 'approved_date')
  list_filter = ('request_no', 'start_date', 'end_date', 'assigned_by', 'approved_date')
  search_fields = ('request_no', 'vehicle', 'requesting_staff', 'department', 'start_date', 'end_date', 'assigned_by', 'approved_date')
  list_per_page = 25


admin.site.register(Assign, AssignAdmin)
