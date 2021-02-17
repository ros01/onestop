from django.urls import path
from . import views
from .views import (
    DashboardTemplateView,
    CategoryListView,
    CategoryCreateView,
    CategoryDetailView,
    CategoryUpdateView,
    CategoryDeleteView,
    VendorListView,
    VendorCreateView,
    VendorDetailView,
    VendorUpdateView,
    VendorDeleteView,
    ContractListView,
    ContractCreateView,
    ContractDetailView,
    ContractUpdateView,
    ContractDeleteView,
    ProjectListView,
    ProjectCreateView,
    ProjectDetailView,
    ProjectUpdateView,
    ProjectDeleteView,
    
   
)


app_name = 'procurement'

urlpatterns = [
	path('dashboard/', DashboardTemplateView.as_view(), name='procurement_dashboard'),
    path('add_category/', CategoryCreateView.as_view(), name='add_category'),
    path('category_list/', CategoryListView.as_view(), name='category_list'), 
    path('<uuid:pk>/category_detail/', CategoryDetailView.as_view(), name='category_detail'),
    path('<uuid:pk>/category_update/', CategoryUpdateView.as_view(), name='category_update'),
    path('<uuid:id>/category_delete/', CategoryDeleteView.as_view(), name='category_delete'),
    path('add_vendor/', VendorCreateView.as_view(), name='add_vendor'),
    path('vendor_list/', VendorListView.as_view(), name='vendor_list'),
    path('<uuid:pk>/vendor_detail/', VendorDetailView.as_view(), name='vendor_detail'),
    path('<uuid:pk>/vendor_update/', VendorUpdateView.as_view(), name='vendor_update'),
    path('<uuid:id>/vendor_delete/', VendorDeleteView.as_view(), name='vendor_delete'),
    path('add_contract/', ContractCreateView.as_view(), name='add_contract'),
    path('contract_list/', ContractListView.as_view(), name='contract_list'),
    path('<uuid:pk>/contract_detail/', ContractDetailView.as_view(), name='contract_detail'),
    path('<uuid:pk>/contract_update/', ContractUpdateView.as_view(), name='contract_update'),
    path('<uuid:id>/contract_delete/', ContractDeleteView.as_view(), name='contract_delete'),
    path('<uuid:id>/add_project/', ProjectCreateView.as_view(), name='add_project'),
    path('projects_list/', ProjectListView.as_view(), name='projects_list'),
    path('<uuid:pk>/project_detail/', ProjectDetailView.as_view(), name='project_detail'),
    path('<uuid:pk>/project_update/', ProjectUpdateView.as_view(), name='project_update'),
    path('<uuid:id>/project_delete/', ProjectDeleteView.as_view(), name='project_delete'),
    
    
    
    
	
    
    ]