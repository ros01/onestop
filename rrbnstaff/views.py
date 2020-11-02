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
from .forms import RequisitionModelForm
from bootstrap_modal_forms.generic import BSModalCreateView
from .models import Requisition
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





    
class RequisitionsListView(ListView):
    template_name = "rrbnstaff/requisition_list2.html"
    context_object_name = 'object'

    def get_queryset(self):
        return Requisition.objects.all()
        

    def get_context_data(self, **kwargs):
        obj = super(RequisitionsListView, self).get_context_data(**kwargs)
        obj['requisition_qs'] = Requisition.objects.order_by('-requisition_date')
        return obj

class RequisitionObjectMixin(object):
    model = Requisition
    def get_object(self):
        id = self.kwargs.get('id')
        obj = None
        if id is not None:
            obj = get_object_or_404(self.model, id=id)
        return obj 




#class RequisitionCreateView(View):
    #template_name = 'rrbnstaff/create_requisition.html'
    #template_name1 = 'rrbnstaff/requisition_detail.html'
    #def get(self, request,  *args, **kwargs):
        #context = {}
        #form = RequisitionModelForm()
        #context['form'] = form

        #return render(request, self.template_name, context)

    #def post(self, request,  *args, **kwargs):
        #form = RequisitionModelForm(request.POST)
        #if form.is_valid():
            #form.save()
        #context = {}
        #context["object"] = Requisition.objects.all()
        #return render(request, self.template_name1, context)


    
class RequisitionDetailView(RequisitionObjectMixin, View):
    template_name = "rrbnstaff/requisition_detail.html"

    def get(self, request, id=None, *args, **kwargs):
        context = {'object': self.get_object()}
        return render(request, self.template_name, context)



class RequisitionUpdateView(PassRequestMixin, SuccessMessageMixin, UpdateView):
    model = Requisition
    template_name = 'rrbnstaff/requisition_update.html'
    form_class = RequisitionModelForm
    success_message = 'Success: Requisition updated Successfully'
    success_url = reverse_lazy('rrbnstaff:requisition_list')


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




