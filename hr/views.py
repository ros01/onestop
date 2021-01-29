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
from .models import Employee, Driver, Department, Performance, Leave, Learning, Location, Title, Grade
from rrbnstaff.models import Request

from .forms import JobTitleModelForm, PayGradeModelForm
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



class DashboardTemplateView(LoginRequiredMixin, TemplateView):
    template_name = "hr/hr_dashboard.html"

    
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

class LocationsListView(LoginRequiredMixin, ListView):
    template_name = "hr/locations_list.html"
    context_object_name = 'object'
    redirect_field_name = 'redirect_to'

    def get_queryset(self):
        return Location.objects.all()
        
    def get_context_data(self, **kwargs):
        obj = super(LocationsListView, self).get_context_data(**kwargs)
        obj['location_qs'] = Location.objects.order_by('-name')
        return obj


class JobTitlesListView(LoginRequiredMixin, ListView):
    template_name = "hr/job_titles_list.html"
    context_object_name = 'object'
    redirect_field_name = 'redirect_to'

    def get_queryset(self):
        return Title.objects.all()
        
    def get_context_data(self, **kwargs):
        obj = super(JobTitlesListView, self).get_context_data(**kwargs)
        obj['job_title_qs'] = Title.objects.order_by('-date_added')
        return obj


class JobTitleCreateView(LoginRequiredMixin, PassRequestMixin, SuccessMessageMixin, CreateView):
    template_name = 'hr/add_job_title.html'
    form_class = JobTitleModelForm
    success_message = 'Job Title Added Successfully.'

    success_url = reverse_lazy('hr:job_titles_list')


class JobTitleDetailView(LoginRequiredMixin, DetailView):
    template_name = "hr/job_titles_detail.html"
    model = Title


class JobTitleUpdateView(LoginRequiredMixin, PassRequestMixin, SuccessMessageMixin, UpdateView):
    model = Title
    template_name = 'hr/update_job_title.html'
    form_class = JobTitleModelForm
    success_message = 'Job Title Successfully Updated'
    success_url = reverse_lazy('hr:job_titles_list')



class JobTitleObjectMixin(object):
    model = Title
    def get_object(self):
        id = self.kwargs.get('id')
        obj = None
        if id is not None:
            obj = get_object_or_404(self.model, id=id)
        return obj 


class JobTitleDeleteView(LoginRequiredMixin, JobTitleObjectMixin, View):
    template_name = "hr/job_title_delete.html" # DetailView
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
            return redirect('hr:job_titles_list')
        return render(request, self.template_name, context)


class PayGradeListView(LoginRequiredMixin, ListView):
    template_name = "hr/pay_grade_list.html"
    context_object_name = 'object'
    redirect_field_name = 'redirect_to'

    def get_queryset(self):
        return Grade.objects.all()
        
    def get_context_data(self, **kwargs):
        obj = super(PayGradeListView, self).get_context_data(**kwargs)
        obj['pay_grade_qs'] = Grade.objects.order_by('-date_created')
        return obj


class PayGradeCreateView(LoginRequiredMixin, PassRequestMixin, SuccessMessageMixin, CreateView):
    template_name = 'hr/add_pay_grade.html'
    form_class = PayGradeModelForm
    success_message = 'Pay Grade Created Successfully.'

    success_url = reverse_lazy('hr:pay_grade_list')


class PayGradeDetailView(LoginRequiredMixin, DetailView):
    template_name = "hr/pay_grade_detail.html"
    model = Grade


class PayGradeUpdateView(LoginRequiredMixin, PassRequestMixin, SuccessMessageMixin, UpdateView):
    model = Grade
    template_name = 'hr/update_pay_grade.html'
    form_class = PayGradeModelForm
    success_message = 'Pay Grade Updated Successfully'
    success_url = reverse_lazy('hr:pay_grade_list')



class PayGradeObjectMixin(object):
    model = Grade
    def get_object(self):
        id = self.kwargs.get('id')
        obj = None
        if id is not None:
            obj = get_object_or_404(self.model, id=id)
        return obj 


class PayGradeDeleteView(LoginRequiredMixin, PayGradeObjectMixin, View):
    template_name = "hr/pay_grade_delete.html" # DetailView
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
            return redirect('hr:pay_grade_list')
        return render(request, self.template_name, context)


class StaffProfileListView(LoginRequiredMixin, ListView):
    template_name = "hr/staff_profile_list.html"
    context_object_name = 'object'
    redirect_field_name = 'redirect_to'

    def get_queryset(self):
        return Employee.objects.all()
        
    def get_context_data(self, **kwargs):
        obj = super(StaffProfileListView, self).get_context_data(**kwargs)
        obj['staff_profile_qs'] = Employee.objects.order_by('-profile_creation_date')
        return obj


class StaffProfileDetailView(LoginRequiredMixin, DetailView):
    template_name = "hr/staff_profile_detail.html"
    model = Employee

