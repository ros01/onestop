from django.contrib import admin

from .models import Vendor, Item, Category, Issue, Restock


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
  list_display = ('item_name', 'item_description', 'category',
                  'stock_code', 'vendor', 'quantity', 're_order_no',)
  list_display_links = ('item_name', 'item_description', 're_order_no')
  list_filter = ('item_name', 'stock_code', 're_order_no')
  search_fields = ('item_name', 'item_description', 'category',
                   'stock_code', 'vendor', 're_order_no')
  list_per_page = 25


admin.site.register(Item, ItemAdmin)

class CategoryAdmin(admin.ModelAdmin):
  list_display = ('category_name', 'description', 'active',
                  'entry_date')
  list_display_links = ('category_name', 'description')
  list_filter = ('category_name', 'entry_date', 'description')
  search_fields = ('category_name', 'description', 'active',
                   'entry_date')
  list_per_page = 25



class IssueAdmin(admin.ModelAdmin):
  list_display = ('requisition_no', 'item', 'quantity_requested', 'quantity_issued', 'requesting_staff',
                  'issued_by', 'issue_date')
  list_display_links = ('requisition_no', 'item', 'quantity_requested', 'quantity_issued', 'issue_date')
  list_filter = ('requisition_no', 'item', 'issued_by', 'quantity_issued', 'issue_date')
  search_fields = ('requisition_no', 'item', 'quantity_issued', 'requesting_staff',
                   'issued_by', 'issue_date')
  list_per_page = 25


admin.site.register(Issue, IssueAdmin)


class RestockAdmin(admin.ModelAdmin):
  list_display = ('restock_no', 'item_name', 'stock_code', 'vendor', 'quantity_ordered',
                  'unit_price', 'quantity_received', 'received_on')
  list_display_links = ('restock_no', 'item_name', 'stock_code', 'vendor', 'quantity_received')
  list_filter = ('restock_no', 'item_name', 'unit_price', 'vendor', 'quantity_received')
  search_fields = ('restock_no', 'item_name', 'vendor', 'quantity_ordered',
                   'unit_price', 'quantity_received')
  list_per_page = 25


admin.site.register(Restock, RestockAdmin)