from django import forms
from django.http import HttpResponse, Http404, HttpResponseRedirect
from .models import Requisition, Request
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field
from django.utils import timezone
from bootstrap_modal_forms.forms import BSModalModelForm, BSModalForm
from bootstrap_modal_forms.mixins import PassRequestMixin, PopRequestMixin, CreateUpdateAjaxMixin


class RequisitionModelForm(PopRequestMixin, CreateUpdateAjaxMixin, forms.ModelForm):

    class Meta:
        model = Requisition
        fields = ('requisition_no', 'item', 'quantity_requested', 'requesting_staff', 'department')


        widgets = {
        'requisition_no': forms.HiddenInput(),
        'requesting_staff': forms.HiddenInput(),
        'department': forms.TextInput(attrs={'readonly': True}),
        
        }

    def __init__(self, *args, **kwargs):
       super(RequisitionModelForm, self).__init__(*args, **kwargs)
       for name in self.fields.keys():
            self.fields[name].widget.attrs.update({
                'class': 'form-control',
            })
       
       self.fields['item'].label = "Item"
       self.fields['quantity_requested'].label = "Quantity Requested"
       self.fields['requesting_staff'].label = "Requesting Staff"
       self.fields['department'].label = "Department"

    def save(self):

      if not self.request.is_ajax():
          instance = super(CreateUpdateAjaxMixin, self).save(commit=True)
          instance.save()
      else:
          instance = super(CreateUpdateAjaxMixin, self).save(commit=False)

      return instance


class RequestModelForm(PopRequestMixin, CreateUpdateAjaxMixin, forms.ModelForm):

    class Meta:
        model = Request
        fields = ('request_no', 'vehicle', 'department', 'request_reason', 'destination', 'request_duration', 'requesting_staff', )


        widgets = {
        'request_no': forms.HiddenInput(),
        'requesting_staff': forms.HiddenInput(),
        'request_reason': forms.Textarea(attrs={'rows':2, 'cols':3}),
        'department': forms.HiddenInput(),
        
        }

    def __init__(self, *args, **kwargs):
       super(RequestModelForm, self).__init__(*args, **kwargs)
       for name in self.fields.keys():
            self.fields[name].widget.attrs.update({
                'class': 'form-control',
            })
       
       self.fields['vehicle'].label = "Vehicle"
       self.fields['request_reason'].label = "Request Reason"
       self.fields['request_reason'].widget.attrs['placeholder'] = "Enter reason for vehicle request"
       self.fields['destination'].label = "Destination"
       self.fields['destination'].widget.attrs['placeholder'] = "Enter Destination"
       self.fields['request_duration'].label = "Trip Duration"
       self.fields['request_duration'].widget.attrs['placeholder'] = "Enter Duration of Trip"
       self.fields['department'].label = "Department"

    def save(self):

      if not self.request.is_ajax():
          instance = super(CreateUpdateAjaxMixin, self).save(commit=True)
          instance.save()
      else:
          instance = super(CreateUpdateAjaxMixin, self).save(commit=False)

      return instance

       