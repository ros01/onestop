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
from .forms import RequisitionModelForm, RequestModelForm
from bootstrap_modal_forms.generic import BSModalCreateView
from .models import Requisition, Request
from store.models import Issue
from fleet.models import Assign
from django.contrib.messages.views import SuccessMessageMixin
from bootstrap_modal_forms.mixins import PassRequestMixin, CreateUpdateAjaxMixin
from django.contrib.auth.models import User
from django.conf import settings



# Create your views here.


class LoginRequiredMixin(object):
    #@classmethod
    #def as_view(cls, **kwargs):
        #view = super(LoginRequiredMixin, cls).as_view(**kwargs)
        #return login_required(view)

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(LoginRequiredMixin, self).dispatch(request, *args, **kwargs)



class DashboardTemplateView(TemplateView):
    template_name = "rrbnstaff/staff_dashboard2.html"
    
    def get_context_data(self, *args, **kwargs):
        context = super(DashboardTemplateView, self).get_context_data(*args, **kwargs)
        #context["inspection"] = Schedule.objects.all()
        return context


class ProfileTemplateView(TemplateView):
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


class RequisitionCreateView(PassRequestMixin, SuccessMessageMixin, CreateView):
    template_name = 'rrbnstaff/create_requisition.html'
    form_class = RequisitionModelForm
    success_message = 'Requisition created successfully.'
    success_url = reverse_lazy('rrbnstaff:requisition_list') 

class CreateVehicleRequest(PassRequestMixin, SuccessMessageMixin, CreateView):
    template_name = 'rrbnstaff/create_vehicle_request.html'
    form_class = RequestModelForm
    success_message = 'Vehicle Request created successfully.'
    success_url = reverse_lazy('rrbnstaff:request_list') 


class RequisitionsListView(ListView):
    template_name = "rrbnstaff/requisition_list2.html"
    context_object_name = 'object'

    def get_queryset(self):
        return Requisition.objects.all()
        

    def get_context_data(self, **kwargs):
        obj = super(RequisitionsListView, self).get_context_data(**kwargs)
        obj['requisition_qs'] = Requisition.objects.filter(requisition_status=1, requesting_staff=self.request.user)
        return obj


class RequestListView(ListView):
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



class RequisitionDetailView(RequisitionObjectMixin, View):
    template_name = "rrbnstaff/requisition_detail.html"

    def get(self, request, id=None, *args, **kwargs):
        context = {'object': self.get_object()}
        return render(request, self.template_name, context)


class VehicleRequestDetailView(DetailView):
    template_name = "fleet/vehicle_detail.html"
    model = Request

class RequisitionUpdateView(PassRequestMixin, SuccessMessageMixin, UpdateView):
    model = Requisition
    template_name = 'rrbnstaff/requisition_update.html'
    form_class = RequisitionModelForm
    success_message = 'Success: Requisition updated Successfully'
    success_url = reverse_lazy('rrbnstaff:requisition_list')


class VehicleRequestUpdateView(PassRequestMixin, SuccessMessageMixin, UpdateView):
    model = Request
    template_name = 'rrbnstaff/update_vehicle_request.html'
    form_class = RequestModelForm
    success_message = 'Success: Vehicle Request updated Successfully'
    success_url = reverse_lazy('rrbnstaff:request_list')


class RequisitionDeleteView(RequisitionObjectMixin, View):
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

class VehicleRequestDeleteView(RequestObjectMixin, View):
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



class MyIssuedRequisitions(ListView):
    template_name = "rrbnstaff/my_issued_requisitions.html"
    context_object_name = 'object'

    def get_queryset(self):
        return Issue.objects.all()
        

    def get_context_data(self, **kwargs):
        obj = super(MyIssuedRequisitions, self).get_context_data(**kwargs)
        obj['issue_qs'] = Issue.objects.filter(requesting_staff=self.request.user)
        return obj 


class MyVehicleAllocations(ListView):
    template_name = "rrbnstaff/my_vehicle_allocations.html"
    context_object_name = 'object'

    def get_queryset(self):
        return Assign.objects.all()
        

    def get_context_data(self, **kwargs):
        obj = super(MyVehicleAllocations, self).get_context_data(**kwargs)
        obj['assign_qs'] = Assign.objects.filter(requesting_staff=self.request.user)
        return obj 


class MyIssuedRequisitionsDetails(DetailView):
    template_name = "rrbnstaff/my_issued_requisitions_details.html"
    model = Issue 

class AssignedVehicleDetails(DetailView):
    template_name = "rrbnstaff/assigned_vehicle_details.html"
    model = Assign



    




