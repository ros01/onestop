from django.urls import path
from . import views
from .views import (
    DashboardTemplateView,
    ItemCategoyListView,
    ItemsListView,
    ItemCreateView,
    ItemDetailView,
    ItemUpdateView,
    ItemDeleteView,
    CategoryCreateView,
    CategoryDetailView,
    CategoryUpdateView,
    CategoryDeleteView,
    VendorListView,
    VendorCreateView,
    VendorDetailView,
    VendorUpdateView,
    VendorDeleteView,
    RequisitionListView,
    RequisitionDetailsView,
    IssueRequisition,
    IssueRequisitionUpdate,
    IssuedRequisitions,
    IssuedRequisitionsDetailView,

)


app_name = 'store'

urlpatterns = [
	path('dashboard', DashboardTemplateView.as_view(), name='store_dashboard'),
	path('category_list/', ItemCategoyListView.as_view(), name='category_list'), 
	path('items_list/', ItemsListView.as_view(), name='items_list'),
	path('vendor_list/', VendorListView.as_view(), name='vendor_list'),
    path('requisition_list/', RequisitionListView.as_view(), name='requisition_list'), 
    path('issued_requisitions_list/', IssuedRequisitions.as_view(), name='issued_requisitions_list'), 
    path('<uuid:id>/requisition_details/', RequisitionDetailsView.as_view(), name='requisition_details'),
	path('create_item/', ItemCreateView.as_view(), name='create_item'),
	path('create_vendor/', VendorCreateView.as_view(), name='create_vendor'),
	path('create_category/', CategoryCreateView.as_view(), name='create_category'),
	path('<uuid:pk>/item_detail/', ItemDetailView.as_view(), name='item_detail'),
    path('<uuid:pk>/issued_requisitions_detail/', IssuedRequisitionsDetailView.as_view(), name='issued_requisitions_detail'),
	path('<uuid:id>/vendor_detail/', VendorDetailView.as_view(), name='vendor_detail'),
	path('<uuid:id>/category_detail/', CategoryDetailView.as_view(), name='category_detail'),
	path('<uuid:pk>/item_update/', ItemUpdateView.as_view(), name='item_update'),
	path('<uuid:pk>/category_update/', CategoryUpdateView.as_view(), name='category_update'),
	path('<uuid:pk>/vendor_update/', VendorUpdateView.as_view(), name='vendor_update'),
	path('<uuid:id>/item_delete/', ItemDeleteView.as_view(), name='item_delete'),
	path('<uuid:id>/category_delete/', CategoryDeleteView.as_view(), name='category_delete'),
	path('<uuid:id>/vendor_delete/', VendorDeleteView.as_view(), name='vendor_delete'),
    path('<uuid:id>/issue_requisition', IssueRequisition.as_view(), name='issue_requisition'),
    path('<uuid:id>/update_requisition/', IssueRequisitionUpdate.as_view(), name='update_requisition'),
    
    ]