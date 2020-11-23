from django.urls import path
from . import views
from .views import (
    DashboardTemplateView,
    WorkshopCreateView,
    StationCreateView,
    CategoryCreateView,
    VehicleCreateView,
    WorkshopListView,
    StationListView,
    CategoryListView,
    VehicleListView,
    VehicleRequestList,
    WorkshopDetailView,
    StationDetailView,
    CategoryDetailView,
    VehicleDetailView,
    VehicleRequestDetail,
    WorkshopUpdateView,
    StationUpdateView,
    CategoryUpdateView,
    VehicleUpdateView,
    WorkshopDeleteView,
    StationDeleteView,
    CategoryDeleteView,
    VehicleDeleteView,
    IssueVehicleRequest,
    UpdateVehicleAssignemt,
    VehicleAssignmentList,
    VehicleAllocationsDetail,
    FinalizeTrip,
    UpdateTripFinalization,
    TripHistoryList,
    TripHistory,
    FuelingRecordView,
    FuelingListView,
    FuelingDetailView,
    FuelingUpdateView,
    RepairsRecordView,
    RepairsListView,
    RepairsDetailView,
    RepairsUpdateView,
    ScheduleMaintenance,
    ScheduleListView,
    ScheduleDetailView,
    ScheduleUpdateView,
    RecordMaintenance, 
    UpdateMaintenance, 
    MaintenanceList,
    MaintenanceDetailView,
    RestockStationCredit,
    StationCreditRestockList,
    StationCreditRestockDetails,



)


app_name = 'fleet'

urlpatterns = [
	path('dashboard', DashboardTemplateView.as_view(), name='fleet_dashboard'),
    path('retrieve_station', views.retrieve_station, name='retrieve_station'),
    path('restock/', views.restock, name='restock'),
    path('<uuid:id>/restock/', RestockStationCredit.as_view(), name='restock_station_credit'),
    path('restock_list/', StationCreditRestockList.as_view(), name='restock_list'), 
    path('<uuid:pk>/restock_details/', StationCreditRestockDetails.as_view(), name='restock_details'),
    path('create_workshop/', WorkshopCreateView.as_view(), name='create_workshop'),
    path('create_station/', StationCreateView.as_view(), name='create_station'),
    path('create_category/', CategoryCreateView.as_view(), name='create_category'),
    path('create_vehicle/', VehicleCreateView.as_view(), name='create_vehicle'),
    path('workshop_list/', WorkshopListView.as_view(), name='workshop_list'),
    path('station_list/', StationListView.as_view(), name='station_list'),
    path('category_list/', CategoryListView.as_view(), name='category_list'),
    path('vehicle_list/', VehicleListView.as_view(), name='vehicle_list'),
    path('request_list/', VehicleRequestList.as_view(), name='vehicle_request_list'),
    path('fueling_list/', FuelingListView.as_view(), name='fueling_list'),
    path('allocations_list/', VehicleAssignmentList.as_view(), name='vehicles_allocations_list'),
    path('repairs_list/', RepairsListView.as_view(), name='repairs_list'),
    path('maintenance_list/', MaintenanceList.as_view(), name='maintenance_list'),
    path('schedule_list/', ScheduleListView.as_view(), name='schedule_list'),
    path('<uuid:pk>/workshop_detail/', WorkshopDetailView.as_view(), name='workshop_detail'),
    path('<uuid:pk>/station_detail/', StationDetailView.as_view(), name='station_detail'),
    path('<uuid:pk>/category_detail/', CategoryDetailView.as_view(), name='category_detail'),
    path('<uuid:id>/request_detail/', VehicleRequestDetail.as_view(), name='vehicle_request_detail'),
    path('<uuid:id>/allocations_detail/', VehicleAllocationsDetail.as_view(), name='vehicles_allocations_detail'),
    path('<uuid:id>/trip_history_details/', TripHistory.as_view(), name='trip_history_details'),
    path('<uuid:pk>/fueling_detail/', FuelingDetailView.as_view(), name='fueling_detail'),
    path('<uuid:pk>/vehicle_detail/', VehicleDetailView.as_view(), name='vehicle_detail'),
    path('<uuid:pk>/repairs_detail/', RepairsDetailView.as_view(), name='repairs_detail'),
    path('<uuid:pk>/schedule_details/', ScheduleDetailView.as_view(), name='schedule_details'),
    path('<uuid:pk>/maintenance_detail/', MaintenanceDetailView.as_view(), name='maintenance_detail'),
    path('<uuid:pk>/workshop_update/', WorkshopUpdateView.as_view(), name='workshop_update'),
    path('<uuid:pk>/station_update/', StationUpdateView.as_view(), name='station_update'),
    path('<uuid:pk>/category_update/', CategoryUpdateView.as_view(), name='category_update'),
    path('<uuid:pk>/vehicle_update/', VehicleUpdateView.as_view(), name='vehicle_update'),
    path('<uuid:pk>/fueling_update/', FuelingUpdateView.as_view(), name='fueling_update'),
    path('<uuid:pk>/repairs_update/', RepairsUpdateView.as_view(), name='repairs_update'),
    path('<uuid:id>/update_release_allocation/', UpdateTripFinalization.as_view(), name='update_trip_finalization'),
    path('<uuid:id>/workshop_delete/', WorkshopDeleteView.as_view(), name='workshop_delete'),
    path('<uuid:id>/station_delete/', StationDeleteView.as_view(), name='station_delete'),
    path('<uuid:id>/category_delete/', CategoryDeleteView.as_view(), name='category_delete'),
    path('<uuid:id>/vehicle_delete/', VehicleDeleteView.as_view(), name='vehicle_delete'),
    path('<uuid:id>/issue_request', IssueVehicleRequest.as_view(), name='issue_vehicle_request'),
    path('<uuid:id>/update_assignment/', UpdateVehicleAssignemt.as_view(), name='update_vehicle_assignment'),
    #path('<uuid:id>/request_detail/', VehicleRequestDetail.as_view(), name='vehicle_request_detail'),
    path('<uuid:id>/release_allocation', FinalizeTrip.as_view(), name='finalize_trip'),
    path('trip_history/', TripHistoryList.as_view(), name='trip_history'), 
    path('record_fueling/', FuelingRecordView.as_view(), name='record_fueling'), 
    path('record_repairs/', RepairsRecordView.as_view(), name='record_repairs'),
    path('create_schedule/', ScheduleMaintenance.as_view(), name='create_maintenance_schedule'),
    path('<uuid:pk>/schedule_update/', ScheduleUpdateView.as_view(), name='schedule_update'),
    path('<uuid:id>/manage_schedule', RecordMaintenance.as_view(), name='create_maintenance_record'),
    path('<uuid:id>/update_maintenance/', UpdateMaintenance.as_view(), name='update_maintenance'),
    
    
	
    
    ]