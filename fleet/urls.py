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
    

)


app_name = 'fleet'

urlpatterns = [
	path('dashboard', DashboardTemplateView.as_view(), name='fleet_dashboard'),
    path('create_workshop/', WorkshopCreateView.as_view(), name='create_workshop'),
    path('create_station/', StationCreateView.as_view(), name='create_station'),
    path('create_category/', CategoryCreateView.as_view(), name='create_category'),
    path('create_vehicle/', VehicleCreateView.as_view(), name='create_vehicle'),
    path('workshop_list/', WorkshopListView.as_view(), name='workshop_list'),
    path('station_list/', StationListView.as_view(), name='station_list'),
    path('category_list/', CategoryListView.as_view(), name='category_list'),
    path('vehicle_list/', VehicleListView.as_view(), name='vehicle_list'),
    path('<uuid:pk>/workshop_detail/', WorkshopDetailView.as_view(), name='workshop_detail'),
    path('<uuid:pk>/station_detail/', StationDetailView.as_view(), name='station_detail'),
    path('<uuid:pk>/category_detail/', CategoryDetailView.as_view(), name='category_detail'),
    path('<uuid:pk>/vehicle_detail/', VehicleDetailView.as_view(), name='vehicle_detail'),
    path('<uuid:pk>/workshop_update/', WorkshopUpdateView.as_view(), name='workshop_update'),
    path('<uuid:pk>/station_update/', StationUpdateView.as_view(), name='station_update'),
    path('<uuid:pk>/category_update/', CategoryUpdateView.as_view(), name='category_update'),
    path('<uuid:pk>/vehicle_update/', VehicleUpdateView.as_view(), name='vehicle_update'),
    path('<uuid:id>/workshop_delete/', WorkshopDeleteView.as_view(), name='workshop_delete'),
    path('<uuid:id>/station_delete/', StationDeleteView.as_view(), name='station_delete'),
    path('<uuid:id>/category_delete/', CategoryDeleteView.as_view(), name='category_delete'),
    path('<uuid:id>/vehicle_delete/', VehicleDeleteView.as_view(), name='vehicle_delete'),
    path('request_list/', VehicleRequestList.as_view(), name='vehicle_request_list'),
    path('<uuid:id>/request_detail/', VehicleRequestDetail.as_view(), name='vehicle_request_detail'),
    path('<uuid:id>/vehicle_request', IssueVehicleRequest.as_view(), name='issue_vehicle_request'),
    path('<uuid:id>/update_assignment/', UpdateVehicleAssignemt.as_view(), name='update_vehicle_assignment'),
    path('allocations_list/', VehicleAssignmentList.as_view(), name='vehicles_allocations_list'),
    path('<uuid:pk>/allocations_detail/', VehicleAllocationsDetail.as_view(), name='vehicles_allocations_detail'),
	
    
    ]