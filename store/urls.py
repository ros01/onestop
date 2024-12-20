from django.urls import path
from . import views
# from forms import ContactForm1, ContactForm2
from .forms import RequisitionsModelForm, RequisitionCartItemModelForm




from .views import (
    RequisitionWizard,
    DashboardTemplateView,
    RequestItem,
    ItemCountView,
    RequisitionCheckout,
    # CreateRequisition,
    CreateRequisitionItems,
    RequisitionUpdateView,
    RequisitionDeleteView,
    ItemCategoyListView,
    ItemsListView,
    ItemListView,
    ItemCreateView,
    InventoryItemCreateView,
    ItemDetailView,
    InventoryIntemDetailView,
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
    IssueInternalRequisition,
    IssueRequisitionUpdate,
    IssuedRequisitions,
    IssuedRequisitionsDetailView,
    RestockItem,
    ReceivedItemsList,
    ItemRestockDetails,

)


app_name = 'store'

urlpatterns = [
    # path('', DashboardTemplateView.as_view(), name='store_dashboard'),
    path('dashboard', views.store_dashboard, name='store_dashboard'),
    path('add_item', views.add_item, name="add_item"),
    path('request_item/', RequestItem.as_view(), name='create_item_requisition'),
    # path('dashboard', DashboardTemplateView.as_view(), name='store_dashboard'),
    path('create_requisitions/', RequisitionWizard.as_view(), name='create_requisitions'),
    path('retrieve_item', views.retrieve_item, name='retrieve_item'),
    path('find_item/', views.find_item, name='find_item'),
    path('search_inventory/', views.search_inventory, name='search_inventory'),
    path('cart/', views.cart, name="cart"),
    path('requisition_checkout/', views.requisition_checkout, name="requisition_checkout"),
    path('restock_cart/', views.restock_cart, name="restock_cart"),
    path('restock_checkout/', views.restock_checkout, name="restock_checkout"),
    path('finalize_restock/', views.finalize_restock, name="finalize_restock"),
    path('ajax/load-employees/', views.load_employees, name='ajax_load_employees'),
    path('ajax/load-users/', views.load_users, name='ajax_load_users'),
    path('requisition_list/', RequisitionListView.as_view(), name='requisition_list'), 
    path('<int:id>/requisition', IssueInternalRequisition.as_view(), name='issue_requisition'),
    path('<int:pk>/requisition_update/', RequisitionUpdateView.as_view(), name='requisition_update'),
    path('update_item/', views.updateItem, name="update_item"),
    path('update_cart/', views.updateRestockCart, name="update_cart"),   
    path('process_order/', views.processOrder, name="process_order"),
    path('create_item/', ItemCreateView.as_view(), name='create_item'),
    path('create_inventory_item/', InventoryItemCreateView.as_view(), name='create_inventory_item'),
    path('ajax/create_stock_code/', views.createStockCode, name="create_stock_code"),
    path('<int:pk>/requisition_details/', RequisitionDetailsView.as_view(), name='requisition_details'),
    path('<int:pk>/update_issue/', IssueRequisitionUpdate.as_view(), name='update_issued_requisition'),
    path('<int:pk>/issue_details/', IssuedRequisitionsDetailView.as_view(), name='issue_details'),
    path('item_list/', ItemListView.as_view(), name='item_list'),
    path('items_list/', ItemsListView.as_view(), name='items_list'),
    path('restock/', views.restock, name='restock'),
    path('<int:pk>/restock/', RestockItem.as_view(), name='restock_item'),
    path('restock_list/', ReceivedItemsList.as_view(), name='restock_list'), 
    path('<int:pk>/restock_details/', ItemRestockDetails.as_view(), name='restock_details'),
    path('<int:id>/create_srv/', views.create_srv, name='create_srv'),
    path('generate_inventory_report/', views.generate_inventory_report, name='generate_inventory_report'),
    path('requisition_items_create/', CreateRequisitionItems.as_view(), name='create_requisition_items'),
    path('request_item/count/', ItemCountView.as_view(), name='requsition_item_count'),
    path('requisition_checkout/', RequisitionCheckout.as_view(), name='requisition_checkout'),
    path('<int:id>/requisition_delete/', RequisitionDeleteView.as_view(), name='requisition_delete'),
    # path('<int:id>/create_requisition/', CreateRequisition.as_view(), name='create_requisition'),
    path('issue_list/', IssuedRequisitions.as_view(), name='issue_list'), 
	path('category_list/', ItemCategoyListView.as_view(), name='category_list'), 
	path('vendor_list/', VendorListView.as_view(), name='vendor_list'),
	path('create_item/', ItemCreateView.as_view(), name='create_item'),
	path('create_vendor/', VendorCreateView.as_view(), name='create_vendor'),
	path('create_category/', CategoryCreateView.as_view(), name='create_category'),
	path('<int:pk>/item_detail/', ItemDetailView.as_view(), name='item_detail'),
    path('<int:id>/inventory_item_details/', InventoryIntemDetailView.as_view(), name='inventory_item_details'),
    path('<int:id>/vendor_detail/', VendorDetailView.as_view(), name='vendor_detail'),
	path('<int:id>/category_detail/', CategoryDetailView.as_view(), name='category_detail'),
	path('<int:pk>/item_update/', ItemUpdateView.as_view(), name='item_update'),
	path('<int:pk>/category_update/', CategoryUpdateView.as_view(), name='category_update'),
	path('<int:pk>/vendor_update/', VendorUpdateView.as_view(), name='vendor_update'),
	path('<int:id>/item_delete/', ItemDeleteView.as_view(), name='item_delete'),
	path('<int:id>/category_delete/', CategoryDeleteView.as_view(), name='category_delete'),
	path('<int:id>/vendor_delete/', VendorDeleteView.as_view(), name='vendor_delete'),    
    ]


htmx_urlpatterns = [
    path('check_item/', views.check_item, name="check_item"),
    path('search-item/', views.search_item, name='search-item'),
    ]


urlpatterns += htmx_urlpatterns