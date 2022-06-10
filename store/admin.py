from django.contrib import admin

from .models import *



class VendorAdmin(admin.ModelAdmin):
  list_display = ('vendor_name', 'address', 'phone',
                  'email', 'description')
  list_display_links = ('vendor_name', 'address')
  list_filter = ('vendor_name',)
  search_fields = ('vendor_name', 'address', 'phone',
                   'email', ' description')
  list_per_page = 25


admin.site.register(Vendor, VendorAdmin)


class ItemAdmin(admin.ModelAdmin):
  list_display = ('item_name', 'item_description', 'category', 'id',
                  'stock_code', 'vendor', 'quantity', 're_order_no',)
  list_display_links = ('item_name', 'item_description', 're_order_no')
  list_filter = ('item_name', 'stock_code', 're_order_no')
  search_fields = ('item_name', 'item_description', 'category',
                   'stock_code', 'vendor', 're_order_no')
  list_per_page = 25


admin.site.register(Item, ItemAdmin)

class CategoryAdmin(admin.ModelAdmin):
  list_display = ('id', 'category_name', 'description', 'active',
                  'entry_date')
  list_display_links = ('category_name', 'description')
  list_filter = ('category_name', 'entry_date', 'description')
  search_fields = ('category_name', 'description', 'active',
                   'entry_date')
  list_per_page = 25

admin.site.register(Category, CategoryAdmin)

# class RequisitionItemInline(admin.TabularInline):
#   model = RequisitionItem

# class IssueAdmin(admin.ModelAdmin):
#   inlines = [
#     RequisitionItemInline
#   ]
#   list_display = ('id', 'requisition', 'issued_by', 'issue_date')
#   class Meta:
#     model = Issue

class RequisitionAdmin(admin.ModelAdmin):
  list_display = ('id', 'employee', 'requisition_cart', 'requisition_reason', 'hod', 'department', 'requisition_status')
  list_display_links = ('id', 'requisition_cart', 'department')
  list_filter = ('id', 'requisition_cart','department')
  search_fields = ('id', 'employee', 'requisition_cart', 'hod', 'department')
  list_per_page = 25

admin.site.register(Requisition, RequisitionAdmin)


# class RequisitionAdmin(admin.ModelAdmin):
#   list_display = ('requisition_no', 'employee', 'requisition_reason')
#   list_display_links = ('requisition_no', 'remployee', 'requisition_reason')
#   list_filter = ('requisition_no', 'employee', 'requisition_reason')
#   search_fields = ('requisition_no', 'employee', 'requisition_reason')
#   list_per_page = 25


# admin.site.register(Requisition, RequisitionAdmin)

class RequisitionCartItemAdmin(admin.ModelAdmin):
  list_display = ('item', 'requisition_cart', 'quantity', 'quantity_issued')
  list_display_links = ('item', 'requisition_cart', 'quantity', 'quantity_issued')
  list_filter = ('item', 'requisition_cart', 'quantity', 'quantity_issued')
  search_fields = ('item', 'requisition_cart', 'quantity', 'quantity_issued')
  list_per_page = 25
  raw_id_fields = ['item']


admin.site.register(RequisitionCartItem, RequisitionCartItemAdmin)



class RequisitionCartAdmin(admin.ModelAdmin):
  list_display = ('requisition_no', 'employee', 'requisition_status')
  list_display_links = ('requisition_no', 'employee', 'requisition_status')
  list_filter = ('requisition_no', 'employee', 'requisition_status')
  search_fields = ('requisition_no', 'employee', 'requisition_status')
  list_per_page = 25


admin.site.register(RequisitionCart, RequisitionCartAdmin)


class IssueRequisitionAdmin(admin.ModelAdmin):
  list_display = ('requisition', 'issued_by', 'issue_date')
  list_display_links = ('requisition', 'issue_date')
  list_filter = ('requisition', 'issued_by', 'issue_date')
  search_fields = ('requisition', 'issued_by', 'issue_date')
  list_per_page = 25


admin.site.register(IssueRequisition, IssueRequisitionAdmin)


class RestockCartAdmin(admin.ModelAdmin):
  list_display = ('id', 'restock_no', 'staff_name', 'date')
  list_display_links = ('id', 'restock_no', 'staff_name', 'date')
  list_filter = ('id', 'restock_no', 'staff_name', 'date')
  search_fields = ('id', 'restock_no', 'staff_name', 'date')
  list_per_page = 25


admin.site.register(RestockCart, RestockCartAdmin)

class RestockCartItemAdmin(admin.ModelAdmin):
  list_display = ('id', 'item_name', 'restock_cart', 'vendor', 'quantity_ordered', 'quantity_received')
  list_display_links = ('id', 'item_name', 'restock_cart', 'vendor', 'quantity_ordered','quantity_received')
  list_filter = ('id', 'item_name', 'restock_cart', 'vendor', 'quantity_ordered', 'quantity_received')
  search_fields = ('id', 'item_name', 'restock_cart', 'vendor', 'quantity_ordered', 'quantity_received')
  list_per_page = 25
  


admin.site.register(RestockCartItem, RestockCartItemAdmin)


# class RestockAdmin(admin.ModelAdmin):
#   list_display = ('id', 'restock_cart', 'restock_date')
#   list_display_links = ('id', 'restock_cart', 'restock_date')
#   list_filter = ('id', 'restock_cart', 'restock_date')
#   search_fields = ('id', 'restock_cart', 'restock_date')
#   list_per_page = 25


# admin.site.register(Restock, RestockAdmin)


# class RestockAdmin(admin.ModelAdmin):
#   list_display = ('restock_no', 'item_name', 'stock_code', 'vendor', 'quantity_ordered',
#                   'unit_price', 'quantity_received', 'received_on')
#   list_display_links = ('restock_no', 'item_name', 'stock_code', 'vendor', 'quantity_received')
#   list_filter = ('restock_no', 'item_name', 'unit_price', 'vendor', 'quantity_received')
#   search_fields = ('restock_no', 'item_name', 'vendor', 'quantity_ordered',
#                    'unit_price', 'quantity_received')
#   list_per_page = 25


# admin.site.register(Restock, RestockAdmin)