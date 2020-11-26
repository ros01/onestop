from django.contrib import admin

from .models import Requisition, Request


class RequisitionAdmin(admin.ModelAdmin):
  list_display = ('requisition_no', 'item', 'quantity_requested', 'requesting_staff', 'department', 'requisition_status')
  list_display_links = ('requisition_no', 'item', 'department')
  list_filter = ('requisition_no', 'department')
  search_fields = ('requisition_no', 'item', 'quantity_requested', 'requesting_staff', 'department')
  list_per_page = 25


admin.site.register(Requisition, RequisitionAdmin)


class RequestAdmin(admin.ModelAdmin):
  list_display = ('request_no', 'vehicle_name', 'request_reason', 'requesting_staff', 'department', 'request_status')
  list_display_links = ('request_no', 'vehicle_name', 'department')
  list_filter = ('request_no', 'department')
  search_fields = ('request_no', 'vehicle_name', 'request_reason', 'requesting_staff', 'department')
  list_per_page = 25


admin.site.register(Request, RequestAdmin)