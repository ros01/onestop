from django.contrib import admin

from .models import Request
from store.models import *


# class RequisitionItemInline(admin.TabularInline):
#   model = RequisitionItem

# class RequisitionAdmin(admin.ModelAdmin):
#   inlines = [
#     RequisitionItemInline
#   ]
#   list_display = ('id', 'requisition_no', 'employee', 'department', 'requisition_status')
#   class Meta:
#     model = Requisition


# admin.site.register(Requisition, RequisitionAdmin)

class RequisitionItemAdmin(admin.ModelAdmin):
  list_display = ('requisition', 'item', 'quantity')
  list_display_links = ('requisition', 'item')
  list_filter = ('requisition', 'item')
  search_fields = ('requisition', 'item', 'quantity')
  list_per_page = 25


#admin.site.register(RequisitionItem, RequisitionItemAdmin)

class RequisitionAdmin(admin.ModelAdmin):
  list_display = ('id', 'requisition_no', 'employee', 'department', 'hod', 'requisition_status')
  list_display_links = ('id', 'requisition_no', 'department')
  list_filter = ('id', 'requisition_no', 'department')
  search_fields = ('id', 'requisition_no', 'employee', 'department')
  list_per_page = 25


#admin.site.register(Requisition, RequisitionAdmin)


class RequestAdmin(admin.ModelAdmin):
  list_display = ('request_no', 'vehicle_name', 'request_reason', 'requesting_staff', 'department', 'request_status')
  list_display_links = ('request_no', 'vehicle_name', 'department')
  list_filter = ('request_no', 'department')
  search_fields = ('request_no', 'vehicle_name', 'request_reason', 'requesting_staff', 'department')
  list_per_page = 25


admin.site.register(Request, RequestAdmin)
