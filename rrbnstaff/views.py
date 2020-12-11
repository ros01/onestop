from django.shortcuts import get_object_or_404, render, redirect
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
from .forms import RequisitionModelForm, RequestModelForm, VehicleFilterForm
from bootstrap_modal_forms.generic import BSModalCreateView
from .models import Requisition, Request
from store.models import Issue
from fleet.models import Assign
from fleet.models import Vehicle
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
        context['res'] = Requisition.objects.all()
        context['resmnth'] = Requisition.objects.filter(requisition_date__lt=this_month)
        context['res_pend'] = Requisition.objects.filter(requisition_status=1)
        context['res_pend_mnth'] = Requisition.objects.filter(requisition_date__lt=this_month, requisition_status=1)
        context['req'] = Request.objects.all()
        context['reqmnth'] = Request.objects.filter(request_date__lt=this_month)
        context['req_pend'] = Request.objects.filter(request_status=1)
        context['req_pend_mnth'] = Request.objects.filter(request_date__lt=this_month, request_status=1)
        
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


    if is_valid_queryparam(location):
        qs = qs.filter(location__iexact=location)


    if is_valid_queryparam(interstate_trip):
        qs = qs.filter(interstate_trip__iexact=interstate_trip)

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


    elif is_valid_queryparam(interstate_trip) and interstate_trip == 'local':
        qs = Vehicle.objects.filter(trip_status=1)

    context = {
        'queryset': qs,
        'location_choices': location_choices,
        'trip_choices': trip_choices,
        'values': request.GET,
        
    }
    return render(request, "rrbnstaff/find_vehicle.html", context)

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


class CreateVehicleRequest(LoginRequiredMixin, VehicleObjectMixin, PassRequestMixin, SuccessMessageMixin, CreateView):
    template_name = 'rrbnstaff/create_vehicle_request.html'
    template_name1 = 'rrbnstaff/vehicle_request_detail.html'
    def get(self, request,  *args, **kwargs):
        context = {}
        obj = self.get_object()
        if obj is not None:
            form = RequestModelForm(instance=obj)
            context['object'] = obj
            context['form'] = form

        return render(request, self.template_name, context)


    def post(self, request,  *args, **kwargs):
        
        form = RequestModelForm(request.POST)
        if form.is_valid():
            if not self.request.is_ajax() or self.request.POST.get('asyncUpdate') == 'True':
                form.save(commit=False)
            else:
                form.save(commit=True)
            
        context = {}

        obj = self.get_object()
        if obj is not None:
            form = RequestModelForm(instance=obj)
            context['object'] = obj
            context['form'] = form
            context['request'] = Request.objects.filter (vehicle_name=obj.vehicle_name, request_no= request.POST['request_no'])

        return render(request, self.template_name1, context)

class RequisitionCreateView(LoginRequiredMixin, PassRequestMixin, SuccessMessageMixin, CreateView):
    template_name = 'rrbnstaff/create_requisition.html'
    form_class = RequisitionModelForm
    success_message = 'Requisition created successfully.'
    success_url = reverse_lazy('rrbnstaff:requisition_list') 

#class CreateVehicleRequest(PassRequestMixin, SuccessMessageMixin, CreateView):
    #template_name = 'rrbnstaff/create_vehicle_request.html'
    #form_class = RequestModelForm
    #success_message = 'Vehicle Request created successfully.'
    #success_url = reverse_lazy('rrbnstaff:request_list') 


class RequisitionsListView(LoginRequiredMixin, ListView):
    template_name = "rrbnstaff/requisition_list2.html"
    context_object_name = 'object'

    def get_queryset(self):
        return Requisition.objects.all()
        

    def get_context_data(self, **kwargs):
        obj = super(RequisitionsListView, self).get_context_data(**kwargs)
        obj['requisition_qs'] = Requisition.objects.filter(requisition_status=1, requesting_staff=self.request.user)
        return obj


class RequestListView(LoginRequiredMixin, ListView):
    template_name = "rrbnstaff/request_list.html"
    context_object_name = 'object'

    def get_queryset(self):
        return Request.objects.all()
        

    def get_context_data(self, **kwargs):
        obj = super(RequestListView, self).get_context_data(**kwargs)
        obj['request_qs'] = Request.objects.filter(request_status=1, requesting_staff=self.request.user)
        return obj

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



class RequisitionDetailView(LoginRequiredMixin, RequisitionObjectMixin, View):
    template_name = "rrbnstaff/requisition_detail.html"

    def get(self, request, id=None, *args, **kwargs):
        context = {'object': self.get_object()}
        return render(request, self.template_name, context)


class VehicleRequestDetailView(LoginRequiredMixin, DetailView):
    template_name = "fleet/vehicle_detail.html"
    model = Request

class RequisitionUpdateView(LoginRequiredMixin, PassRequestMixin, SuccessMessageMixin, UpdateView):
    model = Requisition
    template_name = 'rrbnstaff/requisition_update.html'
    form_class = RequisitionModelForm
    success_message = 'Success: Requisition updated Successfully'
    success_url = reverse_lazy('rrbnstaff:requisition_list')



#class VehicleRequestUpdateView(PassRequestMixin, SuccessMessageMixin, UpdateView):
    #model = Request
    #template_name = 'rrbnstaff/update_vehicle_request.html'
    #form_class = RequestModelForm
    #success_message = 'Success: Vehicle Request updated Successfully'
    #success_url = reverse_lazy('rrbnstaff:request_list')


class VehicleRequestUpdateView(LoginRequiredMixin, RequestObjectMixin, View):
    template_name = "rrbnstaff/update_vehicle_request.html" 
    template_name1 = "rrbnstaff/vehicle_request_detail.html" 
    
    def get(self, request, id=None, *args, **kwargs):
        # GET method
        context = {}
        obj = self.get_object()
        if obj is not None:
            form = RequestModelForm(instance=obj)
            context['object'] = obj
            context['form'] = form
        return render(request, self.template_name, context)

    def post(self, request, id=None,  *args, **kwargs):
        # POST method
        context = {}
        obj = self.get_object()
        if obj is not None:
            form = RequestModelForm(request.POST or None, instance=obj)
            if form.is_valid():
                form.save()
            context['object'] = obj
            context['form'] = form
            context['request'] = Request.objects.filter (vehicle_name=obj.vehicle_name)
        messages.success(request, ('Vehicle Request Updated Successfully'))
        return render(request, self.template_name1, context)

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



class MyIssuedRequisitions(LoginRequiredMixin, ListView):
    template_name = "rrbnstaff/my_issued_requisitions.html"
    context_object_name = 'object'

    def get_queryset(self):
        return Issue.objects.all()
        

    def get_context_data(self, **kwargs):
        obj = super(MyIssuedRequisitions, self).get_context_data(**kwargs)
        obj['issue_qs'] = Issue.objects.filter(requesting_staff=self.request.user)
        return obj 


class MyVehicleAllocations(LoginRequiredMixin, ListView):
    template_name = "rrbnstaff/my_vehicle_allocations.html"
    context_object_name = 'object'

    def get_queryset(self):
        return Assign.objects.all()
        

    def get_context_data(self, **kwargs):
        obj = super(MyVehicleAllocations, self).get_context_data(**kwargs)
        obj['assign_qs'] = Assign.objects.filter(requesting_staff=self.request.user)
        return obj 


class MyIssuedRequisitionsDetails(LoginRequiredMixin, DetailView):
    template_name = "rrbnstaff/my_issued_requisitions_details.html"
    model = Issue 

class AssignedVehicleDetails(LoginRequiredMixin, DetailView):
    template_name = "rrbnstaff/assigned_vehicle_details.html"
    model = Assign



    




