from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.decorators import method_decorator

# Create your views here.
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
from .models import Vendor, Category, Contract, Project
from .forms import VendorModelForm, CategoryModelForm, ContractModelForm, ProjectModelForm
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from bootstrap_modal_forms.generic import BSModalCreateView
from bootstrap_modal_forms.mixins import PassRequestMixin, CreateUpdateAjaxMixin
from django.urls import reverse, reverse_lazy
from django.contrib.auth.models import User
from django.conf import settings
from decimal import Decimal
from django.http import JsonResponse, HttpResponse
from django.template.loader import render_to_string
from django.db.models import Q, Count, F, Value
from django.core.exceptions import ObjectDoesNotExist
from itertools import chain
from operator import attrgetter
import datetime
import csv
from datetime import datetime
from django.template.loader import render_to_string
from weasyprint import HTML
from weasyprint.fonts import FontConfiguration
import tempfile
from django.db.models import Sum
import xlwt
from django.contrib.auth import get_user_model
User = get_user_model()



class DashboardTemplateView(LoginRequiredMixin, TemplateView):
    template_name = "procurement/procurement_dashboard.html"

    
    def get_context_data(self, *args, **kwargs):
        context = super(DashboardTemplateView, self).get_context_data(*args, **kwargs)
        #this_month = (dt.datetime.now() + dt.timedelta(days=30))
        #startdate = datetime.today()
        #enddate = startdate + dt.timedelta(days=30)
        #context['vass'] = Assign.objects.all()
        #context['vassmnth'] = Assign.objects.filter(approved_date__range=[startdate, enddate])
        #context['vreq_pend'] = Request.objects.filter(request_status=1)
        #context['vreq_pend_mnth'] = Request.objects.filter(request_date__lte=this_month, request_status=1)
        #context['sch_pend'] = Schedule.objects.filter(schedule_status=1)
        #context['sch_pend_mnth'] = Schedule.objects.filter(scheduled_on__lte=this_month, schedule_status=1)
        #context['rep'] = Repair.objects.all()
        #context['rep_mnth'] = Repair.objects.filter(repair_date__lt=this_month)
        return context


class VendorListView(LoginRequiredMixin, ListView):
    template_name = "procurement/vendor_list.html"
    context_object_name = 'object'
    

    def get_queryset(self):
        return Vendor.objects.all()
        
    def get_context_data(self, **kwargs):
        obj = super(VendorListView, self).get_context_data(**kwargs)
        obj['vendor_list_qs'] = Vendor.objects.order_by('-date_created')
        return obj


class VendorCreateView(LoginRequiredMixin, PassRequestMixin, SuccessMessageMixin, CreateView):
    template_name = 'procurement/add_vendor.html'
    form_class = VendorModelForm
    success_message = 'Vendor Added Successfully.'

    success_url = reverse_lazy('procurement:vendor_list')

class VendorDetailView(LoginRequiredMixin, DetailView):
    template_name = "procurement/vendor_detail.html"
    model = Vendor


class VendorUpdateView(LoginRequiredMixin, PassRequestMixin, SuccessMessageMixin, UpdateView):
    model = Vendor
    template_name = 'procurement/update_vendor.html'
    form_class = VendorModelForm
    success_message = 'Vendor Updated Successfully'
    success_url = reverse_lazy('procurement:vendor_list')



class VendorObjectMixin(object):
    model = Vendor
    def get_object(self):
        id = self.kwargs.get('id')
        obj = None
        if id is not None:
            obj = get_object_or_404(self.model, id=id)
        return obj 


class VendorDeleteView(LoginRequiredMixin, VendorObjectMixin, View):
    template_name = "procurement/vendor_delete.html" # DetailView
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
            return redirect('procurement:vendor_list')
        return render(request, self.template_name, context)


class CategoryListView(LoginRequiredMixin, ListView):
    template_name = "procurement/category_list.html"
    context_object_name = 'object'
    

    def get_queryset(self):
        return Category.objects.all()
        
    def get_context_data(self, **kwargs):
        obj = super(CategoryListView, self).get_context_data(**kwargs)
        obj['category_list_qs'] = Category.objects.order_by('-added_on')
        return obj

class CategoryCreateView(LoginRequiredMixin, PassRequestMixin, SuccessMessageMixin, CreateView):
    template_name = 'procurement/add_category.html'
    form_class = CategoryModelForm
    success_message = 'Category Added Successfully.'

    success_url = reverse_lazy('procurement:category_list')


class CategoryDetailView(LoginRequiredMixin, DetailView):
    template_name = "procurement/category_detail.html"
    model = Category


class CategoryUpdateView(LoginRequiredMixin, PassRequestMixin, SuccessMessageMixin, UpdateView):
    model = Category
    template_name = 'procurement/update_category.html'
    form_class = CategoryModelForm
    success_message = 'Category Updated Successfully'
    success_url = reverse_lazy('procurement:category_list')



class CategoryObjectMixin(object):
    model = Category
    def get_object(self):
        id = self.kwargs.get('id')
        obj = None
        if id is not None:
            obj = get_object_or_404(self.model, id=id)
        return obj 


class CategoryDeleteView(LoginRequiredMixin, CategoryObjectMixin, View):
    template_name = "procurement/category_delete.html" # DetailView
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
            return redirect('procurement:category_list')
        return render(request, self.template_name, context)

class ContractListView(LoginRequiredMixin, ListView):
    template_name = "procurement/contract_list.html"
    context_object_name = 'object'
    

    def get_queryset(self):
        return Contract.objects.order_by('-date_added')
        
    def get_context_data(self, **kwargs):
        obj = super(ContractListView, self).get_context_data(**kwargs)
        obj['contract_list_qs'] = Contract.objects.filter(contract_status="Awarded")
        return obj

class ContractCreateView(LoginRequiredMixin, PassRequestMixin, SuccessMessageMixin, CreateView):
    template_name = 'procurement/add_contract.html'
    form_class = ContractModelForm
    success_message = 'Contract Created Successfully.'

    success_url = reverse_lazy('procurement:contract_list')

class ContractDetailView(LoginRequiredMixin, DetailView):
    template_name = "procurement/contract_detail.html"
    model = Contract


class ContractUpdateView(LoginRequiredMixin, PassRequestMixin, SuccessMessageMixin, UpdateView):
    model = Contract
    template_name = 'procurement/update_contract.html'
    form_class = ContractModelForm
    success_message = 'Contract Updated Successfully'
    success_url = reverse_lazy('procurement:contract_list')



class ContractObjectMixin(object):
    model = Contract
    def get_object(self):
        id = self.kwargs.get('id')
        obj = None
        if id is not None:
            obj = get_object_or_404(self.model, id=id)
        return obj 


class ContractDeleteView(LoginRequiredMixin, ContractObjectMixin, View):
    template_name = "procurement/contract_delete.html" # DetailView
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
            return redirect('procurement:contract_list')
        return render(request, self.template_name, context)

class ProjectListView(LoginRequiredMixin, ListView):
    template_name = "procurement/project_list.html"
    context_object_name = 'object'
    

    def get_queryset(self):
        return Project.objects.order_by('-date_documented')
        
    def get_context_data(self, **kwargs):
        obj = super(ProjectListView, self).get_context_data(**kwargs)
        obj['project_list_qs'] = Project.objects.order_by('-date_documented')
        return obj

class ProjectCreateView(LoginRequiredMixin, ContractObjectMixin, PassRequestMixin, SuccessMessageMixin, CreateView):
    template_name = 'procurement/add_project.html'
    form_class = ProjectModelForm
    success_message = 'Project Created Successfully.'
    success_url = reverse_lazy('procurement:projects_list')


    def get_context_data(self, *args, **kwargs):
        context = super(ProjectCreateView, self).get_context_data(**kwargs)
        context = {}
        obj = self.get_object()
        if obj is not None:
            form = ProjectModelForm(instance=obj)
            context['object'] = obj  
            context['form'] = form
        return context   
   
    def form_invalid(self, form):
        form = self.get_form()

        context = {}
        obj = self.get_object()
        if obj is not None:
          
           context['object'] = obj
           context['form'] = form 
          
        return self.render_to_response(context)


class ProjectDetailView(LoginRequiredMixin, DetailView):
    template_name = "procurement/project_detail.html"
    model = Project

    
class ProjectUpdateView(LoginRequiredMixin, PassRequestMixin, SuccessMessageMixin, UpdateView):
    model = Project
    template_name = 'procurement/update_project.html'
    form_class = ProjectModelForm
    success_message = 'Project Updated Successfully'
    success_url = reverse_lazy('procurement:projects_list')


class ProjectObjectMixin(object):
    model = Project
    def get_object(self):
        id = self.kwargs.get('id')
        obj = None
        if id is not None:
            obj = get_object_or_404(self.model, id=id)
        return obj 


class ProjectDeleteView(LoginRequiredMixin, ProjectObjectMixin, View):
    template_name = "procurement/project_delete.html" # DetailView
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
            return redirect('procurement:projects_list')
        return render(request, self.template_name, context)


