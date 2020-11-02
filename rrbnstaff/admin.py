from django.contrib import admin

from .models import Requisition


class RequisitionAdmin(admin.ModelAdmin):
  list_display = ('requisition_no', 'item', 'quantity_requested', 'requesting_staff', 'department', 'requisition_status')
  list_display_links = ('requisition_no', 'item', 'department')
  list_filter = ('requisition_no', 'department')
  search_fields = ('requisition_no', 'item', 'quantity_requested', 'requesting_staff', 'department')
  list_per_page = 25


admin.site.register(Requisition, RequisitionAdmin)

