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
from .models import Employee, Driver, Performance, Leave, Location, Title, Grade, Specify, Document, Vendor, Category, Training, Appraisal, Schedule, Discipline, Compliance, Course
from rrbnstaff.models import Request

from .forms import JobTitleModelForm, PayGradeModelForm, AssignLeaveRequestModelForm, EndLeaveModelForm, TrainingModelForm, VendorModelForm, CategoryModelForm, AppraisalModelForm, ScheduleModelForm, PerformanceEvaluationModelForm, DisciplineModelForm, ComplianceModelForm, CourseModelForm
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


class LeaveRequestListView(LoginRequiredMixin, ListView):
    template_name = "hr/leave_request_list.html"
    context_object_name = 'object'
    

    def get_queryset(self):
        return Leave.objects.order_by('-leave_application_date')
        
    def get_context_data(self, **kwargs):
        obj = super(LeaveRequestListView, self).get_context_data(**kwargs)
        obj['leave_request_qs'] = Leave.objects.filter(leave_status="Pending Approval")
        return obj


class LeaveApprovalListView(LoginRequiredMixin, ListView):
    template_name = "hr/leave_approval_list.html"
    context_object_name = 'object'
    
    def get_queryset(self):
        return Leave.objects.order_by('-leave_application_date')
        
    def get_context_data(self, **kwargs):
        obj = super(LeaveApprovalListView, self).get_context_data(**kwargs)
        obj['leave_approval_qs'] = Leave.objects.filter(leave_status="Approved")
        return obj

class LeaveAssignmentListView(LoginRequiredMixin, ListView):
    template_name = "hr/leave_assignment_list.html"
    context_object_name = 'object'
    def get_queryset(self):
        return Leave.objects.order_by('-leave_application_date')
        
    def get_context_data(self, **kwargs):
        obj = super(LeaveAssignmentListView, self).get_context_data(**kwargs)
        obj['leave_assignment_qs'] = Specify.objects.filter(leave_status="Leave Days Assigned")
        return obj

class LeaveRequestDetailView(LoginRequiredMixin, DetailView):
    template_name = "hr/leave_request_detail.html"
    model = Leave

def leave_request_details(request, id):
  leave = get_object_or_404(Leave, pk=id)
  context={'leave': leave,       
           }
  return render(request, 'hr/leave_request_details.html', context)

def approve_leave_request(request, id):
  if request.method == 'POST':
     leave = get_object_or_404(Leave, pk=id)
     leave.leave_status = "Approved"
     leave.save()
     context = {}
     context['object'] = leave
     messages.success(request, ('Leave Approval Successful'))
     return redirect ('hr:leave_approval_list')
 

def reject_leave_request(request, id):
  if request.method == 'POST':
     payment = get_object_or_404(Payment, pk=id)
     payment.vet_status = 3
     payment.save()
     context = {}
     context['object'] = payment
     subject = 'Failed verification of Registration and Payment Details'
     from_email = settings.DEFAULT_FROM_EMAIL
     to_email = [payment.email] 
     contact_message = get_template('monitoring/verification_failed.txt').render(context)
     send_mail(subject, contact_message, from_email, to_email, fail_silently=False)
     messages.error(request, ('Verification failed.  Hospital has been sent an email to re-apply with the correct details.'))
     return redirect('/monitoring/'+str(payment.id))


class LeaveApprovalDetailView(LoginRequiredMixin, DetailView):
    template_name = "hr/leave_request_approved.html"
    model = Leave


class LeaveObjectMixin(object):
    model = Leave
    def get_object(self):
        id = self.kwargs.get('id')
        obj = None
        if id is not None:
            obj = get_object_or_404(self.model, id=id)
        return obj 


class AssignLeaveRequest(LoginRequiredMixin, LeaveObjectMixin, PassRequestMixin, SuccessMessageMixin, CreateView):
    template_name = 'hr/assign_leave_request.html'
    form_class = AssignLeaveRequestModelForm
    success_message = 'Leave days assigned successfully'
    success_url = reverse_lazy('hr:leave_assignment_list') 

    def get_context_data(self, *args, **kwargs):
        context = super(AssignLeaveRequest, self).get_context_data(**kwargs)
        context = {}
        obj = self.get_object()
        if obj is not None:
            form = AssignLeaveRequestModelForm(instance=obj)
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


class LeaveAssignmentDetailView(LoginRequiredMixin, DetailView):
    template_name = "hr/leave_assignment_detail.html"
    model = Specify

class SpecifyObjectMixin(object):
    model = Specify
    def get_object(self):
        id = self.kwargs.get('id')
        obj = None
        if id is not None:
            obj = get_object_or_404(self.model, id=id)
        return obj 

class LeaveHistoryListView(LoginRequiredMixin, ListView):
    template_name = "hr/leave_history_list.html"
    context_object_name = 'object'
    

    def get_queryset(self):
        return Leave.objects.order_by('-leave_application_date')
        
    def get_context_data(self, **kwargs):
        obj = super(LeaveHistoryListView, self).get_context_data(**kwargs)
        obj['leave_history_qs'] = Document.objects.filter(leave_status="Leave Completed")
        return obj


class EndLeave(LoginRequiredMixin, SpecifyObjectMixin, PassRequestMixin, SuccessMessageMixin, CreateView):
    template_name = 'hr/end_leave.html'
    form_class = EndLeaveModelForm
    success_message = 'Leave successfully concluded'
    success_url = reverse_lazy('hr:leave_history_list') 

    def get_context_data(self, *args, **kwargs):
        context = super(EndLeave, self).get_context_data(**kwargs)
        context = {}
        obj = self.get_object()
        if obj is not None:
            form = EndLeaveModelForm(instance=obj)
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


class LeaveHistoryDetailView(LoginRequiredMixin, DetailView):
    template_name = "hr/leave_history_detail.html"
    model = Document


class VendorListView(LoginRequiredMixin, ListView):
    template_name = "hr/vendor_list.html"
    context_object_name = 'object'
    

    def get_queryset(self):
        return Vendor.objects.all()
        
    def get_context_data(self, **kwargs):
        obj = super(VendorListView, self).get_context_data(**kwargs)
        obj['vendor_list_qs'] = Vendor.objects.order_by('-date_created')
        return obj


class VendorCreateView(LoginRequiredMixin, PassRequestMixin, SuccessMessageMixin, CreateView):
    template_name = 'hr/add_vendor.html'
    form_class = VendorModelForm
    success_message = 'Vendor Added Successfully.'

    success_url = reverse_lazy('hr:vendor_list')

class VendorDetailView(LoginRequiredMixin, DetailView):
    template_name = "hr/vendor_detail.html"
    model = Vendor


class VendorUpdateView(LoginRequiredMixin, PassRequestMixin, SuccessMessageMixin, UpdateView):
    model = Vendor
    template_name = 'hr/update_vendor.html'
    form_class = VendorModelForm
    success_message = 'Vendor Updated Successfully'
    success_url = reverse_lazy('hr:vendor_list')



class VendorObjectMixin(object):
    model = Vendor
    def get_object(self):
        id = self.kwargs.get('id')
        obj = None
        if id is not None:
            obj = get_object_or_404(self.model, id=id)
        return obj 


class VendorDeleteView(LoginRequiredMixin, VendorObjectMixin, View):
    template_name = "hr/vendor_delete.html" # DetailView
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
            return redirect('hr:vendor_list')
        return render(request, self.template_name, context)


class CategoryListView(LoginRequiredMixin, ListView):
    template_name = "hr/category_list.html"
    context_object_name = 'object'
    

    def get_queryset(self):
        return Category.objects.all()
        
    def get_context_data(self, **kwargs):
        obj = super(CategoryListView, self).get_context_data(**kwargs)
        obj['category_list_qs'] = Category.objects.order_by('-added_on')
        return obj

class CategoryCreateView(LoginRequiredMixin, PassRequestMixin, SuccessMessageMixin, CreateView):
    template_name = 'hr/add_category.html'
    form_class = CategoryModelForm
    success_message = 'Category Added Successfully.'

    success_url = reverse_lazy('hr:category_list')


class CategoryDetailView(LoginRequiredMixin, DetailView):
    template_name = "hr/category_detail.html"
    model = Category


class CategoryUpdateView(LoginRequiredMixin, PassRequestMixin, SuccessMessageMixin, UpdateView):
    model = Category
    template_name = 'hr/update_category.html'
    form_class = CategoryModelForm
    success_message = 'Category Updated Successfully'
    success_url = reverse_lazy('hr:category_list')



class CategoryObjectMixin(object):
    model = Category
    def get_object(self):
        id = self.kwargs.get('id')
        obj = None
        if id is not None:
            obj = get_object_or_404(self.model, id=id)
        return obj 


class CategoryDeleteView(LoginRequiredMixin, CategoryObjectMixin, View):
    template_name = "hr/category_delete.html" # DetailView
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
            return redirect('hr:category_list')
        return render(request, self.template_name, context)

class CourseListView(LoginRequiredMixin, ListView):
    template_name = "hr/course_list.html"
    context_object_name = 'object'
    

    def get_queryset(self):
        return Course.objects.all()
        
    def get_context_data(self, **kwargs):
        obj = super(CourseListView, self).get_context_data(**kwargs)
        obj['course_list_qs'] = Course.objects.order_by('-date_added')
        return obj

class CourseCreateView(LoginRequiredMixin, PassRequestMixin, SuccessMessageMixin, CreateView):
    template_name = 'hr/add_course.html'
    form_class = CourseModelForm
    success_message = 'Course Created Successfully.'

    success_url = reverse_lazy('hr:course_list')

class CourseDetailView(LoginRequiredMixin, DetailView):
    template_name = "hr/course_detail.html"
    model = Course


class CourseUpdateView(LoginRequiredMixin, PassRequestMixin, SuccessMessageMixin, UpdateView):
    model = Course
    template_name = 'hr/update_course.html'
    form_class = CourseModelForm
    success_message = 'Course Updated Successfully'
    success_url = reverse_lazy('hr:course_list')



class CourseObjectMixin(object):
    model = Course
    def get_object(self):
        id = self.kwargs.get('id')
        obj = None
        if id is not None:
            obj = get_object_or_404(self.model, id=id)
        return obj 


class CourseDeleteView(LoginRequiredMixin, CourseObjectMixin, View):
    template_name = "hr/course_delete.html" # DetailView
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
            return redirect('hr:course_list')
        return render(request, self.template_name, context)

class TrainingListView(LoginRequiredMixin, ListView):
    template_name = "hr/training_list.html"
    context_object_name = 'object'
    

    def get_queryset(self):
        return Training.objects.all()
        
    def get_context_data(self, **kwargs):
        obj = super(TrainingListView, self).get_context_data(**kwargs)
        obj['training_list_qs'] = Training.objects.filter(training_status="Scheduled")
        return obj

class TrainingCreateView(LoginRequiredMixin, CourseObjectMixin, PassRequestMixin, SuccessMessageMixin, CreateView):
    template_name = 'hr/add_training.html'
    form_class = TrainingModelForm
    success_message = 'Training Created Successfully.'
    success_url = reverse_lazy('hr:training_list')


    def get_context_data(self, *args, **kwargs):
        context = super(TrainingCreateView, self).get_context_data(**kwargs)
        context = {}
        obj = self.get_object()
        if obj is not None:
            form = TrainingModelForm(instance=obj)
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


class TrainingDetailView(LoginRequiredMixin, DetailView):
    template_name = "hr/training_detail.html"
    model = Training

    


class TrainingUpdateView(LoginRequiredMixin, PassRequestMixin, SuccessMessageMixin, UpdateView):
    model = Training
    template_name = 'hr/update_training.html'
    form_class = TrainingModelForm
    success_message = 'Training Updated Successfully'
    success_url = reverse_lazy('hr:training_list')



class TrainingObjectMixin(object):
    model = Training
    def get_object(self):
        id = self.kwargs.get('id')
        obj = None
        if id is not None:
            obj = get_object_or_404(self.model, id=id)
        return obj 


class TrainingDeleteView(LoginRequiredMixin, TrainingObjectMixin, View):
    template_name = "hr/training_delete.html" # DetailView
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
            return redirect('hr:training_list')
        return render(request, self.template_name, context)


class AppraisalListView(LoginRequiredMixin, ListView):
    template_name = "hr/appraisal_list.html"
    context_object_name = 'object'
  
    def get_queryset(self):
        return Appraisal.objects.all()
        
    def get_context_data(self, **kwargs):
        obj = super(AppraisalListView, self).get_context_data(**kwargs)
        obj['appraisal_list_qs'] = Appraisal.objects.order_by('-added_on')
        return obj

class AppraisalCreateView(LoginRequiredMixin, PassRequestMixin, SuccessMessageMixin, CreateView):
    template_name = 'hr/add_appraisal.html'
    form_class = AppraisalModelForm
    success_message = 'Appraisal Added Successfully.'

    success_url = reverse_lazy('hr:appraisal_list')


class AppraisalDetailView(LoginRequiredMixin, DetailView):
    template_name = "hr/appraisal_detail.html"
    model = Appraisal


class AppraisalUpdateView(LoginRequiredMixin, PassRequestMixin, SuccessMessageMixin, UpdateView):
    model = Appraisal
    template_name = 'hr/update_appraisal.html'
    form_class = AppraisalModelForm
    success_message = 'Appraisal Updated Successfully'
    success_url = reverse_lazy('hr:appraisal_list')



class AppraisalObjectMixin(object):
    model = Appraisal
    def get_object(self):
        id = self.kwargs.get('id')
        obj = None
        if id is not None:
            obj = get_object_or_404(self.model, id=id)
        return obj 


class AppraisalDeleteView(LoginRequiredMixin, AppraisalObjectMixin, View):
    template_name = "hr/appraisal_delete.html" # DetailView
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
            return redirect('hr:appraisal_list')
        return render(request, self.template_name, context)


class ScheduleListView(LoginRequiredMixin, ListView):
    template_name = "hr/schedule_list.html"
    context_object_name = 'object'
  
    def get_queryset(self):
        return Schedule.objects.all()
        
    def get_context_data(self, **kwargs):
        obj = super(ScheduleListView, self).get_context_data(**kwargs)
        obj['schedule_list_qs'] = Schedule.objects.filter(appraisal_status="Scheduled")
        return obj

class ScheduleCreateView(LoginRequiredMixin, PassRequestMixin, SuccessMessageMixin, CreateView):
    template_name = 'hr/add_schedule.html'
    form_class = ScheduleModelForm
    success_message = 'Schedule Added Successfully.'

    success_url = reverse_lazy('hr:schedule_list')


class ScheduleDetailView(LoginRequiredMixin, DetailView):
    template_name = "hr/schedule_detail.html"
    model = Schedule


class ScheduleUpdateView(LoginRequiredMixin, PassRequestMixin, SuccessMessageMixin, UpdateView):
    model = Schedule
    template_name = 'hr/update_schedule.html'
    form_class = ScheduleModelForm
    success_message = 'Schedule Updated Successfully'
    success_url = reverse_lazy('hr:schedule_list')



class ScheduleObjectMixin(object):
    model = Schedule
    def get_object(self):
        id = self.kwargs.get('id')
        obj = None
        if id is not None:
            obj = get_object_or_404(self.model, id=id)
        return obj 


class ScheduleDeleteView(LoginRequiredMixin, ScheduleObjectMixin, View):
    template_name = "hr/schedule_delete.html" # DetailView
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
            return redirect('hr:schedule_list')
        return render(request, self.template_name, context)


class PerformanceListView(LoginRequiredMixin, ListView):
    template_name = "hr/performance_list.html"
    context_object_name = 'object'
  
    def get_queryset(self):
        return Performance.objects.all()
        
    def get_context_data(self, **kwargs):
        obj = super(PerformanceListView, self).get_context_data(**kwargs)
        obj['performance_list_qs'] = Performance.objects.filter(appraisal_status="Appraised")
        return obj


class PerformanceCreateView(LoginRequiredMixin, ScheduleObjectMixin, PassRequestMixin, SuccessMessageMixin, CreateView):
    template_name = 'hr/add_performance_evaluation.html'
    form_class = PerformanceEvaluationModelForm
    success_message = 'Performance Evaluation Concluded'
    success_url = reverse_lazy('hr:performance_list') 

    def get_context_data(self, *args, **kwargs):
        context = super(PerformanceCreateView, self).get_context_data(**kwargs)
        context = {}
        obj = self.get_object()
        if obj is not None:
            form = PerformanceEvaluationModelForm(instance=obj)
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


class PerformanceDetailView(LoginRequiredMixin, DetailView):
    template_name = "hr/performance_detail.html"
    model = Performance


class PerformanceObjectMixin(object):
    model = Performance
    def get_object(self):
        id = self.kwargs.get('id')
        obj = None
        if id is not None:
            obj = get_object_or_404(self.model, id=id)
        return obj 

class PerformanceUpdateView(LoginRequiredMixin, PassRequestMixin, SuccessMessageMixin, UpdateView):
    model = Performance
    template_name = 'hr/update_performance.html'
    form_class = PerformanceEvaluationModelForm
    success_message = 'Performance Updated Successfully'
    success_url = reverse_lazy('hr:performance_list')



class PerformanceDeleteView(LoginRequiredMixin, PerformanceObjectMixin, View):
    template_name = "hr/performance_delete.html" # DetailView
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
            return redirect('hr:performance_list')
        return render(request, self.template_name, context)




class DisciplineListView(LoginRequiredMixin, ListView):
    template_name = "hr/discipline_list.html"
    context_object_name = 'object'
  
    def get_queryset(self):
        return Discipline.objects.order_by('-assigned_on')
        
    def get_context_data(self, **kwargs):
        obj = super(DisciplineListView, self).get_context_data(**kwargs)
        obj['discipline_list_qs'] = Discipline.objects.filter(case_status="In Progress")
        return obj

class DisciplineCreateView(LoginRequiredMixin, PassRequestMixin, SuccessMessageMixin, CreateView):
    template_name = 'hr/add_discipline.html'
    form_class = DisciplineModelForm
    success_message = 'Discipline Added Successfully.'

    success_url = reverse_lazy('hr:discipline_list')


class DisciplineDetailView(LoginRequiredMixin, DetailView):
    template_name = "hr/discipline_detail.html"
    model = Discipline


class DisciplineUpdateView(LoginRequiredMixin, PassRequestMixin, SuccessMessageMixin, UpdateView):
    model = Discipline
    template_name = 'hr/update_discipline.html'
    form_class = DisciplineModelForm
    success_message = 'Discipline Updated Successfully'
    success_url = reverse_lazy('hr:discipline_list')



class DisciplineObjectMixin(object):
    model = Discipline
    def get_object(self):
        id = self.kwargs.get('id')
        obj = None
        if id is not None:
            obj = get_object_or_404(self.model, id=id)
        return obj 


class DisciplineDeleteView(LoginRequiredMixin, DisciplineObjectMixin, View):
    template_name = "hr/discipline_delete.html" # DetailView
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
            return redirect('hr:discipline_list')
        return render(request, self.template_name, context)


class ComplianceListView(LoginRequiredMixin, ListView):
    template_name = "hr/compliance_list.html"
    context_object_name = 'object'
  
    def get_queryset(self):
        return Compliance.objects.order_by('-closed_on')
        
    def get_context_data(self, **kwargs):
        obj = super(ComplianceListView, self).get_context_data(**kwargs)
        obj['compliance_list_qs'] = Compliance.objects.filter(case_status="Completed")
        return obj


class ComplianceCreateView(LoginRequiredMixin, DisciplineObjectMixin, PassRequestMixin, SuccessMessageMixin, CreateView):
    template_name = 'hr/add_compliance.html'
    form_class = ComplianceModelForm
    success_message = 'Compliance Records Entered Successfully'
    success_url = reverse_lazy('hr:compliance_list') 

    def get_context_data(self, *args, **kwargs):
        context = super(ComplianceCreateView, self).get_context_data(**kwargs)
        context = {}
        obj = self.get_object()
        if obj is not None:
            form = ComplianceModelForm(instance=obj)
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


class ComplianceDetailView(LoginRequiredMixin, DetailView):
    template_name = "hr/compliance_detail.html"
    model = Compliance


class ComplianceObjectMixin(object):
    model = Compliance
    def get_object(self):
        id = self.kwargs.get('id')
        obj = None
        if id is not None:
            obj = get_object_or_404(self.model, id=id)
        return obj 

class ComplianceUpdateView(LoginRequiredMixin, PassRequestMixin, SuccessMessageMixin, UpdateView):
    model = Compliance
    template_name = 'hr/update_compliance.html'
    form_class = ComplianceModelForm
    success_message = 'Compliance Updated Successfully'
    success_url = reverse_lazy('hr:compliance_list')



class ComplianceDeleteView(LoginRequiredMixin, ComplianceObjectMixin, View):
    template_name = "hr/compliance_delete.html" # DetailView
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
            return redirect('hr:compliance_list')
        return render(request, self.template_name, context)
