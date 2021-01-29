from django.contrib import admin

from .models import Category, Station, Fueling, Assign, Release, Schedule, Maintenance, Vehicle


class CategoryAdmin(admin.ModelAdmin):
  list_display = ('category_name', 'description', 'active', 'entered_by', 'date_created')
  list_display_links = ('category_name', 'description', 'date_created')
  list_filter = ('category_name', 'date_created')
  search_fields = ('category_name', 'description', 'active', 'entered_by', 'date_created')
  list_per_page = 25


admin.site.register(Category, CategoryAdmin)



class VehicleAdmin(admin.ModelAdmin):
  list_display = ('vehicle_name', 'vehicle_type', 'location', 'department_assigned', 'date_created')
  list_display_links = ('vehicle_name', 'vehicle_type', 'date_created')
  list_filter = ('vehicle_name', 'date_created')
  search_fields = ('vehicle_name', 'vehicle_type', 'location', 'department_assigned', 'date_created')
  list_per_page = 25


admin.site.register(Vehicle, VehicleAdmin)

class StationAdmin(admin.ModelAdmin):
  list_display = ('station_name', 'contact_name', 'address', 'phone', 'email', 'entered_by', 'date_created')
  list_display_links = ('station_name', 'contact_name', 'phone', 'email','date_created')
  list_filter = ('station_name', 'phone', 'email', 'date_created')
  search_fields = ('station_name', 'contact_name', 'active', 'address', 'phone', 'email', 'date_created')
  list_per_page = 25


admin.site.register(Station, StationAdmin)

class FuelingAdmin(admin.ModelAdmin):
  list_display = ('vehicle', 'driver', 'fuel_input', 'fuel_cost', 'station', 'authorised_by', 'fueling_date')
  list_display_links = ('vehicle', 'driver', 'fuel_cost', 'station','fueling_date')
  list_filter = ('vehicle', 'fuel_cost', 'station', 'fueling_date')
  search_fields = ('vehicle', 'driver', 'active', 'fuel_input', 'fuel_cost', 'station', 'fueling_date')
  list_per_page = 25


admin.site.register(Fueling, FuelingAdmin)



class AssignAdmin(admin.ModelAdmin):
  list_display = ('request_no', 'vehicle_name', 'requesting_staff', 'department', 'approved_start_date', 'approved_end_date', 'assigned_by', 'approved_date', 'trip_status')
  list_display_links = ('request_no', 'vehicle_name', 'approved_start_date', 'approved_end_date', 'assigned_by', 'approved_date')
  list_filter = ('request_no', 'approved_start_date', 'approved_end_date', 'assigned_by', 'approved_date')
  search_fields = ('request_no', 'vehicle_name', 'requesting_staff', 'department', 'approved_start_date', 'approved_end_date', 'assigned_by', 'approved_date')
  list_per_page = 25


admin.site.register(Assign, AssignAdmin)



class ReleaseAdmin(admin.ModelAdmin):
  list_display = ('request_no', 'vehicle_name', 'requesting_staff', 'department', 'actual_trip_start_date', 'actual_trip_end_date', 'released_by', 'trip_start_mileage', 'trip_end_mileage')
  list_display_links = ('request_no', 'vehicle_name', 'actual_trip_start_date', 'actual_trip_end_date', 'released_by', 'trip_start_mileage')
  list_filter = ('request_no', 'actual_trip_start_date', 'actual_trip_end_date', 'released_by', 'trip_start_mileage')
  search_fields = ('request_no', 'vehicle_name', 'requesting_staff', 'department', 'actual_trip_start_date', 'actual_trip_end_date', 'released_by', 'trip_start_mileage')
  list_per_page = 25


admin.site.register(Release, ReleaseAdmin)

class ScheduleAdmin(admin.ModelAdmin):
  list_display = ('schedule_no', 'vehicle', 'target_maintenance_date', 'target_maintenance_mileage', 'maintenance_scheduled_by', 'scheduled_on')
  list_display_links = ('schedule_no', 'vehicle', 'target_maintenance_date', 'target_maintenance_mileage', 'maintenance_scheduled_by', 'scheduled_on')
  list_filter = ('schedule_no', 'target_maintenance_date', 'target_maintenance_mileage', 'maintenance_scheduled_by', 'scheduled_on')
  search_fields = ('schedule_no', 'vehicle', 'target_maintenance_date', 'target_maintenance_mileage', 'maintenance_scheduled_by', 'scheduled_on')
  list_per_page = 25


admin.site.register(Schedule, ScheduleAdmin)


class MaintenanceAdmin(admin.ModelAdmin):
  list_display = ('schedule_no', 'vehicle', 'target_maintenance_date', 'current_mileage', 'maintenance_cost', 'maintenance_recorded_by')
  list_display_links = ('schedule_no', 'vehicle', 'target_maintenance_date', 'current_mileage', 'maintenance_cost')
  list_filter = ('schedule_no', 'target_maintenance_date', 'current_mileage', 'maintenance_cost')
  search_fields = ('schedule_no', 'vehicle', 'target_maintenance_date', 'current_mileage', 'maintenance_cost')
  list_per_page = 25


admin.site.register(Maintenance, MaintenanceAdmin)
