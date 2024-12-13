from django.urls import reverse, reverse_lazy
from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse, HttpResponseRedirect, Http404, JsonResponse, FileResponse
import json
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic.detail import SingleObjectMixin
from django.views.generic import (
     CreateView,
     DetailView,
     ListView,
     UpdateView,
     DeleteView,
     TemplateView
)
from .models import *
from hr.models import *
from rrbnstaff.models import Request
from .mixins import RequisitionObjectMixin, RequisitionsObjectMixin, RequisitionCartItemObjectMixin, IssueObjectMixin
from .forms import *
from django.forms import modelformset_factory
#from rrbnstaff.forms import RequisitionModelForm
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from bootstrap_modal_forms.generic import BSModalCreateView
from bootstrap_modal_forms.mixins import PassRequestMixin, CreateUpdateAjaxMixin
from django.urls import reverse, reverse_lazy
from django.contrib.auth.models import User
from django.conf import settings
from django.db.models import Q, Count, F, Value
from django.core.exceptions import ObjectDoesNotExist
import datetime
from django.contrib.auth import get_user_model
User = get_user_model()
from formtools.wizard.views import SessionWizardView
from .utils import cookieCart, cartData, restockcartData, guestOrder

import io
from django.http import FileResponse
from reportlab.pdfgen import canvas


from io import BytesIO
from reportlab.platypus import SimpleDocTemplate, Paragraph, PageBreak, BaseDocTemplate, PageTemplate, Frame, Spacer, Image, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm, inch
from reportlab.lib.pagesizes import letter, A4, inch, A5
from reportlab.lib.pagesizes import landscape, portrait
from reportlab.graphics.shapes import Drawing
from reportlab.graphics.charts.barcharts import VerticalBarChart
from reportlab.lib import colors
from reportlab.lib.utils import ImageReader
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT, TA_JUSTIFY
import random
import re


import time
from functools import partial



# Create your views here.

def is_valid_queryparam(param):
    return param != '' and param is not None

#@login_required
#def retrieve_item(request):
    #return render(request, 'store/retrieve_item.html')


@login_required
def retrieve_item(request):
    data = cartData(request)
    requisitionCartItems = data['requisitionCartItems']
    requisitionCart = data['requisitionCart']
    qs = Item.objects.all()
    item_name = request.GET.get('item_name')

    if is_valid_queryparam(item_name):
        qs = qs.filter(item_name__iexact=item_name)


    context = {
        'queryset': qs, 'requisitionCartItems':requisitionCartItems,
    }
    return render(request, 'store/retrieve_item2.html', context)


class LoginRequiredMixin(object):
    @classmethod
    def as_view(cls, **kwargs):
        view = super(LoginRequiredMixin, cls).as_view(**kwargs)
        return login_required(view)

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(LoginRequiredMixin, self).dispatch(request, *args, **kwargs)





class DashboardTemplateView(LoginRequiredMixin, TemplateView):
    template_name = "store/store_dashboard2.html"
        
    def get_context_data(self, *args, **kwargs):
        context = super(DashboardTemplateView, self).get_context_data(*args, **kwargs)
        this_month = (datetime.datetime.now() + datetime.timedelta(days=30))
        context['requ'] = Requisition.objects.all()
        context['iss'] = Issue.objects.all()
        context['ite'] = Item.objects.filter(re_order_no__gt=F('quantity'))
        context['res'] = Item.objects.filter(Q(quantity__lte=0))
        context['reqmnth'] = Requisition.objects.filter(requisition_creation_date__lt=this_month)
        context['issmnth'] = Issue.objects.filter(issue_date__lt=this_month)
        context['itemnth'] = Item.objects.filter(re_order_no__gt=F('quantity'), below_re_order_date__lt=this_month)
        context['resmnth'] = Item.objects.filter(Q(quantity__lte=0), below_re_order_date__lt=this_month)
       
        return context

@login_required
def store_dashboard(request):
    data = cartData(request)
    this_month = (datetime.datetime.now() + datetime.timedelta(days=30))

    requisitionCartItems = data['requisitionCartItems']
    requisitionCart = data['requisitionCart']
    items = data['items']
    products = Item.objects.all()
    requ =  Requisition.objects.all()
    iss =  IssueRequisition.objects.all()
    ite =  Item.objects.filter(re_order_no__gt=F('quantity'))
    res =  Item.objects.filter(Q(quantity__lte=0))
    reqmnth =  Requisition.objects.filter(requisition_creation_date__lt=this_month)
    issmnth =  IssueRequisition.objects.filter(issue_date__lt=this_month)
    itemnth =  Item.objects.filter(re_order_no__gt=F('quantity'), below_re_order_date__lt=this_month)
    resmnth =  Item.objects.filter(Q(quantity__lte=0), below_re_order_date__lt=this_month)
    context = {'products':products, 'requisitionCartItems':requisitionCartItems, 'requ':requ, 'iss':iss, 'ite':ite, 'res':res, 'reqmnth':reqmnth, 'issmnth':issmnth, 'itemnth':itemnth, 'resmnth':resmnth}
    return render(request, 'store/store_dashboard2.html', context)

def add_item(request):
    data = cartData(request)

    requisitionCartItems = data['requisitionCartItems']
    requisitionCart = data['requisitionCart']
    items = data['items']

    products = Item.objects.all()
    context = {'products':products, 'requisitionCartItems':requisitionCartItems}
    return render(request, 'store/store.html', context)

@login_required
def find_item(request):
    data = cartData(request)
    requisitionCartItems = data['requisitionCartItems']
    requisitionCart = data['requisitionCart']
    items = data['items']
    # inventory = Item.objects.all()
    qs = Item.objects.all()
    query = request.GET.get('q')
    if query is not None:
        qs = qs.filter(item_name__icontains=query)
    else:
        qs = Item.objects.all()[:3]
    context = {
        'queryset': qs, 'requisitionCartItems':requisitionCartItems, 'items':items, 'requisitionCart':requisitionCart,
    }
    return render(request, 'store/add_to_cart.html', context)


@login_required
def check_item(request):
    data = cartData(request)
    requisitionCartItems = data['requisitionCartItems']
    requisitionCart = data['requisitionCart']
    items = data['items']

    item_name = request.POST.get('item_name')

    products = Item.objects.all()
    context = {'products':products, 'requisitionCartItems':requisitionCartItems}
    return render(request, 'store/search.html', context)


@login_required
def search_item(request):
    data = cartData(request)
    requisitionCartItems = data['requisitionCartItems']
    requisitionCart = data['requisitionCart']
    items = data['items']
    search_text = request.POST.get('search')

    # look up all films that contain the text
    # exclude user films
    # userfilms = UserFilms.objects.filter(user=request.user)
    results = Item.objects.filter(item_name__icontains=search_text)
    context = {"results": results, 'requisitionCartItems':requisitionCartItems, 'items':items, 'requisitionCart':requisitionCart}
    return render(request, 'store/search_results.html', context)


@login_required
def search_inventory(request):
    data = restockcartData(request)
    restockCartItems = data['restockCartItems']
    restockCart = data['restockCart']
    # items = data['items']
    # inventory = Item.objects.all()
    qs = Item.objects.all()
    query = request.GET.get('q')
    if query is not None:
        qs = qs.filter(item_name__icontains=query)
    else:
        qs = Item.objects.all()[:3]
    context = {
        'queryset': qs, 'restockCartItems':restockCartItems, 'restockCart':restockCart,
    }
    return render(request, 'store/inventory_items.html', context)


@login_required
def cart(request):
    data = cartData(request)

    requisitionCartItems = data['requisitionCartItems']
    requisitionCart = data['requisitionCart']
    items = data['items']

    context = {'items':items, 'requisitionCart':requisitionCart, 'requisitionCartItems':requisitionCartItems}
    return render(request, 'store/requisition_cart.html', context)


def restock_cart(request):
    data = restockcartData(request)

    restockCartItems = data['restockCartItems']
    restockCart = data['restockCart']
    items = data['items']

    context = {'items':items, 'restockCart':restockCart, 'restockCartItems':restockCartItems}
    return render(request, 'store/restock_cart.html', context)


def requisition_checkout(request):
    data = cartData(request)
    form = RequisitionsModelForm(request.POST, request.FILES)
    
    requisitionCartItems = data['requisitionCartItems']
    requisitionCart = data['requisitionCart']
    items = data['items']

    context = {'items':items, 'requisitionCart':requisitionCart, 'requisitionCartItems':requisitionCartItems, 'form':form}
    return render(request, 'store/checkout.html', context)


def restock_checkout(request):
    data = restockcartData(request)
    restockCartItems = data['restockCartItems']
    restockCart = data['restockCart']
    items = data['items']

    context = {'items':items, 'restockCart':restockCart, 'restockCartItems':restockCartItems}
    return render(request, 'store/restock_checkout.html', context)


def finalize_restock(request):
   
    data = json.loads(request.body)

    if request.user.is_authenticated:
        
        staff_name = request.user
        restock_cart, created = RestockCart.objects.get_or_create(staff_name=staff_name, complete=False)
          
        restock_cart.complete = True
        restock_cart.save()

    
    return JsonResponse('Rstock Completed', safe=False)



def updateItem(request):
    data = json.loads(request.body)
    itemId = data['itemId']
    action = data['action']
    print('Action:', action)
    print('Item:', itemId)

    # employee = request.user.employee
    employee = request.user
    item = Item.objects.get(id=itemId)
    # requisition_cart, created = RequisitionCart.objects.get_or_create(employee=employee.employee, requisition_status=1)
    requisition_cart, created = RequisitionCart.objects.get_or_create(employee=employee, requisition_status=1)

    requisitionCartItem, created = RequisitionCartItem.objects.get_or_create(requisition_cart=requisition_cart, item=item)

    if action == 'add':
        requisitionCartItem.quantity = (requisitionCartItem.quantity + 1)
    elif action == 'remove':
        requisitionCartItem.quantity = (requisitionCartItem.quantity - 1)

    requisitionCartItem.save()

    if requisitionCartItem.quantity <= 0:
        requisitionCartItem.delete()

    return JsonResponse('Item was added', safe=False)



def updateRestockCart(request):
    data = json.loads(request.body)
    itemId = data['itemId']
    action = data['action']
    print('Action:', action)
    print('Item:', itemId)

    
    staff_name = request.user
    item_name = Item.objects.get(id=itemId)
    restock_cart, created = RestockCart.objects.get_or_create(staff_name=staff_name, complete=False)

    restockCartItem, created = RestockCartItem.objects.get_or_create(restock_cart=restock_cart, item_name=item_name)

    if action == 'add':
        restockCartItem.qty = (restockCartItem.qty + 1)
    elif action == 'remove':
        restockCartItem.qty = (restockCartItem.qty - 1)

    restockCartItem.save()

    if restockCartItem.qty <= 0:
        restockCartItem.delete()

    return JsonResponse('Item was added', safe=False)


class RestockItem(LoginRequiredMixin, PassRequestMixin, SuccessMessageMixin, UpdateView):
    model = RestockCartItem
    template_name = 'store/restock_cart_item.html'
    form_class = RestockCartModelForm
    success_message = 'Item Restock Successful'
    success_url = reverse_lazy('store:restock_cart')
     
    # def get_success_url(self):
    #     print (self.kwargs)
    #     return reverse("store:restock_cart", kwargs={"pk": self.object.pk})
    
    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['schedule_qs'] = Schedule.objects.select_related("hospital_name").filter(application_status=4, hospital_name=self.schedule.hospital_name)      
    #     return context

    # def get_initial(self):
    #     return {
    #         'restock_cart': self.kwargs["pk"],

    #     }


    
    def get_form_kwargs(self):
        self.restock_cart_items = RestockCartItem.objects.get(pk=self.kwargs['pk'])
        kwargs = super().get_form_kwargs()
        kwargs['initial']['item_name'] = self.restock_cart_items.item_name
        # kwargs['initial']['restock_cart'] = self.restock_cart_items.restock_cart
        kwargs['initial']['vendor'] = self.restock_cart_items.item_name.vendor
        kwargs['initial']['unit_price'] = self.restock_cart_items.item_name.unit_price
        return kwargs
    

    

    # def form_invalid(self, form):
    #     return self.render_to_response(self.get_context_data())


class ReceivedItemsList(LoginRequiredMixin, ListView):
    template_name = "store/restock_list.html"
    context_object_name = 'object'

    def get_queryset(self):
        return RestockCart.objects.all()
        

    def get_context_data(self, **kwargs):
        obj = super(ReceivedItemsList, self).get_context_data(**kwargs)
        obj['restock_qs'] = RestockCart.objects.order_by('date')
        return obj




class ItemCreateView(LoginRequiredMixin, PassRequestMixin, SuccessMessageMixin, CreateView):
    template_name = 'store/create_item2.html'
    form_class = ItemModelForm
    success_message = 'Item created Successfully.'
    success_url = reverse_lazy('store:items_list')

    # def get_context_data(self, *args, **kwargs):
    #     context = super(ItemCreateView, self).get_context_data(**kwargs)
    #     # obj = get_object_or_404(RequisitionCart,  requisition_no=self.get_requisition())
    #     # qs = RequisitionCart.objects.filter(requisition=self.get_requisition())
    #     # qs1 = obj.requisitioncartitem_set.all()
    #     # form = IssueRequisitionsModelForm(initial={'requisition':self.get_requisition()})

    #     obj = get_object_or_404(Item)

    #     data = cartData(self.request)
    #     requisitionCartItems = data['requisitionCartItems']
    #     context['requisitionCartItems'] = requisitionCartItems
    #     # context['form'] = form  
    #     context['obj'] = obj 

    #     # print(self.kwargs)
    #     # context['object'] = self.get_requisition()
    #     return context   



class InventoryItemCreateView(LoginRequiredMixin, CreateView):
    template_name = 'store/create_inventory_item.html'
    form_class = InventoryItemsModelForm
    success_message = 'Item created Successfully'
    
    
    def get_success_url(self):
        return reverse("store:item_detail", kwargs={"pk": self.object.pk})


class ItemObjectMixin(object):
    model = Item
    def get_object(self):
        id = self.kwargs.get('id')
        obj = None
        if id is not None:
            obj = get_object_or_404(self.model, id=id)
        return obj

class ItemDetailView(LoginRequiredMixin, DetailView):
    template_name = "store/item_detail2.html"
    model = Item

class InventoryIntemDetailView(LoginRequiredMixin, ItemObjectMixin, View):
    template_name = 'store/item_detail2.html' 

    def get(self, request, id=None, *args, **kwargs):
        context = {'object': self.get_object()}
        return render(request, self.template_name, context)


# def createStockCode1(request):
#     category = request.GET.get("category")
#     category = Category.objects.get(id=category)
#     category_short = category.category_short
  
#     last_stock_code = Item.objects.all().order_by('id').last()
#     if not last_stock_code:
#         stock_code = str(category_short) + '00001'
#     else:
#         stock_code = last_stock_code.stock_code
#         stock_code_int =  int (re.findall(r'\d+', stock_code)[0])
#         new_stock_code_int = stock_code_int + 1
#         new_stock_code = str(category_short) + str(new_stock_code_int).zfill(5)
#         stock_code = new_stock_code
    
#     print (stock_code)
#     return JsonResponse(stock_code, safe=False)

def createStockCode(request):
    category = request.GET.get("category")
    category = Category.objects.get(id=category)
    category_short = category.category_short

    last_stock_code = Item.objects.filter(category__category_short=category_short).order_by('id').last()
    if not last_stock_code:
        stock_code = str(category_short) + '00001'
    else:
        stock_code = last_stock_code.stock_code
        stock_code_int =  int (re.findall(r'\d+', stock_code)[0])
        new_stock_code_int = stock_code_int + 1
        new_stock_code = str(category_short) + str(new_stock_code_int).zfill(5)
        stock_code = new_stock_code
    
    print (stock_code)
    return JsonResponse(stock_code, safe=False)


  


def processOrder(request):
    # transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    if request.user.is_authenticated:
        # employee = request.user.employee
        employee = request.user
        requisition_cart, created = RequisitionCart.objects.get_or_create(employee=employee, requisition_status=1)
        # requisition_cart, created = RequisitionCart.objects.get_or_create(employee=employee.employee, requisition_status=1)
        #requisition_cart, created = RequisitionCart.objects.get_or_create(requisition_status=1)
    # else:
    #     employee, requisition_cart = guestOrder(request, data)

    # total = float(data['form']['total'])
    # requisition_cart.transaction_id = transaction_id

    # if total == requisition_cart.get_cart_total:   
        requisition_cart.requisition_status = 2
        requisition_cart.save()

    # if requisition_cart.requisition_status == 2:

    # if requisition_cart.shipping == True:
    #if requisition_cart.requisition_status == 2:
        Requisition.objects.create(
        # employee=Employee.objects.get(id=data['requisition']['employee']),
        employee=data['requisition']['employee'],
        requisition_cart=requisition_cart,
        requisition_reason=data['requisition']['requisition_reason'],
        # hod=Employee.objects.get(id=data['requisition']['hod']),
        hod=data['requisition']['hod'],
        #department=Department.objects.get(id=data['requisition']["department"]),
        department=data['requisition']['department'],
      
        )

    return JsonResponse('Payment submitted..', safe=False)

def load_employees(request):
    department_id = request.GET.get('department')
    employees = Employee.objects.filter(department_id=department_id)
    return render(request, 'store/employee_dropdown_list_options.html', {'employees': employees})


def load_users(request):
    department_id = request.GET.get('department')
    users = User.objects.filter(department_id=department_id)
    return render(request, 'store/user_dropdown_list_options.html', {'users': users})

class IssueInternalRequisition(RequisitionObjectMixin, SuccessMessageMixin, CreateView):
    template_name = 'store/issue_requisition2.html'
    form_class = IssueRequisitionsModelForm
    formset_class =IssueRequisitionItemFormSet
    success_message = 'Requisition issued successfully'
    success_url = reverse_lazy('store:issue_list') 

    def get_context_data(self, *args, **kwargs):
        context = super(IssueInternalRequisition, self).get_context_data(**kwargs)
        obj = get_object_or_404(RequisitionCart,  requisition_no=self.get_requisition())
        qs = RequisitionCart.objects.filter(requisition=self.get_requisition())
        qs1 = obj.requisitioncartitem_set.all()
        #formset =IssueRequisitionItemFormSet(queryset=qs, initial=[{'requisition':self.get_requisition()}]) 
        formset =IssueRequisitionItemFormSet(queryset=qs1) 
        form = IssueRequisitionsModelForm(initial={'requisition':self.get_requisition()})

        data = cartData(self.request)
        requisitionCartItems = data['requisitionCartItems']

        context['requisitionCartItems'] = requisitionCartItems
        context['requisition_formset'] = formset
        context['form'] = form  
        context['object'] = self.get_requisition()
        return context   

    def post(self, request, *args, **kwargs):
        self.object = self.get_requisition()
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        obj = get_object_or_404(RequisitionCart,  requisition_no=self.get_requisition())
        qs1 = obj.requisitioncartitem_set.all()
        formsets = IssueRequisitionItemFormSet(self.request.POST, queryset=qs1)

        if form.is_valid() and formsets.is_valid():
            formsets.save()   
            form.save()
        return super().post(request, *args, **kwargs)

class RequisitionListView(LoginRequiredMixin, ListView):
    template_name = "store/requisitions_list2.html"
    context_object_name = 'object'

    def get_queryset(self):
        return Requisition.objects.order_by('-requisition_creation_date')
        

    def get_context_data(self, **kwargs):
        obj = super(RequisitionListView, self).get_context_data(**kwargs)
        obj['requisition_qs'] = Requisition.objects.filter(requisition_status=1)
        data = cartData(self.request)
        requisitionCartItems = data['requisitionCartItems']

        obj['requisitionCartItems'] = requisitionCartItems
        return obj

# class RequisitionDetailsView(LoginRequiredMixin, RequisitionObjectMixin, View):
#     template_name = "store/requisition_detail2.html" 
#     def get(self, request, id=None, *args, **kwargs):
#         context = {'object': self.get_requisition()}
#         return render(request, self.template_name, context) 





class IssuedRequisitions(LoginRequiredMixin, ListView):
    template_name = "store/issued_requisitions.html"
    context_object_name = 'object'

    def get_queryset(self):
        return IssueRequisition.objects.all()
        

    def get_context_data(self, **kwargs):
        obj = super(IssuedRequisitions, self).get_context_data(**kwargs)
        obj['issued_requisitions_qs'] = IssueRequisition.objects.all()
        data = cartData(self.request)
        requisitionCartItems = data['requisitionCartItems']
        obj['requisitionCartItems'] = requisitionCartItems
        return obj

class IssuedRequisitionsDetailView(LoginRequiredMixin, DetailView):
    template_name = "store/issued_requisitions_details2.html"
    model = IssueRequisition

    def get_context_data(self, *args, **kwargs):
        context = super(IssuedRequisitionsDetailView, self).get_context_data(**kwargs)
        data = cartData(self.request)
        requisitionCartItems = data['requisitionCartItems']
        context['requisitionCartItems'] = requisitionCartItems
        return context  


class RequisitionUpdateView(UpdateView):
    model = Requisition
    form_class = RequisitionsUpdateModelForm
    formset_class = RequisitionItemFormSet
    template_name = 'store/requisition_update3.html'
    success_url = reverse_lazy('store:requisition_list')

    def get_context_data(self, *args, **kwargs):
        context = super(RequisitionUpdateView, self).get_context_data(**kwargs)
        qs = RequisitionCart.objects.filter(requisition=self.get_object())
        obj = get_object_or_404(RequisitionCart,  requisition_no=self.get_object())
        qs1 = obj.requisitioncartitem_set.all()
        formset =RequisitionItemFormSet(queryset=qs1) 
        data = cartData(self.request)
        requisitionCartItems = data['requisitionCartItems']
        context['requisitionCartItems'] = requisitionCartItems
        # formset = RequisitionItemFormSet(queryset=qs, initial=[{'requisition':self.get_object()}])
        context['requisition_formset'] = formset
        return context

    def get_initial(self):
        return {
            'requisition': self.kwargs["pk"],   
        }

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        qs = RequisitionCart.objects.filter(requisition=self.get_object())
        # qs = RequisitionItem.objects.filter(requisition=self.get_object())
        obj = get_object_or_404(RequisitionCart,  requisition_no=self.get_object())
        qs1 = obj.requisitioncartitem_set.all()
        # formsets = RequisitionItemFormSet(self.request.POST, queryset=qs, initial=[{'requisition':self.get_object()}])
        formsets = RequisitionItemFormSet(self.request.POST, queryset=qs1)

        if form.is_valid() and formsets.is_valid():
            form.save()
            formsets.save()
        return super().post(request, *args, **kwargs)
            # new_instances = formsets.save(commit=False)
            # for new_instance in new_instances:
            #     new_instance.requisition = self.get_object()
            #     new_instance.save()
        #     return self.form_valid(form)
        # else:
        #     return self.form_invalid(form)

class IssueRequisitionUpdate(LoginRequiredMixin, IssueObjectMixin, UpdateView):
    model = IssueRequisition
    template_name = 'store/issue_requisition_update2.html'
    form_class = IssueRequisitionsModelForm
    formset_class = IssueRequisitionItemFormSet
    success_message = 'Issued Requisition updated successfully'
    success_url = reverse_lazy('store:issue_list')

    def get_context_data(self, *args, **kwargs):
        context = super(IssueRequisitionUpdate, self).get_context_data(**kwargs)
        # qs = RequisitionCart.objects.filter(requisition=self.get_object())
        obj = get_object_or_404(RequisitionCart,  requisition_no=self.get_object())
        qs1 = obj.requisitioncartitem_set.all()
        formset =IssueRequisitionItemFormSet(queryset=qs1) 

        # qs = RequisitionCartItem.objects.filter(requisition_cart__issuerequisition=self.get_object())
        # formset = IssueRequisitionItemFormSet(queryset=qs)
        data = cartData(self.request)
        requisitionCartItems = data['requisitionCartItems']
        context['requisitionCartItems'] = requisitionCartItems
        context['requisition_formset'] = formset
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        # qs = RequisitionCartItem.objects.filter(requisition_cart__issuerequisition=self.get_object())
        obj = get_object_or_404(RequisitionCart,  requisition_no=self.get_object())
        qs1 = obj.requisitioncartitem_set.all()
        formsets = IssueRequisitionItemFormSet(self.request.POST, queryset=qs1)

        if form.is_valid() and formsets.is_valid():
            form.save()
            formsets.save()    
        
        return super().post(request, *args, **kwargs)


class VendorListView(LoginRequiredMixin, ListView):
    template_name = "store/vendors_list2.html"
    context_object_name = 'object'

    def get_queryset(self):
        return Vendor.objects.all()
        

    def get_context_data(self, **kwargs):
        obj = super(VendorListView, self).get_context_data(**kwargs)
        data = cartData(self.request)
        requisitionCartItems = data['requisitionCartItems']
        obj['requisitionCartItems'] = requisitionCartItems
        obj['vendor_qs'] = Vendor.objects.order_by('-date_created')
        return obj

# class IssueRequisitionUpdate(LoginRequiredMixin, IssueObjectMixin, UpdateView):
#     model = IssueRequisition
#     template_name = 'store/issue_requisition_update2.html'
#     form_class = IssueRequisitionsModelForm
#     formset_class = IssueRequisitionItemFormSet
#     success_message = 'Issued Requisition updated successfully'
#     success_url = reverse_lazy('store:issue_list')

#     def get_context_data(self, *args, **kwargs):
#         context = super(IssueRequisitionUpdate, self).get_context_data(**kwargs)
#         qs = RequisitionItem.objects.filter(requisition__issue=self.get_object())
#         formset = IssueRequisitionItemFormSet(queryset=qs)
#         context['requisition_formset'] = formset
#         return context

#     def post(self, request, *args, **kwargs):
#         self.object = self.get_object()
#         form_class = self.get_form_class()
#         form = self.get_form(form_class)
#         qs = RequisitionItem.objects.filter(requisition__issue=self.get_object())
#         formsets = IssueRequisitionItemFormSet(self.request.POST, queryset=qs)

#         if form.is_valid() and formsets.is_valid():
#             form.save()
#             formsets.save()    
        
#         return super().post(request, *args, **kwargs)

class ItemListView(ListView):
    template_name = "store/item_list_detail.html"
    model = Item
    queryset = Item.objects.all()


    def get_queryset(self, *args, **kwargs):
        qs = super(ItemListView, self).get_queryset(*args, **kwargs)
        query = self.request.GET.get("q")
        print (self.kwargs)
        return qs

class ItemsListView(LoginRequiredMixin, ListView):
    template_name = "store/items_list2.html"
    context_object_name = 'object'

    def get_queryset(self):
        return Item.objects.all()
        

    def get_context_data(self, **kwargs):
        obj = super(ItemsListView, self).get_context_data(**kwargs)
        obj['items_qs'] = Item.objects.order_by('-entry_date')
        return obj



@login_required
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


class RestockItem2(LoginRequiredMixin, ItemObjectMixin, View):
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

class VendorCreateView(LoginRequiredMixin, PassRequestMixin, SuccessMessageMixin, CreateView):
    template_name = 'store/create_vendor2.html'
    form_class = VendorModelForm
    success_message = 'Vendor created Successfully.'

    success_url = reverse_lazy('store:vendor_list')

class ItemObjectMixin(object):
    model = Item
    def get_object(self):
        id = self.kwargs.get('id')
        obj = None
        if id is not None:
            obj = get_object_or_404(self.model, id=id)
        return obj 


class RestockItem2(LoginRequiredMixin, PassRequestMixin, SuccessMessageMixin, UpdateView):
    model = RestockCartItem
    template_name = 'store/restock_cart_item.html'
    form_class = RestockCartModelForm
    success_message = 'Item Restock Successful'
    success_url = reverse_lazy('store:restock_list')






    # def post(self, request, *args, **kwargs):
    #     self.object = self.get_object()
    #     form_class = self.get_form_class()
    #     form = self.get_form(form_class)
    #     # qs = RequisitionCartItem.objects.filter(requisition_cart__issuerequisition=self.get_object())
    #     obj = get_object_or_404(RequisitionCart,  requisition_no=self.get_object())
    #     qs1 = obj.requisitioncartitem_set.all()
    #     formsets = IssueRequisitionItemFormSet(self.request.POST, queryset=qs1)

    #     if form.is_valid() and formsets.is_valid():
    #         form.save()
    #         formsets.save()    
        
    #     return super().post(request, *args, **kwargs)



# class RestockItem(LoginRequiredMixin, ItemObjectMixin, PassRequestMixin, SuccessMessageMixin, CreateView):
#     template_name = 'store/restock_cart_item.html'
#     form_class = RestockCartModelForm
#     success_message = 'Item Restock Successful.'
#     success_url = reverse_lazy('store:restock_list')


#     def get_context_data(self, *args, **kwargs):
#         context = super(RestockItem, self).get_context_data(**kwargs)
#         context = {}
#         obj = self.get_object()
#         if obj is not None:
#             form = RestockCartModelForm
#             context['object'] = obj  
#             context['form'] = form
#         return context   
   
#     def form_invalid(self, form):
#         return self.render_to_response(self.get_context_data())

class RequisitionDetailsView(LoginRequiredMixin, DetailView):
    template_name = "store/requisition_detail2.html"
    model = Requisition

    def get_context_data(self, *args, **kwargs):
        context = super(RequisitionDetailsView, self).get_context_data(**kwargs)
        data = cartData(self.request)
        requisitionCartItems = data['requisitionCartItems']

        context['requisitionCartItems'] = requisitionCartItems
        return context   

class ItemRestockDetails(LoginRequiredMixin, DetailView):
    template_name = "store/restock_details.html"
    model = RestockCart

    def get_context_data(self, *args, **kwargs):
        context = super(ItemRestockDetails, self).get_context_data(**kwargs)
        data = restockcartData(self.request)
        restockCartItems = data['restockCartItems']

        context['restockCartItems'] = restockCartItems
        return context   

def restock_checkout(request):
    data = restockcartData(request)
    restockCartItems = data['restockCartItems']
    restockCart = data['restockCart']
    items = data['items']

    context = {'items':items, 'restockCart':restockCart, 'restockCartItems':restockCartItems}
    return render(request, 'store/restock_checkout.html', context)





def create_srv(request, id):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'as_attachment=True; filename = "srv.pdf"'

    # doc = SimpleDocTemplate("form_letter.pdf",pagesize=A4,
    #                 rightMargin=72,leftMargin=72,
    #                 topMargin=72,bottomMargin=18)

    doc = SimpleDocTemplate(response,topMargin=20)
    doc.pagesize = landscape(A4)
    doc.title = 'Stores Received Voucher'
    Story=[]
    logo = "static/img/logo_small.png"
    signed_by = "static/img/ceo_sign.jpg"
    limitedDate = "03/05/2010"

    formatted_time = time.ctime()
    full_name = "Infosys"

    
    object = get_object_or_404(RestockCart, pk=id)

    address_parts = ["411 State St.", "Marshalltown, IA 50158"]
    

    # object.vendor


    # Story.append(Spacer(1, 30))

    # Story.append(Paragraph('''<img src="static/img/logo_small.png" valign="middle" width="100" height="100"/> 
    #     <font size=16> <b> RADIOGRAPHERS REGISTRATION BOARD OF NIGERIA<br/>
    #     STORES RECEIVED VOUCHER </b>
    #     </font>'''))
    
    im = Image(logo, 1*inch, 1*inch,hAlign='LEFT')
    sign = Image(signed_by, 1*inch, .8*inch,hAlign='LEFT')

    # Story.append(im)

    
    styles=getSampleStyleSheet()
    styles.add(ParagraphStyle(name='Justify', alignment=TA_JUSTIFY))
    styles.add(ParagraphStyle(name='RIGHT', alignment=TA_RIGHT))

    styles["Normal"].spaceAfter=50
    Story.append(Spacer(1, 25))

    text='''
        <font size=16 style="bulletText">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;RADIOGRAPHERS REGISTRATION BOARD OF NIGERIA<br/>
        <img src="static/img/logo_small.png" valign="middle" width="70" height="70"/> <br/>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
        STORES RECEIVED VOUCHER
        </font>'''

    p_text=Paragraph(text, style=styles["Normal"])
    Story.append(p_text)

    Story.append(Spacer(1, 0))
    ptext = '<font size=14>NO %s</font>' % str(object.restock_no)
    
    Story.append(Paragraph(ptext, styles["RIGHT"]))
    Story.append(Spacer(1, 12))


    # Story.append(Paragraph('''<img src="static/img/logo_small.png" valign="middle" width="100" height="100"/> 
    #     <font size=16> <b> RADIOGRAPHERS REGISTRATION BOARD OF NIGERIA<br/>
    #     STORES RECEIVED VOUCHER </b>
    #     </font>'''))
    Story.append(Spacer(1, 10))


    styles["Normal"].spaceAfter=0
    ptext = '<font size=12>%s</font>' % formatted_time

    Story.append(Paragraph(ptext, styles["Normal"]))
    Story.append(Spacer(1, 12))

    restock_now = object.get_restock_cart_items_qs



    
    # Create return address
    # ptext = '<font size=12> Vendor Name:  </font>' + str(object.vendor)

    # ptext = '<font size=12> Customer Name:  </font>'
    # Story.append(Paragraph(ptext, styles["Normal"]))


    # ptext = '<font size=12>%s</font>' % object.vendor
    # Story.append(Paragraph(ptext, styles["Normal"]))

    # ptext = '<font size=12>%s</font>' % object.vendor.address
    # Story.append(Paragraph(ptext, styles["Normal"]))

    Story.append(Spacer(1, 12))

    
    # restock = RestockCart.objects.filter(restock_no=object.restock_no)
   

    data = []
    data.append(["Item Name", "Vendor", "Unit Price", "Quantity Ordered", "Quantity Received", "Total", "Date Supplied"])



    try:
        for obj in restock_now:
            row = []
            row.append(obj.item_name)
            row.append(obj.vendor)
            row.append(obj.unit_price)
            row.append(obj.quantity_ordered)
            row.append(obj.quantity_received)
            row.append(obj.get_total)
            row.append(obj.date_added)
            data.append(row)
    except:
        pass

    t_style = TableStyle([
                       # ('ALIGN',(1,1),(-2,-2),'RIGHT'),
                       # ('TEXTCOLOR',(1,1),(-2,-2),colors.red),
                       ('VALIGN',(0,0),(0,-1),'TOP'),
                       # ('TEXTCOLOR',(0,0),(0,-1),colors.blue),
                       # ('ALIGN',(0,-1),(-1,-1),'CENTER'),
                       ('VALIGN',(0,-1),(-1,-1),'MIDDLE'),
                       # ('TEXTCOLOR',(0,-1),(0,-1),colors.green),
                       ('TEXTCOLOR',(0,0),(-1,0),colors.green),
                       ('BACKGROUND', (0,0),(-1,0), colors.lavender),
                       ('INNERGRID', (0,0), (-1,-1), 0.25, colors.black),
                       ('BOX', (0,0), (-1,-1), 0.25, colors.black),
                       ])
    s = getSampleStyleSheet()
    s = s["BodyText"]
    s.wordWrap = 'CJK'
    t=Table(data)
    t.setStyle(t_style)

    Story.append(t)
    Story.append(Spacer(1, 12))


    Story.append(Spacer(1, 0))
    ptext = '<font size=14>SRV Total  N%s</font>'% str(object.get_restock_cart_total)
    
    Story.append(Paragraph(ptext, styles["RIGHT"]))
    Story.append(Spacer(1, 12))


    ptext = '<font size=12>Received by:</font>'
    Story.append(Paragraph(ptext, styles["Justify"]))
    Story.append(Spacer(1, 2))
    
    Story.append(sign)

    ptext = '<font size=12>%s</font>' % object.staff_name.get_full_name
    Story.append(Paragraph(ptext, styles["Normal"]))
    Story.append(Spacer(1, 12))
    doc.build(Story)
    return response


styles = getSampleStyleSheet()
styleN = styles['Normal']
styleN.alignment = 1



def footer(canvas, doc):
    canvas.saveState()
    formatted_time = time.ctime()
   


    P = Paragraph(formatted_time + '<font size=10><b> AUTOGENERATED FROM RRBN STORES AND INVENTORY MANAGEMENT SYSTEM </b></font>',
                  styleN)
    w, h = P.wrap(doc.width, doc.bottomMargin)
    P.drawOn(canvas, doc.leftMargin, h)
    canvas.restoreState()


def generate_inventory_report(request):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'as_attachment=True; filename = "inventory_report.pdf"'
    # doc = SimpleDocTemplate("form_letter.pdf",pagesize=A4,
    #                 rightMargin=72,leftMargin=72,
    #                 topMargin=72,bottomMargin=18)
    doc = SimpleDocTemplate(response, rightMargin=50,leftMargin=60,
                    topMargin=120,bottomMargin=38)
    # doc = SimpleDocTemplate(response,topMargin=20)
    doc.pagesize = landscape(A4)
    doc.title = 'Inventory Report'
    
    # frame = Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height, id='normal')
    frame = Frame(inch, inch, 9.8*inch, 7*inch, showBoundary=0)

    template = PageTemplate(id='generate_inventory_report',frames=frame, onPage=footer)
  
    doc.addPageTemplates([template])
   
    Story=[]
    logo = "static/img/logo_small.png"
    signed_by = "static/img/ceo_sign.jpg"
    limitedDate = "03/05/2010"
    formatted_time = time.ctime()
    full_name = "Infosys"
    # object = get_object_or_404(Restock, pk=id)
    address_parts = ["411 State St.", "Marshalltown, IA 50158"]
   
    im = Image(logo, 1*inch, 1*inch,hAlign='LEFT')
    sign = Image(signed_by, 1*inch, .8*inch,hAlign='LEFT')
    # Story.append(im)
    styles=getSampleStyleSheet()
    styles.add(ParagraphStyle(name='Justify', alignment=TA_JUSTIFY))
    styles.add(ParagraphStyle(name='RIGHT', alignment=TA_RIGHT))
    styles.add(ParagraphStyle(name='Center', alignment=TA_CENTER))

    styles["Normal"].spaceAfter=50
    Story.append(Spacer(1, 25))

    text='''
        <font size=16>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;RADIOGRAPHERS REGISTRATION BOARD OF NIGERIA<br/>
        <img src="static/img/logo_small.png" valign="middle" width="70" height="70"/> <br/>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
        STORES INVENTORY REPORT
        </font>'''

    p_text=Paragraph(text, style=styles["Normal"])
    Story.append(p_text)
    Story.append(Spacer(1, 30))


    styles["Normal"].spaceAfter=0
    ptext = '<font size=12>%s</font>' % formatted_time

    Story.append(Paragraph(ptext, styles["Normal"]))
    Story.append(Spacer(1, 12))



    item = Item.objects.count()
    
    ptext = '<font size=14><b>STORES INVENTORY ITEMS COUNT: </b> %s</font>' % item 

    Story.append(Paragraph(ptext, styles["Normal"]))
    Story.append(Spacer(1, 12))
    
    item = Item.objects.all()

    data = []
    data.append(["Stock Code", "Item Name", "Category", "UOM", "Unit Price", "Vendor", "Quantity", "Reorder No"])

    try:
        for obj in item:
            row = []
            row.append(obj.stock_code)
            row.append(obj.item_name)
            row.append(obj.category)
            row.append(obj.unit)
            row.append(obj.unit_price)
            row.append(obj.vendor)
            row.append(obj.quantity)
            row.append(obj.re_order_no)
            data.append(row)
    except:
        pass

    t_style = TableStyle([
                       # ('ALIGN',(1,1),(-2,-2),'RIGHT'),
                       # ('TEXTCOLOR',(1,1),(-2,-2),colors.red),
                       ('VALIGN',(0,0),(0,-1),'TOP'),
                       # ('TEXTCOLOR',(0,0),(0,-1),colors.blue),
                       # ('ALIGN',(0,-1),(-1,-1),'CENTER'),
                       ('VALIGN',(0,-1),(-1,-1),'MIDDLE'),
                       # ('TEXTCOLOR',(0,-1),(0,-1),colors.green),
                       ('TEXTCOLOR',(0,0),(-1,0),colors.green),
                       ('BACKGROUND', (0,0),(-1,0), colors.lavender),
                       ('INNERGRID', (0,0), (-1,-1), 0.25, colors.black),
                       ('BOX', (0,0), (-1,-1), 0.25, colors.black),
                       ])
    s = getSampleStyleSheet()
    s = s["BodyText"]
    s.wordWrap = 'CJK'
    t=Table(data, hAlign='LEFT')
    t.setStyle(t_style)

    Story.append(t)
    Story.append(Spacer(1, 12))
    doc.build(Story)
    
    return response


class RequisitionWizard(SessionWizardView):
    form_list = [RequisitionsModelForm, RequisitionItemFormSet]
    template_name = 'store/formwizard.html'
    # def done(self, form_list, **kwargs):
    #     do_something_with_the_form_data(form_list)
    #     return HttpResponseRedirect("/")
        # return HttpResponseRedirect(reverse("store:find_item"))

    def done(self, form_list, **kwargs):
        form_data = [form.cleaned_data for form in form_list]
        # requisition_data = Requisition(requisition_reason = form_data[0]['requisition_reason'], requesting_staff = form_data[0]['requesting_staff'], authorized_by = form_data[0]['authorized_by'], department = form_data[0]['department'],)
        # requisition_data.save( )
        # requisitionitem_data = RequisitionItem(requisition = form_data[0]['requisition'], item = form_data[0]['item'], quantity = form_data[0]['quantity'])
        form.save( )
        return render(self.request, 'store/emptylist.html', {'data': form_data})


class ItemCountView(View):
    def get(self, request, *args, **kwargs):
        if request.is_ajax():
            requisition_id = self.request.session.get("requisition_id")
            if requisition_id == None:
                count = 0
            else:
                requisition = Requisition.objects.get(id=requisition_id)
                count = requisition.items.count()
            request.session["requisition_item_count"] = count
            return JsonResponse({"count": count})
        else:
            raise Http404

# class ItemCreateView(LoginRequiredMixin, PassRequestMixin, SuccessMessageMixin, CreateView):
#     template_name = 'store/create_item2.html'
#     form_class = ItemModelForm
#     success_message = 'Item created Successfully.'

#     success_url = reverse_lazy('store:items_list')










class CreateRequisitionItems(View):
    def get(self, request, *args, **kwargs):
        requisition_id = request.GET.get("item")
        delete_item = request.GET.get("delete")
        if requisition_id:
            item_instance = get_object_or_404(Item, id=item_id)
            qty = request.GET.get("qty")
            requisition = Requisition.objects.all().first()
            requisition_item = RequisitionItem.objects.get_or_create(requisition=requisition, item=item_instance)[0]
            if delete_item:
                requisition_item.delete()
            else:
                requisition_item.quantity = qty
                requisition_item.save()
        return HttpResponseRedirect("/")

class CreateRequisitionItems(View):
    def get(self, request, *args, **kwargs):
        request.session.set_expiry(0)
        requisition_id = request.session.get("requisition_id")
        if requisition_id == None:
            requisition = Requisition()
            requisition.save()
            requisition_id = requisition.id
            request.session["requisition_id"] = requisition_id
        requisition = Requisition.objects.get(id=requisition_id)
        if request.user.is_authenticated():
            requisition.department = request.user.department
            requisition.requesting_staff = request.user
            requisition.authorized_by = request.user
            requisition.save()
        item_id = request.GET.get("item")
        delete_item = request.GET.get("delete")
        if item_id:
            item_instance = get_object_or_404(Item, id=item_id)
            qty = request.GET.get("qty")
            requisition_item = RequisitionItem.objects.get_or_create(requisition=requisition, item=item_instance)[0]
            if delete_item:
                requisition_item.delete()
            else:
                requisition_item.quantity = qty
                requisition_item.save()
        return HttpResponseRedirect("/")



# class RequestItem(LoginRequiredMixin, CreateView):
#     model = Requisition
#     form_class = RequisitionsModelForm
#     formset_class = RequisitionItemFormSet
#     template_name = 'store/requisition_update3.html'
#     success_url = reverse_lazy('store:requisition_list')

#     def get_context_data(self, *args, **kwargs):
#         context = super(RequestItem, self).get_context_data(**kwargs)
#         # qs = RequisitionItem.objects.filter(requisition=self.get_object())
#         # qs = RequisitionItem.objects.all()
#         formset = RequisitionItemFormSet()
#         context['requisition_formset'] = formset
#         return context

#     # def get_initial(self):
#     #     return {
#     #         'requisition': self.kwargs["pk"],   
#     #     }

#     def post(self, request, *args, **kwargs):
#         self.object = self.get_object()
#         form_class = self.get_form_class()
#         form = self.get_form(form_class)
#         # qs = RequisitionItem.objects.all()
#         formsets = RequisitionItemFormSet(self.request.POST)

#         if form.is_valid() and formsets.is_valid():
#             form.save()

#             new_instances = formsets.save(commit=False)
#             for new_instance in new_instances:
#                 new_instance.requisition = self.get_object()
#                 new_instance.save()

#             formsets.save()    
#             return self.form_valid(form)
#         else:
#             return self.form_invalid(form)


class RequestItem(LoginRequiredMixin, CreateView):
    model = Requisition
    template_name = 'store/requisition_create_list.html'
    form_class = RequisitionsModelForm
    success_url = reverse_lazy('store:requisition_list')

    def get_object(self, *args, **kwargs):
        self.request.session.set_expiry(0)
        requisition_id = self.request.session.get("requisition_id")
        if requisition_id == None:
            requisition = Requisition()
            requisition.save()
            requisition_id = requisition.id
            requisition.department = self.request.user.department
            requisition.requesting_staff = self.request.user
            requisition.authorized_by = self.request.user
            requisition.save()
            self.request.session["requisition_id"] = requisition_id
        requisition, created = Requisition.objects.get_or_create(id=requisition_id)
        return requisition

    def get(self, request, *args, **kwargs):
        requisition = self.get_object()
        item_id = request.GET.get("item")
        delete_item = request.GET.get("delete", False)
        flash_message = ""
        item_added = False
        if item_id:
            item_instance = get_object_or_404(Item, id=item_id)
            qty = request.GET.get("qty", 1)
            try:
                if int(qty) < 1:
                    delete_item = True
            except:
                raise Http404
            requisition_item, created = RequisitionItem.objects.get_or_create(requisition=requisition, item=item_instance)
            
            if created:
                flash_message = "Item added to requisition list"
                item_added = True
            if delete_item:
                flash_message = "Item removed from requisition list"
                requisition_item.delete()
            else:
                if not created:
                    flash_message = "Requisition list item successfully updated"
                requisition_item.quantity = qty
                requisition_item.save()
            if not request.is_ajax():
                return HttpResponseRedirect(reverse("store:find_item"))
       

        if request.is_ajax():
            try:
                total = requisition_item.line_item_total
            except:
                total = None
            data = {
                    "deleted": delete_item,
                    "item_added": item_added,
                    "line_total": total,
                    "flash_message": flash_message,

                    }
            return JsonResponse(data)

        context = {
            
            "form":self.get_form(),
            "object":self.get_object()
        }
        template = self.template_name
        return render(request, template, context)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            requisition = form.save(commit=False)
            del request.session["requisition_id"]
            requisition.save()

        return self.form_valid(form)
        # return self.form_invalid(form)


# class RequestItem(LoginRequiredMixin, CreateView):
#     model = Requisition
#     template_name = 'store/requisition_create_list.html'
#     form_class = RequisitionsModelForm

#     def get(self, request, *args, **kwargs):
#         request.session.set_expiry(0)
#         requisition_id = request.session.get("requisition_id")
#         if requisition_id == None:
#             requisition = Requisition()
#             # if request.user.is_authenticated():
#             requisition.department = request.user.department
#             requisition.requesting_staff = request.user
#             requisition.authorized_by = request.user
#             requisition.save()
                
#             requisition_id = requisition.id
#             request.session["requisition_id"] = requisition_id
#         requisition = Requisition.objects.get(id=requisition_id)
#         return requisition

        
#         item_id = request.GET.get("item")
#         delete_item = request.GET.get("delete")
#         if item_id:
#             item_instance = get_object_or_404(Item, id=item_id)
#             qty = request.GET.get("qty", 1)
#             try:
#                 if int(qty) < 1:
#                     delete_item = True
#             except:
#                 raise Http404
#             requisition_item, created = RequisitionItem.objects.get_or_create(requisition=requisition, item=item_instance)
            
#             if created:
#                 flash_message = "Item added to requisition list"
#                 item_added = True
#             if delete_item:
#                 flash_message = "Item removed from requisition list"
#                 requisition_item.delete()
#             else:
#                 if not created:
#                     flash_message = "Requisition list item successfully updated"
#                 requisition_item.quantity = qty
#                 requisition_item.save()
#             if not request.is_ajax():
#                 return HttpResponseRedirect(reverse("store:find_item"))
       

#         if request.is_ajax():
#             try:
#                 total = requisition_item.line_item_total
#             except:
#                 total = None
#             data = {
#                     "deleted": delete_item,
#                     "item_added": item_added,
#                     "line_total": total,
#                     "flash_message": flash_message,

#                     }
#             return JsonResponse(data)

#         context = {
            
#             "form":self.get_form(),
#             "object":requisition
#         }
#         template = self.template_name
#         return render(request, template, context)

  

#     def post(self, request, *args, **kwargs):
#         # requisition = Requisition.objects.get(id=requisition_id)
#         self.object = requisition
#         form = self.get_form()
#         if form.is_valid():
#             requisition = form.save(commit=False)
#             del request.session["requisition_id"]
#             requisition.save()

#         return self.form_valid(form)
#         return self.form_invalid(form)        


    







# class RequisitionDetailsView(LoginRequiredMixin, DetailView):
#     template_name = "store/requisition_detail2.html" 
#     model = Requisition

class RequisitionDeleteView(LoginRequiredMixin, RequisitionObjectMixin, View):
    template_name = "store/requisition_delete.html" # DetailView
    def get(self, request, id=None, *args, **kwargs):
        # GET method
        context = {}
        obj = self.get_requisition()
        if obj is not None:
            context['object'] = obj
        return render(request, self.template_name, context)

    def post(self, request, id=None,  *args, **kwargs):
        # POST method
        context = {}
        obj = self.get_requisition()
        if obj is not None:
            obj.delete()
            context['object'] = None
            return redirect('store:requisition_list')
        return render(request, self.template_name, context)


# class IssueRequisition(RequisitionObjectMixin, PassRequestMixin, SuccessMessageMixin, CreateView):





class RequisitionUpdateView2(LoginRequiredMixin, PassRequestMixin, SuccessMessageMixin, UpdateView):
    model = Requisition
    template_name = 'store/requisition_update.html'
    form_class = RequisitionForm
    success_message = 'Success: Requisition Items updated.'
    success_url = reverse_lazy('store:requisition_list')


    def get_form(self, *args, **kwargs):
        form = super(RequisitionUpdateView, self).get_form(*args, **kwargs)

        print (form)
        
        return form

class RequisitionCheckout(LoginRequiredMixin, DetailView):
    model = Requisition
    template_name = "store/requisition_checkout.html"
    #form_class = GuestCheckoutForm

    def get_object(self, *args, **kwargs):
        requisition_id = self.request.session.get("requisition_id")
        if requisition_id == None:
            return redirect("store:create_item_requisition")
        requisition = Requisition.objects.get(id=requisition_id)
        return requisition

    def get_context_data(self, *args, **kwargs):
        context = super(RequisitionCheckout, self).get_context_data(*args, **kwargs)
        
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            form.save()
            
    def get_success_url(self):
        return reverse("store:requisition_list")
 




class ItemCategoyListView(LoginRequiredMixin, ListView):
    template_name = "store/items_category_list.html"
    context_object_name = 'object'

    def get_queryset(self):
        return Category.objects.all()
        

    def get_context_data(self, **kwargs):
        obj = super(ItemCategoyListView, self).get_context_data(**kwargs)
        obj['category_qs'] = Category.objects.order_by('id')
        return obj



class VendorCreateView(LoginRequiredMixin, PassRequestMixin, SuccessMessageMixin, CreateView):
    template_name = 'store/create_vendor2.html'
    form_class = VendorModelForm
    success_message = 'Vendor created Successfully.'

    success_url = reverse_lazy('store:vendor_list')

class CategoryCreateView(LoginRequiredMixin, PassRequestMixin, SuccessMessageMixin, CreateView):
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



class VendorDetailView(LoginRequiredMixin, VendorObjectMixin, View):
    template_name = "store/vendor_detail2.html"

    def get(self, request, id=None, *args, **kwargs):
        context = {'object': self.get_object()}
        return render(request, self.template_name, context)


class VendorUpdateView(LoginRequiredMixin, PassRequestMixin, SuccessMessageMixin, UpdateView):
    model = Vendor
    template_name = 'store/vendor_update2.html'
    form_class = VendorModelForm
    success_message = 'Success: Vendor Details were updated.'
    success_url = reverse_lazy('store:vendor_list')



class VendorDeleteView(LoginRequiredMixin, VendorObjectMixin, View):
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


class ItemUpdateView(LoginRequiredMixin, PassRequestMixin, SuccessMessageMixin, UpdateView):
    model = Item
    template_name = 'store/item_update2.html'
    form_class = ItemModelForm
    success_message = 'Success: Item details were updated.'
    success_url = reverse_lazy('store:items_list')



class ItemDeleteView(LoginRequiredMixin, ItemObjectMixin, View):
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


class CategoryDetailView(LoginRequiredMixin, CategoryObjectMixin, View):
    template_name = "store/category_detail2.html"

    def get(self, request, id=None, *args, **kwargs):
        context = {'object': self.get_object()}
        return render(request, self.template_name, context)


class CategoryUpdateView(LoginRequiredMixin, PassRequestMixin, SuccessMessageMixin, UpdateView):
    model = Category
    template_name = 'store/category_update2.html'
    form_class = CategoryModelForm
    success_message = 'Success: Category details were updated.'
    success_url = reverse_lazy('store:category_list')


class CategoryDeleteView(LoginRequiredMixin, CategoryObjectMixin, View):
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

