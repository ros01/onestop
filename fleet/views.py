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
from .models import Station, Workshop, Category, Vehicle, Assign, Release, Fueling, Repair, Maintenance, Schedule, Refill
from rrbnstaff.models import Request

from .forms import WorkshopModelForm, StationModelForm, CategoryModelForm, VehicleModelForm, IssueVehicleRequestModelForm, FinalizeTripModelForm, FuelingModelForm, RepairsModelForm, ScheduleModelForm, RecordMaintenanceModelForm, RefillModelForm
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



# Create your views here.




class DashboardTemplateView(LoginRequiredMixin, TemplateView):
    template_name = "fleet/fleet_dashboard.html"

    
    def get_context_data(self, *args, **kwargs):
        context = super(DashboardTemplateView, self).get_context_data(*args, **kwargs)
        #this_month = (dt.datetime.now() + dt.timedelta(days=30))
        #startdate = datetime.today()
        #enddate = startdate + dt.timedelta(days=30)
        context['vass'] = Assign.objects.all()
        #context['vassmnth'] = Assign.objects.filter(approved_date__range=[startdate, enddate])
        context['vreq_pend'] = Request.objects.filter(request_status=1)
        #context['vreq_pend_mnth'] = Request.objects.filter(request_date__lte=this_month, request_status=1)
        context['sch_pend'] = Schedule.objects.filter(schedule_status=1)
        #context['sch_pend_mnth'] = Schedule.objects.filter(scheduled_on__lte=this_month, schedule_status=1)
        context['rep'] = Repair.objects.all()
        #context['rep_mnth'] = Repair.objects.filter(repair_date__lt=this_month)
        return context

        


@login_required
def retrieve_station(request):
    return render(request, 'fleet/retrieve_station.html')

@login_required
def restock(request):
    try:
        query = request.GET.get('q')
        object = 0

    except ValueError:
        query = None
        object = None
    try:
        object = Station.objects.get(
            Q(station_name=query) | Q(station_name__icontains=query)
        )

    except ObjectDoesNotExist:
        messages.error(request, ('Station Name is Invalid.  Enter a Valid Station'))
        pass

    return render(request, 'fleet/results.html', {"object": object})

class VehicleListView(LoginRequiredMixin, ListView):
    template_name = "fleet/vehicle_list2.html"
    context_object_name = 'object'
    redirect_field_name = 'redirect_to'

    def get_queryset(self):
        return Vehicle.objects.all()
        

    def get_context_data(self, **kwargs):
        obj = super(VehicleListView, self).get_context_data(**kwargs)
        obj['vehicle_qs'] = Vehicle.objects.order_by('-date_created')
        return obj

@login_required
def view_vehicle (request, id):
  vehicle = get_object_or_404(Vehicle, pk=id)
  context={'vehicle': vehicle,       
           }
  return render(request, 'fleet/view_vehicle_details.html', context)

@login_required
def lock_vehicle (request, id):
  if request.method == 'POST':
     vehicle = get_object_or_404(Vehicle, pk=id)
     vehicle.interstate_trip = 'local'
     vehicle.save()

     context = {}
     context['object'] = vehicle
     messages.success(request, ('Vehicle Locked Successfully. Please Remember to unlock vehicle after road worthiness confirmation'))
     return render(request, 'fleet/lock_vehicle_details.html', context)

@login_required
def unlock_vehicle (request, id):
  if request.method == 'POST':
     vehicle = get_object_or_404(Vehicle, pk=id)
     vehicle.interstate_trip = 'interstate'
     vehicle.save()

     context = {}
     context['object'] = vehicle
     messages.success(request, ('Vehicle Unlocked Successfully. Vehicle is now available for Interstate Trips'))
     return render(request, 'fleet/lock_vehicle_details.html', context)




#def maintenance_records(request):
    #error = False
    #if 'q1' and 'q2'in request.GET:
        #q1 = request.GET['q1']
        #q2 = request.GET['q2']
        #if not q1:
            #error = True
        #elif not q2:
            #error = True
        #else:
            #searchresult = Maintenance.objects.filter(maintenance_date__range=(q1,q2))
            #return render(request, 'fleet/maintenance_records.html',
                #{"maintenance_qs": searchresult})

    #maintenance_list = Maintenance.objects.all()
    #return render(request, 'fleet/maintenance_records.html', {'error': error})

def maintenance_records(request):
    maintenance_list = Maintenance.objects.all()
    error = False
    if 'q1' and 'q2'in request.GET:
        q1 = request.GET.get('q1')
        q2 = request.GET.get('q2')
        if not q1:
            error = True
        elif not q2:
            error = True
        else:

            searchresult = Maintenance.objects.filter(maintenance_date__range=(q1,q2))
            
            return render(request, 'fleet/maintenance_records.html', {
                'maintenance_qs': searchresult})
    return render(request, 'fleet/maintenance_records.html', {'error': error})

def maintenance_records_pdf(request):
    maintenance_list = Maintenance.objects.all()
    q1 = request.GET.get('q1')
    q2 = request.GET.get('q2')
    
    searchresult = Maintenance.objects.filter(maintenance_date__range=(q1,q2))


    response = HttpResponse(content_type="application/pdf")
    response['Content-Inline'] = 'attachment; filename=maintenance_records.pdf'.format()

    html = render_to_string('fleet/maintenance_list_pdf.html', {
        'maintenance_qs':searchresult,
        'q1': q1,
        'q2': q2,})

    font_config = FontConfiguration()
    HTML(string=html).write_pdf(response, font_config=font_config)

    return response

#def maintenance_records(request):
    #if request.method == 'POST':
        #fromdate=request.POST.get('fromdate')
        #todate=request.POST.get('todate')
        #searchresult = Maintenance.objects.all(where)
        #return render (request, 'fleet/maintenance_records.html', {"maintenance_qs": searchresult})
    #else:
        #maintenance_list = Maintenance.objects.all()
        #return render (request, 'fleet/maintenance_records.html', {"maintenance_qs": maintenance_list})


class MaintenanceList(LoginRequiredMixin, SuccessMessageMixin, ListView):
    template_name = "fleet/maintenance_list.html"
    context_object_name = 'object'

    def get_queryset(self):
        return Maintenance.objects.all()
     
    def get_context_data(self, **kwargs):
        obj = super(MaintenanceList, self).get_context_data(**kwargs)
        obj['maintenance_qs'] = Maintenance.objects.all()
        return obj





def export_csv(request):
    response = HttpResponse(content_type = 'text/csv')
    writer = csv.writer(response)
    writer.writerow (['Schedule No', 'Vehicle Name', 'Mainteance Details', 'Maintenance Cost', 'Workshop', 'Current Mileage', 'Maintenance Date'])
    maintenance_list = Maintenance.objects.all()

    for maintenance in maintenance_list:
        writer.writerow([maintenance.schedule_no, maintenance.vehicle, maintenance.maintenance_details, maintenance.maintenance_cost, maintenance.workshop, maintenance.current_mileage, maintenance.maintenance_date])

    #response['Content-Dispositon'] = 'attachment; filename = maintenance_report' + str(datetime.datetime.now()) + '.csv'
    #response['Content-Dispositon'] = 'attachment; filename="maintenance_report.csv"'
    response['Content-Disposition'] = 'attachment; filename="vehicle_maintenance_report.csv"'
    return response

def export_excel(request):
    maintenance_list = Maintenance.objects.all()
    response = HttpResponse(content_type ='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename = maintenance_report' + str(datetime.datetime.now()) + '.xls'
    wb = xlwt.Workbook(encoding='utf-8')
    ws=wb.add_sheet('Maintenance')
    row_num = 0
    font_style = xlwt.XFStyle()
    font_style.font.bold = True
    columns = ['Schedule No', 'Vehicle Name', 'Mainteance Details', 'Maintenance Cost', 'Workshop', 'Current Mileage', 'Maintenance Date']
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)
    font_style = xlwt.XFStyle()

    #rows = Maintenance.objects.all().values_list('schedule_no', 'vehicle', 'maintenance_details', 'maintenance_cost', 'workshop', 'current_mileage', 'maintenance_date')
    for maintenance in maintenance_list:
        row_num +=1
        row = [
            maintenance.schedule_no,
            maintenance.vehicle,
            maintenance.maintenance_details,
            maintenance.maintenance_cost,
            maintenance.workshop,
            maintenance.current_mileage,
            maintenance.maintenance_date,
        ]

        for col_num in range(len(row)):
            ws.write(row_num, col_num, str(row[col_num]), font_style)

    wb.save(response)

    return response


def export_pdf(request):
    response = HttpResponse(content_type = 'application/pdf')
    response['Content-Dispositon'] = 'inline: attachment; filename = maintenance_report' + str(datetime.datetime.now()) + '.pdf'
    response['Content-Transfer-Encoding'] = 'binary'

    maintenance_list = Maintenance.objects.all()
    
    #sum = maintenance_list.aggregate(Sum['amount'])

    html_string=render_to_string('fleet/maintenance_list_pdf.html',{'maintenance_qs':maintenance_list})
    html = HTML(string=html_string)
    result = html.write_pdf()

    with tempfile.NamedTemporaryFile(delete=True) as output:
        output.write(result)
        output.flush()

        output = open(output.name, 'rb')
        response.write(output.read())

    return response

    writer.writerow (['Schedule No', 'Vehicle Name', 'Mainteance Details', 'Maintenance Cost', 'Workshop', 'Current Mileage', 'Maintenance Date'])
    
    maintenance_list = Maintenance.objects.all()
    for maintenance in maintenance_list:
        writer.writerow([maintenance.schedule_no, maintenance.vehicle, maintenance.maintenance_details, maintenance.maintenance_cost, maintenance.workshop, maintenance.current_mileage, maintenance.maintenance_date])
        return response

class StationObjectMixin(object):
    model = Station
    def get_object(self):
        id = self.kwargs.get('id')
        obj = None
        if id is not None:
            obj = get_object_or_404(self.model, id=id)
        return obj  


class RestockStationCredit(LoginRequiredMixin, StationObjectMixin, View):
    template_name = "fleet/refill_station_credit.html"
    template_name1 = "fleet/refill_station_credit_details.html"
    
    def get(self, request,  *args, **kwargs):
        context = {}
        obj = self.get_object()
        if obj is not None:
            form = RefillModelForm(instance=obj)
            context['object'] = obj
            context['form'] = form

        return render(request, self.template_name, context)



    def post(self, request,  *args, **kwargs):
        form = RefillModelForm(request.POST)
        if form.is_valid():
            if not self.request.is_ajax() or self.request.POST.get('asyncUpdate') == 'True':
                form.save(commit=False)
            else:
                restock = form.save(commit=False)
                restock.station_credit += Decimal(request.POST['refill_credit_value'])
                restock.save()

        context = {}

        obj = self.get_object()
        if obj is not None:
            form = RefillModelForm(instance=obj)
            context['object'] = obj
            context['form'] = form
            context['refill'] = Refill.objects.filter (station_name=obj.station_name, refill_no= request.POST['refill_no'])

        return render(request, self.template_name1, context)


class StationCreditRestockList(LoginRequiredMixin, ListView):
    template_name = "fleet/restock_list.html"
    context_object_name = 'object'

    def get_queryset(self):
        return Refill.objects.all()
        

    def get_context_data(self, **kwargs):
        obj = super(StationCreditRestockList, self).get_context_data(**kwargs)
        obj['restock_qs'] = Refill.objects.order_by('-refill_on')
        return obj


class StationCreditRestockDetails(LoginRequiredMixin, DetailView):
    template_name = "fleet/restock_station_credit_details.html"
    model = Refill




class WorkshopCreateView(LoginRequiredMixin, PassRequestMixin, SuccessMessageMixin, CreateView):
    template_name = 'fleet/create_workshop.html'
    form_class = WorkshopModelForm
    success_message = 'Workshop created Successfully.'

    success_url = reverse_lazy('fleet:workshop_list')


class StationCreateView(LoginRequiredMixin, PassRequestMixin, SuccessMessageMixin, CreateView):
    template_name = 'fleet/create_station.html'
    form_class = StationModelForm
    success_message = 'Station created Successfully.'

    success_url = reverse_lazy('fleet:station_list')


class CategoryCreateView(LoginRequiredMixin, PassRequestMixin, SuccessMessageMixin, CreateView):
    template_name = 'fleet/create_category.html'
    form_class = CategoryModelForm
    success_message = 'category created Successfully.'

    success_url = reverse_lazy('fleet:category_list')

class VehicleCreateView(LoginRequiredMixin, PassRequestMixin, SuccessMessageMixin, CreateView):
    template_name = 'fleet/create_vehicle.html'
    form_class = VehicleModelForm
    success_message = 'Vehicle created Successfully.'

    success_url = reverse_lazy('fleet:vehicle_list')


class WorkshopListView(LoginRequiredMixin, ListView):
    template_name = "fleet/workshop_list.html"
    context_object_name = 'object'
    redirect_field_name = 'redirect_to'

    def get_queryset(self):
        return Workshop.objects.all()
        
    def get_context_data(self, **kwargs):
        obj = super(WorkshopListView, self).get_context_data(**kwargs)
        obj['workshop_qs'] = Workshop.objects.order_by('-date_created')
        return obj


class StationListView(LoginRequiredMixin, ListView):
    template_name = "fleet/station_list.html"
    context_object_name = 'object'

    def get_queryset(self):
        return Station.objects.all()
        
    def get_context_data(self, **kwargs):
        obj = super(StationListView, self).get_context_data(**kwargs)
        obj['station_qs'] = Station.objects.order_by('-date_created')
        return obj

class CategoryListView(LoginRequiredMixin, ListView):
    template_name = "fleet/category_list.html"
    context_object_name = 'object'

    def get_queryset(self):
        return Category.objects.all()
        
    def get_context_data(self, **kwargs):
        obj = super(CategoryListView, self).get_context_data(**kwargs)
        obj['category_qs'] = Category.objects.order_by('-date_created')
        return obj

class WorkshopDetailView(LoginRequiredMixin, DetailView):
    template_name = "fleet/workshop_detail.html"
    model = Workshop


class StationDetailView(LoginRequiredMixin, DetailView):
    template_name = "fleet/station_detail.html"
    model = Station


class CategoryDetailView(LoginRequiredMixin, DetailView):
    template_name = "fleet/category_detail.html"
    model = Category

class VehicleDetailView(LoginRequiredMixin,DetailView):
    template_name = "fleet/vehicle_detail.html"
    model = Vehicle

#class VehicleRequestDetail(DetailView):
    #template_name = "fleet/vehicle_request_detail.html"
    #model = Request 

class VehicleRequestList(LoginRequiredMixin, ListView):
    template_name = "fleet/vehicle_request_list.html"
    context_object_name = 'object'

    def get_queryset(self):
        return Request.objects.order_by('-request_date')
        
    def get_context_data(self, **kwargs):
        obj = super(VehicleRequestList, self).get_context_data(**kwargs)
        obj['request_qs'] = Request.objects.filter(request_status=1)
        return obj

class RequestObjectMixin(object):
    model = Request
    def get_object(self):
        id = self.kwargs.get('id')
        obj = None
        if id is not None:
            obj = get_object_or_404(self.model, id=id)
        return obj 


class VehicleRequestDetail(LoginRequiredMixin, RequestObjectMixin, View):
    template_name = "fleet/vehicle_request_detail.html" 
    def get(self, request, id=None, *args, **kwargs):
        context = {'object': self.get_object()}
        return render(request, self.template_name, context)

class WorkshopUpdateView(LoginRequiredMixin, PassRequestMixin, SuccessMessageMixin, UpdateView):
    model = Workshop
    template_name = 'fleet/update_workshop.html'
    form_class = WorkshopModelForm
    success_message = 'Success: Workshop Details were updated.'
    success_url = reverse_lazy('fleet:workshop_list')

class StationUpdateView(LoginRequiredMixin, PassRequestMixin, SuccessMessageMixin, UpdateView):
    model = Station
    template_name = 'fleet/update_station.html'
    form_class = StationModelForm
    success_message = 'Success: Station Details were updated.'
    success_url = reverse_lazy('fleet:station_list')


class CategoryUpdateView(LoginRequiredMixin, PassRequestMixin, SuccessMessageMixin, UpdateView):
    model = Category
    template_name = 'fleet/update_category.html'
    form_class = CategoryModelForm
    success_message = 'Success: Category Details were updated.'
    success_url = reverse_lazy('fleet:category_list')

class VehicleUpdateView(LoginRequiredMixin, PassRequestMixin, SuccessMessageMixin, UpdateView):
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

class WorkshopDeleteView(LoginRequiredMixin, WorkshopObjectMixin, View):
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


class VehicleDeleteView(LoginRequiredMixin, VehicleObjectMixin, View):
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

class StationDeleteView(LoginRequiredMixin, StationObjectMixin, View):
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

class CategoryDeleteView(LoginRequiredMixin, CategoryObjectMixin, View):
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

class IssueVehicleRequest(LoginRequiredMixin, RequestObjectMixin, PassRequestMixin, SuccessMessageMixin, CreateView):
    template_name = 'fleet/assign_vehicle2.html'
    form_class = IssueVehicleRequestModelForm
    success_message = 'Vehicle request issued successfully'
    success_url = reverse_lazy('fleet:vehicle_assignment_list') 

    def get_context_data(self, *args, **kwargs):
        context = super(IssueVehicleRequest, self).get_context_data(**kwargs)
        context = {}
        obj = self.get_object()
        if obj is not None:
            form = IssueVehicleRequestModelForm(instance=obj)
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

class AssignObjectMixin(object):
    model = Assign
    def get_object(self):
        id = self.kwargs.get('id')
        obj = None
        if id is not None:
            obj = get_object_or_404(self.model, id=id)
        return obj 

class UpdateVehicleAssignemt(LoginRequiredMixin, AssignObjectMixin, View):
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

class VehicleAssignmentList(LoginRequiredMixin, ListView):
    template_name = "fleet/assigned_vehicles_list2.html"
    context_object_name = 'object'

    def get_queryset(self):
        return Assign.objects.all()
        
    def get_context_data(self, **kwargs):
        obj = super(VehicleAssignmentList, self).get_context_data(**kwargs)
        obj['vehicle_assignment_qs'] = Assign.objects.filter(trip_status="created")
        return obj

class VehicleAllocationsDetail(LoginRequiredMixin, AssignObjectMixin, View):
    template_name = "fleet/vehicle_allocation_details.html" 
    def get(self, request, id=None, *args, **kwargs):
        context = {'object': self.get_object()}
        return render(request, self.template_name, context)

class FinalizeTrip(LoginRequiredMixin, AssignObjectMixin, PassRequestMixin, SuccessMessageMixin, CreateView):
    template_name = 'fleet/finalize_trip.html'
    form_class = FinalizeTripModelForm
    success_message = 'Vehicle release successfull'
    success_url = reverse_lazy('fleet:trip_history') 

    def get_context_data(self, *args, **kwargs):
        context = super(FinalizeTrip, self).get_context_data(**kwargs)
        context = {}
        obj = self.get_object()
        if obj is not None:
            form = FinalizeTripModelForm(instance=obj)
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


class ReleaseObjectMixin(object):
    model = Release
    def get_object(self):
        id = self.kwargs.get('id')
        obj = None
        if id is not None:
            obj = get_object_or_404(self.model, id=id)
        return obj 


class UpdateTripFinalization(LoginRequiredMixin, ReleaseObjectMixin, View):
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

class TripHistoryList(LoginRequiredMixin, ReleaseObjectMixin, ListView):
    template_name = "fleet/trip_history.html"
    context_object_name = 'object'
    queryset = Release.objects.all()
       
    def get_context_data(self, **kwargs):
        context = super(TripHistoryList, self).get_context_data(**kwargs)
        context['trip_qs'] = self.queryset
        obj = self.get_object()
        if obj is not None:    
            context['trip_qs'] = obj
        return context

class TripHistory(LoginRequiredMixin, ReleaseObjectMixin, View):
    template_name = "fleet/trip_history_details.html" 

    def get(self, request, id=None,  *args, **kwargs):
        context = {}
        obj = self.get_object()
        if obj is not None:
            
            context['object'] = obj
            context['assign'] = Assign.objects.filter (request_no=obj.request_no)
        return render(request, self.template_name, context)

class FuelingRecordView(LoginRequiredMixin, PassRequestMixin, SuccessMessageMixin, CreateView):
    template_name = 'fleet/record_fueling.html'
    form_class = FuelingModelForm
    success_message = 'Fueling Records Entered Successfully.'
    success_url = reverse_lazy('fleet:fueling_list')


class FuelingListView(LoginRequiredMixin, ListView):
    template_name = "fleet/fueling_list.html"
    context_object_name = 'object'

    def get_queryset(self):
        return Fueling.objects.all()
        
    def get_context_data(self, **kwargs):
        obj = super(FuelingListView, self).get_context_data(**kwargs)
        obj['fueling_qs'] = Fueling.objects.all()
        return obj

class FuelingDetailView(LoginRequiredMixin, DetailView):
    template_name = "fleet/fueling_detail.html"
    model = Fueling


class FuelingUpdateView(LoginRequiredMixin, PassRequestMixin, SuccessMessageMixin, UpdateView):
    model = Fueling
    template_name = 'fleet/update_fueling_record.html'
    form_class = FuelingModelForm
    success_message = 'Success: Fueling Details Successfully Updated.'
    success_url = reverse_lazy('fleet:fueling_list')

class RepairsRecordView(LoginRequiredMixin, PassRequestMixin, SuccessMessageMixin, CreateView):
    template_name = 'fleet/record_repairs.html'
    form_class = RepairsModelForm
    success_message = 'Repairs Records Entered Successfully.'

    success_url = reverse_lazy('fleet:repairs_list')

class RepairsListView(LoginRequiredMixin, ListView):
    template_name = "fleet/repairs_list.html"
    context_object_name = 'object'

    def get_queryset(self):
        return Repair.objects.all()
        
    def get_context_data(self, **kwargs):
        obj = super(RepairsListView, self).get_context_data(**kwargs)
        obj['repairs_qs'] = Repair.objects.all()
        return obj

class RepairsDetailView(LoginRequiredMixin, DetailView):
    template_name = "fleet/repairs_detail.html"
    model = Repair


class RepairsUpdateView(LoginRequiredMixin, PassRequestMixin, SuccessMessageMixin, UpdateView):
    model = Repair
    template_name = 'fleet/update_repair_records.html'
    form_class = RepairsModelForm
    success_message = 'Repairs Details Successfully Updated.'
    success_url = reverse_lazy('fleet:repairs_list')

    
class ScheduleMaintenance(LoginRequiredMixin, PassRequestMixin, SuccessMessageMixin, CreateView):
    template_name = 'fleet/schedule_maintenance.html'
    form_class = ScheduleModelForm
    success_message = 'Vehicle Maintenance Scheduled Successfully.'

    success_url = reverse_lazy('fleet:schedule_list')

class ScheduleListView(LoginRequiredMixin, ListView):
    template_name = "fleet/schedule_list2.html"
    context_object_name = 'object'

    def get_queryset(self):
        return Schedule.objects.all()
        
    def get_context_data(self, **kwargs):
        obj = super(ScheduleListView, self).get_context_data(**kwargs)
        obj['schedule_qs'] = Schedule.objects.filter(schedule_status=1)
        return obj
        
class ScheduleDetailView(LoginRequiredMixin, DetailView):
    template_name = "fleet/schedule_details.html"
    model = Schedule


class ScheduleUpdateView(LoginRequiredMixin, PassRequestMixin, SuccessMessageMixin, UpdateView):
    model = Schedule
    template_name = 'fleet/update_maintenance_schedule.html'
    form_class = ScheduleModelForm
    success_message = 'Schedule Details Successfully Updated.'
    success_url = reverse_lazy('fleet:schedule_list')


class ScheduleObjectMixin(object):
    model = Schedule
    def get_object(self):
        id = self.kwargs.get('id')
        obj = None
        if id is not None:
            obj = get_object_or_404(self.model, id=id)
        return obj 

#class RecordMaintenance(LoginRequiredMixin, ScheduleObjectMixin, PassRequestMixin, SuccessMessageMixin, CreateView):
    #template_name = 'fleet/record_maintenance2.html'
    #template_name1 = 'fleet/maintenance_details.html'
    #def get(self, request,  *args, **kwargs):
        #context = {}
        #obj = self.get_object()
        #if obj is not None:
            #form = RecordMaintenanceModelForm(instance=obj)
            #context['object'] = obj
            #context['form'] = form

        #return render(request, self.template_name, context)

    #def post(self, request,  *args, **kwargs):
        #form = RecordMaintenanceModelForm(request.POST)
        #if form.is_valid():
            #if not self.request.is_ajax() or self.request.POST.get('asyncUpdate') == 'True':
                #form.save(commit=False)
            #else:
                #form.save(commit=True)

        #context = {}
        #obj = self.get_object()
        #if obj is not None:
          
           #context['object'] = obj
           #context['form'] = form 
           #context['schedule'] = Maintenance.objects.filter (schedule_no=obj.schedule_no)
        
        #return render(request, self.template_name1, context)


class RecordMaintenance(LoginRequiredMixin, ScheduleObjectMixin, PassRequestMixin, SuccessMessageMixin, CreateView):
    template_name = 'fleet/record_maintenance2.html'
    form_class = RecordMaintenanceModelForm
    success_message = 'Vehicle Maintenance Records entered successfully.'
    success_url = reverse_lazy('fleet:maintenance_list') 

    def get_context_data(self, *args, **kwargs):
        context = super(RecordMaintenance, self).get_context_data(**kwargs)
        context = {}
        obj = self.get_object()
        if obj is not None:
            form = RecordMaintenanceModelForm(instance=obj)
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
    
class MaintenanceObjectMixin(object):
    model = Maintenance
    def get_object(self):
        id = self.kwargs.get('id')
        obj = None
        if id is not None:
            obj = get_object_or_404(self.model, id=id)
        return obj 

#class UpdateMaintenance(LoginRequiredMixin, MaintenanceObjectMixin, SuccessMessageMixin, View):
    #template_name = "fleet/update_maintenance2.html" 
    #template_name1 = "fleet/maintenance_detail.html" 
    
    #def get(self, request, id=None, *args, **kwargs):
        # GET method
        #context = {}
        #obj = self.get_object()
        #if obj is not None:
            #form = RecordMaintenanceModelForm(instance=obj)
            #context['object'] = obj
            #context['form'] = form
        #return render(request, self.template_name, context)

    #def post(self, request, id=None,  *args, **kwargs):
        # POST method
        #context = {}
        #obj = self.get_object()
        #if obj is not None:
            #form = RecordMaintenanceModelForm(request.POST or None, instance=obj)
            #if form.is_valid():
                #form.save()
            #context['object'] = obj
            #context['form'] = form
            #context['schedule'] = Maintenance.objects.filter (schedule_no=obj.schedule_no)
        #messages.success(request, ('Maintenance Details Successfully Updated'))
        #return render(request, self.template_name1, context)

class UpdateMaintenance(LoginRequiredMixin, PassRequestMixin, SuccessMessageMixin, UpdateView):
    model = Maintenance
    template_name = 'fleet/update_maintenance2.html'
    form_class = RecordMaintenanceModelForm
    success_message = 'Maintenance Details Successfully Updated'
    success_url = reverse_lazy('fleet:maintenance_list')


class MaintenanceList(LoginRequiredMixin, SuccessMessageMixin, ListView):
    template_name = "fleet/maintenance_list.html"
    context_object_name = 'object'

    def get_queryset(self):
        return Maintenance.objects.all()
     
    def get_context_data(self, **kwargs):
        obj = super(MaintenanceList, self).get_context_data(**kwargs)
        obj['maintenance_qs'] = Maintenance.objects.all()
        return obj


class MaintenanceDetailView(LoginRequiredMixin, DetailView):
    template_name = "fleet/maintenance_detail.html"
    model = Maintenance
