from django.urls import path
from . import views
from .views import (
    DashboardTemplateView,
    RequisitionCreateView,
    RequisitionDetailView,
    RequisitionUpdateView,
    RequisitionsListView,
    RequisitionDeleteView,
    ProfileTemplateView,
    TableTemplateView,
)


app_name = 'rrbnstaff'

urlpatterns = [
	path('dashboard/', DashboardTemplateView.as_view(), name='staff_dashboard'),
	path('profile/', ProfileTemplateView.as_view(), name='edit_profile'),
	path('tables/', TableTemplateView.as_view(), name='table_list'),
	path('requisition_list/', RequisitionsListView.as_view(), name='requisition_list'),
	path('create_requisition/', RequisitionCreateView.as_view(), name='create_requisition'),
	path('<uuid:id>/requisition_detail/', RequisitionDetailView.as_view(), name='requisition_detail'),
	path('<uuid:pk>/requisition_update/', RequisitionUpdateView.as_view(), name='requisition_update'),
	path('<uuid:id>/requisition_delete/', RequisitionDeleteView.as_view(), name='requisition_delete'),
	
    
    ]