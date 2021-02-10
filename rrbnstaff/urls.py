from django.urls import path
from . import views
from .filters import VehicleFilter
from django_filters.views import FilterView
from .views import (
    DashboardTemplateView,
    ProfileTemplateView,
    TableTemplateView,
    FindVehicleView,
    RequisitionsListView,
    RequisitionCreateView,
    RequisitionDetailView,
    RequisitionUpdateView,
    RequisitionDeleteView,
    MyIssuedRequisitions,
    MyIssuedRequisitionsDetails,
    RequestListView,
    CreateVehicleRequest,
    VehicleRequestUpdateView,
    VehicleRequestDetailView,
    VehicleRequestDeleteView,
    MyVehicleAllocations,
    AssignedVehicleDetails,
    StaffProfileCreateView,
    MyProfileListView,
    MyProfileDetailView,
    MyProfileUpdateView,
    MyProfileDeleteView,
    MyLeaveRequestListView,
    LeaveRequestCreateView,
    LeaveRequestDetailView,
    LeaveRequestUpdateView,
    LeaveRequestDeleteView,
    MyApprovedLeaves,
    LeaveApprovalDetailView,
    MyAssignedLeaves,
    LeaveAssignmentDetailView,
    MyLeaveHistory,
    LeaveHistoryDetailView,
    MyScheduledTrainings,
    MyScheduledTrainingsDetails,
    MyPromotionInterviewListView,
    MyPromotionInterviewDetailView,
    MyPerformanceEvaluationListView,
    MyPerformanceEvaluationDetailView,
    ReprisalListView,
    ReprisalDetailView,
    RestitutionListView,
    RestitutionDetailView,
)


app_name = 'rrbnstaff'

urlpatterns = [
	path('dashboard/', DashboardTemplateView.as_view(), name='staff_dashboard'),
    path('retrieve_item', views.retrieve_item, name='retrieve_item'),
    path('find_item/', views.find_item, name='find_item'),
	path('profile/', ProfileTemplateView.as_view(), name='edit_profile'),
	path('tables/', TableTemplateView.as_view(), name='table_list'),
    path('find_vehicle', FindVehicleView, name='find_vehicle'),
	path('list_vehicles', views.list_vehicles, name='list_vehicles'),
    path('search_vehicles', views.search_vehicles, name='search_vehicles'),
    #path('request_vehicle/', RequestVehicle.as_view(), name='request_vehicle'),
	path('requisition_list/', RequisitionsListView.as_view(), name='requisition_list'),
    path('<uuid:id>/create_requisition/', RequisitionCreateView.as_view(), name='create_requisition'),
    path('<uuid:id>/requisition_detail/', RequisitionDetailView.as_view(), name='requisition_detail'),
    path('<uuid:pk>/requisition_update/', RequisitionUpdateView.as_view(), name='requisition_update'),
    path('<uuid:id>/requisition_delete/', RequisitionDeleteView.as_view(), name='requisition_delete'),
    path('my_issued_requisitions/', MyIssuedRequisitions.as_view(), name='my_issued_requisitions'),
    path('<uuid:pk>/issued_requisitions_details/', MyIssuedRequisitionsDetails.as_view(), name='issued_requisitions_details'),
	path('request_list/', RequestListView.as_view(), name='request_list'),
    path('<uuid:id>/create_vehicle_request', CreateVehicleRequest.as_view(), name='create_vehicle_request'),
    path('<uuid:pk>/vehicle_request_update/', VehicleRequestUpdateView.as_view(), name='vehicle_request_update'),
    path('<uuid:id>/vehicle_request_delete/', VehicleRequestDeleteView.as_view(), name='vehicle_request_delete'),
    path('<uuid:pk>/request_list_details/', VehicleRequestDetailView.as_view(), name='request_list_details'),
    path('my_vehicles_allocations_list/', MyVehicleAllocations.as_view(), name='my_vehicles_allocations_list'),
	path('<uuid:pk>/allocated_vehicle_details/', AssignedVehicleDetails.as_view(), name='allocated_vehicle_details'),
	#path('create_vehicle_request/', CreateVehicleRequest.as_view(), name='create_vehicle_request'),
	path('create_staff_profile/', StaffProfileCreateView.as_view(), name='create_staff_profile'),
    path('my_profile_list/', MyProfileListView.as_view(), name='my_profile_list'),
    path('<uuid:pk>/my_profile_detail/', MyProfileDetailView.as_view(), name='my_profile_detail'),
    path('<uuid:pk>/my_profile_update/', MyProfileUpdateView.as_view(), name='my_profile_update'),
    path('<uuid:id>/my_profile_delete/', MyProfileDeleteView.as_view(), name='my_profile_delete'),
    path('my_leave_requests_list/', MyLeaveRequestListView.as_view(), name='my_leave_requests_list'),
    path('create_leave_request/', LeaveRequestCreateView.as_view(), name='create_leave_request'),
    path('<uuid:pk>/leave_request_detail/', LeaveRequestDetailView.as_view(), name='leave_request_detail'),
    path('<uuid:pk>/leave_request_update/', LeaveRequestUpdateView.as_view(), name='leave_request_update'),
    path('<uuid:id>/leave_request_delete/', LeaveRequestDeleteView.as_view(), name='leave_request_delete'),
    path('my_approved_leaves/', MyApprovedLeaves.as_view(), name='my_approved_leaves'),
    path('<uuid:pk>/leave_approval_detail/', LeaveApprovalDetailView.as_view(), name='leave_approval_detail'),
    path('my_assigned_leaves/', MyAssignedLeaves.as_view(), name='my_assigned_leaves'),
    path('<uuid:pk>/leave_assignment_detail/', LeaveAssignmentDetailView.as_view(), name='leave_assignment_detail'),
    path('my_leave_history/', MyLeaveHistory.as_view(), name='my_leave_history'),
    path('<uuid:pk>/leave_history_detail/', LeaveHistoryDetailView.as_view(), name='leave_history_detail'),
    path('my_programs/', MyScheduledTrainings.as_view(), name='my_programs'),
    path('<uuid:pk>/program_details/', MyScheduledTrainingsDetails.as_view(), name='program_details'),
    path('my_promotion_interviews/', MyPromotionInterviewListView.as_view(), name='my_promotion_interviews'), 
    path('<uuid:pk>/my_promotion_interview_details/', MyPromotionInterviewDetailView.as_view(), name='my_promotion_interview_details'),
    path('evaluation_list/', MyPerformanceEvaluationListView.as_view(), name='evaluation_list'), 
    path('<uuid:pk>/evaluation_detail/', MyPerformanceEvaluationDetailView.as_view(), name='evaluation_detail'),
    path('reprisal_list/', ReprisalListView.as_view(), name='reprisal_list'), 
    path('<uuid:pk>/reprisal_detail/', ReprisalDetailView.as_view(), name='reprisal_detail'),
    path('restitution_list/', RestitutionListView.as_view(), name='restitution_list'), 
    path('<uuid:pk>/restitution_detail/', RestitutionDetailView.as_view(), name='restitution_detail'),
    
    
    ]