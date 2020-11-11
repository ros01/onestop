from django.shortcuts import render

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
from .models import Station, Workshop, Category, Vehicle, Assign, Release, Fueling, Repair, Maintenance, Schedule
from rrbnstaff.models import Request

from .forms import WorkshopModelForm, StationModelForm, CategoryModelForm, VehicleModelForm, IssueVehicleRequestModelForm, FinalizeTripModelForm, FuelingModelForm, RepairsModelForm, ScheduleModelForm, RecordMaintenanceModelForm
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from bootstrap_modal_forms.generic import BSModalCreateView
from bootstrap_modal_forms.mixins import PassRequestMixin, CreateUpdateAjaxMixin
from django.urls import reverse, reverse_lazy
from django.contrib.auth.models import User
from django.conf import settings

# Create your views here.

class DashboardTemplateView(TemplateView):
    template_name = "fleet/fleet_dashboard.html"
    
    def get_context_data(self, *args, **kwargs):
        context = super(DashboardTemplateView, self).get_context_data(*args, **kwargs)
        #context["inspection"] = Schedule.objects.all()
        return context

class WorkshopCreateView(PassRequestMixin, SuccessMessageMixin, CreateView):
    template_name = 'fleet/create_workshop.html'
    form_class = WorkshopModelForm
    success_message = 'Workshop created Successfully.'

    success_url = reverse_lazy('fleet:workshop_list')


class StationCreateView(PassRequestMixin, SuccessMessageMixin, CreateView):
    template_name = 'fleet/create_station.html'
    form_class = StationModelForm
    success_message = 'Station created Successfully.'

    success_url = reverse_lazy('fleet:station_list')


class CategoryCreateView(PassRequestMixin, SuccessMessageMixin, CreateView):
    template_name = 'fleet/create_category.html'
    form_class = CategoryModelForm
    success_message = 'category created Successfully.'

    success_url = reverse_lazy('fleet:category_list')

class VehicleCreateView(PassRequestMixin, SuccessMessageMixin, CreateView):
    template_name = 'fleet/create_vehicle.html'
    form_class = VehicleModelForm
    success_message = 'Vehicle created Successfully.'

    success_url = reverse_lazy('fleet:vehicle_list')


class WorkshopListView(ListView):
    template_name = "fleet/workshop_list.html"
    context_object_name = 'object'

    def get_queryset(self):
        return Workshop.objects.all()
        

    def get_context_data(self, **kwargs):
        obj = super(WorkshopListView, self).get_context_data(**kwargs)
        obj['workshop_qs'] = Workshop.objects.order_by('-date_created')
        return obj


class StationListView(ListView):
    template_name = "fleet/station_list.html"
    context_object_name = 'object'

    def get_queryset(self):
        return Station.objects.all()
        

    def get_context_data(self, **kwargs):
        obj = super(StationListView, self).get_context_data(**kwargs)
        obj['station_qs'] = Station.objects.order_by('-date_created')
        return obj

class CategoryListView(ListView):
    template_name = "fleet/category_list.html"
    context_object_name = 'object'

    def get_queryset(self):
        return Category.objects.all()
        

    def get_context_data(self, **kwargs):
        obj = super(CategoryListView, self).get_context_data(**kwargs)
        obj['category_qs'] = Category.objects.order_by('-date_created')
        return obj

class VehicleListView(ListView):
    template_name = "fleet/vehicle_list.html"
    context_object_name = 'object'

    def get_queryset(self):
        return Vehicle.objects.all()
        

    def get_context_data(self, **kwargs):
        obj = super(VehicleListView, self).get_context_data(**kwargs)
        obj['vehicle_qs'] = Vehicle.objects.order_by('-date_created')
        return obj


class VehicleRequestList(ListView):
    template_name = "fleet/vehicle_request_list.html"
    context_object_name = 'object'

    def get_queryset(self):
        return Request.objects.order_by('-request_date')
        

    def get_context_data(self, **kwargs):
        obj = super(VehicleRequestList, self).get_context_data(**kwargs)
        obj['request_qs'] = Request.objects.filter(request_status=1)
        return obj



class WorkshopDetailView(DetailView):
    template_name = "fleet/workshop_detail.html"
    model = Workshop


class StationDetailView(DetailView):
    template_name = "fleet/station_detail.html"
    model = Station


class CategoryDetailView(DetailView):
    template_name = "fleet/category_detail.html"
    model = Category

class VehicleDetailView(DetailView):
    template_name = "fleet/vehicle_detail.html"
    model = Vehicle


#class VehicleRequestDetail(DetailView):
    #template_name = "fleet/vehicle_request_detail.html"
    #model = Request 




class RequestObjectMixin(object):
    model = Request
    def get_object(self):
        id = self.kwargs.get('id')
        obj = None
        if id is not None:
            obj = get_object_or_404(self.model, id=id)
        return obj 


class VehicleRequestDetail(RequestObjectMixin, View):
    template_name = "fleet/vehicle_request_detail.html" 
    def get(self, request, id=None, *args, **kwargs):
        context = {'object': self.get_object()}
        return render(request, self.template_name, context)


class WorkshopUpdateView(PassRequestMixin, SuccessMessageMixin, UpdateView):
    model = Workshop
    template_name = 'fleet/update_workshop.html'
    form_class = WorkshopModelForm
    success_message = 'Success: Workshop Details were updated.'
    success_url = reverse_lazy('fleet:workshop_list')

class StationUpdateView(PassRequestMixin, SuccessMessageMixin, UpdateView):
    model = Station
    template_name = 'fleet/update_station.html'
    form_class = StationModelForm
    success_message = 'Success: Station Details were updated.'
    success_url = reverse_lazy('fleet:station_list')


class CategoryUpdateView(PassRequestMixin, SuccessMessageMixin, UpdateView):
    model = Category
    template_name = 'fleet/update_category.html'
    form_class = CategoryModelForm
    success_message = 'Success: Category Details were updated.'
    success_url = reverse_lazy('fleet:category_list')

class VehicleUpdateView(PassRequestMixin, SuccessMessageMixin, UpdateView):
    model = Vehicle
    template_name = 'fleet/update_vehicle.html'
    form_class = VehicleModelForm
    success_message = 'Success: Vehicle Details were updated.'
    success_url = reverse_lazy('fleet:vehicle_list')



class WorkshopObjectMixin(object):
    model = Workshop
    def get_object(self):
        id = self.kwargs.get('id')
        obj = None
        if id is not None:
            obj = get_object_or_404(self.model, id=id)
        return obj 

class StationObjectMixin(object):
    model = Station
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


class VehicleObjectMixin(object):
    model = Vehicle
    def get_object(self):
        id = self.kwargs.get('id')
        obj = None
        if id is not None:
            obj = get_object_or_404(self.model, id=id)
        return obj 


class WorkshopDeleteView(WorkshopObjectMixin, View):
    template_name = "fleet/workshop_delete.html" # DetailView
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
            return redirect('fleet:workshop_list')
        return render(request, self.template_name, context)


class VehicleDeleteView(VehicleObjectMixin, View):
    template_name = "fleet/vehicle_delete.html" # DetailView
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
            return redirect('fleet:vehicle_list')
        return render(request, self.template_name, context)

class StationDeleteView(StationObjectMixin, View):
    template_name = "fleet/station_delete.html" # DetailView
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
            return redirect('fleet:station_list')
        return render(request, self.template_name, context)


class CategoryDeleteView(CategoryObjectMixin, View):
    template_name = "fleet/category_delete.html" # DetailView
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
            return redirect('fleet:category_list')
        return render(request, self.template_name, context)


class IssueVehicleRequest(RequestObjectMixin, PassRequestMixin, SuccessMessageMixin, CreateView):
    template_name = 'fleet/assign_vehicle.html'
    template_name1 = 'fleet/assigned_vehicle_details.html'
    def get(self, request,  *args, **kwargs):
        context = {}
        obj = self.get_object()
        if obj is not None:
            form = IssueVehicleRequestModelForm(instance=obj)
            context['object'] = obj
            context['form'] = form

        return render(request, self.template_name, context)


    def post(self, request,  *args, **kwargs):
        
        form = IssueVehicleRequestModelForm(request.POST)
        if form.is_valid():
            if not self.request.is_ajax() or self.request.POST.get('asyncUpdate') == 'True':
                form.save(commit=False)
            else:
                form.save(commit=True)
            
        context = {}

        obj = self.get_object()
        if obj is not None:
            form = IssueVehicleRequestModelForm(instance=obj)
            context['object'] = obj
            context['form'] = form
            context['issue'] = Assign.objects.filter (request_no=obj.request_no)

        return render(request, self.template_name1, context)

class AssignObjectMixin(object):
    model = Assign
    def get_object(self):
        id = self.kwargs.get('id')
        obj = None
        if id is not None:
            obj = get_object_or_404(self.model, id=id)
        return obj 

class UpdateVehicleAssignemt(AssignObjectMixin, View):
    template_name = "fleet/update_assign_vehicle.html" 
    template_name1 = "fleet/assigned_vehicle_details2.html" 
    
    def get(self, request, id=None, *args, **kwargs):
        # GET method
        context = {}
        obj = self.get_object()
        if obj is not None:
            form = IssueVehicleRequestModelForm(instance=obj)
            context['object'] = obj
            context['form'] = form
        return render(request, self.template_name, context)

    def post(self, request, id=None,  *args, **kwargs):
        # POST method
        context = {}
        obj = self.get_object()
        if obj is not None:
            form = IssueVehicleRequestModelForm(request.POST or None, instance=obj)
            if form.is_valid():
                form.save()
            context['object'] = obj
            context['form'] = form
            context['issue'] = Assign.objects.filter (request_no=obj.request_no)
        messages.success(request, ('Vehicle Assignment Update Successful'))
        return render(request, self.template_name1, context)


class VehicleAssignmentList(ListView):
    template_name = "fleet/assigned_vehicles_list.html"
    context_object_name = 'object'

    def get_queryset(self):
        return Assign.objects.all()
        

    def get_context_data(self, **kwargs):
        obj = super(VehicleAssignmentList, self).get_context_data(**kwargs)
        obj['vehicle_assignment_qs'] = Assign.objects.filter(trip_status="created")
        return obj





class VehicleAllocationsDetail(AssignObjectMixin, View):
    template_name = "fleet/vehicle_allocation_details.html" 
    def get(self, request, id=None, *args, **kwargs):
        context = {'object': self.get_object()}
        return render(request, self.template_name, context)


class FinalizeTrip(AssignObjectMixin, PassRequestMixin, SuccessMessageMixin, CreateView):
    template_name = 'fleet/finalize_trip.html'
    template_name1 = 'fleet/finalized_trip_details.html'
    def get(self, request,  *args, **kwargs):
        context = {}
        obj = self.get_object()
        if obj is not None:
            form = FinalizeTripModelForm(instance=obj)
            context['object'] = obj
            context['form'] = form

        return render(request, self.template_name, context)


    def post(self, request,  *args, **kwargs):
        
        form = FinalizeTripModelForm(request.POST)
        if form.is_valid():
            if not self.request.is_ajax() or self.request.POST.get('asyncUpdate') == 'True':
                form.save(commit=False)
            else:
                form.save(commit=True)
            
        context = {}

        obj = self.get_object()
        if obj is not None:
            form = FinalizeTripModelForm(instance=obj)
            context['object'] = obj
            context['form'] = form
            context['finalize'] = Release.objects.filter (request_no=obj.request_no)

        return render(request, self.template_name1, context)

class ReleaseObjectMixin(object):
    model = Release
    def get_object(self):
        id = self.kwargs.get('id')
        obj = None
        if id is not None:
            obj = get_object_or_404(self.model, id=id)
        return obj 



class UpdateTripFinalization(ReleaseObjectMixin, View):
    template_name = "fleet/update_finalize_trip.html" 
    template_name1 = "fleet/finalized_trip_details2.html" 
    
    def get(self, request, id=None, *args, **kwargs):
        # GET method
        context = {}
        obj = self.get_object()
        if obj is not None:
            form = FinalizeTripModelForm(instance=obj)
            context['object'] = obj
            context['form'] = form
        return render(request, self.template_name, context)

    def post(self, request, id=None,  *args, **kwargs):
        # POST method
        context = {}
        obj = self.get_object()
        if obj is not None:
            form = FinalizeTripModelForm(request.POST or None, instance=obj)
            if form.is_valid():
                form.save()
            context['object'] = obj
            context['form'] = form
            context['issue'] = Assign.objects.filter (request_no=obj.request_no)
        messages.success(request, ('Vehicle Assignment Update Successful'))
        return render(request, self.template_name1, context)


class TripHistoryList(ListView):
    template_name = "fleet/trip_history.html"
    context_object_name = 'object'

    def get_queryset(self):
        return Assign.objects.all()
        

    def get_context_data(self, **kwargs):
        obj = super(TripHistoryList, self).get_context_data(**kwargs)
        obj['trip_history_qs'] = Assign.objects.all()
        return obj


class TripHistory(AssignObjectMixin, View):
    template_name = "fleet/trip_history_details.html" 

    def get(self, request, id=None,  *args, **kwargs):
        context = {}
        obj = self.get_object()
        if obj is not None:
            
            context['object'] = obj
            context['release'] = Release.objects.filter (request_no=obj.request_no)
        return render(request, self.template_name, context)



class FuelingRecordView(PassRequestMixin, SuccessMessageMixin, CreateView):
    template_name = 'fleet/record_fueling.html'
    form_class = FuelingModelForm
    success_message = 'Fueling Records Entered Successfully.'

    success_url = reverse_lazy('fleet:fueling_list')


class FuelingListView(ListView):
    template_name = "fleet/fueling_list.html"
    context_object_name = 'object'

    def get_queryset(self):
        return Fueling.objects.all()
        

    def get_context_data(self, **kwargs):
        obj = super(FuelingListView, self).get_context_data(**kwargs)
        obj['fueling_qs'] = Fueling.objects.all()
        return obj


class FuelingDetailView(DetailView):
    template_name = "fleet/fueling_detail.html"
    model = Fueling


class FuelingUpdateView(PassRequestMixin, SuccessMessageMixin, UpdateView):
    model = Fueling
    template_name = 'fleet/update_fueling_record.html'
    form_class = FuelingModelForm
    success_message = 'Success: Fueling Details Successfully Updated.'
    success_url = reverse_lazy('fleet:fueling_list')


class RepairsRecordView(PassRequestMixin, SuccessMessageMixin, CreateView):
    template_name = 'fleet/record_repairs.html'
    form_class = RepairsModelForm
    success_message = 'Repairs Records Entered Successfully.'

    success_url = reverse_lazy('fleet:repairs_list')

class RepairsListView(ListView):
    template_name = "fleet/repairs_list.html"
    context_object_name = 'object'

    def get_queryset(self):
        return Repair.objects.all()
        

    def get_context_data(self, **kwargs):
        obj = super(RepairsListView, self).get_context_data(**kwargs)
        obj['repairs_qs'] = Repair.objects.all()
        return obj

class RepairsDetailView(DetailView):
    template_name = "fleet/repairs_detail.html"
    model = Repair


class RepairsUpdateView(PassRequestMixin, SuccessMessageMixin, UpdateView):
    model = Repair
    template_name = 'fleet/update_repair_records.html'
    form_class = RepairsModelForm
    success_message = 'Success: Repairs Details Successfully Updated.'
    success_url = reverse_lazy('fleet:repairs_list')


    
    
class ScheduleMaintenance(SuccessMessageMixin, CreateView):
    template_name = 'fleet/schedule_maintenance2.html'
    form_class = ScheduleModelForm
    success_message = 'Vehicle Maintenance Scheduled Successfully.'

    success_url = reverse_lazy('fleet:schedule_list')

class ScheduleListView(ListView):
    template_name = "fleet/schedule_list.html"
    context_object_name = 'object'

    def get_queryset(self):
        return Schedule.objects.all()
        

    def get_context_data(self, **kwargs):
        obj = super(ScheduleListView, self).get_context_data(**kwargs)
        obj['schedule_qs'] = Schedule.objects.filter(schedule_status=1)
        return obj
        
class ScheduleDetailView(DetailView):
    template_name = "fleet/schedule_details.html"
    model = Schedule


class ScheduleUpdateView(SuccessMessageMixin, UpdateView):
    model = Schedule
    template_name = 'fleet/update_maintenance_schedule2.html'
    form_class = ScheduleModelForm
    success_message = 'Success: Schedule Details Successfully Updated.'
    success_url = reverse_lazy('fleet:schedule_list')




class ScheduleObjectMixin(object):
    model = Schedule
    def get_object(self):
        id = self.kwargs.get('id')
        obj = None
        if id is not None:
            obj = get_object_or_404(self.model, id=id)
        return obj 



class RecordMaintenance(ScheduleObjectMixin, View):
    template_name = 'fleet/record_maintenance.html'
    template_name1 = 'fleet/maintenance_details.html'
    def get(self, request,  *args, **kwargs):
        context = {}
        obj = self.get_object()
        if obj is not None:
            form = RecordMaintenanceModelForm(instance=obj)
            context['object'] = obj
            context['form'] = form

        return render(request, self.template_name, context)

    def post(self, request,  *args, **kwargs):
        form = RecordMaintenanceModelForm(request.POST)
        if form.is_valid():
            form.save()

        context = {}
        obj = self.get_object()
        if obj is not None:
          
           context['object'] = obj
           context['form'] = form 
           context['schedule'] = Maintenance.objects.filter (schedule_no=obj.schedule_no)
        
        return render(request, self.template_name1, context)
     
    



class MaintenanceObjectMixin(object):
    model = Maintenance
    def get_object(self):
        id = self.kwargs.get('id')
        obj = None
        if id is not None:
            obj = get_object_or_404(self.model, id=id)
        return obj 

class UpdateMaintenance(MaintenanceObjectMixin, SuccessMessageMixin, View):
    template_name = "fleet/update_maintenance.html" 
    template_name1 = "fleet/maintenance_detail.html" 
    
    def get(self, request, id=None, *args, **kwargs):
        # GET method
        context = {}
        obj = self.get_object()
        if obj is not None:
            form = RecordMaintenanceModelForm(instance=obj)
            context['object'] = obj
            context['form'] = form
        return render(request, self.template_name, context)

    def post(self, request, id=None,  *args, **kwargs):
        # POST method
        context = {}
        obj = self.get_object()
        if obj is not None:
            form = RecordMaintenanceModelForm(request.POST or None, instance=obj)
            if form.is_valid():
                form.save()
            context['object'] = obj
            context['form'] = form
            context['schedule'] = Maintenance.objects.filter (schedule_no=obj.schedule_no)
        messages.success(request, ('Maintenance Details Successfully Updated'))
        return render(request, self.template_name1, context)


class MaintenanceList(SuccessMessageMixin, ListView):
    template_name = "fleet/maintenance_list.html"
    context_object_name = 'object'

    def get_queryset(self):
        return Maintenance.objects.all()
        

    def get_context_data(self, **kwargs):
        obj = super(MaintenanceList, self).get_context_data(**kwargs)
        obj['maintenance_qs'] = Maintenance.objects.all()
        return obj


class MaintenanceDetailView(DetailView):
    template_name = "fleet/maintenance_detail.html"
    model = Maintenance
