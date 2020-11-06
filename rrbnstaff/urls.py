from django.urls import path
from . import views
from .views import (
    DashboardTemplateView,
    RequisitionCreateView,
    CreateVehicleRequest,
    RequisitionDetailView,
    RequisitionUpdateView,
    VehicleRequestUpdateView,
    VehicleRequestDetailView,
    RequisitionsListView,
    RequestListView,
    RequisitionDeleteView,
    VehicleRequestDeleteView,
    ProfileTemplateView,
    TableTemplateView,
    MyIssuedRequisitions,
    MyIssuedRequisitionsDetails,
    MyVehicleAllocations,
    AssignedVehicleDetails,
)


app_name = 'rrbnstaff'

urlpatterns = [
	path('dashboard/', DashboardTemplateView.as_view(), name='staff_dashboard'),
	path('profile/', ProfileTemplateView.as_view(), name='edit_profile'),
	path('tables/', TableTemplateView.as_view(), name='table_list'),
	path('requisition_list/', RequisitionsListView.as_view(), name='requisition_list'),
	path('request_list/', RequestListView.as_view(), name='request_list'),
	path('my_issued_requisitions/', MyIssuedRequisitions.as_view(), name='my_issued_requisitions'),
	path('my_vehicles_allocations_list/', MyVehicleAllocations.as_view(), name='my_vehicles_allocations_list'),
	path('<uuid:pk>/issued_requisitions_details/', MyIssuedRequisitionsDetails.as_view(), name='issued_requisitions_details'),
	path('create_requisition/', RequisitionCreateView.as_view(), name='create_requisition'),
	path('<uuid:id>/requisition_detail/', RequisitionDetailView.as_view(), name='requisition_detail'),
	path('<uuid:pk>/requisition_update/', RequisitionUpdateView.as_view(), name='requisition_update'),
	path('<uuid:id>/requisition_delete/', RequisitionDeleteView.as_view(), name='requisition_delete'),
	path('create_vehicle_request/', CreateVehicleRequest.as_view(), name='create_vehicle_request'),
	path('<uuid:pk>/vehicle_request_detail/', VehicleRequestDetailView.as_view(), name='vehicle_request_detail'),
	path('<uuid:pk>/vehicle_request_update/', VehicleRequestUpdateView.as_view(), name='vehicle_request_update'),
	path('<uuid:id>/vehicle_request_delete/', VehicleRequestDeleteView.as_view(), name='vehicle_request_delete'),
	path('<uuid:pk>/assigned_vehicle_details/', AssignedVehicleDetails.as_view(), name='assigned_vehicle_details'),
	
    
    ]