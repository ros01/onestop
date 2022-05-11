from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views import View
from django.views.generic import (
     CreateView,
     DetailView,
     ListView,
     UpdateView,
     DeleteView,
     TemplateView
)
from .forms import RequisitionModelForm, OrderModelForm, VehicleFilterForm, StaffProfileModelForm, LeaveRequestModelForm
from bootstrap_modal_forms.generic import BSModalCreateView
from .models import  Request
from store.models import *
from fleet.models import Assign, Vehicle
from hr.models import Employee, Leave, Specify, Document, Training, Record, Appraisal, Schedule, Performance, Discipline, Compliance
from django.contrib.messages.views import SuccessMessageMixin
from bootstrap_modal_forms.mixins import PassRequestMixin, CreateUpdateAjaxMixin
from django.contrib.auth.models import User
from django.conf import settings
from django_filters import FilterSet, CharFilter, NumberFilter
from django.core.exceptions import ImproperlyConfigured
from .filters import VehicleFilter
from django.contrib import messages
from .choices import location_choices, trip_choices
from django.db.models import Q, Count, F, Value
from django.core.exceptions import ObjectDoesNotExist
import datetime
from django.http import JsonResponse



# Create your views here.


class LoginRequiredMixin(object):
    @classmethod
    def as_view(cls, **kwargs):
        view = super(LoginRequiredMixin, cls).as_view(**kwargs)
        return login_required(view)

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        
        return super(LoginRequiredMixin, self).dispatch(request, *args, **kwargs)



class DashboardTemplateView(LoginRequiredMixin, TemplateView):
    template_name = "rrbnstaff/staff_dashboard2.html"
    
    def get_context_data(self, *args, **kwargs):
        context = super(DashboardTemplateView, self).get_context_data(*args, **kwargs)
        this_month = (datetime.datetime.now() + datetime.timedelta(days=30))
        context['res'] = Requisition.objects.filter(requesting_staff=self.request.user)
        context['resmnth'] = Requisition.objects.filter(requesting_staff=self.request.user, requisition_date__lt=this_month)
        context['res_pend'] = Requisition.objects.filter(requesting_staff=self.request.user, requisition_status=1)
        context['res_pend_mnth'] = Requisition.objects.filter(requesting_staff=self.request.user, requisition_date__lt=this_month, requisition_status=1)
        context['req'] = Request.objects.filter(requesting_staff=self.request.user)
        context['reqmnth'] = Request.objects.filter(requesting_staff=self.request.user, request_date__lt=this_month)
        context['req_pend'] = Request.objects.filter(requesting_staff=self.request.user, request_status=1)
        context['req_pend_mnth'] = Request.objects.filter(requesting_staff=self.request.user, request_date__lt=this_month, request_status=1)
        
        return context


class ProfileTemplateView(LoginRequiredMixin, TemplateView):
    template_name = "rrbnstaff/edit_profile.html"
    
    def get_context_data(self, *args, **kwargs):
        context = super(ProfileTemplateView, self).get_context_data(*args, **kwargs)
        #context["inspection"] = Schedule.objects.all()
        return context

class TableTemplateView(TemplateView):
    template_name = "rrbnstaff/table_list.html"
    
    def get_context_data(self, *args, **kwargs):
        context = super(TableTemplateView, self).get_context_data(*args, **kwargs)
        #context["inspection"] = Schedule.objects.all()
        return context

class DashboardListView(ListView):
    template_name = "rrbnstaff/requisition_dashboard.html"
    context_object_name = 'object'

    def get_queryset(self):
        return Requisition.objects.all()
        

    def get_context_data(self, **kwargs):
        obj = super(DashboardListView, self).get_context_data(**kwargs)
        obj['request_qs'] = Requisition.objects.order_by('-requisition_date')
        return obj

@login_required
def list_vehicles(request):
    vehicle_list = Vehicle.objects.filter(trip_status=1)
    vehicle_filter = VehicleFilter(request.GET, queryset=vehicle_list)
    return render(request, 'rrbnstaff/list_vehicles.html', {'filter': vehicle_filter})

def is_valid_queryparam(param):
    return param != '' and param is not None

@login_required
def search_vehicles(request):
    qs = Vehicle.objects.filter(trip_status=1)
    location = request.GET.get('location')
    interstate_trip = request.GET.get('interstate_trip')
   
    if is_valid_queryparam(location):
        qs = qs.filter(location__iexact=location)


    if is_valid_queryparam(interstate_trip) and interstate_trip == 'interstate':
        qs = qs.filter(interstate_trip__iexact=interstate_trip)


    if is_valid_queryparam(interstate_trip) and interstate_trip == 'local':
        qs = qs.filter(location__iexact=location, trip_status=1)

    context = {
        'queryset': qs,
        'location_choices': location_choices,
        'trip_choices': trip_choices,
        'values': request.GET,
        
    }
    return render(request, 'rrbnstaff/search_vehicles2.html', context)

@login_required
def FindVehicleView(request):
    qs = Vehicle.objects.filter(trip_status=1)
    location = request.GET.get('location')
    interstate_trip = request.GET.get('interstate_trip')

    if is_valid_queryparam(location):
        qs = qs.filter(location__iexact=location)


    if is_valid_queryparam(interstate_trip) and interstate_trip == 'interstate':
        qs = qs.filter(interstate_trip__iexact=interstate_trip)


    if is_valid_queryparam(interstate_trip) and interstate_trip == 'local':
        qs = qs.filter(location__iexact=location, trip_status=1)

    context = {
        'queryset': qs,
        'location_choices': location_choices,
        'trip_choices': trip_choices,
        'values': request.GET,
        
    }
    return render(request, "rrbnstaff/find_vehicle.html", context)


@login_required
def retrieve_item(request):
    qs = Item.objects.all()
    item_name = request.GET.get('item_name')

    if is_valid_queryparam(item_name):
        qs = qs.filter(item_name__iexact=item_name)


    context = {
        'queryset': qs,
    }
    return render(request, 'rrbnstaff/retrieve_item.html', context)


@login_required
def find_item(request):
    qs = Item.objects.all()
    query = request.GET.get('q')
    qs = qs.filter(item_name__icontains=query)
    context = {
        'queryset': qs,
    }
    return render(request, 'rrbnstaff/item_results.html', context)

class VehiclesFilter(FilterSet):
    location = CharFilter(name='location', lookup_type='icontains', distinct=True)
    trip_type = CharFilter(name='trip_type', lookup_type='icontains', distinct=True)
   
    
    class Meta:
        model = Vehicle
        fields = [
            'location',
            'trip_type',   
        ]


class VehicleObjectMixin(object):
    model = Vehicle
    def get_object(self):
        id = self.kwargs.get('id')
        obj = None
        if id is not None:
            obj = get_object_or_404(self.model, id=id)
        return obj 


class ItemObjectMixin(object):
    model = Item
    def get_object(self):
        id = self.kwargs.get('id')
        obj = None
        if id is not None:
            obj = get_object_or_404(self.model, id=id)
        return obj


class RequisitionsListView(LoginRequiredMixin, ListView):
    template_name = "rrbnstaff/requisition_list2.html"
    context_object_name = 'object'

    def get_queryset(self):
        return Requisition.objects.all()
        

    def get_context_data(self, **kwargs):
        obj = super(RequisitionsListView, self).get_context_data(**kwargs)
        obj['requisition_qs'] = Requisition.objects.filter(requisition_status=1, requesting_staff=self.request.user)
        return obj


class RequisitionCreateView(LoginRequiredMixin, ItemObjectMixin, PassRequestMixin, SuccessMessageMixin, CreateView):
    template_name = 'rrbnstaff/create_requisition.html'
    form_class = RequisitionModelForm
    success_message = 'Requisition created successfully'
    success_url = reverse_lazy('rrbnstaff:requisition_list') 

    def get_context_data(self, *args, **kwargs):
        context = super(RequisitionCreateView, self).get_context_data(**kwargs)
        context = {}
        obj = self.get_object()
        if obj is not None:
            form = RequisitionModelForm(instance=obj)
            context['object'] = obj  
            context['form'] = form
        return context   
   
    #def form_invalid(self, form):
        #form = self.get_form()

        #context = {}
        #obj = self.get_object()
        #if obj is not None:
          
           #context['object'] = obj
           #context['form'] = form 
          
        #return self.render_to_response(context)


    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data())

      
 
class RequisitionObjectMixin(object):
    model = Requisition
    def get_object(self):
        id = self.kwargs.get('id')
        obj = None
        if id is not None:
            obj = get_object_or_404(self.model, id=id)
        return obj 

class RequestObjectMixin(object):
    model = Request
    def get_object(self):
        id = self.kwargs.get('id')
        obj = None
        if id is not None:
            obj = get_object_or_404(self.model, id=id)
        return obj 


#class RequisitionCreateView(LoginRequiredMixin, PassRequestMixin, SuccessMessageMixin, CreateView):
    #template_name = 'rrbnstaff/create_requisition.html'
    #form_class = RequisitionModelForm
    #success_message = 'Requisition created successfully.'
    #success_url = reverse_lazy('rrbnstaff:requisition_list') 

#class CreateVehicleRequest(PassRequestMixin, SuccessMessageMixin, CreateView):
    #template_name = 'rrbnstaff/create_vehicle_request.html'
    #form_class = RequestModelForm
    #success_message = 'Vehicle Request created successfully.'
    #success_url = reverse_lazy('rrbnstaff:request_list') 

class RequisitionDetailView(LoginRequiredMixin, RequisitionObjectMixin, View):
    template_name = "rrbnstaff/requisition_detail.html"

    def get(self, request, id=None, *args, **kwargs):
        context = {'object': self.get_object()}
        return render(request, self.template_name, context)

class RequisitionUpdateView(LoginRequiredMixin, PassRequestMixin, SuccessMessageMixin, UpdateView):
    model = Requisition
    template_name = 'rrbnstaff/requisition_update.html'
    form_class = RequisitionModelForm
    success_message = 'Requisition updated Successfully'
    success_url = reverse_lazy('rrbnstaff:requisition_list')


class RequisitionDeleteView(LoginRequiredMixin, RequisitionObjectMixin, View):
    template_name = "rrbnstaff/requisition_delete.html" # DetailView
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
            return redirect('rrbnstaff:requisition_list')
        return render(request, self.template_name, context)

class MyIssuedRequisitions(LoginRequiredMixin, ListView):
    template_name = "rrbnstaff/my_issued_requisitions.html"
    context_object_name = 'object'

    def get_queryset(self):
        return Issue.objects.all()
        

    def get_context_data(self, **kwargs):
        obj = super(MyIssuedRequisitions, self).get_context_data(**kwargs)
        obj['issue_qs'] = Issue.objects.filter(requesting_staff=self.request.user)
        return obj 

class MyIssuedRequisitionsDetails(LoginRequiredMixin, DetailView):
    template_name = "rrbnstaff/my_issued_requisitions_details.html"
    model = IssueRequisition 


class RequestListView(LoginRequiredMixin, ListView):
    template_name = "rrbnstaff/request_list.html"
    context_object_name = 'object'

    def get_queryset(self):
        return Request.objects.all()
        
    def get_context_data(self, **kwargs):
        obj = super(RequestListView, self).get_context_data(**kwargs)
        obj['request_qs'] = Request.objects.filter(request_status=1, requesting_staff=self.request.user)
        return obj

class CreateVehicleRequest(LoginRequiredMixin, VehicleObjectMixin, PassRequestMixin, SuccessMessageMixin, CreateView):
    template_name = 'rrbnstaff/create_vehicle_request.html'
    form_class = OrderModelForm
    success_message = 'Vehicle Request created successfully.'
    success_url = reverse_lazy('rrbnstaff:request_list') 

    def get_context_data(self, *args, **kwargs):
        context = super(CreateVehicleRequest, self).get_context_data(**kwargs)
        context = {}
        obj = self.get_object()
        if obj is not None:
            form = OrderModelForm(instance=obj)
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

class VehicleRequestDetailView(LoginRequiredMixin, DetailView):
    template_name = "rrbnstaff/vehicle_request_detail.html"
    model = Request


class VehicleRequestUpdateView(LoginRequiredMixin, PassRequestMixin, SuccessMessageMixin, UpdateView):
    model = Request
    template_name = 'rrbnstaff/update_vehicle_request.html'
    form_class = OrderModelForm
    success_message = 'Vehicle Request updated Successfully'
    success_url = reverse_lazy('rrbnstaff:request_list')


class VehicleRequestDeleteView(LoginRequiredMixin, RequestObjectMixin, View):
    template_name = "rrbnstaff/vehicle_request_delete.html" # DetailView
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
            return redirect('rrbnstaff:request_list')
        return render(request, self.template_name, context)


class MyVehicleAllocations(LoginRequiredMixin, ListView):
    template_name = "rrbnstaff/my_vehicle_allocations.html"
    context_object_name = 'object'

    def get_queryset(self):
        return Assign.objects.all()
        
    def get_context_data(self, **kwargs):
        obj = super(MyVehicleAllocations, self).get_context_data(**kwargs)
        obj['assign_qs'] = Assign.objects.filter(requesting_staff=self.request.user)
        return obj 

class AssignedVehicleDetails(LoginRequiredMixin, DetailView):
    template_name = "rrbnstaff/assigned_vehicle_details.html"
    model = Assign

class StaffProfileCreateView(LoginRequiredMixin, PassRequestMixin, SuccessMessageMixin, CreateView):
    template_name = 'rrbnstaff/create_staff_profile.html'
    form_class = StaffProfileModelForm
    success_message = 'Staff Profile Created Successfully.'
    success_url = reverse_lazy('rrbnstaff:my_profile_list')
    
class MyProfileListView(LoginRequiredMixin, ListView):
    template_name = "rrbnstaff/my_profile_list.html"
    context_object_name = 'object'

    def get_queryset(self):
        return Employee.objects.all()
        

    def get_context_data(self, **kwargs):
        obj = super(MyProfileListView, self).get_context_data(**kwargs)
        obj['my_profile_qs'] = Employee.objects.filter(employee=self.request.user)
        return obj    

class MyProfileDetailView(LoginRequiredMixin, DetailView):
    template_name = "rrbnstaff/my_profile_detail.html"
    model = Employee


class MyProfileUpdateView(LoginRequiredMixin, PassRequestMixin, SuccessMessageMixin, UpdateView):
    model = Employee
    template_name = 'rrbnstaff/update_staff_profile.html'
    form_class = StaffProfileModelForm
    success_message = 'Profile Updated Successfully'
    success_url = reverse_lazy('rrbnstaff:my_profile_list')

class ProfileObjectMixin(object):
    model = Employee
    def get_object(self):
        id = self.kwargs.get('id')
        obj = None
        if id is not None:
            obj = get_object_or_404(self.model, id=id)
        return obj 


class MyProfileDeleteView(LoginRequiredMixin, ProfileObjectMixin, View):
    template_name = "rrbnstaff/my_profile_delete.html" # DetailView
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
            return redirect('rrbnstaff:my_profile_list')
        return render(request, self.template_name, context)


class MyLeaveRequestListView(LoginRequiredMixin, ListView):
    template_name = "rrbnstaff/my_leave_request_list.html"
    context_object_name = 'object'
    

    def get_queryset(self):
        return Leave.objects.all()
        
    def get_context_data(self, **kwargs):
        obj = super(MyLeaveRequestListView, self).get_context_data(**kwargs)
        obj['leave_requests_qs'] = Leave.objects.filter(leave_status="Pending Approval", staff_name=self.request.user)
        return obj

class LeaveRequestCreateView(LoginRequiredMixin, PassRequestMixin, SuccessMessageMixin, CreateView):
    template_name = 'rrbnstaff/create_leave_request.html'
    form_class = LeaveRequestModelForm
    success_message = 'Leave Request Created Successfully'

    success_url = reverse_lazy('rrbnstaff:my_leave_requests_list')

class LeaveRequestDetailView(LoginRequiredMixin, DetailView):
    template_name = "rrbnstaff/leave_request_detail.html"
    model = Leave


class LeaveRequestUpdateView(LoginRequiredMixin, PassRequestMixin, SuccessMessageMixin, UpdateView):
    model = Leave
    template_name = 'rrbnstaff/update_leave_request.html'
    form_class = LeaveRequestModelForm
    success_message = 'Leave Request Updated Successfully'
    success_url = reverse_lazy('rrbnstaff:my_leave_requests_list')


class LeaveObjectMixin(object):
    model = Leave
    def get_object(self):
        id = self.kwargs.get('id')
        obj = None
        if id is not None:
            obj = get_object_or_404(self.model, id=id)
        return obj 

class LeaveRequestDeleteView(LoginRequiredMixin, LeaveObjectMixin, View):
    template_name = "rrbnstaff/leave_request_delete.html" # DetailView
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
            return redirect('rrbnstaff:my_leave_requests_list')
        return render(request, self.template_name, context)

class MyApprovedLeaves(LoginRequiredMixin, ListView):
    template_name = "rrbnstaff/my_approved_leaves.html"
    context_object_name = 'object'
    
    def get_queryset(self):
        return Leave.objects.order_by('-leave_application_date')
        
    def get_context_data(self, **kwargs):
        obj = super(MyApprovedLeaves, self).get_context_data(**kwargs)
        obj['approved_leaves_qs'] = Leave.objects.filter(leave_status="Approved", staff_name=self.request.user)
        return obj

class MyAssignedLeaves(LoginRequiredMixin, ListView):
    template_name = "rrbnstaff/my_assigned_leaves.html"
    context_object_name = 'object'
    
    def get_queryset(self):
        return Leave.objects.order_by('-leave_application_date')
        
    def get_context_data(self, **kwargs):
        obj = super(MyAssignedLeaves, self).get_context_data(**kwargs)
        obj['assigned_leaves_qs'] = Specify.objects.filter(leave_status="Leave Days Assigned", staff_name=self.request.user)
        return obj

class MyLeaveHistory(LoginRequiredMixin, ListView):
    template_name = "rrbnstaff/my_leave_history.html"
    context_object_name = 'object'
    
    def get_queryset(self):
        return Leave.objects.order_by('-leave_application_date')
        
    def get_context_data(self, **kwargs):
        obj = super(MyLeaveHistory, self).get_context_data(**kwargs)
        obj['leave_history_qs'] = Document.objects.filter(leave_status="Leave Completed", staff_name=self.request.user)
        return obj


class LeaveApprovalDetailView(LoginRequiredMixin, DetailView):
    template_name = "rrbnstaff/leave_approval_detail.html"
    model = Leave

class LeaveAssignmentDetailView(LoginRequiredMixin, DetailView):
    template_name = "rrbnstaff/leave_assignment_detail.html"
    model = Specify

class LeaveHistoryDetailView(LoginRequiredMixin, DetailView):
    template_name = "rrbnstaff/leave_history_detail.html"
    model = Document


class MyScheduledTrainings(LoginRequiredMixin, ListView):
    template_name = "rrbnstaff/my_programs_list.html"
    context_object_name = 'object'
  
    def get_queryset(self):
        return Training.objects.order_by('-date_added')
        
    def get_context_data(self, **kwargs):
        obj = super(MyScheduledTrainings, self).get_context_data(**kwargs)
        obj['my_training_list_qs'] = Training.objects.filter(staff_name=self.request.user)
        return obj

class MyScheduledTrainingsDetails(LoginRequiredMixin, DetailView):
    template_name = "rrbnstaff/my_training_details.html"
    model = Training

class MyPromotionInterviewListView(LoginRequiredMixin, ListView):
    template_name = "rrbnstaff/my_scheduled_promotion_interviews.html"
    context_object_name = 'object'
  
    def get_queryset(self):
        return Schedule.objects.all()
        
    def get_context_data(self, **kwargs):
        obj = super(MyPromotionInterviewListView, self).get_context_data(**kwargs)
        obj['my_schedule_list_qs'] = Schedule.objects.filter(staff_name=self.request.user, appraisal_status="Scheduled")
        return obj


class MyPromotionInterviewDetailView(LoginRequiredMixin, DetailView):
    template_name = "rrbnstaff/my_scheduled_interview_details.html"
    model = Schedule

class MyPerformanceEvaluationListView(LoginRequiredMixin, ListView):
    template_name = "rrbnstaff/my_performance_evaluations_list.html"
    context_object_name = 'object'
  
    def get_queryset(self):
        return Performance.objects.all()
        
    def get_context_data(self, **kwargs):
        obj = super(MyPerformanceEvaluationListView, self).get_context_data(**kwargs)
        obj['my_performance_list_qs'] = Performance.objects.filter(staff_name=self.request.user, appraisal_status="Appraised")
        return obj


class MyPerformanceEvaluationDetailView(LoginRequiredMixin, DetailView):
    template_name = "rrbnstaff/my_performance_evaluation_details.html"
    model = Performance

class ReprisalListView(LoginRequiredMixin, ListView):
    template_name = "rrbnstaff/my_reprisal_list.html"
    context_object_name = 'object'
  
    def get_queryset(self):
        return Discipline.objects.all()
        
    def get_context_data(self, **kwargs):
        obj = super(ReprisalListView, self).get_context_data(**kwargs)
        obj['repraisal_list_qs'] = Discipline.objects.filter(staff_name=self.request.user, case_status="In Progress")
        return obj

class ReprisalDetailView(LoginRequiredMixin, DetailView):
    template_name = "rrbnstaff/my_reprisal_details.html"
    model = Discipline

class RestitutionListView(LoginRequiredMixin, ListView):
    template_name = "rrbnstaff/restitution_list.html"
    context_object_name = 'object'
  
    def get_queryset(self):
        return Compliance.objects.all()
        
    def get_context_data(self, **kwargs):
        obj = super(RestitutionListView, self).get_context_data(**kwargs)
        obj['restitution_list_qs'] = Compliance.objects.filter(staff_name=self.request.user, case_status="Completed")
        return obj

class RestitutionDetailView(LoginRequiredMixin, DetailView):
    template_name = "rrbnstaff/restitution_detail.html"
    model = Compliance

