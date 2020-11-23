from django.shortcuts import get_object_or_404, render, redirect
from django.views import View
from django.views.generic import (
     CreateView,
     DetailView,
     ListView,
     UpdateView,
     DeleteView,
     TemplateView
)
from .models import Category, Item, Vendor, Issue, Restock
from rrbnstaff.models import Requisition

from .forms import ItemModelForm, CategoryModelForm, VendorModelForm, IssueRequisitionModelForm, RestockModelForm
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from bootstrap_modal_forms.generic import BSModalCreateView
from bootstrap_modal_forms.mixins import PassRequestMixin, CreateUpdateAjaxMixin
from django.urls import reverse, reverse_lazy
from django.contrib.auth.models import User
from django.conf import settings
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist

# Create your views here.


class DashboardTemplateView(TemplateView):
    template_name = "store/store_dashboard2.html"
    
    def get_context_data(self, *args, **kwargs):
        context = super(DashboardTemplateView, self).get_context_data(*args, **kwargs)
        #context["inspection"] = Schedule.objects.all()
        return context


class ItemCreateView(PassRequestMixin, SuccessMessageMixin, CreateView):
    template_name = 'store/create_item2.html'
    form_class = ItemModelForm
    success_message = 'Item created Successfully.'

    success_url = reverse_lazy('store:items_list')


def retrieve_item(request):
    return render(request, 'store/retrieve_item.html')


def restock(request):
    try:
        query = request.GET.get('q')
        object = 0

    except ValueError:
        query = None
        object = None
    try:
        object = Item.objects.get(
            Q(stock_code=query) | Q(item_name__icontains=query)
        )

    except ObjectDoesNotExist:
        messages.error(request, ('Stock Code or Item Name is Invalid.  Enter a Valid Stock Code or Item Name'))
        pass

    return render(request, 'store/results.html', {"object": object})


class ItemObjectMixin(object):
    model = Item
    def get_object(self):
        id = self.kwargs.get('id')
        obj = None
        if id is not None:
            obj = get_object_or_404(self.model, id=id)
        return obj 


class RestockItem(ItemObjectMixin, View):
    template_name = "store/restock_item.html"
    template_name1 = "store/restock_item_details.html"
    
    def get(self, request,  *args, **kwargs):
        context = {}
        obj = self.get_object()
        if obj is not None:
            form = RestockModelForm(instance=obj)
            context['object'] = obj
            context['form'] = form

        return render(request, self.template_name, context)



    def post(self, request,  *args, **kwargs):
        
        form = RestockModelForm(request.POST)
        if form.is_valid():
            if not self.request.is_ajax() or self.request.POST.get('asyncUpdate') == 'True':
                form.save(commit=False)
            else:
                form.save(commit=True)
            
        context = {}

        obj = self.get_object()
        if obj is not None:
            form = RestockModelForm(instance=obj)
            context['object'] = obj
            context['form'] = form
            context['restock'] = Restock.objects.filter (stock_code=obj.stock_code, restock_no= request.POST['restock_no'])

        return render(request, self.template_name1, context)


class ReceivedItemsList(ListView):
    template_name = "store/restock_list.html"
    context_object_name = 'object'

    def get_queryset(self):
        return Restock.objects.all()
        

    def get_context_data(self, **kwargs):
        obj = super(ReceivedItemsList, self).get_context_data(**kwargs)
        obj['restock_qs'] = Restock.objects.order_by('-received_on')
        return obj


class ItemRestockDetails(DetailView):
    template_name = "store/restock_details.html"
    model = Restock


class VendorListView(ListView):
    template_name = "store/vendors_list2.html"
    context_object_name = 'object'

    def get_queryset(self):
        return Vendor.objects.all()
        

    def get_context_data(self, **kwargs):
        obj = super(VendorListView, self).get_context_data(**kwargs)
        obj['vendor_qs'] = Vendor.objects.order_by('-date_created')
        return obj

class ItemCategoyListView(ListView):
    template_name = "store/items_category_list.html"
    context_object_name = 'object'

    def get_queryset(self):
        return Category.objects.all()
        

    def get_context_data(self, **kwargs):
        obj = super(ItemCategoyListView, self).get_context_data(**kwargs)
        obj['category_qs'] = Category.objects.order_by('-entry_date')
        return obj

class ItemsListView(ListView):
    template_name = "store/items_list2.html"
    context_object_name = 'object'

    def get_queryset(self):
        return Item.objects.all()
        

    def get_context_data(self, **kwargs):
        obj = super(ItemsListView, self).get_context_data(**kwargs)
        obj['items_qs'] = Item.objects.order_by('-entry_date')
        return obj

class RequisitionListView(ListView):
    template_name = "store/requisitions_list2.html"
    context_object_name = 'object'

    def get_queryset(self):
        return Requisition.objects.order_by('-requisition_date')
        

    def get_context_data(self, **kwargs):
        obj = super(RequisitionListView, self).get_context_data(**kwargs)
        obj['requisition_qs'] = Requisition.objects.filter(requisition_status=1)
        return obj


class RequisitionListView(ListView):
    template_name = "store/requisitions_list2.html"
    context_object_name = 'object'

    def get_queryset(self):
        return Requisition.objects.order_by('-requisition_date')
        

    def get_context_data(self, **kwargs):
        obj = super(RequisitionListView, self).get_context_data(**kwargs)
        obj['requisition_qs'] = Requisition.objects.filter(requisition_status=1)
        return obj


class IssuedRequisitions(ListView):
    template_name = "store/issued_requisitions.html"
    context_object_name = 'object'

    def get_queryset(self):
        return Issue.objects.all()
        

    def get_context_data(self, **kwargs):
        obj = super(IssuedRequisitions, self).get_context_data(**kwargs)
        obj['issued_requisitions_qs'] = Issue.objects.all()
        return obj


class VendorCreateView(PassRequestMixin, SuccessMessageMixin, CreateView):
    template_name = 'store/create_vendor2.html'
    form_class = VendorModelForm
    success_message = 'Vendor created Successfully.'

    success_url = reverse_lazy('store:vendor_list')

class CategoryCreateView(PassRequestMixin, SuccessMessageMixin, CreateView):
    template_name = 'store/create_category2.html'
    form_class = CategoryModelForm
    success_message = 'Category created Successfully.'

    success_url = reverse_lazy('store:category_list')



class VendorObjectMixin(object):
    model = Vendor
    def get_object(self):
        id = self.kwargs.get('id')
        obj = None
        if id is not None:
            obj = get_object_or_404(self.model, id=id)
        return obj 

class CategoryObjectMixin(object):
    model = Category
    def get_object(self):
        id = self.kwargs.get('id')
        obj = None
        if id is not None:
            obj = get_object_or_404(self.model, id=id)
        return obj 


   

class RequisitionObjectMixin(object):
    model = Requisition
    def get_object(self):
        id = self.kwargs.get('id')
        obj = None
        if id is not None:
            obj = get_object_or_404(self.model, id=id)
        return obj 

class IssueObjectMixin(object):
    model = Issue
    def get_object(self):
        id = self.kwargs.get('id')
        obj = None
        if id is not None:
            obj = get_object_or_404(self.model, id=id)
        return obj 

class IssueRequisition(RequisitionObjectMixin, PassRequestMixin, SuccessMessageMixin, CreateView):
    template_name = 'store/issue_requisition.html'
    template_name1 = 'store/issue_requisition_details2.html'
    def get(self, request,  *args, **kwargs):
        context = {}
        obj = self.get_object()
        if obj is not None:
            form = IssueRequisitionModelForm(instance=obj)
            context['object'] = obj
            context['form'] = form

        return render(request, self.template_name, context)


    def post(self, request,  *args, **kwargs):
        
        form = IssueRequisitionModelForm(request.POST)
        if form.is_valid():
            if not self.request.is_ajax() or self.request.POST.get('asyncUpdate') == 'True':
                form.save(commit=False)
            else:
                form.save(commit=True)
            
        context = {}

        obj = self.get_object()
        if obj is not None:
            form = IssueRequisitionModelForm(instance=obj)
            context['object'] = obj
            context['form'] = form
            context['issue'] = Issue.objects.filter (requisition_no=obj.requisition_no)

        return render(request, self.template_name1, context)


class ItemDetailView(DetailView):
    template_name = "store/item_detail2.html"
    model = Item



class IssuedRequisitionsDetailView(DetailView):
    template_name = "store/issued_requisitions_details.html"
    model = Issue



class VendorDetailView(VendorObjectMixin, View):
    template_name = "store/vendor_detail2.html"

    def get(self, request, id=None, *args, **kwargs):
        context = {'object': self.get_object()}
        return render(request, self.template_name, context)


class VendorUpdateView(PassRequestMixin, SuccessMessageMixin, UpdateView):
    model = Vendor
    template_name = 'store/vendor_update2.html'
    form_class = VendorModelForm
    success_message = 'Success: Vendor Details were updated.'
    success_url = reverse_lazy('store:vendor_list')



class VendorDeleteView(VendorObjectMixin, View):
    template_name = "store/vendor_delete2.html" # DetailView
    def get(self, request, id=None, *args, **kwargs):
        # GET method
        context = {}
        obj = self.get_object()
        if obj is not None:
            context['object'] = obj
        return render(request, self.template_name, context)

    def post(self, request, id=None,  *args, **kwargs):
        # POST method
        context = {}
        obj = self.get_object()
        if obj is not None:
            obj.delete()
            context['object'] = None
            return redirect('store:vendor_list')
        return render(request, self.template_name, context)


class ItemUpdateView(PassRequestMixin, SuccessMessageMixin, UpdateView):
    model = Item
    template_name = 'store/item_update2.html'
    form_class = ItemModelForm
    success_message = 'Success: Item details were updated.'
    success_url = reverse_lazy('store:items_list')



class ItemDeleteView(ItemObjectMixin, View):
    template_name = "store/item_delete2.html" # DetailView
    def get(self, request, id=None, *args, **kwargs):
        # GET method
        context = {}
        obj = self.get_object()
        if obj is not None:
            context['object'] = obj
        return render(request, self.template_name, context)

    def post(self, request, id=None,  *args, **kwargs):
        # POST method
        context = {}
        obj = self.get_object()
        if obj is not None:
            obj.delete()
            context['object'] = None
            return redirect('store:items_list')
        return render(request, self.template_name, context)


class CategoryDetailView(CategoryObjectMixin, View):
    template_name = "store/category_detail2.html"

    def get(self, request, id=None, *args, **kwargs):
        context = {'object': self.get_object()}
        return render(request, self.template_name, context)


class CategoryUpdateView(PassRequestMixin, SuccessMessageMixin, UpdateView):
    model = Category
    template_name = 'store/category_update2.html'
    form_class = CategoryModelForm
    success_message = 'Success: Category details were updated.'
    success_url = reverse_lazy('store:category_list')


class CategoryDeleteView(CategoryObjectMixin, View):
    template_name = "store/category_delete2.html" # DetailView
    def get(self, request, id=None, *args, **kwargs):
        # GET method
        context = {}
        obj = self.get_object()
        if obj is not None:
            context['object'] = obj
        return render(request, self.template_name, context)

    def post(self, request, id=None,  *args, **kwargs):
        # POST method
        context = {}
        obj = self.get_object()
        if obj is not None:
            obj.delete()
            context['object'] = None
            return redirect('store:category_list')
        return render(request, self.template_name, context)

class RequisitionDetailsView(RequisitionObjectMixin, View):
    template_name = "store/requisition_detail2.html" 
    def get(self, request, id=None, *args, **kwargs):
        context = {'object': self.get_object()}
        return render(request, self.template_name, context)



class IssueRequisitionDetail(IssueObjectMixin, View):
    template_name = "store/issue_requisition_details2.html"

    def get(self, request, id=None, *args, **kwargs):
        context = {'object': self.get_object()}
        return render(request, self.template_name, context)

 
class IssueRequisitionUpdate(IssueObjectMixin, View):
    template_name = "store/issue_requisition_update.html" 
    template_name1 = "store/issue_requisition_details2.html" 
    
    def get(self, request, id=None, *args, **kwargs):
        # GET method
        context = {}
        obj = self.get_object()
        if obj is not None:
            form = IssueRequisitionModelForm(instance=obj)
            context['object'] = obj
            context['form'] = form
        return render(request, self.template_name, context)

    def post(self, request, id=None,  *args, **kwargs):
        # POST method
        context = {}
        obj = self.get_object()
        if obj is not None:
            form = IssueRequisitionModelForm(request.POST or None, instance=obj)
            if form.is_valid():
                form.save()
            context['object'] = obj
            context['form'] = form
            context['issue'] = Issue.objects.filter (requisition_no=obj.requisition_no)
        messages.success(request, ('Requisition Update Successful'))
        return render(request, self.template_name1, context)
